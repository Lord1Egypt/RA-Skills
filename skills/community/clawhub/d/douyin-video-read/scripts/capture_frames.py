#!/usr/bin/env python3
"""逐帧抓取网页里的视频画面（不下载视频文件）。

原理：让真实浏览器加载页面，再用 ``canvas.drawImage(video)`` 在任意时间点取帧，
因此可以精确按时间轴采样，且完全避开「预加载污染」——用捕获网络请求下载视频时，
播放器预加载的推荐流视频常常会把你带到错误的文件上。

**不限于抖音**：任何页面只要有一个 HTML5 ``<video>`` 元素就能用。
抖音链接会被自动解析成视频页地址。

用法:
    python capture_frames.py "<链接或分享文本>" --out <输出目录> [--interval 1.5] [--headed]

依赖: playwright（+ 任一已安装的 Chromium 系浏览器，或 playwright 自带 Chromium）
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import json
import os
import re
import sys

import requests

UA_DESKTOP = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")
UA_MOBILE = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) "
             "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")

# 抖音视频页的登录弹窗关闭按钮坐标（视口 1600x900 下实测）
DOUYIN_MODAL_CLOSE_COORDS = [(763, 167), (800, 170), (1200, 170), (760, 200)]
CHANNEL_ORDER = ("msedge", "chrome", "chrome-beta", "chromium")


def first_url(text: str) -> str:
    urls = re.findall(r"https?://[^\s\u201c\u201d\u3002]+", text or "")
    if not urls:
        raise ValueError("输入里没有找到链接")
    return urls[0].rstrip("/,")


def resolve_target(text: str) -> dict:
    """把用户输入解析成 (要打开的页面地址, 平台, 视频 ID)。"""
    url = first_url(text)
    if "douyin.com" in url:
        m = re.search(r"/video/(\d+)", url) or re.search(r"(\d{15,})", url)
        if m:
            vid = m.group(1)
        else:  # 短链，跟随 302
            try:
                resp = requests.get(url, headers={"User-Agent": UA_MOBILE},
                                    allow_redirects=True, timeout=20)
                m = re.search(r"/video/(\d+)", resp.url) or re.search(r"(\d{15,})", resp.url)
                vid = m.group(1) if m else None
            except Exception:
                vid = None
        if not vid:
            raise ValueError(f"无法从 {url} 解析抖音视频 ID")
        return {"page_url": f"https://www.douyin.com/video/{vid}",
                "platform": "douyin", "video_id": vid, "warmup": "https://www.douyin.com/"}
    return {"page_url": url, "platform": "generic", "video_id": None, "warmup": None}


async def launch_browser(p, prefer: str = "auto", headless: bool = True):
    """按可用性挑一个浏览器。返回 (browser, 说明)。

    优先用系统已装的 Edge / Chrome（免下载 500MB Chromium），都没有就用 playwright 自带的。
    """
    tried = []
    order = CHANNEL_ORDER if prefer == "auto" else (prefer,)
    for ch in order:
        try:
            b = await p.chromium.launch(headless=headless, channel=ch)
            return b, f"channel={ch}"
        except Exception as e:
            tried.append(f"{ch}({str(e)[:60]})")
    try:
        b = await p.chromium.launch(headless=headless)
        return b, "playwright 自带 chromium"
    except Exception as e:
        tried.append(f"bundled({str(e)[:80]})")
    raise RuntimeError("没有可用的浏览器，尝试过：\n  " + "\n  ".join(tried) +
                       "\n→ 安装 Edge/Chrome，或运行 `playwright install chromium`")


async def dismiss_douyin_modal(page):
    """关闭抖音的「登录后免费畅享高清视频」弹窗，否则内容被遮住。"""
    for _ in range(5):
        try:
            await page.keyboard.press("Escape")
        except Exception:
            pass
        for sel in ('[class*="close"]', 'svg[class*="close"]', '[aria-label="关闭"]',
                    '[aria-label="Close"]'):
            try:
                el = await page.query_selector(sel)
                if el:
                    await el.click(timeout=1200)
                    break
            except Exception:
                pass
        for x, y in DOUYIN_MODAL_CLOSE_COORDS:
            try:
                await page.mouse.click(x, y)
            except Exception:
                pass
        await asyncio.sleep(0.8)


async def video_state(page, selector: str = "video"):
    return await page.evaluate("""(sel) => {
        const v = document.querySelector(sel);
        if (!v) return {found: false};
        return {found: true, duration: isFinite(v.duration) ? v.duration : 0,
                w: v.videoWidth, h: v.videoHeight, ready: v.readyState,
                paused: v.paused, cur: v.currentTime};
    }""", selector)


async def capture(target: dict, out_dir: str, interval: float, max_frames: int,
                  selector: str, prefer: str, headless: bool):
    from playwright.async_api import async_playwright

    os.makedirs(out_dir, exist_ok=True)
    frames_dir = os.path.join(out_dir, "frames")
    os.makedirs(frames_dir, exist_ok=True)
    shots = []

    async with async_playwright() as p:
        browser, how = await launch_browser(p, prefer, headless)
        print(f"[info] 浏览器: {how}", file=sys.stderr)
        try:
            ctx = await browser.new_context(user_agent=UA_DESKTOP,
                                            viewport={"width": 1600, "height": 900})
            page = await ctx.new_page()

            if target.get("warmup"):
                try:
                    await page.goto(target["warmup"], wait_until="domcontentloaded",
                                    timeout=25000)
                    await asyncio.sleep(2)
                except Exception as e:
                    print(f"[warn] 预热超时（不致命）: {str(e)[:70]}", file=sys.stderr)

            try:
                await page.goto(target["page_url"], wait_until="domcontentloaded",
                                timeout=25000)
            except Exception as e:
                print(f"[warn] 页面加载超时（不致命，继续读页面状态）: {str(e)[:70]}",
                      file=sys.stderr)
            await asyncio.sleep(3)

            st = {"found": False, "duration": 0}
            for _ in range(12):
                if target["platform"] == "douyin":
                    await dismiss_douyin_modal(page)
                st = await video_state(page, selector)
                if st.get("found") and st.get("ready", 0) >= 1 and st.get("duration"):
                    break
                await asyncio.sleep(2)

            print(f"[info] video 元素: {st}", file=sys.stderr)
            if not st.get("found"):
                raise RuntimeError(
                    f"页面上找不到 video 元素（选择器 {selector!r}）。"
                    "可能需要登录、或页面尚未渲染完 → 试试 --headed 观察实际页面")
            duration = float(st.get("duration") or 0)
            if duration <= 0:
                raise RuntimeError("拿不到视频时长，播放器未加载出媒体")

            try:
                await page.evaluate("""(sel) => { const v=document.querySelector(sel);
                    v.muted = true; v.pause(); }""", selector)
            except Exception:
                pass

            ts, n = 0.0, 0
            while ts < duration and n < max_frames:
                b64 = await page.evaluate("""async ([sel, t]) => {
                    const v = document.querySelector(sel);
                    if (!v) throw new Error('no video');
                    await new Promise((res) => {
                        let done = false;
                        const fin = () => { if (!done) { done = true; res(); } };
                        v.addEventListener('seeked', fin, {once: true});
                        v.currentTime = t;
                        setTimeout(fin, 2500);
                    });
                    await new Promise(r => setTimeout(r, 220));
                    const c = document.createElement('canvas');
                    const w = v.videoWidth || 720, h = v.videoHeight || 1280;
                    c.width = w; c.height = h;
                    c.getContext('2d').drawImage(v, 0, 0, w, h);
                    return c.toDataURL('image/jpeg', 0.85);
                }""", [selector, ts])
                if "," not in b64:
                    raise RuntimeError("canvas 取证失败（可能被跨域策略拦截）")
                raw = base64.b64decode(b64.split(",", 1)[1])
                fp = os.path.join(frames_dir, f"{int(ts*1000):07d}.jpg")
                with open(fp, "wb") as f:
                    f.write(raw)
                shots.append({"t": round(ts, 1), "file": fp})
                n += 1
                if n % 10 == 0:
                    print(f"[info] 已抓 {n} 帧 / {ts:.0f}s of {duration:.0f}s", file=sys.stderr)
                ts += interval

            meta = {"platform": target["platform"], "video_id": target.get("video_id"),
                    "page_url": target["page_url"], "duration": duration,
                    "width": st.get("w"), "height": st.get("h"),
                    "browser": how, "interval": interval, "frames": shots}
            with open(os.path.join(out_dir, "frames.json"), "w", encoding="utf-8") as f:
                json.dump(meta, f, ensure_ascii=False, indent=1)
            print(f"[info] 共 {len(shots)} 帧 → {frames_dir}", file=sys.stderr)
            return meta
        finally:
            await browser.close()


def main():
    ap = argparse.ArgumentParser(description="逐帧抓取网页视频画面（不下载视频）")
    ap.add_argument("input", help="链接 / 含链接的分享文本 / 抖音分享口令")
    ap.add_argument("--out", "-o", required=True, help="输出目录")
    ap.add_argument("--interval", type=float, default=1.5,
                    help="采样间隔秒数（默认 1.5；字幕约 2-3 秒换一次，1.5 能保证不漏）")
    ap.add_argument("--max-frames", type=int, default=600, help="最大帧数（默认 600）")
    ap.add_argument("--selector", default="video", help="视频元素选择器（默认 video）")
    ap.add_argument("--browser", default="auto",
                    help="浏览器：auto|msedge|chrome|chromium（默认 auto，依次尝试）")
    ap.add_argument("--headed", action="store_true",
                    help="显示浏览器窗口（页面有反爬/需要观察时用）")
    args = ap.parse_args()

    target = resolve_target(args.input)
    print(f"[info] 平台: {target['platform']}，页面: {target['page_url']}", file=sys.stderr)
    meta = asyncio.run(capture(target, args.out, args.interval, args.max_frames,
                               args.selector, args.browser, not args.headed))
    print(json.dumps({k: v for k, v in meta.items() if k != "frames"},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
