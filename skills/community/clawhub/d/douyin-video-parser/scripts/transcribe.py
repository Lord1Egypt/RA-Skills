#!/usr/bin/env python3
"""
抖音视频 → 中文字幕稿 + 结构化 HTML 报告（本地、免费、不要 API key）

流程：
    抖音链接 → video_id → 拿 mp4 直链（多级 fallback）→ 下载 → faster-whisper 转写 → 落盘 txt + 生成 HTML

mp4 直链获取（按顺序尝试）：
    1. iesdouyin share API（正则抠 play_addr，快路径）
    2. CDP 浏览器方案（headless Edge/Chrome + 调试协议截获 aweme/detail 响应，
       抖音前端 JS 自己完成签名，无需手动 cookie）——2026-08 抖音反爬后主通道
    3. yt-dlp + 手动 cookies 文件（--cookies 参数，作为最后手段）

用法：
    python3 transcribe.py "https://www.douyin.com/video/7634579290163531035"
    python3 transcribe.py "https://v.douyin.com/xa-wFiDUUvVs/"
    python3 transcribe.py <链接> --model small                # 用更准的 small 模型
    python3 transcribe.py <链接> --generate-html              # 生成 HTML 报告
    python3 transcribe.py <链接> --out-dir ./outputs          # 自定义输出目录
    python3 transcribe.py <链接> --tag 公共知识女博主           # 给输出文件加个识别标签
    python3 transcribe.py <链接> --cookies cookies.txt        # yt-dlp 兜底时指定 cookie 文件
"""

import argparse
import datetime as dt
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request

# 跨平台临时目录
TEMP_DIR = tempfile.gettempdir()
MODEL_DIR = os.path.join(TEMP_DIR, "whisper-models")

MOBILE_UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
             "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1")

DESKTOP_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


# ═══════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════

def _http_get(url: str, headers: dict, max_timeout: int = 20) -> str:
    """用 urllib 发起 GET 请求（不依赖外部 curl）"""
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=max_timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _http_download(url: str, dest: str, headers: dict, max_timeout: int = 180) -> bool:
    """用 urllib 分块下载文件（不依赖外部 curl）"""
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=max_timeout) as resp:
            with open(dest, "wb") as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"[ERROR] 下载失败: {e}", file=sys.stderr)
        return False


def _safe_filename(s: str, max_len: int = 40) -> str:
    for ch in r'\/:*?"<>|':
        s = s.replace(ch, "_")
    return s.strip().replace(" ", "_")[:max_len]


