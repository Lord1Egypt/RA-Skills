"""Shared helpers for the clipping agency scripts: files, video probing, each platform's limits, text
rules, time zones, the client files, the batch fingerprint and the one ledger shared by every client.
Standard library only."""
import datetime, functools, hashlib, json, os, re, subprocess, sys, unicodedata

try:  # Windows consoles default to cp1252; captions are often not Latin
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
               "fps": (23, 60), "max_side": 4096, "min_side": 360},
    "INSTAGRAM": {"label": "Instagram Reels", "min_s": 3, "max_s": 900, "bytes": 300 * MB, "text": 2200,
                  "fps": (23, 60), "max_width": 1920, "tags_max": 5, "strict": True},
    "YOUTUBE": {"label": "YouTube Shorts", "min_s": 1, "max_s": 180, "bytes": 256 * GB,
                "text_bytes": 5000, "title": 100},
}
PLATFORMS = tuple(LIMITS)
TIKTOK_PRIVACY = ("PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS", "FOLLOWER_OF_CREATOR", "SELF_ONLY")
TIKTOK_DAILY_CAP = 15   # TikTok takes about 15 direct posts a day per creator account through its posting API
HDR_TRANSFER = ("smpte2084", "arib-std-b67")
WINDOWS_RESERVED = {"con", "prn", "aux", "nul"} | {f"com{n}" for n in range(1, 10)} | {f"lpt{n}" for n in range(1, 10)}

_reading = [None]   # the file being read, for the last-resort message in guard()


def reading(path):
    _reading[0] = path


def die(msg):
    raise SystemExit("error: " + msg)


def guard(main):
    """Run a script's main(): any unexpected error becomes one clear line, not a traceback.
    Set AGENCY_DEBUG=1 to see the traceback."""
    try:
        main()
    except SystemExit:
        raise
    except KeyboardInterrupt:
        sys.exit("stopped. Run the same command again when you are ready")
    except Exception as e:
        if os.environ.get("AGENCY_DEBUG"):
            raise
        if isinstance(e, UnicodeEncodeError):
            sys.exit("error: a text holds half an emoji or a broken character (a cut-off copy). Retype that text")
        if isinstance(e, OSError):
            name = rel(str(e.filename)) if e.filename else "a file"
            sys.exit(f"error: can't read or write {name}: {e.strerror or e}. Check that it exists, that you "
                     "may write to that folder, and that no file there has the name of a folder this needs")
        where = (rel(str(_reading[0])) if _reading[0] else
                 "one of the files you gave (client.json, batch.json or a saved reply)")
        sys.exit(f"error: {where} has a value of the wrong kind somewhere (text where a number belongs, a list "
                 f"where one value belongs, or the reverse): {type(e).__name__}: {e}. "
                 "Set AGENCY_DEBUG=1 for details.")


def read_json(path, what=None):
    reading(path)
    try:
        with open(path, encoding="utf-8-sig") as fh:
            data = json.load(fh)
        reading(None)   # read cleanly: a later wrong value is not this file's fault
        return data
    except FileNotFoundError:
        die(f"{path} not found" + (f" ({what})" if what else ""))
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


def _mark(ch):
    return unicodedata.category(ch).startswith("M")


def slug(text):
    """A safe file name from any text: letters and digits of every script, lowercase, the rest
    becomes one dash."""
    out = []
    for ch in unicodedata.normalize("NFC", str(text)).lower():
        if ch.isalnum() or (out and out[-1] != "-" and _mark(ch)):
            out.append(ch)
        elif out and out[-1] != "-":
            out.append("-")
    s = "".join(out)[:80].strip("-")
    if not s:
        s = "x" + hashlib.sha1(str(text).encode("utf-8", "surrogatepass")).hexdigest()[:8]
    if s in WINDOWS_RESERVED:
        s += "-1"
    return s


def valid_id(text):
    """An id: lowercase letters and digits, single dashes between them, 80 at most."""
    return isinstance(text, str) and unicodedata.normalize("NFC", text) == slug(text)


@functools.lru_cache(maxsize=None)
def _sha256_cached(path, size, mtime):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def sha256(path):
    """The file's fingerprint: two files with the same one are the same edit, whatever their names."""
    st = os.stat(path)
    return _sha256_cached(os.path.abspath(path), st.st_size, st.st_mtime)


def need_ffmpeg():
    import shutil
    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        die("ffmpeg not found. Mac: brew install ffmpeg. Windows: winget install Gyan.FFmpeg (then open a "
            "new terminal). Linux: sudo apt install ffmpeg")


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


