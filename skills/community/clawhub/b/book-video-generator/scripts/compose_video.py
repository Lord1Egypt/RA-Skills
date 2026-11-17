#!/usr/bin/env python3
"""
三分钟精读书 视频合成脚本
将图片+音频合成为带字幕的 MP4 视频，替代扣子工作流中的剪映小助手。

v2.6.0 改进：
- 进度条：顶部显示板块标题，当前板块高亮（橙色 #FF7F72），底部进度线
- 关键词高亮：ASS 字幕格式，关键词用橙色高亮显示
- 逐句单行字幕：利用 TTS 词级时间戳精确同步语音

v2.3.0 改进：
- 逐句单行字幕：利用 edge-tts WordBoundary 词级时间戳，将长字幕拆分为单行短句
- 精确语音同步：每条字幕的开始/结束时间与语音精确对应
- 字体增大至 36pt，仅显示一行，不再遮挡画面

依赖：
- imageio-ffmpeg（自动提供 ffmpeg 二进制）
- Pillow（进度条 PNG 生成）

使用方法：
  python compose_video.py < segments.json

segments.json 格式：
{
  "output": "output.mp4",
  "cover": "cover.png",                          // 可选，封面图（第一分镜前5秒显示）
  "cover_duration": 5.0,                         // 可选，封面显示时长（秒，默认5）
  "chapter_titles": ["开篇引言", "核心方法", "实践技巧", "总结"],  // 可选，进度条标题
  "segment_chapters": [0, 0, 0, 1, 1, ...],      // 可选，每个分镜所属板块索引
  "keywords": ["原子习惯", "微小改变"],            // 可选，字幕高亮关键词
  "segments": [
    {"image": "1.png", "audio": "1.mp3", "caption": "字幕文本"},
    ...
  ]
}
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile


try:
    import imageio_ffmpeg
    FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG = "ffmpeg"


# ── 字体检测 ──────────────────────────────────────────────

def detect_font():
    """自动检测系统可用的中文字体，返回 ffmpeg subtitles 滤镜可用的 FontName"""
    import platform

    system = platform.system().lower()
    candidates = []

    if system == "windows":
        candidates = [
            ("C:/Windows/Fonts/msyh.ttc", "Microsoft YaHei"),
            ("C:/Windows/Fonts/msyhbd.ttc", "Microsoft YaHei"),
            ("C:/Windows/Fonts/simhei.ttf", "SimHei"),
            ("C:/Windows/Fonts/simsun.ttc", "SimSun"),
        ]
    elif system == "darwin":
        candidates = [
            ("/System/Library/Fonts/PingFang.ttc", "PingFang SC"),
            ("/System/Library/Fonts/STHeiti Medium.ttc", "STHeiti"),
            ("/Library/Fonts/Arial Unicode.ttf", "Arial Unicode MS"),
        ]
    else:
        candidates = [
            ("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc", "Noto Sans CJK SC"),
            ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", "Noto Sans CJK SC"),
            ("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", "WenQuanYi Zen Hei"),
            ("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", "WenQuanYi Micro Hei"),
        ]

    for path, name in candidates:
        if os.path.exists(path):
            return name

    try:
        result = subprocess.run(
            ["fc-list", ":lang=zh", "family"],
            capture_output=True, text=True, timeout=5,
        )
        if result.stdout.strip():
            return result.stdout.strip().split("\n")[0].split(",")[0].strip()
    except (FileNotFoundError, subprocess.SubprocessError, subprocess.TimeoutExpired):
        pass

    return "Sans"


def detect_font_path():
    """自动检测系统可用的中文字体文件路径，供 Pillow 使用"""
    import platform

    system = platform.system().lower()
    candidates = []

    if system == "windows":
        candidates = [
            "C:/Windows/Fonts/msyhbd.ttc",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/simsun.ttc",
        ]
    elif system == "darwin":
        candidates = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        ]

    for path in candidates:
        if os.path.exists(path):
            return path

    return None


def _find_asset(filename):
    """查找技能自带的素材文件（BGM、音效等）

    按以下顺序查找：
    1. 脚本同级 assets/ 目录
    2. 脚本父级 assets/ 目录（技能根目录下的 assets/）
    3. 脚本同级目录
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, "assets", filename),
        os.path.join(script_dir, "..", "assets", filename),
        os.path.join(script_dir, filename),
    ]
    for path in candidates:
        if os.path.exists(path):
            return os.path.normpath(path)
    return None


