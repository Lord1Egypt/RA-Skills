"""Shared helpers for the cross-post video scripts: files, video probing and each platform's limits.
Standard library only."""
import functools, hashlib, json, os, re, subprocess, sys, unicodedata

try:  # Windows consoles default to cp1252; post texts are often not Latin
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Sizes are decimal megabytes (1 MB = 1,000,000 bytes): the stricter reading of every platform's
# limit, so a file that passes here passes whichever way a platform counts.
MB = 1000 ** 2
GB = 1000 * MB
# Documented limits for one video post through each platform's own posting API (seconds, bytes,
# characters). "text" is the caption or description; YouTube counts its description in bytes.
LIMITS = {
    "TIKTOK": {"label": "TikTok", "min_s": 3, "max_s": 600, "bytes": 4 * GB, "text": 2200,
               "fps": (23, 60), "max_side": 4096, "min_side": 360, "tags_warn": 5},
    "INSTAGRAM": {"label": "Instagram Reels", "min_s": 3, "max_s": 900, "bytes": 300 * MB, "text": 2200,
                  "fps": (23, 60), "max_width": 1920, "tags_max": 5, "mentions": 20, "strict": True},
    "YOUTUBE": {"label": "YouTube Shorts", "min_s": 1, "max_s": 180, "bytes": 256 * GB,
                "text_bytes": 5000, "title": 100, "tags_chars": 500, "tags_ignored": 60, "tags_warn": 5},
    "FACEBOOK": {"label": "Facebook", "min_s": 3, "max_s": 14400, "bytes": 4 * GB, "text": 5000},
    "LINKEDIN": {"label": "LinkedIn", "min_s": 3, "max_s": 900, "bytes": 5 * GB, "text": 3000},
    "LINKEDIN_PAGES": {"label": "LinkedIn Page", "min_s": 3, "max_s": 900, "bytes": 5 * GB, "text": 3000},
    "PINTEREST": {"label": "Pinterest", "min_s": 4, "max_s": 900, "bytes": 2 * GB, "text": 800,
                  "title": 100},
    "THREADS": {"label": "Threads", "min_s": 0, "max_s": 300, "bytes": 1 * GB, "text": 500},
    "X": {"label": "X", "min_s": 0.5, "max_s": 140, "bytes": 512 * MB, "text": 280},
    "BLUESKY": {"label": "Bluesky", "min_s": 0, "max_s": 180, "bytes": 100 * MB, "text": 300},
}
SHORT_FORM = ("TIKTOK", "INSTAGRAM", "YOUTUBE", "FACEBOOK")   # shown full screen, vertical
TIKTOK_PRIVACY = ("PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS", "FOLLOWER_OF_CREATOR", "SELF_ONLY")
HDR_TRANSFER = ("smpte2084", "arib-std-b67")
WINDOWS_RESERVED = {"con", "prn", "aux", "nul"} | {f"com{n}" for n in range(1, 10)} | {f"lpt{n}" for n in range(1, 10)}

_reading = [None]   # the file being read, for the last-resort message in guard()


def reading(path):
    _reading[0] = path


def die(msg):
    raise SystemExit("error: " + msg)


def guard(main):
    """Run a script's main(): any unexpected error becomes one clear line, not a traceback.
    Set CROSSPOST_DEBUG=1 to see the traceback."""
    try:
        main()
    except SystemExit:
        raise
    except KeyboardInterrupt:
        sys.exit("stopped. Run the same command again when you are ready")
    except Exception as e:
        if os.environ.get("CROSSPOST_DEBUG"):
            raise
        if isinstance(e, UnicodeEncodeError):
            sys.exit("error: a text holds half an emoji or a broken character (a cut-off copy). Retype that text")
        if isinstance(e, OSError):
            name = rel(str(e.filename)) if e.filename else "a file"
            sys.exit(f"error: can't read or write {name}: {e.strerror or e}. Check that it exists, that you "
                     "may write to that folder, and that no file there has the name of a folder this needs")
        where = rel(str(_reading[0])) if _reading[0] else "the file you gave"
        sys.exit(f"error: {where} has a value of the wrong kind somewhere (text where a number belongs, a list "
                 f"where one value belongs, or the reverse): {type(e).__name__}: {e}. "
                 "Set CROSSPOST_DEBUG=1 for details.")


