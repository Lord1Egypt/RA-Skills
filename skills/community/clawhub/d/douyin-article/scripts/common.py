#!/usr/bin/env python3
"""douyin-article 公共函数模块。

包含跨平台命令探测、时间戳格式化、JSON 读写、CLIXML 噪声清理等共享工具。
"""
from __future__ import annotations
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Optional


def find_command(cmd: str) -> str:
    """跨平台探测命令路径。

    顺序：which/where → Windows 常见路径 → Unix 常见路径 → 原命令名 fallback。
    """
    # 1. 先试 which/where
    try:
        which = "where.exe" if sys.platform == "win32" else "which"
        result = subprocess.run(
            [which, cmd], capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0:
            path = result.stdout.strip().split("\n")[0].strip()
            if path and Path(path).is_file():
                return path
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # 2. Windows 常见安装路径
    if sys.platform == "win32":
        candidates = [
            rf"C:\ffmpeg\bin\{cmd}.exe",
            rf"C:\Program Files\ffmpeg\bin\{cmd}.exe",
            rf"C:\Program Files (x86)\ffmpeg\bin\{cmd}.exe",
            rf"C:\Users\{Path.home().name}\AppData\Local\Microsoft\WinGet\Links\{cmd}.exe",
        ]
        for p in candidates:
            if Path(p).is_file():
                return p

    # 3. Unix 常见路径
    for p in [f"/usr/local/bin/{cmd}", f"/usr/bin/{cmd}", f"/opt/homebrew/bin/{cmd}"]:
        if Path(p).is_file():
            return p

    # 4. fallback：直接返回命令名，让后续报错暴露具体问题
    return shutil.which(cmd) or cmd


def format_timestamp(seconds: float, include_hours: bool = True) -> str:
    """秒数 → mm:ss 或 HH:mm:ss 格式。"""
    total = max(0, int(round(seconds)))
    hours, remainder = divmod(total, 3600)
    minutes, secs = divmod(remainder, 60)
    if include_hours or hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


def write_json(path: Path, value: Any) -> None:
    """原子写入 JSON 文件（先写 .tmp 再 replace）。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    tmp.replace(path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def md5_file(path: Path) -> str:
    """计算文件 MD5，用于音频去重。"""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def clean_clixml(text: str) -> str:
    """清理 PowerShell CLIXML 序列化噪声。

    抖音实战发现：agent-browser 输出中混入 #<CLIXML 和 <Objs> 标签。
    """
    text = re.sub(r"#<\s*CLIXML.*?(?=https?|\[|$)", "", text, flags=re.DOTALL)
    text = re.sub(r'<Objs\s+xmlns="[^"]+">.*?</Objs>', "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", "", text)  # 兜底清理残留 XML 标签
    return text.strip()


def probe_media_duration(path: Path) -> float:
    """用 ffprobe 探测媒体时长（秒）。"""
    try:
        result = subprocess.run(
            [
                find_command("ffprobe"),
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "json",
                str(path),
            ],
            capture_output=True, text=True, timeout=10,
        )
        data = json.loads(result.stdout)
        return float(data.get("format", {}).get("duration", 0))
    except Exception:
        return 0.0


def run_cmd(cmd_args: list[str], timeout: int = 60) -> tuple[bool, str]:
    """运行命令，返回 (success, output)。

    统一处理 subprocess 调用，避免重复代码。
    """
    try:
        result = subprocess.run(
            cmd_args, capture_output=True, text=True, timeout=timeout
        )
        output = (result.stdout or "") + (result.stderr or "")
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, f"TIMEOUT after {timeout}s"
    except Exception as e:
        return False, str(e)


# ===== 抖音实战补丁：URL 提取相关 =====

# agent-browser 在 Windows 的实际路径
def get_agent_browser_path() -> str:
    """探测 agent-browser 可执行文件路径。"""
    candidates = [
        r"C:\Users\Administrator\AppData\Roaming\npm\agent-browser.cmd",
        shutil.which("agent-browser"),
    ]
    for p in candidates:
        if p and Path(p).is_file():
            return p
    return "agent-browser"  # fallback


# eval JS：从 video.src 提取直接 CDN URL（跳过 blob:）
JS_GET_VIDEO_URL = (
    "(function(){var v=document.querySelector('video');"
    "if(!v) return null;"
    "var s=v.src||v.currentSrc;"
    "return (s && s.startsWith('http') && s.indexOf('douyinvod')>-1) ? s : null})()"
)

# eval JS：获取当前页面的视频 ID（用于 __vid 匹配）
JS_GET_VIDEO_ID = (
    "(function(){var m=location.pathname.match(/(\\d+)/);"
    "return m ? m[1] : null})()"
)


def extract_url_from_eval(output: str) -> Optional[str]:
    """从 agent-browser eval 输出中提取 CDN URL。"""
    out = clean_clixml(output).strip().strip('"').strip("'")
    if out.startswith("http") and "douyinvod" in out:
        return out
    return None


def extract_url_from_network(output: str, vid: Optional[str] = None) -> Optional[str]:
    """从 agent-browser network requests 输出中提取匹配 __vid 的 CDN URL。

    抖音实战：network requests 累积所有历史请求，必须用 __vid 匹配当前视频。
    """
    out = clean_clixml(output)
    urls = re.findall(r"https://v\d+-web\.douyinvod\.com/[^\s\)\]\}]+", out)
    if not urls:
        return None
    if vid:
        matching = [u for u in urls if f"__vid={vid}" in u]
        if matching:
            return matching[-1]
    return urls[-1]


# ===== 错字修正字典（faster-whisper 在中文上的常见同音错字）=====

ERROR_CORRECTIONS = {
    # 长难句相关
    "长男具": "长难句",
    "长男句": "长难句",
    "长男剧": "长难句",
    "长南剧": "长难句",
    "长诞句": "长难句",
    "常诞句": "长难句",
    "长单剧": "长单句",
    "长丹句": "长难句",
    # 从句相关
    "宠具": "从句",
    "定语宠具": "定语从句",
    "名词性宠具": "名词性从句",
    "主语宠具": "主语从句",
    "宾与宠具": "宾语从句",
    "表与宠具": "表语从句",
    # 语法术语
    "主位": "主谓",
    "冰与": "宾语",
    "兵语": "宾语",
    "宾与": "宾语",
    "表裔": "表语",
    "表与": "表语",
    "菲菲语": "非谓语",
    "非语动词": "非谓语动词",
    "非位于": "非谓语",
    "非谓语语": "非谓语",
    "分位语": "非谓语",
    "后制定语": "后置定语",
    "位于动词": "谓语动词",
    "卫语动词": "谓语动词",
    "卫语": "谓语",
    "核心卫语": "核心谓语",
    "戒词": "介词",
    "借词": "介词",
    "疫群": "意群",
    "识权": "实权",
    "主心鼓": "主心骨",
    "小鼓钉": "小补丁",
    "补钉": "补丁",
    # 动词形式
    "异地": "ed",
    "双异地": "双ed",
    "多异地": "多ed",
    # 时态相关
    "实态": "时态",
    "实态变化": "时态变化",
    # 胶水/连接
    "浇水": "胶水",
    # 意义/记忆
    "记忆上的": "意义上的",
    "记忆": "意义",
    # 进阶/初级
    "出击": "初级",
    "出击伪装": "初级伪装",
    # 倒装
    "导装": "倒装",
    "导装翻译": "倒装翻译",
    "头重矫情": "头重脚轻",
    "头重矫轻": "头重脚轻",
    # 接着
    "接著": "接着",
    # 理据/例句
    "理据": "例句",
    # 履约
    "铝月": "履约",
    # 其他常见错字
    "摸狱者": "魔语者",
    "答应": "答疑",
    "脱踏": "拖沓",
    "前衣后果": "前因后果",
    "试试细节": "细枝末节",
    "指老虎": "纸老虎",
    "道歉": "叠加",
    "老保服": "劳保服",
    "野蛮": "野蔓",
    "派车": "派生",
    "式子": "句子",
    "剧子": "句子",
    # 英文识别修正
    "zart": "that",
    "Zart": "that",
    "downs out": "that",
    "mortise": "Maldives",
    # 语气词修正
    "语异内话": "语意内化",
    "语异": "语意",
    "盟盟": "盲目",
    "盟盟接受": "盲目接受",
    "顺度": "顺序",
    "顺之读": "顺序读",
    "顺著读": "顺序读",
    "顺著理解": "顺序理解",
    "顺度": "顺序",
    # 尾音修正
    "飞起": "废弃",
    "飞起了": "废弃了",
    "锌绿": "深绿",
    "锌绿植物": "深绿植物",
    # v3.1: 句法分析常见错字（11 集小宇宙英语课转录实测）
    # "句" 被识别为 "剧" / "具"
    "主剧": "主句",
    "分剧": "分句",
    "主剧分析": "主句分析",
    "分剧分析": "分句分析",
    "主剧翻译": "主句翻译",
    "分剧翻译": "分句翻译",
    "主剧跟分剧": "主句跟分句",
    "主分剧": "主分句",
    "主剧与分剧": "主句与分句",
    "主剧里边": "主句里边",
    "剧法分析": "句法分析",
    "剧法结构": "句法结构",
    "高级剧法": "高级句法",
    "剧子": "句子",  # 已有
    # "短语" 被识别为 "端语"
    "端语": "短语",
    "介词端语": "介词短语",
    "后置定语端语": "后置定语短语",
    # "先行词" 被识别为 "线型词" / "显型词" 等
    "线型词": "先行词",
    "显型词": "先行词",
    "先行位": "先行词",
    # "谓语" 被识别为 "位于"（已有"卫语"）
    "位于动词": "谓语动词",  # 已有
    "主谓宾": "主谓宾",  # 占位，确保不破坏
    # "表语" 被识别为 "表与"（已有）
    # "宾语" 被识别为 "宾与"（已有）
    # "定语从句" 被识别为 "定义从句"
    "定义从句": "定语从句",
    "定义从旧": "定语从句",
    # "原子核" 被识别为 "原子和"（教学用语）
    "原子和": "原子核",
    "原子和的": "原子核的",
    # "分析" 被识别为 "分祈" 等
    "分祈": "分析",
    # "成分" 被识别为 "城分"
    "城分": "成分",
    # "谓语" 误识别
    "谓位于": "谓语",
    # "提示" 被识别为 "提示" 正确，但 "提示语" 被识别为 "提示与"
    "提示与": "提示语",
    # "所有格" 被识别为 "所有隔"
    "所有隔": "所有格",
    # "答疑" 被识别为 "答应"（已有"答应": "答疑"）
    # "成分" 误识别为 "成汾"
    "成汾": "成分",
    # "句法" 被识别为 "剧法"（已加）
    # "句法结构" 误识别
    "剧法结构分析": "句法结构分析",
    # "表情达意" 被识别为 "表情打印" / "表情答疑"
    "表情打印": "表情达意",
    "表情答疑": "表情达意",
    "表情打印上": "表情达意",
    # "标识" 被识别为 "标上"（口语化）
    # "中央性" - 应保留（教学用语）
    # "抛丁" - 应为 "拆解" 的口误识别（保留口语风格）
    # "抛丁解句子" → "拆解句子"（v3.1 修复：只保留更长的 "抛丁解"，避免重复替换）
    "抛丁解": "拆解",
    # " dishes" / 餐桌等 - 已跳过
    # "诸语" - 应为 "赘语"
    "诸语": "赘语",
    # "炸一读" - 应为 "乍一读"
    "炸一读": "乍一读",
    # "强调" 被识别为 "强调"
    # "去到那里边" - 口语，保留
}


def apply_error_corrections(text: str) -> str:
    """应用错字修正字典。"""
    for wrong, right in ERROR_CORRECTIONS.items():
        text = text.replace(wrong, right)
    return text


# ===== 平台抽象层（v3.0：抖音/B站/小宇宙/YouTube 四平台支持）=====

# 平台检测正则
DOUYIN_URL_RE = re.compile(r"https?://v\.douyin\.com/[A-Za-z0-9_]+/?")
BILIBILI_URL_RE = re.compile(r"https?://www\.bilibili\.com/video/(BV[\w]+)")
BILIBILI_P_RE = re.compile(r"[?&]p=(\d+)")
# v3.0 新增：小宇宙 episode / podcast URL
XIAOYUZHOU_EPISODE_RE = re.compile(r"https?://(?:www\.)?xiaoyuzhoufm\.com/(?:episode|podcast)/([A-Za-z0-9]+)")
# v3.0 新增：YouTube 视频/Shorts URL
YOUTUBE_URL_RE = re.compile(r"https?://(?:www\.|m\.)?(?:youtube\.com/(?:watch\?v=|shorts/|embed/|live/)|youtu\.be/)([\w-]{11})")


def detect_platform(url: str) -> str:
    """检测 URL 所属平台。

    返回 'douyin' / 'bilibili' / 'xiaoyuzhou' / 'youtube' / 'unknown'
    """
    if DOUYIN_URL_RE.search(url):
        return "douyin"
    if BILIBILI_URL_RE.search(url):
        return "bilibili"
    if XIAOYUZHOU_EPISODE_RE.search(url):
        return "xiaoyuzhou"
    if YOUTUBE_URL_RE.search(url):
        return "youtube"
    return "unknown"


def extract_bvid(url: str) -> Optional[str]:
    """从 B 站 URL 提取 BV 号。"""
    m = BILIBILI_URL_RE.search(url)
    return m.group(1) if m else None


def extract_p(url: str) -> int:
    """从 B 站 URL 提取 p 参数（分 P 编号，默认 1）。"""
    m = BILIBILI_P_RE.search(url)
    return int(m.group(1)) if m else 1


def normalize_bilibili_url(url: str) -> str:
    """规范化 B 站 URL：去掉 spm_id_from 等追踪参数，保留 BV 号和 p 参数。"""
    bvid = extract_bvid(url)
    if not bvid:
        return url
    p = extract_p(url)
    if p > 1:
        return f"https://www.bilibili.com/video/{bvid}?p={p}"
    return f"https://www.bilibili.com/video/{bvid}"


def extract_xiaoyuzhou_id(url: str) -> Optional[str]:
    """从小宇宙 URL 提取 episode/podcast ID。"""
    m = XIAOYUZHOU_EPISODE_RE.search(url)
    return m.group(1) if m else None


def normalize_xiaoyuzhou_url(url: str) -> str:
    """规范化小宇宙 URL：去掉追踪参数，保留 episode/podcast ID。"""
    eid = extract_xiaoyuzhou_id(url)
    if not eid:
        return url
    # 默认按 episode 处理（转录场景绝大多数是 episode）
    if "/podcast/" in url:
        return f"https://www.xiaoyuzhoufm.com/podcast/{eid}"
    return f"https://www.xiaoyuzhoufm.com/episode/{eid}"


def extract_youtube_id(url: str) -> Optional[str]:
    """从 YouTube URL 提取 11 位视频 ID。"""
    m = YOUTUBE_URL_RE.search(url)
    return m.group(1) if m else None


def normalize_youtube_url(url: str) -> str:
    """规范化 YouTube URL：统一为 https://www.youtube.com/watch?v=ID 格式。"""
    vid = extract_youtube_id(url)
    if not vid:
        return url
    return f"https://www.youtube.com/watch?v={vid}"


def parse_input_urls_unified(input_path: Path) -> list[dict]:
    """解析输入文件（统一版 v4.0）：自动识别抖音/B站/小宇宙/YouTube/通用平台 链接。

    返回 [{url, title?, platform, line}]
    - platform: 'douyin' / 'bilibili' / 'xiaoyuzhou' / 'youtube' / 'ytdlp-generic'
    - 抖音：支持分享文本（含【标题】）
    - B站/小宇宙/YouTube：URL 自动规范化，标题由对应 adapter 元数据提取
    - v4.0 ytdlp-generic：Vimeo/TikTok/Twitter 等 yt-dlp 支持平台
    """
    items = []
    share_title_re = re.compile(r"【([^\】]+)】")
    for i, line in enumerate(input_path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        platform = detect_platform(line)
        # v4.0: detect_platform 未识别时，尝试 yt-dlp 通用平台
        if platform == "unknown":
            if is_ytdlp_supported_url(line):
                platform = "ytdlp-generic"
            else:
                continue

        if platform == "douyin":
            url_match = DOUYIN_URL_RE.search(line)
            url = url_match.group(0)
            title_match = share_title_re.search(line)
            title = title_match.group(1) if title_match else None
        elif platform == "bilibili":
            url = normalize_bilibili_url(line)
            title = None
        elif platform == "xiaoyuzhou":
            url = normalize_xiaoyuzhou_url(line)
            title = None
        elif platform == "youtube":
            url = normalize_youtube_url(line)
            title = None
        elif platform == "ytdlp-generic":
            # v4.0: yt-dlp 全平台（Vimeo/TikTok/Twitch/Dailymotion/Twitter 等）
            url = line.strip()
            title = None
        else:
            continue

        items.append({"url": url, "title": title, "platform": platform, "line": i})
    return items


# ===== v4.0 新增：yt-dlp 全平台 URL 检测 + 语言检测 + SRT 解析 =====

# yt-dlp 常见平台域名（除已显式支持的 4 个）
YTDLP_GENERIC_DOMAINS = (
    "vimeo.com", "tiktok.com", "twitch.tv", "dailymotion.com",
    "twitter.com", "x.com", "instagram.com", "facebook.com",
    "reddit.com", "soundcloud.com", "pinterest.com", "linkedin.com",
    "streamable.com", "vevo.com", "wikipedia.org", "udemy.com",
    "coursera.org", "skillshare.com", "ted.com", "loom.com",
)


def is_ytdlp_supported_url(url: str) -> bool:
    """v4.0: 检测 URL 是否属于 yt-dlp 支持的通用平台（非 4 个显式平台）。

    用于扩展支持 Vimeo/TikTok/Twitch 等平台，无需为每个平台写 adapter。
    """
    url_lower = url.lower()
    for domain in YTDLP_GENERIC_DOMAINS:
        if domain in url_lower:
            return True
    return False


def detect_language(text: str) -> str:
    """v4.0: 检测文本主要语言。

    基于 Unicode 字符范围统计，返回 'zh' / 'en' / 'ja' / 'ko' / 'unknown'。
    用于判断是否触发翻译管线。
    """
    if not text or not text.strip():
        return "unknown"

    # 统计各语言字符数
    cjk_unified = 0      # 中日韩统一表意文字
    hiragana = 0         # 平假名（日文）
    katakana = 0         # 片假名（日文）
    hangul = 0           # 韩文
    latin = 0            # 拉丁字母
    total_alpha = 0      # 所有字母字符

    for ch in text:
        code = ord(ch)
        if 0x4E00 <= code <= 0x9FFF:       # CJK 统一表意文字
            cjk_unified += 1
            total_alpha += 1
        elif 0x3040 <= code <= 0x309F:     # 平假名
            hiragana += 1
            total_alpha += 1
        elif 0x30A0 <= code <= 0x30FF:     # 片假名
            katakana += 1
            total_alpha += 1
        elif 0xAC00 <= code <= 0xD7AF:     # 韩文音节
            hangul += 1
            total_alpha += 1
        elif (0x41 <= code <= 0x5A) or (0x61 <= code <= 0x7A):  # A-Z a-z
            latin += 1
            total_alpha += 1

    if total_alpha == 0:
        return "unknown"

    # 判断逻辑
    japanese_chars = hiragana + katakana
    if japanese_chars > 0 and japanese_chars / total_alpha > 0.1:
        return "ja"
    if hangul > 0 and hangul / total_alpha > 0.2:
        return "ko"
    if cjk_unified > 0:
        # CJK 占比高且无日文假名 → 中文
        if cjk_unified / total_alpha > 0.3:
            return "zh"
    if latin / total_alpha > 0.5:
        return "en"
    if cjk_unified > 0:
        return "zh"  # 有中文字符但占比不高，默认中文
    return "unknown"


def detect_transcript_language(transcript: dict) -> str:
    """v4.0: 检测 transcript 的语言。

    优先用 transcript.language 字段，fallback 到采样 segments 文本。
    """
    # 1. 优先用字段
    lang = transcript.get("language", "")
    if lang and lang != "unknown":
        return lang

    # 2. 采样前 10 个 segment 的文本
    segments = transcript.get("segments", [])
    sample_text = " ".join(seg.get("text", "") for seg in segments[:10])
    return detect_language(sample_text)


def needs_translation(transcript: dict, target_language: str = "zh-CN") -> bool:
    """v4.0: 判断 transcript 是否需要翻译。

    中文内容不需要翻译（target_language=zh-CN 时）。
    """
    source_lang = detect_transcript_language(transcript)
    # target_language "zh-CN" 的主语言是 "zh"
    target_main = target_language.split("-")[0].lower()
    return source_lang != target_main and source_lang != "unknown"


# ===== SRT 解析与生成 =====

def parse_srt_time(time_str: str) -> float:
    """v4.0: SRT 时间码 'HH:MM:SS,mmm' → 秒数。"""
    # 兼容 "HH:MM:SS,mmm" 和 "HH:MM:SS.mmm"
    time_str = time_str.strip().replace(",", ".")
    parts = time_str.split(":")
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    else:
        return float(time_str)


def format_srt_time(seconds: float) -> str:
    """v4.0: 秒数 → SRT 时间码 'HH:MM:SS,mmm'。"""
    total_ms = int(round(seconds * 1000))
    h = total_ms // 3600000
    m = (total_ms % 3600000) // 60000
    s = (total_ms % 60000) // 1000
    ms = total_ms % 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def parse_srt(srt_content: str) -> list[dict]:
    """v4.0: 解析 SRT 字幕内容为 segments 列表。

    返回 [{"start": float, "end": float, "text": str}, ...]

    支持标准 SRT 格式：
        1
        00:00:01,000 --> 00:00:04,000
        Hello world

    约束（与 subtitle_pipeline.prepare 兼容）：
    - UTF-8 编码
    - 标准时间码
    - start 单调递增
    - text 非空
    """
    segments = []
    # 按空行分割块
    blocks = re.split(r"\n\s*\n", srt_content.strip())

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue

        # 第 1 行：序号（可跳过）
        # 第 2 行：时间码
        # 第 3+ 行：文本
        time_line_idx = 0
        for i, line in enumerate(lines):
            if "-->" in line:
                time_line_idx = i
                break
        else:
            continue

        time_line = lines[time_line_idx]
        time_match = re.match(
            r"(\d{2}:\d{2}:\d{2}[,.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,.]\d{3})",
            time_line,
        )
        if not time_match:
            continue

        start = parse_srt_time(time_match.group(1))
        end = parse_srt_time(time_match.group(2))

        # 文本（时间码行之后的所有行）
        text_lines = lines[time_line_idx + 1:]
        text = "\n".join(text_lines).strip()
        if not text:
            continue

        # 去除 HTML 标签（如 <i>...</i>）
        text = re.sub(r"<[^>]+>", "", text)

        segments.append({
            "start": round(start, 3),
            "end": round(end, 3),
            "text": text,
        })

    return segments
