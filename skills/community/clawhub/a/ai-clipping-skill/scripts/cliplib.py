"""Shared helpers for the AI clipping scripts: files, video probing, each platform's limits, text
rules, overlap of source time ranges, and the phrases that are never followed. Standard library only."""
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
HDR_TRANSFER = ("smpte2084", "arib-std-b67")
WINDOWS_RESERVED = {"con", "prn", "aux", "nul"} | {f"com{n}" for n in range(1, 10)} | {f"lpt{n}" for n in range(1, 10)}
SUBMIT_MINUTES = 30      # most campaigns take a post only when it is submitted within 30 minutes of going live
DEFAULT_WINDOW_DAYS = 30
DEFAULT_FEE_PCT = 10.0
DEFAULT_MAX_OVERLAP = 0.5

# Brief or caption text that asks to hide that a clip is paid. Never followed; campaign.py flags each one.
_NEG = r"(?:do not|don'?t|dont|never|avoid|no need to|please don'?t)"
_ADTAG = r"#\s?(?:ad|ads|sponsored|spon|paid|advert|advertisement)\b"
_ADWORD = r"(?:ad|ads|paid|sponsor(?:ed|ship)?|partnership|brand(?:ed)?|promo(?:tion(?:al)?)?)"
# A disclosure named in words: "disclosure", "the ad label", "paid partnership label", "branded content toggle".
_DISCWORD = (r"(?:(?:ad\s+|paid\s+|sponsor(?:ship|ed)?\s+)?(?:disclosures?|disclaimers?)|(?:ad|sponsor(?:ed)?)\s+(?:label|tag|hashtag)s?"
             r"|paid[- ]partnership(?:\s+(?:label|toggle|tag))?|branded[- ]content(?:\s+(?:label|toggle|setting))?)")
_TOGGLE = (r"paid[- ]partnership|branded[- ]content|promotion(?:al)?(?:\s+content)?|sponsor(?:ed|ship)?|content disclosure"
           r"|disclosure|ad\s+(?:label|toggle|setting)")
_REJECT = (r"\b(?:rejected|refused|declined|disqualif\w*|not (?:be )?(?:approved|accepted|paid|counted)|"
           r"won'?t (?:be )?(?:approved|accepted|paid|counted)|unpaid|removed)\b")