# ── 工具函数 ──────────────────────────────────────────────

def get_duration(audio_path: str) -> float:
    """使用 ffmpeg 获取音频时长"""
    cmd = [FFMPEG, "-i", audio_path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", r.stderr)
    if m:
        h, m_, s = m.groups()
        return int(h) * 3600 + int(m_) * 60 + float(s)
    raise RuntimeError(f"无法获取音频时长: {audio_path}")


def _fmt_srt_time(t: float) -> str:
    """将秒数格式化为 SRT 时间戳 HH:MM:SS,mmm"""
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def _fmt_ass_time(t: float) -> str:
    """将秒数格式化为 ASS 时间戳 H:MM:SS.cc（百分秒）"""
    total_cs = int(round(t * 100))
    h = total_cs // 360000
    m = (total_cs % 360000) // 6000
    s = (total_cs % 6000) // 100
    cs = total_cs % 100
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


# ── 字幕断句 ──────────────────────────────────────────────

# 断句标点：遇到这些字符时断句（保留标点到当前短语末尾）
_BREAK_PUNCT = set("，。！？；：、…")
# 所有标点（用于匹配时跳过，不消耗词字符）
_ALL_PUNCT = _BREAK_PUNCT | set("「」""''《》【】（）()[] \n\t\r'·～‥—–-")


def build_phrases(caption, words, max_chars=18):
    """从原始字幕文本和词级时间戳构建带标点的单行短语

    逐字符遍历原始字幕，将每个字符与词序列匹配以获取精确时间戳。
    断句策略：
    1. 遇到断句标点（，。！？等）时断句，标点保留在当前短语末尾
    2. 超过 max_chars 时标记超限，在下一个标点处断句
    3. 超过 1.5 倍 max_chars 仍无标点时强制断句

    Args:
        caption: 原始字幕文本（含标点）
        words: [{"text": "词", "start": 0.0, "end": 0.5}, ...]
        max_chars: 每行最大字符数

    Returns:
        [(phrase_text, start_time, end_time), ...]
    """
    if not words or not caption:
        return [(caption, 0.0, 0.0)] if caption else []

    phrases = []
    buf = ""
    buf_start = words[0]["start"]
    buf_end = words[0]["end"]
    wi = 0
    ci = 0
    over_max = False

    for ch in caption:
        if ch in _ALL_PUNCT:
            buf += ch
            if ch in _BREAK_PUNCT and buf.strip():
                phrases.append((buf.strip(), buf_start, buf_end))
                buf = ""
                over_max = False
                if wi < len(words):
                    buf_start = words[wi]["start"]
                ci = 0
        else:
            matched = False
            while wi < len(words) and not matched:
                w = words[wi]
                if ci < len(w["text"]) and w["text"][ci] == ch:
                    buf += ch
                    buf_end = w["end"]
                    ci += 1
                    if ci >= len(w["text"]):
                        wi += 1
                        ci = 0
                    matched = True
                elif ci == 0 and ch in w["text"]:
                    pos = w["text"].find(ch)
                    ci = pos + 1
                    buf += ch
                    buf_end = w["end"]
                    if ci >= len(w["text"]):
                        wi += 1
                        ci = 0
                    matched = True
                else:
                    wi += 1
                    ci = 0

            if not matched:
                buf += ch

            if ci == 0 and wi > 0:
                if not over_max and len(buf) >= max_chars:
                    over_max = True
                if over_max and len(buf) >= int(max_chars * 1.5):
                    phrases.append((buf.strip(), buf_start, buf_end))
                    buf = ""
                    over_max = False
                    if wi < len(words):
                        buf_start = words[wi]["start"]

    if buf.strip():
        phrases.append((buf.strip(), buf_start, buf_end))

    return phrases


# ── 关键词高亮 ────────────────────────────────────────────

# ASS 颜色（BGR 格式）：#FF7F72 → B=72, G=7F, R=FF
HIGHLIGHT_COLOR = "&H727FFF&"  # 橙色 #FF7F72
DEFAULT_COLOR = "&HFFFFFF&"    # 白色


def highlight_keywords(text, keywords):
    """在文本中高亮关键词，使用 ASS 颜色标签

    按关键词长度降序匹配，避免短词匹配到长词的子串。
    使用正则表达式一次性替换所有非重叠匹配。

    Args:
        text: 原始文本
        keywords: 关键词列表

    Returns:
        带 ASS 颜色标签的文本，如 {\\c&H727FFF&}原子习惯{\\c&HFFFFFF&}的力量
    """
    if not keywords:
        return text

    # 筛选实际出现在文本中的关键词，按长度降序
    active_kw = sorted(set(kw for kw in keywords if kw and kw in text),
                       key=len, reverse=True)
    if not active_kw:
        return text

    # 构建正则表达式（长词优先，避免部分匹配）
    pattern = "|".join(re.escape(kw) for kw in active_kw)

    def replacer(m):
        return f"{{\\c{HIGHLIGHT_COLOR}}}{m.group()}{{\\c{DEFAULT_COLOR}}}"

    return re.sub(pattern, replacer, text)


# ── ASS 字幕生成 ──────────────────────────────────────────

def make_ass(segments, durations, output_path, gap=0.0, max_chars=16,
             keywords=None, fade_in_ms=200, fade_out_ms=150):
    """生成 ASS 字幕文件，支持关键词高亮 + 入场/出场动画

    优先使用词级时间戳（.words.json）实现精确语音同步，
    将长字幕拆分为单行短句，每句不超过 max_chars 个字符。
    关键词用橙色高亮显示。
    每条字幕带淡入+上滑入场、淡出出场动画。

    Args:
        segments: 分镜列表
        durations: 每个分镜的时长列表
        output_path: ASS 文件输出路径
        gap: 分镜间隔（秒）
        max_chars: 每行最大字符数
        keywords: 高亮关键词列表（可选）
        fade_in_ms: 入场淡入时长（毫秒）
        fade_out_ms: 出场淡出时长（毫秒）

    Returns: output_path
    """
    font_name = detect_font()

    header = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        "PlayResX: 1920\n"
        "PlayResY: 1080\n"
        "WrapStyle: 2\n"
        "ScaledBorderAndShadow: yes\n"
        "\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Default,{font_name},64,&H00FFFFFF,&H000000FF,&H00000000,"
        f"&H80000000,1,0,0,0,100,100,0,0,1,2,1,2,30,30,30,1\n"
        "\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, "
        "MarginV, Effect, Text\n"
    )

    # 动画标签：淡入淡出 + 从下方滑入
    # \fad(in,out) 控制淡入淡出
    # \move(x1,y1,x2,y2,t1,t2) 从下方 20px 滑入正常位置
    fade_tag = f"\\fad({fade_in_ms},{fade_out_ms})"
    # 正常位置 y=1050 (PlayResY - MarginV = 1080-30)，起始位置 y=1070
    move_tag = f"\\move(960,1070,960,1050,0,{fade_in_ms})"

    lines = [header]
    seg_start = 0.0
    idx = 1

    for seg, dur in zip(segments, durations):
        caption = seg.get("caption", "")
        audio_path = seg.get("audio", "")
        words_path = ""
        if audio_path:
            words_path = audio_path.rsplit(".", 1)[0] + ".words.json"

        seg_end = seg_start + dur

        # 跳过空字幕（如封面片头）
        if not caption.strip():
            seg_start = seg_end + gap
            continue

        if words_path and os.path.exists(words_path):
            with open(words_path, "r", encoding="utf-8") as f:
                words = json.load(f)

            phrases = build_phrases(caption, words, max_chars=max_chars)

            for phrase_text, p_start, p_end in phrases:
                abs_start = seg_start + p_start
                abs_end = seg_start + min(p_end, dur)

                if abs_end <= abs_start:
                    abs_end = abs_start + 0.5

                highlighted = highlight_keywords(phrase_text, keywords)
                # 在文本前添加动画标签
                if highlighted.startswith("{"):
                    text_with_anim = "{" + fade_tag + move_tag + highlighted[1:]
                else:
                    text_with_anim = "{" + fade_tag + move_tag + "}" + highlighted

                lines.append(
                    f"Dialogue: 0,{_fmt_ass_time(abs_start)},"
                    f"{_fmt_ass_time(abs_end)},Default,,0,0,0,,{text_with_anim}"
                )
                idx += 1
        else:
            highlighted = highlight_keywords(caption, keywords)
            if highlighted.startswith("{"):
                text_with_anim = "{" + fade_tag + move_tag + highlighted[1:]
            else:
                text_with_anim = "{" + fade_tag + move_tag + "}" + highlighted
            lines.append(
                f"Dialogue: 0,{_fmt_ass_time(seg_start)},"
                f"{_fmt_ass_time(seg_end)},Default,,0,0,0,,{text_with_anim}"
            )
            idx += 1

        seg_start = seg_end + gap

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    total_entries = idx - 1
    kw_count = len(keywords) if keywords else 0
    kw_msg = f"，关键词高亮 {kw_count} 个" if kw_count else ""
    print(f"ASS字幕生成完成：共 {total_entries} 条逐句字幕{kw_msg}"
          f"，入场淡入{fade_in_ms}ms/出场淡出{fade_out_ms}ms")
    return output_path


