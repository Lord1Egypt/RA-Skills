#!/usr/bin/env python3
"""
push_manager.py — BidHunter v1.2 推送通道管理器

通道优先级：🥇 钉钉 → 🥈 企微 → 📧 邮件兜底（飞书 v1.5）

用法:
  python3 push_manager.py test [--channel dingtalk|wecom|email]   # 测试通道连通性
  python3 push_manager.py send  --subject "..." [--content "..."] [--channel ...]
  python3 push_manager.py history [--days 30]                     # 查看推送历史
  python3 push_manager.py stats                                   # 推送统计
  python3 push_manager.py health-check                            # 健康检查（失败告警）
  python3 push_manager.py retry-failed [--days 7]                 # 重试失败消息
  python3 push_manager.py send-file <report.txt> [--summary]      # 推送报告文件

配置文件: ~/.config/bidhunter/push.json （由 config_wizard.py 生成，权限 600）
历史库:   scripts/push_history.db （SQLite，WAL 模式，30 天滚动清理）
"""

import argparse
import base64
import hashlib
import hmac
import json
import os
import smtplib
import sqlite3
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from email.header import Header
from email.mime.text import MIMEText

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "push_history.db")
CONFIG_PATH = os.path.expanduser("~/.config/bidhunter/push.json")

RETRY_BACKOFF = [1, 5, 30]  # 指数退避（秒）
CHANNEL_PRIORITY = ["dingtalk", "wecom", "email"]


# ---------------------------------------------------------------------------
# 配置加载
# ---------------------------------------------------------------------------

def load_config(path=CONFIG_PATH):
    """加载推送配置；不存在时返回 None（调用方应静默跳过推送，保持向后兼容）。"""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[push] 配置文件解析失败: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# SQLite 历史库（WAL 模式，防交叉写锁）
# ---------------------------------------------------------------------------

def _conn():
    c = sqlite3.connect(DB_PATH, timeout=10)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("""CREATE TABLE IF NOT EXISTS push_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        channel TEXT NOT NULL,
        subject TEXT NOT NULL,
        status TEXT NOT NULL,
        retry_count INTEGER DEFAULT 0,
        error_msg TEXT DEFAULT '',
        idempotency_key TEXT UNIQUE
    )""")
    c.execute("CREATE INDEX IF NOT EXISTS idx_push_ts ON push_log(ts DESC)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_push_status ON push_log(status)")
    return c


