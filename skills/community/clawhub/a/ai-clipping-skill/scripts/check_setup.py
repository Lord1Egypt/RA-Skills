#!/usr/bin/env python3
"""Check what the AI clipping skill needs, and say how to fix anything missing.

    python3 scripts/check_setup.py
"""
import os, platform, shutil, subprocess, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cliplib  # noqa: E402  (also makes this console print UTF-8 on Windows)

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
        line("ok", "ffmpeg", (out.split() + ["", "", "?"])[2] + ": reads, cuts and checks the clips")
        if not cliplib.ffmpeg_has("encoders", "libx264"):
            line("note", "libx264", "this ffmpeg can check clips but cutting new ones needs libx264. Mac: brew "
                 "install ffmpeg. Windows: winget install Gyan.FFmpeg. Linux: your distro's full ffmpeg package")
    else:
        line("missing", "ffmpeg", "Mac: brew install ffmpeg. Windows: winget install Gyan.FFmpeg (then open a "
             "new terminal). Linux: sudo apt install ffmpeg")
        ok = False
    try:
        import PIL
        line("ok", "Pillow", f"{PIL.__version__}: draws captions, the hook and the on-screen disclosure")
    except ImportError:
        line("optional", "Pillow", "pip install pillow (needed only to cut clips with make_clips.py; checking, "
             "planning, posting and the ledger work without it)")
    try:
        import faster_whisper  # noqa: F401
        line("ok", "faster-whisper", "free local transcription")
    except ImportError:
        keys = [k for k in ("GROQ_API_KEY", "OPENAI_API_KEY") if os.environ.get(k)]
        if keys:
            line("ok", "Transcription", f"{keys[0]} is set")
        else:
            line("optional", "Transcription", "pip install faster-whisper (free, local), or set GROQ_API_KEY or "
                 "OPENAI_API_KEY, or pass captions you already have with transcribe.py --from captions.srt")
    try:
        import zoneinfo
        zoneinfo.ZoneInfo("America/New_York")
        line("ok", "Time zones", "deadlines are shown in the campaign's own time zone")
    except Exception:
        line("optional", "Time zones", "pip install tzdata (Windows has no time zone database of its own; without "
             "it every time is shown in UTC)")
    home = cliplib.user_home()
    line("ok", "Ledger", f"{cliplib.ledger_path(None)} (one for every campaign; AI_CLIPPING_LEDGER or --ledger "
         f"moves it), saved accounts in {os.path.join(home, 'accounts.json')}")
    scripts = os.path.dirname(os.path.abspath(__file__))
    print()
    if ok:
        py = "py" if os.name == "nt" else "python3"
        print(f"Ready. From your own project folder (not this skill's), run: {py} {scripts}{os.sep}<name>.py ...")
    else:
        print("Install what's missing above, then run this again.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    cliplib.guard(main)
