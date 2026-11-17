#!/usr/bin/env python3
"""Burn captions into the videos, in each output's style, shape and language.

    python3 scripts/render.py job.json --preview     # review sheet only (fast): look before rendering
    python3 scripts/render.py job.json               # render every video x output x language
    python3 scripts/render.py job.json --only speed --outputs vertical --lang es --force

Each output in the job sets:
  "style":    a preset in styles/ (pop, bold, highlight, reveal, lines, clean, minimal, one-word)
              or a path to your own style .json; "style_overrides": {"active": "#22D3EE", ...}
  "canvas":   "source" (keep the shape), "9:16", "4:5", "1:1" or "16:9"
  "fit":      when the shape changes: "crop" (fill, cut the sides), "blur" (whole frame on a blurred
              copy of itself) or "pad" (bars). "focus_x": 0 to 1, where to crop (0.5 = centre).
  "position": 0.05 to 0.95, how far down the caption block sits (default from the style; with
              "fit": "blur" the captions sit just under the picture)
  "languages": which caption languages to make (default: the spoken one plus every finished translation)
  "sounds":   true to burn sound tags like [laughter] too (they are always in the SRT)
A video can set "focus_x" and "position" for itself, which wins over the output's.

It first runs captions.py, so the subtitle files always match the videos. Then it writes
<out>/<id>/<id>.<output>.<lang>.mp4 (H.264, AAC, ready to post), a cover frame, and review-<id>.jpg;
<out>/manifest.json lists every file. Captions are drawn with Pillow, so any ffmpeg build works
(no libass needed). Done files are skipped until something changes.
"""
import argparse, hashlib, json, os, re, shutil, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aclib import (APPROX, CANVAS, CONNECT, WARNINGS, base_lang, die, ffmpeg_has, font_for, get_font, guard,  # noqa: E402
                   h264_args, hexrgb, is_rtl, is_symbol, joiner, load_job, load_pillow, load_style,
                   missing_glyphs, need_ffmpeg, probe, read_json, rel, run, selected, shape_check,
                   small_words, snap_fps, split_text, video_dir, visual, warn, write_json)
import captions  # noqa: E402
import fix  # noqa: E402

MAX_LONG = 1920      # output long side cap: what the apps show; bigger sources are scaled down
HOLD_GAP = 0.7       # a caption stays up through pauses shorter than this
TAIL = 0.35          # and lingers this long after the last word otherwise
SHEET_H = 480        # review sheet frame height
RENDER_VERSION = 5   # bump when the drawing or layout changes, so finished videos render again
HDR = {"smpte2084", "arib-std-b67"}


def norm(t):
    return re.sub(r"\W", "", str(t).lower())


# ---------- words for a language ----------

def words_for(job, v, lang, src_lang):
    """(words, estimated, sounds): the proofread words, or a translation's cues split into words
    (times shared out by length, so the highlight is off for them)."""
    if base_lang(lang) == base_lang(src_lang):
        data = fix.apply(job, v, quiet=True)
        return data["words"], data.get("timing") == "estimated", data.get("sounds", [])
    path = os.path.join(video_dir(job, v), f"cues.{lang}.json")
    if not os.path.exists(path):
        return None, True, []
    data = read_json(path)
    emph = [[norm(t) for t in split_text(e, lang) if norm(t)] for e in data.get("emphasis") or []]
    out = []
    for c in data["cues"]:
        toks = c.get("tokens") or split_text(c["text"], lang)
        span_end = max(c["start"] + 0.3, c["end"] - 0.45)  # cues linger after speech
        total = sum(max(len(t), 1) for t in toks) or 1
        t = c["start"]
        first = len(out)
        for tok in toks:
            d = (span_end - c["start"]) * max(len(tok), 1) / total
            out.append({"w": tok, "start": round(t, 3), "end": round(t + d, 3)})
            t += d
        if len(out) > first:
            out[-1]["cue_end"] = True  # translations break where the original cue did
    for phrase in emph:
        n = len(phrase)
        for i in range(len(out) - n + 1):
            if n and [norm(out[i + k]["w"]) for k in range(n)] == phrase:
                for k in range(n):
                    out[i + k]["k"] = 1
    return out, True, []


# ---------- layout ----------