def _cleanup_old(days=30):
    with _conn() as c:
        cutoff = (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")
        c.execute("DELETE FROM push_log WHERE ts < ?", (cutoff,))


def _idem_key(channel, subject):
    raw = f"{datetime.now().date()}|{channel}|{subject}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def log_push(channel, subject, status, retry_count=0, error_msg="", idem_key=None):
    """写入推送日志；幂等键冲突（同日同题已成功）返回 False 表示跳过。"""
    with _conn() as c:
        if idem_key:
            row = c.execute(
                "SELECT id, status FROM push_log WHERE idempotency_key=?",
                (idem_key,)).fetchone()
            if row and row[1] == "success":
                return False
        try:
            c.execute("""INSERT OR REPLACE INTO push_log
                (ts, channel, subject, status, retry_count, error_msg, idempotency_key)
                VALUES (?,?,?,?,?,?,?)""",
                (datetime.now().isoformat(timespec="seconds"), channel, subject,
                 status, retry_count, error_msg, idem_key))
        except sqlite3.IntegrityError:
            return False
    return True


# ---------------------------------------------------------------------------
# 通道适配器
# ---------------------------------------------------------------------------

def _http_post_json(url, payload, timeout=10):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    return body


def send_dingtalk(cfg, subject, content):
    """钉钉自定义机器人（加签）。返回 (ok, err)。"""
    webhook = cfg.get("webhook", "")
    secret = cfg.get("secret", "")
    if not webhook:
        return False, "缺少 webhook"
    if secret:
        ts = str(round(time.time() * 1000))
        sign_str = f"{ts}\n{secret}"
        digest = hmac.new(secret.encode("utf-8"), sign_str.encode("utf-8"),
                          digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(digest))
        webhook = f"{webhook}&timestamp={ts}&sign={sign}"
    text = f"**{subject}**\n\n{content}"
    if len(text) > 18000:  # 钉钉单条上限约 20000 字符，留余量
        text = text[:18000] + "\n...(内容过长已截断)"
    body = _http_post_json(webhook, {
        "msgtype": "markdown",
        "markdown": {"title": subject[:64], "text": text},
    })
    if body.get("errcode") == 0:
        return True, ""
    return False, f"errcode={body.get('errcode')} {body.get('errmsg', '')}"


def send_wecom(cfg, subject, content):
    """企微群机器人 webhook。返回 (ok, err)。"""
    webhook = cfg.get("webhook", "")
    if not webhook:
        return False, "缺少 webhook"
    text = f"**{subject}**\n{content}"
    if len(text) > 4000:  # 企微 markdown 上限 4096 字节，留余量
        text = text[:3800] + "\n...(内容过长已截断)"
    body = _http_post_json(webhook, {
        "msgtype": "markdown",
        "markdown": {"content": text},
    })
    if body.get("errcode") == 0:
        return True, ""
    return False, f"errcode={body.get('errcode')} {body.get('errmsg', '')}"


def send_email(cfg, subject, content):
    """SMTP 邮件兜底。返回 (ok, err)。"""
    host = cfg.get("host", "")
    port = int(cfg.get("port", 465))
    user = cfg.get("user", "")
    password = os.path.expanduser(str(cfg.get("password", "")))
    to = cfg.get("to", user)
    if not (host and user and password and to):
        return False, "邮件配置不完整（host/user/password/to）"
    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = Header(subject, "utf-8")
    msg["From"] = user
    msg["To"] = to
    try:
        with smtplib.SMTP_SSL(host, port, timeout=15) as s:
            s.login(user, password)
            s.sendmail(user, [to], msg.as_string())
        return True, ""
    except Exception as e:  # noqa: BLE001
        return False, str(e)[:300]


SENDERS = {"dingtalk": send_dingtalk, "wecom": send_wecom, "email": send_email}


# ---------------------------------------------------------------------------
# 发送（含重试 + 幂等 + 兜底切换）
# ---------------------------------------------------------------------------

def send_one(channel, subject, content, config, allow_fallback=True):
    """单通道发送：幂等检查 → 重试 3 次（1s/5s/30s）→ 失败切备用通道。"""
    key = _idem_key(channel, subject)
    if not log_push(channel, subject, "pending", idem_key=key):
        print(f"[push] 跳过（同日同题已成功）: {channel} · {subject[:40]}")
        return True

    cfg = (config.get("channels") or {}).get(channel)
    if not cfg or not cfg.get("enabled", True):
        log_push(channel, subject, "failed", error_msg="通道未配置或未启用", idem_key=key)
        return False

    sender = SENDERS[channel]
    last_err = ""
    for attempt, delay in enumerate([0] + RETRY_BACKOFF[:-1]):
        time.sleep(delay)
        try:
            ok, err = sender(cfg, subject, content)
        except Exception as e:  # noqa: BLE001
            ok, err = False, str(e)[:300]
        if ok:
            log_push(channel, subject, "success", retry_count=attempt, idem_key=key)
            return True
        last_err = err
        print(f"[push] {channel} 第 {attempt + 1} 次失败: {err}", file=sys.stderr)

    log_push(channel, subject, "failed", retry_count=len(RETRY_BACKOFF),
             error_msg=last_err, idem_key=key)

    # 主通道失败 → 备用通道兜底（按优先级）
    if allow_fallback:
        for alt in CHANNEL_PRIORITY:
            if alt == channel:
                continue
            alt_cfg = (config.get("channels") or {}).get(alt)
            if alt_cfg and alt_cfg.get("enabled", True):
                print(f"[push] {channel} 失败，切备用通道 {alt}")
                # 兜底发送不记录同 key，避免覆盖主通道日志
                ok2, err2 = SENDERS[alt](alt_cfg, subject, content)
                log_push(alt, f"[fallback]{subject}", "success" if ok2 else "failed",
                         error_msg="" if ok2 else err2)
                return ok2
    return False


def send_multi(subject, content, config=None, channels=None):
    """多通道并行（顺序发送，日志逐条落库）。channels 为空时用配置里的启用通道。"""
    config = config or load_config()
    if not config:
        print("[push] 未配置推送（~/.config/bidhunter/push.json 不存在），跳过")
        return False
    if not channels:
        channels = [c for c in CHANNEL_PRIORITY
                    if (config.get("channels") or {}).get(c, {}).get("enabled")]
    if not channels:
        print("[push] 无已启用通道，跳过")
        return False
    results = {c: send_one(c, subject, content, config) for c in channels}
    ok_count = sum(results.values())
    print(f"[push] 完成: {ok_count}/{len(results)} 通道成功")
    return ok_count > 0


# ---------------------------------------------------------------------------
# 历史查询 / 统计 / 健康检查 / 重试
# ---------------------------------------------------------------------------

def get_history(days=30):
    _cleanup_old(days)
    cutoff = (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")
    with _conn() as c:
        rows = c.execute(
            "SELECT ts, channel, subject, status, retry_count, error_msg "
            "FROM push_log WHERE ts >= ? ORDER BY ts DESC LIMIT 200",
            (cutoff,)).fetchall()
    return rows


def get_stats():
    with _conn() as c:
        total = c.execute("SELECT COUNT(*) FROM push_log").fetchone()[0]
        ok = c.execute("SELECT COUNT(*) FROM push_log WHERE status='success'").fetchone()[0]
        fail = c.execute("SELECT COUNT(*) FROM push_log WHERE status='failed'").fetchone()[0]
        by_ch = c.execute(
            "SELECT channel, COUNT(*), SUM(status='success') FROM push_log "
            "GROUP BY channel").fetchall()
    return {"total": total, "success": ok, "failed": fail, "by_channel": by_ch}


def health_check(config=None):
    """健康检查：连续 3 天有失败且无成功 → 强制走邮件告警管理员。"""
    config = config or load_config()
    stats = get_stats()
    with _conn() as c:
        cutoff = (datetime.now() - timedelta(days=3)).isoformat(timespec="seconds")
        row = c.execute(
            "SELECT SUM(status='failed'), SUM(status='success') FROM push_log WHERE ts>=?",
            (cutoff,)).fetchone()
    recent_fail, recent_ok = (row[0] or 0), (row[1] or 0)
    alert = recent_fail >= 3 and recent_ok == 0
    return {"stats": stats, "recent_fail_3d": recent_fail,
            "recent_ok_3d": recent_ok, "alert": alert}


def retry_failed(days=7, config=None):
    """重试近 N 天失败消息（去掉幂等键重新入队）。"""
    config = config or load_config()
    cutoff = (datetime.now() - timedelta(days=days)).isoformat(timespec="seconds")
    with _conn() as c:
        rows = c.execute(
            "SELECT channel, subject FROM push_log "
            "WHERE status='failed' AND ts>=? AND subject NOT LIKE '[fallback]%'",
            (cutoff,)).fetchall()
    ok = 0
    for channel, subject in rows:
        # 清除幂等键以允许重发
        with _conn() as c:
            c.execute("DELETE FROM push_log WHERE channel=? AND subject=? AND status='failed'",
                      (channel, subject))
        if send_one(channel, subject, "（重试消息，内容见最近一次报告）", config,
                    allow_fallback=False):
            ok += 1
    print(f"[push] 重试完成: {ok}/{len(rows)} 成功")
    return ok


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_test(args, config):
    if not config:
        print("未找到配置，请先运行: python3 config_wizard.py")
        return 1
    channels = [args.channel] if args.channel else CHANNEL_PRIORITY
    all_ok = True
    for ch in channels:
        cfg = (config.get("channels") or {}).get(ch)
        if not cfg or not cfg.get("enabled", True):
            print(f"  {ch}: 未配置/未启用 — 跳过")
            continue
        try:
            ok, err = SENDERS[ch](cfg, "[BidHunter] 通道测试",
                                  f"通道连通性测试 · {datetime.now():%Y-%m-%d %H:%M}")
        except Exception as e:  # noqa: BLE001
            ok, err = False, str(e)[:200]
        print(f"  {ch}: {'✅ 通过' if ok else '❌ 失败 — ' + err}")
        all_ok = all_ok and ok
    return 0 if all_ok else 2


def main():
    p = argparse.ArgumentParser(description="BidHunter 推送通道管理器")
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("test", help="测试通道连通性")
    t.add_argument("--channel", choices=CHANNEL_PRIORITY)
    s = sub.add_parser("send", help="发送消息")
    s.add_argument("--subject", required=True)
    s.add_argument("--content", default="")
    s.add_argument("--channel", choices=CHANNEL_PRIORITY)
    sf = sub.add_parser("send-file", help="推送报告文件（自动取前 60 行）")
    sf.add_argument("file")
    sf.add_argument("--summary", action="store_true", help="仅推前 25 行精华")
    h = sub.add_parser("history", help="查看推送历史")
    h.add_argument("--days", type=int, default=30)
    sub.add_parser("stats", help="推送统计")
    sub.add_parser("health-check", help="健康检查（连续 3 天失败则告警）")
    r = sub.add_parser("retry-failed", help="重试失败消息")
    r.add_argument("--days", type=int, default=7)

    args = p.parse_args()
    config = load_config()
    _cleanup_old()

    if args.cmd == "test":
        sys.exit(cmd_test(args, config))
    if args.cmd == "send":
        send_multi(args.subject, args.content, config,
                   channels=[args.channel] if args.channel else None)
        return
    if args.cmd == "send-file":
        with open(args.file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        limit = 25 if args.summary else 60
        body = "".join(lines[:limit])
        send_multi(f"BidHunter 标讯日报 {datetime.now():%m-%d}", body, config)
        return
    if args.cmd == "history":
        rows = get_history(args.days)
        if not rows:
            print(f"近 {args.days} 天无推送记录")
            return
        print(f"{'时间':<20}{'通道':<10}{'状态':<8}重试  标题")
        for ts, ch, subj, st, rc, err in rows:
            print(f"{ts:<20}{ch:<10}{st:<8}{rc:<4}  {subj[:44]}"
                  + (f"  ⚠️{err[:40]}" if err else ""))
        return
    if args.cmd == "stats":
        st = get_stats()
        print(f"总计 {st['total']} 条 | 成功 {st['success']} | 失败 {st['failed']}")
        for ch, n, ok in st["by_channel"]:
            print(f"  {ch}: {n} 条（成功 {ok or 0}）")
        return
    if args.cmd == "health-check":
        hc = health_check(config)
        st = hc["stats"]
        print(f"近3天: 失败 {hc['recent_fail_3d']} / 成功 {hc['recent_ok_3d']}")
        if hc["alert"]:
            print("🚨 连续 3 天推送失败且无成功记录，触发告警！")
            mail_cfg = (config or {}).get("channels", {}).get("email")
            if mail_cfg and mail_cfg.get("enabled", True):
                send_email(mail_cfg, "[BidHunter告警] 推送连续失败",
                           f"近3天失败 {hc['recent_fail_3d']} 次、成功 0 次。\n"
                           f"请检查通道配置: python3 config_wizard.py")
        else:
            print("✅ 推送状态正常")
        return
    if args.cmd == "retry-failed":
        retry_failed(args.days, config)


if __name__ == "__main__":
    main()