def read_json(path):
    reading(path)
    try:
        with open(path, encoding="utf-8-sig") as fh:
            return json.load(fh)
    except FileNotFoundError:
        die(f"{path} not found")
    except IsADirectoryError:
        die(f"{path} is a folder, not a JSON file")
    except UnicodeDecodeError:
        die(f"{path} is not UTF-8 text (is it a JSON file?)")
    except json.JSONDecodeError as e:
        die(f"{path} is not valid JSON (line {e.lineno}, column {e.colno}): {e.msg}")
    except RecursionError:
        die(f"{path} has brackets nested far too deep to be one of this skill's files")


def write_json(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=1)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def write_text(path, text):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def rel(path, start=None):
    try:
        r = os.path.relpath(path, start or os.getcwd())
    except ValueError:  # another drive on Windows
        return path.replace(os.sep, "/")
    if r.startswith(os.pardir + os.sep + os.pardir + os.sep):
        return os.path.abspath(path).replace(os.sep, "/")
    return r.replace(os.sep, "/")


def same_file(a, b):
    """True when two paths are one file. Asks the disk, so CLIP.MP4 and clip.mp4 are one file on
    the disks that ignore upper and lower case (macOS, Windows) and two files where they differ."""
    try:
        if os.path.samefile(a, b):
            return True
    except OSError:
        pass
    return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))


def _mark(ch):
    return unicodedata.category(ch).startswith("M")


def slug(text):
    """A safe file name from any text: letters and digits of every script, lowercase, the rest
    becomes one dash. A text without a single letter or digit gets a name made from its content,
    so two different texts never share one."""
    out = []
    for ch in unicodedata.normalize("NFC", str(text)).lower():
        if ch.isalnum() or (out and out[-1] != "-" and _mark(ch)):
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    s = "".join(out)[:80].strip("-")
    if not s:
        s = "x" + hashlib.sha1(str(text).encode("utf-8", "surrogatepass")).hexdigest()[:8]
    if s in WINDOWS_RESERVED:   # Windows can't create a file with these names
        s += "-1"
    return s


def valid_id(text):
    """A video id: letters and digits of any script, single dashes between them, 80 at most."""
    return isinstance(text, str) and unicodedata.normalize("NFC", text).lower() == slug(text)


def need_ffmpeg():
    import shutil
    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        die("ffmpeg not found. Mac: brew install ffmpeg. Windows: winget install Gyan.FFmpeg (then open a "
            "new terminal). Linux: sudo apt install ffmpeg")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        last = (r.stderr.strip().splitlines() or ["(it gave no message)"])[-1].strip()
        die(f"{os.path.basename(cmd[0])} could not finish: {last}")
    return r


@functools.lru_cache(maxsize=None)
def ffmpeg_has(kind, name):
    """Whether this ffmpeg build has an encoder or filter."""
    r = subprocess.run(["ffmpeg", "-hide_banner", f"-{kind}"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return bool(re.search(rf"\s{re.escape(name)}\s", r.stdout))


def moov_first(path):
    """True when the MP4's index (moov) sits before the video data (mdat), which Instagram needs.
    None when the file isn't an MP4/MOV this can read."""
    try:
        with open(path, "rb") as fh:
            size = os.path.getsize(path)
            pos = 0
            while pos + 8 <= size:
                fh.seek(pos)
                head = fh.read(16)
                n = int.from_bytes(head[:4], "big")
                kind = head[4:8]
                if n == 1 and len(head) == 16:
                    n = int.from_bytes(head[8:16], "big")
                elif n == 0:
                    n = size - pos
                if kind == b"moov":
                    return True
                if kind == b"mdat":
                    return False
                if n < 8 or not kind.strip(b"\0").isalnum():
                    return None
                pos += n
    except OSError:
        return None
    return None


def jpeg_size(path):
    """(width, height) of a JPEG image, read from the file's own bytes (not its name).
    None when the file is not a JPEG that can be read."""
    try:
        with open(path, "rb") as fh:
            if fh.read(3) != b"\xff\xd8\xff":
                return None
            fh.seek(2)
            while True:
                b = fh.read(1)
                if not b:
                    return None
                if b != b"\xff":
                    continue
                m = fh.read(1)
                while m == b"\xff":
                    m = fh.read(1)
                if not m:
                    return None
                k = m[0]
                if k in (0x00, 0x01, 0xD8) or 0xD0 <= k <= 0xD7:
                    continue
                if k in (0xD9, 0xDA):   # the picture data starts and no size was found
                    return None
                seg = fh.read(2)
                if len(seg) < 2:
                    return None
                n = int.from_bytes(seg, "big")
                if 0xC0 <= k <= 0xCF and k not in (0xC4, 0xC8, 0xCC):
                    d = fh.read(5)
                    if len(d) < 5:
                        return None
                    w, h = int.from_bytes(d[3:5], "big"), int.from_bytes(d[1:3], "big")
                    return (w, h) if w and h else None
                if n < 2:
                    return None
                fh.seek(n - 2, 1)
    except OSError:
        return None


def file_kind(path):
    """A word for what a file really is, from its first bytes: for messages about a wrong cover."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(16)
    except OSError:
        return "a file that can't be read"
    if not head:
        return "an empty file"
    if head.startswith(b"\xff\xd8\xff"):
        return "a JPEG"
    if head.startswith(b"\x89PNG"):
        return "a PNG image"
    if head.startswith(b"GIF8"):
        return "a GIF image"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "a WebP image"
    if head[4:8] == b"ftyp":
        return "a HEIC photo or a video" if head[8:12] in (b"heic", b"heix", b"mif1", b"hevc") else "a video"
    return "not an image"


def _measured_duration(path, fps):
    """Length of a file that doesn't store one (browser and screen recordings): from its frames."""
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=pts_time",
                        "-of", "csv=p=0", path], capture_output=True, text=True, encoding="utf-8", errors="replace")
    times = []
    for x in r.stdout.replace(",", " ").split():
        try:
            times.append(float(x))
        except ValueError:
            pass
    if len(times) < 2:
        return 0.0
    return max(times) - min(times) + (1 / fps if fps else 0)


