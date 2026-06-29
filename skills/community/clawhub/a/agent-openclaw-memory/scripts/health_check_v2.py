"""
health_check_v2.py — 健康巡检 + 自动修复（借鉴不死鸟自愈系统）

检查所有组件状态，匹配抗体库，自动修复或提醒。

用法: python scripts/health_check_v2.py
"""
import _suppress_windows
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(os.environ["USERPROFILE"]) / ".openclaw" / "workspace"
from shared_config import VAULT_DIR
ANTIBODIES_FILE = WORKSPACE / "data" / "antibodies.json"
LMSTUDIO_URL = "LMSTUDIO_MODELS_URL_PLACEHOLDER"
QDRANT_URL = "http://127.0.0.1:6333/collections/knowledge_base"

def load_antibodies():
    if ANTIBODIES_FILE.exists():
        with open(ANTIBODIES_FILE, "r", encoding="utf-8") as f:
            all_abs = json.load(f).get("antibodies", [])
        return [a for a in all_abs if a.get("enabled", True)]
    return []

def save_antibodies(antibodies):
    with open(ANTIBODIES_FILE, "w", encoding="utf-8") as f:
        json.dump({"antibodies": antibodies}, f, ensure_ascii=False, indent=2)

def match_antibody(error_msg, antibodies):
    error_lower = error_msg.lower()
    for ab in antibodies:
        if ab["pattern"].lower() in error_lower:
            return ab
    return None

def record_hit(antibody_name, antibodies):
    for ab in antibodies:
        if ab["name"] == antibody_name:
            ab["hits"] = ab.get("hits", 0) + 1
            break
    save_antibodies(antibodies)

def check_cron_tasks():
    """检查 cron 任务状态（直接读取 cron 存储文件）"""
    issues = []
    try:
        cron_dir = Path(os.environ["USERPROFILE"]) / ".openclaw" / "agents" / "main"
        cron_file = cron_dir / "cron.json"
        if cron_file.exists():
            with open(cron_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            jobs = data if isinstance(data, list) else data.get("jobs", [])
            for job in jobs:
                name = job.get("name", "?")
                state = job.get("state", {})
                if state.get("consecutiveErrors", 0) > 2:
                    issues.append({"component": "cron", "error": f"{name}: {state['consecutiveErrors']} consecutive errors"})
        else:
            # fallback: 尝试 CLI
            try:
                openclaw = Path(os.environ["APPDATA"]) / "npm" / "openclaw.cmd"
                result = subprocess.run(
                    [str(openclaw), "cron", "list"],
                    capture_output=True, text=True, timeout=30,
                    encoding="utf-8", errors="replace"
                )
                if result.returncode != 0:
                    issues.append({"component": "cron", "error": result.stderr[:200]})
            except Exception:
                pass
    except Exception as e:
        issues.append({"component": "cron", "error": str(e)})
    return issues

def check_qdrant():
    """检查 Qdrant 向量库"""
    issues = []
    try:
        req = urllib.request.Request(QDRANT_URL, method="GET")
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())["result"]
        if data["status"] != "green":
            issues.append({"component": "qdrant", "error": f"status={data['status']}"})
        if data["points_count"] < 800:
            issues.append({"component": "qdrant", "error": f"only {data['points_count']} vectors"})
    except Exception as e:
        issues.append({"component": "qdrant", "error": f"Qdrant connection refused: {e}"})
    return issues

def check_lmstudio():
    """检查 LM Studio"""
    issues = []
    try:
        cfg = json.load(open(WORKSPACE.parent / "openclaw.json", encoding="utf-8-sig"))
        key = cfg.get("models", {}).get("providers", {}).get("lmstudio", {}).get("apiKey", "")
        req = urllib.request.Request(LMSTUDIO_URL)
        req.add_header("Authorization", f"Bearer {key}")
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        models = data.get("data", [])
        if len(models) < 2:
            issues.append({"component": "lmstudio", "error": f"only {len(models)} models"})
    except Exception as e:
        issues.append({"component": "lmstudio", "error": f"LM Studio offline: {e}"})
    return issues

def check_vault_watcher():
    """检查 vault_watcher 计划任务"""
    issues = []
    try:
        result = subprocess.run(
            ["powershell", "-Command",
             "(Get-ScheduledTask -TaskName 'OpenClaw-VaultWatcher').State"],
            capture_output=True, text=True, timeout=10,
            encoding="utf-8", errors="replace"
        )
        state = result.stdout.strip()
        if not state:
            issues.append({"component": "vault_watcher", "error": "scheduled task not found"})
        elif state != "Running":
            issues.append({"component": "vault_watcher", "error": f"state={state}"})
    except Exception as e:
        issues.append({"component": "vault_watcher", "error": str(e)})
    return issues

def check_logs():
    """扫描当日日志，匹配已知失败模式（抗体）"""
    issues = []
    try:
        log_dir = Path(os.environ.get("LOCALAPPDATA", "")) / "Temp" / "openclaw"
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"openclaw-{today}.log"
        if not log_file.exists():
            return issues
        file_size = log_file.stat().st_size
        if file_size > 5_000_000:  # >5MB: skip, too large for fast scan
            return issues
        from collections import defaultdict
        antibodies = load_antibodies()
        # 只匹配 active（未 resolved）抗体中的错误模式
        active = [a for a in antibodies if not a.get("resolved")]
        if not active:
            return issues
        # 只读最后 200 行，跳过抗体自身的输出行防止递归
        lines = log_file.read_text(encoding="utf-8", errors="replace").splitlines()[-200:]
        for line in lines:
            if 'matched antibody' in line:
                continue
            for ab in active:
                patterns = ab["pattern"].split("|")
                for pat in patterns:
                    if pat.lower() in line.lower():
                        issues.append({"component": f"log/{ab['name']}",
                                      "error": f"found '{ab['name']}' rule: {pat}"})
                        record_hit(ab["name"], antibodies)
                        break
    except Exception:
        pass
    return issues


