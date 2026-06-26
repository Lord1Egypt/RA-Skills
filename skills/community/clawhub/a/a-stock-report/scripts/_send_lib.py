#!/usr/bin/env python3
"""
A-stock-report 推送共用库

提供 4 个 send 脚本的共用能力：
- get_webhook_url()：从 env 读 webhook
- wx(text)：curl 风格推送 + 自动重试
- notify_failure(prefix, msg)：v3.1.0 补丁 2 修复版 — 内部 try/except，
  wx() 自身失败时只打印 stderr，不再阻断主流程

设计原则（2026-06-08 教训）：
    except 块内调用的任何可能抛异常的函数，必须被调方内部包裹 try/except。
    否则新异常会替换原异常冒泡，外层 _exit_code = 1 等清理代码被跳过。

用法：
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from _send_lib import get_webhook_url, wx, notify_failure
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta

# 北京时区，统一时间戳
_BJ = timezone(timedelta(hours=8))
_ts = lambda: datetime.now(_BJ).strftime("%H:%M:%S")


def get_webhook_url() -> str:
    """从 env 读 webhook URL，缺失时抛 RuntimeError"""
    key = os.environ.get("WECOM_WEBHOOK_KEY", "")
    if not key:
        raise RuntimeError("WECOM_WEBHOOK_KEY environment variable not set")
    return f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key.strip()}"


def wx(text: str, max_retries: int = 2) -> int:
    """企业微信推送，curl 风格，带自动重试。
    返回 0 = 成功，-1 = 失败。

    v3.1.1 修复：内部 try/except 包住 get_webhook_url()。
    若 WECOM_WEBHOOK_KEY 缺失（RuntimeError）则返回 -1 而不抛异常，
    避免外层 `except Exception` 块中调用的 wx() 自身崩（与 v3.1.0 教训同源）。
    """
    payload = json.dumps({"msgtype": "text", "text": {"content": text}}, ensure_ascii=False)
    for attempt in range(max_retries + 1):
        try:
            url = get_webhook_url()
        except RuntimeError as _e:
            print(f"[{_ts()}] [WX] webhook URL 获取失败: {_e}")
            return -1
        r = subprocess.run(
            ["curl", "-s", "-X", "POST", url,
             "-H", "Content-Type: application/json", "-d", "@-"],
            input=payload.encode("utf-8"), capture_output=True)
        try:
            errcode = json.loads(r.stdout.decode()).get("errcode", -1)
        except Exception:
            errcode = -1
        if errcode == 0:
            return 0
        if attempt < max_retries:
            print(f"[{_ts()}] [WX] 发送失败，errcode={errcode}，重试中...")
    return -1


def notify_failure(prefix: str, msg: str) -> None:
    """推送失败时通过企业微信发预警通知（v3.1.0 补丁 2 修复版）。

    关键修复：内部包裹 try/Exception，wx() 自身失败时（包括 WECOM_WEBHOOK_KEY
    缺失导致的 RuntimeError、网络错误等）仅打印到 stderr，**不再阻断主流程**。

    原 bug：notify_failure 自身 wx() 失败时抛异常，外层 `except Exception` 块
    里 `_exit_code = 1` 还没执行就被新异常冒泡替换，导致脚本永远 exit 0 +
    打印"✅ 已完成"误导监控。

    prefix 示例：「晚报」「晨报」「收盘小结」「盘中预警」「周末要闻」「IPO周报」
    """
    try:
        alert = f"⚠️ 【{prefix}推送失败】\n{msg}\n\n请及时检查 cron 任务状态。"
        _err = wx(alert)
        if _err == 0:
            print(f"[{_ts()}] 失败通知已发送")
        else:
            print(f"[{_ts()}] 失败通知发送失败: err={_err}")
    except Exception as _e:
        # notify_failure 自身失败也不能让外层崩
        # 退化方案：仅打印到 stderr，让 cron 日志能捕获
        sys.stderr.write(f"[{_ts()}] notify_failure 失败: type={type(_e).__name__} msg={_e}\n")
        sys.stderr.flush()
