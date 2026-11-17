#!/usr/bin/env python3
"""Check what the cross-post video skill needs, and say how to fix anything missing.

    python3 scripts/check_setup.py
"""
import os, platform, shutil, subprocess, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xplib  # noqa: E402  (also makes this console print UTF-8 on Windows)

ok = True


def line(state, what, detail=""):
    print(f"[{state}] {what}{': ' + detail if detail else ''}")


def main():
    global ok
    if sys.version_info < (3, 9):
        line("missing", "Python 3.9 or newer", f"this is {platform.python_version()}")
        ok = False
    else:
        line("ok", "Python", platform.python_version())
    if shutil.which("ffmpeg") and shutil.which("ffprobe"):
        out = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True).stdout.split("\n")[0]
        line("ok", "ffmpeg", (out.split() + ["", "", "?"])[2] + ": reads the video and re-encodes it when needed")
        if not any(xplib.ffmpeg_has("encoders", e) for e in ("libx264", "h264_videotoolbox", "h264_mf",
                                                               "h264_nvenc", "h264_qsv", "libopenh264")):
            line("note", "H.264 encoder", "this ffmpeg can check videos but not re-encode them (--fix). Mac: brew "
                 "install ffmpeg. Windows: winget install Gyan.FFmpeg. Linux: your distro's full ffmpeg package")
        if not (xplib.ffmpeg_has("filters", "zscale") and xplib.ffmpeg_has("filters", "tonemap")):
            line("note", "HDR video", "this ffmpeg has no zscale filter, so --fix can't turn HDR video (the "
                 "extra-bright colour newer phones record) into standard colour. Everything else works. For an "
                 "HDR video, export a standard-colour (Rec. 709, SDR) copy from the phone or editor, or install "
                 "an ffmpeg build with zscale")
    else:
        line("missing", "ffmpeg", "Mac: brew install ffmpeg. Windows: winget install Gyan.FFmpeg (then open a "
             "new terminal). Linux: sudo apt install ffmpeg")
        ok = False
    try:
        import PIL
        line("ok", "Pillow", f"{PIL.__version__}: makes the cover sheet")
    except ImportError:
        line("optional", "Pillow", "pip install pillow (only for picking a cover with cover.py)")
    try:
        from zoneinfo import ZoneInfo
        ZoneInfo("Europe/Amsterdam")
        line("ok", "Time zones")
    except Exception:
        line("missing", "Time zones", "pip install tzdata (needed on Windows to schedule in your own time zone)")
        ok = False
    scripts = os.path.dirname(os.path.abspath(__file__))
    print()
    if ok:
        py = "py" if os.name == "nt" else "python3"
        print(f"Ready. From your own project folder (not this skill's), run: {py} {scripts}{os.sep}<name>.py ...")
    else:
        print("Install what's missing above, then run this again.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    xplib.guard(main)
