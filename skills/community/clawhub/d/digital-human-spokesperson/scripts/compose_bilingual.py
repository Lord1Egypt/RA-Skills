#!/usr/bin/env python3
"""Compose the bilingual single talking-head video.

Takes the English and Arabic talking-head clips plus their text, then:
  1. Builds proportional .srt subtitles from each text file (timing by audio duration).
  2. Burns subtitles into each clip.
  3. Adds a labeled title card (English / العربية) before each segment.
  4. Applies China's mandatory AI-content labels (《人工智能生成合成内容标识办法》):
     - Explicit (显式): a persistent "AI 生成" corner watermark on every segment
       plus a bilingual end notice card ("本视频由 AI 生成" / "AI-Generated Content").
     - Implicit (隐式): MP4 metadata (comment / description) marking the file as
       AI-generated synthetic content.
  5. Concatenates everything into one MP4.

Labels are ON by default. Use --no-ai-label to disable (not recommended — the
regulation is mandatory for publicly distributed synthetic content, and the labels
double as qualification evidence when submitting to the WorkBuddy open platform).

Requires ffmpeg + ffprobe on PATH (or pass --ffmpeg). For best Arabic glyph
rendering, pass --fontfile pointing to an Arabic-capable TTF (e.g. Noto Naskh Arabic).
Chinese label glyphs need a CJK font (auto-detected; override with --cjk-fontfile).

Usage:
  python compose_bilingual.py \
    --en en_talk.mp4 --ar ar_talk.mp4 \
    --en-text en.txt --ar-text ar.txt \
    --en-label "English" --ar-label "العربية" \
    --out bilingual_final.mp4
"""
import argparse
import os
import re
import shutil
import subprocess
import sys


def find_ffmpeg(explicit=None):
    if explicit:
        return explicit
    found = shutil.which("ffmpeg")
    if not found:
        candidate = os.path.join(
            os.environ.get("LOCALAPPDATA", ""), "PASMStudio", "bin", "ffmpeg.exe"
        )
        if os.path.exists(candidate):
            return candidate
        sys.exit("ffmpeg not found. Install ffmpeg on PATH or pass --ffmpeg.")
    return found


# CJK font candidates (first hit wins). Needed to render the Chinese label glyphs.
CJK_FONT_CANDIDATES = [
    "C:/Windows/Fonts/msyh.ttc",      # Windows 微软雅黑
    "C:/Windows/Fonts/msyhl.ttc",
    "C:/Windows/Fonts/simhei.ttf",    # Windows 黑体
    "C:/Windows/Fonts/simsun.ttc",
    "/System/Library/Fonts/PingFang.ttc",           # macOS
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",  # Linux
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
]


def find_cjk_font(explicit=None) -> str:
    if explicit:
        return explicit
    for path in CJK_FONT_CANDIDATES:
        if os.path.exists(path):
            return path.replace("\\", "/")
    return ""


def esc(text: str) -> str:
    """Escape text for use inside a drawtext='...' value."""
    return (
        text.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("%", "%%")
    )