def _format_duration(seconds: float) -> str:
    if not seconds:
        return ""
    m = int(seconds // 60)
    s = int(seconds % 60)
    if m == 0:
        return f"{s}秒"
    return f"{m}分{s}秒"


def _esc(text) -> str:
    """HTML 转义"""
    return html.escape(str(text) if text is not None else "")


# ═══════════════════════════════════════════════════════════
# 1. 视频下载
# ═══════════════════════════════════════════════════════════

def extract_video_id(url: str) -> str:
    """从抖音链接里掏出 video_id。短链会先 follow 一次。"""
    m = re.search(r"/video/(\d+)", url) or re.search(r"/shipin/(\d+)", url)
    if m:
        return m.group(1)

    # 短链：跟一次 302（用 urllib，不依赖 curl）
    if "v.douyin.com" in url or "iesdouyin.com" in url:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": MOBILE_UA})
            with urllib.request.urlopen(req, timeout=10) as resp:
                final_url = resp.geturl()
                m = re.search(r"/video/(\d+)", final_url)
                if m:
                    return m.group(1)
        except Exception as e:
            print(f"[WARN] 跟随短链失败: {e}", file=sys.stderr)

    sys.exit(f"[ERROR] 无法从 URL 提取 video_id: {url}\n"
             f"        请改用 https://www.douyin.com/video/<id> 形式的长链")


def _clean_title(raw: str) -> str:
    """从抖音 desc 中清洗出干净的标题：去掉话题标签、声明、冗长描述，只留核心标题。"""
    # 1. 去掉 " - 抖音" 后缀
    s = raw.rsplit(" - ", 1)[0].strip() or raw
    # 2. 去掉 #话题标签（#xxx 或 #xxx#xxx 链）
    s = re.sub(r'#\S+', '', s)
    # 3. 去掉常见声明/免责声明
    decl = [
        "本片为原创虚构短片", "片中内容并非否定", "也无意鼓励",
        "并非否定工作", "并非否定", "无意鼓励", "仅供参考",
        "个人观点", "不代表", "如有侵权", "如有雷同", "纯属虚构",
        "本视频仅供", "本视频为", "本视频不代表", "如有不适",
        "请理性看待", "请理性", "理性看待", "请勿模仿",
    ]
    for d in decl:
        idx = s.find(d)
        if idx != -1:
            s = s[:idx]
    # 4. 去掉多余空白和标点
    s = re.sub(r'[\s\u3000]+', ' ', s).strip()
    s = re.sub(r'^[\s\u3000，,、；;：:]+', '', s)
    s = re.sub(r'[\s\u3000，,、；;：:]+$', '', s)
    # 5. 如果清洗后只剩空或太短，回退到第一个有意义句子（按句号/逗号/换行切）
    if len(s) < 3:
        parts = [p.strip() for p in re.split(r'[。！？\n]', raw) if len(p.strip()) >= 3]
        if parts:
            s = parts[0]
            s = re.sub(r'#\S+', '', s).strip()
    return s or raw[:60].strip()

def fetch_video_title(video_id: str) -> str:
    """从 iesdouyin share 页面提取视频标题（已清洗）"""
    share_url = f"https://www.iesdouyin.com/share/video/{video_id}"
    headers = {"User-Agent": MOBILE_UA}
    page_html = _http_get(share_url, headers, max_timeout=20)

    title = "untitled"
    tm = re.search(r'<title[^>]*>(.*?)</title>', page_html, re.S)
    if tm:
        raw = tm.group(1).strip()
        title = _clean_title(raw)
    return title


def fetch_mp4_url(video_id: str) -> str:
    """从 iesdouyin share 页面里抠出 mp4 直链。"""
    share_url = f"https://www.iesdouyin.com/share/video/{video_id}"
    headers = {"User-Agent": MOBILE_UA}
    page_html = _http_get(share_url, headers, max_timeout=20)

    m = re.search(r'"play_addr":\{[^}]*"url_list":\[([^\]]+)\]', page_html)
    if not m:
        sys.exit(f"[ERROR] iesdouyin 没返回 play_addr，可能是反爬或视频已删。video_id={video_id}")
    raw_urls = re.findall(r'"([^"]+)"', m.group(1))
    if not raw_urls:
        sys.exit("[ERROR] play_addr.url_list 为空")
    # \u002F → /
    return raw_urls[0].encode("utf-8").decode("unicode_escape")


def download_video(url: str, dest: str) -> None:
    print(f"[1/3] 下载 mp4 -> {dest}")
    headers = {
        "User-Agent": MOBILE_UA,
        "Referer": "https://www.douyin.com/",
    }

    if not _http_download(url, dest, headers, max_timeout=180):
        sys.exit("[ERROR] mp4 下载失败（urllib）")

    size_mb = os.path.getsize(dest) / 1024 / 1024
    print(f"      ok, {size_mb:.1f} MB")


# ═══════════════════════════════════════════════════════════
# 1b. CDP 浏览器兜底（2026-08 抖音反爬后主通道）
# ═══════════════════════════════════════════════════════════

def _find_browser() -> str:
    """找本机可用的 Edge/Chrome 可执行文件"""
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",  # macOS
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/microsoft-edge",  # Linux
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return ""


def _pick_cdn_media(urls) -> str:
    """从候选 CDN 直链里挑出最适合转写的媒体文件，下载后返回本地路径。

    抖音对部分视频（如 AI 短片）用 DASH 分离：视频流和音频流是两个不同的
    CDN 文件。转写只需要音轨，所以逐个下载探测（文件都很小），挑带音轨的；
    多个都带音轨时取时长最长的。全部探测失败返回 ""。
    """
    try:
        import av
    except ImportError:
        av = None

    best_path, best_dur, best_has_audio = "", 0.0, False
    for i, u in enumerate(urls):
        tmp = os.path.join(TEMP_DIR, f"cdn_probe_{i}.mp4")
        try:
            req = urllib.request.Request(u, headers={
                "User-Agent": DESKTOP_UA,
                "Referer": "https://www.douyin.com/",
            })
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            if len(data) < 300 * 1024:   # 太小，跳过
                continue
            with open(tmp, "wb") as f:
                f.write(data)

            has_audio, dur = False, 0.0
            if av is not None:
                try:
                    c = av.open(tmp)
                    has_audio = any(s.type == "audio" for s in c.streams)
                    if c.duration:
                        dur = float(c.duration) / 1_000_000
                    c.close()
                except Exception:
                    pass

            if (has_audio and not best_has_audio) or \
               (has_audio == best_has_audio and dur > best_dur):
                # 换新的最优就删掉旧的
                if best_path and best_path != tmp:
                    try:
                        os.remove(best_path)
                    except OSError:
                        pass
                best_path, best_dur, best_has_audio = tmp, dur, has_audio
                print(f"      [cdp] 候选[{i}] "
                      f"{'含音轨' if has_audio else '无音轨'} "
                      f"{len(data) / 1024 / 1024:.1f}MB {dur:.0f}s "
                      f"{'← 当前最优' if has_audio else ''}")
            else:
                try:
                    os.remove(tmp)
                except OSError:
                    pass
        except Exception:
            continue

    if best_path and best_has_audio:
        print(f"      [cdp] CDN 直链兜底成功（含音轨，{best_dur:.0f}s）")
        return best_path
    if best_path:  # av 探测不可用时退化为"取最大文件"
        print("      [cdp] CDN 直链兜底成功（未探测到音轨，取最大文件）")
        return best_path
    return ""


def fetch_video_via_cdp(video_id: str):
    """CDP 浏览器方案：启动 headless Edge/Chrome，让抖音前端 JS 自己完成
    签名/种 cookie，再从 Network 响应里截获视频数据。

    返回 (title, mp4_url, local_path)：
      - detail 接口路径：(title, 直链URL, None) —— 由调用方下载
      - CDN 兜底路径（SSR 页面）：(title, None, 本地文件路径) —— 已下载好
      - 失败：(None, None, None)。不依赖手动 cookie。
    """
    browser = _find_browser()
    if not browser:
        print("[ERROR] 未找到 Edge/Chrome，CDP 兜底不可用", file=sys.stderr)
        return None, None

    try:
        import websocket  # 延迟导入，避免启动时硬依赖
    except ImportError:
        print("[ERROR] 缺少 websocket-client 库，请先安装: pip install websocket-client",
              file=sys.stderr)
        return None, None

    port = 9333 + (os.getpid() % 500)
    profile = os.path.join(tempfile.gettempdir(), f"douyin-cdp-{os.getpid()}")
    shutil.rmtree(profile, ignore_errors=True)

    print("      [cdp] 启动 headless 浏览器获取直链…")
    proc = subprocess.Popen(
        [browser, "--headless=new", "--disable-gpu", "--no-first-run",
         "--disable-extensions", "--mute-audio",
         f"--remote-debugging-port={port}", "--remote-allow-origins=*",
         f"--user-data-dir={profile}", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

    try:
        # 等 CDP 端口起来
        targets = None
        for _ in range(60):
            try:
                with urllib.request.urlopen(
                        f"http://127.0.0.1:{port}/json", timeout=2) as r:
                    targets = json.loads(r.read())
                    break
            except Exception:
                time.sleep(0.5)
        if not targets:
            print("[ERROR] CDP 端口未能启动", file=sys.stderr)
            return None, None

        page = next((t for t in targets if t.get("type") == "page"), None)
        if not page:
            print("[ERROR] 没有可用的 page target", file=sys.stderr)
            return None, None

        ws = websocket.create_connection(page["webSocketDebuggerUrl"], timeout=60)
        msg_id = 0

        def send(method, params=None):
            nonlocal msg_id
            msg_id += 1
            ws.send(json.dumps({"id": msg_id, "method": method,
                                "params": params or {}}))
            return msg_id

        send("Network.enable")
        send("Page.enable")

        # 先访问首页种匿名标识（ttwid/msToken），再进视频页，成功率更高。
        # 注意：不能等 Page.loadEventFired —— 浏览器启动时 about:blank 已触发过该事件，
        # 循环会立即退出导致首页 cookie 未种好。固定 sleep 让首页完全加载稳定。
        print("      [cdp] 先访问 douyin.com 首页种标识…")
        send("Page.navigate", {"url": "https://www.douyin.com/"})
        time.sleep(8)

        send("Page.navigate",
             {"url": f"https://www.douyin.com/video/{video_id}"})
        send("Network.enable")  # 重新 enable，对齐已验证的 POC 逻辑

        title, mp4_url = None, None
        req_url = {}          # requestId -> URL 映射
        cdn_urls = []         # 视频元素实际请求的 CDN 直链（SSR 页面兜底用）
        t0 = time.time()
        while time.time() - t0 < 75:
            # 25 秒内没等到 detail 接口但已有 CDN 直链：SSR 页面，提前走兜底
            if mp4_url is None and cdn_urls and time.time() - t0 > 25:
                break
            try:
                msg = json.loads(ws.recv())
            except Exception:
                continue
            method = msg.get("method")
            if method == "Network.responseReceived":
                p = msg["params"]
                u = p["response"].get("url", "")
                req_url[p["requestId"]] = u
                # 记录视频 CDN 直链——有些视频页数据走 SSR 直出，
                # 不发 aweme/detail XHR，但 <video> 元素的 mp4 请求一定会有
                if "douyinvod.com" in u and ("video/tos" in u or ".mp4" in u):
                    cdn_urls.append(u)
                continue
            if method != "Network.loadingFinished":
                continue
            rid = msg["params"]["requestId"]
            resp_url = req_url.get(rid, "")
            # 匹配条件放宽：详情接口实际 URL 带尾斜杠/参数变体
            if ("aweme/detail" not in resp_url and
                    "aweme/v1" not in resp_url):
                continue
            body_id = send("Network.getResponseBody",
                           {"requestId": rid})
            body_msg = None
            # 用时间窗等响应而非固定次数——页面加载时事件大量堆积，
            # 固定次数的 recv 会被不匹配事件消耗完，永远等不到响应
            t1 = time.time()
            while time.time() - t1 < 10:
                try:
                    m = json.loads(ws.recv())
                    if m.get("id") == body_id:
                        body_msg = m
                        break
                except Exception:
                    continue
            if not (body_msg and body_msg.get("result", {}).get("body")):
                continue
            try:
                raw = body_msg["result"]["body"]
                if body_msg["result"].get("base64Encoded"):
                    import base64
                    raw = base64.b64decode(raw).decode("utf-8", errors="replace")
                detail = json.loads(raw).get("aweme_detail") or {}
            except Exception:
                continue
            title = detail.get("desc") or None
            if title:
                title = _clean_title(title)
            play = (detail.get("video") or {}).get("play_addr") or {}
            urls = play.get("url_list") or []
            if urls:
                mp4_url = urls[0]
                break

        if mp4_url:
            print(f"      [cdp] 直链获取成功（detail 接口）: {mp4_url[:70]}...")
            try:
                ws.close()
            except Exception:
                pass
            return title, mp4_url, None

        # ---- 兜底：detail 接口没出现（SSR 直出页面），直接用截获的 CDN 直链 ----
        if cdn_urls:
            print("      [cdp] detail 接口未出现（SSR 页面），改用截获的 CDN 直链…")
            if not title:
                try:
                    t_id = send("Runtime.evaluate",
                                {"expression": "document.title"})
                    t1 = time.time()
                    while time.time() - t1 < 10:
                        try:
                            m = json.loads(ws.recv())
                        except Exception:
                            continue
                        if m.get("id") == t_id:
                            v = (m.get("result", {}).get("result")
                                 or {}).get("value", "")
                            if v.endswith(" - 抖音"):
                                v = v[:-len(" - 抖音")]
                            title = _clean_title(v) if v else None
                            break
                except Exception:
                    pass
            try:
                ws.close()
            except Exception:
                pass
            local_file = _pick_cdn_media(dict.fromkeys(cdn_urls))
            if local_file:
                return title, None, local_file

        try:
            ws.close()
        except Exception:
            pass
        print("[ERROR] CDP 未能截获视频数据（抖音可能要求登录）", file=sys.stderr)
        return None, None, None
    except Exception as e:
        print(f"[ERROR] CDP 方案异常: {e}", file=sys.stderr)
        return None, None
    finally:
        proc.terminate()
        try:
            proc.kill()
        except Exception:
            pass


def download_with_ytdlp(video_url: str, dest: str, cookies_file: str = "") -> None:
    """yt-dlp 兜底下载（最后手段，需要 cookie 文件）"""
    print("      [yt-dlp] 尝试 yt-dlp 下载…")
    try:
        import yt_dlp
    except ImportError:
        sys.exit("[ERROR] 未安装 yt-dlp。安装: pip install yt-dlp")
    opts = {
        "outtmpl": dest.rsplit(".", 1)[0] + ".%(ext)s",
        "format": "mp4/best[ext=mp4]/best",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }
    if cookies_file:
        opts["cookiefile"] = cookies_file
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
        dl = (info.get("requested_downloads") or [])
        if dl and dl[0].get("filepath"):
            actual = dl[0]["filepath"]
            if os.path.abspath(actual) != os.path.abspath(dest):
                os.replace(actual, dest)
    except Exception as e:
        sys.exit(f"[ERROR] yt-dlp 兜底下载失败: {e}\n"
                 f"         抖音现已要求浏览器 cookie，请用 --cookies 指定 cookies.txt\n"
                 f"         （浏览器扩展 'Get cookies.txt LOCALLY' 可一键导出）")


# ═══════════════════════════════════════════════════════════
# 2. 转写
# ═══════════════════════════════════════════════════════════

def transcribe(mp4_path: str, model_size: str, language: str):
    from faster_whisper import WhisperModel

    # 本地模型优先：~/.whisper-models-local 存在且 model.bin 完整时直接用它，
    # 避免反复下载/缓存损坏问题
    local_model = os.path.join(os.path.expanduser("~"), ".whisper-models-local")
    local_bin = os.path.join(local_model, "model.bin")
    if os.path.exists(local_bin) and os.path.getsize(local_bin) > 10_000_000:
        print(f"[2/3] 加载本地 faster-whisper 模型: {local_model}")
        model = WhisperModel(local_model, device="cpu", compute_type="int8")
    else:
        print(f"[2/3] 加载 faster-whisper '{model_size}' 模型（首次会下载到 {MODEL_DIR}）")
        model = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8",
            download_root=MODEL_DIR,
        )
    print(f"[3/3] 转写中... (语言={language})")
    segments, info = model.transcribe(
        mp4_path,
        language=language,
        beam_size=1,
        vad_filter=True,
    )
    return list(segments), info


# ═══════════════════════════════════════════════════════════
# 3. 本地智能提取（无 API Key 时）
# ═══════════════════════════════════════════════════════════

def local_analysis(title: str, plain_text: str) -> dict:
    """无 LLM 时的本地规则提取

    通过关键词密度、段落结构和数字线索尝试提取有意义的分析结果。
    """
    # whisper 转写的中文常无标点（整段连排），先按句号类标点切，超长块再按逗号/空格二次切分
    raw_chunks = [s.strip() for s in re.split(r'[。！？；\n]', plain_text) if s.strip()]
    sentences = []
    for chunk in raw_chunks:
        if len(chunk) <= 60:
            sentences.append(chunk)
        else:
            sub = [s.strip() for s in re.split(r'[，,、：: ]', chunk) if len(s.strip()) > 4]
            sentences.extend(sub if sub else [chunk])
    full_text = plain_text[:6000]

    # ── 摘要 ──
    summary = ""
    title_keywords = [w for w in re.split(r'[#\s、，,]+', title) if len(w) >= 2]
    start = max(len(sentences) // 3, 1)
    for s in sentences[start:]:
        if len(s) > 10 and len(s) < 80:
            score = sum(1 for kw in title_keywords if kw in s)
            if score >= 1 or ("核心" in s or "关键" in s or "总结" in s or "本质" in s):
                summary = s
                break
    if not summary and sentences:
        mid_idx = len(sentences) // 2
        for offset in range(min(10, len(sentences) // 4)):
            idx = mid_idx + offset
            if idx < len(sentences) and 12 < len(sentences[idx]) < 80:
                summary = sentences[idx]
                break
    if not summary:
        summary = title
    if len(summary) > 100:
        summary = summary[:97] + "..."

    # ── 核心观点 ──
    section_markers = [
        r'(?:第[一二三四五六七八九十\d]|首先|其次|最后|另外|此外|还有|那么|所以|因此|但是|然而)',
        r'(?:什么是|如何|怎么|为什么|方式|方法|途径|步骤|类型|种类|分类)',
        r'(?:问题|答案|结论|重点|关键|核心|本质)',
        r'(?:比如|例如|举个|打个|就是|意思是|简单来说)',
    ]
    marker_pattern = '|'.join(section_markers)

    candidates = []
    for s in sentences:
        if len(s) < 8 or len(s) > 60:
            continue
        has_number = bool(re.search(r'[\d一二三四五六七八九十]', s))
        has_marker = bool(re.search(marker_pattern, s))
        if has_number or has_marker:
            candidates.append(s)

    key_points = []
    seen = set()
    for c in candidates:
        short = c[:15]
        if short not in seen:
            seen.add(short)
            key_points.append(c)
        if len(key_points) >= 6:
            break

    if len(key_points) < 3:
        for s in sentences:
            if len(s) > 15 and len(s) < 60 and s[:15] not in seen:
                seen.add(s[:15])
                key_points.append(s)
            if len(key_points) >= 4:
                break
    if not key_points:
        key_points = [title]

    # ── 金句 ──
    # 口播/视频字幕多为口语化短句，规则匹配书面句式（名言/这就是/不是…而是）
    # 命中率太低。改为"观点强度打分"：转折/反问/强情绪词/因果词命中即入选。
    quotes = []
    quote_patterns = [
        r'(?:不是.*而是|不是.*是|与其.*不如|宁可.*也不|没有.*只有|只有.*才能)',
        r'(?:说白了|归根结底|说到底|本质上|其实|真正|永远|唯一|根本)',
        r'(?:记住|请记住|一定要|千万不要|别再|不要)',
        r'(?:凭什么|为什么|到底|居然|竟然|居然会)',
        r'(?:最重要|最关键|最大的|最难|最容易|最值钱)',
        r'(?:这就是|这就是所谓|所谓|说白了)',
    ]
    for s in sentences:
        if len(s) < 8 or len(s) > 60:
            continue
        if s in [q.get("text", "") for q in quotes]:
            continue
        score = sum(1 for p in quote_patterns if re.search(p, s))
        score += 1 if ("?" in s or "!" in s or "？" in s or "！" in s) else 0
        score += 1 if any(kw in s for kw in ["真正", "本质", "根本", "唯一", "所有", "一切", "永远", "最"]) else 0
        if score >= 1:
            quotes.append({"text": s, "context": ""})
            if len(quotes) >= 8:
                break

    # 回退：规则没捞够时，按句子长度 + 观点词密度挑最像金句的短句
    if len(quotes) < 2:
        fallback_kw = ["不是", "而是", "其实", "真正", "本质", "永远", "唯一", "根本",
                       "记住", "为什么", "凭什么", "最关键", "最重要", "最"]
        ranked = []
        for s in sentences:
            if s in [q["text"] for q in quotes]:
                continue
            if len(s) < 10 or len(s) > 55:
                continue
            score = sum(1 for kw in fallback_kw if kw in s)
            if "？" in s or "！" in s or "?" in s or "!" in s:
                score += 1
            if score > 0:
                ranked.append((score, s))
        ranked.sort(key=lambda x: -x[0])
        for _, s in ranked[:8]:
            if s not in [q["text"] for q in quotes]:
                quotes.append({"text": s, "context": ""})
            if len(quotes) >= 8:
                break

    # ── 结构拆解 ──
    struct_type = "通用分析"
    breakdown = {}

    struct_signals = {
        "开场引入": [r'今天', r'大家', r'我们', r'各位', r'分享', r'聊聊'],
        "提出问题": [r'什么是', r'为什么', r'怎么', r'如何', r'问题', r'知道吗'],
        "核心论述": [r'首先', r'第二', r'第三', r'第[一二三四]', r'分类', r'类型', r'方式'],
        "举例说明": [r'比如', r'例如', r'举个', r'假设', r'你看', r'比方'],
        "方法总结": [r'方法', r'方式', r'途径', r'步骤', r'关键', r'重点', r'核心'],
        "结尾收束": [r'综上', r'最后', r'总结', r'所以', r'希望大家', r'下课'],
    }

    third = max(len(sentences) // 3, 3)
    first_part = sentences[:third]
    mid_part = sentences[third:2 * third]
    last_part = sentences[2 * third:]

    for label, patterns in struct_signals.items():
        search_in = first_part if "开场" in label or "提出" in label else (
            last_part if "结尾" in label or "总结" in label else mid_part
        )
        for s in search_in:
            if len(s) > 8 and any(re.search(p, s) for p in patterns):
                breakdown[label] = s[:60]
                break

    if not breakdown:
        breakdown["开场"] = sentences[0][:60] if sentences else ""
        breakdown["核心内容"] = f"全文约 {len(sentences)} 句"
        breakdown["结尾"] = sentences[-1][:60] if len(sentences) > 1 else ""

    if "知识" in title or "学习" in title or "教程" in title or "教你" in title:
        struct_type = "知识口播"
    elif "vlog" in title.lower() or "日常" in title:
        struct_type = "Vlog"
    elif "搞笑" in title or "段子" in title:
        struct_type = "情景剧"
    elif any(kw in title for kw in ["测评", "推荐", "种草", "好物"]):
        struct_type = "营销内容"
    elif any(kw in title for kw in ["采访", "对话", "访谈"]):
        struct_type = "采访"

    # ── 内容判断 ──
    stance = "创作者"
    credibility = "-"
    if any(kw in full_text for kw in ["研究", "数据", "调查", "实验", "论文"]):
        credibility = "中高: 文本含研究/数据类引用"
    elif len(sentences) > 30:
        credibility = "中: 内容有一定篇幅，但无明确数据来源标注"
    else:
        credibility = "-: 文本过短，无法判断可信度"

    takeaway = "-"
    if len(sentences) > 40:
        takeaway = "内容体量较大，适合作为结构化口播学习素材"
    elif len(sentences) > 15:
        takeaway = "中等体量内容，可关注其开头/结尾的结构设计"

    # ── 亮点 ──
    highlights = []
    for i, p in enumerate(key_points[:6]):
        highlights.append({
            "name": p[:20] + ("..." if len(p) > 20 else ""),
            "desc": p if len(p) <= 60 else p[:57] + "...",
            "tag": f"观点{i + 1:02d}"
        })

    return {
        "summary": summary,
        "key_points": key_points,
        "structure": {"type": struct_type, "breakdown": breakdown},
        "quotes": quotes,
        "judgment": {"stance": stance, "credibility": credibility, "takeaway": takeaway},
        "highlights": highlights,
    }


# ═══════════════════════════════════════════════════════════
# 4. HTML 报告
# ═══════════════════════════════════════════════════════════

HTML_CSS = r"""
  :root {
    --bg:          oklch(0.975 0.005 90);
    --bg-warm:     oklch(0.96 0.01 85);
    --surface:     #fff;
    --surface-hover: oklch(0.98 0.005 88);
    --text:        oklch(0.18 0.01 90);
    --text-secondary: oklch(0.42 0.01 90);
    --text-muted:  oklch(0.58 0.01 90);
    --accent:      oklch(0.48 0.18 25);
    --accent-light: oklch(0.70 0.12 30);
    --accent-bg:   oklch(0.92 0.04 35);
    --accent-bg-light: oklch(0.96 0.02 30);
    --border:      oklch(0.88 0.01 85);
    --shadow-sm:   0 1px 3px oklch(0 0 0 / 0.06);
    --shadow-md:   0 4px 16px oklch(0 0 0 / 0.08);
    --shadow-lg:   0 8px 32px oklch(0 0 0 / 0.10);
    --radius-sm:   8px;
    --radius-md:   14px;
    --radius-lg:   22px;
  }

  * { margin:0; padding:0; box-sizing:border-box; }

  body {
    font-family: system-ui, -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
    background: var(--bg); color: var(--text); line-height:1.75;
    -webkit-font-smoothing: antialiased;
  }
  h1, .big-text, .quote-text, .detail-title, .cap-title,
  .point-num, .pd-rank, .quote-mark {
    font-family: 'PingFang SC', 'Noto Serif CJK SC', 'SimSun', serif;
  }

  .container { max-width:880px; margin:0 auto; padding:0 24px 80px; }

  /* Hero */
  .hero { text-align:center; padding:80px 0 48px; }
  .hero-badge {
    display:inline-flex; align-items:center; gap:8px;
    padding:5px 16px; border-radius:999px;
    background: oklch(0.85 0.06 30 / 0.12);
    font-size:12px; color:var(--accent); font-weight:600;
    letter-spacing:0.5px; margin-bottom:20px;
  }
  .hero-badge .dot { width:6px; height:6px; border-radius:50%; background:var(--accent); }
  .hero h1 {
    font-size:clamp(1.8rem, 4.5vw, 2.8rem);
    font-weight:900; line-height:1.35; letter-spacing:0.02em;
  }
  .hero-meta {
    display:flex; gap:24px; justify-content:center;
    margin-top:14px; font-size:13px; color:var(--text-muted);
  }

  /* Summary */
  .summary-card {
    background:var(--surface); border-radius:var(--radius-lg);
    padding:48px 40px; margin-bottom:44px;
    box-shadow:var(--shadow-lg);
    position:relative; overflow:hidden;
  }
  .summary-card::before {
    content:''; position:absolute; top:0; left:0;
    width:4px; height:100%;
    background:linear-gradient(180deg, var(--accent), var(--accent-light));
  }
  .summary-card .label {
    font-size:11px; text-transform:uppercase; letter-spacing:0.14em;
    color:var(--accent); font-weight:700; margin-bottom:14px;
  }
  .summary-card .big-text {
    font-size:clamp(1.15rem, 2.2vw, 1.45rem);
    font-weight:600; line-height:1.9;
  }
  .big-text em {
    font-style:normal; color:var(--accent); font-weight:700;
  }

  /* Section */
  .section-head {
    display:flex; align-items:center; gap:12px; margin-bottom:24px;
  }
  .section-head .icon {
    width:32px; height:32px; border-radius:8px;
    background:var(--accent-bg);
    display:flex; align-items:center; justify-content:center;
    font-size:15px; flex-shrink:0;
  }
  .section-head h2 {
    font-size:1.25rem; font-weight:700;
  }

  /* Quotes */
  .quotes-section { margin-bottom:44px; }
  .quotes-grid {
    display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:20px;
  }
  .quote-card {
    background:var(--surface); border-radius:var(--radius-md);
    padding:36px 28px 32px; box-shadow:var(--shadow-md);
    transition:transform 0.2s,box-shadow 0.2s; position:relative;
  }
  .quote-card:hover { transform:translateY(-2px); box-shadow:var(--shadow-lg); }
  .quote-mark {
    font-size:4rem; font-weight:900; color:var(--accent-bg);
    line-height:0.6; margin-bottom:12px;
  }
  .quote-text {
    font-size:1.15rem; font-weight:700; line-height:1.8;
  }
  .share-tag {
    display:inline-block; margin-top:16px;
    padding:3px 12px; font-size:11px; border-radius:999px;
    background:var(--accent-bg-light); color:var(--accent);
    font-weight:500; letter-spacing:0.5px;
  }
  .quote-card { cursor:pointer; }

  /* Quote Modal - 3:4 弹窗卡片 */
  .quote-modal {
    position:fixed; inset:0; z-index:999;
    display:none; align-items:center; justify-content:center;
    background:oklch(0.16 0.01 30 / 0.55);
    backdrop-filter:blur(5px); -webkit-backdrop-filter:blur(5px);
    padding:24px;
  }
  .quote-modal.open { display:flex; animation:fadeIn 0.25s ease; }
  .quote-modal-card {
    width:min(72vw, 360px); aspect-ratio:3/4;
    background:linear-gradient(165deg, #fffdf7 0%, #fdf5ea 55%, #f8ecdd 100%);
    border-radius:0;
    box-shadow:0 28px 70px oklch(0 0 0 / 0.30);
    padding:46px 34px 32px;
    display:flex; flex-direction:column; align-items:center; text-align:center;
    position:relative; overflow:hidden;
    animation:cardIn 0.35s cubic-bezier(0.18,0.9,0.32,1.15);
  }
  .quote-modal-card::before {
    content:''; position:absolute; top:-80px; right:-80px; width:220px; height:220px;
    border-radius:50%;
    background:radial-gradient(circle, oklch(0.92 0.07 45 / 0.32), transparent 70%);
  }
  .quote-modal-card::after {
    content:''; position:absolute; bottom:-60px; left:-60px; width:160px; height:160px;
    border-radius:50%;
    background:radial-gradient(circle, oklch(0.90 0.06 75 / 0.28), transparent 70%);
  }
  .qm-close {
    position:absolute; top:16px; right:16px; width:38px; height:38px;
    border-radius:50%; border:none; cursor:pointer; z-index:2;
    background:oklch(0.90 0.03 40 / 0.55); color:var(--text-secondary);
    font-size:15px; line-height:1;
    display:flex; align-items:center; justify-content:center;
    transition:all 0.25s;
  }
  .qm-close:hover { background:var(--accent); color:#fff; transform:rotate(90deg); }
  .qm-mark {
    font-family:'PingFang SC','Noto Serif CJK SC',serif;
    font-size:4.4rem; font-weight:900; color:var(--accent-light);
    line-height:0.7; margin:8px 0 12px; opacity:0.85; z-index:1;
  }
  .qm-text {
    flex:1; display:flex; align-items:center; justify-content:center;
    font-family:'PingFang SC','Noto Serif CJK SC','SimSun',serif;
    font-size:1.4rem; font-weight:700; line-height:1.9;
    letter-spacing:0.02em; z-index:1; padding:0 4px;
  }
  .qm-footer { z-index:1; }
  .qm-tag {
    display:inline-block; padding:5px 16px; border-radius:999px;
    background:var(--accent-bg); color:var(--accent);
    font-size:12px; font-weight:600; letter-spacing:0.5px; margin-bottom:12px;
  }
  .qm-brand {
    font-size:11px; color:var(--text-muted); letter-spacing:0.14em;
    display:flex; align-items:center; justify-content:center; gap:8px;
  }
  .qm-brand::before, .qm-brand::after {
    content:''; width:20px; height:1px; background:var(--border);
  }
  @keyframes fadeIn {{ from{{opacity:0}} to{{opacity:1}} }}
  @keyframes cardIn {{
    from{{opacity:0; transform:translateY(26px) scale(0.92)}}
    to{{opacity:1; transform:translateY(0) scale(1)}}
  }}

  /* Bookshelf (Capsules) */
  .bookshelf-section { margin-bottom:44px; }
  .capsule-grid {
    display:grid; grid-template-columns:repeat(2, 1fr); gap:14px;
  }
  .capsule {
    background:var(--surface); border-radius:var(--radius-md);
    padding:26px 22px; cursor:pointer;
    border:1px solid var(--border); box-shadow:var(--shadow-sm);
    transition:all 0.2s;
  }
  .capsule:hover {
    transform:translateY(-1px); box-shadow:var(--shadow-md);
    border-color:var(--accent-light);
  }
  .cap-icon { font-size:1.6rem; display:block; margin-bottom:14px; }
  .cap-title { font-size:0.95rem; font-weight:700; margin-bottom:4px; }
  .cap-sub {
    font-size:12px; color:var(--text-muted);
    display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical;
    overflow:hidden;
  }

  .capsule-detail {
    display:none;
    background:var(--surface); border-radius:var(--radius-lg);
    padding:40px 36px; margin-top:20px;
    box-shadow:var(--shadow-lg); position:relative;
    animation:slideUp 0.3s ease;
  }
  .capsule-detail.active { display:block; }

  @keyframes slideUp {
    from { opacity:0; transform:translateY(12px); }
    to   { opacity:1; transform:translateY(0); }
  }

  .close-btn {
    position:absolute; top:12px; right:16px;
    width:36px; height:36px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:1.2rem; color:var(--text-muted); cursor:pointer;
    background:none; border:none;
    transition:background 0.15s;
  }
  .close-btn:hover { background:var(--surface-hover); color:var(--text); }

  .detail-title {
    font-size:1.25rem; font-weight:700; padding-right:40px;
    margin-bottom:24px;
  }

  /* Points List */
  .points-list { display:flex; flex-direction:column; gap:18px; }
  .point-item { display:flex; gap:16px; align-items:flex-start; }
  .point-num {
    width:36px; height:36px; border-radius:10px;
    background:var(--accent-bg);
    display:flex; align-items:center; justify-content:center;
    font-weight:700; color:var(--accent); flex-shrink:0;
  }
  .point-content h4 { font-size:0.95rem; font-weight:700; margin-bottom:4px; }
  .point-content p { font-size:0.85rem; color:var(--text-secondary); line-height:1.7; }

  /* Struct List */
  .struct-list { display:flex; flex-direction:column; gap:14px; }
  .struct-item { display:flex; gap:16px; align-items:baseline; }
  .struct-label {
    flex-shrink:0; font-weight:700; font-size:0.88rem;
    color:var(--accent); min-width:72px;
  }
  .struct-content { font-size:0.9rem; color:var(--text-secondary); line-height:1.7; }

  /* Judge Grid */
  .judge-grid {
    display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:16px;
  }
  .judge-mini {
    background:oklch(0.97 0.005 88); border-radius:var(--radius-sm);
    padding:22px 18px;
  }
  .jm-label {
    font-size:11px; text-transform:uppercase; letter-spacing:0.08em;
    color:var(--accent); font-weight:600; margin-bottom:6px;
  }
  .jm-title { font-weight:700; font-size:0.9rem; margin-bottom:6px; }
  .jm-desc { font-size:0.82rem; color:var(--text-secondary); line-height:1.7; }

  /* Paradox List */
  .paradox-detail-list {
    display:flex; flex-direction:column; gap:1px;
    background:var(--border); border-radius:var(--radius-sm);
    overflow:hidden;
  }
  .paradox-detail-item {
    display:grid; grid-template-columns:52px 1fr auto;
    gap:16px; padding:14px 18px; background:var(--surface);
  }
  .pd-rank {
    font-size:1.5rem; font-weight:900; color:var(--accent-light);
    text-align:center; line-height:1.2;
  }
  .pd-rank.top3 { color:var(--accent); }
  .pd-name { font-weight:700; font-size:0.9rem; line-height:1.2; }
  .pd-desc { font-size:0.82rem; color:var(--text-secondary); margin-top:2px; }
  .pd-tag {
    font-size:11px; border-radius:999px; padding:2px 10px;
    background:var(--accent-bg-light); color:var(--text-muted);
    align-self:center; white-space:nowrap;
  }

  /* Footer */
  .footer {
    text-align:center; color:var(--text-muted); font-size:12px;
    margin-top:52px; padding-top:20px; border-top:1px solid var(--border);
  }
  .footer p { margin:0; }
  .footer .brand { font-weight:600; color:var(--text-secondary); }

  /* Responsive */
  @media (max-width:640px) {
    .hero             { padding:48px 0 32px; }
    .summary-card     { padding:32px 24px; }
    .capsule-grid     { grid-template-columns:repeat(2, 1fr); }
    .capsule-detail   { padding:28px 20px; }
    .quote-card       { padding:28px 20px 24px; }
    .paradox-detail-item { grid-template-columns:40px 1fr; gap:10px; padding:12px 14px; }
    .paradox-detail-item .pd-tag { display:none; }
    .judge-grid       { grid-template-columns:1fr; }
  }
"""

HTML_PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - 视频解析报告</title>
<style>{css}</style>
</head>
<body>
<div class="container">

<header class="hero">
  <div class="hero-badge"><span class="dot"></span>抖音 - 视频解析</div>
  <h1>{title}</h1>
  {hero_meta}
</header>

<div class="summary-card">
  <div class="label">一句话总结</div>
  <div class="big-text">{summary_body}</div>
</div>

<section class="quotes-section">
  <div class="section-head"><div class="icon">&#10022;</div><h2>金句卡片 - 适合分享</h2></div>
  <div class="quotes-grid">{quote_cards}</div>
</section>

<section class="bookshelf-section">
  <div class="section-head"><div class="icon" style="font-size:18px;">&#128218;</div><h2>深度解析：点击查看详情</h2></div>
  <div class="capsule-grid">
    <div class="capsule" data-cid="points">
      <span class="cap-icon">&#128161;</span>
      <div class="cap-title">{point_count}个核心观点</div>
      <div class="cap-sub">{point_sub}</div>
    </div>
    <div class="capsule" data-cid="structure">
      <span class="cap-icon">&#128196;</span>
      <div class="cap-title">视频结构拆解</div>
      <div class="cap-sub">{struct_type}</div>
    </div>
    <div class="capsule" data-cid="judgment">
      <span class="cap-icon">&#128270;</span>
      <div class="cap-title">内容判断</div>
      <div class="cap-sub">{judge_sub}</div>
    </div>
    <div class="capsule" data-cid="highlight">
      <span class="cap-icon">&#129352;</span>
      <div class="cap-title">内容亮点</div>
      <div class="cap-sub">{highlight_sub}</div>
    </div>
  </div>

  <div class="capsule-detail" id="detail-points">
    <button class="close-btn" data-action="close">&#10005;</button>
    <div class="detail-title">{point_count}个核心观点</div>
    <div class="points-list">{point_items}</div>
  </div>

  <div class="capsule-detail" id="detail-structure">
    <button class="close-btn" data-action="close">&#10005;</button>
    <div class="detail-title">视频结构拆解</div>
    <div class="struct-list">{struct_items}</div>
  </div>

  <div class="capsule-detail" id="detail-judgment">
    <button class="close-btn" data-action="close">&#10005;</button>
    <div class="detail-title">内容判断</div>
    <div class="judge-grid">{judge_cards}</div>
  </div>

  <div class="capsule-detail" id="detail-highlight">
    <button class="close-btn" data-action="close">&#10005;</button>
    <div class="detail-title">内容亮点</div>
    <div class="paradox-detail-list">{highlight_items}</div>
  </div>
</section>

<div class="footer">
  <p class="brand">douyin-video-parser</p>
  <p>丢个抖音链接，还你一份结构化分析 &middot; {date}</p>
</div>

</div>

<!-- 金句弹窗 -->
<div class="quote-modal" id="quote-modal">
  <div class="quote-modal-card">
    <button class="qm-close" aria-label="关闭">&#10005;</button>
    <div class="qm-mark">&ldquo;</div>
    <div class="qm-text" id="qm-text"></div>
    <div class="qm-footer">
      <span class="qm-tag" id="qm-tag"></span>
      <div class="qm-brand">视频金句卡片</div>
    </div>
  </div>
</div>

<script>
(function(){{
  var active=null;
  document.addEventListener('click', function(e){{
    var cap = e.target.closest('[data-cid]');
    if (cap) {{
      var id = cap.getAttribute('data-cid');
      if(active) active.classList.remove('active');
      var d = document.getElementById('detail-' + id);
      if (d) {{ d.classList.add('active'); d.scrollIntoView({{behavior:'smooth',block:'nearest'}}); active = d; }}
      return;
    }}
    if (e.target.closest('[data-action="close"]')) {{
      if (active) {{ active.classList.remove('active'); active = null; }}
    }}
  }});

  // 金句弹窗
  var qModal = document.getElementById('quote-modal');
  var qmText = document.getElementById('qm-text');
  var qmTag = document.getElementById('qm-tag');
  function openQuote(text, tag) {{
    qmText.textContent = text;
    qmTag.textContent = tag;
    qModal.classList.add('open');
    document.body.style.overflow = 'hidden';
  }}
  function closeQuote() {{
    qModal.classList.remove('open');
    document.body.style.overflow = '';
  }}
  document.addEventListener('click', function(e) {{
    var qc = e.target.closest('.quote-card');
    if (qc) {{ openQuote(qc.getAttribute('data-quote'), qc.getAttribute('data-tag')); return; }}
    if (e.target.closest('.qm-close') || e.target === qModal) closeQuote();
  }});
  document.addEventListener('keydown', function(e) {{ if (e.key === 'Escape') closeQuote(); }});
}})();
</script>

</body>
</html>"""


def generate_html(title: str, duration_sec, plain_text: str,
                  timed_text: str, analysis: dict) -> str:
    """生成 HTML 报告（所有用户内容均经 html.escape 转义）"""
    a = analysis or {}

    # Hero meta
    meta_parts = []
    if duration_sec:
        meta_parts.append(f"<span>时长 {_esc(_format_duration(duration_sec))}</span>")
    meta_parts.append("<span>抖音</span>")
    hero_meta = f'<div class="hero-meta">{"".join(meta_parts)}</div>' if meta_parts else ""

    # 一句话总结
    summary = a.get("summary", title)
    summary_esc = _esc(summary)
    # 给【关键词】加 em 强调
    summary_body = re.sub(
        r'【(.+?)】', r'<em>\1</em>', summary_esc
    )
    if "[" not in summary_esc and len(summary) > 15:
        words = summary[:15]
        summary_body = summary_esc.replace(_esc(words), f"<em>{_esc(words)}</em>", 1)

    # 金句
    share_tags = ["朋友圈金句", "情感共鸣", "引人深思", "社交媒体", "职场共鸣", "人生感悟"]
    quotes = a.get("quotes", [])[:8]
    quote_cards = ""
    for i, q in enumerate(quotes):
        tag = share_tags[i % len(share_tags)]
        qtext = q.get("text", q) if isinstance(q, dict) else q
        quote_cards += f"""<div class="quote-card" data-quote="{_esc(qtext)}" data-tag="{_esc(tag)}" title="点击查看大图">
  <div class="quote-mark">&ldquo;</div>
  <div class="quote-text">{_esc(qtext)}</div>
  <span class="share-tag">{_esc(tag)}</span>
</div>"""
    if not quote_cards:
        quote_cards = '<p style="color:var(--text-muted);font-size:14px;">暂无金句数据</p>'

    # 核心观点
    points = a.get("key_points", [])
    point_items = ""
    point_sub = ""
    for i, p in enumerate(points):
        if isinstance(p, dict):
            point_items += f"""<div class="point-item">
  <div class="point-num">{i+1:02d}</div>
  <div class="point-content">
    <h4>{_esc(p.get('title',''))}</h4>
    <p>{_esc(p.get('desc',''))}</p>
  </div>
</div>"""
            if i < 2:
                point_sub += (", " if point_sub else "") + _esc(p.get("title", ""))[:10]
            elif i == 2:
                point_sub += "..."
        else:
            point_items += f"""<div class="point-item">
  <div class="point-num">{i+1:02d}</div>
  <div class="point-content"><h4>{_esc(p)}</h4></div>
</div>"""
            if i < 2:
                point_sub += (", " if point_sub else "") + _esc(p[:10])
            elif i == 2:
                point_sub += "..."

    point_count = len(points)
    if not point_sub:
        point_sub = "点击查看详情"

    # 结构拆解
    st = a.get("structure", {}) or {}
    struct_type = _esc(st.get("type", "分段解读"))
    bd = st.get("breakdown", {})
    struct_items = ""
    if bd:
        for k, v in bd.items():
            struct_items += f"""<div class="struct-item">
  <span class="struct-label">{_esc(k)}</span>
  <span class="struct-content">{_esc(v)}</span>
</div>"""
    else:
        struct_items = '<p style="color:var(--text-muted);font-size:14px;">暂无结构拆解数据</p>'

    # 内容判断
    j = a.get("judgment", {}) or {}
    judge_cards = ""
    jmap = [
        ("立场", "stance"),
        ("可信度", "credibility"),
        ("可借鉴", "takeaway"),
    ]
    for label, key in jmap:
        val = j.get(key, "-")
        val_esc = _esc(val)
        if isinstance(val, str) and "-" not in val and len(val) < 60:
            judge_cards += f"""<div class="judge-mini">
  <div class="jm-label">{_esc(label)}</div>
  <div class="jm-title">{val_esc if len(val)<30 else val_esc[:27]+"..."}</div>
</div>"""
        else:
            title_part = val_esc[:24] + "..." if len(val) > 24 else val_esc
            judge_cards += f"""<div class="judge-mini">
  <div class="jm-label">{_esc(label)}</div>
  <div class="jm-title">{title_part}</div>
  <div class="jm-desc">{val_esc}</div>
</div>"""

    judge_sub = _esc(j.get("stance", "-")) + " - " + _esc(j.get("credibility", "-"))

    # 内容亮点
    highlights = a.get("highlights", [])
    if not highlights:
        for i, p in enumerate(points[:5]):
            text = p if isinstance(p, str) else p.get("title", "")
            highlights.append({"name": text, "desc": "", "tag": f"观点{i+1:02d}"})
    highlight_items = ""
    highlight_sub = ""
    for i, h in enumerate(highlights):
        if isinstance(h, dict):
            name = _esc(h.get("name", ""))
            desc = _esc(h.get("desc", ""))
            tag = _esc(h.get("tag", ""))
            top3_class = " top3" if i < 3 else ""
            highlight_items += f"""<div class="paradox-detail-item">
  <div class="pd-rank{top3_class}">{i+1:02d}</div>
  <div>
    <div class="pd-name">{name}</div>
    <div class="pd-desc">{desc}</div>
  </div>
  <span class="pd-tag">{tag}</span>
</div>"""
            if i < 2:
                highlight_sub += (", " if highlight_sub else "") + name[:8]
            elif i == 2:
                highlight_sub += "..."
    if not highlight_items:
        highlight_items = '<p style="color:var(--text-muted);font-size:14px;">暂无数据</p>'
    if not highlight_sub:
        highlight_sub = "点击查看详情"

    return HTML_PAGE.format(
        title=_esc(title),
        hero_meta=hero_meta,
        summary_body=summary_body,
        quote_cards=quote_cards,
        point_count=point_count, point_sub=_esc(point_sub), point_items=point_items,
        struct_type=struct_type, struct_items=struct_items,
        judge_sub=_esc(judge_sub), judge_cards=judge_cards,
        highlight_sub=_esc(highlight_sub), highlight_items=highlight_items,
        css=HTML_CSS,
        date=dt.datetime.now().strftime("%Y-%m-%d"),
    )


# ═══════════════════════════════════════════════════════════
# 5. 主入口
# ═══════════════════════════════════════════════════════════

def write_outputs(segments, out_dir: str, tag: str, video_id: str):
    os.makedirs(out_dir, exist_ok=True)
    date_prefix = dt.datetime.now().strftime("%m%d")
    label = f"{tag}-" if tag else ""

    timed_path = os.path.join(out_dir, f"{date_prefix}-{label}{video_id}-逐字稿.txt")
    plain_path = os.path.join(out_dir, f"{date_prefix}-{label}{video_id}-连贯稿.txt")

    with open(timed_path, "w", encoding="utf-8") as f_t, \
         open(plain_path, "w", encoding="utf-8") as f_p:
        plain_chunks = []
        for seg in segments:
            text = seg.text.strip()
            f_t.write(f"[{seg.start:6.1f}-{seg.end:6.1f}] {text}\n")
            plain_chunks.append(text)
        f_p.write(" ".join(plain_chunks))

    return timed_path, plain_path


def main():
    parser = argparse.ArgumentParser(description="抖音视频 -> 字幕稿 + HTML 报告（本地 whisper）")
    parser.add_argument("url", help="抖音视频链接（长链或短链都行）")
    parser.add_argument("--model", default="base",
                        choices=["tiny", "base", "small", "medium", "large-v3"],
                        help="whisper 模型大小，默认 base（速度/准确度平衡）")
    parser.add_argument("--language", default="zh", help="语言代码，默认 zh")
    parser.add_argument("--out-dir", default=None,
                        help="输出目录，默认写到脚本同级目录下的 work/ 下")
    parser.add_argument("--tag", default="",
                        help="文件名里加个识别标签，例如 '公共知识女博主'")
    parser.add_argument("--cookies", default="",
                        help="yt-dlp 兜底时使用的 cookies.txt 文件（Netscape 格式）")
    parser.add_argument("--keep-mp4", action="store_true",
                        help="保留下载的 mp4 文件（默认转写完会删）")
    parser.add_argument("--generate-html", action="store_true", default=True,
                        help="生成 HTML 报告（默认开启）")
    parser.add_argument("--no-html", action="store_true",
                        help="不生成 HTML 报告（仅输出 txt）")
    parser.add_argument("--print-transcript", action="store_true",
                        help="把连贯稿全文打印到终端（默认只打印摘要，避免敏感语音内容进入日志/终端回滚）")
    args = parser.parse_args()

    # 默认输出目录：脚本同级目录下的 work/
    if args.out_dir is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        args.out_dir = os.path.join(script_dir, "work")

    t0 = time.time()
    video_id = extract_video_id(args.url)
    print(f"[0/4] video_id = {video_id}")

    mp4_path = os.path.join(TEMP_DIR, f"douyin_{video_id}.mp4")
    title = None

    # ── 第 1 级：iesdouyin share API（快路径）──
    try:
        title = fetch_video_title(video_id)
        mp4_url = fetch_mp4_url(video_id)
        print(f"      title: {title}")
        print(f"      mp4 url: {mp4_url[:80]}...")
        download_video(mp4_url, mp4_path)
    except SystemExit:
        # ── 第 2 级：CDP 浏览器方案（主通道）──
        print("[info] iesdouyin share API 不可用，切换 CDP 浏览器方案…")
        cdp_title, mp4_url, local_file = fetch_video_via_cdp(video_id)
        if local_file:
            # CDN 兜底路径：文件已下载好（挑过带音轨的），直接用
            if cdp_title and (not title or "记录美好生活" in title):
                title = cdp_title
            print(f"      title: {title}")
            print(f"      media file: {local_file}")
            mp4_path = local_file
        elif not mp4_url:
            # ── 第 3 级：yt-dlp + cookies（最后手段）──
            print("[info] CDP 方案失败，尝试 yt-dlp 兜底…")
            download_with_ytdlp(args.url, mp4_path, args.cookies)
        else:
            if cdp_title and (not title or "记录美好生活" in title):
                title = cdp_title
            print(f"      title: {title}")
            download_video(mp4_url, mp4_path)

    segments, info = transcribe(mp4_path, args.model, args.language)

    timed, plain = write_outputs(segments, args.out_dir, args.tag, video_id)

    if not args.keep_mp4:
        try:
            os.remove(mp4_path)
        except OSError:
            pass

    elapsed = time.time() - t0
    print(f"\n[done] 用时 {elapsed:.0f} 秒，视频 {info.duration:.1f} 秒，共 {len(segments)} 段")
    print(f"  逐字稿: {timed}")
    print(f"  连贯稿: {plain}")

    # 生成 HTML 报告
    if not args.no_html:
        print(f"\n[html] 生成报告...")
        with open(plain, "r", encoding="utf-8") as f:
            transcript_text = f.read()

        analysis = local_analysis(title, transcript_text)

        html_content = generate_html(
            title=title,
            duration_sec=info.duration if info else None,
            plain_text=transcript_text,
            timed_text=None,
            analysis=analysis,
        )

        date_prefix = dt.datetime.now().strftime("%m%d")
        label = f"{args.tag}-" if args.tag else ""
        html_path = os.path.join(args.out_dir, f"{date_prefix}-{label}{video_id}-报告.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  HTML:   {html_path}")

    # 输出连贯稿：默认只打印摘要 + 文件路径（隐私考虑），
    # 需要全文时加 --print-transcript 显式打印
    with open(plain, "r", encoding="utf-8") as f:
        transcript_txt = f.read()
    if args.print_transcript:
        print(f"\n---连贯稿内容---")
        print(transcript_txt)
        print(f"---连贯稿结束---")
    else:
        preview = transcript_txt[:500] + ("..." if len(transcript_txt) > 500 else "")
        print(f"\n[连贯稿摘要·前500字]（完整内容见：{plain}，需全文打印请加 --print-transcript）")
        print(preview)


if __name__ == "__main__":
    main()
