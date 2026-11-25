#!/usr/bin/env python3
"""Check what the AI dubbing skill needs, and say how to fix anything missing.

    python3 scripts/check_setup.py
"""
import os, platform, shutil, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import aclib  # noqa: E402  (also makes this console print UTF-8 on Windows)

ok = True


def line(state, what, detail=""):
    print(f"[{state}] {what}{': ' + detail if detail else ''}")


def main():
    global ok
    v = sys.version_info
    if v < (3, 9):
        line("missing", "Python 3.9 or newer", f"this is {platform.python_version()}")
        ok = False
    else:
        line("ok", "Python", platform.python_version())
    try:
        import PIL
        line("ok", "Pillow", f"{PIL.__version__}: draws the captions")
    except ImportError:
        line("missing", "Pillow", "pip install pillow")
        ok = False
    try:
        import numpy
        line("ok", "numpy", f"{numpy.__version__}: fits and mixes the dub")
    except ImportError:
        line("missing", "numpy", "pip install numpy")
        ok = False
    if shutil.which("ffmpeg") and shutil.which("ffprobe"):
        out = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.split("\n")[0]
        line("ok", "ffmpeg", (out.split() + ["", "", "?"])[2])
        if aclib.ffmpeg_has("encoders", "libx264"):
            line("ok", "H.264 encoder", "libx264")
        elif any(aclib.ffmpeg_has("encoders", e) for e in ("h264_videotoolbox", "h264_mf", "h264_nvenc",
                                                             "h264_qsv", "libopenh264")):
            line("note", "H.264 encoder", "no libx264; a hardware encoder will be used (bigger files)")
        else:
            line("missing", "H.264 encoder", "this ffmpeg can't make MP4s for social apps. Mac: brew install "
                 "ffmpeg. Windows: winget install Gyan.FFmpeg. Linux: your distro's full ffmpeg package")
            ok = False
    else:
        line("missing", "ffmpeg", "Mac: brew install ffmpeg. Windows: winget install Gyan.FFmpeg (then open a "
             "new terminal). Linux: sudo apt install ffmpeg")
        ok = False
    routes = []
    try:
        import faster_whisper
        routes.append(f"local faster-whisper {faster_whisper.__version__} (free, private)")
    except ImportError:
        pass
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        try:
            import mlx_whisper  # noqa: F401
            routes.append("mlx-whisper (fast on Apple Silicon)")
        except ImportError:
            pass
    for env, name in (("GROQ_API_KEY", "Groq"), ("DEEPGRAM_API_KEY", "Deepgram")):
        if os.environ.get(env):
            routes.append(f"{name} ({env} set)")
    if routes:
        line("ok", "Transcription", "; ".join(routes))
    else:
        line("missing", "Transcription",
             "pip install faster-whisper (free, runs on this computer). Or set GROQ_API_KEY or DEEPGRAM_API_KEY. "
             "Or give each video's own .srt/.vtt subtitles")
        ok = False
    voices = []
    try:
        import kokoro_onnx, soundfile  # noqa: F401
        voices.append("Kokoro (free: English, Spanish, French, Italian, Portuguese, Hindi)")
    except ImportError:
        pass
    try:
        import piper  # noqa: F401
        voices.append("Piper (free: German, Dutch, Polish, Russian and more)")
    except ImportError:
        pass
    if os.environ.get("ELEVENLABS_API_KEY"):
        voices.append("ElevenLabs (ELEVENLABS_API_KEY set: any language, your own voice; uses your credits)")
    if voices:
        line("ok", "Voices", "; ".join(voices))
        if not any(v.startswith("Kokoro") for v in voices):
            line("optional", "Free voices for English, Spanish, French, Italian, Portuguese, Hindi",
                 "pip install kokoro-onnx soundfile")
        if not any(v.startswith("Piper") for v in voices):
            line("optional", "Free voices for German, Dutch, Polish, Russian and more", "pip install piper-tts")
    else:
        line("missing", "Voices", "pip install kokoro-onnx soundfile (free; English, Spanish, French, Italian, "
             "Portuguese, Hindi) and/or pip install piper-tts (free; German, Dutch, Polish, Russian and more). "
             "Or set ELEVENLABS_API_KEY to use your own ElevenLabs account")
        ok = False
    try:
        import demucs  # noqa: F401
        line("ok", "Voice removal", "demucs installed: dub.background \"separate\" works")
    except ImportError:
        line("optional", "Remove the original voice under the dub", "pip install demucs (about 2 GB, slow on a laptop); "
             "without it the original sound is turned down under the dub")
    if platform.system() == "Darwin" and platform.machine() == "arm64" and "mlx" not in " ".join(routes):
        line("optional", "Faster on this Mac", "pip install mlx-whisper")
    rtl = []
    try:
        import arabic_reshaper, bidi  # noqa: F401
        rtl.append("ok")
    except ImportError:
        pass
    if aclib.has_raqm():
        line("ok", "Complex scripts", "Pillow has text shaping (Arabic, Hebrew, Hindi, Thai...)")
    elif rtl:
        line("ok", "Arabic and Hebrew captions", "arabic-reshaper and python-bidi installed")
    else:
        line("optional", "Arabic, Persian, Urdu or Hebrew captions", "pip install arabic-reshaper python-bidi")
    for f in ("Poppins-ExtraBold.ttf", "Poppins-Bold.ttf", "Anton-Regular.ttf", "Inter.ttf"):
        p = os.path.join(aclib.FONT_DIR, f)
        if not (os.path.exists(p) and os.path.getsize(p) > 10000):
            line("note", "Fonts", f"{f} will be downloaded on first use (SIL Open Font License)")
            break
    else:
        line("ok", "Fonts", "bundled (Poppins, Anton, Inter)")
    scripts = os.path.dirname(os.path.abspath(__file__))
    print()
    if ok:
        print(f"Ready. From your own project folder (not this skill's), run: python3 {scripts}{os.sep}<name>.py ...")
    else:
        print("Install what's missing above, then run this again.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    aclib.guard(main)
