#!/usr/bin/env python3
"""晨报推送脚本 - 三步模式：
第一步（由LLM在cron prompt中完成）：搜索新闻 + 生成报告，写入 /tmp/morning_report_content.txt
第二步（Python）：读取文件 → 检查去重锁 → 保存MD → 推送（失败时发预警）
第三步（由LLM在cron prompt第四步中调用）：检查本脚本退出码，0=成功，非0=失败需预警
"""
from datetime import datetime, timezone, timedelta, timedelta as td
import sys, os, json

# ── 共用推送库（v3.1.1 抽取）────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _send_lib import get_webhook_url, wx, notify_failure  # noqa: E402

# ── 配置加载（白名单读取外部配置，路径可通过 ENV_FILE 系列变量覆盖）──────────────
_REQUIRED_KEYS = ["WECOM_WEBHOOK_KEY", "IWENCAI_API_KEY"]
for _p in (
    os.environ.get("ENV_FILE", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../.env")),
    os.environ.get("ENV_FILE_FALLBACK", "/workspace/.env"),
):
    if not os.path.exists(_p):
        continue
    try:
        for _line in open(_p):
            _line = _line.strip()
            if not _line or _line.startswith("#") or "=" not in _line:
                continue
            _k, _v = _line.split("=", 1)
            _k = _k.strip()
            if _k in _REQUIRED_KEYS and _k not in os.environ:
                os.environ[_k] = _v.strip().strip('"').strip("'")
    except (OSError, UnicodeDecodeError):
        continue

def _now(): return datetime.now(timezone(td(hours=8)))
TS = lambda: _now().strftime("%H:%M:%S")
_date_str = lambda: _now().strftime("%Y%m%d")
content_file = "/tmp/morning_report_content.txt"
_lock_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".morning_report_lock.json")

def read_lock():
    if os.path.exists(_lock_file):
        try:
            with open(_lock_file) as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def write_lock(date_str, status):
    with open(_lock_file, 'w') as f:
        json.dump({'date': date_str, 'status': status, 'ts': _now().isoformat()}, f)


if __name__ == "__main__":
    _today = _date_str()
    # ---------- 防重复推送：检查当日是否已推送 ----------
    lock = read_lock()
    if lock.get('date') == _today and lock.get('status') == 'ok':
        print(f"[{TS()}] ⏭ 已推送，跳过（date={_today}）")
        sys.exit(0)

    print(f"[{TS()}] 第一步：读取报告内容...")

    # ---------- 检查内容文件 ----------
    if not os.path.exists(content_file):
        msg = f"报告文件不存在: {content_file}"
        print(f"[{TS()}] ❌ {msg}")
        notify_failure("晨报", msg)
        sys.exit(1)

    with open(content_file, encoding='utf-8') as f:
        report = f.read()

    if not report.strip():
        msg = "报告内容为空"
        print(f"[{TS()}] ❌ {msg}")
        notify_failure("晨报", msg)
        sys.exit(1)

    # ---------- 保存 Markdown ----------
    print(f"[{TS()}] 第二步：保存Markdown报告...")
    _dir = "/workspace/projects/A股报告系统/reports"
    os.makedirs(_dir, exist_ok=True)
    _path = os.path.join(_dir, f"晨报_{_today}.md")
    with open(_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  已保存: {_path}")

    print("\n" + "=" * 60)
    print(report)
    print("=" * 60)

    # ---------- 推送 ----------
    print(f"\n[{TS()}] 第三步：推送...")
    err = wx(report)
    if err == 0:
        write_lock(_today, 'ok')
        print(f"\n[{TS()}] ✅ 已推送")
        sys.exit(0)
    else:
        msg = f"webhook 返回错误: err={err}"
        print(f"\n[{TS()}] ❌ {msg}")
        notify_failure("晨报", msg)
        sys.exit(1)
