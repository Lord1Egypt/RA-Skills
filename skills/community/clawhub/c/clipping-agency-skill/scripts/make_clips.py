#!/usr/bin/env python3
"""Cut one episode's vertical clips in the client's brand: word-by-word captions in the client's
colours and font, names spelled the way the client's dictionary says, a hook line, the client's logo
and an end card.

    python3 scripts/make_clips.py clients/<client>/episodes/<episode>/batch.json
    python3 scripts/make_clips.py batch.json --preview      # crop check and first/last words, no render
    python3 scripts/make_clips.py batch.json --width 540    # smaller files (examples, drafts)

batch.json (the agent writes it after reading work/transcript.txt; references/batch-file.md has every field):
{
  "client": "example-orbit-podcast",
  "episode": {"id": "ep-112", "title": "...", "source": "source.mp4", "transcript": "work/transcript.json"},
  "clips": [
    {"id": "01", "start": 754.2, "end": 801.9, "why": "the answer stands alone and opens on the point",
     "hook": "Text on screen for the first seconds", "reframe": "fit",
     "cut": [[770.4, 774.9]], "tighten": true, "fillers": true, "snap": true,
     "captions": {"TIKTOK": "...", "INSTAGRAM": "...", "YOUTUBE": "..."}, "title": "..."}
  ]
}

The brand comes from the client's client.json ("brand"): caption accent and text colours, the hook
box colours, uppercase or not, a font file (else Poppins), a logo in a corner and an end card with the
show's name for its last seconds. The client's "names" dictionary is applied to every caption word
("Apollo" never shows as "Appolo"), and the manifest lists each fix. An example client
(client.json "example": true) gets "EXAMPLE ONLY" on screen for the whole clip.

reframe: "auto" (face crop when OpenCV finds one speaker, else fit), "face", "center",
  "fit" (whole frame on a blurred copy of itself, under the hook: screen shares, wide shots),
  "split" (two speakers: "speakers": [{x, y, w, h}, {x, y, w, h}] in source pixels, one above the other),
  "stack" (stream layout: "facecam": {x, y, w, h} on top, gameplay below).
focus_x: 0 to 1, sets the crop by hand. shots: [[source second, focus_x], ...] re-aims the crop at each
  camera switch (read the times from --preview or the episode). zoom: punch-in for crops (default 1.1).
track: [[source second, focus_x], ...] follows a camera move: the crop slides in a straight line from
  one point to the next (shots jump, track glides).
hook_at: "top" puts the hook high in the frame (over hair or background on a close-up), "captions" (the
  default for crops) just above the captions. logo_at: the logo's corner for this clip: top-left,
  top-right, high-left, high-right (high = near the top edge, above most heads) or none. Look at the
  frames (--preview) and keep both off the face in the first seconds.
cut: source-time ranges to remove inside the clip. tighten (off unless set): remove pauses over 0.45 s.
  fillers: remove "um", "uh", stutters and "you know,". snap: fix small slips to sentence edges. Every
  cut inside a clip that tighten or fillers makes is checked against the sound itself: when anything
  louder than the room is in the stretch to be removed (other than the filler), that cut isn't made, so
  a word the transcript timed wrongly is never cut out. When the word times are estimated (a
  transcript made from subtitles), tighten and fillers are off.

Clean edges: a clip starts just before its first word and ends just after its last, never later than
40 ms before the next word in the episode, with a short fade in and out of the sound. An edge in a
pause then takes up to 0.12 s more room tone (still clear of the words around it), so the loop doesn't
feel abrupt; an end on sound (a last word timed short) follows it to the first quiet point, unless that
is past the middle of the next word.

Never adds music, speeds up, mirrors or filters a clip. Writes <episode>/clips/clip-01.mp4 ... (1080x1920
or --width, H.264, AAC, -14 LUFS), a cover frame per clip, contact-sheet.jpg and manifest.json (each
clip's fingerprint, the source time ranges it uses, the names it fixed, the brand it used). Needs ffmpeg
with libx264 and Pillow (pip install pillow). OpenCV is optional: pip install opencv-python-headless.
"""
import argparse, functools, json, os, re, shutil, subprocess, sys, tempfile

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agencylib import (die, guard, is_num, load_zone, probe as probe_file, read_json, rel, sha256,  # noqa: E402
                       user_home, workspace_of, HEX, cut_spec)

W, H = 1080, 1920
# Text is centred on the frame, inside x 180-900 and y 290-1250: clear of the buttons on the right and the platform captions at the bottom.
SAFE_CX = W // 2
CAP_SIZE = 96          # fixed caption size; groups that don't fit are split, never shrunk
CAP_MAX_W = 720
HOOK_SIZE = 78
HOOK_SECONDS = 3.5
MARK_SIZE = 44          # "EXAMPLE ONLY" on example clients' clips
MARK_Y = 1300          # EXAMPLE ONLY line: under the captions, above the apps' own caption area
SAFE_LEFT, SAFE_RIGHT = 80, 900     # the right-side buttons start around x 920
SAFE_TOP, SAFE_BOTTOM = 420, 1340   # below the apps' top tabs, above the apps' captions
STACK_TOP = 760        # stream layout: facecam 1080x760 on top, gameplay 1080x1160 below
EYE_LINE = 0.38        # eyes sit about here in a typical talking-head frame
TOP_UI = 250           # "high": just below the apps' own top tabs, above most heads in a close-up
LOGO_SPOTS = ("top-left", "top-right", "high-left", "high-right", "bottom-left", "bottom-right", "top", "bottom")
FIT_TOP = 690          # fit: the frame sits below the hook box (420 to about 660), never under it
BEST = False           # --best: slower encode, slightly smaller files at the same quality
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "..", "fonts")
FONT_FILES = ["Poppins-ExtraBold.ttf", "Poppins-Bold.ttf"]
BRAND_FONT = [None]    # the client's own font file, when the brand kit names one
END_MAX = 3.0          # an end card longer than 3 s loses viewers before the loop
FONT_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/"
FUNCTION_WORDS = {"a", "an", "the", "of", "to", "for", "and", "that", "with", "on", "in", "is",
                  "so", "but", "i", "or", "at", "as", "if", "by", "from", "my", "your", "our"}
FILLERS = {"um", "uh", "uhm", "erm", "hmm", "mm"}
WARNINGS = []
ESTIMATED = [False]    # word times estimated from subtitles: no cuts inside the clip at guessed times


def warn(msg):
    WARNINGS.append(msg)
    print("warning: " + msg, file=sys.stderr)


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    if r.returncode != 0:
        die("ffmpeg failed: " + (r.stderr.strip().splitlines() or ["no message"])[-1][-600:])
    return r.stdout


def check_ffmpeg():
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        die("ffmpeg is not installed. Mac: brew install ffmpeg. Windows: winget install Gyan.FFmpeg. "
            "Linux: sudo apt install ffmpeg.")
    load_pillow()


def probe(path):
    """(width, height as displayed after any rotation, duration, frame rate to keep, has sound)."""
    info = probe_file(path)
    fps = info["fps"] or 30.0
    # keep the source rate (25 or 29.97 judder when forced to 30) unless it's unusual
    fps_out = info.get("rate") if 23.5 <= fps <= 60.5 and info.get("rate") else "30"
    return info["width"], info["height"], info["duration"], fps_out, info["audio"]


# ---------- speech and timing ----------

def clean(w):
    return re.sub(r"[^\w']", "", w.lower())


ABBREV = {"dr.", "mr.", "mrs.", "ms.", "st.", "jr.", "sr.", "prof.", "vs.", "etc.", "e.g.", "i.e.", "u.s."}


def sentence_end(word):
    w = word["w"].rstrip("\"')]")
    return w[-1:] in ".?!" and w.lower().lstrip("\"'(") not in ABBREV


def in_clip(w, a, b):
    """A word belongs to the clip when it starts inside it, or when the clip starts inside the word and
    most of the word is after that start (a transcriber that timed a word too early: the clip starts at a
    camera cut, and the word is spoken after it)."""
    if w["end"] > b + 0.15:
        return False
    if w["start"] >= a - 0.05:
        return True
    return w["end"] > a and (w["end"] - a) > 0.5 * (w["end"] - w["start"])