def make_srt(segments, durations, output_path, gap=0.0, max_chars=16):
    """生成 SRT 字幕文件（兼容旧版，推荐使用 make_ass）"""
    lines = []
    seg_start = 0.0
    idx = 1

    for seg, dur in zip(segments, durations):
        caption = seg.get("caption", "")
        audio_path = seg.get("audio", "")
        words_path = ""
        if audio_path:
            words_path = audio_path.rsplit(".", 1)[0] + ".words.json"

        seg_end = seg_start + dur

        if words_path and os.path.exists(words_path):
            with open(words_path, "r", encoding="utf-8") as f:
                words = json.load(f)

            phrases = build_phrases(caption, words, max_chars=max_chars)

            for phrase_text, p_start, p_end in phrases:
                abs_start = seg_start + p_start
                abs_end = seg_start + min(p_end, dur)

                if abs_end <= abs_start:
                    abs_end = abs_start + 0.5

                lines.append(str(idx))
                lines.append(f"{_fmt_srt_time(abs_start)} --> {_fmt_srt_time(abs_end)}")
                lines.append(phrase_text)
                lines.append("")
                idx += 1
        else:
            lines.append(str(idx))
            lines.append(f"{_fmt_srt_time(seg_start)} --> {_fmt_srt_time(seg_end)}")
            lines.append(caption)
            lines.append("")
            idx += 1

        seg_start = seg_end + gap

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    total_entries = idx - 1
    print(f"字幕生成完成：共 {total_entries} 条逐句字幕")
    return output_path