class Layout:
    def __init__(self, st, W, H, lang, font_path):
        self.st, self.W, self.H, self.lang = st, W, H, lang
        self.scale = min(W, H) / 1080
        self.size = max(12, int(round(st["size"] * self.scale)))
        self.font = get_font(font_path, self.size, st.get("weight"))
        self.max_w = st["max_width"] * W
        self.space = self.font.getlength(" ") if joiner(lang) else 0
        ab = st.get("active_box")
        if ab:  # room for the pill so it never covers the next word
            self.space += ab.get("pad", [14, 6])[0] * self.scale * (1 if joiner(lang) else 0.5)
        self.rtl = is_rtl(lang)

    def case(self, t):
        if self.st.get("uppercase"):
            return t.upper()
        if self.st.get("lowercase"):
            return t.lower()
        return t

    def wlen(self, t):
        return self.font.getlength(visual(self.case(t), self.lang))

    def lines(self, ws):
        """Split a chunk's words into at most style['lines'] lines of similar width, broken at good
        places (after punctuation, never after "the" or inside "10 minutes"), or None if it can't fit."""
        n = self.st["lines"]
        widths = [self.wlen(w["w"]) for w in ws]
        toks = [w["w"] for w in ws]
        unit = self.size * 0.3  # one break-cost point is worth this much width

        def width(a, b):
            return sum(widths[a:b]) + self.space * max(0, b - a - 1)

        def cost(k):
            return captions.break_cost(toks[k - 1], toks[k], self.lang, k) * unit
        one = [list(range(len(ws)))]
        fits = width(0, len(ws)) <= self.max_w
        if fits and (n == 1 or len(ws) < 2 or width(0, len(ws)) <= self.max_w * 0.55):
            return one
        if n == 1:
            return None
        best = None
        for k in range(1, len(ws)):
            a, b = width(0, k), width(k, len(ws))
            if max(a, b) <= self.max_w:
                score = max(a, b) + cost(k)
                if best is None or score < best[0]:
                    best = (score, [list(range(0, k)), list(range(k, len(ws)))], cost(k))
        if fits and (best is None or best[2] > 0):
            return one  # no good place to break ("9 o | 10 minutos"): keep one line
        if best is None and n >= 3:
            for k in range(1, len(ws) - 1):
                for m in range(k + 1, len(ws)):
                    ww = (width(0, k), width(k, m), width(m, len(ws)))
                    if max(ww) <= self.max_w:
                        score = max(ww) + cost(k) + cost(m)
                        if best is None or score < best[0]:
                            best = (score, [list(range(0, k)), list(range(k, m)), list(range(m, len(ws)))], 0)
        return best[1] if best else None

    def block(self, group):
        """(lines, top, line height): where a chunk sits on the frame."""
        lines = self.lines(group) or [list(range(len(group)))]
        lh = self.size * self.st["line_gap"]
        total_h = lh * len(lines)
        margin = 0.04 * self.H
        top = min(max(self.st["position"] * self.H - total_h / 2, margin), self.H - margin - total_h)
        return lines, top, lh

    def line_width(self, group, idxs):
        return sum(self.wlen(group[i]["w"]) for i in idxs) + self.space * (len(idxs) - 1)


