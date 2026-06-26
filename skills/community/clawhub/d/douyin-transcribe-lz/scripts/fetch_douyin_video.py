#!/usr/bin/env python3
"""
Douyin Video Fetcher & Whisper Transcriber

端到端流程：抖音短链接 → 视频下载 → Whisper 转录 → agent 整理 → 保存 Markdown

用法：
    python fetch_douyin_video.py <douyin_short_url> [--output OUTPUT_DIR]

LLM 整理说明：
    脚本本身不调用任何外部 LLM API。
    转录完成后输出原始文本，由调用方（agent）负责整理纠错，
    再调用 write_cleaned_md() 将整理后的文本写入 .md 文件。

共享的转录和 MD 写入逻辑见：scripts/transcribe.py
"""

import asyncio
import os
import re
import sys
import json
import requests
from pathlib import Path
from urllib.parse import unquote

# Windows 下强制 UTF-8 输出
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        os.environ.setdefault("PYTHONIOENCODING", "utf-8")

# ── 导入共享模块 ──────────────────────────────────────────────────────────────

# 将 scripts/ 目录加入 sys.path
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from transcribe import (                  # noqa: E402
    check_dependencies,
    make_timestamp,
    transcribe,
    write_cleaned_md,
)

# 核心依赖检查（不含 playwright，因为可能有 API 备用方案）
check_dependencies(require_douyin=False)

# playwright 延迟导入：仅在需要时才检查和加载
# 如果 playwright 不可用，脚本仍可通过 API 备用方案运行
_playwright_available = False
_async_playwright = None

try:
    from playwright.async_api import async_playwright   # noqa: E402
    _playwright_available = True
    _async_playwright = async_playwright
except ImportError:
    print("[Info] playwright 未安装，抖音视频将使用 API 方案获取（无需浏览器）")


# ── 配置 ──────────────────────────────────────────────────────────────────────

OUTPUT_DIR = "."


# ── Step 1: 通过 Playwright 捕获视频 URL ─────────────────────────────────────

async def _try_capture_once(short_url: str, wait_seconds: int) -> tuple[str | None, str]:
    """单次尝试用 Playwright 捕获视频 URL。

    Args:
        short_url: 抖音短链接
        wait_seconds: 等待 JS 渲染的秒数

    Returns:
        (video_url, resolved_page_url)
    """
    async with _async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )
        page = await context.new_page()

        await page.goto(short_url, wait_until="domcontentloaded", timeout=30000)
        print(f"[Step 1] 等待 JS 渲染 ({wait_seconds}秒)...")
        await asyncio.sleep(wait_seconds)

        # 多选择器尝试
        selectors = [
            'video[src*="douyin"]',
            'video[src*="douyinvod"]',
            'video[src*="aweme"]',
            'video',
            'xgplayer-container video',
        ]

        video_src = None
        for sel in selectors:
            try:
                el = await page.query_selector(sel)
                if el:
                    src = await el.get_attribute("src")
                    if src and ".mp4" in src and ("douyin" in src or "douyinvod" in src or "aweme" in src):
                        video_src = src
                        print(f"[Step 1] 通过选择器捕获: {sel}")
                        break
            except Exception:
                pass

        # 兜底：page.evaluate
        if not video_src:
            video_src = await page.evaluate("""
                () => {
                    const videos = document.querySelectorAll('video');
                    for (const v of videos) {
                        if (v.src && v.src.includes('.mp4') && (v.src.includes('douyin') || v.src.includes('douyinvod') || v.src.includes('aweme')))
                            return v.src;
                        const sources = v.querySelectorAll('source');
                        for (const s of sources) { if (s.src) return s.src; }
                    }
                    return null;
                }
            """)
            if video_src:
                print("[Step 1] 通过 page.evaluate 捕获")

        final_url = page.url
        print(f"[Step 1] 解析后页面: {final_url}")
        await browser.close()

    return video_src, final_url


async def capture_video_url(short_url: str) -> tuple[str | None, str]:
    """
    打开抖音短链接，等待 JS 渲染，从 video 元素中提取 src。
    此方法在登录模态框覆盖视频元素时仍然有效。

    内置重试机制：首次等待 8 秒，如果未捕获到则再等 13 秒重试一次。

    返回: (video_url, resolved_page_url)

    如果 playwright 不可用，直接返回 None，让调用方走 API 备用方案。
    """
    if not _playwright_available:
        print("[Step 1] playwright 不可用，跳过浏览器捕获")
        return None, ""

    print(f"[Step 1] 正在打开: {short_url}")

    # 第一次尝试：等待 8 秒
    video_src, final_url = await _try_capture_once(short_url, 8)

    if video_src:
        print(f"[Step 1] 视频 URL 已获取 ({len(video_src)} 字符)")
        return video_src, final_url

    # 第二次尝试：等待更长时间（13 秒），某些视频 JS 加载较慢
    print("[Step 1] 首次捕获失败，增加等待时间重试...")
    video_src, final_url = await _try_capture_once(short_url, 13)

    if video_src:
        print(f"[Step 1] 重试成功！视频 URL 已获取 ({len(video_src)} 字符)")
        return video_src, final_url

    print("[Step 1] Playwright 捕获失败（2次尝试均未找到视频 URL）")
    return None, final_url