def check_vault():
    """检查 vault 目录"""
    issues = []
    vault = VAULT_DIR  # from shared_config
    if not vault.exists():
        issues.append({"component": "vault", "error": "vault directory not found"})
    return issues

def try_fix(issue, antibody):
    """尝试自动修复"""
    auto_fix = antibody.get("auto_fix")
    if not auto_fix:
        return False, "no auto_fix defined"

    # 替换占位符
    if "{job_id}" in auto_fix:
        # 需要 job_id 但这里拿不到，跳过
        return False, "auto_fix needs job_id, skipped"

    try:
        result = subprocess.run(
            ["powershell", "-Command", auto_fix],
            capture_output=True, text=True, timeout=30,
            encoding="utf-8", errors="replace"
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr[:200]
    except Exception as e:
        return False, str(e)

import threading

def run_check_with_timeout(name, check_fn, timeout=15):
    """Wrapper to run a check with a timeout, returning (issues, timed_out).
    Uses threading + polling since Windows multiprocessing spawn has issues.
    """
    result = {"issues": None, "exception": None, "done": False}
    def target():
        try:
            result["issues"] = check_fn()
        except Exception as e:
            result["exception"] = e
        finally:
            result["done"] = True
    t = threading.Thread(target=target, daemon=True)
    t.start()
    t.join(timeout)
    if not result["done"]:
        return [], True
    if result["exception"]:
        return [], False
    return result["issues"], False

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 健康巡检开始")
    print("=" * 50)

    antibodies = load_antibodies()
    all_issues = []
    fixed = 0
    skipped = 0

    # 执行所有检查
    checks = {
        "Logs": check_logs,
        "Qdrant": check_qdrant,
        "LM Studio": check_lmstudio,
        "Vault": check_vault,
        "Vault Watcher": check_vault_watcher,
        "Cron Tasks": check_cron_tasks,
    }

    for name, check_fn in checks.items():
        issues, timed_out = run_check_with_timeout(name, check_fn)
        if timed_out:
            print(f"  [TIMEOUT] {name} (超过{15}秒)")
            all_issues.append({"component": name, "error": "timed out"})
            skipped += 1
            continue
        if not issues:
            print(f"  [OK] {name}")
        else:
            for issue in issues:
                error_msg = issue["error"]
                print(f"  [WARN] {name}: {error_msg}")

                # 匹配抗体
                ab = match_antibody(error_msg, antibodies)
                if ab:
                    print(f"    [ANTIBODY] {ab['name']}: {ab['fix']}")
                    record_hit(ab["name"], antibodies)

                    if ab.get("auto_fix"):
                        success, msg = try_fix(issue, ab)
                        if success:
                            print(f"    [FIXED] {msg}")
                            # 验证修复
                            verify_issues = check_fn()
                            if not verify_issues:
                                print(f"    [VERIFIED] {name} 已恢复正常")
                                fixed += 1
                                ab["success_rate"] = min(1.0, ab.get("success_rate", 0) + 0.1)
                            else:
                                print(f"    [NOT_FIXED] {name} 仍有问题: {verify_issues[0]['error'][:50]}")
                                skipped += 1
                        else:
                            print(f"    [SKIP] Cannot auto-fix: {msg}")
                            skipped += 1
                    else:
                        print(f"    [MANUAL] Needs human intervention")
                        skipped += 1
                else:
                    print(f"    [NEW] No antibody found, recording...")
                    antibodies.append({
                        "name": f"auto-{issue['component']}-{len(antibodies)}",
                        "pattern": error_msg[:100],
                        "fix": "TODO: determine fix",
                        "auto_fix": None,
                        "created": datetime.now().strftime("%Y-%m-%d"),
                        "hits": 1,
                        "success_rate": 0.0
                    })
                    save_antibodies(antibodies)
                    skipped += 1

                all_issues.append(issue)

    print("=" * 50)
    if not all_issues:
        print("[OK] 所有组件正常，无需修复")
    else:
        print(f"[SUMMARY] 发现 {len(all_issues)} 个问题，自动修复 {fixed} 个，需手动 {skipped} 个")

    # 触发进化引擎分析
    print("\n--- 启动进化引擎 ---")
    try:
        evo_script = Path(WORKSPACE) / "scripts" / "evolution_engine.py"
        if evo_script.exists():
            result = subprocess.run(
                [sys.executable, str(evo_script)],
                capture_output=True, text=True, timeout=30,
                encoding="utf-8", errors="replace"
            )
            stdout = result.stdout or ""
            for line in stdout.strip().split("\n")[-10:]:
                if line.strip():
                    print(f"  [EVO] {line.strip()}")
        else:
            print("  [EVO] evolution_engine.py not found")
    except Exception as e:
        print(f"  [EVO] error: {e}")

    # 输出到 vault 系统状态
    status_file = VAULT_DIR / "02-知识" / "系统健康状态.md"
    lines = [
        "# 系统健康状态",
        "",
        f"> 自动巡检于 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "| 组件 | 状态 |",
        "|------|------|",
    ]
    for name, check_fn in checks.items():
        issues, _ = run_check_with_timeout(name, check_fn, timeout=10)
        status = "✅ 正常" if not issues else f"⚠️ {issues[0]['error'][:50]}"
        lines.append(f"| {name} | {status} |")

    if all_issues:
        lines.append("")
        lines.append("## 待处理问题")
        for issue in all_issues:
            lines.append(f"- **{issue['component']}**: {issue['error'][:100]}")

    with open(status_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n[OK] 状态已写入 {status_file}")

if __name__ == "__main__":
    main()