# The disclosure itself is what gets a clip rejected: "Posts with #ad will not be approved", "Clips that
# look like ads will be rejected". Never followed, whatever else the sentence says.
DISCLOSURE_REJECTED = [
    r"\bwith\s+(?:an?\s+|the\s+|any\s+)?(?:" + _ADTAG + r"|" + _DISCWORD + r")[^.\n]{0,60}?" + _REJECT,
    r"\b(?:look|looks|feel|feels|seem|seems|sound|sounds|come across|comes across)\s+(?:like\s+|as\s+)?(?:an?\s+)?"
    r"(?:ad|ads|advert|advertisement|sponsored|promo|commercial)\b[^.\n]{0,40}?" + _REJECT,
]
HIDE_AD = [
    _NEG + r"\s+(?:make|let)\s+(?:it|this|them|the (?:clip|video|post)s?)\s+(?:look|feel|seem|sound|appear)\s+like\s+(?:an?\s+)?(?:ad|advert|advertisement|sponsored|promo|paid)",
    _NEG + r"\s+(?:make|let)\s+(?:it|this|them|the (?:clip|video|post)s?)\s+(?:look|feel|seem|appear)\s+(?:sponsored|paid|promotional|branded|like a promotion)",
    r"(?:\bno|without|skip|remove|drop|leave out|lose|ditch)\s+(?:the\s+|any\s+|a\s+)?" + _ADTAG,
    _NEG + r"\s+(?:use|put|add|include|using|adding|putting|including|write|type|tag)\s+(?:the\s+|a\s+|an\s+|any\s+)?(?:" + _ADTAG
    + r"|" + _ADWORD + r"\s+(?:disclosure|disclaimer|label|tag|toggle|hashtag|setting)s?)",
    _NEG + r"\s+(?:disclose|mention|say|tag|label|tell|flag|mark)\b[^.\n]{0,40}\b(?:ad|paid|sponsor|sponsored|partnership|brand deal|promotion)",
    _NEG + r"\s+(?:use|turn on|tick|enable|add|switch on|toggle)\s+(?:the\s+)?(?:paid[- ]partnership|branded[- ]content|promotion(?:al)?|sponsor(?:ed)?|content disclosure)\s*(?:label|toggle|tag|tool|setting|disclosure|box)?",
    r"\b(?:leave out|skip|drop|remove|forget|no|without|ditch)\s+(?:the\s+|any\s+|a\s+)?(?:ad\s+|paid\s+|sponsor(?:ship|ed)?\s+)?(?:disclosures?|disclaimers?|paid[- ]partnership(?:\s+(?:label|toggle|tag|setting))?|branded[- ]content(?:\s+(?:label|toggle|setting))?)\b",
    r"\b(?:make|keep)\s+(?:it|them|this|the (?:clip|video|post)s?)\s+(?:look|feel|seem|looking|feeling|seeming)\s+(?:organic|native|like (?:a |an )?(?:fan|organic|regular|normal|random))",
    r"\b(?:look|feel|seem|appear|read)s?\s+like\s+[^.\n]{0,40}?,?\s*not\s+(?:like\s+)?(?:an?\s+)?(?:ad|advert|advertisement|sponsored|paid|promo)\b",
    r"\b(?:look|feel|seem)s?\s+(?:natural|organic|authentic)\b[^.\n]{0,40}\bnot\s+(?:an?\s+)?(?:ad|paid|sponsored)",
    r"\b(?:hide|hiding|conceal)\s+(?:that|the fact)\b[^.\n]{0,40}\b(?:paid|ad|sponsor)",
    r"\bnot\s+(?:obviously|clearly)\s+(?:an?\s+)?(?:ad|sponsored|paid)",
    r"\b(?:no|without)\s+(?:ad|sponsor(?:ship|ed)?|paid)\s+(?:disclosure|label|tag|hashtag)s?\b",
    r"\bpretend\b[^.\n]{0,40}\b(?:fan|found|organic|not paid|your own)",
    r"\b(?:#sp|#collab)\s+(?:is\s+)?(?:enough|instead)\b",
] + DISCLOSURE_REJECTED + [
    # "Disclosure is not required", "#ad isn't mandatory", "You don't need to disclose this"
    r"(?:" + _ADTAG + r"|" + _DISCWORD + r")\s+(?:is|are)\s*(?:not|n'?t)\s+(?:required|needed|necessary|mandatory)",
    r"(?:" + _ADTAG + r"|" + _DISCWORD + r")\s+(?:is|are)\s+(?:optional|not a must)\b",
    r"\b(?:don'?t|do not|doesn'?t|does not|won'?t|no)\s+need\s+(?:to\s+)?(?:disclose|label|tag|mark|flag|add\s+(?:the\s+)?#)",
    r"\bneed\s*(?:n'?t|not)\s+(?:disclose|label|tag|mark)\b",
    # toggles switched off: "Turn off the branded content toggle", "Leave the Paid Partnership label off"
    r"\b(?:turn|switch|toggle|keep|leave)\s+off\s+(?:the\s+|any\s+)?(?:" + _TOGGLE + r")",
    r"\b(?:turn|switch|toggle|keep|leave)\s+(?:the\s+|any\s+)?(?:" + _TOGGLE + r")\s*(?:label|toggle|tag|setting|box|switch)?\s+off\b",
    r"\b(?:no|without|avoid|skip)\s+(?:hash)?tags?\s+(?:like|such as)\s+(?:the\s+)?" + _ADTAG,
    # "Don't make it obvious it's an ad", "nobody should know it's sponsored", "no ad vibes"
    _NEG + r"\s+mak\w*\s+(?:it|this|them|the (?:clip|video|post)s?)\s+(?:too\s+|so\s+)?(?:obvious|clear|evident|apparent)\b"
    r"[^.\n]{0,30}\b(?:ad|ads|advert|sponsored|paid|promo\w*|brand deal|commercial)\b",
    r"\b(?:nobody|no one|no-one|(?:viewers?|people|followers?|they)\s+(?:shouldn'?t|should not|mustn'?t|must not|"
    r"don'?t need to|can'?t|cannot))\b[^.\n]{0,30}\b(?:know|tell|notice|realise|realize|guess|see)\b[^.\n]{0,40}\b"
    r"(?:ad|ads|advert|sponsored|paid|promo\w*|brand deal|partnership|commercial)\b",
    r"\bno\s+(?:ad|ads|advert|sponsored|promo|commercial|salesy)[- ]?(?:vibes?|feel(?:ing)?|look|energy|style|tone)\b",
]
# Only in a brief: the same words can be innocent in a caption ("how to act natural on camera").
HIDE_AD_BRIEF = [r"\bact\s+(?:natural|organic|normal)\b"]
# A sentence that names the disclosure as what is required asks for it, not against it: "Posts without
# #ad are rejected", "No #ad means not paid", "#ad is required". A sentence where the disclosure itself
# causes the rejection ("with #ad ... not approved", "looks like an ad ... rejected") is not one of these.
DISCLOSE_REQUIRED = [
    r"\b(?:without|no|missing|lacking|forget\w*|leave out|leaving out|skip\w*)\s+(?:an?\s+|the\s+|any\s+|a clear\s+)?"
    r"(?:" + _ADTAG + r"|" + _DISCWORD + r"|ad)\b[^.\n]{0,60}?(?:" + _REJECT + r"|\bmeans\s+(?:not paid|no pay|rejected))",
    r"(?:" + _ADTAG + r"|" + _DISCWORD + r")\s+(?:is|are)\s+(?:always\s+)?(?:required|mandatory|a must|compulsory)\b",
    r"\b(?:must|always|has to|have to)\s+(?:include|use|add|have|carry|show|start with)\s+(?:an?\s+|the\s+)?(?:"
    + _ADTAG + r"|" + _DISCWORD + r")",
]
# Words that name a disclosure, for the "read this sentence yourself" net.
DISCLOSURE_MENTION = r"(?:" + _ADTAG + r"|\b(?:ad|ads|advert\w*|disclos\w+|disclaimer|sponsor\w*|paid[- ]partnership|branded[- ]content|promotion(?:al)? content)\b)"
NEGATION_OR_REJECT = r"\b(?:no|not|never|don'?t|do not|without|avoid|skip|remove|hide|off|rejected|isn'?t|aren'?t|won'?t)\b"
# Brief text that forbids the disclosure on the video itself. The skill keeps it on screen anyway, so the
# brief and the skill disagree: the user asks the brand in writing or skips the campaign.
DISCLOSURE_CONFLICT = [
    r"\bno\s+(?:paid[- ]partnership|ad|disclosure|sponsor(?:ed|ship)?|promo(?:tional)?|branded)\s+(?:text|label|overlay|banner|sticker|title|pill)s?\b",
    r"\b(?:no|without|zero)\s+(?:any\s+)?(?:text|overlays?|stickers?|graphics?|banners?)\s+(?:burned\s+|burnt\s+)?(?:on|over|in|into)\s+(?:the\s+)?(?:video|clip|screen|footage)",
    _NEG + r"\s+(?:put|show|burn|write|add|place|display)\s+(?:any\s+|the\s+)?[\"'“]?(?:ad|paid partnership|sponsored|disclosure|text|overlays?)[\"'”]?\s+(?:on|in|over|into)\s+(?:the\s+)?(?:video|clip|screen|footage)",
    r"\bno\s+on[- ]screen\s+(?:disclosure|text|label|ad)\b",
    r"\bno\s+(?:text\s+)?overlays?\b",
    r"\bno\s+burn(?:ed|t)[- ]in\s+(?:text|disclosure|label)",
]
# Asking for or arranging engagement: a permanent ban on the marketplaces and a platform rule break.
ENGAGEMENT_BAIT = [
    r"\bl4l\b", r"\bf4f\b", r"\bsub4sub\b", r"\bengagement\s+(?:group|pod|chat)s?\b",
    r"\bbuy(?:ing)?\s+(?:views|likes|followers|comments|shares)\b", r"\bview\s*bots?\b", r"\bbot(?:ted|ting)?\s+(?:views|likes)\b",
]
# In a caption these read as asking viewers to swap follows; often meant, sometimes quoted. A warning there.
ENGAGEMENT_SOFT = [r"\b(?:like|follow|sub)\s*(?:4|for)\s*(?:like|follow|sub)\b"]
# Only in a brief: location tricks. The word VPN in a caption ("the best VPN for travel") is fine.
LOCATION_TRICKS = [
    r"\b(?:use|using|with|via|through|turn on|get|need)\s+(?:a\s+|your\s+)?vpn\b",
    r"\bvpn\s+(?:to|for|set to|in)\s+(?:change|fake|spoof|appear|look|get|set|switch|the us|us|usa|america)\b",
    r"\b(?:fake|spoof|change)\s+(?:your\s+)?(?:location|country|region|ip)\b",
    r"\b(?:from|on|over|provide|provides|give|gives|offer|offers)\b[^.\n]{0,20}\bvpn\b",
]
# A sentence that bans something (the brief's own "no engagement groups") is not a request for it.
BANS_IT = r"\b(?:no|not|never|don'?t|do not|without|avoid|banned?|forbidden|prohibited|disallowed|zero|against)\b"

