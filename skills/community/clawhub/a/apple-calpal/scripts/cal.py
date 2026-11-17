# -*- coding: utf-8 -*-
"""
cal.py —— apple-calpal 的日历读写（iCloud CalDAV，纯 Python 标准库，零第三方依赖）。

子命令:
    calendars                       列出 iCloud 里所有日历（名字 + URL）
    query  --date 2026-10-03        查某天的事件（--days N 查 N 天；--calendar 名 只查一个日历）
    push   plan.json [--dry-run]    批量写入事件，输入格式见 SKILL.md
    cancel --date 2026-10-03        删除某天**本 skill 写入的**事件（只认 calpal- 前缀 UID）
    cancel --uid <uid>              按 UID 精确删除一条

安全设计:
    - cancel 只碰 calpal- 前缀的事件，用户手工加的、老课表管道写入的（cumtb- 前缀）
      一律不碰 —— 承诺类数据删错一条，学期后头的提醒全完。
    - 写入的 UID 由内容推导（确定性），同样的内容重推是覆盖不是重复。
"""

import base64
import datetime
import hashlib
import json
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from xml.etree import ElementTree as ET

TIMEOUT = 30
UID_PREFIX = "calpal-"
PROFILE_PATH = Path(__file__).resolve().parent.parent / "data" / "profile.json"


def die(msg, hint=""):
    print("[错误] " + msg, file=sys.stderr)
    if hint:
        print("       " + hint, file=sys.stderr)
    sys.exit(1)


def load_profile():
    try:
        with open(PROFILE_PATH, encoding="utf-8") as f:
            p = json.load(f)
    except FileNotFoundError:
        die("找不到 %s" % PROFILE_PATH, "skill 目录必须完整拷贝，data/ 不能丢")
    if not p.get("apple_id") or not p.get("app_password"):
        die("data/profile.json 里没填 apple_id / app_password")
    return p


# ---------------------------------------------------------------- HTTP / CalDAV
class Dav:
    """iCloud CalDAV 的最小客户端。Basic auth + PROPFIND/PUT/DELETE/MKCALENDAR。"""

    def __init__(self, base, user, pwd):
        self.base = base
        self.token = base64.b64encode(("%s:%s" % (user, pwd)).encode()).decode()

    def _raw(self, method, url, body=None, depth=None, ctype=None):
        r = urllib.request.Request(url, data=body.encode("utf-8") if body else None,
                                   method=method)
        r.add_header("Authorization", "Basic " + self.token)
        r.add_header("User-Agent", "apple-calpal/1.0")
        if ctype:
            r.add_header("Content-Type", ctype)
        if depth is not None:
            r.add_header("Depth", str(depth))
        try:
            with urllib.request.urlopen(r, timeout=TIMEOUT) as resp:
                return resp.status, resp.read()
        except urllib.error.HTTPError as e:
            return e.code, e.read()
        except urllib.error.URLError as e:
            die("连不上 iCloud：%s" % e.reason,
                "检查 NAS 的网络，或代理是否拦截了 caldav.icloud.com")

    def dav(self, method, url, body=None, depth=None, ctype=None):
        if ctype is None and method in ("PROPFIND", "REPORT", "MKCALENDAR"):
            ctype = 'application/xml; charset="utf-8"'
        status, content = self._raw(method, url, body, depth, ctype)
        if status == 401:
            die("Apple ID 或 App 专用密码不对（401）",
                "必须用 App 专用密码（appleid.apple.com 生成），不是登录密码")
        if status == 403:
            die("被拒绝（403）",
                "确认这个 Apple ID 已开双重认证和 iCloud 日历")
        return status, content


def tags(root, name):
    """命名空间无关查找，iCloud 换 XML 前缀也不怕。"""
    return [el for el in root.iter() if el.tag.split("}")[-1] == name]


