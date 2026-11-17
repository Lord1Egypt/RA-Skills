#!/usr/bin/env python3
"""读取抖音视频内容：标题 / 作者 / 官方 AI 章节要点 / 互动数据。

用法:
    python read_douyin.py "7.47 复制打开抖音，看看【xxx的作品】... https://v.douyin.com/xxxx/"
    python read_douyin.py https://v.douyin.com/xxxx/ --json

依赖: playwright, requests（+ 系统已装的 Edge/Chrome，或用 playwright 自带 Chromium）
"""
import argparse
import asyncio
import json
import os
import re
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capture_frames import launch_browser  # noqa: E402

UA_MOBILE = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) "
             "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
UA_DESKTOP = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")

MODAL_CLOSE_COORDS = [(763, 167), (800, 170), (1200, 170)]


def extract_video_id(text: str) -> str:
    """从分享文本中解析视频 ID。"""
    urls = re.findall(r"https?://[^\s\u201c\u201d]+", text)
    if not urls:
        raise ValueError("未在输入中找到链接")
    url = urls[0].rstrip('/')
    m = re.search(r'/video/(\d+)', url)
    if m:
        return m.group(1)
    m = re.search(r'(\d{15,})', url)
    if m:
        return m.group(1)
    # 短链：跟随 302 取真实地址
    resp = requests.get(url, headers={"User-Agent": UA_MOBILE}, allow_redirects=True, timeout=20)
    m = re.search(r'/video/(\d+)', resp.url)
    if not m:
        m = re.search(r'(\d{15,})', resp.url)
    if not m:
        raise ValueError(f"无法从 {resp.url} 解析视频 ID")
    return m.group(1)


async def grab_page_text(video_id: str, keep_screenshot: str | None = None) -> str:
    from playwright.async_api import async_playwright

    video_url = f"https://www.douyin.com/video/{video_id}"
    async with async_playwright() as p:
        # 优先用系统已装的 Edge / Chrome，都没有再用 playwright 自带的 Chromium
        browser, how = await launch_browser(p, prefer="auto", headless=True)
        print(f"[info] 浏览器: {how}", file=sys.stderr)
        try:
            ctx = await browser.new_context(user_agent=UA_DESKTOP,
                                            viewport={"width": 1600, "height": 900})
            page = await ctx.new_page()

            # 1. 预热会话，拿匿名 cookie
            try:
                await page.goto("https://www.douyin.com/", wait_until="domcontentloaded", timeout=25000)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"[warn] 预热超时: {str(e)[:80]}", file=sys.stderr)

            # 2. 打开视频页（超时不致命）
            try:
                await page.goto(video_url, wait_until="domcontentloaded", timeout=25000)
            except Exception as e:
                print(f"[warn] 视频页加载超时: {str(e)[:80]}", file=sys.stderr)
            await asyncio.sleep(3)

            # 3. 关掉登录弹窗（否则内容被遮住）
            for _ in range(4):
                await page.keyboard.press("Escape")
                for sel in ('[class*="close"]', 'svg[class*="close"]', '[aria-label="关闭"]'):
                    try:
                        el = await page.query_selector(sel)
                        if el:
                            await el.click(timeout=1500)
                            break
                    except Exception:
                        pass
                for x, y in MODAL_CLOSE_COORDS:
                    try:
                        await page.mouse.click(x, y)
                    except Exception:
                        pass
                await asyncio.sleep(1)

            await asyncio.sleep(2)
            if keep_screenshot:
                try:
                    await page.screenshot(path=keep_screenshot)
                except Exception:
                    pass
            return await page.evaluate("() => document.body.innerText")
        finally:
            await browser.close()