# ── 进度条生成 ────────────────────────────────────────────

PROGRESS_BAR_HEIGHT = 80
ACCENT_RGB = (255, 127, 114)    # #FF7F72 与分镜主角上衣同色
INACTIVE_RGB = (170, 170, 170)  # #AAAAAA


def generate_progress_bar(titles, current_chapter, progress, output_path,
                          width=1920, height=PROGRESS_BAR_HEIGHT):
    """生成进度条 PNG overlay

    顶部半透明深色背景上显示板块标题，当前板块用橙色高亮+实心圆点，
    其余板块灰色+空心圆点。底部有进度线显示总体播放进度。

    Args:
        titles: 板块标题列表（如 ["开篇引言", "核心方法", "实践技巧", "总结"]）
        current_chapter: 当前板块索引（高亮显示）
        progress: 总体进度 0.0~1.0（用于进度线填充比例）
        output_path: PNG 输出路径
        width: 视频宽度
        height: 进度条高度
    """
    from PIL import Image, ImageDraw, ImageFont

    # 半透明深色背景
    img = Image.new("RGBA", (width, height), (0, 0, 0, 130))
    draw = ImageDraw.Draw(img)

    font_path = detect_font_path()
    font_size = 44 if width >= 1920 else 30
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    n = len(titles)
    section_width = width // n

    for i, title in enumerate(titles):
        is_current = (i == current_chapter)
        text_color = ACCENT_RGB + (255,) if is_current else INACTIVE_RGB + (255,)

        # 指示符圆点
        dot_x = section_width * i + 36
        dot_y = height // 2 - 5
        dot_r = 7
        if is_current:
            draw.ellipse(
                [dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r],
                fill=ACCENT_RGB + (255,),
            )
        else:
            draw.ellipse(
                [dot_x - dot_r, dot_y - dot_r, dot_x + dot_r, dot_y + dot_r],
                outline=INACTIVE_RGB + (180,), width=1,
            )

        # 标题文字
        bbox = draw.textbbox((0, 0), title, font=font)
        text_w = bbox[2] - bbox[0]
        text_x = dot_x + dot_r + 14
        text_y = (height - (bbox[3] - bbox[1])) // 2 - 3
        draw.text((text_x, text_y), title, font=font, fill=text_color)

    # 底部进度线
    line_y = height - 3
    draw.line([(0, line_y), (width, line_y)], fill=(60, 60, 60, 200), width=2)
    fill_w = int(width * max(0.0, min(1.0, progress)))
    if fill_w > 0:
        draw.line([(0, line_y), (fill_w, line_y)],
                  fill=ACCENT_RGB + (255,), width=2)

    img.save(output_path, "PNG")
    return output_path