def first_text(root, name):
    els = tags(root, name)
    if not els:
        return None
    for el in els[0].iter():
        if el.tag.split("}")[-1] == "href" and el.text:
            return el.text.strip()
    return (els[0].text or "").strip() or None


def connect(prof):
    cli = Dav(prof["caldav_base"], prof["apple_id"], prof["app_password"])
    s, c = cli.dav("PROPFIND", prof["caldav_base"],
                   '<?xml version="1.0" encoding="UTF-8"?>'
                   '<d:propfind xmlns:d="DAV:"><d:prop>'
                   "<d:current-user-principal/></d:prop></d:propfind>", depth=0)
    principal = urllib.parse.urljoin(prof["caldav_base"], first_text(ET.fromstring(c), "current-user-principal"))
    s, c = cli.dav("PROPFIND", principal,
                   '<?xml version="1.0" encoding="UTF-8"?>'
                   '<d:propfind xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">'
                   "<d:prop><c:calendar-home-set/></d:prop></d:propfind>", depth=0)
    home = urllib.parse.urljoin(prof["caldav_base"], first_text(ET.fromstring(c), "calendar-home-set"))
    s, c = cli.dav("PROPFIND", home,
                   '<?xml version="1.0" encoding="UTF-8"?>'
                   '<d:propfind xmlns:d="DAV:"><d:prop>'
                   "<d:displayname/><d:resourcetype/></d:prop></d:propfind>", depth=1)
    calendars = {}
    for resp in tags(ET.fromstring(c), "response"):
        href = first_text(resp, "href")
        rt = tags(resp, "resourcetype")
        is_cal = rt and any(x.tag.split("}")[-1] == "calendar" for x in rt[0].iter())
        if is_cal and href:
            name_els = tags(resp, "displayname")
            name = (name_els[0].text or "").strip() if name_els and name_els[0].text else ""
            calendars[name] = urllib.parse.urljoin(home, href)
    return cli, home, calendars


def get_calendar(prof, cli, home, calendars, name):
    """按名字找日历；行程日历不存在就自动建（承诺日历不允许静默新建）。"""
    if name in calendars:
        return calendars[name]
    if name == prof["calendars"]["commitments"]:
        die("找不到承诺日历「%s」" % name,
            "承诺数据关系课表提醒，不允许静默新建。先在 iPhone 日历 App 里建好，或检查 profile.json 的 calendars 配置")
    print("  日历「%s」不存在，新建..." % name, file=sys.stderr)
    body = ('<?xml version="1.0" encoding="UTF-8"?>'
            '<c:mkcalendar xmlns:d="DAV:" xmlns:c="urn:ietf:params:xml:ns:caldav">'
            "<d:set><d:prop><d:displayname>%s</d:displayname>"
            '<c:supported-calendar-component-set><c:comp name="VEVENT"/>'
            "</c:supported-calendar-component-set>"
            "</d:prop></d:set></c:mkcalendar>" % name)
    # ↑ <c:comp> 是自闭合的，不要给它补 </c:comp>，补了整段 XML 非法、MKCALENDAR 必挂
    # iCloud 的日历路径段必须是 UUID，中文名直接 403
    url = home.rstrip("/") + "/" + str(uuid.uuid4()).upper() + "/"
    s, c = cli.dav("MKCALENDAR", url, body)
    if s not in (200, 201, 204):
        die("建日历失败（%d）" % s, c.decode("utf-8", "replace")[:300])
    return url


# ---------------------------------------------------------------- ICS 文本
def esc(s):
    return (s.replace("\\", "\\\\").replace(";", "\\;")
             .replace(",", "\\,").replace("\r\n", "\\n").replace("\n", "\\n"))


def fold(line):
    """RFC 5545：每行 ≤75 字节，按 UTF-8 字节折行，不切坏汉字。"""
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    out, cur, limit = [], b"", 75
    for ch in line:
        cb = ch.encode("utf-8")
        if len(cur + cb) > limit:
            out.append(cur.decode("utf-8"))
            cur, limit = b" ", 74
        cur += cb
    out.append(cur.decode("utf-8"))
    return "\r\n".join(out)