_reading = [None]   # the file being read, for the last-resort message in guard()


def reading(path):
    _reading[0] = path


def die(msg):
    raise SystemExit("error: " + msg)


def guard(main):
    """Run a script's main(): any unexpected error becomes one clear line, not a traceback.
    Set CLIP_DEBUG=1 to see the traceback."""
    try:
        main()
    except SystemExit:
        raise
    except KeyboardInterrupt:
        sys.exit("stopped. Run the same command again when you are ready")
    except Exception as e:
        if os.environ.get("CLIP_DEBUG"):
            raise
        if isinstance(e, UnicodeEncodeError):
            sys.exit("error: a text holds half an emoji or a broken character (a cut-off copy). Retype that text")
        if isinstance(e, OSError):
            name = rel(str(e.filename)) if e.filename else "a file"
            sys.exit(f"error: can't read or write {name}: {e.strerror or e}. Check that it exists, that you "
                     "may write to that folder, and that no file there has the name of a folder this needs")
        where = (rel(str(_reading[0])) if _reading[0] else
                 "one of the files you gave (campaign.json, clipjob.json, clips.json or a saved reply)")
        sys.exit(f"error: {where} has a value of the wrong kind somewhere (text where a number belongs, a list "
                 f"where one value belongs, or the reverse): {type(e).__name__}: {e}. "
                 "Set CLIP_DEBUG=1 for details.")


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