def snap_bounds(words, clip):
    """Move start and end to the nearest sentence edge within 4 s; warn when there's none."""
    a, b = float(clip["start"]), float(clip["end"])
    idx = [i for i, w in enumerate(words) if w["start"] >= a - 0.05]
    if not idx:
        return a, b
    i = idx[0]
    starts_ok = lambda j: (j == 0 or sentence_end(words[j - 1])) and (words[j]["w"][:1].isupper() or
                                                                      not words[j]["w"][:1].isalpha())
    if not starts_ok(i) and clip.get("snap", True) is not False:
        # only small slips are fixed automatically; a start further away is the agent's call
        near = [j for j in range(len(words)) if abs(words[j]["start"] - a) <= 1.0 and starts_ok(j)
                and words[j]["start"] < b - 8]
        if near:
            j = min(near, key=lambda j: abs(words[j]["start"] - a))
            print(f"  clip {clip['id']}: start moved {words[j]['start'] - a:+.1f} s to a sentence start", flush=True)
            a = words[j]["start"] - 0.05
        else:
            first = " ".join(w["w"] for w in words[i:i + 5])
            warn(f"clip {clip['id']} starts mid-sentence: '{first}'. Move it, or set \"snap\": false "
                 "if this clause stands alone on purpose")
    inside = [j for j, w in enumerate(words) if in_clip(w, a, b)]
    if inside and not sentence_end(words[inside[-1]]) and clip.get("snap", True) is not False:
        near = [j for j in range(len(words)) if abs(words[j]["end"] - b) <= 4 and sentence_end(words[j])
                and words[j]["end"] > a + 8]
        if near and clip.get("snap", True):
            j = min(near, key=lambda j: abs(words[j]["end"] - b))
            print(f"  clip {clip['id']}: end moved {words[j]['end'] - b:+.1f} s to a sentence end", flush=True)
            b = words[j]["end"] + 0.05
        else:
            last = " ".join(w["w"] for w in words[max(inside[-1] - 4, 0):inside[-1] + 1])
            warn(f"clip {clip['id']} ends mid-sentence: '...{last}'")
    return a, b


def select_words(words, a, b, clip):
    """Words inside the clip, with fillers, stutters and cut ranges marked as removed.
    Returns a list of (word, removed) in order; word end times are capped so silences the
    transcriber stretches over a word count as pauses."""
    ws = [dict(w) for w in words if in_clip(w, a, b)]
    cuts = [(float(s), float(e)) for s, e in clip.get("cut", [])]
    fillers = clip.get("fillers", True) and not ESTIMATED[0]
    if fillers:
        for w in ws:
            w["w"] = destutter(w["w"])
    out = []
    for i, w in enumerate(ws):
        w["end_heard"] = w["end"]
        cap = 0.10 + 0.075 * len(clean(w["w"]))
        w["end"] = min(w["end"], w["start"] + max(cap, 0.12))
        removed = any(s - 0.02 <= w["start"] and w["end"] <= e + 0.02 for s, e in cuts)
        c = clean(w["w"])
        if fillers and not removed:
            nxt = clean(ws[i + 1]["w"]) if i + 1 < len(ws) else None
            if c in FILLERS:
                removed = True
            elif c and c == nxt:  # stutter: keep the second copy
                removed = True
            elif c == "you" and i + 1 < len(ws) and ws[i + 1]["w"].lower().startswith("know,"):
                removed = True
            elif c == "know" and w["w"].endswith(",") and i > 0 and clean(ws[i - 1]["w"]) == "you":
                removed = True
        out.append((w, removed))
    return out


def destutter(word):
    """A stutter inside one caption word: "IF-IF" -> "IF", "THE-THE" -> "THE", "AN-ANOTHER" -> "ANOTHER",
    and a cut-off "DO--" -> "DO". Real hyphenated words ("follow-up", "pre-launch") stay."""
    m = re.fullmatch(r"([\"'(\[]*)([A-Za-z']+)-([A-Za-z']+)(.*)", word)
    if m:
        lead, first, rest, tail = m.groups()
        if rest.lower() == first.lower() or (len(first) <= 3 and rest.lower().startswith(first.lower())
                                             and len(rest) > len(first)):
            return lead + rest + tail
    if word.endswith("--") and len(word) > 2:
        return word.rstrip("-")
    return word


def punch_spans(spans, marked, every=7.0):
    """Split long stretches at the pause nearest their middle, so the alternating punch-in lands on a
    sentence or a breath, never mid-word."""
    words = [w for w, r in marked if not r]
    out = []
    todo = list(spans)
    while todo:
        s, e = todo.pop(0)
        if e - s <= every:
            out.append((s, e))
            continue
        gaps = [((words[i]["end"] + words[i + 1]["start"]) / 2, words[i]["w"][-1:] in ".?!,")
                for i in range(len(words) - 1) if s + 2.5 < words[i]["end"] and words[i + 1]["start"] < e - 2.5]
        if not gaps:
            out.append((s, e))
            continue
        mid = (s + e) / 2
        g = min([x for x, stop in gaps if stop] or [x for x, _ in gaps], key=lambda x: abs(x - mid))
        todo[:0] = [(s, g), (g, e)]
    return out


def neighbours(words, a, b):
    """(end of the last word before the clip, start of the first word after it) in the whole episode."""
    before = [w["end"] for w in words if w["start"] < a - 0.05 and not in_clip(w, a, b)]
    after = [w["start"] for w in words if w["start"] >= a - 0.05 and w["end"] > b + 0.15]
    return (max(before) if before else None), (min(after) if after else None)


def keep_spans(marked, a, b, tighten, prev_end=None, next_start=None):
    """Source-time spans to keep: pauses over 0.45 s and every removed word become cuts. The first span
    starts just before the first word (never into the word before it); the last ends just after the last
    word, never into the next word of the episode."""
    kept = [(w, r) for w, r in marked]
    if not any(not r for _, r in kept):
        return [(a, b)]
    pad, max_gap = 0.12, (0.45 if tighten else 99)
    spans, cur = [], None
    prev_removed = False
    for w, r in kept:
        if r:
            prev_removed = True
            continue
        if cur is None:
            lo = w["start"] - pad
            if prev_end is not None:
                lo = max(lo, min(prev_end + 0.04, w["start"] - 0.02))
            if w["start"] < a:
                lo = a      # the clip starts inside its first word as timed: keep the start that was set
            cur = [lo, w["end"]]
        elif prev_removed or w["start"] - cur[1] > max_gap:
            spans.append((cur[0], cur[1] + pad))
            cur = [w["start"] - pad, w["end"]]
        else:
            cur[1] = max(cur[1], w["end"])
        prev_removed = False
    last = next((w for w, r in reversed(kept) if not r), None)
    end = max(cur[1] + 0.2, last.get("end_heard", cur[1]) + 0.08)   # a little air after the last word
    if next_start is not None:
        end = min(end, max(next_start - 0.04, cur[1] + 0.02))      # never into the next word
    spans.append((cur[0], end))
    merged = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))
    return [(s, e) for s, e in merged if e - s > 0.15]


