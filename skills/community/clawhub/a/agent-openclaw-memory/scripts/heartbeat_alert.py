"""
heartbeat_alert.py — 趋势告警（Phase 5）

E1: 闸门拒绝率突变
E2: 蒸馏自评均分下降
E3: Qdrant 写入失败率
E4: 综合告警 → 推微信

由 heartbeat 末尾调用。返回告警条数。
"""
import json, sys, os
from pathlib import Path
from datetime import datetime, timezone, timedelta

WORKSPACE = Path(__file__).parent.parent
DATA = WORKSPACE / "data"
SCRIPTS = Path(__file__).parent

# 告警阈值
GATE_REJECT_SPIKE = 0.5          # 拒绝率 > 50%
GATE_REJECT_JUMP = 0.3           # 比 24h 均值上涨 > 30%
SELF_EVAL_LOW = 3.0              # 自评均分 < 3
QDRANT_WRITE_FAIL_RATE = 0.10    # 写入失败 > 10%
MAX_ALERT_ITEMS = 3              # 新增告警 > 3


def load_history():
    """加载质量快照历史"""
    qf = DATA / "quality_snapshot.json"
    if not qf.exists():
        return []
    try:
        return [json.loads(line) for line in qf.read_text(encoding="utf-8").strip().split("\n") if line.strip()]
    except Exception:
        return []


def load_smoke():
    """加载冒烟测试结果"""
    sf = DATA / "smoke_snapshot.json"
    if not sf.exists():
        return {}
    try:
        return json.loads(sf.read_text(encoding="utf-8"))
    except Exception:
        return {}


def calc_gate_rate(history_24h: list) -> float:
    """计算过去 24h 的平均闸门拒绝率"""
    total = rejected = 0
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    for h in history_24h:
        try:
            ts = datetime.fromisoformat(h["ts"].replace("Z", "+00:00"))
            if ts < cutoff:
                continue
            t = h.get("compress_total", 0)
            r = h.get("compress_rejected", 0)
            total += t
            rejected += r
        except Exception:
            continue
    return rejected / total if total > 0 else 0


def check_alerts():
    """检查所有告警条件，返回告警列表"""
    alerts = []
    history = load_history()
    smoke = load_smoke()

    latest = history[-1] if history else {}

    # ── E1: 闸门拒绝率突变 ──
    if history:
        recent = history[-3:]  # 最近 3 次心跳
        recent_good = [h for h in recent if h.get("compress_total", 0) > 0]
        if len(recent_good) >= 2:
            recent_rates = [h["compress_rejected"] / h["compress_total"] for h in recent_good]
            avg_rate_24h = calc_gate_rate(history)
            if all(r > GATE_REJECT_SPIKE for r in recent_rates):
                jump = recent_rates[-1] - avg_rate_24h
                if jump > GATE_REJECT_JUMP:
                    alerts.append({
                        "type": "gate_reject_spike",
                        "level": "warn",
                        "msg": f"压缩闸门拒绝率 {recent_rates[-1]:.0%}，24h均值 {avg_rate_24h:.0%}（+{jump:.0%}）",
                    })

    # ── E2: 蒸馏自评均分下降 ──
    if latest.get("consolidate_scores"):
        scores = latest["consolidate_scores"]
        avg = sum(scores) / len(scores)
        if avg < SELF_EVAL_LOW:
            alerts.append({
                "type": "low_self_eval",
                "level": "warn",
                "msg": f"蒸馏自评均分 {avg:.1f} < {SELF_EVAL_LOW}",
            })

    # ── E3: Qdrant 写入失败率 ──
    qdrant_total = latest.get("qdrant_write_total", 0)
    qdrant_fail = latest.get("qdrant_write_fail", 0)
    if qdrant_total > 0 and qdrant_fail / qdrant_total > QDRANT_WRITE_FAIL_RATE:
        alerts.append({
            "type": "qdrant_write_fail",
            "level": "error",
            "msg": f"Qdrant 写入失败 {qdrant_fail}/{qdrant_total}（{qdrant_fail/qdrant_total:.0%}）",
        })

    # ── E4: 综合告警 ──
    smoke_alerts = smoke.get("alerts", 0)
    if smoke_alerts > 0:
        alerts.append({
            "type": "smoke_test_fail",
            "level": "error",
            "msg": f"冒烟测试 {smoke_alerts} 项失败",
        })

    # 心跳脚本失败
    health_file = DATA / "system_health.json"
    recent_fails = 0
    if health_file.exists():
        try:
            health = json.loads(health_file.read_text(encoding="utf-8"))
            tasks = health.get("tasks", {})
            for name, t in tasks.items():
                if t.get("last_status") != "ok":
                    recent_fails += 1
        except Exception:
            pass

    if recent_fails > MAX_ALERT_ITEMS:
        alerts.append({
            "type": "health_fails",
            "level": "error",
            "msg": f"心跳脚本 {recent_fails} 个失败",
        })

    return alerts


def push_wechat(alerts: list):
    """推送到微信（复用 morning-push 通道）"""
    if not alerts:
        print("  无告警")
        return

    lines = [f"[系统心跳告警] {len(alerts)} 项异常:"]
    for a in alerts:
        icon = "❌" if a["level"] == "error" else "⚠️"
        lines.append(f"  {icon} {a['msg']}")

    msg = "\n".join(lines)
    print(msg)

    # 尝试推微信
    try:
        import requests

        cfg_file = SCRIPTS / "config.json"
        if cfg_file.exists():
            cfg = json.loads(cfg_file.read_text(encoding="utf-8"))
            wx_cfg = cfg.get("wechat_push", {})
            if wx_cfg.get("enabled") and wx_cfg.get("webhook"):
                requests.post(wx_cfg["webhook"], json={"content": msg}, timeout=10)
    except Exception:
        pass


def main():
    alerts = check_alerts()
    push_wechat(alerts)
    # 写告警记录
    record = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "alerts": len(alerts),
        "details": alerts,
    }
    DATA.mkdir(parents=True, exist_ok=True)
    alert_file = DATA / "alert_history.jsonl"
    with open(alert_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return len(alerts)


if __name__ == "__main__":
    count = main()
    sys.exit(1 if count > 0 else 0)