# ── Step 2: 下载视频 ──────────────────────────────────────────────────────────

def download_video(url: str, output_path: str, referer: str = "https://www.douyin.com/") -> str:
    """通过 HTTP 下载视频，使用与抖音兼容的请求头。"""
    print(f"[Step 2] 下载中: {output_path}")
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Referer": referer,
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    resp = requests.get(url, headers=headers, stream=True, timeout=120, allow_redirects=True)
    print(f"[Step 2] HTTP {resp.status_code} | Content-Type: {resp.headers.get('Content-Type')}")

    if not resp.ok:
        raise RuntimeError(f"下载失败: HTTP {resp.status_code}")

    total = int(resp.headers.get("Content-Length", 0))
    downloaded = 0
    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total:
                    print(f"  {downloaded/1024/1024:.1f} MB / {total/1024/1024:.1f} MB", end="\r")

    size_mb = downloaded / 1024 / 1024
    print(f"\n[Step 2] 下载完成: {size_mb:.1f} MB")
    return output_path


# ── Step 1-备用: 通过 Douyin API 获取视频 URL ────────────────────────────────


def _fix_douyin_text(text: str) -> str:
    """修复 Douyin API 返回的中文文本编码问题。

    Douyin API 的响应编码取决于请求头的 Accept 字段：
    - 有时返回正确的 UTF-8 JSON
    - 有时返回 latin1 编码的 UTF-8 内容（需要二次解码）

    检测逻辑：如果文本中存在大量 latin1 范围的非 ASCII 字符（通常是 UTF-8 被误读为 latin1），
    尝试 encode("latin1").decode("utf-8") 修复；如果修复失败或文本看起来正常，保持原样。
    """
    if not text:
        return text

    # 检查是否包含疑似乱码的 latin1 字符（UTF-8 中文字节被误读为 latin1 的特征）
    # latin1 范围 0x80-0xFF 的字符如果在中文文本中大量出现，通常是编码错误
    suspicious_chars = sum(1 for c in text if 0x80 <= ord(c) <= 0xFF and ord(c) > 0x9F)
    total_non_ascii = sum(1 for c in text if ord(c) > 127)

    # 如果大部分非 ASCII 字符在 latin1 的"扩展"区域（0xA0-0xFF），大概率是编码错误
    if suspicious_chars > 0 and total_non_ascii > 0 and suspicious_chars / total_non_ascii > 0.3:
        try:
            fixed = text.encode("latin1").decode("utf-8")
            # 验证修复后的文本确实包含中文字符（更合理）
            chinese_chars = sum(1 for c in fixed if 0x4E00 <= ord(c) <= 0x9FFF)
            if chinese_chars > 0:
                return fixed
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass  # 修复失败，保持原样

    return text


def _extract_video_id(url: str) -> str | None:
    """从抖音页面 URL 中提取视频 ID。

    支持的 URL 格式：
    - /video/7650152339977948416
    - /note/7650152339977948416（图文笔记）
    - /modal/7650152339977948416（弹窗模式）
    - ?modal_id=7650152339977948416（查询参数）
    - /share/video/7650152339977948416（分享页面）
    """
    # 优先从路径提取
    match = re.search(r'/(?:video|note|modal|share/video)/(\d+)', url)
    if match:
        return match.group(1)

    # 从查询参数提取
    match = re.search(r'modal_id=(\d+)', url)
    if match:
        return match.group(1)

    return None