def probe(path, label=None):
    """Width and height as displayed (after rotation), fps, duration, codecs, colour, sound, size."""
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
    if fps > 1000:
        fps = 0.0
    dur = 0.0
    for src in ((d.get("format") or {}).get("duration"), v.get("duration")):
        try:
            dur = float(src)
            break
        except (TypeError, ValueError):
            continue
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
    return {"width": w, "height": h, "fps": round(fps, 3), "duration": round(max(dur, 0.0), 3),
            "rate": v.get("r_frame_rate") or "30/1", "vcodec": v.get("codec_name"), "pix_fmt": v.get("pix_fmt"), "transfer": v.get("color_transfer"),
            "acodec": a.get("codec_name"), "audio": bool(aus), "audio_rate": a_rate, "channels": channels,
            "bytes": size, "mbps": round(size * 8 / dur / 1e6, 2) if dur else 0.0,
            "mp4": any(x in fmt for x in ("mp4", "mov")), "moov_first": moov_first(path)}


def size_text(n):
    return f"{n / GB:g} GB" if n >= GB and n % GB == 0 else f"{n / MB:.1f} MB"


def file_issues(info, platform, tiktok_max_s=None):
    """Problems one platform has with this file: a list of (level, message)."""
    L = LIMITS[platform]
    name = L["label"]
    out = []
    s, w, h = info["duration"], info["width"], info["height"]
    max_s = float(tiktok_max_s) if platform == "TIKTOK" and tiktok_max_s else L["max_s"]
    if not s:
        out.append(("error", "can't read this file's length; export it again as MP4"))
    elif s < L["min_s"]:
        out.append(("error", f"{s:.1f} s is shorter than the {name} minimum of {L['min_s']} s"))
    if platform == "YOUTUBE":
        if s > max_s or w > h:
            why = f"{s:.0f} s is over 3 minutes" if s > max_s else f"{w}x{h} is wider than it is tall"
            out.append(("error", f"{why}, so YouTube would publish it as a normal video, not a Short"))
    elif s > max_s:
        out.append(("error", f"{s:.0f} s is over the {name} limit of {max_s:.0f} s"))
    if info["bytes"] > L["bytes"]:
        out.append(("error", f"{size_text(info['bytes'])} is over the {name} limit of {size_text(L['bytes'])}"))
    fps = L.get("fps")
    if fps and info["fps"] and not fps[0] - 0.1 <= info["fps"] <= fps[1] + 0.5:
        out.append(("error", f"{info['fps']:g} frames a second; {name} accepts {fps[0]} to {fps[1]}"))
    if L.get("max_width") and w > L["max_width"]:
        out.append(("error", f"{w} px wide; {name} accepts up to {L['max_width']} px"))
    if L.get("max_side") and max(w, h) > L["max_side"]:
        out.append(("error", f"{w}x{h}; {name} accepts up to {L['max_side']} px per side"))
    if L.get("min_side") and min(w, h) < L["min_side"]:
        out.append(("error", f"{w}x{h}; {name} needs at least {L['min_side']} px per side"))
    if info["vcodec"] != "h264" and not (info["vcodec"] == "hevc" and not L.get("strict")):
        out.append(("error" if L.get("strict") else "warning",
                    f"video codec is {info['vcodec']}; H.264 is the one every platform takes"))
    if info["pix_fmt"] and not info["pix_fmt"].startswith(("yuv420p", "yuvj420p")):
        out.append(("error" if L.get("strict") else "warning", f"pixel format {info['pix_fmt']}; platforms expect yuv420p"))
    if info["transfer"] in HDR_TRANSFER:
        out.append(("error" if L.get("strict") else "warning", "HDR video; it can be rejected or look washed out"))
    if L.get("strict"):
        if not info["mp4"]:
            out.append(("error", f"{name} takes MP4 or MOV files only"))
        elif info["moov_first"] is False:
            out.append(("error", f"the file's index is at the end; {name} needs it at the start (\"fast start\")"))
        if info["audio"] and info["acodec"] != "aac":
            out.append(("error", f"audio codec is {info['acodec']}; {name} needs AAC"))
        if info["audio_rate"] > 48000:
            out.append(("error", f"audio is {info['audio_rate']} Hz; {name} accepts up to 48,000 Hz"))
        if info["mbps"] > 25:
            out.append(("error", f"{info['mbps']:g} Mbps; {name} accepts up to 25 Mbps"))
    if not info["audio"]:
        out.append(("warning", "no sound track"))
    return out


# ---- text: hashtags, handles, links and each platform's way of counting

URL_RE = re.compile(r"(?i:https?://|www\.)\S+"
                    r"|(?<![@\w.-])[A-Za-z0-9-]+\.(?:com|net|org|io|co|app|ai|dev|shop|store|me|ly|gg|tv)(?![A-Za-z0-9])(?:/\S*)?")


def hashtags(text):
    """Hashtags as the platforms read them: a # followed by letters or digits with at least one letter."""
    return [h for h in re.findall(r"(?<![\w&])#\w+", text or "") if any(c.isalpha() for c in h)]