# ── 音频混音（BGM + 转场音效）──────────────────────────────

def mix_audio(video_path, output_path, bgm_path=None, bgm_volume=0.15,
              transition_sound=None, transition_points=None,
              transition_volume=0.3):
    """将背景音乐和转场音效混入视频音频

    BGM 全程循环播放，以低音量混合。
    转场音效在指定时间点叠加播放。

    Args:
        video_path: 输入视频路径（已有 TTS 音频 + 字幕）
        output_path: 输出视频路径
        bgm_path: BGM 文件路径（可选）
        bgm_volume: BGM 音量 (0.0-1.0)
        transition_sound: 转场音效文件路径（可选）
        transition_points: 转场音效时间点列表（秒）（可选）
        transition_volume: 转场音效音量 (0.0-1.0)

    如果没有 BGM 和转场音效，直接复制文件。
    """
    has_bgm = bgm_path and os.path.exists(bgm_path)
    has_ts = (transition_sound and os.path.exists(transition_sound)
              and transition_points)

    if not has_bgm and not has_ts:
        shutil.copy(video_path, output_path)
        return

    inputs = [FFMPEG, "-y", "-i", video_path]
    input_idx = 1  # 下一个输入索引

    filter_parts = []
    # 将主音频（TTS）统一转换为立体声，避免 BGM 被降级为单声道
    filter_parts.append("[0:a]aformat=channel_layouts=stereo[tts]")
    mix_inputs = ["[tts]"]

    # BGM 输入（循环播放）
    if has_bgm:
        inputs.extend(["-stream_loop", "-1", "-i", bgm_path])
        filter_parts.append(
            f"[{input_idx}:a]volume={bgm_volume}[bgm]"
        )
        mix_inputs.append("[bgm]")
        input_idx += 1

    # 转场音效输入（每个时间点一个输入）
    if has_ts:
        for ts in transition_points:
            inputs.extend(["-i", transition_sound])
            delay_ms = int(max(0, ts) * 1000)
            filter_parts.append(
                f"[{input_idx}:a]adelay={delay_ms}|{delay_ms},"
                f"volume={transition_volume}[t{input_idx}]"
            )
            mix_inputs.append(f"[t{input_idx}]")
            input_idx += 1

    n_mix = len(mix_inputs)
    filter_complex = ";".join(filter_parts)
    filter_complex += (f";{''.join(mix_inputs)}"
                       f"amix=inputs={n_mix}:duration=first:normalize=0[a]")

    inputs.extend([
        "-filter_complex", filter_complex,
        "-map", "0:v", "-map", "[a]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        output_path,
    ])

    subprocess.run(inputs, capture_output=True, check=True)

    parts = []
    if has_bgm:
        parts.append(f"BGM(音量{bgm_volume})")
    if has_ts:
        parts.append(f"转场音效×{len(transition_points)}(音量{transition_volume})")
    print(f"音频混音完成：{' + '.join(parts)}")


# ── 视频合成 ──────────────────────────────────────────────