def fetch_video_url_via_api(short_url: str) -> tuple[str | None, str, dict | None]:
    """
    当 Playwright 捕获失败时，通过 Douyin web API 获取视频 URL 作为备用方案。

    流程：
    1. 先访问短链接获取 resolved URL（从中提取 video_id）
    2. 调用 Douyin aweme detail API 获取视频信息
    3. 从返回的 JSON 中提取 play_addr URL

    Returns: (video_url, resolved_url, detail_dict)
    """
    print("[Step 1-备用] 尝试通过 Douyin API 获取视频 URL...")

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.douyin.com/",
        "Accept": "*/*",
    }

    # Step 1: 获取 resolved URL 和 video_id
    try:
        resp = requests.get(short_url, headers=headers, timeout=15, allow_redirects=True)
        resolved_url = resp.url
        print(f"[Step 1-备用] 解析后页面: {resolved_url}")
    except Exception as e:
        print(f"[Step 1-备用] 访问短链接失败: {e}")
        return None, "", None

    video_id = _extract_video_id(resolved_url)
    if not video_id:
        print("[Step 1-备用] 无法从 URL 中提取视频 ID")
        return None, resolved_url, None

    print(f"[Step 1-备用] 视频 ID: {video_id}")

    # Step 2: 调用 Douyin API
    api_url = f"https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id={video_id}&aid=6383"
    try:
        api_resp = requests.get(api_url, headers={
            "User-Agent": headers["User-Agent"],
            "Referer": "https://www.douyin.com/",
            "Accept": "application/json",
        }, timeout=15)
        print(f"[Step 1-备用] API HTTP {api_resp.status_code}")

        if not api_resp.ok:
            print(f"[Step 1-备用] API 请求失败")
            return None, resolved_url, None

        data = api_resp.json()
        detail = data.get("aweme_detail")
        if not detail:
            print(f"[Step 1-备用] API 返回无 aweme_detail（status_code={data.get('status_code', 'N/A')}）")
            return None, resolved_url, None

        # Step 3: 提取视频 URL
        play_addr = detail.get("video", {}).get("play_addr", {})
        url_list = play_addr.get("url_list", [])
        if not url_list:
            print("[Step 1-备用] API 返回无视频 URL")
            return None, resolved_url, detail

        video_url = url_list[0]
        # 修复 URL 中的特殊字符
        video_url = video_url.replace("~", "%7E")

        desc = _fix_douyin_text(detail.get("desc", ""))

        author = _fix_douyin_text(detail.get("author", {}).get("nickname", ""))

        print(f"[Step 1-备用] 视频 URL 已获取 ({len(video_url)} 字符)")
        print(f"[Step 1-备用] 描述: {desc[:80]}")
        print(f"[Step 1-备用] 作者: {author}")
        return video_url, resolved_url, detail

    except Exception as e:
        print(f"[Step 1-备用] API 调用失败: {e}")
        return None, resolved_url, None


# ── Main ──────────────────────────────────────────────────────────────────────

async def main():
    args = sys.argv[1:]
    if not args:
        print("用法: python fetch_douyin_video.py <douyin_short_url> [--output DIR]")
        print("示例: python fetch_douyin_video.py https://v.douyin.com/xxxxx/")
        print("      python fetch_douyin_video.py https://v.douyin.com/xxxxx/ --output ./result")
        sys.exit(1)

    # 解析参数
    output_dir = OUTPUT_DIR

    if "--output" in args:
        idx = args.index("--output")
        if idx + 1 < len(args):
            output_dir = args.pop(idx + 1)
        args.pop(idx)

    if not args:
        print("[ERROR] 请提供抖音短链接")
        sys.exit(1)

    short_url = args[0]

    ts = make_timestamp()
    print(f"[Info] 时间戳: {ts}")
    print(f"[Info] 输出目录: {output_dir}")
    print("[Info] 流程: Step1 捕获URL -> Step2 下载视频 -> Step3 Whisper转录 -> Step4 整理输出")

    # Step 1: 捕获视频 URL（Playwright 优先，API 备用）
    print("\n[Step 1/4] 正在捕获视频 URL...")
    video_url, resolved_url = await capture_video_url(short_url)

    if not video_url:
        print("[Step 1] Playwright 捕获失败，尝试 API 备用方案...")
        video_url, resolved_url, _detail = fetch_video_url_via_api(short_url)

    if not video_url:
        print("[ERROR] 未能捕获视频 URL（Playwright 和 API 均失败），请确认链接有效")
        print("  提示：某些视频需要登录后才能播放，可尝试使用完整视频页面 URL")
        sys.exit(1)

    # Step 2: 下载视频
    print("\n[Step 2/4] 正在下载视频...")
    video_filename = f"douyin_video_{ts}.mp4"
    video_path = os.path.join(output_dir, video_filename)
    video_path = download_video(video_url, video_path, resolved_url or "https://www.douyin.com/")

    # Step 3: Whisper 转录（共享模块，使用默认 medium 模型）
    print("\n[Step 3/4] 正在转录（Whisper medium 模型，耗时取决于视频长度）...")
    result, txt_path, json_path = transcribe(video_path, output_dir, timestamp=ts)

    # Step 4: 输出原始文本，由 agent 整理后调用 write_cleaned_md()
    raw_text = result["text"].strip()
    print("\n[Step 4/4] 转录完成，请 agent 整理后调用 write_cleaned_md() 写入 MD")
    print(f"[Step 4/4] RAW_TRANSCRIPT_START\n{raw_text}\n[Step 4/4] RAW_TRANSCRIPT_END")

    print("\n[Done] 转录完毕")
    print(f"  视频:   {video_path}")
    print(f"  文本:   {txt_path}")
    print(f"  JSON:   {json_path}")
    print(f"  时间戳: {ts}")
    print(f"\n预览: {raw_text[:200]}...")

    # 返回数据供外部使用
    return {
        "timestamp": ts,
        "video_path": video_path,
        "txt_path": txt_path,
        "json_path": json_path,
        "raw_text": raw_text,
        "source_url": short_url,
        "resolved_url": resolved_url,
        "segments": result["segments"],
    }


if __name__ == "__main__":
    asyncio.run(main())