def _find_ffprobe(ffmpeg: str):
    """Locate ffprobe next to the ffmpeg binary or on PATH; None if absent."""
    candidates = [
        shutil.which("ffprobe"),
        os.path.join(os.path.dirname(ffmpeg), "ffprobe.exe"),
        os.path.join(os.path.dirname(ffmpeg), "ffprobe"),
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None


def probe_duration(path: str, ffmpeg: str) -> float:
    """Duration in seconds. Prefers ffprobe; falls back to parsing `ffmpeg -i`
    stderr (some bundles, e.g. PASMStudio's, ship ffmpeg without ffprobe)."""
    ffprobe = _find_ffprobe(ffmpeg)
    if ffprobe:
        try:
            out = subprocess.check_output(
                [
                    ffprobe,
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    path,
                ],
                stderr=subprocess.DEVNULL,
            )
            return float(out.strip())
        except (subprocess.CalledProcessError, ValueError):
            pass
    proc = subprocess.run(
        [ffmpeg, "-i", path], capture_output=True, text=True, errors="replace"
    )
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", proc.stderr)
    if not m:
        sys.exit(f"could not determine duration of {path}")
    hh, mm, ss = m.groups()
    return int(hh) * 3600 + int(mm) * 60 + float(ss)


def build_srt(text_path: str, duration: float, srt_path: str):
    with open(text_path, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.read().splitlines() if ln.strip()]
    if not lines:
        lines = [""]
    total_chars = sum(len(ln) for ln in lines) or 1
    # Small tail padding so the last subtitle does not cut off early.
    usable = duration * 0.97
    cursor = 0.0
    entries = []
    for i, ln in enumerate(lines):
        share = (len(ln) / total_chars) * usable
        start = cursor
        end = cursor + share if i < len(lines) - 1 else duration
        entries.append((i + 1, start, end, ln))
        cursor += share

    def fmt(t: float) -> str:
        ms = int(round(t * 1000))
        h, ms = divmod(ms, 3600_000)
        m, ms = divmod(ms, 60_000)
        s, ms = divmod(ms, 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    with open(srt_path, "w", encoding="utf-8") as f:
        for idx, start, end, txt in entries:
            f.write(f"{idx}\n{fmt(start)} --> {fmt(end)}\n{txt}\n\n")
    print(f"[compose] wrote {srt_path} ({len(entries)} cues)")


def run(cmd, cwd=None):
    print("[cmd]", " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=cwd)


def _font_part(fontfile: str) -> str:
    return f"fontfile='{fontfile}'" if fontfile else "font='Arial'"


def _watermark_filter(label: str, cjk_font: str, height: int) -> str:
    """Persistent top-right corner watermark (explicit AI label)."""
    fontsize = max(22, int(height / 28))
    return (
        f"drawtext=text='{esc(label)}':{_font_part(cjk_font)}:"
        f"fontsize={fontsize}:fontcolor=white@0.92:borderw=2:bordercolor=black@0.55:"
        f"x=w-text_w-28:y=28"
    )


def main():
    ap = argparse.ArgumentParser(description="Compose bilingual talking-head video")
    ap.add_argument("--en", required=True, help="English talking-head clip (.mp4)")
    ap.add_argument("--ar", required=True, help="Arabic talking-head clip (.mp4)")
    ap.add_argument("--en-text", required=True, help="English transcript (.txt)")
    ap.add_argument("--ar-text", required=True, help="Arabic transcript (.txt)")
    ap.add_argument("--en-label", default="English")
    ap.add_argument("--ar-label", default="العربية")
    ap.add_argument("--out", required=True, help="Output MP4")
    ap.add_argument("--ffmpeg", default=None)
    ap.add_argument("--fontfile", default=None, help="TTF for Arabic-capable rendering")
    ap.add_argument("--card-dur", type=float, default=2.0, help="Title card seconds")
    ap.add_argument("--resolution", default="1280x720")
    # --- AI content labels (on by default, per 《人工智能生成合成内容标识办法》) ---
    ap.add_argument("--ai-label", default="AI 生成",
                    help="Corner watermark text (explicit label). Default: 'AI 生成'")
    ap.add_argument("--ai-notice", default="本视频由 AI 生成",
                    help="End-card Chinese notice line")
    ap.add_argument("--ai-notice-en", default="AI-Generated Content",
                    help="End-card English notice line")
    ap.add_argument("--label-card-dur", type=float, default=3.0,
                    help="End notice card seconds")
    ap.add_argument("--no-ai-label", action="store_true",
                    help="Disable explicit labels (watermark + end card). "
                         "Not recommended for public distribution.")
    ap.add_argument("--cjk-fontfile", default=None,
                    help="Override auto-detected CJK font for Chinese label glyphs")
    args = ap.parse_args()

    ffmpeg = find_ffmpeg(args.ffmpeg)
    # ffmpeg's filter parser mishandles Windows drive-letter colons in the
    # positional subtitles filename (quotes do NOT protect it on some builds),
    # so inputs/outputs become absolute and subtitle burns run with cwd=work
    # using bare basenames.
    args.en = os.path.abspath(args.en)
    args.ar = os.path.abspath(args.ar)
    args.out = os.path.abspath(args.out)
    if args.fontfile:
        args.fontfile = args.fontfile.replace("\\", "/")
    w, h = args.resolution.split("x")
    h = int(h)
    work = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(work, exist_ok=True)

    cjk_font = find_cjk_font(args.cjk_fontfile)
    if not args.no_ai_label:
        if cjk_font:
            print(f"[compose] CJK font: {cjk_font}")
        else:
            print("[compose][warn] no CJK font found — Chinese label glyphs would "
                  "render as boxes. Watermark falls back to 'AI' and the end card "
                  "to English only. Pass --cjk-fontfile to fix.")
            args.ai_label = "AI"
            args.ai_notice = ""  # skip Chinese line

    en_dur = probe_duration(args.en, ffmpeg)
    ar_dur = probe_duration(args.ar, ffmpeg)

    en_srt = os.path.join(work, "en.srt")
    ar_srt = os.path.join(work, "ar.srt")
    build_srt(args.en_text, en_dur, en_srt)
    build_srt(args.ar_text, ar_dur, ar_srt)

    # Subtitle style; inject a fontfile when provided.
    sub_style = "FontSize=28,Alignment=2,Bold=1,Outline=2,Shadow=1"
    if args.fontfile:
        sub_style += f",FontFile={args.fontfile}"
    en_sub = os.path.join(work, "en_sub.mp4")
    ar_sub = os.path.join(work, "ar_sub.mp4")
    run(
        [
            ffmpeg, "-y", "-i", args.en,
            "-vf", f"subtitles={os.path.basename(en_srt)}:force_style='{sub_style}'",
            "-c:v", "libx264", "-c:a", "aac", "-movflags", "+faststart", en_sub,
        ],
        cwd=work,
    )
    run(
        [
            ffmpeg, "-y", "-i", args.ar,
            "-vf", f"subtitles={os.path.basename(ar_srt)}:force_style='{sub_style}'",
            "-c:v", "libx264", "-c:a", "aac", "-movflags", "+faststart", ar_sub,
        ],
        cwd=work,
    )

    # Title cards with silent audio (so concat has audio on every input).
    title_en = os.path.join(work, "title_en.mp4")
    run(
        [
            ffmpeg, "-y",
            "-f", "lavfi", "-i", f"color=c=0x101830:s={args.resolution}:d={args.card_dur}",
            "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={args.card_dur}",
            "-vf", _drawtext(args.en_label, args.fontfile, h, 72, "(h-text_h)/2"),
            "-c:v", "libx264", "-c:a", "aac", "-pix_fmt", "yuv420p", "-shortest", title_en,
        ]
    )
    title_ar = os.path.join(work, "title_ar.mp4")
    run(
        [
            ffmpeg, "-y",
            "-f", "lavfi", "-i", f"color=c=0x101830:s={args.resolution}:d={args.card_dur}",
            "-f", "lavfi", "-i", f"anullsrc=r=44100:cl=stereo:d={args.card_dur}",
            "-vf", _drawtext(args.ar_label, args.fontfile, h, 72, "(h-text_h)/2"),
            "-c:v", "libx264", "-c:a", "aac", "-pix_fmt", "yuv420p", "-shortest", title_ar,
        ]
    )

    # End notice card (explicit AI label). Built like the title cards.
    notice = os.path.join(work, "notice_card.mp4")
    if not args.no_ai_label:
        lines = []
        if args.ai_notice:
            lines.append(
                _drawtext(args.ai_notice, cjk_font, h, max(40, int(h / 9)),
                          f"(h/2)-(h/12)-20")
            )
        lines.append(
            _drawtext(args.ai_notice_en, cjk_font, h, max(28, int(h / 16)),
                      "(h/2)+20")
        )
        run(
            [
                ffmpeg, "-y",
                "-f", "lavfi", "-i",
                f"color=c=0x101830:s={args.resolution}:d={args.label_card_dur}",
                "-f", "lavfi", "-i",
                f"anullsrc=r=44100:cl=stereo:d={args.label_card_dur}",
                "-vf", ",".join(lines),
                "-c:v", "libx264", "-c:a", "aac", "-pix_fmt", "yuv420p", "-shortest",
                notice,
            ]
        )

    # Normalize resolution (+ optional watermark) then concat.
    scale = (
        f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
        f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1"
    )
    wm = "" if args.no_ai_label else "," + _watermark_filter(
        args.ai_label, cjk_font, h
    )
    if not args.no_ai_label:
        inputs = ["-i", title_en, "-i", en_sub, "-i", title_ar, "-i", ar_sub,
                  "-i", notice]
        chains = []
        for i in range(4):
            chains.append(f"[{i}:v]{scale}{wm}[{i}v]")
        chains.append(f"[4:v]{scale}[4v]")  # notice card is itself the label
        concat_n = 5
    else:
        inputs = ["-i", title_en, "-i", en_sub, "-i", title_ar, "-i", ar_sub]
        chains = [f"[{i}:v]{scale}[{i}v]" for i in range(4)]
        concat_n = 4

    stream_specs = "".join(f"[{i}v][{i}:a]" for i in range(concat_n))
    filter_complex = (
        ";".join(chains) + ";" + stream_specs +
        f"concat=n={concat_n}:v=1:a=1[outv][outa]"
    )

    out_cmd = [
        ffmpeg, "-y", *inputs,
        "-filter_complex", filter_complex,
        "-map", "[outv]", "-map", "[outa]",
        "-c:v", "libx264", "-c:a", "aac", "-movflags", "+faststart",
        "-pix_fmt", "yuv420p",
        # Implicit (隐式) AI-content label: file metadata.
        "-metadata", "comment=本视频由人工智能（AI）生成合成（数字人+语音合成+自动字幕）",
        "-metadata", "description=AI-generated synthetic content (digital human, "
                     "TTS voiceover, auto subtitles). Generated by the "
                     "digital-human-spokesperson skill.",
        args.out,
    ]
    run(out_cmd)

    if args.no_ai_label:
        print("[compose] AI labels DISABLED via --no-ai-label "
              "(metadata comment still written).")
    else:
        print("[compose] AI labels ON: corner watermark + end notice card + "
              "MP4 metadata (comment/description).")
    total = args.card_dur * 2 + en_dur + ar_dur + (
        0 if args.no_ai_label else args.label_card_dur
    )
    print(f"[compose] done -> {args.out} (total ~{total:.1f}s)")


def _drawtext(label: str, fontfile: str, height: int, fontsize: int,
              y_expr: str) -> str:
    return (
        f"drawtext=text='{esc(label)}':{_font_part(fontfile)}:"
        f"fontcolor=white:fontsize={fontsize}:x=(w-text_w)/2:y={y_expr}"
    )


if __name__ == "__main__":
    main()