def mentions(text):
    return re.findall(r"(?<![\w@.])@[A-Za-z0-9_](?:[A-Za-z0-9_.]*[A-Za-z0-9_])?", text or "")


def links(text):
    return [m.group(0).rstrip(".,;:!?)]}\"'") for m in URL_RE.finditer(text or "")]


def norm_link(u):
    """A link without scheme, www, case and trailing slash, so example.com/x and https://www.example.com/x/ match."""
    u = re.sub(r"(?i)^https?://", "", (u or "").strip())
    u = re.sub(r"(?i)^www\.", "", u)
    return u.rstrip("/").lower()


# Share-menu links carry tracking parameters (?igsh=, ?si=, ?is_from_webapp=1&sender_device=pc, utm_...).
TRACKING = re.compile(r"^(?:utm_\w*|igsh|igshid|si|is_from_webapp|sender_device|sender_web_id|_t|_r|_d|feature|"
                      r"share_\w*|ref|refer|referrer|source|web_id|tt_from|u_code|preview_pb|checksum|sec_uid|"
                      r"lang|embed_source|fbclid|gclid|mibextid|rdid|img_index|pp|app|t)$", re.I)


def post_key(url):
    """One key per post, whatever link the app's share menu gave: "TIKTOK:<video id>",
    "INSTAGRAM:<shortcode>", "YOUTUBE:<video id>", or for other links the host and path without
    tracking parameters. Ids keep their case (they are case-sensitive). A TikTok short link
    (vm.tiktok.com, /t/) gives "TIKTOK-SHORT:<code>": it can't be matched to a post, so ask for the
    full link."""
    import urllib.parse
    u = (url or "").strip()
    if not u:
        return ""
    if not re.match(r"(?i)^[a-z]+://", u):
        u = "https://" + u
    try:
        p = urllib.parse.urlsplit(u)
    except ValueError:
        return "URL:" + u
    host = (p.hostname or "").lower()
    bare = re.sub(r"^(?:www|m|mobile|web)\.", "", host)
    path = re.sub(r"/{2,}", "/", p.path or "/")
    if bare.endswith("tiktok.com"):
        if bare.startswith(("vm.", "vt.")) or path.startswith("/t/"):
            return "TIKTOK-SHORT:" + path.strip("/").split("/")[-1]
        m = re.search(r"/(?:video|photo|v)/([A-Za-z0-9_-]+)", path)
        if m:
            return "TIKTOK:" + m.group(1)
    if bare.endswith("instagram.com"):
        m = re.search(r"/(?:reels?|p|tv)/([A-Za-z0-9_-]+)", path)
        if m:
            return "INSTAGRAM:" + m.group(1)
    if bare == "youtu.be":
        vid = path.strip("/").split("/")[0]
        if vid:
            return "YOUTUBE:" + vid
    if bare.endswith("youtube.com"):
        m = re.search(r"/(?:shorts|live|embed|v)/([A-Za-z0-9_-]+)", path)
        if m:
            return "YOUTUBE:" + m.group(1)
        q = urllib.parse.parse_qs(p.query)
        if q.get("v"):
            return "YOUTUBE:" + q["v"][0]
    kept = [(k, v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True) if not TRACKING.match(k)]
    tail = ("?" + urllib.parse.urlencode(sorted(kept))) if kept else ""
    return "URL:" + bare + path.rstrip("/") + tail


def short_link(url):
    """True for a share link that hides the post id (vm.tiktok.com/..., tiktok.com/t/...)."""
    return post_key(url).startswith("TIKTOK-SHORT:")


def text_length(platform, text):
    """Length the way this platform counts it."""
    text = text or ""
    if platform == "YOUTUBE":
        return len(text.encode("utf-8", "surrogatepass"))
    if platform == "TIKTOK":   # UTF-16 units: most emoji count 2
        return len(text.encode("utf-16-le", "surrogatepass")) // 2
    return len(text)


def find_phrases(text, patterns):
    """Every match of these patterns in a text: (the sentence it is in, the words that matched)."""
    hits = []
    flat = re.sub(r"[‘’]", "'", text or "")
    for pat in patterns:
        for m in re.finditer(pat, flat, flags=re.I):
            start = max(flat.rfind(".", 0, m.start()), flat.rfind("\n", 0, m.start())) + 1
            ends = [i for i in (flat.find(".", m.end()), flat.find("\n", m.end())) if i != -1]
            end = min(ends) + 1 if ends else len(flat)
            sentence = " ".join(flat[start:end].split()).lstrip("-*•> ").strip()
            if sentence not in (h[0] for h in hits):   # one line per sentence, however many patterns match it
                hits.append((sentence, m.group(0)))
    return hits

