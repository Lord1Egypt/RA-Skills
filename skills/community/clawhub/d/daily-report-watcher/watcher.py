#!/usr/bin/env python3
"""
daily-report-watcher.py v1.0 — 19:30 日报轻量兜底监控
====================================================================
背景：
  - 2026-06-12 周五 19:30 码虫日报 cron 失败 → 沉默 2 天才发现（ERR-20260614-001）
  - 根因：M3 overloaded + OpenClaw update_goal fail + failureAlert 投递失败
  - 原监控任务 ba67d0ff 早已 not found
  - OpenClaw 平台层告警不可靠 → 必须应用层独立兜底

功能（轻量、独立、不依赖平台告警）：
  1. 检查 19:30 日报任务（6ade489c）最近一次 run 状态
  2. 检查日报 markdown 文件是否存在
  3. 连续 error + 过去 24h 内 → 主动用飞书 post API 发告警
  4. 静默期 4 小时（避免重复告警）

触发：
  - 设计为 cron 任务，每天 8:30 / 12:30 / 16:30 跑（每天 3 次）
  - 静默期内跳过；超静默期才告警
  - 周一 8:30 必跑（捕获周末后的失败）

依赖：
  - feishu_post.py 发送告警
  - openclaw CLI 查 cron 状态
  - requests (已安装)

用法：
  python3 watcher.py                # 检查并按需告警
  python3 watcher.py --dry-run      # 检查但不告警
  python3 watcher.py --check-only   # 只检查状态，exit code 反映结果

退出码：
  0 = 日报正常（无告警）
  1 = 日报异常（已告警）
  2 = 检查出错（cron 不可达等）

沉淀规则：
  - RULE-20260614-001 cron 失败 → 立即写文件兜底 + 不打扰老板原则
  - HOT-20260614-001 候选（30 天观察期）

作者: 码虫 🐛 | 2026-06-14
"""
import os
import sys
import json
import subprocess
import argparse
from datetime import datetime, timezone, timedelta

# ──── 配置 ────
WORKSPACE = "/home/colbert/.openclaw/workspace-coding-advisor"
DAILY_REPORT_JOB_ID = "6ade489c-f234-4877-a462-ba30504e529f"
DAILY_REPORT_FILE = f"{WORKSPACE}/memory/daily-reports"
STATE_FILE = "/tmp/coding-advisor-daily-report-watcher-state.json"
RECIPIENT = "ou_991021547578f722d08533accc83651d"
COOLDOWN_MS = 4 * 60 * 60 * 1000  # 4 小时
ERROR_WINDOW_HOURS = 36  # 过去 36h 内 fail 才告警（覆盖工作日 + 周末）

# 引入 feishu_post
sys.path.insert(0, f"{WORKSPACE}/scripts")
from feishu_post import send_post  # noqa: E402

# ──── 状态持久化 ────
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_alert_at_ms": 0, "last_alert_reason": None}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