def hhmm(t):
    """归一化成 HH:MM。模型偶尔会给 '8:05' 或 '0805'，不归一会写坏 DTSTART。"""
    t = str(t).strip().replace(":", "").zfill(4)
    if len(t) != 4 or not t.isdigit():
        die("时间格式不对：%r（要 HH:MM）" % t)
    return "%s:%s" % (t[:2], t[2:])


def stamp(date_str, hm):
    d = datetime.date.fromisoformat(date_str)
    return "%04d%02d%02dT%s00" % (d.year, d.month, d.day, hm.replace(":", ""))


def calendar_body(vevent_lines):
    """PUT 正文：单 VEVENT 的 VCALENDAR。不能带 METHOD（会被当 iTIP 邀请）。"""
    L = ["BEGIN:VCALENDAR", "VERSION:2.0",
         "PRODID:-//ZhongZiheng//apple-calpal//CN", "CALSCALE:GREGORIAN"]
    L += vevent_lines
    L.append("END:VCALENDAR")
    return "\r\n".join(fold(x) for x in L) + "\r\n"


def unfold(text):
    out = []
    for line in text.replace("\r\n", "\n").split("\n"):
        if line[:1] in (" ", "\t") and out:
            out[-1] += line[1:]
        else:
            out.append(line)
    return out


def parse_vevents(text):
    """把一份 ICS 资源拆成事件 dict 列表。iCloud 可能在同一资源里补第二个 UID 行。"""
    events, cur = [], None
    for line in unfold(text):
        if line == "BEGIN:VEVENT":
            cur = {"uids": []}
        elif line == "END:VEVENT":
            if cur is not None:
                events.append(cur)
            cur = None
        elif cur is not None:
            if line.startswith("UID:"):
                cur["uids"].append(line[4:].strip())
            elif line.startswith("SUMMARY:"):
                cur.setdefault("title", line[8:].strip())
            elif line.startswith("LOCATION:"):
                cur.setdefault("location", line[9:].strip())
            elif line.startswith("DESCRIPTION:"):
                cur.setdefault("note", line[12:].strip())
            elif line.startswith("DTSTART"):
                v = line.split(":", 1)[-1].strip()
                cur.setdefault("date", v[:8])
                cur.setdefault("start", v[9:13] if len(v) >= 13 else "")
            elif line.startswith("DTEND"):
                v = line.split(":", 1)[-1].strip()
                cur.setdefault("end", v[9:13] if len(v) >= 13 else "")
    return events


def fmt_hhmm(hhmm_str):
    return "%s:%s" % (hhmm_str[:2], hhmm_str[2:4]) if len(hhmm_str) >= 4 else hhmm_str


# ---------------------------------------------------------------- 事件展开
def expand_dates(ev, default_week1_monday, skip_dates):
    """事件给 date 就直用；给 weekday+weeks 就按学期起点展开成具体日期。"""
    if ev.get("date"):
        return [ev["date"]]
    wd, weeks = ev.get("weekday"), ev.get("weeks")
    if not wd or not weeks:
        die("事件既没有 date 也没有 weekday+weeks，无法确定日期：%s" % json.dumps(ev, ensure_ascii=False))
    w1m = ev.get("week1_monday") or default_week1_monday
    if not w1m:
        die("周次事件需要 week1_monday（学期第一周周一），事件或文件顶层都没有")
    base = datetime.date.fromisoformat(w1m)
    base -= datetime.timedelta(days=base.weekday())
    skip = set(skip_dates or [])
    return [(base + datetime.timedelta(weeks=w - 1, days=int(wd) - 1)).isoformat()
            for w in weeks if (base + datetime.timedelta(weeks=w - 1, days=int(wd) - 1)).isoformat() not in skip]


