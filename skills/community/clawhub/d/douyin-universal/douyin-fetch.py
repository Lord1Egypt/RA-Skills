#!/usr/bin/env python3
"""
douyin-fetch.py - 抖音抓取 skill 核心脚本

3 个子命令:
  1. search  <keyword> --type {video,user}    主题/人物搜索
  2. user    <nickname|sec_uid> --videos N    拿用户作品列表
  3. video   <aweme_id|url> --comments N      视频详情 + 评论

数据路径: search/user 走 HTTP API (general/search/single + aweme/post)
         video 的评论走 agent-browser eval 抓 [data-e2e="comment-item"]

cookie/state 路径由 paths.py 统一管理(默认 $SKILL/data/, 可用 DOUYIN_DATA_DIR 环境变量覆盖,
兼容老路径 /tmp/douyin/)
"""
import argparse
import json
import os
import re
import sys
import time
import subprocess
from pathlib import Path
from typing import Any, Optional
from urllib.parse import quote, unquote, urlparse

try:
    import requests
except ImportError:
    print("❌ 缺 requests: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from downloader import download_for_aweme
    HAS_DOWNLOADER = True
except ImportError:
    HAS_DOWNLOADER = False


# === 常量(路径由 paths.py 统一管理)===
from paths import COOKIE_FILE, STATE_FILE, DATA_DIR, TMP_DIR, EXPORTS_DIR

# 抖音 web 端通用查询参数(从 XHR 抓的,不带会被 verify_check 拦截)
COMMON_PARAMS = {
    "device_platform": "webapp",
    "aid": "6383",
    "channel": "channel_pc_web",
    "pc_client_type": "1",
    "version_code": "170400",
    "version_name": "17.4.0",
    "cookie_enabled": "true",
    "screen_width": "1536",
    "screen_height": "864",
    "browser_language": "zh-CN",
    "browser_platform": "Linux+x86_64",
    "browser_name": "Chrome",
    "browser_version": "120.0.0.0",
    "browser_online": "true",
    "engine_name": "Blink",
    "engine_version": "120.0.0.0",
    "os_name": "Linux",
    "os_version": "x86_64",
    "device_memory": "16",
    "platform": "PC",
    "downlink": "10",
    "effective_type": "4g",
    "round_trip_time": "50",
}

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


# === 工具函数 ===
def err(msg):
    print(f"❌ {msg}", file=sys.stderr)


def ok(msg):
    print(f"✅ {msg}")


def load_cookie() -> str:
    """读 /tmp/douyin/cookies.txt,返回 Cookie header 字符串"""
    p = Path(COOKIE_FILE)
    if not p.exists():
        err(f"cookie 文件不存在: {COOKIE_FILE}")
        err("→ 先跑 keepalive.py setup (从浏览器导 cookie)")
        sys.exit(2)
    raw = p.read_text().strip()
    parts = []
    for line in raw.split("\n"):
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        # Netscape 格式: domain TAB flag TAB path TAB secure TAB expiry TAB name TAB value
        # 也兼容: name=value
        if "\t" in line:
            cols = line.split("\t")
            if len(cols) >= 7:
                parts.append(f"{cols[5]}={cols[6]}")
            else:
                # 拿最后两列
                parts.append(f"{cols[-2]}={cols[-1]}")
        elif "=" in line:
            parts.append(line)
    if not parts:
        err("cookie 文件解析失败,确保是 Netscape 格式或 key=value 一行一个")
        sys.exit(2)
    return "; ".join(parts)


def fmt_num(n: int) -> str:
    """把 10000 格式化成 1.0万,12345 → 1.2万"""
    if n is None:
        return "0"
    if n < 10000:
        return str(n)
    if n < 100000000:
        w = n / 10000
        return f"{w:.1f}万" if w >= 10 else f"{w:.1f}万"
    e = n / 100000000
    return f"{e:.1f}亿"


def truncate(s: str, n: int = 100) -> str:
    if not s:
        return ""
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[:n] + "..."


def fmt_time(ts: int) -> str:
    if not ts:
        return "?"
    import datetime
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")


def relative_time(ts: int) -> str:
    if not ts:
        return "?"
    import datetime
    dt = datetime.datetime.fromtimestamp(ts)
    diff = datetime.datetime.now() - dt
    days = diff.days
    if days < 1:
        hours = diff.seconds // 3600
        if hours < 1:
            return "刚刚"
        return f"{hours}小时前"
    if days < 30:
        return f"{days}天前"
    if days < 365:
        return f"{days // 30}个月前"
    return f"{days // 365}年前"


def http_get(path: str, params: dict, cookie: str, timeout: int = 10) -> dict:
    """调抖音 API 端点,返回解析后的 JSON"""
    qp = {**COMMON_PARAMS, **params}
    qs = "&".join(f"{k}={quote(str(v))}" for k, v in qp.items())
    url = f"https://www.douyin.com{path}?{qs}"
    headers = {
        "User-Agent": UA,
        "Referer": "https://www.douyin.com/",
        "Cookie": cookie,
    }
    r = requests.get(url, headers=headers, timeout=timeout)
    if r.status_code != 200 or not r.text:
        raise RuntimeError(f"API 返回空: {r.status_code} (可能 cookie 过期)")
    try:
        return r.json()
    except json.JSONDecodeError as e:
        raise RuntimeError(f"API 响应不是 JSON: {e}; head={r.text[:200]}")


# === 1. search 子命令 ===
def cmd_search(args, cookie: str):
    kw = args.keyword
    if args.type == "video":
        d = http_get(
            "/aweme/v1/web/general/search/single/",
            {"keyword": kw, "search_type": "video", "count": args.limit},
            cookie,
        )
        items = [x.get("aweme_info") for x in (d.get("data") or []) if x.get("aweme_info")]
        if args.raw_out:
            Path(args.raw_out).write_text(json.dumps(d, ensure_ascii=False, indent=2))
        if args.full:
            print(json.dumps(d, ensure_ascii=False, indent=2))
            return
        # compact 模式
        if not items:
            print(f"⚠ '{kw}' 没搜到视频")
            return
        print(f"=== 视频搜索: {kw} (返回 {len(items)} 条) ===\n")
        for i, v in enumerate(items, 1):
            a = v.get("author") or {}
            tags = " ".join("#" + t.get("tag_name", "") for t in (v.get("text_extra") or []) if t.get("tag_name"))
            url = f"https://www.douyin.com/video/{v.get('aweme_id')}"
            print(f"[{i}] {truncate(v.get('desc', ''), 100)} ({fmt_num(v.get('statistics', {}).get('digg_count'))}赞) "
                  f"@{a.get('nickname', '?')} - {fmt_time(v.get('create_time'))}")
            print(f"    {url}")
            if tags:
                print(f"    {tags}")
            print()
    else:  # user
        d = http_get(
            "/aweme/v1/web/general/search/single/",
            {"keyword": kw, "search_type": "user", "count": args.limit},
            cookie,
        )
        users = []
        for x in (d.get("data") or []):
            users.extend(x.get("user_list", []) or [])
        if args.raw_out:
            Path(args.raw_out).write_text(json.dumps(d, ensure_ascii=False, indent=2))
        if args.full:
            print(json.dumps(d, ensure_ascii=False, indent=2))
            return
        if not users:
            print(f"⚠ '{kw}' 没搜到用户")
            return
        print(f"=== 用户搜索: {kw} (返回 {len(users)} 条) ===\n")
        for i, u in enumerate(users, 1):
            ui = u.get("user_info", u)
            url = f"https://www.douyin.com/user/{ui.get('sec_uid')}"
            print(f"[{i}] {ui.get('nickname', '?')} ({fmt_num(ui.get('follower_count'))}粉 / "
                  f"{ui.get('aweme_count', '?')}作品)")
            if ui.get("custom_verify"):
                print(f"    认证: {ui.get('custom_verify')}")
            if ui.get("signature"):
                print(f"    简介: {truncate(ui.get('signature'), 100)}")
            print(f"    抖音号: {ui.get('unique_id', '?')}")
            print(f"    {url}")
            print()


# === 2. user 子命令 ===
def cmd_user(args, cookie: str):
    q = args.query
    sec_uid = None
    user_info = None
    # 1) 先看是不是直接 sec_uid
    if q.startswith("MS4w") or re.match(r"^[A-Za-z0-9_-]{20,}$", q):
        sec_uid = q
    else:
        # 2) 用 search API 找
        d = http_get(
            "/aweme/v1/web/general/search/single/",
            {"keyword": q, "search_type": "user", "count": 5},
            cookie,
        )
        users = []
        for x in (d.get("data") or []):
            users.extend(x.get("user_list", []) or [])
        if not users:
            err(f"没找到用户: {q}")
            sys.exit(3)
        # 精确匹配优先
        exact = [u for u in users if (u.get("user_info", u).get("nickname") or "").lower() == q.lower()]
        if exact:
            ui = exact[0]["user_info"]
        else:
            ui = users[0].get("user_info", users[0])
            if len(users) > 1:
                print(f"⚠ '{q}' 匹配到多个,默认取第一个 @{ui.get('nickname')}({fmt_num(ui.get('follower_count'))}粉)", file=sys.stderr)
                print(f"  候选: " + ", ".join(f"@{u.get('user_info',u).get('nickname')}" for u in users[:5]), file=sys.stderr)
        sec_uid = ui.get("sec_uid")
        user_info = ui
    if not sec_uid:
        err("无法获取 sec_uid")
        sys.exit(3)
    # 3) 拿作品列表
    d = http_get(
        "/aweme/v1/web/aweme/post/",
        {"sec_user_id": sec_uid, "max_cursor": 0, "count": args.videos},
        cookie,
    )
    items = d.get("aweme_list") or []
    if args.raw_out:
        Path(args.raw_out).write_text(json.dumps(d, ensure_ascii=False, indent=2))
    if args.full:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return
    # 4) 输出
    nickname = (user_info or {}).get("nickname") or "?"
    fans = (user_info or {}).get("follower_count") or 0
    total_videos = (user_info or {}).get("aweme_count") or "?"
    print(f"=== @{nickname} (近 {len(items)} 条 / 共 {total_videos} 作品 · {fmt_num(fans)} 粉) ===\n")
    for i, v in enumerate(items, 1):
        a = v.get("author") or {}
        tags = " ".join("#" + t.get("tag_name", "") for t in (v.get("text_extra") or []) if t.get("tag_name"))
        url = f"https://www.douyin.com/video/{v.get('aweme_id')}"
        print(f"[{i}] {truncate(v.get('desc', ''), 100)} "
              f"({fmt_num(v.get('statistics', {}).get('digg_count'))}赞) - {fmt_time(v.get('create_time'))}")
        print(f"    {url}")
        if tags:
            print(f"    {tags}")
        print()


# === 3. video 子命令 ===
def cmd_video(args, cookie: str):
    # 解析 aweme_id
    if args.query.startswith("http"):
        m = re.search(r"/video/(\d+)", args.query)
        if not m:
            err(f"无法从 URL 提取 aweme_id: {args.query}")
            sys.exit(3)
        aweme_id = m.group(1)
    else:
        aweme_id = args.query
    # 1) 拿视频元信息 - 优先 detail API,失败明示不用静默 fallback
    detail_resp = None
    detail_err = None
    try:
        detail_resp = http_get(
            "/aweme/v1/web/aweme/detail/",
            {"aweme_id": aweme_id},
            cookie,
        )
    except Exception as e:
        detail_err = str(e)
    v = (detail_resp or {}).get("aweme_detail") or {}
    detail_source = "detail"
    if not v:
        # detail 拿不到 → fallback search,显式提示
        detail_source = "search-fallback"
        try:
            d2 = http_get(
                "/aweme/v1/web/general/search/single/",
                {"keyword": aweme_id, "search_type": "video", "count": 1},
                cookie,
            )
            items = [x.get("aweme_info") for x in (d2.get("data") or []) if x.get("aweme_info")]
            v = items[0] if items else {}
        except Exception as e:
            err(f"detail API 失败 ({detail_err or '空响应'}),search fallback 也失败: {e}")
            v = {}
    # 落盘原始 JSON (如果有)
    download_info = None
    if args.download:
        if not HAS_DOWNLOADER:
            err("--download 需要 downloader.py 模块(检查 skill 目录完整性)")
            sys.exit(4)
        # 决定下载目录: --download-dir > <raw-out 父目录>/downloads/ > <EXPORTS_DIR>/downloads/
        if args.download_dir:
            dest_dir = Path(args.download_dir)
        elif args.raw_out:
            dest_dir = Path(args.raw_out).resolve().parent / "downloads"
        else:
            dest_dir = EXPORTS_DIR / "downloads"
        print(f"\n=== 下载视频 (quality={args.quality}) → {dest_dir} ===")
        download_info = download_for_aweme(
            aweme_id=aweme_id, dest_dir=dest_dir, cookie=cookie,
            title_hint=v.get("desc", ""), quality=args.quality,
        )
        if not download_info.get("ok"):
            err(f"下载失败: {download_info.get('error', '未知错误')}")
        else:
            ok(f"本地路径: {download_info['path']}")
    if args.raw_out:
        out = {"aweme_id": aweme_id, "detail_source": detail_source}
        if detail_resp is not None:
            out["detail_response"] = detail_resp
        if download_info is not None:
            out["download"] = download_info
        Path(args.raw_out).write_text(json.dumps(out, ensure_ascii=False, indent=2))
        ok(f"原始 JSON 已落盘: {args.raw_out}")
        if download_info and download_info.get("path"):
            ok(f"视频本地路径(也写在 JSON 的 download.path 字段): {download_info['path']}")
    # 2) 输出元信息
    if v:
        a = v.get("author") or {}
        s = v.get("statistics") or {}
        print("=== 视频详情 ===")
        if detail_source != "detail":
            print(f"⚠ 元信息来源: {detail_source} (detail API 不可用)")
        print(f"标题: {v.get('desc', '?')}")
        print(f"作者: @{a.get('nickname', '?')} ({fmt_num(a.get('follower_count'))}粉)"
              + (f" - {a.get('custom_verify')}" if a.get("custom_verify") else ""))
        print(f"发布: {fmt_time(v.get('create_time'))}")
        print(f"数据: {fmt_num(s.get('digg_count'))}赞 | {fmt_num(s.get('comment_count'))}评论 | "
              f"{fmt_num(s.get('collect_count'))}收藏 | {fmt_num(s.get('share_count'))}分享")
        print(f"时长: {v.get('video', {}).get('duration', '?')}ms")
        tags = " ".join("#" + t.get("tag_name", "") for t in (v.get("text_extra") or []) if t.get("tag_name"))
        if tags:
            print(f"话题: {tags}")
        print(f"URL:  https://www.douyin.com/video/{aweme_id}")
    else:
        err(f"视频元信息完全拿不到 (aweme_id={aweme_id})")
        print(f"⚠ 只能继续拉评论,可能不准确")
        print(f"URL:  https://www.douyin.com/video/{aweme_id}")
    # 3) 评论: agent-browser 抓
    if args.comments > 0:
        # 大量评论需求 → 自动推荐走 harvest 脚本
        if args.comments > 20:
            print(f"\n=== 评论 ({args.comments} 条需求超过默认 20 条) ===")
            print(f"建议用 comments-harvest.py 走虚拟滚动 harvest 拿全量:")
            print(f"  python3 $SKILL/comments-harvest.py {aweme_id} --max {args.comments}")
            print()
        print(f"=== 评论 (前 {args.comments} 条,需登录态) ===")
        comments = fetch_comments_via_ab(aweme_id, args.comments)
        if not comments:
            print("(未拿到评论 - 可能是 cookie 过期 / agent-browser state 损坏 / 触发验证码)")
            print("  自检: agent-browser eval \"document.title\"  应返回 '<视频标题> - 抖音'")
        else:
            for i, c in enumerate(comments, 1):
                user = c.get("user", "匿名")
                text = truncate(c.get("text", ""), 100)
                like = fmt_num(c.get("digg_count"))
                when = c.get("time", "?")
                print(f"[{i}] {user} ({like}赞) - {when}")
                print(f"    {text}")


def fetch_comments_via_ab(aweme_id: str, limit: int) -> list:
    """用 agent-browser 打开视频页,eval 拿 [data-e2e=comment-item]"""
    url = f"https://www.douyin.com/video/{aweme_id}"
    # 1) open
    r = subprocess.run(
        ["agent-browser", "--state", STATE_FILE, "open", url],
        capture_output=True, text=True, timeout=30,
    )
    if r.returncode != 0:
        err(f"agent-browser open 失败: {r.stderr[:200]}")
        return []
    time.sleep(4)
    # 2) 检测页面状态 — 验证码 / 登录态 / cookie 注入
    title_check = subprocess.run(
        ["agent-browser", "eval", "document.title"],
        capture_output=True, text=True, timeout=10,
    )
    title = title_check.stdout.strip().strip('"').strip("'")
    if "验证码中间页" in title:
        err(f"页面是验证码中间页 — 风控触发,等 30s 再 reload")
        return []
    # 额外查 captcha iframe 是否实际可见 (不是空壳)
    captcha_check = subprocess.run(
        ["agent-browser", "eval",
         "Array.from(document.querySelectorAll('iframe[id*=\"captcha\"]')).filter(f => f.offsetWidth>100 && f.offsetHeight>100).length"],
        capture_output=True, text=True, timeout=10,
    )
    if captcha_check.stdout.strip().strip('"').strip("'") != "0":
        err(f"页面出现可见 captcha iframe — 风控触发,等 30s 再 reload")
        return []
    if title.startswith("抖音-") or title == "":
        # 落到首页 / 空标题,说明 cookie 没注入(daemon 抢占问题)
        err(f"页面 title 异常: '{title[:50]}' — cookie 可能没注入,跑 keepalive.py state load 重建")
        return [] 
    # 3) 移除登录弹窗
    subprocess.run(["agent-browser", "eval", """
      (() => {
        ['#login-full-panel-1pukt12088zk0', '#douyin_login_comp_flat_panel'].forEach(sel => {
          const p = document.querySelector(sel);
          if (p) { let cur = p; for (let i=0; i<5; i++) { if (!cur.parentElement) break; cur = cur.parentElement; } cur.remove(); }
        });
        document.querySelectorAll('[class*="mask"], [class*="Mask"]').forEach(e => e.remove());
      })();
    """], capture_output=True, timeout=10)
    # 4) eval 拿评论 - 写临时文件避免 escape
    eval_file = "/tmp/douyin/_eval_comments.js"
    Path(eval_file).write_text(f"""JSON.stringify(
  Array.from(document.querySelectorAll('[data-e2e="comment-item"]'))
    .slice(0, {limit})
    .map(item => {{
      const ls = item.innerText.split('\\n').map(s => s.trim()).filter(Boolean);
      if (ls.length < 2) return null;
      const user = ls[0] || '匿名';
      let timeStr = '';
      for (const l of ls) {{
        if (/\\d+(天|小时|分|秒)前|刚刚|周前|月前|年前/.test(l) && l.length < 30) timeStr = l;
      }}
      // ★ 跳过 douyin UI 占位符和操作按钮
      let text = '', like = 0;
      for (let i = 1; i < ls.length; i++) {{
        const l = ls[i];
        if (l === '...' || l === '回复' || l === '展开' || l === '收起' ||
            l === '置顶' || l === '作者' || l === '热' || l === '分享' || l === '举报') continue;
        if (timeStr && l === timeStr) continue;
        if (/^\\d+(\\.\\d+)?$/.test(l) && l.length < 8) {{ like = parseFloat(l); continue; }}
        if (l === user) continue;
        if (/^展开\\d+条回复$/.test(l)) continue;
        if (!text && l.length >= 2) text = l;
      }}
      return {{user, text, digg_count: like, time: timeStr}};
    }})
    .filter(Boolean)
)""")
    r = subprocess.run(
        f"agent-browser eval \"$(cat {eval_file})\"",
        capture_output=True, text=True, timeout=15, shell=True,
    )
    if r.returncode != 0 or not r.stdout.strip():
        return []
    # agent-browser eval 返回值是 shell-quoted 字符串,形如 "[{...}]" (双引号包 JSON)
    out = r.stdout.strip()
    # 如果外层是双引号,用 ast.literal_eval 展开
    if out.startswith('"'):
        import ast
        try:
            out = ast.literal_eval(out)
        except (ValueError, SyntaxError):
            # 备选:手动剥外层引号
            if out.startswith('"') and out.endswith('"'):
                out = out[1:-1].replace('\\"', '"').replace('\\n', '\n')
    try:
        return json.loads(out)
    except (json.JSONDecodeError, TypeError):
        return []


# === main ===
def main():
    ap = argparse.ArgumentParser(description="douyin 抓取 skill")
    sub = ap.add_subparsers(dest="cmd", required=True)

    # search
    p = sub.add_parser("search", help="搜索主题视频或用户")
    p.add_argument("keyword")
    p.add_argument("--type", choices=["video", "user"], default="video")
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--full", action="store_true", help="输出完整 JSON")
    p.add_argument("--raw-out", help="落盘原始 JSON 到指定路径")

    # user
    p = sub.add_parser("user", help="拿用户作品列表")
    p.add_argument("query", help="昵称或 sec_uid")
    p.add_argument("--videos", type=int, default=20)
    p.add_argument("--full", action="store_true")
    p.add_argument("--raw-out", help="落盘原始 JSON")

    # video
    p = sub.add_parser("video", help="视频详情 + 评论")
    p.add_argument("query", help="aweme_id 或视频 URL")
    p.add_argument("--comments", type=int, default=5)
    p.add_argument("--raw-out", help="落盘原始 JSON")
    p.add_argument("--download", action="store_true",
                   help="下载视频到本地(无水印 1080p),路径写入 --raw-out JSON")
    p.add_argument("--download-dir",
                   help=f"视频下载目录(默认: <--raw-out 父目录>/downloads/ 或 {TMP_DIR.parent}/downloads/)")
    p.add_argument("--quality", choices=["play", "download"], default="play",
                   help="下载画质: play=1080p 无水印(默认) / download=720p 带水印")

    args = ap.parse_args()
    cookie = load_cookie()
    if args.cmd == "search":
        cmd_search(args, cookie)
    elif args.cmd == "user":
        cmd_user(args, cookie)
    elif args.cmd == "video":
        cmd_video(args, cookie)


if __name__ == "__main__":
    main()