def audio_levels(src, a, b, step=0.01):
    """Loudness (dB) of the source's sound every `step` seconds from a to b, or None without sound."""
    import array
    rate = 8000
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0.0, a):.3f}", "-t", f"{b - a:.3f}", "-i", src, "-vn",
                        "-ac", "1", "-ar", str(rate), "-f", "s16le", "-"], capture_output=True)
    if r.returncode != 0 or not r.stdout:
        return None
    pcm = array.array("h")
    pcm.frombytes(r.stdout[:len(r.stdout) // 2 * 2])
    if sys.byteorder != "little":
        pcm.byteswap()
    n = int(rate * step)
    out = []
    for i in range(0, len(pcm) - n + 1, n):
        chunk = pcm[i:i + n]
        ms = sum(x * x for x in chunk) / n
        out.append(10 * __import__("math").log10(ms / (32768.0 ** 2)) if ms > 0 else -120.0)
    return {"t0": max(0.0, a), "step": step, "db": out}


def guard_cuts(spans, marked, levels):
    """Merge back every cut inside the clip where the sound in the removed stretch is louder than the room,
    outside the words removed on purpose (fillers, stutters). A transcriber often stretches a word over the
    pause before it, so its times are wrong exactly where a pause would be cut; the sound itself decides.
    Returns (spans, number of cuts kept back)."""
    if not levels or len(spans) < 2 or not levels["db"]:
        return spans, 0
    db, t0, step = levels["db"], levels["t0"], levels["step"]
    thr = _thr(db)
    removed = [(w["start"] - 0.05, w.get("end_heard", w["end"]) + 0.05) for w, r in marked if r]
    out, kept = [list(spans[0])], 0
    for s, e in spans[1:]:
        gap_a, gap_b = out[-1][1], s
        loud, run = False, 0
        i = int((gap_a - t0) / step)
        while gap_a < gap_b and t0 + i * step < gap_b:
            t = t0 + i * step
            if 0 <= i < len(db) and db[i] > thr and not any(x <= t <= y for x, y in removed):
                run += 1
                if run >= 2:
                    loud = True
                    break
            else:
                run = 0
            i += 1
        if loud:
            out[-1][1] = e
            kept += 1
        else:
            out.append([s, e])
    return [tuple(x) for x in out], kept


def _thr(db):
    srt = sorted(db)
    floor, speech = srt[len(srt) // 10], srt[len(srt) * 9 // 10]
    return floor + 0.4 * (speech - floor)


def fit_edges(spans, levels, prev=None, nxt=None, room=0.12, gap=0.04, reach=0.45):
    """Set the clip's outer edges by the sound. `prev` and `nxt` are the (start, end) of the words just
    before and after the clip in the episode.
    - An edge in a pause takes up to `room` seconds more room tone, never closer than `gap` to those words.
    - An end on sound (a last word the transcriber timed short) follows the sound to the first quiet point
      within `reach`, but only when that point comes before the middle of the next word as timed: past
      it, the sound is the next word, and the end stays. A start on sound stays: there the sound is
      nearly always the tail of the word before. The listening check names either."""
    if not levels or not levels["db"] or not spans:
        return spans
    db, t0, step = levels["db"], levels["t0"], levels["step"]
    thr = _thr(db)
    lvl = lambda t: db[min(max(int(round((t - t0) / step)), 0), len(db) - 1)]  # noqa: E731
    out = [list(x) for x in spans]

    def move(t, sign, near, mid):
        if lvl(t) > thr:
            if sign < 0:
                return t
            for k in range(1, int(reach / step) + 1):
                u = t + sign * k * step
                if lvl(u) <= thr:
                    return u if mid is None or sign * (mid - u) > 0 else t
            return t
        k = 0
        while (k + 1) * step <= room + 1e-9 and (near is None or sign * (near - (t + sign * (k + 1) * step)) >= 0) \
                and lvl(t + sign * (k + 1) * step) <= thr:
            k += 1
        return t + sign * k * step

    out[0][0] = max(0.0, move(out[0][0], -1, prev[1] + gap if prev else None,
                              (prev[0] + prev[1]) / 2 if prev else None))
    out[-1][1] = move(out[-1][1], 1, nxt[0] - gap if nxt else None, (nxt[0] + nxt[1]) / 2 if nxt else None)
    return [tuple(x) for x in out]


def to_output_time(t, spans):
    """Map a source time to the time in the cut clip."""
    acc = 0.0
    for s, e in spans:
        if t <= s:
            return acc
        if t <= e:
            return acc + (t - s)
        acc += e - s
    return acc


# ---------- framing ----------

def detect_faces(path, a, b, samples=14):
    try:
        import cv2
        cap = cv2.VideoCapture(path)
        casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        found = []
        for i in range(samples):
            t = a + (b - a) * (i + 0.5) / samples
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ok, frame = cap.read()
            if not ok:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            fw = gray.shape[1]
            faces = casc.detectMultiScale(gray, 1.1, 6, minSize=(max(40, fw // 14),) * 2)
            found.append([(x + w / 2) / fw for x, y, w, h in faces])
        cap.release()
        return found
    except AttributeError:
        warn("OpenCV is installed without its face detector (OpenCV 5 moved it out), so faces weren't found: set "
             "focus_x by hand, or pip install \"opencv-python-headless<5\"")
        return None
    except Exception:
        return None  # no or partial OpenCV install: skip


def choose_frame(clip, src_w, src_h, path):
    mode = clip.get("reframe", "auto")
    if mode == "stack":
        return "stack", 0.5
    if mode == "split":
        return "split", 0.5
    if src_w / src_h <= W / H + 0.01:
        return "vertical", 0.5
    if "focus_x" in clip and mode in ("auto", "face", "center"):
        return "crop", float(clip["focus_x"])
    if mode == "center":
        return "crop", 0.5
    if mode == "fit":
        return "fit", 0.5
    found = detect_faces(path, float(clip["start"]), float(clip["end"]))
    if found is None:
        if mode == "face":
            warn(f"clip {clip['id']}: face mode needs OpenCV (pip install opencv-python-headless); using center")
        return ("fit", 0.5) if src_w / src_h > 2.0 and mode != "face" else ("crop", 0.5)
    with_face = [f for f in found if f]
    if len(with_face) < max(3, len(found) * 0.4):
        return ("crop", 0.5) if mode == "face" else ("fit", 0.5)
    xs = sorted(x for f in with_face for x in f)
    if mode == "auto" and xs[-1] - xs[0] > 0.35 and sum(len(f) > 1 for f in with_face) > len(with_face) * 0.3:
        return "fit", 0.5  # two people far apart: show both
    one = sorted(f[0] if len(f) == 1 else min(f, key=lambda x: abs(x - 0.5)) for f in with_face)
    return "crop", one[len(one) // 2]


def box(b, src_w, src_h):
    """A {x, y, w, h} box in source pixels, kept inside the frame and even-sized for ffmpeg."""
    x, y = int(max(0, min(b["x"], src_w - 16))), int(max(0, min(b["y"], src_h - 16)))
    w, h = int(min(b["w"], src_w - x)) // 2 * 2, int(min(b["h"], src_h - y)) // 2 * 2
    return x, y, w, h


def track_x(clip, s0, cw, src_w):
    """The crop's x as an ffmpeg expression of the span's own time t, sliding between the clip's track
    points (source seconds), or None without a track."""
    pts = sorted((float(t) - s0, float(fx)) for t, fx in (clip or {}).get("track") or [])
    if not pts:
        return None
    px = [(t, min(max(fx * src_w - cw / 2, 0), src_w - cw)) for t, fx in pts]
    expr = f"{px[-1][1]:.1f}"
    for (ta, xa), (tb, xb) in reversed(list(zip(px, px[1:]))):
        if tb - ta < 0.01:
            continue
        expr = f"if(lt(t,{tb:.3f}),{xa:.1f}+({xb - xa:.1f})*(t-{ta:.3f})/{tb - ta:.3f},{expr})"
    return f"if(lt(t,{px[0][0]:.3f}),{px[0][1]:.1f},{expr})"


def frame_filter(kind, focus, src_w, src_h, zoom, tag, clip=None, s0=0.0):
    """Filter chain from a span's frames to 1080x1920. zoom > 1 punches in, eyes kept level."""
    if kind == "stack":
        fx, fy, fw, fh = box(clip["facecam"], src_w, src_h)
        g = clip.get("game") or {"x": 0, "y": 0, "w": src_w, "h": src_h}
        gx, gy, gw, gh = box(g, src_w, src_h)
        if zoom > 1.0:   # the punch-in lands on the gameplay; the facecam stays as it is
            nw, nh = int(gw / zoom) // 2 * 2, int(gh / zoom) // 2 * 2
            gx, gy, gw, gh = gx + (gw - nw) // 2, gy + (gh - nh) // 2, nw, nh
        bot = H - STACK_TOP
        return (f"split=2[f{tag}][g{tag}];[f{tag}]crop={fw}:{fh}:{fx}:{fy},scale={W}:{STACK_TOP}:"
                f"force_original_aspect_ratio=increase,crop={W}:{STACK_TOP}[ft{tag}];[g{tag}]crop={gw}:{gh}:{gx}:{gy},"
                f"scale={W}:{bot}:force_original_aspect_ratio=increase,crop={W}:{bot}[gt{tag}];[ft{tag}][gt{tag}]vstack")
    if kind == "split":
        (ax, ay, aw, ah), (bx, by, bw, bh) = (box(b, src_w, src_h) for b in clip["speakers"][:2])
        half = H // 2
        return (f"split=2[sa{tag}][sb{tag}];[sa{tag}]crop={aw}:{ah}:{ax}:{ay},scale={W}:{half}:"
                f"force_original_aspect_ratio=increase,crop={W}:{half}[ta{tag}];[sb{tag}]crop={bw}:{bh}:{bx}:{by},"
                f"scale={W}:{half}:force_original_aspect_ratio=increase,crop={W}:{half}[tb{tag}];[ta{tag}][tb{tag}]vstack")
    if kind == "vertical":
        return f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
    if kind == "crop":
        ch = int(src_h / zoom) // 2 * 2
        cw = int(ch * W / H) // 2 * 2
        x = int(min(max(focus * src_w - cw / 2, 0), src_w - cw))
        y = int(min(max(EYE_LINE * src_h * (1 - 1 / zoom), 0), src_h - ch))
        tx = track_x(clip, s0, cw, src_w)
        xs = f"'{tx}'" if tx else str(x)
        return f"crop={cw}:{ch}:{xs}:{y},scale={W}:{H}:flags=lanczos"
    return (f"split=2[bg{tag}][fg{tag}];[bg{tag}]scale={W}:{H}:force_original_aspect_ratio=increase,"
            f"crop={W}:{H},gblur=sigma=40,eq=brightness=-0.15[bgb{tag}];[fg{tag}]scale={W}:-2[fgs{tag}];"
            f"[bgb{tag}][fgs{tag}]overlay=(W-w)/2:min(max((H-h)/2\\,{FIT_TOP})\\,H-h)")


# ---------- captions ----------
# Drawn with Pillow and laid over the video, so any ffmpeg build works
# (many builds, including Homebrew's, ship without libass or drawtext).

def load_pillow():
    try:
        from PIL import Image, ImageDraw, ImageFont
        return Image, ImageDraw, ImageFont
    except ImportError:
        die("captions need Pillow: pip install pillow (python3 scripts/check_setup.py checks everything)")


@functools.lru_cache(maxsize=None)
def caption_font(size):
    _, _, ImageFont = load_pillow()
    if BRAND_FONT[0]:
        return ImageFont.truetype(BRAND_FONT[0], size)
    cache = os.path.join(user_home(), "fonts")   # never written into the skill's own folder
    for d in (FONT_DIR, cache):
        for name in FONT_FILES:
            path = os.path.join(d, name)
            if os.path.exists(path) and os.path.getsize(path) > 10000:
                return ImageFont.truetype(path, size)
    os.makedirs(cache, exist_ok=True)
    path = os.path.join(cache, FONT_FILES[0])
    try:  # some skill registries strip binary files; fetch the open-licensed font once
        import urllib.request
        urllib.request.urlretrieve(FONT_URL + FONT_FILES[0], path)
    except Exception:
        if shutil.which("curl"):
            subprocess.run(["curl", "-sfL", FONT_URL + FONT_FILES[0], "-o", path], check=False)
    if os.path.exists(path) and os.path.getsize(path) > 10000:
        return ImageFont.truetype(path, size)
    warn("caption font missing; using Pillow's default font")
    return ImageFont.load_default(size)


@functools.lru_cache(maxsize=None)
def _measure():
    Image, ImageDraw, _ = load_pillow()
    return ImageDraw.Draw(Image.new("RGBA", (10, 10)))


def text_w(text, size):
    return _measure().textlength(text, font=caption_font(size))


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def balanced_lines(words, size, max_w, max_lines=2):
    """Split words into at most max_lines lines of similar width."""
    lines, cur = [], []
    for w in words:
        if cur and text_w(" ".join(cur + [w]), size) > max_w:
            lines.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(cur)
    if len(lines) == 2:  # balance two lines
        best = lines
        for k in range(1, len(words)):
            a, b = words[:k], words[k:]
            wa, wb = text_w(" ".join(a), size), text_w(" ".join(b), size)
            if max(wa, wb) <= max_w and max(wa, wb) < max(text_w(" ".join(x), size) for x in best):
                best = [a, b]
        lines = best
    return lines


@functools.lru_cache(maxsize=None)
def logo_image(path, scale, opacity):
    """The client's logo, sized to `scale` of the frame's width (at most 300 px tall), at `opacity`."""
    Image, _, _ = load_pillow()
    im = Image.open(path).convert("RGBA")
    w = max(40, int(W * scale))
    h = max(1, int(im.height * w / im.width))
    if h > 300:
        w, h = max(1, int(w * 300 / h)), 300
    im = im.resize((w, h), Image.LANCZOS)
    if opacity < 1:
        alpha = im.getchannel("A").point(lambda a: int(a * opacity))
        im.putalpha(alpha)
    return im


def place(position, w, h):
    """Top-left corner for a w x h item at a named position, inside the safe area every app leaves
    clear: right of x 80, left of the button rail at x 900, below the top tabs, above the captions
    the apps draw at the bottom."""
    if position.endswith("left"):
        x = SAFE_LEFT
    elif position.endswith("right"):
        x = SAFE_RIGHT - w
    else:
        x = (W - w) // 2
    if position.startswith("high"):
        y = TOP_UI
    elif position.startswith("top"):
        y = SAFE_TOP
    elif position.startswith("bottom"):
        y = SAFE_BOTTOM - h
    else:
        y = (H - h) // 2
    return int(max(SAFE_LEFT // 2, x)), int(y)



def logo_box(brand):
    """(logo image, (x, y)) for the client's logo, or (None, None)."""
    if not brand.get("logo_path"):
        return None, None
    logo = logo_image(brand["logo_path"], brand.get("logo_scale") or 0.16, brand.get("logo_opacity") or 0.9)
    return logo, place(brand.get("logo_position") or "top-right", logo.width, logo.height)


def draw_mark(img, draw, brand, logo=True):
    """The client's logo in its corner, and "EXAMPLE ONLY" across the bottom on an example client's clips."""
    im, xy = logo_box(brand) if logo else (None, None)
    if im is not None:
        img.alpha_composite(im, xy)
    if brand.get("mark"):
        f = caption_font(MARK_SIZE)
        tw = int(text_w(brand["mark"], MARK_SIZE))
        draw.text((SAFE_CX - tw // 2, MARK_Y - MARK_SIZE // 2), brand["mark"], font=f, fill=(255, 255, 255, 220),
                  stroke_width=4, stroke_fill=(0, 0, 0, 200))


def render_overlay(path, cap_words, hook, brand, cap_y, hook_bottom, hook_top=None):
    """One transparent 1080x1920 frame: caption (spoken word in the accent), the hook in the client's
    hook colours, the client's logo and, on example clients, the EXAMPLE ONLY line."""
    Image, ImageDraw, _ = load_pillow()
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    show_logo = True
    accent = hexrgb(brand.get("accent", "#FFD43B"))
    text_col = hexrgb(brand.get("text", "#FFFFFF"))
    if hook:
        # two lines at 78 to 70 px; if it needs more, three lines at full size (never drop words)
        size, lines = HOOK_SIZE, balanced_lines(hook.split(), HOOK_SIZE, 640)
        for trial in range(HOOK_SIZE - 4, 69, -4):
            if len(lines) <= 2:
                break
            alt = balanced_lines(hook.split(), trial, 640)
            if len(alt) <= 2:
                size, lines = trial, alt
        if len(lines) > 2:
            size, lines = HOOK_SIZE, balanced_lines(hook.split(), HOOK_SIZE, 640)
        f = caption_font(size)
        lh = int(size * 1.18)
        box_h = lh * len(lines) + 56
        box_w = max(text_w(" ".join(ln), size) for ln in lines) + 80
        y0 = hook_top if hook_top is not None else hook_bottom - box_h
        x0 = SAFE_CX - box_w / 2
        im, xy = logo_box(brand)
        if im is not None and xy[0] < x0 + box_w and x0 < xy[0] + im.width and xy[1] < y0 + box_h and y0 < xy[1] + im.height:
            # the hook would cover the logo: move the hook under it, or leave the logo out while the hook shows
            below = xy[1] + im.height + 16
            if hook_top == TOP_UI:
                show_logo = False   # a hook placed high on purpose stays there; the logo returns after it
            elif below + box_h <= cap_y - int(CAP_SIZE * 1.18) - 24:
                y0 = below
            else:
                show_logo = False
        draw.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], 24, fill=hexrgb(brand.get("hook_bg", "#FFFFFF")) + (255,))
        for i, ln in enumerate(lines):
            draw.text((SAFE_CX, y0 + 28 + i * lh + lh / 2), " ".join(ln), font=f,
                      fill=hexrgb(brand.get("hook_text", "#000000")) + (255,), anchor="mm")
    draw_mark(img, draw, brand, show_logo)
    if cap_words:
        f = caption_font(CAP_SIZE)
        space = text_w(" ", CAP_SIZE)
        total = sum(text_w(w, CAP_SIZE) for w, _ in cap_words) + space * (len(cap_words) - 1)
        x = SAFE_CX - total / 2
        y = cap_y - int(CAP_SIZE * 1.18)
        for w, active in cap_words:
            fill = accent + (255,) if active else text_col + (255,)
            draw.text((x, y + 6), w, font=f, fill=(0, 0, 0, 140))  # soft drop shadow
            draw.text((x, y), w, font=f, fill=fill, stroke_width=8, stroke_fill=(0, 0, 0, 255))
            x += text_w(w, CAP_SIZE) + space
    img.save(path, optimize=True)


def end_card(path, brand):
    """The end card: the show's line (and the logo) on the brand's colour, full frame."""
    Image, ImageDraw, _ = load_pillow()
    ec = brand["end_card"]
    img = Image.new("RGBA", (W, H), hexrgb(ec.get("bg") or "#111111") + (255,))
    draw = ImageDraw.Draw(img)
    y = H // 2 - 120
    if brand.get("logo_path"):
        logo = logo_image(brand["logo_path"], 0.36, 1.0)
        img.alpha_composite(logo, ((W - logo.width) // 2, max(SAFE_TOP, y - logo.height - 40)))
    lines = balanced_lines(ec["text"].split(), HOOK_SIZE, 820, max_lines=3)
    f = caption_font(HOOK_SIZE)
    lh = int(HOOK_SIZE * 1.25)
    for i, ln in enumerate(lines):
        draw.text((SAFE_CX, y + i * lh + lh / 2), " ".join(ln), font=f,
                  fill=hexrgb(ec.get("color") or brand.get("text", "#FFFFFF")) + (255,), anchor="mm")
    if brand.get("mark"):
        draw_mark(img, draw, {"mark": brand["mark"]})
    img.convert("RGB").save(path, quality=92)


def fix_names(kept, names):
    """Apply the client's names dictionary to caption words, also across two or three words ("moon walk"
    becomes "Moonwalk"). The words stay in the sound; only what is written changes. Returns the fixes."""
    if not isinstance(names, dict) or not kept:
        return []
    fixes = []
    pairs = []
    for right, wrongs in names.items():
        if isinstance(right, str) and right.strip():
            for v in set([right] + [x for x in (wrongs if isinstance(wrongs, list) else []) if isinstance(x, str) and x.strip()]):
                pairs.append(([clean(t) for t in v.split()], right.strip()))
    pairs.sort(key=lambda p: -len(p[0]))
    i = 0
    while i < len(kept):
        for toks, right in pairs:
            n = len(toks)
            if i + n <= len(kept) and [clean(kept[i + k]["w"]) for k in range(n)] == toks:
                last = kept[i + n - 1]["w"]
                tail = re.search(r"[^\w']*$", last).group(0)
                lead = re.match(r"^[^\w']*", kept[i]["w"]).group(0)
                found = " ".join(kept[i + k]["w"] for k in range(n))
                new = lead + right + tail
                if new != found:
                    fixes.append({"from": found, "to": right})
                kept[i]["w"] = new
                kept[i]["end"] = kept[i + n - 1]["end"]
                del kept[i + 1:i + n]
                break
        i += 1
    return fixes


COMMON_CAPS = {"well", "really", "it's", "so", "but", "yes", "no", "now", "think", "just"}


def mid_caps(words):
    """Transcribers capitalize the first word of each stretch they hear, so a caption reads "my Emotions".
    A capitalized word right after a word that doesn't end a sentence is lower-cased when the episode
    also has it in lower case, or it is a common word; names ("Earth", "NASA", "I") keep theirs."""
    lower = {clean(w["w"]) for w in words if str(w.get("w", ""))[:1].islower()}
    out = []
    for i, w in enumerate(words):
        t = str(w.get("w", ""))
        if i and t[:1].isupper() and t[1:2].islower() and clean(t) not in {"i", "i'm", "i'd", "i've", "i'll"} \
                and str(words[i - 1].get("w", ""))[-1:] not in ".?!" \
                and (clean(t) in lower or clean(t) in FUNCTION_WORDS or clean(t) in COMMON_CAPS):
            w = dict(w, w=t[:1].lower() + t[1:])
        out.append(w)
    return out


def caption_groups(kept, upper):
    """Up to 3 words per caption, one line at a fixed size. Breaks at punctuation and pauses;
    a group never ends on a small word like "the" or "of"."""
    groups, cur = [], []
    for i, w in enumerate(kept):
        cur.append(w)
        nxt = kept[i + 1] if i + 1 < len(kept) else None
        txt = lambda g: " ".join((x["w"].upper() if upper else x["w"]) for x in g)
        too_wide = nxt is not None and text_w(txt(cur + [nxt]), CAP_SIZE) > CAP_MAX_W
        brk = (nxt is None or len(cur) >= 3 or w["w"][-1:] in ".?!,;:" or too_wide
               or nxt["start"] - w["end"] > 0.25)
        if brk and nxt is not None and clean(w["w"]) in FUNCTION_WORDS and w["w"][-1:] not in ".?!,;:" \
                and len(cur) > 1:
            groups.append(cur[:-1])  # carry the small word to the next group
            cur = [cur[-1]]
            continue
        if brk:
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return [g for g in groups if g]




def build_overlays(clip, marked, spans, brand, length, frame_kind, tmp, names=None):
    """Write PNG overlays plus an ffmpeg concat list that shows each one for the right time. Returns the
    list file and the names the dictionary fixed."""
    if clip.get("logo_at") == "none":
        brand = dict(brand, logo_path=None)
    elif clip.get("logo_at") in LOGO_SPOTS:
        brand = dict(brand, logo_position=clip["logo_at"])
    upper = brand.get("uppercase", False)
    cap_y = int(brand.get("caption_y", 1230))
    cap_top = cap_y - int(CAP_SIZE * 1.18)
    hook = clip.get("hook") if brand.get("hook", True) else None
    kept = [dict(w) for w, r in marked if not r]
    if kept and kept[0]["w"][:1].islower():
        kept[0]["w"] = kept[0]["w"][:1].upper() + kept[0]["w"][1:]  # a clip that starts mid-sentence still reads as one
    fixes = fix_names(kept, names)
    if hook:
        if len(hook.split()) > 10:
            warn(f"clip {clip['id']}: hook has {len(hook.split())} words; 8 or fewer reads in time")
        spoken = " ".join(clean(w["w"]) for w in kept if to_output_time(w["start"], spans) < 10)
        hook_c = " ".join(clean(x) for x in hook.split())
        if len(hook_c.split()) >= 3 and hook_c in spoken:
            warn(f"clip {clip['id']}: the hook repeats words spoken in the first 10 s; say something new")
    hook_windows = []
    if hook:
        hook_windows.append((0.0, min(HOOK_SECONDS, length)))
        if length > 40:
            mid = length * 0.5
            hook_windows.append((mid, min(mid + 2.0, length)))
    # crop: hook sits just above the captions (the face fills the top); fit: at the top
    hook_top = SAFE_TOP if frame_kind == "fit" else None
    if clip.get("hook_at") == "top":
        hook_top = TOP_UI
    hook_bottom = cap_top - 36
    events = []
    timed = [[(to_output_time(w["start"], spans), to_output_time(w["end"], spans), w["w"]) for w in g]
             for g in caption_groups(kept, upper)]
    for gi, tw in enumerate(timed):
        next_start = timed[gi + 1][0][0] if gi + 1 < len(timed) else length
        for i, (s, e, _) in enumerate(tw):
            end = tw[i + 1][0] if i + 1 < len(tw) else min(next_start, max(e + 0.1, tw[0][0] + 0.4))
            if next_start - end < 0.15:
                end = next_start  # no flicker between groups
            if end - s < 0.02:
                continue
            events.append((s, end, [((ww.upper() if upper else ww), j == i) for j, (_, _, ww) in enumerate(tw)]))
    cuts = {0.0, length} | {t for s, e, _ in events for t in (s, e)} | {t for w in hook_windows for t in w}
    cuts = sorted(c for c in cuts if 0 <= c <= length)
    rendered, listing = {}, []
    for a, b in zip(cuts, cuts[1:]):
        if b - a < 0.005:
            continue
        mid = (a + b) / 2
        cap = next((w for s, e, w in events if s <= mid < e), None)
        show_hook = hook if any(s <= mid < e for s, e in hook_windows) else None
        key = (tuple(cap) if cap else None, show_hook)
        if key not in rendered:
            name = f"o{clip['id']}-{len(rendered):04d}.png"
            render_overlay(os.path.join(tmp, name), cap, show_hook, brand, cap_y, hook_bottom, hook_top)
            rendered[key] = name
        listing.append((rendered[key], b - a))
    if not listing:
        name = f"o{clip['id']}-blank.png"
        render_overlay(os.path.join(tmp, name), None, None, brand, cap_y, hook_bottom, hook_top)
        listing = [(name, length)]
    lst = f"overlays-{clip['id']}.txt"
    with open(os.path.join(tmp, lst), "w", encoding="utf-8") as fh:
        fh.write("ffconcat version 1.0\n")
        for name, d in listing:
            fh.write(f"file '{name}'\nduration {d:.3f}\n")
        fh.write(f"file '{listing[-1][0]}'\n")  # the concat demuxer needs the last file twice
    return lst, fixes


# ---------- render ----------

def plan_clip(clip, words, src, src_w, src_h):
    a, b = snap_bounds(words, clip)
    if b <= a:
        die(f"clip {clip['id']}: end must be after start")
    marked = select_words(words, a, b, clip)
    prev_end, next_start = neighbours(words, a, b)
    spans = keep_spans(marked, a, b, clip.get("tighten", False) is True and not ESTIMATED[0], prev_end, next_start)
    levels = audio_levels(src, a - 1.0, b + 1.0)
    if len(spans) > 1:
        spans, back = guard_cuts(spans, marked, levels)
        if back:
            print(f"  clip {clip['id']}: {back} cut(s) inside the clip not made: there is sound in them", flush=True)
    first = next((w for w, r in marked if not r), None)
    if first is not None and first["start"] < a:
        prev_w = (a - 0.04, a - 0.04)     # a start set inside a mistimed word (a camera cut) is kept as set
    else:
        prev_w = next(((w["start"], w["end"]) for w in reversed(words) if w["end"] == prev_end), None) \
            if prev_end is not None else None
    next_w = next(((w["start"], w["end"]) for w in words if w["start"] == next_start), None) \
        if next_start is not None else None
    spans = fit_edges(spans, levels, prev_w, next_w)
    for s, e in clip.get("cut", []):  # remove cut ranges even where no word was spoken
        spans = [p for sp in spans for p in ((sp[0], min(sp[1], s)), (max(sp[0], e), sp[1])) if p[1] - p[0] > 0.15]
    length = sum(e - s for s, e in spans)
    kind, focus = choose_frame(clip, src_w, src_h, src)
    if clip.get("punch") and kind in ("crop", "stack"):
        spans = punch_spans(spans, marked)
    if clip.get("shots") and kind == "crop":
        cuts_at = sorted(float(t) for t, _ in clip["shots"])
        out = []
        for s_, e_ in spans:
            for t in cuts_at:
                if s_ + 0.1 < t < e_ - 0.1:
                    out.append((s_, t))
                    s_ = t
            out.append((s_, e_))
        spans = out
    return a, b, marked, spans, length, kind, focus


def focus_at(clip, t, focus):
    """The crop position for a span starting at source time t: the last shot change before it."""
    best = focus
    for st, fx in sorted((float(x), float(y)) for x, y in clip.get("shots") or []):
        if st <= t + 0.05:
            best = fx
    return best




def render_clip(clip, src, words, brand, tmp, out_dir, src_w, src_h, fps, width=W, has_audio=True, names=None):
    a, b, marked, spans, length, kind, focus = plan_clip(clip, words, src, src_w, src_h)
    if length < 8:
        warn(f"clip {clip['id']}: only {length:.0f} s long")
    if length > 180:
        warn(f"clip {clip['id']}: {length:.0f} s is over the 3-minute limit for Shorts and TikTok's API")
    elif length > 60:
        warn(f"clip {clip['id']}: {length:.0f} s; most strong clips are 25 to 45 s, and YouTube blocks Shorts over "
             "60 s that get a Content ID claim (keep it under 60 s if any music or footage isn't the client's)")
    zoom = float(clip.get("zoom", 1.1 if kind == "crop" else 1.0))
    if kind == "crop" and src_h * W / H / zoom < width * 0.5:
        warn(f"clip {clip['id']}: a {src_h}p source is enlarged about {H * zoom / src_h:.1f}x in a crop; "
             "it will look soft. Use \"reframe\": \"fit\" or a bigger source")
    overlay_list, fixes = build_overlays(clip, marked, spans, brand, length, kind, tmp, names)
    seek = max(0.0, a - 3)
    parts, labels = [], []
    for i, (s, e) in enumerate(spans):
        # crops alternate a small punch-in at each cut, so removed pauses read as edits, not glitches
        z = zoom * (1.12 if i % 2 == 1 and (kind == "crop" or (kind == "stack" and clip.get("punch"))) else 1.0)
        fade_out = 0.06 if i == len(spans) - 1 else 0.01
        fade_in = 0.03 if i == 0 else 0.01
        audio = (f"[0:a]atrim=start={s - seek:.3f}:end={e - seek:.3f},asetpts=PTS-STARTPTS,"
                 f"afade=t=in:d={fade_in},afade=t=out:st={max(0, e - s - fade_out):.3f}:d={fade_out}[a{i}]" if has_audio
                 else f"aevalsrc=0:c=stereo:s=48000:d={e - s:.3f}[a{i}]")
        parts.append(f"[0:v]trim=start={s - seek:.3f}:end={e - seek:.3f},setpts=PTS-STARTPTS,"
                     f"{frame_filter(kind, focus_at(clip, s, focus), src_w, src_h, z, i, clip, s)},setsar=1[v{i}];{audio}")
        labels.append(f"[v{i}][a{i}]")
    out_h = int(width * H / W) // 2 * 2
    graph = ";".join(parts) + f";{''.join(labels)}concat=n={len(spans)}:v=1:a=1[cv][ca];"
    graph += f"[cv]fps={fps}[base];[1:v]fps={fps},format=yuva420p[ov];"
    final = "" if width == W else f",scale={width}:{out_h}:flags=lanczos"
    graph += f"[base][ov]overlay=0:0:format=yuv420:shortest=0:eof_action=pass{final},format=yuv420p,setsar=1[vm];"
    graph += ("[ca]highpass=f=80,loudnorm=I=-14:TP=-1:LRA=11,aresample=48000[am];" if has_audio
              else "[ca]anull[am];")
    inputs = ["-ss", f"{seek:.3f}", "-t", f"{b - seek + 1:.3f}", "-i", os.path.abspath(src),
              "-f", "concat", "-safe", "0", "-i", overlay_list]
    ec = brand.get("end_card")
    end_s = 0.0
    if ec:
        end_s = float(ec.get("seconds") or 1.5)
        card = os.path.join(tmp, f"end-{clip['id']}.jpg")
        end_card(card, brand)
        inputs += ["-loop", "1", "-framerate", str(fps), "-t", f"{end_s:.3f}", "-i", card]
        graph += (f"[2:v]scale={width}:{out_h}:flags=lanczos,fps={fps},format=yuv420p,setsar=1[ev];"
                  f"aevalsrc=0:c=stereo:s=48000:d={end_s:.3f}[ea];[vm][am][ev][ea]concat=n=2:v=1:a=1[v][a]")
    else:
        graph += "[vm]null[v];[am]anull[a]"
    out = os.path.abspath(os.path.join(out_dir, f"clip-{clip['id']}.mp4"))
    print(f"  clip {clip['id']}: {length + end_s:.1f} s, {kind}" + (f" x={focus:.2f} zoom {zoom}" if kind == "crop" else ""),
          flush=True)
    run(["ffmpeg", "-y", "-v", "error", *inputs,
         "-filter_complex", graph, "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "medium" if BEST else "veryfast",
         "-crf", ("19" if BEST else "20") if width == W else "27" if width > 432 else "30",
         "-profile:v", "high", "-maxrate", "12M", "-bufsize", "24M", "-g", "60", "-keyint_min", "30",
         "-bf", "2", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
         "-c:a", "aac", "-b:a", "192k" if width == W else "128k" if width > 432 else "64k", "-ac", "2", "-movflags", "+faststart",
         "-map_metadata", "-1", out], cwd=tmp)
    cover = os.path.join(out_dir, f"clip-{clip['id']}-cover.jpg")
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{min(1.0, length / 2):.2f}", "-i", out,
         "-frames:v", "1", "-q:v", "4", cover])
    return {"id": clip["id"], "file": rel(out, out_dir), "sha256": sha256(out), "bytes": os.path.getsize(out),
            "seconds": round(length + end_s, 1), "end_card_seconds": round(end_s, 2),
            "window": [round(a, 2), round(b, 2)], "ranges": [[round(s, 2), round(e, 2)] for s, e in spans],
            "framing": kind, "hook": clip.get("hook", ""), "names_fixed": fixes, "cover": rel(cover, out_dir),
            "spec": cut_spec(clip)}


def preview(clip, words, src, src_w, src_h, out_dir):
    """Three source frames with the planned 9:16 crop drawn on, plus the snapped first and last
    words. Look at it before rendering; adjust focus_x, reframe or the times if needed."""
    Image, ImageDraw, _ = load_pillow()
    a, b, marked, spans, length, kind, focus = plan_clip(clip, words, src, src_w, src_h)
    zoom = float(clip.get("zoom", 1.1 if kind == "crop" else 1.0))
    frames = []
    for i, t in enumerate((a + 1, (a + b) / 2, b - 1)):
        p = os.path.join(out_dir, f"preview-{clip['id']}-{i}.jpg")
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(0, t):.2f}", "-i", src, "-frames:v", "1", "-q:v", "4", p])
        im = Image.open(p).convert("RGB")
        if kind == "split":
            d = ImageDraw.Draw(im)
            for b in clip["speakers"][:2]:
                x, y, w, h = box(b, src_w, src_h)
                d.rectangle([x, y, x + w, y + h], outline=(255, 212, 59), width=max(4, src_w // 240))
        if kind == "stack":
            d = ImageDraw.Draw(im)
            for b, col in ((clip["facecam"], (255, 212, 59)), (clip.get("game") or {"x": 0, "y": 0, "w": src_w, "h": src_h},
                                                                (80, 200, 255))):
                x, y, w, h = box(b, src_w, src_h)
                d.rectangle([x, y, x + w, y + h], outline=col, width=max(4, src_w // 240))
        if kind == "crop":
            ch = src_h / zoom
            cw = ch * W / H
            x = min(max(focus * src_w - cw / 2, 0), src_w - cw)
            y = min(max(EYE_LINE * src_h * (1 - 1 / zoom), 0), src_h - ch)
            ImageDraw.Draw(im).rectangle([x, y, x + cw, y + ch], outline=(255, 212, 59), width=max(4, src_w // 240))
        frames.append(im.resize((640, int(640 * src_h / src_w))))
        os.remove(p)
    sheet = Image.new("RGB", (640 * 3 + 20, frames[0].height), "#222222")
    for i, f in enumerate(frames):
        sheet.paste(f, (i * 650, 0))
    path = os.path.join(out_dir, f"preview-{clip['id']}.jpg")
    sheet.save(path, quality=85)
    kept = [w["w"] for w, r in marked if not r]
    print(f"  clip {clip['id']}: {kind}" + (f" focus_x={focus:.2f}" if kind == "crop" else "")
          + f", {length:.1f} s after tightening -> {path}")
    print(f"     starts: \"{' '.join(kept[:8])} ...\"")
    print(f"     ends:   \"... {' '.join(kept[-8:])}\"")




def contact_sheet(covers, path):
    if not covers:
        return None
    n = len(covers)
    cols = min(5, n)
    inputs = []
    for c in covers:
        inputs += ["-i", c]
    if n == 1:
        graph = "[0:v]scale=270:480[out]"
    else:
        layout = "|".join(f"{(i % cols) * 270}_{(i // cols) * 480}" for i in range(n))
        graph = ("".join(f"[{i}:v]scale=270:480[t{i}];" for i in range(n)) + "".join(f"[t{i}]" for i in range(n))
                 + f"xstack=inputs={n}:layout={layout}:fill=black[out]")
    run(["ffmpeg", "-y", "-v", "error", *inputs, "-filter_complex", graph, "-map", "[out]",
         "-frames:v", "1", "-q:v", "3", path])
    return os.path.abspath(path)




def brand_of(client, cdir):
    """The brand kit from client.json, checked: colours are #RRGGBB, the logo and font files exist."""
    b = client.get("brand") if isinstance(client.get("brand"), dict) else {}
    out = {"hook": b.get("hook", True) is not False, "uppercase": b.get("uppercase") is True}
    for k, default in (("accent", "#FFD43B"), ("text", "#FFFFFF"), ("hook_bg", "#FFFFFF"), ("hook_text", "#000000")):
        v = b.get(k) or default
        if not isinstance(v, str) or not HEX.fullmatch(v):
            die(f"client.json brand.{k} must be a colour like #FFD43B")
        out[k] = v
    if is_num(b.get("caption_y")) and 900 <= b["caption_y"] <= 1300:
        out["caption_y"] = int(b["caption_y"])
    if b.get("logo"):
        path = b["logo"] if os.path.isabs(b["logo"]) else os.path.join(cdir, b["logo"])
        if not os.path.isfile(path):
            die(f"the brand logo {b['logo']} isn't there (paths are from the client's folder)")
        out["logo_path"] = path
        out["logo_position"] = b.get("logo_position") or "top-right"
        if out["logo_position"] not in LOGO_SPOTS:
            die("client.json brand.logo_position is one of " + ", ".join(LOGO_SPOTS))
        if is_num(b.get("logo_scale")) and 0.05 <= b["logo_scale"] <= 0.4:
            out["logo_scale"] = b["logo_scale"]
    if b.get("font"):
        path = b["font"] if os.path.isabs(b["font"]) else os.path.join(cdir, b["font"])
        if not os.path.isfile(path) or not path.lower().endswith((".ttf", ".otf")):
            die(f"the brand font {b['font']} isn't a .ttf or .otf file in the client's folder")
        BRAND_FONT[0] = path
    ec = b.get("end_card")
    if isinstance(ec, dict) and isinstance(ec.get("text"), str) and ec["text"].strip():
        secs = ec.get("seconds", 1.5)
        if not is_num(secs) or not 0.5 <= secs <= END_MAX:
            die(f"client.json brand.end_card.seconds is 0.5 to {END_MAX:g}")
        for k in ("bg", "color"):
            if ec.get(k) and not (isinstance(ec[k], str) and HEX.fullmatch(ec[k])):
                die(f"client.json brand.end_card.{k} must be a colour like #101820")
        out["end_card"] = {"text": ec["text"].strip(), "seconds": float(secs), "bg": ec.get("bg"), "color": ec.get("color")}
    if client.get("example") is True:
        out["mark"] = "EXAMPLE ONLY"
    return out


CLIP_ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,39}")   # lower case only: "A" and "a" are one file on macOS and Windows


def check_clip(c, total, src_w, src_h):
    """Stop on a clip entry that can't be cut: a bad id (it becomes a file name), times or numbers that
    aren't numbers, a stack layout without its facecam box."""
    if not isinstance(c, dict) or "id" not in c or "start" not in c or "end" not in c:
        die("every clip needs an id, a start and an end (seconds in the source)")
    c["id"] = str(c["id"]).zfill(2)
    if not CLIP_ID.fullmatch(c["id"]):
        die(f"clip id {c['id']!r}: use lowercase letters, digits, dashes or underscores only (it becomes the file name)")
    for k in ("start", "end", "zoom", "focus_x"):
        if k in c and not is_num(c[k], 0):
            die(f"clip {c['id']}: {k} must be a number" + (" of seconds in the source" if k in ("start", "end") else ""))
    if float(c["end"]) <= float(c["start"]):
        die(f"clip {c['id']}: end must be after start")
    if "focus_x" in c and c["focus_x"] > 1:
        die(f"clip {c['id']}: focus_x is 0 (left) to 1 (right)")
    if "zoom" in c and not 1.0 <= c["zoom"] <= 2.0:
        die(f"clip {c['id']}: zoom is 1.0 (none) to 2.0")
    cut = c.get("cut", [])
    if not isinstance(cut, list) or not all(isinstance(r, list) and len(r) == 2 and all(is_num(x, 0) for x in r)
                                            and r[1] > r[0] for r in cut):
        die(f"clip {c['id']}: cut is a list of [start, end] pairs in seconds of the source")
    if c.get("reframe", "auto") not in ("auto", "face", "center", "fit", "stack", "split"):
        die(f"clip {c['id']}: reframe is auto, face, center, fit, split or stack")
    if c.get("reframe") == "split":
        sp = c.get("speakers")
        if not (isinstance(sp, list) and len(sp) == 2 and all(
                isinstance(b, dict) and all(is_num(b.get(x), 0) for x in ("x", "y", "w", "h")) and b["w"] >= 32
                and b["h"] >= 32 and b["x"] + 8 <= src_w and b["y"] + 8 <= src_h for b in sp)):
            die(f"clip {c['id']}: the split layout needs \"speakers\": two {{\"x\", \"y\", \"w\", \"h\"}} boxes in pixels of "
                f"the {src_w}x{src_h} source, one per face (--preview draws them)")
    shots = c.get("shots")
    if shots is not None and not (isinstance(shots, list) and all(
            isinstance(x, list) and len(x) == 2 and is_num(x[0], 0) and is_num(x[1], 0) and x[1] <= 1 for x in shots)):
        die(f"clip {c['id']}: shots is a list of [source second, focus_x 0 to 1] pairs")
    track = c.get("track")
    if track is not None and not (isinstance(track, list) and len(track) >= 2 and all(
            isinstance(x, list) and len(x) == 2 and is_num(x[0], 0) and is_num(x[1], 0) and x[1] <= 1 for x in track)):
        die(f"clip {c['id']}: track is a list of at least two [source second, focus_x 0 to 1] pairs")
    if c.get("hook_at") not in (None, "top", "captions"):
        die(f"clip {c['id']}: hook_at is top or captions")
    if c.get("logo_at") not in (None, "none") + LOGO_SPOTS:
        die(f"clip {c['id']}: logo_at is none or one of " + ", ".join(LOGO_SPOTS))
    if c.get("tighten") is True and ESTIMATED[0]:
        warn(f"clip {c['id']}: tighten is off here: the word times are estimated")
    if c.get("reframe") == "stack":
        for k in ("facecam", "game"):
            b = c.get(k)
            if k == "game" and b is None:
                continue
            if not isinstance(b, dict) or not all(is_num(b.get(x), 0) for x in ("x", "y", "w", "h")) or \
                    b["w"] < 32 or b["h"] < 32 or b["x"] + 8 > src_w or b["y"] + 8 > src_h:
                die(f"clip {c['id']}: the stack layout needs \"{k}\": {{\"x\", \"y\", \"w\", \"h\"}} in pixels of the "
                    f"{src_w}x{src_h} source (read them from a frame; --preview draws the boxes)")
    if float(c["end"]) > total + 0.5:
        die(f"clip {c['id']} ends at {c['end']} s but the video is {total:.0f} s")
    for k in ("speed", "mirror", "flip", "hflip", "filter"):
        if k in c:
            die(f"clip {c['id']} asks for \"{k}\". This skill never changes speed, mirrors or filters a clip")
    for k in ("music", "sound", "song", "audio_track"):
        if k in c:
            die(f"clip {c['id']} asks for \"{k}\". This skill never adds music or sounds to a client's clip: trending or "
                "unlicensed music can get it muted, claimed or taken down on the client's account. The client adds "
                "licensed music in the app if they want it")



def load_batch(path):
    """(batch, client, client folder, batch folder) for a batch.json inside clients/<client>/episodes/<episode>/."""
    batch = read_json(path, "the episode batch")
    if not isinstance(batch, dict) or not isinstance(batch.get("episode"), dict) or not isinstance(batch.get("clips"), list):
        die("batch.json needs \"client\", \"episode\" (with its source) and \"clips\" (a list)")
    bdir = os.path.dirname(os.path.abspath(path))
    ws = workspace_of(bdir)
    cid = batch.get("client")
    if not ws or not isinstance(cid, str):
        die("batch.json must sit in clients/<client>/episodes/<episode>/ and name its \"client\"")
    cdir = os.path.join(ws, "clients", cid)
    if not os.path.isfile(os.path.join(cdir, "client.json")):
        die(f"batch.json names client \"{cid}\" but clients/{cid}/client.json isn't there")
    if os.path.commonpath([cdir, bdir]) != cdir:
        die(f"batch.json names client \"{cid}\" but sits in another client's folder. A batch belongs to the client "
            "whose folder it is in")
    client = read_json(os.path.join(cdir, "client.json"), "the client file")
    if not isinstance(client, dict):
        die(f"clients/{cid}/client.json must hold one JSON object")
    return batch, client, cdir, bdir


def main():
    ap = argparse.ArgumentParser(description="Cut one episode's vertical clips in the client's brand.")
    ap.add_argument("batch")
    ap.add_argument("--transcript", help="default: the episode's transcript (work/transcript.json next to batch.json)")
    ap.add_argument("--only", help="render just these clip ids, comma separated")
    ap.add_argument("--width", type=int, default=W, help="output width (default 1080; 540 for small files)")
    ap.add_argument("--best", action="store_true", help="slower, higher-efficiency encode")
    ap.add_argument("--preview", action="store_true",
                    help="don't render; save frames with the planned crop and print each clip's first and last words")
    a = ap.parse_args()
    if a.width < 360 or a.width > W or a.width % 2:
        die("--width must be an even number from 360 to 1080")
    check_ffmpeg()
    global BEST
    BEST = a.best
    batch, client, cdir, bdir = load_batch(a.batch)
    if client.get("status") in ("offboarding", "offboarded"):
        die(f"client {client.get('id')} is {client.get('status')}: no new clips")
    ep = batch["episode"]
    if not isinstance(ep.get("source"), str) or not ep["source"].strip():
        die("batch.json episode.source names the episode's video file (from the episode folder)")
    src = ep["source"] if os.path.isabs(ep["source"]) else os.path.join(bdir, ep["source"])
    if not os.path.isfile(src):
        die(f"the episode's video isn't there: {ep['source']} (paths are from the episode folder)")
    brand = brand_of(client, cdir)
    tpath = a.transcript or os.path.join(bdir, ep.get("transcript") or os.path.join("work", "transcript.json"))
    if not os.path.isfile(tpath):
        die(f"{rel(tpath)} not found. Run transcribe.py on the episode first (--out work, in the episode folder)")
    tr = read_json(tpath, "the transcript")
    words = tr.get("words") if isinstance(tr, dict) else None
    if not isinstance(words, list) or not words:
        die(f"{rel(tpath)} has no words. Run transcribe.py on the episode again")
    if all(isinstance(w, dict) for w in words):
        words = mid_caps(words)
    if str(tr.get("source") or "").startswith("subtitles"):
        ESTIMATED[0] = True
        print("the word times come from subtitles (estimated): pauses and fillers stay in, so no cut lands mid-word")
    src_w, src_h, total, fps, has_audio = probe(src)
    if not has_audio:
        warn("the episode has no sound track: the clips get silence under the captions")
    clips = batch["clips"]
    if a.only:
        keep = {x.strip().zfill(2) for x in a.only.split(",")}
        clips = [c for c in clips if isinstance(c, dict) and str(c.get("id", "")).zfill(2) in keep]
    if not clips:
        die("no clips in batch.json" + (f" with the ids {a.only}" if a.only else ""))
    seen = set()
    for c in clips:
        check_clip(c, total, src_w, src_h)
        if c["id"] in seen:
            die(f"clip id {c['id']} is used twice")
        seen.add(c["id"])
    out_dir = os.path.join(bdir, "clips")
    os.makedirs(out_dir, exist_ok=True)
    if a.preview:
        for c in clips:
            preview(c, words, src, src_w, src_h, out_dir)
        return
    names = client.get("names") if isinstance(client.get("names"), dict) else {}
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        for c in clips:
            results.append(render_clip(c, src, words, brand, tmp, out_dir, src_w, src_h, fps, a.width, has_audio, names))
    mpath = os.path.join(out_dir, "manifest.json")
    old = {}
    if os.path.isfile(mpath) and a.only:   # keep the clips that weren't rendered again
        try:
            old = {c["id"]: c for c in json.load(open(mpath, encoding="utf-8")).get("clips", [])}
        except (ValueError, OSError, AttributeError, TypeError, KeyError):
            old = {}
    for r in results:
        old[r["id"]] = r
    every = [old[k] for k in sorted(old)]
    sheet = contact_sheet([os.path.join(out_dir, r["cover"]) for r in every], os.path.join(out_dir, "contact-sheet.jpg"))
    brand_rec = {k: v for k, v in brand.items() if k not in ("logo_path",)}
    if brand.get("logo_path"):
        brand_rec["logo_sha256"] = sha256(brand["logo_path"])
    manifest = {"client": client.get("id"), "episode": ep.get("id"), "video": rel(src, out_dir), "video_sha256": sha256(src),
                "brand": brand_rec, "clips": every, "contactSheet": rel(sheet, out_dir) if sheet else None,
                "warnings": WARNINGS}
    with open(mpath, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1, ensure_ascii=False)
    from agencylib import clear_requests, ledger_path, load_ledger, save_ledger
    lp = ledger_path()
    led = load_ledger(lp)
    gone = clear_requests(bdir, led, client.get("id"), ep.get("id"))
    if gone or os.path.exists(lp):
        save_ledger(lp, led)
    if gone:
        print(f"removed {len(gone)} unsent request(s) written for the clips as they were: the new cut needs the client's "
              "yes first")
    fixed = sum(len(r["names_fixed"]) for r in results)
    print(f"{len(results)} clip(s) in {rel(out_dir)}/, manifest: {rel(mpath)}, contact sheet: {rel(sheet) if sheet else 'none'}")
    if fixed:
        print(f"{fixed} caption word(s) spelled by the client's names dictionary (listed in the manifest)")
    if WARNINGS:
        print(f"{len(WARNINGS)} warning(s); check them before the approval page.")
    print("next: write each clip's captions in batch.json and run check_clips.py on it")


if __name__ == "__main__":
    guard(main)