def parse(text: str) -> dict:
    lines = [l.rstrip() for l in text.splitlines()]
    stripped = [l.strip() for l in lines]

    out = {"title": "", "author": "", "publish_time": "", "stats": {},
           "summary": "", "chapters": [], "comments": []}

    # 标题：其后紧跟连续 4 个纯数字行（点赞/评论/收藏/分享）的那一行最可靠
    for i, s in enumerate(stripped):
        run = 0
        for j in range(i + 1, min(i + 6, len(stripped))):
            if re.fullmatch(r'\d+', stripped[j]):
                run += 1
            else:
                break
        if run >= 4 and len(s) > 10 and not s.startswith("热门"):
            out["title"] = s
            break
    if not out["title"]:
        cands = [s for s in stripped if '#' in s and len(s) > 20 and not s.startswith("热门")]
        if cands:
            out["title"] = max(cands, key=len)
        else:
            t = re.search(r'<title>(.*?)(?:\s*-\s*抖音)?</title>', text)
            if t:
                out["title"] = t.group(1).strip()

    m = re.search(r'发布时间[：:]\s*(\S+\s*\S*)', text)
    if m:
        out["publish_time"] = m.group(1).strip()

    # 互动数据：出现在标题行之后的四个连续纯数字
    if out["title"] in stripped:
        i = stripped.index(out["title"])
        nums = []
        for s in stripped[i + 1:i + 12]:
            if re.fullmatch(r'\d+', s):
                nums.append(int(s))
            elif nums:
                break
        if len(nums) >= 4:
            out["stats"] = dict(zip(["点赞", "评论", "收藏", "分享"], nums[:4]))

    # 作者：「粉丝xxx获赞yyy」附近的上一行
    for i, s in enumerate(stripped):
        if re.search(r'粉丝[\d.万]+获赞[\d.万]+', s) and i > 0:
            out["author"] = stripped[i - 1]
            break

    # 章节要点
    try:
        start = stripped.index("章节要点")
    except ValueError:
        start = -1
    end = -1
    if start >= 0:
        for j in range(start + 1, len(stripped)):
            if stripped[j] in ("内容由AI生成", "全部评论"):
                end = j
                break
        if end < 0:
            end = len(stripped)
        block = stripped[start + 1:end]
        # 去掉免责声明等噪声
        noise = {"个人观点，仅供参考", "章节要点", "下一章", "因浏览器限制，当前为静音", "打开声音", "倍速", "智能", "清屏", "连播"}
        block = [b for b in block if b and b not in noise]
        # 第一个非时间戳段落 = 总述
        chapters = []
        idx = 0
        while idx < len(block) and not re.fullmatch(r'\d{2}:\d{2}', block[idx]):
            out["summary"] += block[idx] + " "
            idx += 1
        out["summary"] = out["summary"].strip()
        # 时间戳 -> 标题 -> 摘要
        while idx < len(block):
            if re.fullmatch(r'\d{2}:\d{2}', block[idx]):
                ts = block[idx]
                idx += 1
                name = block[idx] if idx < len(block) else ""
                idx += 1
                desc_parts = []
                while idx < len(block) and not re.fullmatch(r'\d{2}:\d{2}', block[idx]):
                    desc_parts.append(block[idx])
                    idx += 1
                chapters.append({"time": ts, "name": name, "desc": " ".join(desc_parts).strip()})
            else:
                idx += 1
        out["chapters"] = chapters

    return out


def to_markdown(d: dict, video_id: str) -> str:
    L = []
    L.append(f"# {d['title'] or '(无标题)'}")
    L.append("")
    meta = [f"**视频 ID**：{video_id}"]
    if d["author"]:
        meta.append(f"**作者**：{d['author']}")
    if d["publish_time"]:
        meta.append(f"**发布**：{d['publish_time']}")
    if d["stats"]:
        meta.append("**数据**：" + " / ".join(f"{k} {v}" for k, v in d["stats"].items()))
    L.append("　|　".join(meta))
    L.append("")
    if d["summary"]:
        L.append("## 内容总述")
        L.append("")
        L.append(d["summary"])
        L.append("")
    if d["chapters"]:
        L.append("## 章节要点")
        L.append("")
        L.append("| 时间 | 章节 | 要点 |")
        L.append("| --- | --- | --- |")
        for c in d["chapters"]:
            L.append(f"| {c['time']} | {c['name']} | {c['desc']} |")
        L.append("")
    if not d["chapters"] and not d["summary"]:
        L.append("> 该视频暂无官方 AI 章节要点。")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="读取抖音视频内容")
    ap.add_argument("input", help="抖音分享文本或链接")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--screenshot", help="同时保存页面截图到该路径")
    args = ap.parse_args()

    vid = extract_video_id(args.input)
    print(f"[info] 视频 ID: {vid}", file=sys.stderr)
    text = asyncio.run(grab_page_text(vid, args.screenshot))
    if keep := args.screenshot:
        print(f"[info] 截图: {keep}", file=sys.stderr)
    data = parse(text)
    data["video_id"] = vid
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(data, vid))


if __name__ == "__main__":
    main()