def hide_ad_hits(text, brief=False):
    """Sentences that ask to hide that a clip is paid. A sentence saying a clip without the disclosure
    is rejected asks for the disclosure, so it isn't one."""
    pats = HIDE_AD + (HIDE_AD_BRIEF if brief else [])
    return [(s, m) for s, m in find_phrases(text, pats) if not requires_disclosure(s)]


def requires_disclosure(sentence):
    """True when the sentence names the disclosure as what is required ("Posts without #ad are
    rejected", "#ad is required"), and doesn't also make the disclosure the cause of a rejection."""
    flat = re.sub(r"[‘’]", "'", sentence or "")
    if not any(re.search(p, flat, re.I) for p in DISCLOSE_REQUIRED):
        return False
    return not any(re.search(p, flat, re.I) for p in DISCLOSURE_REJECTED)


def read_yourself(text, already=()):
    """Sentences of a brief that name a disclosure next to a negation or a rejection, and that the
    patterns neither flagged nor read as asking for the disclosure. The agent reads each one itself."""
    flat = re.sub(r"[‘’]", "'", text or "")
    out = []
    for raw in re.split(r"(?<=[.!?])\s+|\n", flat):
        s = " ".join(raw.split()).lstrip("-*•> ").strip()
        if not s or s in already or s in out:
            continue
        if re.search(DISCLOSURE_MENTION, s, re.I) and re.search(NEGATION_OR_REJECT, s, re.I) \
                and not requires_disclosure(s):
            out.append(s)
    return out


def asks_for(text, patterns):
    """Sentences that ask for one of these things. One that bans it ("no engagement groups") doesn't."""
    return [(s, m) for s, m in find_phrases(text, patterns) if not re.search(BANS_IT, s, re.I)]


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
    """The clock the scripts use. CLIP_NOW (an ISO time) fixes it for examples and tests."""
    fixed = os.environ.get("CLIP_NOW")
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


def clock(t, zone=None):
    """A time as people read it: 'Mon 16 Nov 09:31 America/New_York (EST)', or in UTC when the zone
    is unknown. The abbreviation tells EDT from EST on the night the clocks go back."""
    tz = load_zone(zone)
    if tz is None:
        return t.astimezone(datetime.timezone.utc).strftime("%a %d %b %H:%M UTC")
    t = t.astimezone(tz)
    abbr = t.strftime("%Z")
    return t.strftime("%a %d %b %H:%M ") + zone + (f" ({abbr})" if abbr and abbr != zone else "")