def make_uid(cal_name, title, date_str, start):
    key = hashlib.md5(("%s|%s|%s|%s" % (cal_name, title, date_str, start))
                      .encode("utf-8")).hexdigest()[:12]
    return "%s%s-%s@calpal" % (UID_PREFIX, date_str.replace("-", ""), key)


def build_vevent(cal_name, ev):
    date_str, start, end = ev["date"], hhmm(ev["start"]), hhmm(ev["end"])
    uid = ev.get("uid") or make_uid(cal_name, ev["title"], date_str, start)
    alarm = ev.get("alarm_minutes", None)
    alarm = int(alarm) if alarm is not None else 0
    alarm_text = "马上开始：%s" % ev["title"] if alarm <= 0 else \
                 "还有 %d 分钟：%s" % (alarm, ev["title"])
    if ev.get("note"):
        alarm_text += "（%s）" % ev["note"]
    has_alarm = ev.get("alarm_minutes") is not None
    alarm_text = ("马上开始：" + ev["title"] if alarm <= 0 else
                  "还有 %d 分钟：" % alarm + ev["title"])
    if ev.get("note"):
        alarm_text += "（" + ev["note"] + "）"
    lines = [
        "BEGIN:VEVENT",
        "UID:" + uid,
        "DTSTAMP:" + datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "DTSTART:" + stamp(date_str, start),
        "DTEND:" + stamp(date_str, end),
        "SUMMARY:" + esc(ev["title"]),
        "LOCATION:" + esc(ev.get("location") or ""),
        "DESCRIPTION:" + esc(ev.get("note") or ""),
    ]
    if has_alarm:
        lines += [
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            "TRIGGER:-PT%dM" % max(alarm, 0),
            "DESCRIPTION:" + esc(alarm_text),
            "END:VALARM",
        ]
    lines.append("END:VEVENT")
    return uid, lines


# ---------------------------------------------------------------- 子命令
def cmd_calendars(prof):
    _cli, _home, calendars = connect(prof)
    print("iCloud 里的日历：")
    for name, url in sorted(calendars.items()):
        print("  %-16s %s" % (name or "(无名)", url))


def collect_events(cli, cal_url, cal_name, d1, d2):
    """列出 [d1, d2] 区间内该日历的事件（全部来源，不只 calpal-）。

    用 REPORT calendar-query 让服务器端按时间过滤 —— 一个日历一次请求。
    之前逐资源 GET 的做法，课表日历 68 个事件就是 68 轮 HTTPS，慢到没法用。
    time-range 要求 UTC；事件是浮动本地时间，边界差由「范围放宽一天 +
    客户端再按 DTSTART 精确过滤」兜底。
    """
    start = (d1 - datetime.timedelta(days=1)).strftime("%Y%m%dT000000Z")
    end = (d2 + datetime.timedelta(days=2)).strftime("%Y%m%dT000000Z")
    body = ('<?xml version="1.0" encoding="UTF-8"?>'
            '<C:calendar-query xmlns:D="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav">'
            "<D:prop><C:calendar-data/></D:prop>"
            '<C:filter><C:comp-filter name="VCALENDAR">'
            '<C:comp-filter name="VEVENT">'
            '<C:time-range start="%s" end="%s"/>'
            "</C:comp-filter></C:comp-filter></C:filter></C:calendar-query>"
            % (start, end))
    s, c = cli.dav("REPORT", cal_url, body, depth=1)
    if s not in (200, 207):
        die("查询失败（%d）" % s, c.decode("utf-8", "replace")[:300])
    found = []
    for resp in tags(ET.fromstring(c), "response"):
        href = first_text(resp, "href")
        data = tags(resp, "calendar-data")
        if not href or not data or not (data[0].text or "").strip():
            continue
        url = urllib.parse.urljoin(cal_url, href)
        for ev in parse_vevents(data[0].text):
            if not ev.get("date"):
                continue
            try:
                d = datetime.datetime.strptime(ev["date"], "%Y%m%d").date()
            except ValueError:
                continue
            if d1 <= d <= d2:
                found.append({
                    "calendar": cal_name,
                    "url": url,
                    "uid": next((u for u in ev["uids"] if u.startswith(UID_PREFIX)),
                                ev["uids"][0] if ev["uids"] else ""),
                    "title": ev.get("title", ""),
                    "date": d.isoformat(),
                    "start": fmt_hhmm(ev.get("start", "")),
                    "end": fmt_hhmm(ev.get("end", "")),
                    "location": ev.get("location", ""),
                    "note": ev.get("note", ""),
                })
    found.sort(key=lambda e: (e["date"], e["start"]))
    return found