def probe(path, label=None):
    """Width and height as displayed (after rotation), fps, duration, codecs, colour, sound, size.
    label is the name used in messages (default: the path as given)."""
    name = label or path
    if not os.path.exists(path):
        die(f"{name} not found")
    if os.path.isdir(path):
        die(f"{name} is a folder; give one video file")
    if not os.path.getsize(path):
        die(f"{name} is an empty file (0 bytes)")
    need_ffmpeg()
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        d = json.loads(r.stdout or "{}")
    except json.JSONDecodeError:
        d = {}
    if not isinstance(d, dict):
        d = {}
    streams = d.get("streams") or []
    vs = [s for s in streams if s.get("codec_type") == "video" and not (s.get("disposition") or {}).get("attached_pic")]
    aus = [s for s in streams if s.get("codec_type") == "audio"]
    fmt = (d.get("format") or {}).get("format_name", "")
    if vs and (fmt == "image2" or fmt.endswith("_pipe")):
        die(f"{name} is an image, not a video")
    if not vs:
        die(f"{name}: no video in this file (is it a video?)")
    v = vs[0]
    w, h = int(v.get("width") or 0), int(v.get("height") or 0)
    if not w or not h:
        die(f"{name}: no video in this file (is it a video?)")
    rot = 0
    for sd in v.get("side_data_list") or []:
        if "rotation" in sd:
            try:
                rot = int(float(sd["rotation"]))
            except (TypeError, ValueError):
                pass
    try:
        rot = int(float((v.get("tags") or {}).get("rotate", rot)))
    except (TypeError, ValueError):
        pass
    if rot % 180:
        w, h = h, w

    def rate(txt):
        try:
            n, dd = (txt or "0/1").split("/")
            return float(n) / float(dd) if float(dd) else 0.0
        except (ValueError, ZeroDivisionError):
            return 0.0
    fps = rate(v.get("avg_frame_rate")) or rate(v.get("r_frame_rate"))
    if fps > 1000:   # a time base, not a frame rate (files without a stored rate)
        fps = 0.0
    dur = 0.0
    for src in ((d.get("format") or {}).get("duration"), v.get("duration")):
        try:
            dur = float(src)
            break
        except (TypeError, ValueError):
            continue
    if not dur or dur < 0:
        dur = _measured_duration(path, fps)
    a = aus[0] if aus else {}
    try:
        a_rate = int(a.get("sample_rate") or 0)
    except ValueError:
        a_rate = 0
    try:
        channels = int(a.get("channels") or 0)
    except (TypeError, ValueError):
        channels = 0
    size = os.path.getsize(path)
    return {"width": w, "height": h, "fps": round(fps, 3), "duration": round(dur, 3),
            "vcodec": v.get("codec_name"), "pix_fmt": v.get("pix_fmt"), "transfer": v.get("color_transfer"),
            "field_order": v.get("field_order"), "acodec": a.get("codec_name"), "audio": bool(aus),
            "audio_rate": a_rate, "channels": channels, "bytes": size,
            "mbps": round(size * 8 / dur / 1e6, 2) if dur else 0.0,
            "mp4": any(x in fmt for x in ("mp4", "mov")), "moov_first": moov_first(path)}


