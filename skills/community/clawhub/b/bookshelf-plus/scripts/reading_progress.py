#!/usr/bin/env python3
"""
reading_progress.py — 閱讀進度打卡腳本
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# ── ANSI 顏色（純標準庫，無需 colorama）───────────────────────
class _C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[97m"

    BG_GREEN  = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_CYAN   = "\033[46m"


def _c(color, text):
    return f"{color}{text}{_C.RESET}"


def _bold(text):
    return f"{_C.BOLD}{text}{_C.RESET}"


# ── 路徑設定 ──────────────────────────────────────────────
BOOKSHELF_DIR = Path.home() / ".bookshelf-plus"
LOG_FILE      = BOOKSHELF_DIR / "reading_log.json"

# ── Notion Client（本地 import，與 bookshelf-plus 同層）─────
_script_dir = Path(__file__).parent
_parent_dir = _script_dir.parent

_notion_client = None


def _load_notion_client():
    global _notion_client
    if _notion_client is None:
        try:
            sys.path.insert(0, str(_script_dir))
            import notion_client as nc
            _notion_client = nc
        except ImportError:
            _notion_client = False
    return _notion_client if _notion_client else None


# ── 數據讀寫 ──────────────────────────────────────────────

def _load_log() -> dict:
    """讀取或初始化 reading_log.json"""
    if not LOG_FILE.exists():
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        _init_log()
    with LOG_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def _save_log(data: dict):
    """寫入 reading_log.json"""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = LOG_FILE.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(LOG_FILE)


def _init_log():
    """引導訊息 + 初始化空的日誌"""
    print(f"\n{_c(_C.CYAN, '📚 Bookshelf Plus — 閱讀進度追蹤')}")
    print(f"{_c(_C.DIM, '─' * 42)}")
    print("首次使用！已建立資料庫：")
    print(f"  {LOG_FILE}")
    print(f"\n{_c(_C.GREEN, '✅ 初始化完成，開始記錄你的閱讀旅程吧！')}\n")
    _save_log({"sessions": [], "streak": {"current": 0, "longest": 0, "last_date": ""}})


# ── Streak 計算 ───────────────────────────────────────────

def _update_streak(data: dict, today: date):
    """根據打卡日更新連續天數（streak）"""
    streak = data.get("streak", {"current": 0, "longest": 0, "last_date": ""})
    last_str = streak.get("last_date", "")

    if last_str:
        try:
            last = date.fromisoformat(last_str)
            delta = (today - last).days
        except ValueError:
            delta = -1  # 無效日期，強制歸零
    else:
        delta = -1

    if delta == 0:
        # 今日已打卡，不重複計算
        return
    elif delta == 1:
        # 昨天有打卡 → streak +1
        streak["current"] = streak.get("current", 0) + 1
    else:
        # 中斷或首次 → 重新計算
        streak["current"] = 1

    streak["last_date"] = today.isoformat()
    streak["longest"] = max(streak.get("longest", 0), streak["current"])
    data["streak"] = streak


# ── 查詢輔助 ──────────────────────────────────────────────

def _find_sessions_by_title(data: dict, title: str):
    """不分大小寫、部分匹配"""
    t = title.lower()
    return [s for s in data["sessions"] if t in s.get("book_title", "").lower()]


def _sessions_in_period(data: dict, period: str):
    """過濾特定時段內的打卡記錄"""
    today = date.today()
    if period == "week":
        start = today - timedelta(days=today.weekday())
    elif period == "month":
        start = today.replace(day=1)
    elif period == "year":
        start = today.replace(month=1, day=1)
    else:
        start = date.min

    sessions = [s for s in data["sessions"] if s.get("date", "") >= start.isoformat()]
    return sessions


def _calc_book_stats(sessions: list):
    """計算某本書的總頁數、平均閱讀速度"""
    if not sessions:
        return None, None
    total_pages = sum(s.get("pages_read", 0) for s in sessions)
    total_min   = sum(s.get("duration_minutes", 0) or 0 for s in sessions)
    days = (date.fromisoformat(sessions[-1]["date"]) -
            date.fromisoformat(sessions[0]["date"])).days + 1
    avg_per_day = total_pages / max(days, 1)
    return total_pages, round(avg_per_day, 1)


# ── Notion 同步 ──────────────────────────────────────────

def _notion_sync(args, total_pages_read: int, book_title: str):
    """同步閱讀進度到 Notion"""
    nc = _load_notion_client()
    if nc is None:
        print(f"  {_c(_C.YELLOW, '⚠  未找到 notion_client.py，跳過 Notion 同步')}")
        return

    NOTION_KEY = args.api_key or ""
    DATABASE_ID = args.database_id or ""

    if not NOTION_KEY or not DATABASE_ID:
        print(f"  {_c(_C.YELLOW, '⚠  缺少 Notion API Key 或 Database ID，跳過同步')}")
        return

    # 搜尋該書
    nc.NOTION_KEY  = NOTION_KEY
    nc.DATABASE_ID = DATABASE_ID

    pages = nc.search_pages(book_title, filter_object=True)
    if not pages:
        print(f"  {_c(_C.YELLOW, f'⚠  Notion 中找不到「{book_title}」，跳過同步')}")
        return

    page_id = pages[0]["id"]
    props   = pages[0]["properties"]

    # 取得現有閱讀頁數
    current = props.get("閱讀頁數", {}).get("number", 0) or 0
    new_total = current + total_pages_read

    # 更新 Notion
    result = nc.api_patch(f"/pages/{page_id}", {
        "properties": {
            "閱讀頁數": nc.make_number(new_total)
        }
    })

    notion_ok = result.get("id", "")
    if notion_ok:
        print(f"  {_c(_C.CYAN, '🔄 Notion 已同步：閱讀頁數更新為')} {_c(_C.GREEN, str(new_total))}")
    else:
        print(f"  {_c(_C.RED, '⚠  Notion 同步失敗')}")


# ── 命令實作 ─────────────────────────────────────────────

def cmd_checkin(args):
    data  = _load_log()
    today = date.today()
    today_str = today.isoformat()

    # 防重複打卡（同一天同一本書）
    dup = next(
        (s for s in data["sessions"]
         if s["date"] == today_str and s.get("book_title", "").lower() == args.title.lower()),
        None
    )
    if dup:
        print(f"\n{_c(_C.YELLOW, '⚠  今日「' + args.title + '」已有打卡記錄')}")
        print(f"  已記錄：{dup['pages_read']} 頁，{dup.get('duration_minutes', '?')} 分鐘")
        resp = input(f"\n{_c(_C.BOLD, '是否追加閱讀頁數？(y/N): ')}").strip().lower()
        if resp != "y":
            print("已取消。")
            return
        dup["pages_read"]        += args.pages
        dup["duration_minutes"]   = (dup.get("duration_minutes") or 0) + (args.duration or 0)
        if args.note:
            dup["note"] = (dup.get("note", "") + " | " + args.note).strip()
        _save_log(data)
    else:
        session = {
            "date":               today_str,
            "book_title":         args.title,
            "isbn":               args.isbn    or "",
            "pages_read":         args.pages,
            "duration_minutes":   args.duration or 0,
            "note":               args.note    or "",
        }
        data["sessions"].append(session)
        _update_streak(data, today)
        _save_log(data)

    # ── 輸出摘要 ──
    book_sessions = _find_sessions_by_title(data, args.title)
    total_pages, avg = _calc_book_stats(book_sessions)

    # 總頁數（從 Notion 或 session 推估）
    total_book_pages = args.total_pages or 0

    print(f"\n{_c(_C.BG_GREEN, '  ✅ 打卡成功  ')}")
    print(f"  {_c(_C.BOLD, '📖')}  {_c(_C.WHITE, args.title)}")
    print(f"  {_c(_C.BOLD, '📄')}  今日閱讀：{args.pages} 頁", end="")
    if args.duration:
        print(f"  |  {_c(_C.BOLD, '⏱')}  {args.duration} 分鐘")
    else:
        print()

    if args.note:
        print(f"  {_c(_C.BOLD, '📝')}  {args.note}")

    if total_pages:
        print(f"\n  {_c(_C.DIM, '─' * 36)}")
        print(f"  📊 累計閱讀：{total_pages} 頁（{len(book_sessions)} 次打卡）")
        if avg:
            print(f"  📈 平均速度：{avg} 頁/天")
        if total_book_pages:
            pct = min(100, round(total_pages / total_book_pages * 100, 1))
            bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
            print(f"  📐 進度：[{bar}] {pct}%")

    streak = data["streak"]
    print(f"\n  {_c(_C.YELLOW, '🔥')}  連續打卡：{streak['current']} 天（最高 {streak['longest']} 天）")

    # Notion 同步
    if args.sync:
        _notion_sync(args, args.pages, args.title)


def cmd_status(args):
    data  = _load_log()
    today = date.today()
    today_str = today.isoformat()

    sessions = _find_sessions_by_title(data, args.title)
    if not sessions:
        print(f"\n{_c(_C.RED, '❌ 查無「' + args.title + '」的閱讀記錄')}")
        return

    # 累積頁數 & 速度
    total_pages, avg = _calc_book_stats(sessions)
    total_min = sum(s.get("duration_minutes", 0) or 0 for s in sessions)

    # 起始日 & 結束日
    start_date = date.fromisoformat(sessions[0]["date"])
    end_date   = date.fromisoformat(sessions[-1]["date"])
    span_days  = (end_date - start_date).days + 1

    # 最近一次打卡
    last = sessions[-1]
    days_since = (today - end_date).days

    # 計算進度 %
    total_book_pages = args.total_pages or 0
    pct = round(total_pages / total_book_pages * 100, 1) if total_book_pages else None

    print(f"\n{_c(_C.CYAN, '📖 ' + args.title)}")
    print(f"  {_c(_C.DIM, '─' * 40)}")
    print(f"  累計閱讀：{total_pages} 頁 / {total_book_pages or '?'} 頁")
    if pct is not None:
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"  進度：[{bar}] {pct}%")
    print(f"  打卡次數：{len(sessions)} 次")
    print(f"  閱讀天數：{span_days} 天（{start_date} ～ {end_date}）")
    print(f"  平均速度：{avg} 頁/天")
    print(f"  總閱讀時長：{total_min} 分鐘")

    if days_since == 0:
        last_label = _c(_C.GREEN, "今天")
    elif days_since == 1:
        last_label = _c(_C.YELLOW, "昨天")
    else:
        last_label = f"{days_since} 天前"
    print(f"  最近打卡：{last_date}（{last_label}）", end="")
    if last.get("note"):
        print(f"\n  最新筆記：{last['note']}")
    else:
        print()


def cmd_streak(args):
    data   = _load_log()
    streak = data.get("streak", {})
    cur    = streak.get("current", 0)
    best   = streak.get("longest", 0)
    last   = streak.get("last_date", "")

    print(f"\n{_c(_C.YELLOW, '🔥 閱讀連續天數')}")
    print(f"  {_c(_C.DIM, '─' * 30)}")

    if cur > 0:
        print(f"  目前：{_c(_C.BOLD, str(cur))} 天")
    else:
        print(f"  目前：{_c(_C.DIM, '0 天（還沒開始打卡！）')}")

    print(f"  歷史最高：{best} 天")

    if last:
        days_ago = (date.today() - date.fromisoformat(last)).days
        if days_ago == 0:
            ago = _c(_C.GREEN, "今天")
        elif days_ago == 1:
            ago = _c(_C.YELLOW, "昨天")
        else:
            ago = f"{days_ago} 天前"
        print(f"  上次打卡：{last}（{ago}）")

    if cur > best - 1 and cur > 0:
        print(f"\n  {_c(_C.GREEN, '🎉 保持勢頭！')}")
    elif cur == 0 and best > 0:
        print(f"\n  {_c(_C.YELLOW, '💡 重新開始挑戰吧！')}")
    print()


def cmd_stats(args):
    data    = _load_log()
    period  = args.period
    sessions = _sessions_in_period(data, period)

    if not sessions:
        print(f"\n{_c(_C.DIM, '📊 ' + period.capitalize() + ' 統計報告')}")
        print(f"  {_c(_C.DIM, '─' * 36)}")
        print(f"  暂无阅读记录。\n")
        return

    # ── 全域統計 ──
    total_pages   = sum(s.get("pages_read", 0) for s in sessions)
    total_min     = sum(s.get("duration_minutes", 0) or 0 for s in sessions)
    books_read    = len({s.get("book_title", "").lower() for s in sessions})
    days_with_log = len({s["date"] for s in sessions})
    avg_per_day   = round(total_pages / max(days_with_log, 1), 1)

    today = date.today()
    if period == "week":
        start = today - timedelta(days=today.weekday())
        period_label = f"{start} ～ {today}"
    elif period == "month":
        period_label = f"{today.year}-{today.month:02d}"
    elif period == "year":
        period_label = f"{today.year}"
    else:
        period_label = "全時間"

    # ── 按書分組 ──
    from collections import defaultdict
    by_book = defaultdict(list)
    for s in sessions:
        by_book[s.get("book_title", "未知")].append(s)

    # ── 輸出 Markdown 表格 ──
    print(f"\n{_c(_C.CYAN, '📊 ' + period.capitalize() + ' 閱讀統計報告')}")
    print(f"  {_c(_C.DIM, '─' * 46)}")
    print(f"  📅 統計區間：{period_label}")
    print(f"  📚 閱讀書籍：{books_read} 本")
    print(f"  📄 總閱讀頁數：{total_pages} 頁")
    print(f"  ⏱  總閱讀時長：{total_min} 分鐘")
    print(f"  📆 打卡天數：{days_with_log} 天")
    print(f"  📈 日均閱讀：{avg_per_day} 頁/天")

    print(f"\n{_c(_C.BOLD, '  📖 各書閱讀概況')}")
    print(f"  | {'書名':<20} | {'頁數':>5} | {'次數':>4} | {'均速':>6} |")
    print(f"  |{'-' * 21}|{'-' * 7}|{'-' * 6}|{'-' * 8}|")

    for title, sess in sorted(by_book.items(), key=lambda x: sum(s.get("pages_read", 0) for s in x[1]), reverse=True):
        pages   = sum(s.get("pages_read", 0) for s in sess)
        cnt     = len(sess)
        spd     = round(pages / max(cnt, 1), 1)
        display = (title[:18] + "…") if len(title) > 19 else title
        print(f"  | {display:<20} | {pages:>5} | {cnt:>4} | {spd:>6} |")

    print()


def cmd_history(args):
    data     = _load_log()
    sessions = _find_sessions_by_title(data, args.title)

    if not sessions:
        print(f"\n{_c(_C.RED, '❌ 查無「' + args.title + '」的閱讀記錄')}")
        return

    total_pages, avg = _calc_book_stats(sessions)

    print(f"\n{_c(_C.CYAN, '📖 ' + args.title + ' — 閱讀歷史')}")
    print(f"  {_c(_C.DIM, '─' * 46)}")
    print(f"  累計：{total_pages} 頁 · {avg} 頁/天 · {len(sessions)} 次打卡\n")
    print(f"  | {'日期':<12} | {'頁數':>5} | {'時長':>6} | {'備註':<20} |")
    print(f"  |{'-' * 13}|{'-' * 7}|{'-' * 8}|{'-' * 21}|")

    for s in sessions:
        d   = s["date"]
        p   = s.get("pages_read", 0)
        m   = s.get("duration_minutes", 0) or 0
        nte = (s.get("note", "") or "")[:20]
        note_display = nte + ("…" if len(s.get("note", "") or "") > 20 else "")
        print(f"  | {d:<12} | {p:>5} | {m:>6} | {note_display:<20} |")

    print()


# ── CLI 主體 ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="📚 閱讀進度打卡腳本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例：
  打卡：  python3 reading_progress.py checkin --title "原子習慣" --pages 30 --duration 45
  進度：  python3 reading_progress.py status  --title "原子習慣"
  統計：  python3 reading_progress.py stats  --period week
  連續：  python3 reading_progress.py streak
  歷史：  python3 reading_progress.py history --title "原子習慣"
"""
    )
    parser.add_argument("--api-key",     default="", help="Notion Integration Token")
    parser.add_argument("--database-id", default="", help="Notion Database ID")

    sub = parser.add_subparsers(dest="cmd", metavar="COMMAND")

    # ── checkin ──
    p = sub.add_parser("checkin", help="每日打卡")
    p.add_argument("--title",       required=True, help="書名")
    p.add_argument("--isbn",        default="",   help="ISBN（選填）")
    p.add_argument("--pages",       type=int, required=True, help="閱讀頁數")
    p.add_argument("--duration",    type=int, default=0,    help="閱讀時長（分鐘）")
    p.add_argument("--total-pages", type=int, default=0,   help="該書總頁數（用於計算進度）")
    p.add_argument("--note",         default="",   help="閱讀筆記（選填）")
    p.add_argument("--sync",        action="store_true",  help="同步至 Notion")

    # ── status ──
    p = sub.add_parser("status", help="查進度")
    p.add_argument("--title",       required=True, help="書名")
    p.add_argument("--total-pages", type=int, default=0, help="該書總頁數")

    # ── streak ──
    sub.add_parser("streak", help="連續天數")

    # ── stats ──
    p = sub.add_parser("stats", help="統計報告")
    p.add_argument("--period", default="week",
                   choices=["week", "month", "year", "all"],
                   help="統計週期（預設 week）")

    # ── history ──
    p = sub.add_parser("history", help="歷史記錄")
    p.add_argument("--title", required=True, help="書名")

    args = parser.parse_args()

    if args.cmd == "checkin":
        cmd_checkin(args)
    elif args.cmd == "status":
        cmd_status(args)
    elif args.cmd == "streak":
        cmd_streak(args)
    elif args.cmd == "stats":
        cmd_stats(args)
    elif args.cmd == "history":
        cmd_history(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