def cmd_query(prof, args):
    if not args.get("date"):
        die("query 需要 --date YYYY-MM-DD")
    d1 = datetime.date.fromisoformat(args["date"])
    d2 = d1 + datetime.timedelta(days=int(args.get("days", 1)) - 1)
    cli, _home, calendars = connect(prof)
    if args.get("calendar"):
        calendars = {k: v for k, v in calendars.items() if k == args["calendar"]}
    events = []
    for name, url in calendars.items():
        events += collect_events(cli, url, name, d1, d2)
    events.sort(key=lambda e: (e["date"], e["start"]))
    print(json.dumps({"range": [d1.isoformat(), d2.isoformat()],
                      "count": len(events), "events": events},
                     ensure_ascii=False, indent=2))


def cmd_push(prof, args):
    if not args.get("file"):
        die("push 需要 plan.json 文件路径")
    try:
        with open(args["file"], encoding="utf-8") as f:
            plan = json.load(f)
    except FileNotFoundError:
        die("找不到输入文件 %s" % args["file"])
    except json.JSONDecodeError as e:
        die("plan.json 不是合法 JSON：%s" % e)

    cal_name = args.get("calendar") or plan.get("calendar") or prof["calendars"]["plans"]
    week1m = plan.get("week1_monday")
    skip = plan.get("skip_dates") or []
    default_alarm = prof["default_alarm_minutes"].get(
        "commitments" if cal_name == prof["calendars"]["commitments"] else "plans", 30)

    todo = []
    for ev in plan.get("events", []):
        if not ev.get("title") or not ev.get("start") or not ev.get("end"):
            die("事件缺 title/start/end：%s" % json.dumps(ev, ensure_ascii=False))
        # 偏好：默认不设提醒；只有事件显式给了非 None 的 alarm_minutes 才写 VALARM
        ev["alarm_minutes"] = ev.get("alarm_minutes")
        if ev["alarm_minutes"] is None:
            ev["alarm_minutes"] = plan.get("default_alarm_minutes")
            if ev["alarm_minutes"] is None:
                ev["alarm_minutes"] = prof["default_alarm_minutes"].get(
                    "commitments" if cal_name == prof["calendars"]["commitments"] else "plans")
        for d in expand_dates(ev, week1m, skip):
            e = dict(ev, date=d)
            uid, lines = build_vevent(cal_name, e)
            todo.append((uid, lines, e))
    if not todo:
        die("没有可写入的事件（全是空周次或全被 skip_dates 排除？）")

    if args.get("dry_run"):
        print("dry-run：将写入 %d 条到「%s」：" % (len(todo), cal_name))
        for uid, _lines, e in todo:
            print("  %s  %s-%s  %s%s" % (e["date"], e["start"], e["end"], e["title"],
                  " @%s" % e["location"] if e.get("location") else ""))
        return

    cli, home, calendars = connect(prof)
    target = get_calendar(prof, cli, home, calendars, cal_name)
    ok = 0
    for uid, lines, e in todo:
        url = target.rstrip("/") + "/" + urllib.parse.quote(uid, safe="") + ".ics"
        s, body = cli.dav("PUT", url, calendar_body(lines), ctype="text/calendar; charset=utf-8")
        if s not in (200, 201, 204):
            die("写入失败 %s（%d）" % (uid, s), body.decode("utf-8", "replace")[:300])
        print("  [ok] %s  %s %s-%s  %s" % (e["date"], e["start"], e["end"], e["title"], uid))
        ok += 1
    print("已写入 %d 条到「%s」。几秒内同步到 iPhone。" % (ok, cal_name))