def size_text(n):
    """A byte count in words: 3.0 MB, 4 GB."""
    return f"{n / GB:g} GB" if n >= GB and n % GB == 0 else f"{n / MB:.1f} MB"


def file_issues(info, platform, tiktok_max_s=None):
    """Problems one platform has with this file: a list of (level, message, fixable by re-encoding)."""
    L = LIMITS[platform]
    name = L["label"]
    out = []
    s, w, h = info["duration"], info["width"], info["height"]
    max_s = L["max_s"]
    if platform == "TIKTOK" and tiktok_max_s:
        max_s = float(tiktok_max_s)
    if not s:
        out.append(("error", "can't read this file's length; re-save it as MP4 (check_video.py --fix)", True))
    elif s < L["min_s"]:
        out.append(("error", f"{s:.1f} s is shorter than the {name} minimum of {L['min_s']} s", False))
    if platform == "YOUTUBE":
        if s > max_s or w > h:
            why = f"{s:.0f} s is over 3 minutes" if s > max_s else f"{w}x{h} is wider than it is tall"
            out.append(("error", f"{why}, so YouTube would publish it as a normal video, not a Short", False))
    elif s > max_s:
        which = "this TikTok account's limit" if platform == "TIKTOK" and tiktok_max_s else f"the {name} limit"
        out.append(("error", f"{s:.0f} s is over {which} of {max_s:.0f} s", False))
    if platform == "INSTAGRAM" and s > 180:
        out.append(("warning", "over 3 minutes: it posts, but reports say Instagram doesn't recommend longer "
                    "Reels to people who don't follow the account", False))
    if info["bytes"] > L["bytes"]:
        out.append(("error", f"{size_text(info['bytes'])} is over the {name} limit of {size_text(L['bytes'])}", True))
    fps = L.get("fps")
    if fps and info["fps"] and not fps[0] - 0.1 <= info["fps"] <= fps[1] + 0.5:
        out.append(("error", f"{info['fps']:g} frames a second; {name} accepts {fps[0]} to {fps[1]}", True))
    if L.get("max_width") and w > L["max_width"]:
        out.append(("error", f"{w} px wide; {name} accepts up to {L['max_width']} px", True))
    if L.get("max_side") and max(w, h) > L["max_side"]:
        out.append(("error", f"{w}x{h}; {name} accepts up to {L['max_side']} px per side", True))
    if L.get("min_side") and min(w, h) < L["min_side"]:
        out.append(("error", f"{w}x{h}; {name} needs at least {L['min_side']} px per side", False))
    if platform in SHORT_FORM and h and platform != "YOUTUBE" and w > h:
        out.append(("warning", f"{w}x{h} is horizontal; {name} shows it small with bars. A vertical 9:16 "
                    "version fits", False))
    elif platform in SHORT_FORM and h and abs(w / h - 9 / 16) > 0.03:
        out.append(("warning", f"{w}x{h} isn't 9:16; {name} shows it with bars or crops the sides", False))
    if info["vcodec"] not in ("h264",) and not (info["vcodec"] == "hevc" and not L.get("strict")):
        lvl = "error" if L.get("strict") and info["vcodec"] != "hevc" else "warning"
        out.append((lvl, f"video codec is {info['vcodec']}; H.264 is the one every platform takes", True))
    if info["pix_fmt"] and not info["pix_fmt"].startswith(("yuv420p", "yuvj420p")):
        out.append(("error" if L.get("strict") else "warning",
                    f"pixel format {info['pix_fmt']}; platforms expect yuv420p", True))
    elif info["pix_fmt"] and "10" in info["pix_fmt"]:
        out.append(("warning", "10-bit video; 8-bit is the safe choice", True))
    if info["transfer"] in HDR_TRANSFER:
        out.append(("error" if L.get("strict") else "warning",
                    "HDR video; it can be rejected or look washed out. Convert it to standard colour", True))
    if info["field_order"] not in (None, "progressive", "unknown"):
        out.append(("warning", "interlaced video; platforms expect progressive", True))
    if L.get("strict"):
        if not info["mp4"]:
            out.append(("error", f"{name} takes MP4 or MOV files only", True))
        elif info["moov_first"] is False:
            out.append(("error", f"the file's index is at the end; {name} needs it at the start "
                        "(\"fast start\")", True))
        if info["audio"] and info["acodec"] != "aac":
            out.append(("error", f"audio codec is {info['acodec']}; {name} needs AAC", True))
        if info["audio_rate"] > 48000:
            out.append(("error", f"audio is {info['audio_rate']} Hz; {name} accepts up to 48,000 Hz", True))
        if info.get("channels", 0) > 2:
            out.append(("error", f"the sound has {info['channels']} channels (surround); {name} takes mono or "
                        "stereo", True))
        if info["mbps"] > 25:
            out.append(("error", f"{info['mbps']:g} Mbps; {name} accepts up to 25 Mbps", True))
    if not info["audio"] and platform in SHORT_FORM:
        out.append(("warning", "no sound track", False))
    return out


