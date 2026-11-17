#!/usr/bin/env python3
"""Check one video file against TikTok, Instagram Reels and YouTube Shorts (and others) at once.

    python3 scripts/check_video.py clip.mp4                       # the three short-video platforms
    python3 scripts/check_video.py clip.mp4 --platforms TIKTOK,INSTAGRAM,YOUTUBE,FACEBOOK
    python3 scripts/check_video.py clip.mp4 --tiktok-max 180      # this TikTok account's own limit, in seconds
    python3 scripts/check_video.py clip.mp4 --fix                 # write clip.crosspost.mp4 that passes

--fix never touches the original. It re-encodes to the one format every platform takes (MP4,
H.264, 8-bit, AAC stereo sound, index at the start, under 300 MB). It keeps the picture size and
only scales down a video that is over 1920 px wide or 4096 px on a side. It doesn't crop, pad,
speed up or add anything; length and shape problems are yours to decide. HDR video is converted
to standard colour when this ffmpeg can do that properly (the zscale filter); when it can't,
--fix stops and says how to get a standard-colour file, and writes nothing.
Exit code 0 when no platform has an error, 1 otherwise. --json prints the result as JSON.
"""
import argparse, json, math, os, subprocess, sys

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xplib import (HDR_TRANSFER, LIMITS, MB, die, ffmpeg_has, file_issues, guard, need_ffmpeg, probe,  # noqa: E402
                   reading, rel, run, same_file)

SIZE_TARGET = 285 * 10 ** 6   # bytes: under Instagram's 300 MB however a megabyte is counted
HDR_WAYS = ("On a phone: export or share it as a standard (SDR / Most Compatible) video if your phone offers that, "
            "or turn off HDR video in the camera settings and film again. An editing app: export as Rec. 709 (also "
            "called SDR). Or install an ffmpeg build that has the zscale filter and use --fix")
HDR_HELP = ("this video is HDR (the extra-bright colour that newer phones record), and this ffmpeg can't turn HDR "
            "into standard colour, so no file was written. Get a standard-colour file one of these ways. " + HDR_WAYS)


def can_convert_hdr():
    return ffmpeg_has("filters", "zscale") and ffmpeg_has("filters", "tonemap")


def describe(info):
    sound = f"{info['acodec']} {info['audio_rate']} Hz" if info["audio"] else "no sound"
    length = f"{info['duration']:.1f} s" if info["duration"] else "length unknown"
    return (f"{info['width']}x{info['height']}, {length}, {info['fps']:g} fps, {info['vcodec']} "
            f"{info['pix_fmt']}, {sound}, {info['bytes'] / MB:.1f} MB, {info['mbps']:g} Mbps")


def encoder(cap_kbps, exact=False):
    """H.264 settings. cap_kbps keeps the file under the size target; exact aims straight at it."""
    if ffmpeg_has("encoders", "libx264"):
        if exact:
            return ["-c:v", "libx264", "-preset", "medium", "-b:v", f"{cap_kbps}k", "-maxrate",
                    f"{cap_kbps}k", "-bufsize", f"{cap_kbps * 2}k", "-profile:v", "high"]
        top = min(12000, cap_kbps or 12000)
        return ["-c:v", "libx264", "-preset", "medium", "-crf", "19", "-maxrate", f"{top}k", "-bufsize",
                f"{top * 2}k", "-profile:v", "high"]
    for enc in ("h264_videotoolbox", "h264_mf", "h264_nvenc", "h264_qsv", "libopenh264"):
        if ffmpeg_has("encoders", enc):
            return ["-c:v", enc, "-b:v", f"{min(9000, cap_kbps or 9000)}k"]
    die("this ffmpeg build has no H.264 encoder. Install a full build: Mac: brew install ffmpeg. "
        "Windows: winget install Gyan.FFmpeg. Linux: your distro's full ffmpeg package")


