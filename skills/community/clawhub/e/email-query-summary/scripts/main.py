import imaplib
import email
import json
import sys
import os
from email.header import decode_header
from datetime import datetime, timezone, timedelta
import calendar

# ---- 从 skill 根目录加载账户配置 ----
_skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_config_path = os.path.join(_skill_dir, "accounts.json")
_SETUP_HINT = "请阅读同目录 SETUP.md 配置 accounts.json"


def _error(msg: str, *, setup: bool = False) -> None:
    payload = {"error": msg}
    if setup:
        payload["setup_hint"] = _SETUP_HINT
    print(json.dumps(payload, ensure_ascii=False))
    sys.exit(1)


def _load_accounts():
    try:
        with open(_config_path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        _error(f"未找到配置文件: {_config_path}", setup=True)
    except json.JSONDecodeError as e:
        _error(f"配置文件 JSON 格式错误: {e}", setup=True)
    except Exception as e:
        _error(f"配置文件读取失败: {e}", setup=True)

    accounts = data.get("accounts")
    if not isinstance(accounts, list):
        _error("accounts.json 缺少 accounts 数组", setup=True)

    valid = [a for a in accounts if a.get("username") and a.get("password")]
    if not valid:
        _error("没有已启用的邮箱账户（username 或 password 为空），请先完成配置", setup=True)

    return valid


ACCOUNTS = _load_accounts()

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CST = timezone(timedelta(hours=8))

# ---------------------------------------------------------------------------
# 时间工具函数
# ---------------------------------------------------------------------------

def _today_cst() -> datetime:
    return datetime.now(CST).replace(hour=0, minute=0, second=0, microsecond=0)


def _day_range(base: datetime):
    return base, base.replace(hour=23, minute=59, second=59)


def _week_start(base: datetime) -> datetime:
    return base - timedelta(days=base.weekday())


def _month_range(year: int, month: int):
    last_day = calendar.monthrange(year, month)[1]
    start = datetime(year, month, 1, 0, 0, 0, tzinfo=CST)
    end = datetime(year, month, last_day, 23, 59, 59, tzinfo=CST)
    return start, end


def resolve_period(period: str):
    today = _today_cst()
    p = period.strip()

    if p in ("今天", "今日", "当天", "当日"):
        return _day_range(today)
    if p in ("昨天", "昨日"):
        return _day_range(today - timedelta(days=1))
    if p in ("前天", "前日"):
        return _day_range(today - timedelta(days=2))

    if p == "本周":
        start = _week_start(today)
        return start, (start + timedelta(days=6)).replace(hour=23, minute=59, second=59)
    if p == "上周":
        start = _week_start(today) - timedelta(weeks=1)
        return start, (start + timedelta(days=6)).replace(hour=23, minute=59, second=59)
    if p == "上上周":
        start = _week_start(today) - timedelta(weeks=2)
        return start, (start + timedelta(days=6)).replace(hour=23, minute=59, second=59)

    if p == "本月":
        return _month_range(today.year, today.month)
    if p == "上月":
        first = today.replace(day=1) - timedelta(days=1)
        return _month_range(first.year, first.month)
    if p == "上上月":
        first = today.replace(day=1) - timedelta(days=1)
        first = first.replace(day=1) - timedelta(days=1)
        return _month_range(first.year, first.month)

    for days in (3, 7, 14, 30):
        if p in (f"最近{days}天", f"最近 {days} 天"):
            start = today - timedelta(days=days - 1)
            return start, today.replace(hour=23, minute=59, second=59)

    return None, None


def normalize_date(s: str) -> str:
    s = s.strip()
    if len(s) <= 5:
        return f"{datetime.now(CST).year}-{s}"
    return s


def parse_args():
    args = sys.argv[1:]

    if not args:
        _error(
            "用法:\n"
            "  python main.py --period <关键词>\n"
            "  python main.py DATE_START [DATE_END]"
        )

    if args[0] == "--period":
        if len(args) < 2:
            _error("--period 后需要提供时间关键词，如：本周、上月、最近7天")
        start, end = resolve_period(args[1])
        if start is None:
            _error(f"不支持的时间关键词: {args[1]}")
        return start, end

    try:
        date_start = normalize_date(args[0])
        date_end = normalize_date(args[1]) if len(args) >= 2 else date_start
        start = datetime.strptime(date_start, "%Y-%m-%d").replace(tzinfo=CST)
        end = datetime.strptime(date_end, "%Y-%m-%d").replace(
            hour=23, minute=59, second=59, tzinfo=CST
        )
    except ValueError as e:
        _error(f"日期格式错误，请使用 YYYY-MM-DD 或 MM-DD: {e}")
    return start, end


# ---------------------------------------------------------------------------
# 邮件工具函数
# ---------------------------------------------------------------------------

def decode_str(s):
    if not s:
        return ""
    parts = decode_header(s)
    result = []
    for part, enc in parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            result.append(part)
    return "".join(result)


def get_body(msg):
    plain, html = "", ""
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            cd = str(part.get("Content-Disposition", ""))
            if "attachment" in cd:
                continue
            payload = part.get_payload(decode=True)
            if not payload:
                continue
            charset = part.get_content_charset() or "utf-8"
            decoded = payload.decode(charset, errors="replace")
            if ct == "text/plain":
                plain += decoded
            elif ct == "text/html" and not plain:
                html += decoded
    else:
        payload = msg.get_payload(decode=True)
        charset = msg.get_content_charset() or "utf-8"
        if payload:
            ct = msg.get_content_type()
            decoded = payload.decode(charset, errors="replace")
            if ct == "text/html":
                html = decoded
            else:
                plain = decoded
    return (plain or html).strip()[:3000]


def get_attachments(msg):
    attachments = []
    if msg.is_multipart():
        for part in msg.walk():
            cd = str(part.get("Content-Disposition", ""))
            if "attachment" in cd:
                filename = decode_str(part.get_filename() or "")
                size = len(part.get_payload(decode=True) or b"")
                attachments.append({"filename": filename, "size": size})
    return attachments


def parse_email_date(date_str):
    if not date_str:
        return None
    try:
        from email.utils import parsedate_to_datetime
        return parsedate_to_datetime(date_str).astimezone(CST)
    except Exception:
        return None


def fetch_account(account, start_dt, end_dt, imap_since, imap_before):
    results = []
    label = account.get("label") or account.get("username", "未知账户")
    try:
        mail = imaplib.IMAP4_SSL(account["host"], account["port"])
        mail.login(account["username"], account["password"])
    except Exception as e:
        return results, f"{label} 连接失败: {str(e)}"

    for folder in account.get("folders", ["INBOX"]):
        try:
            status, _ = mail.select(folder, readonly=True)
            if status != "OK":
                continue
            _, uids = mail.search(None, f'(SINCE "{imap_since}" BEFORE "{imap_before}")')
            uid_list = uids[0].split()
            for uid in uid_list:
                _, data = mail.fetch(uid, "(RFC822)")
                for part in data:
                    if isinstance(part, tuple):
                        msg = email.message_from_bytes(part[1])
                        date_obj = parse_email_date(msg.get("Date", ""))
                        if date_obj and not (start_dt <= date_obj <= end_dt):
                            continue
                        results.append({
                            "account": label,
                            "folder": folder,
                            "from": decode_str(msg.get("From", "")),
                            "to": decode_str(msg.get("To", "")),
                            "subject": decode_str(msg.get("Subject", "(无主题)")),
                            "date": date_obj.strftime("%Y-%m-%d %H:%M") if date_obj else "",
                            "body": get_body(msg),
                            "attachments": get_attachments(msg),
                        })
        except Exception:
            continue

    mail.logout()
    return results, None


def main():
    start_dt, end_dt = parse_args()

    imap_since = start_dt.strftime("%d-%b-%Y")
    imap_before = (end_dt + timedelta(days=1)).strftime("%d-%b-%Y")

    all_results = []
    errors = []

    for acc in ACCOUNTS:
        items, err = fetch_account(acc, start_dt, end_dt, imap_since, imap_before)
        all_results.extend(items)
        if err:
            errors.append(err)

    if errors and not all_results:
        _error(
            "所有邮箱账户均连接失败，请检查 accounts.json 中的授权码与 IMAP 参数。"
            f" 详情: {'; '.join(errors)}",
            setup=True,
        )

    output = {
        "period": {
            "start": start_dt.strftime("%Y-%m-%d"),
            "end": end_dt.strftime("%Y-%m-%d"),
        },
        "emails": all_results,
    }
    if errors:
        output["errors"] = errors

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