def money(x, cur="USD"):
    sign = "$" if cur == "USD" else ""
    tail = "" if cur == "USD" else f" {cur}"
    return f"{sign}{x:,.2f}{tail}"


def payout(views, rate_per_1k, min_payout=0.0, cap=None, fee_pct=DEFAULT_FEE_PCT, min_views=0, cur="USD"):
    """(gross, paid after the fee, why) for one clip at this many views. Below the campaign's
    minimum nothing is paid; above its cap the cap is paid. The campaign's own count decides."""
    views = max(0, int(views or 0))
    if min_views and views < min_views:
        return 0.0, 0.0, f"under the {min_views:,} view minimum"
    gross = views / 1000.0 * float(rate_per_1k or 0)
    why = ""
    if cap is not None and gross > cap:
        gross, why = float(cap), "capped"
    if min_payout and gross < min_payout:
        return gross, 0.0, f"under the {money(min_payout, cur)} minimum payout"
    return gross, round(gross * (1 - float(fee_pct) / 100.0), 2), why


def place_name(geo):
    """'US' reads as 'the US' in a sentence; a country name stays as it is."""
    g = str(geo or "").strip()
    return f"the {g}" if g.upper() in ("US", "USA", "UK", "UAE", "NETHERLANDS", "PHILIPPINES") else g


def is_num(v, minimum=None):
    """A real, finite number (not true/false, not Infinity or NaN)."""
    import math
    ok = isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
    return ok and (minimum is None or v >= minimum)


# Fields a brief often leaves out: null or a wrong value reads as the default (campaign.py reports the
# wrong value as an error), so no script ever does arithmetic with None.
CAMPAIGN_DEFAULTS = {"fee_pct": DEFAULT_FEE_PCT, "window_days": DEFAULT_WINDOW_DAYS, "days_live": DEFAULT_WINDOW_DAYS,
                     "submit_within_minutes": SUBMIT_MINUTES, "max_overlap": DEFAULT_MAX_OVERLAP}


def with_defaults(c):
    """A copy of a campaign with every optional field filled in: the defaults above, "window_from"
    ("threshold" for a marketplace campaign: views count for window_days from the day the clip
    crosses the payout threshold; "post" for your own campaign), "required_sound" as
    {name, platforms, volume} or None, "currency" and "aspect"."""
    out = dict(c) if isinstance(c, dict) else {}
    for k, v in CAMPAIGN_DEFAULTS.items():
        if not is_num(out.get(k), 0):
            out[k] = v
    if out.get("window_from") not in ("threshold", "post"):
        out["window_from"] = "post" if out.get("own_content") is True else "threshold"
    if not isinstance(out.get("currency"), str) or not out["currency"].strip():
        out["currency"] = "USD"
    if out.get("aspect") not in ("9:16", "any"):
        out["aspect"] = "9:16"
    out["required_sound"] = sound_spec(out.get("required_sound"))
    return out


def sound_spec(v):
    """A required sound as {"name", "platforms", "volume"}, or None."""
    if isinstance(v, str) and v.strip():
        return {"name": v.strip(), "platforms": ["TIKTOK"], "volume": None}
    if isinstance(v, dict) and isinstance(v.get("name"), str) and v["name"].strip():
        plats = v.get("platforms") if isinstance(v.get("platforms"), list) else ["TIKTOK"]
        plats = [p.strip().upper() for p in plats if isinstance(p, str)] or ["TIKTOK"]
        vol = v.get("volume") if isinstance(v.get("volume"), str) and v["volume"].strip() else None
        return {"name": v["name"].strip(), "platforms": plats, "volume": vol}
    return None


def terms(c, platform):
    """(rate per 1,000 views, minimum payout, cap per clip, view minimum) for one platform: the
    platform's own numbers when the brief sets them per platform, else the campaign's."""
    plat = (c.get("platforms") or {}).get(platform) if isinstance(c.get("platforms"), dict) else None
    plat = plat if isinstance(plat, dict) else {}

    def pick(k):
        v = plat.get(k) if plat.get(k) is not None else c.get(k)
        return v if is_num(v, 0) else None
    rate = plat.get("rate_per_1k") if is_num(plat.get("rate_per_1k"), 0) else 0.0
    return float(rate), float(pick("min_payout") or 0), pick("cap_per_clip"), int(pick("min_views") or 0)