# ──── 核心检查 ────
def check_cron_status():
    """调用 openclaw cron get 检查 19:30 日报任务状态"""
    try:
        result = subprocess.run(
            ["openclaw", "cron", "get", DAILY_REPORT_JOB_ID],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return None, f"openclaw cron get 失败: {result.stderr[:200]}"
        # 跳过 config warnings
        out = result.stdout
        if "{" in out:
            json_start = out.index("{")
            data = json.loads(out[json_start:])
        else:
            return None, "openclaw cron get 无 JSON 输出"
        return data, None
    except Exception as e:
        return None, f"openclaw cron get 异常: {e}"

def get_yesterday_date():
    """返回昨天日期字符串（YYYY-MM-DD）"""
    tz = timezone(timedelta(hours=8))  # Asia/Shanghai
    yesterday = (datetime.now(tz) - timedelta(days=1)).strftime("%Y-%m-%d")
    return yesterday

def get_last_weekday_date():
    """返回最近一个工作日（周一到周五）日期字符串"""
    tz = timezone(timedelta(hours=8))
    d = datetime.now(tz) - timedelta(days=1)
    # 跳过周末
    while d.weekday() >= 5:  # 5=周六, 6=周日
        d -= timedelta(days=1)
    return d.strftime("%Y-%m-%d")

def is_weekend():
    tz = timezone(timedelta(hours=8))
    return datetime.now(tz).weekday() >= 5

# ──── 告警发送 ────
def send_alert(reason, detail_lines):
    """发送飞书告警"""
    title = f"🚨 码虫日报异常：{reason}"
    lines = [
        ("📌 整理：码虫 🐛 | daily-report-watcher v1.0\n", {"bold": True}),
        ("━━━━━━━━━━━━━━━━━━━━", {}),
    ]
    for ln in detail_lines:
        lines.append((ln, {}))
    lines.append(("━━━━━━━━━━━━━━━━━━━━", {}))
    lines.append((
        f"🔧 手动处理：检查 memory/daily-reports/ 是否缺失文件，按需补发",
        {"grey": True}
    ))
    try:
        result = send_post(title, lines, RECIPIENT)
        return result.get("code") == 0
    except Exception as e:
        print(f"[ERROR] 飞书告警发送失败: {e}", file=sys.stderr)
        return False

# ──── 主流程 ────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="只检查不告警")
    parser.add_argument("--check-only", action="store_true", help="只检查，exit code 反映结果")
    args = parser.parse_args()

    state = load_state()
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    now_iso = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
    yesterday = get_yesterday_date()
    last_weekday = get_last_weekday_date()

    print(f"[{now_iso}] daily-report-watcher 启动")
    print(f"  昨天日期: {yesterday} ({'周末' if is_weekend() else '工作日'})")
    print(f"  最近工作日: {last_weekday}")

    # 1. 检查 cron 状态
    cron_data, err = check_cron_status()
    if err:
        print(f"[ERROR] {err}", file=sys.stderr)
        if not args.check_only:
            # 检查出错 → 不发告警（避免误报）
            print("[SKIP] 检查出错，跳过告警")
        return 2

    job_state = cron_data.get("state", {})
    last_run_status = job_state.get("lastRunStatus", "unknown")
    last_run_at_ms = job_state.get("lastRunAtMs", 0)
    consecutive_errors = job_state.get("consecutiveErrors", 0)
    last_delivered = job_state.get("lastDelivered", False)
    last_diagnostic = job_state.get("lastDiagnosticSummary", "")

    print(f"  上次状态: {last_run_status} (consecutive: {consecutive_errors})")
    print(f"  上次运行: {datetime.fromtimestamp(last_run_at_ms/1000, tz=timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S') if last_run_at_ms else 'never'}")
    print(f"  上次送达: {last_delivered}")
    if last_diagnostic:
        print(f"  上次诊断: {last_diagnostic[:100]}")

    # 2. 计算错误时间窗口
    if not last_run_at_ms:
        print("[OK] 日报任务从未运行过（不告警）")
        return 0
    
    age_hours = (now_ms - last_run_at_ms) / (1000 * 60 * 60)
    if age_hours > ERROR_WINDOW_HOURS:
        print(f"[OK] 上次运行 {age_hours:.1f}h 前，超出 {ERROR_WINDOW_HOURS}h 窗口，不告警")
        return 0

    # 3. 检查日报文件
    target_date = last_weekday if is_weekend() else yesterday
    report_path = f"{DAILY_REPORT_FILE}/{target_date}.md"
    file_exists = os.path.exists(report_path)
    print(f"  检查文件: {report_path} → {'存在' if file_exists else '❌ 缺失'}")

    # 4. 判断是否告警
    reasons = []
    if last_run_status == "error" or not last_delivered:
        reasons.append(f"日报任务 status={last_run_status}, delivered={last_delivered}")
    if not file_exists and not is_weekend():
        reasons.append(f"日报 markdown 文件缺失: {report_path}")

    if not reasons:
        print(f"[OK] 日报状态正常（{target_date}）")
        return 0

    reason = " + ".join(reasons)
    print(f"[ALERT] 发现异常: {reason}")

    # 5. 检查静默期
    last_alert_ms = state.get("last_alert_at_ms", 0)
    if now_ms - last_alert_ms < COOLDOWN_MS:
        remaining_min = (COOLDOWN_MS - (now_ms - last_alert_ms)) / 60000
        print(f"[SKIP] 静默期内（还剩 {remaining_min:.0f} 分钟），跳过告警")
        print(f"       上次告警原因: {state.get('last_alert_reason', '?')}")
        return 0 if not args.check_only else 1

    if args.dry_run or args.check_only:
        print(f"[DRY-RUN] 本应告警: {reason}")
        return 1

    # 6. 发送告警
    detail_lines = [
        f"📅 检查时间：{now_iso}",
        f"📂 目标日报：{target_date}",
        f"🔴 异常原因：{reason}",
        f"📊 Cron 状态：status={last_run_status}, consecutive={consecutive_errors}",
        f"🔍 诊断信息：{last_diagnostic[:200] if last_diagnostic else '(无)'}",
        f"📁 文件路径：{report_path}",
        "",
        "🛠 建议处理：",
        "1. 检查 OpenClaw 日志（cron runs --id 6ade489c）",
        "2. 如确认失败 → 手工触发重跑或补发",
        "3. 检查 failureAlert 是否配置正确",
    ]
    
    print(f"[SEND] 发送飞书告警...")
    if send_alert(reason, detail_lines):
        state["last_alert_at_ms"] = now_ms
        state["last_alert_reason"] = reason
        save_state(state)
        print(f"[OK] 告警已发送，下次静默至 {datetime.fromtimestamp((now_ms+COOLDOWN_MS)/1000, tz=timezone(timedelta(hours=8))).strftime('%H:%M:%S')}")
        return 1
    else:
        print(f"[ERROR] 告警发送失败", file=sys.stderr)
        return 2

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[INTERRUPTED]")
        sys.exit(130)
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(2)