def units(words, lang, phrases=True):
    """Words that must stay on screen together: a number and what follows it ("10 minutes",
    "9 or 10 minutes"), and small words with the word after them ("the station"). With phrases
    (styles that show 3 or more words) also "about" with its number and names ("Space Station"). Up to 5."""
    small = small_words(lang)
    spaced = bool(joiner(lang))
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if nxt is None or len(cur) >= 5 or w.get("cue_end") or w["w"][-1:] in ".?!,;:。？！，、…" \
                or nxt["start"] - w["end"] > 0.6 or w.get("sound") or nxt.get("sound"):
            out.append(cur)
            cur = []
            continue
        tok, ntok = norm(w["w"]), norm(nxt["w"])
        if spaced:
            stick = tok in small or (w["w"][:1].isdigit() and ntok != "") \
                or (tok in CONNECT and len(cur) >= 2 and cur[-2]["w"][:1].isdigit() and nxt["w"][:1].isdigit())
            if phrases and not stick:
                prev = words[i - 1]["w"] if i else "."
                name = w["w"][:1].isupper() and nxt["w"][:1].isupper() and w["w"][:1].isalpha() \
                    and nxt["w"][:1].isalpha() and prev[-1:] not in ".?!:" and i > 0
                stick = name or (tok in APPROX and nxt["w"][:1].isdigit())
        else:  # characters: keep digits and Latin words in one piece
            stick = w["w"].isascii() and w["w"].isalnum() and nxt["w"].isascii() and nxt["w"].isalnum()
        if not stick:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def chunks(words, lay):
    """Caption groups: up to style['words'] words and style['chars'] characters per line, broken at
    sentence ends, commas and pauses, never splitting "9 or 10 minutes" or ending on "the"."""
    st, lang = lay.st, lay.lang
    j = joiner(lang)
    max_words = st["words"] if j else st["words"] * 4  # no-space languages: tokens are characters
    max_chars = st["chars"] * st["lines"]
    us = []
    small = small_words(lang)
    for u in units(words, lang, phrases=st["words"] >= 3 or not j):
        # too wide together: first let leading small words go ("about | 9 or 10 minutes"),
        # then split where it still fits
        k = 0
        while len(u) - k > 1 and lay.lines(u[k:]) is None and norm(u[k]["w"]) in small:
            k += 1
        if k and lay.lines(u[k:]) is not None:
            us.append(u[:k])
            u = u[k:]
        while len(u) > 1 and lay.lines(u) is None:
            k = len(u) - 1
            while k > 1 and lay.lines(u[:k]) is None:
                k -= 1
            us.append(u[:k])
            u = u[k:]
        us.append(u)
    groups, cur, forced = [], [], set()  # forced: group i was cut by the limits, not at a natural break
    for ui, u in enumerate(us):
        trial = cur + u
        if cur:
            text = j.join(x["w"] for x in trial)
            if lay.lines(trial) is None or len(trial) > max_words or len(text) > max_chars:
                forced.add(len(groups))
                groups.append(cur)
                cur = []
        if not cur and len(u) == 1 and lay.lines(u) is None:
            warn(f"'{u[0]['w']}' is wider than the caption area at this size; it will overflow")
        cur += u
        w = cur[-1]
        nxt = us[ui + 1][0] if ui + 1 < len(us) else None
        if nxt is None or w["w"][-1:] in ".?!。？！…" or w.get("cue_end") \
                or (w["w"][-1:] in ",;:，、" and (st["lines"] == 1 or len(cur) >= max_words // 2)) \
                or (nxt["start"] - w["end"] > st["pause"]) \
                or ("speaker" in w and nxt.get("speaker") != w.get("speaker")) \
                or bool(w.get("sound")) != bool(nxt.get("sound")):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return merge_flashes(balance(groups, forced, us, lay), lay)


def merge_flashes(groups, lay, least=0.3):
    """A caption on screen for less than 0.3 s can't be read: join it to a neighbour that has room."""
    i = 0
    while i < len(groups):
        g = groups[i]
        nxt = groups[i + 1][0]["start"] if i + 1 < len(groups) else g[-1]["end"] + TAIL
        if nxt - g[0]["start"] >= least or len(groups) == 1:
            i += 1
            continue
        if i > 0 and lay.lines(groups[i - 1] + g) is not None:
            groups[i - 1] = groups[i - 1] + g
            groups.pop(i)
        elif i + 1 < len(groups) and lay.lines(g + groups[i + 1]) is not None:
            groups[i + 1] = g + groups[i + 1]
            groups.pop(i)
        else:
            i += 1
    return groups


def balance(groups, forced, us, lay):
    """A forced cut can leave a scrap ("... la velocidad | del sonido."): share the words of the
    two groups evenly instead, cutting only between units and never after a small word."""
    j = joiner(lay.lang)
    small = small_words(lay.lang)
    start_of = {id(u[0]) for u in us}
    for i in sorted(forced):
        if i + 1 >= len(groups):
            continue
        a, b = groups[i], groups[i + 1]
        if len(b) * 2 >= len(a) and len(j.join(w["w"] for w in b)) * 2 >= len(j.join(w["w"] for w in a)):
            continue
        both = a + b
        best = None
        for k in range(1, len(both)):
            if id(both[k]) not in start_of or norm(both[k - 1]["w"]) in small:
                continue
            x, y = both[:k], both[k:]
            if lay.lines(x) is None or lay.lines(y) is None:
                continue
            score = abs(len(j.join(w["w"] for w in x)) - len(j.join(w["w"] for w in y)))
            if best is None or score < best[0]:
                best = (score, k)
        if best:
            groups[i], groups[i + 1] = both[:best[1]], both[best[1]:]
    return [g for g in groups if g]


def events(groups, st, estimated, length):
    """(start, end, group index, visible count, active index) for every caption state."""
    active = (st.get("active") or st.get("active_box")) and not estimated
    reveal = st.get("reveal")
    ev = []
    for gi, g in enumerate(groups):
        nxt = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else length
        speech_end = g[-1]["end"]
        end = nxt if nxt - speech_end < HOLD_GAP else speech_end + TAIL
        end = min(max(end, g[0]["start"] + st["min_show"]), max(nxt, g[0]["start"] + 0.05), length)
        if not (active or reveal):
            ev.append((g[0]["start"], end, gi, len(g), -1))
            continue
        for k, w in enumerate(g):
            s = g[0]["start"] if k == 0 else w["start"]
            e = g[k + 1]["start"] if k + 1 < len(g) else end
            if e - s < 0.02:
                continue
            ev.append((s, e, gi, (k + 1) if reveal else len(g), k if active else -1))
    clean = []
    for s, e, *rest in sorted(ev):
        if clean and s < clean[-1][1]:
            prev = clean[-1]
            clean[-1] = (prev[0], s) + prev[2:]
            if clean[-1][1] - clean[-1][0] < 0.02:
                clean.pop()
        if e > s:
            clean.append((s, min(e, length)) + tuple(rest))
    return clean


def draw_state(path, lay, group, visible, active, Image, ImageDraw, ImageFilter):
    st, W, H = lay.st, lay.W, lay.H
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lines, top, lh = lay.block(group)
    color = hexrgb(st["color"]) + (255,)
    act = hexrgb(st["active"]) + (255,) if st.get("active") else None
    key = hexrgb(st["keyword"]) + (255,) if st.get("keyword") else None
    stroke = int(round(st["stroke"] * lay.scale))
    placed = []  # (x, y_mid, text, fill, index, width)
    boxes = []
    for li, idxs in enumerate(lines):
        texts = [visual(lay.case(group[i]["w"]), lay.lang) for i in idxs]
        widths = [lay.font.getlength(t) for t in texts]
        lw = sum(widths) + lay.space * (len(idxs) - 1)
        x = W / 2 - lw / 2
        y = top + li * lh + lh / 2
        order = list(zip(idxs, texts, widths))
        if lay.rtl:
            order = order[::-1]
        if st.get("box"):
            boxes.append((x, y, lw))
        for i, t, wdt in order:
            if i < visible:
                fill = color
                if key and group[i].get("k"):
                    fill = key
                if act and i == active:
                    fill = act
                placed.append((x, y, t, fill, i, wdt))
            x += wdt + lay.space
    if st.get("box"):
        b = st["box"]
        d = ImageDraw.Draw(img)
        pad_x, pad_y = (v * lay.scale for v in b.get("pad", [24, 10]))
        fill = hexrgb(b.get("color", "#000000")) + (int(255 * float(b.get("alpha", 0.6))),)
        for x, y, lw in boxes:
            d.rounded_rectangle([x - pad_x, y - lh / 2 - pad_y + lh * 0.06, x + lw + pad_x, y + lh / 2 + pad_y - lh * 0.06],
                                int(b.get("radius", 14) * lay.scale), fill=fill)
    if st.get("active_box") and active >= 0:
        ab = st["active_box"]
        d = ImageDraw.Draw(img)
        for x, y, t, fill, i, wdt in placed:
            if i == active:
                px, py = (v * lay.scale for v in ab.get("pad", [14, 6]))
                d.rounded_rectangle([x - px, y - lay.size * 0.58 - py, x + wdt + px, y + lay.size * 0.58 + py],
                                    int(ab.get("radius", 16) * lay.scale), fill=hexrgb(ab["color"]) + (255,))
    sh = st.get("shadow")
    if sh:
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        for x, y, t, fill, i, wdt in placed:
            d.text((x + sh.get("dx", 0) * lay.scale, y + sh.get("dy", 4) * lay.scale), t, font=lay.font,
                   fill=(0, 0, 0, int(255 * float(sh.get("alpha", 0.5)))), anchor="lm",
                   stroke_width=stroke, stroke_fill=(0, 0, 0, int(255 * float(sh.get("alpha", 0.5)))))
        if sh.get("blur"):
            layer = layer.filter(ImageFilter.GaussianBlur(sh["blur"] * lay.scale))
        img = Image.alpha_composite(img, layer)
    d = ImageDraw.Draw(img)
    sc = hexrgb(st["stroke_color"]) + (255,)
    for x, y, t, fill, i, wdt in placed:
        if st.get("active_box") and i == active and st.get("active_box", {}).get("text"):
            fill = hexrgb(st["active_box"]["text"]) + (255,)
        d.text((x, y), t, font=lay.font, fill=fill, anchor="lm", stroke_width=stroke, stroke_fill=sc)
    img.save(path)


# ---------- geometry ----------

def colour_filter(info):
    """HDR phone footage (HLG, PQ) tone-mapped to normal video, else it plays grey and washed out."""
    if info.get("transfer") not in HDR:
        return ""
    if ffmpeg_has("filters", "zscale") and ffmpeg_has("filters", "tonemap"):
        return ("zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,"
                "zscale=t=bt709:m=bt709:r=tv,format=yuv420p,")
    warn(f"{os.path.basename(info.get('file', 'this video'))} is HDR (iPhone and Android HDR video) and this "
         "ffmpeg can't convert it to normal video (it has no zscale filter), so colours may look washed out. "
         "Export the video as SDR first (iPhone: share it with Options > Most Compatible, or turn off "
         "Settings > Camera > Formats > HDR Video for new clips), or use an ffmpeg build with zimg.")
    return ""


def geometry(info, o, v):
    """(ffmpeg filter from the source frame to the output frame, W, H, band): band is the picture's
    (top, bottom) as fractions of the frame when it doesn't fill it (blur and pad)."""
    sw, sh = info["width"], info["height"]
    pre = colour_filter(info)
    canvas = o.get("canvas", "source")
    if canvas == "source":
        k = min(1.0, MAX_LONG / max(sw, sh))
        W, H = int(sw * k) // 2 * 2, int(sh * k) // 2 * 2
        return f"{pre}scale={W}:{H}:flags=lanczos,setsar=1", W, H, None
    W, H = CANVAS[canvas]
    if abs(sw / sh - W / H) < 0.01:
        return f"{pre}scale={W}:{H}:flags=lanczos,setsar=1", W, H, None
    fit = o.get("fit", "crop")
    if fit == "crop":
        fx = float(v.get("focus_x", o.get("focus_x", 0.5)))
        if sw / sh > W / H:
            cw, ch = int(sh * W / H) // 2 * 2, sh
        else:
            cw, ch = sw, int(sw * H / W) // 2 * 2
        x = int(min(max(fx * sw - cw / 2, 0), sw - cw))
        y = int((sh - ch) / 2)
        if ch < H * 0.5:
            warn(f"{v['id']}/{o['id']}: the crop is enlarged {H / ch:.1f}x and will look soft; use \"fit\": \"blur\"")
        return f"{pre}crop={cw}:{ch}:{x}:{y},scale={W}:{H}:flags=lanczos,setsar=1", W, H, None
    ph = min(H, W * sh / sw)
    band = ((H - ph) / 2 / H, (H + ph) / 2 / H) if ph < H - 2 else None
    if fit == "blur":
        return (f"{pre}split=2[bg][fg];[bg]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
                f"gblur=sigma=40,eq=brightness=-0.12[bgb];[fg]scale={W}:{H}:force_original_aspect_ratio=decrease,"
                f"setsar=1[fgs];[bgb][fgs]overlay=(W-w)/2:(H-h)/2,setsar=1"), W, H, band
    return (f"{pre}scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:black,"
            "setsar=1"), W, H, band


def place(st, v, o, W, H, band):
    """Where the caption block sits: the video's "position" (a number, or one per output id:
    {"youtube": 0.7}), else the output's; else under the picture when it doesn't fill the frame;
    else the style's (position_tall on 9:16)."""
    vp = v.get("position")
    if isinstance(vp, dict):
        vp = vp.get(o["id"])
    if vp is not None:
        return float(vp), "set"
    if o.get("position") is not None:
        return float(o["position"]), "set"
    if band and band[1] < 0.8:
        return min(band[1] + 0.07, 0.78 if H > W * 1.5 else 0.88), "under the picture"
    if H > W * 1.5 and st.get("position_tall") is not None:
        return st["position_tall"], "style"
    return st["position"], "style"


UI = {  # where each app usually draws its buttons and text over a 9:16 video (fractions of the frame)
    "TikTok": [(0.885, 0.43, 0.99, 0.84, "rail"), (0.02, 0.80, 0.80, 0.93, "text"), (0.25, 0.04, 0.75, 0.08, "bar")],
    "Reels": [(0.89, 0.55, 0.99, 0.88, "rail"), (0.02, 0.80, 0.82, 0.92, "text"), (0.02, 0.04, 0.30, 0.08, "bar")],
    "Shorts": [(0.875, 0.47, 0.99, 0.88, "rail"), (0.02, 0.81, 0.80, 0.93, "text"), (0.80, 0.03, 0.98, 0.07, "bar")],
}


def ui_clash(lay, groups):
    """{app: kinds} where an app's buttons ("rail") or caption text ("text") would cover captions
    (9:16 only). A graze of under 2% of the frame doesn't count."""
    hit = {}
    for g in groups:
        lines, top, lh = lay.block(g)
        for li, idxs in enumerate(lines):
            lw = lay.line_width(g, idxs)
            x0, x1 = (lay.W - lw) / 2 / lay.W, (lay.W + lw) / 2 / lay.W
            y0, y1 = (top + li * lh + lh * 0.2) / lay.H, (top + (li + 1) * lh - lh * 0.2) / lay.H
            for app, rects in UI.items():
                for rx0, ry0, rx1, ry1, kind in rects:
                    if kind != "bar" and min(x1, rx1) - max(x0, rx0) > 0.02 and min(y1, ry1) - max(y0, ry0) > 0.01:
                        hit.setdefault(app, set()).add(kind)
    return hit


# ---------- review sheet ----------

def ui_panel(frame, app, Image, ImageDraw, font):
    im = frame.convert("RGBA")
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w, h = im.size
    for x0, y0, x1, y1, kind in UI[app]:
        if kind == "rail":
            n = 5
            for k in range(n):
                cy = y0 * h + (k + 0.5) * (y1 - y0) * h / n
                r = (x1 - x0) * w * 0.38
                d.ellipse([(x0 + x1) / 2 * w - r, cy - r, (x0 + x1) / 2 * w + r, cy + r], fill=(255, 255, 255, 150))
        elif kind == "text":
            rows = 3
            for k in range(rows):
                yy = y0 * h + k * (y1 - y0) * h / rows
                d.rounded_rectangle([x0 * w, yy + 2, (x1 - k * 0.12) * w, yy + (y1 - y0) * h / rows - 6], 6,
                                    fill=(255, 255, 255, 135))
        else:
            d.rounded_rectangle([x0 * w, y0 * h, x1 * w, y1 * h], 8, fill=(255, 255, 255, 135))
    im = Image.alpha_composite(im, layer)
    ImageDraw.Draw(im).text((12, 10), app, font=font, fill=(255, 255, 255, 255), stroke_width=3,
                            stroke_fill=(0, 0, 0, 255))
    return im.convert("RGB")


def frame_at(src, t, vf, out):
    """One output frame at time t, SHEET_H pixels tall."""
    cmd = ["ffmpeg", "-y", "-v", "error", "-ss", f"{max(0.0, t):.3f}", "-i", src]
    small = f"{vf},scale=-2:{SHEET_H}"
    cmd += ["-filter_complex", f"[0:v]{small}"] if "[" in vf else ["-vf", small]
    run(cmd + ["-frames:v", "1", "-q:v", "3", out])


def review_sheet(rows, path, Image, ImageDraw, ImageFont):
    """rows: [(label, [PIL frames], vertical)]: each row's frames side by side, app guides on vertical ones."""
    try:
        label_font = ImageFont.load_default(22)
    except TypeError:  # Pillow before 10.1
        label_font = ImageFont.load_default()
    try:
        label_font = get_font(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts", "Inter.ttf"), 22, "SemiBold")
    except SystemExit:
        pass
    ph = SHEET_H
    built = []
    for label, frames, vertical in rows:
        panels = [f if f.height == ph else f.resize((int(f.width * ph / f.height), ph)) for f in frames]
        if vertical and panels:
            mid = panels[len(panels) // 2]
            panels += [ui_panel(mid, app, Image, ImageDraw, label_font) for app in UI]
        built.append((label, panels))
    width = max(sum(p.width for p in ps) + 12 * (len(ps) + 1) for _, ps in built)
    height = sum(ph + 56 for _ in built) + 12
    sheet = Image.new("RGB", (width, height), "#1b1b1f")
    d = ImageDraw.Draw(sheet)
    y = 12
    for label, panels in built:
        d.text((12, y + 4), label, font=label_font, fill="#e8e8ea")
        x = 12
        for p in panels:
            sheet.paste(p, (x, y + 40))
            x += p.width + 12
        y += ph + 56
    sheet.save(path, quality=86)


# ---------- render ----------

def signature(*parts):
    return hashlib.sha1(json.dumps(parts, sort_keys=True, default=str).encode()).hexdigest()[:16]


def render_one(job, v, o, lang, src_lang, preview, force, manifest, tmp_root, rows, skip=False):
    """skip: filtered out of this run; only its review-sheet row is made."""
    Image, ImageDraw, ImageFont = load_pillow()
    from PIL import ImageFilter
    words, estimated, sounds = words_for(job, v, lang, src_lang)
    if words is None:
        warn(f"{v['id']}/{o['id']}: no '{lang}' captions yet; fill work/{v['id']}/translate.{lang}.json "
             "and run captions.py")
        return
    if not words:
        warn(f"{v['id']}/{o['id']}/{lang}: no speech found, so there is nothing to caption")
        return
    shape_check(lang)
    st = load_style(o.get("style", "pop"), o.get("style_overrides"), base=job["_base"])
    translated = base_lang(lang) != base_lang(src_lang)
    if translated:  # translated word times are estimates: show whole phrases, not single words
        st["words"], st["chars"], st["lines"] = max(st["words"], 6), max(st["chars"], 18), max(st["lines"], 2)
    if o.get("sounds") and sounds:
        for snd in sounds:
            words.append({"w": snd["text"], "start": snd["at"], "end": snd["at"] + 1.2, "sound": True})
        words.sort(key=lambda w: w["start"])
    info = probe(v["file"])
    vf, W, H, band = geometry(dict(info, file=v["file"]), o, v)
    st["position"], where = place(st, v, o, W, H, band)
    sample = joiner(lang).join(w["w"] for w in words)
    sample = sample.upper() if st.get("uppercase") else sample
    fpath, note = font_for(st["font"], lang, sample, 80, o.get("font_file") or job.get("font_file"), st.get("weight"))
    if note:
        print(f"  {v['id']}/{o['id']}/{lang}: using {note} (the style's font can't draw this text)")
    lost = [ch for ch in missing_glyphs(sample, get_font(fpath, 80, st.get("weight"))) if is_symbol(ch)]
    if lost:
        warn(f"{v['id']}/{o['id']}/{lang}: the font has no {''.join(lost[:8])} (emoji or symbols); left out")
        words = [dict(w, w="".join(ch for ch in w["w"] if ch not in lost)) for w in words]
        words = [w for w in words if w["w"].strip()]
    lay = Layout(st, W, H, lang, fpath)
    length = info["duration"]
    groups = chunks(words, lay)
    evs = events(groups, st, estimated, length)
    if estimated and (st.get("active") or st.get("active_box")) and not translated:
        print(f"  {v['id']}/{o['id']}/{lang}: word times are estimated here, so the spoken-word highlight is off")
    if H > W * 1.5 and not skip:
        clash = ui_clash(lay, groups)
        kinds = set().union(*clash.values()) if clash else set()
        if clash:
            fix_it = []
            if "text" in kinds:
                fix_it.append("move them up with \"position\" (0.62 clears every app)")
            if "rail" in kinds:
                fix_it.append("narrow them with \"style_overrides\": {\"max_width\": 0.72}")
            what = " and ".join(x for x in (("buttons" if "rail" in kinds else ""), ("caption text" if "text" in kinds else "")) if x)
            warn(f"{v['id']}/{o['id']}/{lang}: some captions sit under {', '.join(sorted(clash))}'s {what} "
                 f"(position {st['position']:.2f}); {' or '.join(fix_it)}, and check the review sheet")
    folder = os.path.join(job["out"], v["id"])
    os.makedirs(folder, exist_ok=True)
    out = os.path.join(folder, f"{v['id']}.{o['id']}.{lang}.mp4")
    o_sig = {k: val for k, val in o.items() if k != "languages" and not (k == "sounds" and not val)}
    sig = signature(words, st, vf, o_sig, {k: info[k] for k in info if k != "bytes"}, os.path.basename(fpath),
                    job.get("preset", "veryfast"), RENDER_VERSION)
    tmp = tempfile.mkdtemp(dir=tmp_root)
    try:
        states = {}

        def state_png(gi, vis, act):
            k = (gi, vis, act)
            if k not in states:
                p = os.path.join(tmp, f"s{len(states):05d}.png")
                if gi is None:
                    Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(p)
                else:
                    draw_state(p, lay, groups[gi], vis, act, Image, ImageDraw, ImageFilter)
                states[k] = p
            return states[k]

        # review sheet: three moments with a caption on screen
        picks = [evs[int(len(evs) * f)] for f in (0.1, 0.5, 0.85)] if evs else []
        frames = []
        for n, (s, e, gi, vis, act) in enumerate(picks):
            fp = os.path.join(tmp, f"f{n}.jpg")
            frame_at(v["file"], (s + e) / 2, vf, fp)
            base = Image.open(fp).convert("RGBA")
            ov = Image.open(state_png(gi, vis, act)).resize(base.size, Image.LANCZOS)
            frames.append(Image.alpha_composite(base, ov).convert("RGB"))
        pos = f"position {st['position']:.2f}" + (f" ({where})" if where != "style" else "")
        rows.append((f"{v['id']} / {o['id']} / {lang}: {st['name']}, {W}x{H}, {pos}", frames, H > W * 1.5))
        entry = {"video": v["id"], "output": o["id"], "language": lang, "style": st["name"],
                 "file": rel(out, job["out"]), "width": W, "height": H, "seconds": round(length, 2),
                 "captions": len(groups), "srt": rel(os.path.join(folder, f"{v['id']}.{lang}.srt"), job["out"]),
                 "timing": "estimated" if estimated else "measured", "signature": sig}
        if skip:
            return
        if preview:
            print(f"  {v['id']}/{o['id']}/{lang}: {len(groups)} captions at {pos}")
            return
        old = next((m for m in manifest if m.get("file") == entry["file"]), None)
        if old and old.get("signature") == sig and os.path.exists(out) and not force \
                and os.path.getsize(out) == old.get("bytes"):
            print(f"  {v['id']}/{o['id']}/{lang}: up to date ({rel(out)})")
            return
        listing, t = [], 0.0
        for s, e, gi, vis, act in evs:
            if s - t > 0.005:
                listing.append((state_png(None, 0, -1), s - t))
            listing.append((state_png(gi, vis, act), e - s))
            t = e
        if length - t > 0.005 or not listing:
            listing.append((state_png(None, 0, -1), max(length - t, 0.04)))
        lst = os.path.join(tmp, "overlays.txt")
        with open(lst, "w", encoding="utf-8") as fh:
            fh.write("ffconcat version 1.0\n")
            for p, d in listing:
                fh.write(f"file '{os.path.basename(p)}'\nduration {d:.3f}\n")
            fh.write(f"file '{os.path.basename(listing[-1][0])}'\n")
        fps = snap_fps(info["fps"])
        tags = ",setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709" \
            if ffmpeg_has("filters", "setparams") else ""
        graph = f"[0:v]{vf}[base];[1:v]fps={fps},format=yuva420p[ov];" \
                f"[base][ov]overlay=0:0:format=yuv420:shortest=0:eof_action=pass,format=yuv420p{tags}[v]"
        part = out[:-4] + ".part.mp4"
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", os.path.abspath(v["file"]), "-f", "concat", "-safe", "0",
               "-i", lst, "-filter_complex", graph, "-map", "[v]"]
        if info["audio"]:
            cmd += ["-map", f"0:a:{info['audio_index']}"]
            cmd += ["-c:a", "copy"] if info["acodec"] == "aac" else ["-c:a", "aac", "-b:a", "192k"]
        cmd += ["-t", f"{length:.3f}"] + h264_args(job.get("preset", "veryfast")) + ["-r", fps, "-pix_fmt", "yuv420p",
                "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                "-movflags", "+faststart", "-f", "mp4", os.path.abspath(part)]
        print(f"  {v['id']}/{o['id']}/{lang}: rendering {len(groups)} captions at {W}x{H}...", flush=True)
        try:
            run(cmd)
        except BaseException:  # failed or stopped (Ctrl-C): never leave a half-written file
            if os.path.exists(part):
                os.remove(part)
            raise
        os.replace(part, out)
        cover = out[:-4] + ".cover.jpg"
        first = picks[0] if picks else None
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{((first[0] + first[1]) / 2) if first else 0:.2f}", "-i", out,
             "-frames:v", "1", "-q:v", "3", cover])
        entry.update(bytes=os.path.getsize(out), fps=fps, cover=rel(cover, job["out"]))
        if old:
            manifest.remove(old)
        manifest.append(entry)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def save_manifest(path, manifest):
    manifest.sort(key=lambda m: (m["video"], m["output"], m["language"]))
    write_json(path, {"about": "Paths are relative to this file.", "files": manifest, "warnings": WARNINGS})


def prune(manifest, job):
    """Drop manifest rows whose video, output or file no longer exists."""
    vids = {v["id"] for v in job["videos"]}
    outs = {o["id"] for o in job["outputs"]}
    keep = [m for m in manifest if isinstance(m, dict) and m.get("video") in vids and m.get("output") in outs
            and os.path.exists(os.path.join(job["out"], str(m.get("file"))))]
    return keep


def main():
    ap = argparse.ArgumentParser(description="Burn captions into videos.")
    ap.add_argument("job")
    ap.add_argument("--preview", action="store_true", help="review sheet only, no video")
    ap.add_argument("--only", help="video ids, comma-separated")
    ap.add_argument("--outputs", help="output ids, comma-separated")
    ap.add_argument("--lang", help="caption languages, comma-separated")
    ap.add_argument("--force", action="store_true", help="render again even if up to date")
    a = ap.parse_args()
    need_ffmpeg()
    Image, ImageDraw, ImageFont = load_pillow()
    job = load_job(a.job)
    outs = job["outputs"]
    want_out = set(a.outputs.split(",")) if a.outputs else None
    if want_out and not want_out & {o["id"] for o in outs}:
        die(f"--outputs {a.outputs}: no such output (ids: {', '.join(o['id'] for o in outs)})")
    want_lang = set(a.lang.split(",")) if a.lang else None
    man_path = os.path.join(job["out"], "manifest.json")
    manifest = []
    if os.path.exists(man_path):
        old = read_json(man_path)
        manifest = prune(old.get("files", []) if isinstance(old, dict) else [], job)
    tmp_root = tempfile.mkdtemp(prefix="captions-")
    made = set()
    try:
        for v in selected(job, a.only):
            if not os.path.exists(v["file"]):
                die(f"{v['id']}: {rel(v['file'])} not found")
            todo = captions.run_video(job, v, quiet=True)  # subtitle files always match the videos
            for p in todo:
                print(f"  translate: fill in {p}, then run render.py again")
            data = fix.apply(job, v, quiet=True)
            src_lang = data["language"] or "en"
            if not data.get("proofread"):
                warn(f"{v['id']}: not proofread (no work/{v['id']}/fixes.json). Read transcript.txt first: "
                     "names and numbers are the usual mistakes")
            rows = []
            for o in outs:
                langs = o.get("languages") or [src_lang] + [t for t in job["translations"]
                                                            if base_lang(t) != base_lang(src_lang) and
                                                            os.path.exists(os.path.join(video_dir(job, v), f"cues.{t}.json"))]
                for m in [m for m in manifest if m["video"] == v["id"] and m["output"] == o["id"]
                          and m["language"] not in langs]:
                    manifest.remove(m)  # a language taken out of the job: its old video isn't posted
                for lang in langs:
                    skip = (want_out is not None and o["id"] not in want_out) or \
                           (want_lang is not None and lang not in want_lang)
                    if not skip:
                        made.add(lang)
                    render_one(job, v, o, lang, src_lang, a.preview, a.force, manifest, tmp_root, rows, skip)
                    if not a.preview:  # saved after every video, so a stopped batch keeps its list
                        save_manifest(man_path, manifest)
            if rows:
                sheet = os.path.join(job["out"], v["id"], f"review-{v['id']}.jpg")
                os.makedirs(os.path.dirname(sheet), exist_ok=True)
                review_sheet(rows, sheet, Image, ImageDraw, ImageFont)
                print(f"{v['id']}: review sheet -> {rel(sheet)}")
    finally:
        shutil.rmtree(tmp_root, ignore_errors=True)
    for lang in sorted((want_lang or set()) - made):
        warn(f"--lang {lang}: nothing made in that language (not in the job's translations, or not translated yet)")
    if not a.preview:
        save_manifest(man_path, manifest)
        print(f"{len(manifest)} captioned video(s) listed in {rel(man_path)}")


if __name__ == "__main__":
    guard(main)