def cmd_cancel(prof, args):
    cli, _home, calendars = connect(prof)

    if args.get("uid"):
        # 按 UID 精确删：扫全部日历找到那条资源的 URL
        for name, url in calendars.items():
            s, c = cli.dav("PROPFIND", url,
                           '<?xml version="1.0" encoding="UTF-8"?>'
                           '<d:propfind xmlns:d="DAV:"><d:prop><d:getetag/></d:prop>'
                           "</d:propfind>", depth=1)
            for resp in tags(ET.fromstring(c), "response"):
                href = first_text(resp, "href")
                if not href or not href.rstrip("/").endswith(".ics"):
                    continue
                item = urllib.parse.urljoin(url, href)
                s, body = cli._raw("GET", item)
                if s == 200 and any(l.startswith("UID:" + args["uid"])
                                    for l in unfold(body.decode("utf-8", "replace"))):
                    cli.dav("DELETE", item)
                    print("已删除 %s（%s）" % (args["uid"], name))
                    return
        die("所有日历里都没找到 UID=%s" % args["uid"])

    if not args.get("date"):
        die("cancel 需要 --uid 或 --date")
    cal_name = args.get("calendar") or prof["calendars"]["plans"]
    if cal_name == prof["calendars"]["commitments"] and not args.get("force"):
        die("「%s」是承诺日历，批量删除被拒绝" % cal_name,
            "确认要动承诺数据就加 --force；平时取消临时安排不要指定这个日历")
    d = datetime.date.fromisoformat(args["date"])
    target = calendars.get(cal_name)
    if not target:
        die("找不到日历「%s」" % cal_name)
    found = [e for e in collect_events(cli, target, cal_name, d, d)
             if e["uid"].startswith(UID_PREFIX)]
    if args.get("title"):
        found = [e for e in found if args["title"] in e["title"]]
    if not found:
        print("该范围没有本 skill 写入的事件，什么都没动。")
        return
    for e in found:
        cli.dav("DELETE", e["url"])
        print("  已删 %s %s-%s  %s" % (e["date"], e["start"], e["end"], e["title"]))
    print("共删除 %d 条。" % len(found))
    foreign = [e for e in collect_events(cli, target, cal_name, d, d)
               if not e["uid"].startswith(UID_PREFIX)]
    if foreign:
        print("（该日还有 %d 条非本 skill 的事件未动：%s）" %
              (len(foreign), "、".join(e["title"] for e in foreign[:5])))


# ---------------------------------------------------------------- 入口
def main():
    args, pos = {}, []
    argv = sys.argv[1:]
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--"):
            key = a[2:].replace("-", "_")
            if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
                args[key] = argv[i + 1]
                i += 2
            else:
                args[key] = True
                i += 1
        else:
            pos.append(a)
            i += 1
    args["file"] = args.get("file") or (pos[1] if len(pos) > 1 and pos[0] == "push" else None)

    if not argv:
        print(__doc__)
        return
    cmd, prof = argv[0], load_profile()
    if cmd == "calendars":
        cmd_calendars(prof)
    elif cmd == "query":
        cmd_query(prof, args)
    elif cmd == "push":
        cmd_push(prof, args)
    elif cmd == "cancel":
        cmd_cancel(prof, args)
    else:
        die("未知子命令 %r" % cmd, "可用：calendars / query / push / cancel")


if __name__ == "__main__":
    main()