# ---- time ranges in the source video

def ranges_total(ranges):
    return sum(max(0.0, b - a) for a, b in ranges)


def overlap_seconds(r1, r2):
    """Seconds of the source that two edits share."""
    return sum(max(0.0, min(b1, b2) - max(a1, a2)) for a1, b1 in r1 for a2, b2 in r2)


def overlap_share(r1, r2):
    """The part of the shorter edit that the other edit also uses (0 to 1)."""
    shorter = min(ranges_total(r1), ranges_total(r2))
    return overlap_seconds(r1, r2) / shorter if shorter > 0 else 0.0


def clean_ranges(value):
    """[[start, end], ...] in seconds, or None when the value isn't that."""
    if not isinstance(value, list) or not value:
        return None
    out = []
    for r in value:
        if (not isinstance(r, (list, tuple)) or len(r) != 2
                or not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in r) or r[1] <= r[0] or r[0] < 0):
            return None
        out.append((float(r[0]), float(r[1])))
    return out


def stamp(t):
    m, s = divmod(float(t), 60)
    return f"{int(m)}:{s:04.1f}"


# ---- time and money

def now_utc():
    """The clock the scripts use. AGENCY_NOW (an ISO time) fixes it for examples and tests."""
    fixed = os.environ.get("AGENCY_NOW")
    if fixed:
        t = parse_time(fixed)
        if t:
            return t
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)


def _iso_clean(text):
    t = re.sub(r"\.\d+", "", text.strip())
    t = re.sub(r"^(\d{4}-\d{2}-\d{2}) (\d)", r"\1T\2", t)
    t = re.sub(r"[Zz]$", "+00:00", t)
    return re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", t)   # +0100 -> +01:00 (Python 3.9 needs the colon)


def parse_time(text):
    """A stored ISO 8601 time ("2026-11-15T14:03:00Z" or with an offset; without one, UTC). None if not."""
    if not isinstance(text, str) or not text.strip():
        return None
    try:
        d = datetime.datetime.fromisoformat(_iso_clean(text))
    except ValueError:
        return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=datetime.timezone.utc)
    return d.astimezone(datetime.timezone.utc)


def load_zone(zone):
    """The ZoneInfo for an IANA name, or None when this computer can't load it (Windows needs
    pip install tzdata)."""
    if not zone or not isinstance(zone, str):
        return None
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(zone)
    except Exception:
        return None


def parse_user_time(text, zone=None):
    """A time the user typed: (time in UTC, the zone it was read in when it had no offset, problem).
    A time without an offset is the user's own clock time: read in `zone` (the job's timezone),
    else in this computer's zone. A date alone is refused (it would be midnight)."""
    if not isinstance(text, str) or not text.strip():
        return None, None, "give a time like 2026-11-16T09:05 (your clock) or 2026-11-16T14:05Z (UTC)"
    if re.fullmatch(r"\s*\d{4}-\d{2}-\d{2}\s*", text):
        return None, None, "give the time of day too, like 2026-11-16T09:05; a date alone would be read as midnight"
    try:
        d = datetime.datetime.fromisoformat(_iso_clean(text))
    except ValueError:
        return None, None, "give a time like 2026-11-16T09:05 (your clock) or 2026-11-16T14:05Z (UTC)"
    assumed = None
    if d.tzinfo is None:
        tz = load_zone(zone)
        if tz is not None:
            d, assumed = d.replace(tzinfo=tz), zone
        else:
            d = d.astimezone()   # this computer's own zone
            assumed = "this computer's time zone (" + (d.strftime("%Z") or "local") + ")"
    return d.astimezone(datetime.timezone.utc), assumed, None


def iso(t):
    return t.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def client_clock(t, zone=None):
    """A time as a client reads it: 'Wed 07 Oct, 18:00 New York time (EDT)'."""
    tz = load_zone(zone)
    if tz is None:
        return t.astimezone(datetime.timezone.utc).strftime("%a %d %b, %H:%M UTC")
    t = t.astimezone(tz)
    abbr = t.strftime("%Z")
    city = str(zone).split("/")[-1].replace("_", " ")
    return t.strftime("%a %d %b, %H:%M ") + f"{city} time" + (f" ({abbr})" if abbr and abbr != zone and not abbr.startswith(("+", "-")) else "")


def plural(n, word, many=None):
    """'1 clip', '3 clips'."""
    return f"{n} {word if n == 1 else (many or word + 's')}"


def read_text(path):
    """A saved reply as text, whatever encoding a mail app or editor saved it in (UTF-8, UTF-16 with its
    mark, Windows-1252)."""
    with open(path, "rb") as fh:
        raw = fh.read()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16")
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    die(f"couldn't read the text encoding of {path}. Save the reply as plain text (UTF-8) and try again")