def target_size(w, h):
    """The size to scale down to, or None when no platform limit asks for it. Instagram takes up
    to 1920 px wide and TikTok up to 4096 px a side, so 1920x1080 and 1920x1920 stay as they are."""
    if not w or not h or (w <= 1920 and max(w, h) <= 4096):
        return None
    box_w, box_h = (1080, 1920) if h > w else (1920, 1920)
    f = min(box_w / w, box_h / h)
    return max(int(w * f / 2) * 2, 2), max(int(h * f / 2) * 2, 2)


def fix(src, info, out):
    hdr = info["transfer"] in HDR_TRANSFER
    if hdr and not can_convert_hdr():
        die(HDR_HELP)
    vf = []
    if hdr:
        vf.append("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,"
                  "zscale=t=bt709:m=bt709:r=tv")
    if info["field_order"] not in (None, "progressive", "unknown"):
        vf.append("yadif")
    size = target_size(info["width"], info["height"])
    vf.append(f"scale={size[0]}:{size[1]}" if size else "scale=trunc(iw/2)*2:trunc(ih/2)*2")
    vf.append("format=yuv420p")
    if hdr:   # the frames carry their own colour tags; set them on the frames, output flags are ignored
        vf.append("setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709")
    fps = info["fps"]
    rate = []
    if fps and fps > 60:
        rate, fps = ["-r", "60"], 60
    elif fps and fps < 23:
        rate, fps = ["-r", "30"], 30
    gop = str(int(round(fps * 2))) if fps else "60"   # a keyframe every 2 seconds
    cap = None
    if info["duration"]:
        cap = int(SIZE_TARGET * 8 / info["duration"] / 1000) - 140   # minus the sound and the file's own overhead
        if cap < 800:
            die(f"at {info['duration']:.0f} s this video can't fit Instagram's 300 MB at a watchable quality. "
                "Post a shorter cut there")
    part = out[:-4] + ".part.mp4"
    if same_file(part, src):
        die(f"{rel(src)} has the name --fix uses for its unfinished file; rename the video or give another --out")

    def encode(video_args):
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", src, "-map", "0:v:0", "-map", "0:a:0?", "-vf", ",".join(vf)]
        cmd += rate + video_args + ["-g", gop, "-pix_fmt", "yuv420p"]
        cmd += ["-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
                "-map_metadata", "-1", part]
        run(cmd)

    try:   # whatever happens (an error, Ctrl-C), no unfinished file stays behind
        try:
            encode(encoder(cap))
        except SystemExit:
            if not hdr:
                raise
            die("this ffmpeg could not convert this video's HDR colour to standard colour, so no file was "
                "written. Get a standard-colour file one of these ways. " + HDR_WAYS)
        if os.path.getsize(part) > SIZE_TARGET and cap:
            encode(encoder(int(cap * 0.9), exact=True))
        if os.path.getsize(part) > SIZE_TARGET:
            die("the re-encoded file is still over Instagram's 300 MB; nothing was written. Post a shorter cut there")
        r = subprocess.run(["ffmpeg", "-v", "error", "-i", part, "-f", "null", "-"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode != 0 or r.stderr.strip():
            die("the new file didn't play back cleanly; nothing was written. ffmpeg said: "
                + (r.stderr.strip().splitlines() or ["(no message)"])[-1])
        if probe(part, rel(out))["transfer"] in HDR_TRANSFER:
            die("the new file still came out as HDR, so nothing was written. Get a standard-colour file one "
                "of these ways. " + HDR_WAYS)
        os.replace(part, out)
    finally:
        if os.path.exists(part):
            try:
                os.remove(part)
            except OSError:
                pass


def report(info, platforms, tiktok_max):
    return {p: file_issues(info, p, tiktok_max) for p in platforms}


def show(result, tiktok_max=None):
    for p, found in result.items():
        errs = [m for lv, m, _ in found if lv == "error"]
        state = "PROBLEM" if errs else ("ok, with notes" if found else "ok")
        print(f"  {LIMITS[p]['label']}: {state}")
        for lv, m, _ in found:
            print(f"    {lv}: {m}")
        if p == "TIKTOK" and not tiktok_max and not errs:
            print("    TikTok's maximum length is set per account; pass --tiktok-max once the account is connected.")


def main():
    ap = argparse.ArgumentParser(description="Check a video against each platform before posting.")
    ap.add_argument("video")
    ap.add_argument("--platforms", default="TIKTOK,INSTAGRAM,YOUTUBE")
    ap.add_argument("--tiktok-max", type=float, help="this TikTok account's maximum video length in seconds")
    ap.add_argument("--fix", action="store_true", help="write a re-encoded copy that passes")
    ap.add_argument("--out", help="where --fix writes (default: <name>.crosspost.mp4 next to the video)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    reading(a.video)
    need_ffmpeg()
    platforms = [p.strip().upper() for p in a.platforms.split(",") if p.strip()]
    bad = [p for p in platforms if p not in LIMITS]
    if bad or not platforms:
        die(f"unknown platform {', '.join(bad) or '(none)'}. Use: {', '.join(LIMITS)}")
    if a.tiktok_max is not None and not (math.isfinite(a.tiktok_max) and a.tiktok_max > 0):
        die("--tiktok-max is a number of seconds above 0, like 180")
    info = probe(a.video)
    result = report(info, platforms, a.tiktok_max)
    fixable = any(f for found in result.values() for lv, _, f in found if lv == "error" or f)
    hdr_stuck = info["transfer"] in HDR_TRANSFER and not can_convert_hdr()
    out, fixed = None, None
    if a.fix:
        if not any(f for found in result.values() for _, _, f in found):
            if not a.json:
                print(f"{rel(a.video)}: nothing a re-encode would fix; no new file written")
        else:
            out = a.out or os.path.splitext(a.video)[0] + ".crosspost.mp4"
            if same_file(out, a.video):
                die("--out must be a different file from the video; the original is never overwritten")
            if not out.lower().endswith(".mp4"):
                die("--out must end in .mp4")
            folder = os.path.dirname(os.path.abspath(out))
            if os.path.isdir(out):
                die(f"--out {out} is a folder; give a file name ending in .mp4")
            if not os.path.isdir(folder):
                die(f"the folder for --out doesn't exist: {rel(folder)}. Make it first, or pick another place")
            if not os.access(folder, os.W_OK):
                die(f"can't write in {rel(folder)}; pick another place with --out")
            fix(a.video, info, out)
            fixed = report(probe(out), platforms, a.tiktok_max)
    final = fixed if fixed is not None else result
    errors = sum(1 for found in final.values() for lv, _, _ in found if lv == "error")
    if a.json:
        print(json.dumps({"file": rel(a.video), "info": info, "fixed_file": rel(out) if out else None,
                          "platforms": {p: [{"level": lv, "message": m, "fixable": f} for lv, m, f in found]
                                        for p, found in final.items()}, "errors": errors,
                          "hdr_needs_another_file": hdr_stuck}, indent=1))
        sys.exit(1 if errors else 0)
    print(f"{rel(a.video)}: {describe(info)}")
    show(result, a.tiktok_max)
    if out:
        print(f"\nwrote {rel(out)}: {describe(probe(out))}")
        show(fixed, a.tiktok_max)
        print("The original is untouched. Watch the new file once before posting it.")
    elif errors and fixable and not a.fix:
        if hdr_stuck:
            print("\nThis video is HDR (the extra-bright colour that newer phones record) and this ffmpeg can't "
                  "turn HDR into standard colour, so --fix can't solve it here. Get a standard-colour file one of "
                  "these ways. " + HDR_WAYS + ".")
        else:
            print("\nSome of this can be fixed by re-encoding: run again with --fix (the original stays as it is).")
    if errors:
        left = "after the re-encode " if out else ""
        print(f"\n{errors} problem(s) {left}to solve before this video can go to every platform checked.")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    guard(main)