def compose_video(
    segments,
    output_path=None,
    output=None,
    cover=None,
    chapter_titles=None,
    segment_chapters=None,
    keywords=None,
    bgm=None,
    bgm_volume=0.15,
    transition_sound=None,
    transition_interval=3,
    transition_volume=0.3,
    video_width=1920,
    video_height=1080,
    fps=24,
    gap=0.0,
    max_chars=16,
    cover_duration=5.0,
):
    """合成视频

    Args:
        segments: 分镜列表 [{"image":..., "audio":..., "caption":...}, ...]
        output_path / output: 输出 MP4 路径
        cover: 封面图路径（可选，用于第一分镜前N秒，旁白不中断）
        chapter_titles: 板块标题列表（可选，用于进度条）
        segment_chapters: 每个分镜所属板块索引列表（可选，无则均匀分配）
        keywords: 字幕高亮关键词列表（可选）
        bgm: 背景音乐路径（可选，自动查找 assets/bgm_reading.mp3）
        bgm_volume: BGM 音量 (0.0-1.0)
        transition_sound: 转场音效路径（可选，自动查找 assets/transition_page_flip.mp3）
        transition_interval: 每 N 个分镜添加一次转场音效
        transition_volume: 转场音效音量 (0.0-1.0)
        video_width / video_height: 视频分辨率
        fps: 帧率
        gap: 分镜间隔（秒）
        max_chars: 字幕每行最大字符数
        cover_duration: 封面显示时长（秒，默认5秒，仅作用于第一分镜前半段）
    """
    if output_path is None and output:
        output_path = output
    if not output_path:
        raise ValueError("必须提供 output_path 或 output")

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    tmpdir = tempfile.mkdtemp(prefix="book_video_")

    # 自动查找默认 BGM 和转场音效
    if bgm is None:
        bgm = _find_asset("bgm_reading.mp3")
    if transition_sound is None:
        transition_sound = _find_asset("transition_page_flip.mp3")

    # 封面图用于第一分镜前 cover_duration 秒（旁白不中断，之后切回原图）
    cover_for_first = None
    if cover and os.path.exists(cover) and len(segments) > 0:
        cover_for_first = cover
        print(f"封面图将用于第一分镜前 {cover_duration} 秒：{cover}")

    # 预计算所有分镜时长
    print("预计算音频时长...")
    durations = []
    for i, seg in enumerate(segments):
        img = seg["image"]
        aud = seg["audio"]
        if not os.path.exists(img):
            print(f"警告：图片不存在 {img}")
            durations.append(0)
            continue
        if not os.path.exists(aud):
            print(f"警告：音频不存在 {aud}")
            durations.append(0)
            continue
        durations.append(get_duration(aud))

    valid_count = sum(1 for d in durations if d > 0)
    total_duration = sum(d for d in durations if d > 0) + gap * max(0, valid_count - 1)

    # 生成进度条 PNG（如果提供了 chapter_titles 且 Pillow 可用）
    progress_bars = {}
    use_progress_bar = False

    if chapter_titles and len(chapter_titles) > 0:
        try:
            from PIL import Image  # noqa: F401
        except ImportError:
            print("警告：Pillow 未安装，跳过进度条生成")
            chapter_titles = None

    if chapter_titles and len(chapter_titles) > 0:
        use_progress_bar = True
        n_chapters = len(chapter_titles)
        print(f"生成进度条（{n_chapters} 个板块）...")

        # 如果没有提供 segment_chapters，均匀分配
        if not segment_chapters or len(segment_chapters) != len(segments):
            n_segs = len(segments)
            segment_chapters = []
            for i in range(n_segs):
                segment_chapters.append(
                    min(n_chapters - 1, i * n_chapters // n_segs)
                )

        # 为每个分镜生成进度条 PNG（按 10% 进度区间分组以减少文件数）
        elapsed = 0.0
        for i, seg in enumerate(segments):
            if durations[i] <= 0:
                continue

            chapter_idx = segment_chapters[i] if i < len(segment_chapters) else 0
            progress = elapsed / total_duration if total_duration > 0 else 0

            progress_key = (chapter_idx, int(progress * 10))
            if progress_key not in progress_bars:
                png_path = os.path.join(
                    tmpdir,
                    f"progress_{chapter_idx}_{int(progress * 10)}.png",
                )
                generate_progress_bar(
                    chapter_titles, chapter_idx, progress, png_path,
                    width=video_width,
                )
                progress_bars[progress_key] = png_path

            elapsed += durations[i] + gap

    # 逐分镜生成视频片段
    clip_files = []
    elapsed = 0.0

    for i, seg in enumerate(segments):
        dur = durations[i]
        if dur <= 0:
            continue

        img = seg["image"]
        aud = seg["audio"]

        total_frames = max(1, int(dur * fps))
        fade_dur = min(0.3, dur / 2)

        # 封面图用于第一分镜前 cover_duration 秒（旁白不中断）
        if i == 0 and cover_for_first:
            split_t = min(cover_duration, dur)
            remaining_t = dur - split_t

            # 确定进度条 PNG（两个子片段共用）
            progress_png = None
            if use_progress_bar:
                chapter_idx = segment_chapters[0] if segment_chapters else 0
                progress = elapsed / total_duration if total_duration > 0 else 0
                progress_key = (chapter_idx, int(progress * 10))
                progress_png = progress_bars.get(progress_key)

            # Clip A: 封面图 + 前 split_t 秒音频
            vf_a = (
                f"scale={video_width}:{video_height}:force_original_aspect_ratio=decrease,"
                f"pad={video_width}:{video_height}:(ow-iw)/2:(oh-ih)/2:black,"
                f"fade=t=in:st=0:d={fade_dur},"
                f"fade=t=out:st={max(0, split_t - fade_dur)}:d={fade_dur}"
            )
            clip_a = os.path.join(tmpdir, f"clip_{i:03d}a.mp4")
            if progress_png and os.path.exists(progress_png):
                cmd_a = [
                    FFMPEG, "-y", "-loop", "1", "-i", cover_for_first, "-i", aud,
                    "-i", progress_png,
                    "-filter_complex",
                    f"[0:v]{vf_a}[bg];[bg][2:v]overlay=0:0[v]",
                    "-map", "[v]", "-map", "1:a",
                    "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
                    "-pix_fmt", "yuv420p",
                    "-r", str(fps), "-t", str(split_t), "-shortest",
                    clip_a,
                ]
            else:
                cmd_a = [
                    FFMPEG, "-y", "-loop", "1", "-i", cover_for_first, "-i", aud,
                    "-c:v", "libx264",
                    "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
                    "-r", str(fps), "-t", str(split_t), "-vf", vf_a, "-shortest",
                    clip_a,
                ]
            subprocess.run(cmd_a, capture_output=True, check=True)
            clip_files.append(clip_a)

            # Clip B: 原始图 + 剩余音频（从 split_t 开始）
            if remaining_t > 0.1:
                vf_b = (
                    f"scale={video_width}:{video_height}:force_original_aspect_ratio=decrease,"
                    f"pad={video_width}:{video_height}:(ow-iw)/2:(oh-ih)/2:black,"
                    f"fade=t=in:st=0:d={fade_dur},"
                    f"fade=t=out:st={max(0, remaining_t - fade_dur)}:d={fade_dur}"
                )
                clip_b = os.path.join(tmpdir, f"clip_{i:03d}b.mp4")
                if progress_png and os.path.exists(progress_png):
                    cmd_b = [
                        FFMPEG, "-y", "-loop", "1", "-i", img,
                        "-ss", str(split_t), "-i", aud,
                        "-i", progress_png,
                        "-filter_complex",
                        f"[0:v]{vf_b}[bg];[bg][2:v]overlay=0:0[v]",
                        "-map", "[v]", "-map", "1:a",
                        "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
                        "-pix_fmt", "yuv420p",
                        "-r", str(fps), "-t", str(remaining_t), "-shortest",
                        clip_b,
                    ]
                else:
                    cmd_b = [
                        FFMPEG, "-y", "-loop", "1", "-i", img,
                        "-ss", str(split_t), "-i", aud,
                        "-c:v", "libx264",
                        "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
                        "-r", str(fps), "-t", str(remaining_t), "-vf", vf_b,
                        "-shortest",
                        clip_b,
                    ]
                subprocess.run(cmd_b, capture_output=True, check=True)
                clip_files.append(clip_b)

            elapsed += dur + gap
            print(f"[{i+1}/{len(segments)}] clip {dur:.2f}s"
                  f" (封面{split_t:.1f}s + 画面{remaining_t:.1f}s)"
                  f"{' +进度条' if progress_png else ''}")
            continue

        # 无缩放：仅缩放到目标尺寸 + 黑边填充 + 淡入淡出
        vf = (
            f"scale={video_width}:{video_height}:force_original_aspect_ratio=decrease,"
            f"pad={video_width}:{video_height}:(ow-iw)/2:(oh-ih)/2:black,"
            f"fade=t=in:st=0:d={fade_dur},"
            f"fade=t=out:st={max(0, dur - fade_dur)}:d={fade_dur}"
        )

        clip_out = os.path.join(tmpdir, f"clip_{i:03d}.mp4")

        # 确定进度条 PNG
        progress_png = None
        if use_progress_bar:
            chapter_idx = segment_chapters[i] if i < len(segment_chapters) else 0
            progress = elapsed / total_duration if total_duration > 0 else 0
            progress_key = (chapter_idx, int(progress * 10))
            progress_png = progress_bars.get(progress_key)

        if progress_png and os.path.exists(progress_png):
            # 带进度条 overlay 的命令
            cmd = [
                FFMPEG, "-y", "-loop", "1", "-i", img, "-i", aud,
                "-i", progress_png,
                "-filter_complex",
                f"[0:v]{vf}[bg];[bg][2:v]overlay=0:0[v]",
                "-map", "[v]", "-map", "1:a",
                "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k",
                "-pix_fmt", "yuv420p",
                "-r", str(fps), "-t", str(dur), "-shortest",
                clip_out,
            ]
        else:
            # 原始命令（无进度条）
            cmd = [
                FFMPEG, "-y", "-loop", "1", "-i", img, "-i", aud,
                "-c:v", "libx264",
                "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
                "-r", str(fps), "-t", str(dur), "-vf", vf, "-shortest",
                clip_out,
            ]

        subprocess.run(cmd, capture_output=True, check=True)
        clip_files.append(clip_out)
        elapsed += dur + gap
        print(f"[{i+1}/{len(segments)}] clip {dur:.2f}s"
              f"{' +进度条' if progress_png else ''}")

    # 1. 拼接无字幕视频
    concat_list = os.path.join(tmpdir, "clips.txt")
    with open(concat_list, "w") as f:
        for cf in clip_files:
            f.write(f"file '{cf}'\n")

    no_subs = os.path.join(tmpdir, "no_subs.mp4")
    subprocess.run(
        [FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
         "-c", "copy", no_subs],
        capture_output=True, check=True,
    )

    # 2. 生成 ASS 字幕（含关键词高亮）
    ass_path = os.path.join(tmpdir, "subtitles.ass")
    make_ass(segments, durations, ass_path, gap=gap, max_chars=max_chars,
             keywords=keywords)

    # 3. 烧录字幕 + 混音
    # Windows 下路径使用正斜杠 + 冒号转义
    ass_escaped = ass_path.replace("\\", "/").replace(":", "\\:")
    font_name = detect_font()
    print(f"字幕字体：{font_name}")
    style = (
        f"FontName={font_name},FontSize=64,Bold=1,"
        f"PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
        f"Outline=2,Shadow=1,ShadowColour=&H80000000,"
        f"Alignment=2,MarginV=30"
    )

    has_bgm = bgm and os.path.exists(bgm)
    has_trans = transition_sound and os.path.exists(transition_sound)
    need_mix = has_bgm or has_trans
    transition_points = []

    if need_mix:
        # 先烧录字幕到临时文件，再混音
        subs_output = os.path.join(tmpdir, "with_subs.mp4")
        subprocess.run(
            [FFMPEG, "-y", "-i", no_subs, "-vf",
             f"subtitles='{ass_escaped}':force_style='{style}'",
             "-c:a", "copy", subs_output],
            capture_output=True, check=True,
        )
        print("字幕烧录完成")

        # 4. 计算转场音效时间点
        transition_points = []
        if has_trans:
            elapsed_ts = 0.0
            for i, dur_t in enumerate(durations):
                if dur_t > 0:
                    seg_end_ts = elapsed_ts + dur_t
                    # 每 N 个分镜在结尾前 0.5s 添加转场音效（跳过最后一个分镜）
                    if i % transition_interval == 0 and i < len(durations) - 1:
                        ts = seg_end_ts - 0.5
                        if ts > 0:
                            transition_points.append(max(0, ts))
                    elapsed_ts += dur_t + gap

        # 5. 混音（BGM + 转场音效）
        mix_audio(
            subs_output, output_path,
            bgm_path=bgm if has_bgm else None,
            bgm_volume=bgm_volume,
            transition_sound=transition_sound if transition_points else None,
            transition_points=transition_points if transition_points else None,
            transition_volume=transition_volume,
        )
    else:
        # 无混音，直接烧录字幕到最终输出
        subprocess.run(
            [FFMPEG, "-y", "-i", no_subs, "-vf",
             f"subtitles='{ass_escaped}':force_style='{style}'",
             "-c:a", "copy", output_path],
            capture_output=True, check=True,
        )

    shutil.rmtree(tmpdir, ignore_errors=True)

    total = sum(d for d in durations if d > 0) + gap * max(0, valid_count - 1)
    features = []
    if use_progress_bar:
        features.append("进度条")
    if keywords:
        features.append(f"关键词高亮({len(keywords)}个)")
    if has_bgm:
        features.append(f"BGM(音量{bgm_volume})")
    if has_trans and transition_points:
        features.append(f"转场音效×{len(transition_points)}")
    features.append("字幕动画")
    feature_msg = f" | {' + '.join(features)}" if features else ""
    print(f"\n视频合成完成：{output_path}")
    print(f"总时长：{total:.1f}秒 | 分镜数：{len(clip_files)}{feature_msg}")


if __name__ == "__main__":
    data = json.loads(sys.stdin.read())
    compose_video(**data)