def clock(t, zone=None):
    """A time as people read it: 'Mon 16 Nov 09:31 America/New_York (EST)', or in UTC when the zone
    is unknown. The abbreviation tells EDT from EST on the night the clocks go back."""
    tz = load_zone(zone)
    if tz is None:
        return t.astimezone(datetime.timezone.utc).strftime("%a %d %b %H:%M UTC")
    t = t.astimezone(tz)
    abbr = t.strftime("%Z")
    return t.strftime("%a %d %b %H:%M ") + zone + (f" ({abbr})" if abbr and abbr != zone else "")


def is_num(v, minimum=None):
    """A real, finite number (not true/false, not Infinity or NaN)."""
    import math
    ok = isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
    return ok and (minimum is None or v >= minimum)

def unwrap_reply(data):
    """A tool reply saved as the MCP envelope ({"content": [{"type": "text", "text": "{...json...}"}]})
    becomes the JSON inside it. Anything else comes back as it was."""
    if isinstance(data, dict) and isinstance(data.get("content"), list) and not data.get("socialAccountPosts"):
        parsed = []
        for part in data["content"]:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                try:
                    v = json.loads(part["text"])
                except ValueError:
                    continue
                if isinstance(v, (dict, list)):
                    parsed.append(v)
        if len(parsed) == 1:
            return parsed[0]
        if parsed:
            return parsed
    return data

def placeholder_id(sid):
    s = str(sid).strip().lower()
    return s.startswith("<") or s in ("", "id", "...", "socialaccountid", "todo") or s.startswith(("your", "xxx"))


def post_items(data, depth=0):
    """Every per-post entry in a saved WoopSocial reply (posts_get, social_account_posts_list or
    social_account_posts_list_analytics), wherever the reply nests them: the dicts that carry an
    externalPostUrl or a socialAccountId with a delivery status or metrics."""
    found = []
    if depth > 6:
        return found
    if isinstance(data, list):
        for x in data:
            found += post_items(x, depth + 1)
    elif isinstance(data, dict):
        if isinstance(data.get("externalPostUrl"), str) or (
                isinstance(data.get("socialAccountId"), str) and ("deliveryStatus" in data or "metrics" in data)):
            found.append(data)
        else:
            for v in data.values():
                if isinstance(v, (list, dict)):
                    found += post_items(v, depth + 1)
    return found


# ---- the agency's own files: one ledger for every client, whatever folder each client lives in

def user_home():
    """Where the ledger lives: CLIPPING_AGENCY_HOME, else ~/.clipping-agency (the .clipping-agency folder
    in the user's home folder, on Windows too)."""
    home = os.environ.get("CLIPPING_AGENCY_HOME")
    return os.path.abspath(os.path.expanduser(home)) if home else os.path.join(os.path.expanduser("~"), ".clipping-agency")


def ledger_path(override=None):
    """The one ledger of every clip handed to a client and every post: --ledger, else
    CLIPPING_AGENCY_LEDGER, else <user_home>/ledger.json. One file is what lets the skill refuse a clip
    file that already went to another client, or an account that belongs to another client."""
    p = override or os.environ.get("CLIPPING_AGENCY_LEDGER")
    return os.path.abspath(os.path.expanduser(p)) if p else os.path.join(user_home(), "ledger.json")


_LOADED = {}   # ledger path -> fingerprint of the file as it was read, so a save can't drop another session's write


def _file_fp(path):
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except FileNotFoundError:
        return None


def load_ledger(path=None):
    """ledger.json: {"clips": {"<sha256>": {client, episode, clip, at}}, "accounts": {"<socialAccountId>":
    "<client id>"}, "posts": {"<postId>|<socialAccountId>": {...}}}. A damaged file is an error and is left
    exactly as it is: it may be the only record of what went out."""
    path = path or ledger_path()
    _LOADED[os.path.abspath(path)] = _file_fp(path)
    if not os.path.exists(path):
        return {"clips": {}, "accounts": {}, "posts": {}, "planned": {}}
    data = read_json(path, "the ledger")
    if (not isinstance(data, dict)
            or not all(isinstance(data.get(k, {}), dict) for k in ("clips", "accounts", "posts"))
            or not all(isinstance(v, dict) for v in data.get("posts", {}).values())
            or not all(isinstance(v, dict) for v in data.get("clips", {}).values())):
        die(f"the ledger ({rel(path)}) is damaged: it must hold \"clips\", \"accounts\" and \"posts\". It was left as "
            "it is. Repair it, or move it away if nothing in it was really scheduled or posted")
    for k in ("clips", "accounts", "posts", "planned"):
        data.setdefault(k, {})
    if not isinstance(data["planned"], dict):
        data["planned"] = {}
    reading(None)
    return data