def threshold_views(c, platform):
    """Views at which a clip starts to pay on this platform (0 when there is no minimum)."""
    rate, mn, _, mv = terms(c, platform)
    need = int(mn / rate * 1000 + 0.999) if mn and rate else 0
    return max(mv, need)


# ---- the user's own files: one ledger and one accounts file for every campaign and folder

def user_home():
    """Where the ledger and the saved accounts live: AI_CLIPPING_HOME, else ~/.ai-clipping (the
    .ai-clipping folder in the user's home folder, on Windows too)."""
    home = os.environ.get("AI_CLIPPING_HOME")
    return os.path.abspath(os.path.expanduser(home)) if home else os.path.join(os.path.expanduser("~"), ".ai-clipping")


def ledger_path(override=None):
    """The one ledger of every post and submission, for every campaign, whatever folder it was made
    in: --ledger, else AI_CLIPPING_LEDGER, else <user_home>/ledger.json. One file is what lets the
    skill refuse an edit or a link already used for another campaign."""
    p = override or os.environ.get("AI_CLIPPING_LEDGER")
    return os.path.abspath(os.path.expanduser(p)) if p else os.path.join(user_home(), "ledger.json")


_LOADED = {}   # ledger path -> fingerprint of the file as it was read, so a save can't drop another session's write


def _file_fp(path):
    try:
        with open(path, "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except FileNotFoundError:
        return None


def load_ledger(path=None):
    """ledger.json: {"posts": {"<postId>|<account>": {...}}, "submissions": [{...}], "campaigns":
    {id: the campaign's terms}}. A damaged file is an error and is left exactly as it is: it may be
    the only record of what went out."""
    path = path or ledger_path()
    _LOADED[os.path.abspath(path)] = _file_fp(path)
    if not os.path.exists(path):
        return {"posts": {}, "submissions": [], "campaigns": {}}
    data = read_json(path, "the ledger")
    if (not isinstance(data, dict) or not isinstance(data.get("posts", {}), dict)
            or not isinstance(data.get("submissions", []), list)
            or not isinstance(data.get("campaigns", {}), dict)
            or not all(isinstance(v, dict) for v in data.get("posts", {}).values())
            or not all(isinstance(v, dict) and isinstance(v.get("url"), str) for v in data.get("submissions", []))):
        die(f"the ledger ({rel(path)}) is damaged: it must hold \"posts\" (one entry per post) and \"submissions\" (a "
            "list). It was left as it is. Repair it, or move it away if nothing in it was really posted")
    data.setdefault("posts", {})
    data.setdefault("submissions", [])
    data.setdefault("campaigns", {})
    reading(None)
    return data


def save_ledger(path, data):
    """Write the ledger under a lock file. When another session (a second agent, another campaign's
    script) wrote it after this one read it, nothing is written: run the command again, it reads the
    new ledger first. That way no post or submission is ever lost."""
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


def proof_path(lpath=None):
    """The proof log: proof.csv next to the ledger, one file for every campaign (each row names its
    campaign), so earnings and proof never depend on the folder a command runs in."""
    return os.path.join(os.path.dirname(os.path.abspath(lpath or ledger_path())), "proof.csv")


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


def load_saved_accounts():
    """The accounts the user saved once (<user_home>/accounts.json): {"accounts": [{name, platform,
    handle, the comment/duet/stitch and YouTube choices, audience}]}. [] when none. They are only ever
    shown as suggestions; nothing from this file goes into a post unless the agent writes it into
    clipjob.json after the user confirms it."""
    path = os.path.join(user_home(), "accounts.json")
    if not os.path.exists(path):
        return []
    data = read_json(path, "your saved accounts")
    reading(None)
    accs = data.get("accounts") if isinstance(data, dict) else None
    return [a for a in accs if isinstance(a, dict) and isinstance(a.get("name"), str)] if isinstance(accs, list) else []


def account_key(a):
    """"TIKTOK|example.clipper": an account is the same account only when platform and handle both
    match (names like "TikTok" are reused across accounts). None without both."""
    if not isinstance(a, dict):
        return None
    p, h = a.get("platform"), a.get("handle")
    if not (isinstance(p, str) and p.strip() and isinstance(h, str) and h.strip().lstrip("@").strip()):
        return None
    return p.strip().upper() + "|" + h.strip().lstrip("@").strip().casefold()


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