# ---- text: hashtags, handles, links and each platform's way of counting

URL_RE = re.compile(r"(?i:https?://|www\.)\S+"
                    r"|(?<![@\w.-])[A-Za-z0-9-]+\.(?:com|net|org|io|co|app|ai|dev|shop|store|me|ly)(?![A-Za-z0-9])(?:/\S*)?")


def hashtags(text):
    """Hashtags as the platforms read them: a # followed by letters or digits with at least one
    letter. "#1" is a number, not a hashtag."""
    return [h for h in re.findall(r"(?<![\w&])#\w+", text or "") if any(c.isalpha() for c in h)]


def mentions(text):
    return re.findall(r"(?<![\w@.])@[A-Za-z0-9_](?:[A-Za-z0-9_.]*[A-Za-z0-9_])", text or "")


def links(text):
    return [m.group(0).rstrip(".,;:!?)]}\"'") for m in URL_RE.finditer(text or "")]


def _emoji(ch):
    o = ord(ch)
    return o >= 0x1F000 or 0x2600 <= o <= 0x27BF or 0x2B00 <= o <= 0x2BFF or o in (0x200D, 0xFE0F, 0x20E3)


def clusters(text):
    """The text split into the characters a reader sees. A simple rule, not the full Unicode one:
    accents and marks, joined emoji, skin tones and flag pairs stay with the character before."""
    out, flag = [], False
    for ch in unicodedata.normalize("NFC", text or ""):
        o = ord(ch)
        is_flag = 0x1F1E6 <= o <= 0x1F1FF
        attach = bool(out) and (_mark(ch) or ch in "‍️︎⃣" or 0x1F3FB <= o <= 0x1F3FF
                                or 0xE0020 <= o <= 0xE007F or out[-1].endswith("‍") or (is_flag and flag))
        if attach:
            out[-1] += ch
        else:
            out.append(ch)
        flag = is_flag and not flag
    return out


def _x_units(part):
    """X's weighted length of text without links: most Latin, Greek, Cyrillic, Arabic, Hebrew, Thai
    and Indian letters count 1; Chinese, Japanese, Korean and emoji count 2 (a joined emoji is 2)."""
    n = 0
    for c in clusters(part):
        if any(_emoji(ch) for ch in c):
            n += 2
            continue
        for ch in c:
            o = ord(ch)
            n += 1 if (o <= 0x10FF or 0x2000 <= o <= 0x200D or 0x2010 <= o <= 0x201F or 0x2032 <= o <= 0x2037) else 2
    return n


def text_length(platform, text):
    """(length the way this platform counts it, True when that count is approximate).
    The check and the number on the plan page both come from here."""
    text = text or ""
    if platform == "YOUTUBE":
        return len(text.encode("utf-8", "surrogatepass")), False
    if platform == "TIKTOK":   # UTF-16 units: most emoji count 2
        return len(text.encode("utf-16-le", "surrogatepass")) // 2, False
    joined = any(len(c) > 1 for c in clusters(text))
    if platform == "X":        # every link counts 23, wide characters and emoji 2
        n, pos = 0, 0
        t = unicodedata.normalize("NFC", text)
        for m in URL_RE.finditer(t):
            link = m.group(0).rstrip(".,;:!?)]}\"'")
            n += _x_units(t[pos:m.start()]) + 23
            pos = m.start() + len(link)
        return n + _x_units(t[pos:]), joined
    if platform == "BLUESKY":  # characters as a reader sees them
        return len(clusters(text)), joined
    return len(text), False


def tags_length(tags):
    """YouTube's count for hidden tags: commas between them, and a tag with a space counts 2 more
    (YouTube wraps it in quotes)."""
    return sum(len(t) + (2 if " " in t else 0) for t in tags) + max(len(tags) - 1, 0)