def save_ledger(path, data):
    """Write the ledger under a lock file. When another session wrote it after this one read it,
    nothing is written: run the command again, it reads the new ledger first."""
    import time
    path = os.path.abspath(path or ledger_path())
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lock = path + ".lock"
    for _ in range(100):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(lock) > 60:   # left behind by a script that was stopped
                    os.remove(lock)
                    continue
            except OSError:
                pass
            time.sleep(0.1)
    else:
        die(f"the ledger ({rel(path)}) is being written by another session. Wait a moment and run this again")
    try:
        if path in _LOADED and _file_fp(path) != _LOADED[path]:
            die(f"the ledger ({rel(path)}) changed while this ran (another session wrote to it). Nothing was written; "
                "run the same command again")
        write_json(path, data)
        _LOADED[path] = _file_fp(path)
    finally:
        try:
            os.remove(lock)
        except OSError:
            pass


# ---- clients and their folders

DAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
CLIENT_STATUS = ("active", "paused", "offboarding", "offboarded")
GUEST_RELEASE_EPISODE = ("on_file", "not_needed", "missing", "unknown")
APPROVAL_RULES = ("hold", "auto_after_hours")
YT_PRIVACY = ("public", "unlisted", "private")
MIN_LEAD_HOURS = 1.0      # never schedule sooner than this: time to cancel a post if something changes
MIN_SEND_MINUTES = 30     # a request is never sent when its time is closer than this
MIN_CLIPS, MAX_CLIPS = 3, 12
HEX = re.compile(r"#[0-9A-Fa-f]{6}")
HHMM = re.compile(r"([01]\d|2[0-3]):([0-5]\d)")
VIEW_MEANS = {"TIKTOK": "plays of the video", "YOUTUBE": "plays of the Short",
              "INSTAGRAM": "times the Reel was shown, repeats included"}


def workspace_of(path):
    """The agency's folder: the one holding clients/. Found by walking up from a file or folder inside it."""
    d = os.path.abspath(path if os.path.isdir(path) else os.path.dirname(os.path.abspath(path)))
    while True:
        if os.path.basename(d) == "clients" and os.path.isdir(d):
            return os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "clients")):
            return d
        up = os.path.dirname(d)
        if up == d:
            return None
        d = up


def client_dir(workspace, cid):
    return os.path.join(workspace, "clients", cid)


def client_ids(workspace):
    root = os.path.join(workspace, "clients")
    if not os.path.isdir(root):
        return []
    return sorted(d for d in os.listdir(root) if os.path.isfile(os.path.join(root, d, "client.json")))


def read_client(workspace, cid):
    path = os.path.join(client_dir(workspace, cid), "client.json")
    if not os.path.isfile(path):
        known = ", ".join(client_ids(workspace)) or "none yet"
        die(f"no client \"{cid}\" (clients/{cid}/client.json). Clients here: {known}")
    c = read_json(path, "the client file")
    if not isinstance(c, dict):
        die(f"clients/{cid}/client.json must hold one JSON object")
    reading(path)
    return c


def accounts_of(c):
    """{platform: account dict} from the client's woopsocial.accounts."""
    ws = c.get("woopsocial") if isinstance(c.get("woopsocial"), dict) else {}
    accs = ws.get("accounts") if isinstance(ws.get("accounts"), dict) else {}
    return {p.upper(): a for p, a in accs.items() if isinstance(p, str) and isinstance(a, dict)}


def connected_id(acc):
    sid = acc.get("socialAccountId") if isinstance(acc, dict) else None
    return sid.strip() if isinstance(sid, str) and sid.strip() and not placeholder_id(sid) else None


def account_owner(workspace, sid, ledger=None):
    """Every client that names this socialAccountId: in its client.json, and in the ledger."""
    owners = set()
    for cid in client_ids(workspace):
        try:
            c = read_json(os.path.join(client_dir(workspace, cid), "client.json"))
        except SystemExit:
            continue
        if isinstance(c, dict) and any(connected_id(a) == sid for a in accounts_of(c).values()):
            owners.add(cid)
    if ledger and ledger.get("accounts", {}).get(sid):
        owners.add(ledger["accounts"][sid])
    reading(None)
    return owners


def names_fix(text, names):
    """Apply the client's names dictionary to a text: every listed wrong spelling, and the right one in
    the wrong case, becomes the right spelling. Returns (text, [(found, right), ...])."""
    fixes = []
    if not isinstance(names, dict):
        return text, fixes
    for right, wrongs in names.items():
        if not isinstance(right, str) or not right.strip():
            continue
        variants = [w for w in (wrongs if isinstance(wrongs, list) else []) if isinstance(w, str) and w.strip()]
        for v in sorted(set(variants + [right]), key=len, reverse=True):
            pat = re.compile(r"(?<![\w])" + r"\s+".join(re.escape(x) for x in v.split()) + r"(?![\w])", re.I)

            def sub(m):
                if m.group(0) != right:
                    fixes.append((m.group(0), right))
                return right
            text = pat.sub(sub, text)
    return text, fixes


