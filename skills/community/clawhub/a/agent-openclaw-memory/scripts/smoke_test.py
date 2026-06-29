"""
smoke_test.py — 管道烟火测试（Phase 4）

D1: 跨 pipeline 抽样校验
D4: 端到端冒烟测试

由 heartbeat 调用。返回 0=通过, 1=告警。
"""
import json, sys, uuid
from pathlib import Path
from datetime import datetime, timezone

WORKSPACE = Path(__file__).parent.parent
SCRIPTS = WORKSPACE / "scripts"
DATA = WORKSPACE / "data"

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
KB_COLLECTION = "knowledge_base"


def check_qdrant():
    """D1: 从 Qdrant 各 pipeline 抽最新 1 条，检查必填字段"""
    import requests

    checks = {
        "compress": {"type": True, "title": True, "narrative_min": 10},
        "vault_sync": {"type": True, "title": True, "text_min": 20},
        "consolidate": {"type": True, "current_state": True},
    }

    results = {}
    for pipeline, fields in checks.items():
        try:
            resp = requests.post(
                f"http://{QDRANT_HOST}:{QDRANT_PORT}/collections/{KB_COLLECTION}/points/scroll",
                json={"limit": 100, "with_payload": True, "with_vector": False},
                timeout=10,
            )
            if resp.status_code != 200:
                results[pipeline] = {"status": "error", "reason": "Qdrant 不可达"}
                continue

            pts = resp.json().get("result", {}).get("points", [])
            match = None
            for pt in pts:
                p = pt.get("payload", {})
                if p.get("pipeline") == pipeline:
                    match = p
                    break

            if not match:
                results[pipeline] = {"status": "ok", "note": "无新条目"}
                continue

            # 检查必填字段
            missing = []
            for f, required in fields.items():
                if f.endswith("_min"):
                    base = f.replace("_min", "")
                    val = match.get(base, "") if base != "narrative_min" else match.get("narrative", "")
                    actual = match.get("narrative" if base == "narrative_min" else base, "")
                    if isinstance(required, int) and len(str(actual)) < required:
                        missing.append(f"{base} 长度 < {required}")
                elif required and not match.get(f):
                    missing.append(f"{f} 为空")

            if missing:
                results[pipeline] = {"status": "fail", "missing": missing}
            else:
                results[pipeline] = {"status": "ok"}

        except Exception as e:
            results[pipeline] = {"status": "error", "reason": str(e)[:100]}

    return results


def smoke_end_to_end():
    """D4: 端到端冒烟——假数据走 parse → compress → quality_gate"""
    import tempfile, subprocess

    sys.path.insert(0, str(SCRIPTS))
    from extract_memories import parse_to_observations

    # 模拟一段 session dump（>=4 条 user:/assistant: 行以触发 session dump 检测）
    fake = """## Conversation Summary
user: 今天决定把日常模型从 Flash 切换到 Pro
assistant: 好的，已切换到 Pro 模型。Pro 在复杂分析任务中显著优于 Flash。
user: 那心跳任务用什么模型
assistant: 心跳和日常维护用 Flash 省成本，分析类任务用 Pro
user: 确认一下 config 改好了吗
assistant: 已改。primary 设为 deepseek-v4-pro，subagents 保持 Flash
"""

    obs = parse_to_observations(fake, "smoke-test")
    if not obs:
        return {"status": "fail", "reason": "parse_to_observations 返回空"}

    tf = tempfile.NamedTemporaryFile(mode="w", suffix=".json", encoding="utf-8", delete=False)
    json.dump(obs, tf)
    tmp_path = tf.name
    tf.close()

    try:
        r = subprocess.run(
            ["python", str(SCRIPTS / "compress.py"), "--input", tmp_path],
            capture_output=True, timeout=30, encoding="utf-8",
        )
        if r.returncode != 0:
            return {"status": "fail", "reason": f"compress.py 返回 {r.returncode}"}

        bracket = r.stdout.find("[")
        cl = json.loads(r.stdout[bracket:]) if bracket >= 0 else []
        if not cl:
            return {"status": "fail", "reason": "compress 返回空列表"}

        from compress import quality_gate

        passed = sum(1 for c in cl if quality_gate(c))
        if passed == 0:
            return {"status": "fail", "reason": "质量闸门拒绝所有条目"}
    finally:
        try:
            Path(tmp_path).unlink()
        except Exception:
            pass

    return {"status": "ok", "observations": len(obs), "compressed": len(cl), "passed": passed}


def main():
    print("=== smoke_test ===")
    alerts = 0

    # D1
    print("\n[D1] 跨管线抽样:")
    results = check_qdrant()
    for pipeline, r in sorted(results.items()):
        icon = "✅" if r["status"] == "ok" else "❌"
        extra = r.get("note", "") or r.get("missing", []) or r.get("reason", "")
        if isinstance(extra, list):
            extra = ", ".join(extra)
        print(f"  {icon} {pipeline}: {r['status']}" + (f" ({extra})" if extra else ""))
        if r["status"] != "ok":
            alerts += 1

    # D4
    print("\n[D4] 端到端冒烟:")
    smoke = smoke_end_to_end()
    icon = "✅" if smoke["status"] == "ok" else "❌"
    extra = smoke.get("reason", "")
    if smoke["status"] == "ok":
        extra = f"{smoke['observations']} obs → {smoke['compressed']} compressed → {smoke['passed']} passed"
    print(f"  {icon} {smoke['status']}" + (f" ({extra})" if extra else ""))
    if smoke["status"] != "ok":
        alerts += 1

    # D5: 关键路径可达性
    print("\n[D5] 关键路径:")
    d5_checks = 0
    from shared_config import VAULT_DIR, LMSTUDIO_EMBED_URL, CONFIG_FILE
    checks = [
        ("openclaw.json", CONFIG_FILE.exists()),
        ("vault 目录", VAULT_DIR.exists()),
        ("scripts/ 目录", (WORKSPACE / "scripts").exists()),
    ]
    for name, ok in checks:
        icon = "✅" if ok else "❌"
        print(f"  {icon} {name}")
        if not ok: alerts += 1; d5_checks += 1

    print(f"\n结果: {3 - alerts}/3 通过, {alerts} 告警")

    # 写快照给 heartbeat_alert 用
    snapshot = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "d1_pipelines": {k: v["status"] for k, v in results.items()},
        "d4_status": smoke["status"],
        "alerts": alerts,
    }
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / "smoke_snapshot.json").write_text(json.dumps(snapshot, ensure_ascii=False), encoding="utf-8")

    return 0 if alerts == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
