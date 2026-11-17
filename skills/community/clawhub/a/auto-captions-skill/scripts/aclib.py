"""Shared helpers for the auto captions scripts: the job file, video probing, fonts, scripts
(writing systems) and styles. Standard library only, except Pillow where noted."""
import functools, json, math, os, re, shutil, subprocess, sys, unicodedata

try:  # Windows consoles default to cp1252; captions are often not Latin
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
FONT_DIR = os.path.join(SKILL, "fonts")
STYLE_DIR = os.path.join(SKILL, "styles")
VIDEO_EXT = (".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi")
AUDIO_EXT = (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg", ".opus")

# Languages written without spaces between words: captions join their tokens directly.
NO_SPACE = {"zh", "ja", "th", "lo", "my", "km", "bo"}
# Right-to-left scripts: words are laid out from the right.
RTL = {"ar", "he", "fa", "ur", "ps", "yi", "ug", "sd", "ckb"}
# Arabic-script languages: letters change shape by position (reshaped when Pillow lacks raqm).
ARABIC_SCRIPT = {"ar", "fa", "ur", "ps", "ug", "sd", "ckb"}
# Scripts that need a text shaper (libraqm) to draw correctly at all.
NEEDS_SHAPER = {"hi", "mr", "ne", "bn", "pa", "gu", "or", "ta", "te", "kn", "ml", "si", "th", "lo",
                "km", "my", "bo", "sa"}
CJK = {"zh", "ja", "ko"}
# Caption line limits (characters) for SRT files, after the Netflix timed text style guides.
SRT_LINE = {"zh": 16, "ja": 13, "ko": 16}
SRT_CPS = {"zh": 9, "ja": 4, "ko": 12}   # Netflix adult reading speeds for these languages
# Small words a caption or a line should not end on (they belong with the next word).
SMALL = {
    "en": {"a", "an", "the", "of", "to", "for", "and", "or", "but", "that", "with", "on", "in", "at", "by",
           "from", "as", "if", "my", "your", "our", "their", "his", "her", "its", "i", "into", "over", "than",
           "about", "be", "is", "are", "was", "were", "will", "we", "you", "it", "this", "so", "can", "not"},
    "es": {"el", "la", "los", "las", "un", "una", "de", "del", "y", "o", "que", "en", "con", "por", "para", "a",
           "al", "su", "sus", "mi", "tu", "es", "se", "lo", "le", "no", "sobre"},
    "pt": {"o", "a", "os", "as", "um", "uma", "de", "do", "da", "dos", "das", "e", "ou", "que", "em", "no", "na",
           "com", "por", "para", "se", "é", "seu", "sua"},
    "fr": {"le", "la", "les", "un", "une", "de", "du", "des", "et", "ou", "que", "en", "au", "aux", "à", "pour",
           "par", "sur", "ce", "se", "ne", "est", "son", "sa"},
    "de": {"der", "die", "das", "den", "dem", "ein", "eine", "einen", "und", "oder", "von", "zu", "mit", "im",
           "in", "am", "auf", "für", "ist", "zum", "zur"},
    "nl": {"de", "het", "een", "en", "of", "van", "te", "met", "op", "in", "aan", "voor", "is", "om"},
    "it": {"il", "lo", "la", "i", "gli", "le", "un", "una", "di", "e", "o", "che", "in", "con", "per", "a",
           "del", "della", "è"},
}
CONNECT = {"or", "to", "and", "-", "o", "y", "a", "ou", "e", "et", "bis", "und", "of", "tot"}
# Words that belong with the number after them ("about 9 or 10 minutes", "unos 9 o 10 minutos").
APPROX = {"about", "around", "roughly", "nearly", "almost", "approximately", "over", "under", "some",
          "unos", "unas", "casi", "cerca", "más", "menos", "cerca de", "environ", "presque", "près",
          "etwa", "ungefähr", "fast", "über", "ongeveer", "bijna", "circa", "ruim", "cerca", "quase",
          "mais", "menos", "circa", "quasi", "oltre"}

CANVAS = {"9:16": (1080, 1920), "4:5": (1080, 1350), "1:1": (1080, 1080), "16:9": (1920, 1080)}
FITS = ("crop", "blur", "pad")

WARNINGS = []


def warn(msg):
    if msg in WARNINGS:  # the same warning once per run
        return
    WARNINGS.append(msg)
    print("warning: " + msg, file=sys.stderr)


class Stop(Exception):
    pass


def die(msg):
    raise SystemExit("error: " + msg)


def guard(main):
    """Run a script's main(): any unexpected error becomes one clear line, not a traceback.
    Set CAPTIONS_DEBUG=1 to see the traceback."""
    try:
        main()
    except (SystemExit, KeyboardInterrupt):
        raise
    except Exception as e:
        if os.environ.get("CAPTIONS_DEBUG"):
            raise
        sys.exit(f"error: {type(e).__name__}: {e}. Check the JSON files you edited for a wrong type "
                 "(text where a number belongs, or the reverse). Set CAPTIONS_DEBUG=1 for details.")


# ---------- files ----------

def read_json(path):
    try:
        with open(path, encoding="utf-8-sig") as fh:
            return json.load(fh)
    except FileNotFoundError:
        die(f"{path} not found")
    except IsADirectoryError:
        die(f"{path} is a folder, not a JSON file")
    except UnicodeDecodeError:
        die(f"{path} is not UTF-8 text")
    except json.JSONDecodeError as e:
        die(f"{path} is not valid JSON (line {e.lineno}, column {e.colno}): {e.msg}")


def write_json(path, data):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def rel(path, start=None):
    try:
        r = os.path.relpath(path, start or os.getcwd())
    except ValueError:  # another drive on Windows
        return path.replace(os.sep, "/")
    if r.startswith(os.pardir + os.sep + os.pardir + os.sep):
        return os.path.abspath(path).replace(os.sep, "/")  # far outside: the full path reads better
    return r.replace(os.sep, "/")


def num(value, what, lo=None, hi=None):
    """A finite number within [lo, hi], or a clear error."""
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        die(f"{what} must be a number, not {value!r}")
    if (lo is not None and value < lo) or (hi is not None and value > hi):
        die(f"{what} must be from {lo} to {hi}, not {value}")
    return float(value)


def text_of(value, what):
    if not isinstance(value, str):
        die(f"{what} must be text, not {value!r}")
    return value


SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
LANG = re.compile(r"^[a-z]{2,3}(-[A-Za-z0-9]{2,8})?$")
OUTPUT_KEYS = {"id", "style", "style_overrides", "canvas", "fit", "focus_x", "position", "languages", "sounds",
               "font_file"}


def load_job(path):
    """The job file the agent writes. Paths in it are relative to the job file's folder."""
    if path.lower().endswith(VIDEO_EXT + AUDIO_EXT):
        die(f"{path} is a media file. Write a job file first (see references/job-file.md), or run "
            "transcribe.py on the video directly.")
    job = read_json(path)
    if not isinstance(job, dict):
        die(f"{path}: the job must be a JSON object")
    base = os.path.dirname(os.path.abspath(path))
    job["_base"] = base
    job["_path"] = os.path.abspath(path)
    vids = job.get("videos")
    if not isinstance(vids, list) or not vids:
        die(f"{path}: 'videos' must list at least one video")
    seen, out = set(), []
    for i, v in enumerate(vids):
        if isinstance(v, str):
            v = {"file": v}
        if not isinstance(v, dict) or not isinstance(v.get("file"), str) or not v["file"].strip():
            die(f"{path}: videos[{i}] needs a 'file'")
        vid = v.get("id") if v.get("id") is not None else os.path.splitext(os.path.basename(v["file"]))[0]
        vid = re.sub(r"[^\w.-]+", "-", str(vid)).strip("-._")[:64] or f"video-{i + 1}"
        if vid in seen:
            die(f"{path}: two videos share the id '{vid}'; give one an 'id'")
        seen.add(vid)
        for k, lo, hi in (("focus_x", 0, 1), ("position", 0.05, 0.95)):
            if isinstance(v.get(k), dict) and k == "position":
                for oid, p in v[k].items():
                    num(p, f"videos[{i}].position.{oid}", lo, hi)
            elif v.get(k) is not None:
                num(v[k], f"videos[{i}].{k}", lo, hi)
        if v.get("subtitles") is not None and isinstance(v["subtitles"], str) \
                and not os.path.exists(os.path.join(base, v["subtitles"])):
            die(f"{path}: videos[{i}].subtitles: {v['subtitles']} not found (paths are relative to the job file)")
        for k in ("subtitles", "language"):
            if v.get(k) is not None:
                text_of(v[k], f"videos[{i}].{k}")
        v = dict(v, id=vid, file=os.path.normpath(os.path.join(base, v["file"])))
        out.append(v)
    job["videos"] = out
    for k, d in (("work", "work"), ("out", "captioned")):
        val = job.get(k, d)
        if not isinstance(val, str) or not val.strip():
            die(f"{path}: '{k}' must be a folder name")
        job[k] = os.path.normpath(os.path.join(base, val))
    for k in ("language", "font_file", "preset"):
        if job.get(k) is not None:
            text_of(job[k], f"{path}: '{k}'")
    if job.get("language") and not LANG.match(job["language"]):
        die(f"{path}: 'language' must be a code like en, es or pt-BR")
    vocab = job.get("vocab", [])
    if not isinstance(vocab, list) or not all(isinstance(x, str) for x in vocab):
        die(f"{path}: 'vocab' must be a list of names and terms")
    outs = job.get("outputs") or [{"id": "main", "style": "pop", "canvas": "source"}]
    if not isinstance(outs, list):
        die(f"{path}: 'outputs' must be a list")
    ids = set()
    for o in outs:
        if not isinstance(o, dict):
            die(f"{path}: each output must be an object")
        o.setdefault("id", o.get("style", "main"))
        if not isinstance(o["id"], str) or not SAFE_ID.match(o["id"]) or o["id"] in ids:
            die(f"{path}: output id {o['id']!r} must be unique letters, digits, . - or _")
        ids.add(o["id"])
        unknown = set(o) - OUTPUT_KEYS
        if unknown:
            die(f"{path}: output {o['id']}: unknown setting(s) {', '.join(sorted(unknown))}")
        if not isinstance(o.get("style", "pop"), str):
            die(f"{path}: output {o['id']}: 'style' must be a preset name or a style file")
        if o.get("canvas", "source") not in ("source",) + tuple(CANVAS):
            die(f"{path}: output {o['id']}: canvas must be source, {', '.join(CANVAS)}")
        if o.get("fit", "crop") not in FITS:
            die(f"{path}: output {o['id']}: fit must be crop, blur or pad")
        for k, lo, hi in (("focus_x", 0, 1), ("position", 0.05, 0.95)):
            if o.get(k) is not None:
                num(o[k], f"output {o['id']}: {k}", lo, hi)
        if "languages" in o and (not isinstance(o["languages"], list)
                                 or not all(isinstance(x, str) and LANG.match(x) for x in o["languages"])):
            die(f"{path}: output {o['id']}: 'languages' must be a list like [\"en\", \"es\"]")
        if "style_overrides" in o and not isinstance(o["style_overrides"], dict):
            die(f"{path}: output {o['id']}: 'style_overrides' must be an object")
        if "sounds" in o and not isinstance(o["sounds"], bool):
            die(f"{path}: output {o['id']}: 'sounds' is true or false")
        if o.get("font_file") is not None:
            text_of(o["font_file"], f"output {o['id']}: font_file")
    job["outputs"] = outs
    langs = job.get("translations") or []
    if not isinstance(langs, list) or not all(isinstance(x, str) and LANG.match(x) for x in langs):
        die(f"{path}: 'translations' must be language codes like [\"es\", \"pt-BR\"]")
    job["translations"] = langs
    return job


def video_dir(job, v):
    return os.path.join(job["work"], v["id"])


def selected(job, only):
    if not only:
        return job["videos"]
    want = set(only.split(","))
    vids = [v for v in job["videos"] if v["id"] in want]
    if not vids:
        die(f"--only {only}: no video with that id (ids: {', '.join(v['id'] for v in job['videos'])})")
    return vids


# ---------- ffmpeg ----------

def need_ffmpeg():
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        die("ffmpeg is not installed. Mac: brew install ffmpeg. Windows: winget install Gyan.FFmpeg "
            "(then open a new terminal). Linux: sudo apt install ffmpeg (or your distro's package).")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        tail = "\n".join(r.stderr.strip().splitlines()[-6:])
        die(f"{os.path.basename(cmd[0])} failed:\n{tail}")
    return r


@functools.lru_cache(maxsize=None)
def ffmpeg_has(kind, name):
    """Whether this ffmpeg build has an encoder or filter."""
    r = subprocess.run(["ffmpeg", "-hide_banner", f"-{kind}"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return bool(re.search(rf"\s{re.escape(name)}\s", r.stdout))


def h264_args(preset, crf=19):
    """Video encoder arguments: libx264 when the build has it, else a hardware or open encoder."""
    if ffmpeg_has("encoders", "libx264"):
        return ["-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-profile:v", "high",
                "-maxrate", "16M", "-bufsize", "32M"]
    for enc in ("h264_videotoolbox", "h264_mf", "h264_nvenc", "h264_qsv", "libopenh264"):
        if ffmpeg_has("encoders", enc):
            return ["-c:v", enc, "-b:v", "10M"]
    die("this ffmpeg build has no H.264 encoder (libx264). Install a full build: Mac: brew install "
        "ffmpeg. Windows: winget install Gyan.FFmpeg. Linux: your distro's full ffmpeg package "
        "(Fedora: ffmpeg from RPM Fusion).")


def snap_fps(rate):
    """The output frame rate as ffmpeg text: the source's rate snapped to a standard one, 24 to 60."""
    std = [("24000/1001", 23.976), ("24", 24), ("25", 25), ("30000/1001", 29.97), ("30", 30),
           ("50", 50), ("60000/1001", 59.94), ("60", 60)]
    if not rate or rate < 1:
        return "30"
    if rate > 61:
        rate = 60 if rate % 30 < 1 else rate / round(rate / 30)
    return min(std, key=lambda s: abs(s[1] - max(rate, 23.976)))[0]


@functools.lru_cache(maxsize=None)
def probe(path):
    """width, height (as displayed, after rotation), fps, duration, codecs, audio, colour, size."""
    if not os.path.exists(path):
        die(f"{path} not found")
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        d = json.loads(r.stdout or "{}")
    except json.JSONDecodeError:
        d = {}
    streams = d.get("streams", [])
    vs = [s for s in streams if s.get("codec_type") == "video" and not (s.get("disposition") or {}).get("attached_pic")]
    aus = [s for s in streams if s.get("codec_type") == "audio"]
    if not vs:
        if aus:
            die(f"{path} is audio only. This skill captions videos; for a podcast, make it a video first "
                "(a still image and the audio), or use its subtitle file from captions.py.")
        die(f"{path}: no video stream (is it a video file?)")
    v = vs[0]
    w, h = int(v.get("width") or 0), int(v.get("height") or 0)
    rot = 0
    for sd in v.get("side_data_list") or []:
        if "rotation" in sd:
            rot = int(float(sd["rotation"]))
    try:
        rot = int(float((v.get("tags") or {}).get("rotate", rot)))
    except ValueError:
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
    dur = 0.0
    for src in ((d.get("format") or {}).get("duration"), v.get("duration")):
        try:
            dur = float(src)
            break
        except (TypeError, ValueError):
            continue
    # the audio track to use: the default one, else the first (same choice everywhere)
    a_idx = next((k for k, s in enumerate(aus) if (s.get("disposition") or {}).get("default")), 0)
    a = aus[a_idx] if aus else {}
    return {"width": w, "height": h, "fps": round(fps, 3), "duration": round(dur, 3),
            "vcodec": v.get("codec_name"), "pix_fmt": v.get("pix_fmt"),
            "transfer": v.get("color_transfer"), "primaries": v.get("color_primaries"),
            "acodec": a.get("codec_name"), "audio": bool(aus), "audio_index": a_idx,
            "bytes": os.path.getsize(path), "rotation": rot}


# ---------- languages ----------

def base_lang(code):
    return (code or "").split("-")[0].lower()


def joiner(lang):
    return "" if base_lang(lang) in NO_SPACE else " "


def small_words(lang):
    return SMALL.get(base_lang(lang), set())


def split_text(text, lang):
    """Caption text into tokens: words, or characters for languages without spaces. A space inside
    a number ("28 000") becomes a no-break space so the number stays one token."""
    text = re.sub(r"(?<=\d) (?=\d{3}\b)", "\u00a0", str(text))
    if not joiner(lang):
        return [ch for ch in text if not ch.isspace() or ch == "\u00a0"]
    return [t for t in re.split(r"[ \t\r\n]+", text) if t]


def is_rtl(lang):
    return base_lang(lang) in RTL


def has_raqm():
    try:
        from PIL import features
        return bool(features.check("raqm"))
    except Exception:
        return False


def shape_check(lang):
    """Exit early, with a fix, when this language can't be drawn correctly on this machine."""
    b = base_lang(lang)
    if b in NEEDS_SHAPER and not has_raqm():
        die(f"Burned-in captions in '{lang}' need Pillow with text shaping (libraqm), which this Python "
            "doesn't have. Mac: brew install fribidi harfbuzz libraqm, then pip install --force-reinstall "
            "--no-binary pillow pillow. Linux: sudo apt install libraqm0 (or libfribidi0). Windows: use "
            "the SRT file the skill wrote and the platform's own captions, or caption in another language.")
    if b in ARABIC_SCRIPT and not has_raqm():
        try:
            import arabic_reshaper, bidi  # noqa: F401
        except ImportError:
            die(f"Burned-in captions in '{lang}' need two small packages on this machine: "
                "pip install arabic-reshaper python-bidi")
    elif b in RTL and not has_raqm():
        try:
            import bidi  # noqa: F401
        except ImportError:
            die(f"Burned-in captions in '{lang}' need: pip install python-bidi")


def visual(text, lang):
    """Text in display order for Pillow without raqm (RTL scripts reshaped and reordered)."""
    b = base_lang(lang)
    if b not in RTL or has_raqm():
        return text
    if b in ARABIC_SCRIPT:
        import arabic_reshaper
        text = arabic_reshaper.reshape(text)
    try:
        from bidi import get_display
    except ImportError:
        from bidi.algorithm import get_display
    return get_display(text)


# ---------- fonts ----------

def load_pillow():
    try:
        from PIL import Image, ImageDraw, ImageFont
        return Image, ImageDraw, ImageFont
    except ImportError:
        die("Pillow is missing: pip install pillow")


WINDIR = os.environ.get("WINDIR", "C:/Windows").replace("\\", "/")
SYSTEM_FONTS = {
    "zh": ["/System/Library/Fonts/PingFang.ttc", "/System/Library/Fonts/STHeiti Medium.ttc",
           f"{WINDIR}/Fonts/msyhbd.ttc", f"{WINDIR}/Fonts/msyh.ttc",
           "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
           "/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc"],
    "ja": ["/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc", "/System/Library/Fonts/Hiragino Sans GB.ttc",
           f"{WINDIR}/Fonts/YuGothB.ttc", f"{WINDIR}/Fonts/meiryob.ttc", f"{WINDIR}/Fonts/msgothic.ttc",
           "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc"],
    "ko": ["/System/Library/Fonts/AppleSDGothicNeo.ttc", f"{WINDIR}/Fonts/malgunbd.ttf",
           "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"],
    "rtl": ["/System/Library/Fonts/GeezaPro.ttc", "/System/Library/Fonts/SFArabic.ttf",
            "/System/Library/Fonts/ArialHB.ttc", "/Library/Fonts/Arial Unicode.ttf",
            f"{WINDIR}/Fonts/arialbd.ttf", f"{WINDIR}/Fonts/tahomabd.ttf", f"{WINDIR}/Fonts/segoeuib.ttf",
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "any": ["/Library/Fonts/Arial Unicode.ttf", f"{WINDIR}/Fonts/seguisb.ttf", f"{WINDIR}/Fonts/arialbd.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"],
}
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/"
BUNDLED_URL = {"Poppins-ExtraBold.ttf": "poppins/Poppins-ExtraBold.ttf",
               "Poppins-Bold.ttf": "poppins/Poppins-Bold.ttf",
               "Anton-Regular.ttf": "anton/Anton-Regular.ttf",
               "Inter.ttf": "inter/Inter%5Bopsz,wght%5D.ttf"}


def cache_dir():
    """Where downloaded fonts go: the user's cache, never the skill folder."""
    if os.name == "nt":
        root = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    else:
        root = os.environ.get("XDG_CACHE_HOME") or os.path.join(os.path.expanduser("~"), ".cache")
    return os.path.join(root, "auto-captions-skill", "fonts")


def _fetch(url, path):
    """Download an open-licensed font once (some skill registries strip binary files)."""
    part = path + ".part"
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            import urllib.request
            urllib.request.urlretrieve(url, part)
        except Exception:
            if shutil.which("curl"):
                subprocess.run(["curl", "-sfL", url, "-o", part], check=False, timeout=120)
        if os.path.exists(part) and os.path.getsize(part) > 10000:
            from PIL import ImageFont
            ImageFont.truetype(part, 20)  # a whole, readable font file
            os.replace(part, path)
            return True
    except Exception:
        pass
    try:
        os.remove(part)
    except OSError:
        pass
    return False


def font_path(name):
    """A bundled font (or its cached download), or a font file path the user gave."""
    if not isinstance(name, str) or not name:
        die("a font must be a font file name or path")
    if os.path.isabs(name) or os.sep in name or "/" in name:
        if not os.path.exists(name):
            die(f"font file {name} not found")
        return name
    for folder in (FONT_DIR, cache_dir()):
        path = os.path.join(folder, name)
        if os.path.exists(path) and os.path.getsize(path) > 10000:
            return path
    if name in BUNDLED_URL and _fetch(FONT_URL + BUNDLED_URL[name], os.path.join(cache_dir(), name)):
        return os.path.join(cache_dir(), name)
    if os.path.exists(name):
        return name
    die(f"font {name} is missing and could not be downloaded; reinstall the skill or give a font file "
        "(font_file in the job)")


@functools.lru_cache(maxsize=None)
def get_font(path, size, weight=None):
    _, _, ImageFont = load_pillow()
    try:
        f = ImageFont.truetype(path, size)
    except OSError as e:
        die(f"could not open font {path}: {e}")
    if weight:
        try:
            f.set_variation_by_name(weight)
        except Exception:
            pass
    return f


def is_symbol(ch):
    """Emoji and pictographs: dropped (with a warning) when no font draws them, never fatal."""
    return unicodedata.category(ch) in ("So", "Sk", "Cn", "Co") or ch in "\u200d\ufe0f\ufe0e"


def missing_glyphs(text, f):
    """Characters the font can't draw (they'd come out as empty boxes)."""
    Image, ImageDraw, _ = load_pillow()

    def ink(ch):
        size = max(8, int(getattr(f, "size", 40) * 2))
        im = Image.new("L", (size * 2, size * 2))
        ImageDraw.Draw(im).text((size // 2, size // 2), ch, font=f, fill=255)
        return im.tobytes()
    try:
        notdef = ink("\uffff")
    except Exception:
        return []
    out = []
    for ch in sorted(set(str(text))):
        if ch.isspace() or unicodedata.category(ch) in ("Cc", "Cf", "Zs", "Zl", "Zp"):
            continue
        try:
            if ink(ch) == notdef:
                out.append(ch)
        except Exception:
            out.append(ch)
    return out


def font_for(style_font, lang, sample, size=80, font_file=None, weight=None):
    """The style's font if it can draw this text (as it will be drawn, reshaped for Arabic); else a
    system font that can; else a Noto download. Emoji are ignored here (dropped when drawn).
    Returns (path, note)."""
    sample = "".join(ch for ch in visual(sample, lang) if not is_symbol(ch))
    if font_file:
        return font_path(font_file), "your font file"
    first = font_path(style_font)
    if not missing_glyphs(sample, get_font(first, size, weight)):
        return first, None
    b = base_lang(lang)
    group = b if b in CJK else "rtl" if b in RTL else "any"
    for cand in SYSTEM_FONTS.get(group, []) + SYSTEM_FONTS["any"]:
        if os.path.exists(cand) and not missing_glyphs(sample, get_font(cand, size)):
            return cand, f"system font {os.path.basename(cand)}"
    noto = {"zh": "notosanssc/NotoSansSC%5Bwght%5D.ttf", "ja": "notosansjp/NotoSansJP%5Bwght%5D.ttf",
            "ko": "notosanskr/NotoSansKR%5Bwght%5D.ttf", "ar": "notosansarabic/NotoSansArabic%5Bwdth,wght%5D.ttf",
            "fa": "notosansarabic/NotoSansArabic%5Bwdth,wght%5D.ttf", "ur": "notosansarabic/NotoSansArabic%5Bwdth,wght%5D.ttf",
            "he": "notosanshebrew/NotoSansHebrew%5Bwdth,wght%5D.ttf"}.get(b)
    if noto:
        path = os.path.join(cache_dir(), noto.split("/")[-1].replace("%5B", "[").replace("%5D", "]"))
        if os.path.exists(path) or _fetch(FONT_URL + noto, path):
            if not missing_glyphs(sample, get_font(path, size, "Bold")):
                return path, f"downloaded {os.path.basename(path)} (SIL Open Font License)"
    miss = "".join(missing_glyphs(sample, get_font(first, size, weight)))[:20]
    die(f"no font on this machine can draw these characters: {miss}. Give a font file that covers "
        "them (font_file in the job, any .ttf or .otf).")


# ---------- styles ----------

STYLE_DEFAULTS = {
    "font": "Poppins-ExtraBold.ttf", "weight": None, "size": 84, "uppercase": False, "lowercase": False,
    "color": "#FFFFFF", "active": None, "active_box": None, "keyword": None,
    "stroke": 0, "stroke_color": "#000000", "shadow": None, "box": None,
    "words": 3, "chars": 20, "lines": 1, "pause": 0.3, "reveal": False,
    "position": 0.62, "position_tall": None, "max_width": 0.8, "line_gap": 1.12, "min_show": 0.3,
}
STYLE_NUMBERS = {"size": (12, 400), "words": (1, 20), "chars": (4, 80), "lines": (1, 3), "pause": (0.05, 5),
                 "position": (0.05, 0.95), "position_tall": (0.05, 0.95), "max_width": (0.3, 0.98),
                 "line_gap": (0.8, 3), "min_show": (0.05, 5), "stroke": (0, 30)}
STYLE_INTS = {"words", "chars", "lines"}


def check_style(st, name):
    for k in ("color", "stroke_color", "active", "keyword"):
        if st.get(k) is not None:
            hexrgb(st[k], f"style {name}: '{k}'")
    for k, (lo, hi) in STYLE_NUMBERS.items():
        if st.get(k) is None and k == "position_tall":
            continue
        num(st.get(k), f"style {name}: '{k}'", lo, hi)
        if k in STYLE_INTS and st[k] != int(st[k]):
            die(f"style {name}: '{k}' must be a whole number")
        if k in STYLE_INTS:
            st[k] = int(st[k])
    for k in ("uppercase", "lowercase", "reveal"):
        if not isinstance(st.get(k), bool):
            die(f"style {name}: '{k}' is true or false")
    for k in ("font",):
        text_of(st.get(k), f"style {name}: '{k}'")
    if st.get("weight") is not None:
        text_of(st["weight"], f"style {name}: 'weight'")
    for k, fields in (("shadow", {"dx": (-50, 50), "dy": (-50, 50), "alpha": (0, 1), "blur": (0, 40)}),
                      ("box", {"alpha": (0, 1), "radius": (0, 100)}),
                      ("active_box", {"radius": (0, 100)})):
        obj = st.get(k)
        if obj is None:
            continue
        if not isinstance(obj, dict):
            die(f"style {name}: '{k}' must be an object like "
                + ('{"dx": 0, "dy": 6, "alpha": 0.45, "blur": 3}' if k == "shadow" else
                   '{"color": "#000000", "alpha": 0.6, "radius": 10, "pad": [18, 6]}' if k == "box" else
                   '{"color": "#7C3AED", "radius": 18, "pad": [16, 6], "text": "#FFFFFF"}'))
        for f, (lo, hi) in fields.items():
            if f in obj:
                num(obj[f], f"style {name}: {k}.{f}", lo, hi)
        for f in ("color", "text"):
            if obj.get(f) is not None:
                hexrgb(obj[f], f"style {name}: {k}.{f}")
        if k == "active_box" and "color" not in obj:
            die(f"style {name}: active_box needs a 'color'")
        if "pad" in obj and (not isinstance(obj["pad"], list) or len(obj["pad"]) != 2):
            die(f"style {name}: {k}.pad must be [x, y]")
        for p in obj.get("pad", []):
            num(p, f"style {name}: {k}.pad", 0, 80)
    return st


def load_style(name_or_path, overrides=None, base=None):
    """A preset from styles/ or a style JSON file, with per-output overrides on top."""
    if not isinstance(name_or_path, str) or not name_or_path:
        die("an output's 'style' must be a preset name or a style file path")
    if name_or_path.endswith(".json"):
        path = name_or_path if os.path.isabs(name_or_path) or not base else os.path.join(base, name_or_path)
    else:
        path = os.path.join(STYLE_DIR, name_or_path + ".json")
    if not os.path.exists(path):
        names = sorted(f[:-5] for f in os.listdir(STYLE_DIR) if f.endswith(".json"))
        die(f"style '{name_or_path}' not found. Presets: {', '.join(names)}; or a path to your own .json")
    data = read_json(path)
    if not isinstance(data, dict):
        die(f"{path}: a style must be a JSON object")
    st = dict(STYLE_DEFAULTS)
    st.update({k: v for k, v in data.items() if k not in ("about", "name") and not k.startswith("_")})
    unknown = set(st) - set(STYLE_DEFAULTS)
    if unknown:
        die(f"{rel(path)}: unknown style setting(s): {', '.join(sorted(unknown))}")
    if overrides:
        if not isinstance(overrides, dict):
            die("style_overrides must be an object")
        unknown = set(overrides) - set(STYLE_DEFAULTS)
        if unknown:
            die(f"unknown style setting(s): {', '.join(sorted(unknown))}. Settings: {', '.join(sorted(STYLE_DEFAULTS))}")
        st.update(overrides)
    st["name"] = data.get("name") or os.path.splitext(os.path.basename(path))[0]
    return check_style(st, st["name"])


def hexrgb(h, what="colour"):
    if not isinstance(h, str) or not re.match(r"^#?[0-9A-Fa-f]{6}$", h):
        die(f"{what} must be a colour like #FFD43B, not {h!r}")
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def stamp(t, sep=","):
    """SRT (00:00:01,250) or VTT (sep='.') time."""
    t = max(0.0, t)
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def short(t):
    m, s = divmod(max(0.0, t), 60)
    return f"{int(m):02d}:{s:04.1f}"