def wrong_names(text, names):
    """Listed wrong spellings (not the right one in another case) that a text contains."""
    found = []
    if not isinstance(names, dict):
        return found
    for right, wrongs in names.items():
        for v in (wrongs if isinstance(wrongs, list) else []):
            if isinstance(v, str) and v.strip() and v.casefold() != str(right).casefold():
                pat = r"(?<![\w])" + r"\s+".join(re.escape(x) for x in v.split()) + r"(?![\w])"
                if re.search(pat, text or "", re.I):
                    found.append((v, right))
    return found


def topic_hits(text, topics):
    """No-go topics (words or phrases) that a text mentions."""
    out = []
    for t in topics if isinstance(topics, list) else []:
        if isinstance(t, str) and t.strip():
            pat = r"(?<![\w])" + r"\s+".join(re.escape(x) for x in t.split()) + r"\w{0,3}(?![\w])"
            if re.search(pat, text or "", re.I):
                out.append(t)
    return out


DISCLOSURE_WORDS = re.compile(r"(?i)(?:#ad\b|#sponsored\b|#paidpartnership\b|\bpaid partnership\b|\bsponsored by\b|"
                              r"\bin partnership with\b|\bad:)")
SPONSOR_READ = re.compile(r"(?i)\b(?:sponsored by|brought to you by|promo code|use (?:the )?code|discount code|"
                          r"affiliate link|today'?s sponsor|our sponsor|this episode is supported by)\b")


# ---- the batch: an episode's clips, and the fingerprint the client's approval is bound to

def captions_of(clip):
    caps = clip.get("captions") if isinstance(clip.get("captions"), dict) else {}
    return {p.upper(): t for p, t in caps.items() if isinstance(p, str) and isinstance(t, str)}


def clip_hash(file_sha, clip):
    """One fingerprint for what the client approves for one clip: the video file and every word that goes
    out with it (each platform's caption, the YouTube title and tags). Change any of it and the approval
    no longer matches."""
    caps = captions_of(clip)
    body = {"file": file_sha, "captions": {p: caps[p] for p in sorted(caps)}, "title": clip.get("title") or "",
            "tags": clip.get("tags") if isinstance(clip.get("tags"), list) else [],
            "promotes_client_business": clip.get("promotes_client_business") is True}
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()


CUT_KEYS = ("start", "end", "hook", "reframe", "focus_x", "zoom", "cut", "tighten", "fillers", "snap", "facecam", "game",
            "shots", "track", "speakers", "punch", "hook_at", "logo_at")


def cut_spec(clip):
    """A fingerprint of what make_clips.py cuts from: the times, the hook burned in, the framing. A clip whose
    batch entry changed after it was cut no longer matches its file."""
    body = {k: clip.get(k) for k in CUT_KEYS if clip.get(k) is not None}
    for k in ("start", "end"):
        if is_num(body.get(k)):
            body[k] = round(float(body[k]), 2)
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]


def batch_fp(client_id, episode_id, hashes):
    """The batch fingerprint: client, episode and every clip's fingerprint in order."""
    body = json.dumps([client_id, episode_id, [[k, h] for k, h in hashes]], ensure_ascii=False)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


PRIV_WORDS = {"PUBLIC_TO_EVERYONE": "everyone", "FOLLOWER_OF_CREATOR": "followers",
              "MUTUAL_FOLLOW_FRIENDS": "friends", "SELF_ONLY": "only me"}


def local_day(t, zone):
    tz = load_zone(zone)
    return (t.astimezone(tz) if tz else t).date()


# ---- the schedule: the client's days and times, in the client's time zone

def cadence_of(c):
    cad = c.get("cadence") if isinstance(c.get("cadence"), dict) else {}
    days = [d.lower()[:3] for d in cad.get("days") or [] if isinstance(d, str) and d.lower()[:3] in DAYS]
    times = sorted(t for t in cad.get("times") or [] if isinstance(t, str) and HHMM.fullmatch(t))
    mpd = cad.get("max_per_day", 1)
    mpd = mpd if isinstance(mpd, int) and not isinstance(mpd, bool) and mpd >= 1 else 1
    gap = cad.get("min_gap_hours", 3)
    lead = cad.get("start_after_hours", 2)
    lead = max(float(lead), MIN_LEAD_HOURS) if is_num(lead, 0) else 2.0
    return {"days": days or list(DAYS[:5]), "times": times or ["12:00"], "max_per_day": min(mpd, TIKTOK_DAILY_CAP),
            "min_gap_hours": float(gap) if is_num(gap, 0) else 3.0, "start_after_hours": lead}


def plan_slots(c, count, busy=(), tiktok_busy=(), now=None, not_before=None, horizon_days=180):
    """`count` posting times (UTC) for one client: on the client's days, at the client's clock times in
    the client's time zone (daylight saving included), at most max_per_day a day, at least min_gap_hours
    from each other and from every time already in `busy` (the client's scheduled and live posts), never
    sooner than start_after_hours from now nor before `not_before`, and with fewer than TikTok's daily cap
    of posts on the client's TikTok account on any day (`tiktok_busy`)."""
    tz = load_zone(c.get("timezone"))
    if tz is None:
        die(f"client {c.get('id')}: the time zone {c.get('timezone')!r} can't be loaded (on Windows: pip install tzdata)")
    cad = cadence_of(c)
    now = now or now_utc()
    start = now + datetime.timedelta(hours=cad["start_after_hours"])
    if not_before and not_before > start:
        start = not_before
    taken = sorted(busy)
    per_day, tt_day = {}, {}
    for t in taken:
        d = t.astimezone(tz).date()
        per_day[d] = per_day.get(d, 0) + 1
    for t in tiktok_busy:
        d = t.astimezone(tz).date()
        tt_day[d] = tt_day.get(d, 0) + 1
    gap = datetime.timedelta(hours=cad["min_gap_hours"])
    out = []
    day = start.astimezone(tz).date()
    for _ in range(horizon_days):
        if DAYS[day.weekday()] in cad["days"]:
            for hm in cad["times"]:
                if len(out) >= count:
                    return out
                h, m = map(int, hm.split(":"))
                local = datetime.datetime(day.year, day.month, day.day, h, m, tzinfo=tz)
                t = local.astimezone(datetime.timezone.utc)
                back = t.astimezone(tz)
                if (back.hour, back.minute) != (h, m):   # a clock time that doesn't exist that night (clocks go forward)
                    t = (local + datetime.timedelta(hours=1)).astimezone(datetime.timezone.utc)
                if t < start or per_day.get(day, 0) >= cad["max_per_day"] or tt_day.get(day, 0) >= TIKTOK_DAILY_CAP:
                    continue
                if any(abs(t - x) < gap for x in taken + out):
                    continue
                out.append(t)
                per_day[day] = per_day.get(day, 0) + 1
                tt_day[day] = tt_day.get(day, 0) + 1
        day += datetime.timedelta(days=1)
    return out


def client_busy(ledger, cid, account_id=None, exclude_episode=None):
    """(times of this client's scheduled, live or planned posts, one per post; times of posts on one
    account). Planned slots are those of requests written but not yet sent, for other episodes than
    `exclude_episode` (the one being planned again)."""
    busy, acct = {}, []
    for k, e in ledger.get("posts", {}).items():
        if e.get("status") in ("cancelled", "failed"):
            continue
        t = parse_time(e.get("scheduledFor") or e.get("deliveryCompletedAt"))
        if not t:
            continue
        if e.get("client") == cid:
            busy[k.split("|")[0]] = t
        if account_id and k.split("|")[-1] == account_id:
            acct.append(t)
    for k, e in (ledger.get("planned") or {}).items():
        if not isinstance(e, dict) or e.get("client") != cid or e.get("episode") == exclude_episode:
            continue
        t = parse_time(e.get("scheduledFor"))
        if t:
            busy["planned:" + k] = t
            if account_id and account_id in (e.get("accounts") or []):
                acct.append(t)
    return sorted(busy.values()), acct


def postable_id(acc):
    """The account id to post to: connected, and not marked by WoopSocial as needing a new link."""
    sid = connected_id(acc)
    if sid and str(acc.get("status") or "CONNECTED").upper() == "CONNECTED":
        return sid
    return None


def clear_requests(bdir, ledger=None, cid=None, episode=None):
    """Remove the send requests schedule.py wrote for an episode (and their planned slots in the ledger),
    so a request written for an earlier state can never be sent. Cancel notes stay. Returns the names
    removed. The caller saves the ledger."""
    rdir = os.path.join(bdir, "requests")
    idx = os.path.join(rdir, "index.json")
    removed = []
    if os.path.isfile(idx):
        try:
            names = read_json(idx).get("requests", {})
        except (SystemExit, AttributeError):
            names = {}
        reading(None)
        for n in names:
            p = os.path.join(rdir, os.path.basename(n))
            if os.path.isfile(p):
                os.remove(p)
                removed.append(os.path.basename(n))
        os.remove(idx)
    if ledger is not None and cid:
        for k in [k for k, e in ledger.get("planned", {}).items()
                  if isinstance(e, dict) and e.get("client") == cid and (episode is None or e.get("episode") == episode)]:
            del ledger["planned"][k]
    return removed
