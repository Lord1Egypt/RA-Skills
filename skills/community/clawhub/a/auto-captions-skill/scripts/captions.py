#!/usr/bin/env python3
"""Subtitle files and translations.

    python3 scripts/captions.py job.json          # SRT, VTT and transcript per video and language

For each video it applies the fixes (fix.py), then writes to <out>/<id>/:
  <id>.<lang>.srt   subtitles for YouTube, Facebook and any editor
  <id>.<lang>.vtt   the same for web players
  <id>.<lang>.txt   a plain transcript (accessibility, show notes, the post text)
Each cue has at most 2 lines of 42 characters (16 in Chinese and Korean, 13 in Japanese), lasts 5/6
of a second to 7 seconds and is broken at punctuation. Cues follow the speaker word for word, so a
fast speaker gives fast cues; the script lists them.

Translations: for every language in the job's "translations" it writes
work/<id>/translate.<lang>.json, one entry per cue with "text" empty. The agent fills in each
"text" (same meaning, natural for that language, short enough to read), then runs this again to get
that language's files. Cue times never change, so the translation stays in sync. render.py runs
this too, so the subtitle files always match the captioned videos.
"""
import argparse, math, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aclib import (APPROX, CONNECT, SRT_CPS, SRT_LINE, base_lang, die, guard, joiner, load_job, read_json, rel, selected,  # noqa: E402
                   small_words, split_text, stamp, video_dir, warn, write_json)
import fix  # noqa: E402

MIN_CUE, MAX_CUE, LINGER, GAP, MIN_GAP = 0.833, 7.0, 0.6, 0.7, 0.083  # MIN_GAP: 2 frames between cues


def line_max(lang):
    return SRT_LINE.get(base_lang(lang), 42)


def cps_max(lang):
    return SRT_CPS.get(base_lang(lang), 20)


def text_of(ws, lang):
    return joiner(lang).join(w["w"] for w in ws)


def cue_words(words, lang):
    """Group words into subtitle cues."""
    L = line_max(lang)
    cues, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if nxt is None:
            break
        n = len(text_of(cur, lang))
        n_next = len(text_of(cur + [nxt], lang))
        end_sentence = w["w"][-1:] in ".?!。？！…"
        clause = w["w"][-1:] in ",;:、，" and n >= L * 0.8
        pause = nxt["start"] - w["end"] > GAP
        too_long = n_next > 2 * L or nxt["end"] - cur[0]["start"] > MAX_CUE
        speaker = "speaker" in w and nxt.get("speaker") != w.get("speaker")
        if end_sentence or clause or pause or speaker:
            cues.append(cur)
            cur = []
        elif too_long:
            k = best_break(cur, lang)
            cues.append(cur[:k])
            cur = cur[k:]
    if cur:
        cues.append(cur)
    return cues


def best_break(cur, lang):
    """Where to end a cue that got too long: after the last comma, else not after a small word."""
    small = small_words(lang)
    half = max(1, len(cur) // 2)
    for k in range(len(cur) - 1, half - 1, -1):
        if cur[k - 1]["w"][-1:] in ",;:、，":
            return k
    for k in range(len(cur), half - 1, -1):
        last = re.sub(r"\W", "", cur[k - 1]["w"].lower())
        if last not in small and not re.search(r"\d$", cur[k - 1]["w"]):
            return k
    return len(cur)


def break_cost(prev_tok, next_tok, lang, k):
    """How bad a line break between two tokens is (lower is better)."""
    small = small_words(lang)
    last = re.sub(r"\W", "", prev_tok.lower())
    cost = 0
    if prev_tok[-1:] in ",.;:!?，。、":
        cost -= 10
    elif last in small:
        cost += 12
    nxt = re.sub(r"\W", "", next_tok.lower())
    if re.search(r"\d$", prev_tok) and prev_tok[-1:] not in ",.;:":  # "10 | minutes", "9 | or 10"
        cost += 25
    if (last in CONNECT or last in APPROX) and next_tok[:1].isdigit():  # "9 or | 10", "about | 9"
        cost += 25
    if nxt in CONNECT and re.search(r"\d$", prev_tok):
        cost += 5
    if prev_tok[:1].isupper() and next_tok[:1].isupper() and prev_tok[-1:].isalpha() and k > 1:
        cost += 10  # don't split a name
    return cost


def line_split(text_tokens, lang):
    """(lines, cost of the break): one line if it fits, else the best two lines."""
    j = joiner(lang)
    L = line_max(lang)
    full = j.join(text_tokens)
    if len(full) <= L or len(text_tokens) < 2:
        return [full], 0
    best, best_score, best_cost = None, None, 0
    for k in range(1, len(text_tokens)):
        a, b = j.join(text_tokens[:k]), j.join(text_tokens[k:])
        cost = break_cost(text_tokens[k - 1], text_tokens[k], lang, k)
        score = max(len(a), len(b)) + cost
        if max(len(a), len(b)) > L:
            score += 1000
        if best_score is None or score < best_score:
            best, best_score, best_cost = [a, b], score, cost
    return best, best_cost


def split_lines(text_tokens, lang):
    """One line if it fits, else two lines of similar length, broken after punctuation and never
    right after a small word like "the" or between a number and its unit."""
    return line_split(text_tokens, lang)[0]


def clean_cues(groups, lang):
    """A cue whose only two-line layouts cut a phrase ("about 9 / or 10 minutes") becomes two cues,
    split where the break is clean ("So we'll actually only have / about 9 or 10 minutes ...")."""
    L = line_max(lang)
    j = joiner(lang)
    out = []
    for g in groups:
        toks = [w["w"] for w in g]
        _, cost = line_split(toks, lang)
        if cost < 20 or len(g) < 4 or g[-1]["end"] - g[0]["start"] < 1.6:
            out.append(g)
            continue
        best = None
        for k in range(2, len(g) - 1):
            a, b = j.join(toks[:k]), j.join(toks[k:])
            c = break_cost(toks[k - 1], toks[k], lang, k)
            if len(a) > 2 * L or len(b) > 2 * L or c >= 10:
                continue
            score = abs(len(a) - len(b)) + 3 * c
            if best is None or score < best[0]:
                best = (score, k)
        if best:
            out += [g[:best[1]], g[best[1]:]]
        else:
            out.append(g)
    return out


def build_cues(words, lang, sounds=None, duration=None):
    words = [w for w in words if duration is None or w["start"] < duration]
    cues = [{"start": g[0]["start"], "end": g[-1]["end"], "tokens": [w["w"] for w in g]}
            for g in clean_cues(cue_words(words, lang), lang) if g]
    for s in sounds or []:  # a sound tag gets its own cue in a gap, or its own line in a cue
        at = s["at"]
        if duration is not None and at >= duration:
            continue
        hit = next((c for c in cues if c["start"] - 0.2 <= at <= c["end"] + 0.2), None)
        if hit:
            hit.setdefault("tags", []).append(s["text"])
        else:
            cues.append({"start": at, "end": at + 1.5, "tokens": [s["text"]], "sound": True})
    cues.sort(key=lambda c: c["start"])
    # linger a little after speech, at least 5/6 s, never into the next cue or past the end
    i = 0
    while i < len(cues):
        c = cues[i]
        nxt = cues[i + 1]["start"] if i + 1 < len(cues) else math.inf
        end = min(max(c["end"] + LINGER, c["start"] + MIN_CUE), nxt - MIN_GAP)
        if duration is not None:
            end = min(end, duration)
        if end - c["start"] < 0.3 and i + 1 < len(cues) and not c.get("sound") and not cues[i + 1].get("sound"):
            nx = cues[i + 1]  # too short to read on its own ("Okay?"): merge it into the next cue
            nx["tokens"] = c["tokens"] + nx["tokens"]
            nx["start"] = c["start"]
            nx["tags"] = c.get("tags", []) + nx.get("tags", [])
            cues.pop(i)
            continue
        c["end"] = max(end, min(c["start"] + 0.3, duration if duration is not None else math.inf, nxt - MIN_GAP))
        i += 1
    cues = [c for c in cues if c["end"] > c["start"]]
    for i, c in enumerate(cues):
        c["i"] = i + 1
        c["text"] = joiner(lang).join(c["tokens"])
        if not c.get("tags"):
            c.pop("tags", None)
    return cues


def write_files(folder, vid, lang, cues, translated=False, quiet=False):
    os.makedirs(folder, exist_ok=True)
    base = os.path.join(folder, f"{vid}.{lang}")
    slow = []
    with open(base + ".srt", "w", encoding="utf-8") as srt, open(base + ".vtt", "w", encoding="utf-8") as vtt:
        vtt.write("WEBVTT\n\n")
        for c in cues:
            lines = split_lines(split_text(c["text"], lang), lang) if not c.get("sound") else [c["text"]]
            if c.get("tags"):
                lines = [" ".join(c["tags"])] + lines
            dur = c["end"] - c["start"]
            if dur > 0 and len(c["text"]) / dur > cps_max(lang) * 1.1:
                slow.append(c["i"])
            srt.write(f"{c['i']}\n{stamp(c['start'])} --> {stamp(c['end'])}\n" + "\n".join(lines) + "\n\n")
            vtt.write(f"{stamp(c['start'], '.')} --> {stamp(c['end'], '.')}\n" + "\n".join(lines) + "\n\n")
    with open(base + ".txt", "w", encoding="utf-8") as fh:
        j = " " if joiner(lang) else ""
        para, out = [], []
        for c in cues:
            if c.get("sound"):
                continue
            para.append(c["text"])
            if c["text"][-1:] in ".?!。？！" and len(j.join(para)) > 280:
                out.append(j.join(para))
                para = []
        if para:
            out.append(j.join(para))
        fh.write("\n\n".join(out) + "\n")
    if slow and translated:
        warn(f"{vid} ({lang}): cue(s) {', '.join(map(str, slow))} read faster than {cps_max(lang)} characters "
             "per second; shorten them in the translation before rendering")
    elif slow and not quiet:
        print(f"  {vid}: cue(s) {', '.join(map(str, slow))} are faster than {cps_max(lang)} characters per second "
              "because the speaker talks fast; the subtitle file follows the speech word for word")
    return base


def translation(job, v, lang, src_cues, src_lang, duration):
    folder = video_dir(job, v)
    path = os.path.join(folder, f"translate.{lang}.json")
    want = [{"i": c["i"], "start": round(c["start"], 3), "end": round(c["end"], 3), "source": c["text"]}
            for c in src_cues if not c.get("sound")]
    if not os.path.exists(path):
        write_json(path, {"from": src_lang, "to": lang,
                          "how": "Fill every 'text' with the translation of 'source': the same meaning in natural "
                                 f"{lang}, short enough to read in the cue's time; keep names and numbers. Optional "
                                 "'emphasis': words to colour, as in fixes.json. Don't change i, start or end.",
                          "emphasis": [],
                          "cues": [dict(c, text="") for c in want]})
        return None, path, []
    data = read_json(path)
    cues = data.get("cues") if isinstance(data, dict) else None
    if not isinstance(cues, list) or not all(isinstance(c, dict) for c in cues):
        die(f"{rel(path)}: expected {{\"cues\": [{{\"i\": 1, \"start\": ..., \"end\": ..., \"text\": \"...\"}}]}}")
    ids = [c.get("i") for c in cues]
    if len(set(map(str, ids))) != len(ids):
        die(f"{rel(path)}: a cue number appears twice; each cue once, as in the template")
    have = {c.get("i"): c for c in cues}
    match = [c["i"] for c in want] == sorted(i for i in have if isinstance(i, int)) and len(have) == len(want)
    if match:
        for c in want:
            st = have[c["i"]].get("start")
            if isinstance(st, bool) or not isinstance(st, (int, float)) or abs(st - c["start"]) > 0.01:
                match = False
    if not match and not any(str(c.get("text") or "").strip() for c in cues):
        os.remove(path)  # never filled in: just make a fresh template
        return translation(job, v, lang, src_cues, src_lang, duration)
    if not match:
        die(f"{rel(path)} no longer matches the {src_lang} cues (the transcript or fixes changed, or a cue's "
            "number or time was edited). Rename it, run captions.py for a fresh template, and translate again.")
    for c, s in zip(sorted(cues, key=lambda x: x["i"]), want):
        if isinstance(c.get("source"), str) and c["source"].strip() != s["source"].strip():
            warn(f"{v['id']} ({lang}) cue {s['i']}: the {src_lang} text changed after it was translated "
                 f"(now: \"{s['source'][:80]}\"); check the translation in {rel(path)}")
    for c in cues:
        if c.get("text") is not None and not isinstance(c.get("text"), str):
            die(f"{rel(path)}: cue {c['i']}: 'text' must be the translation (text)")
    if any(not (c.get("text") or "").strip() for c in cues):
        return None, path, []
    emph = data.get("emphasis") or []
    if not isinstance(emph, list) or not all(isinstance(e, str) for e in emph):
        die(f"{rel(path)}: 'emphasis' must be a list of words or phrases")
    out = []
    for c, s in zip(sorted(cues, key=lambda x: x["i"]), want):
        t = re.sub(r"\s+", " ", c["text"]).strip()
        end = min(s["end"], duration) if duration else s["end"]
        out.append({"i": s["i"], "start": s["start"], "end": end, "text": t, "tokens": split_text(t, lang)})
        if len(t) > max(2 * line_max(lang), len(s["source"]) * 1.6):
            warn(f"{v['id']} ({lang}) cue {s['i']}: the translation is much longer than the original; shorten it")
    return out, path, emph


def run_video(job, v, quiet=False):
    """Fixes -> cues -> subtitle files, for the spoken language and every finished translation."""
    data = fix.apply(job, v, quiet=True)
    lang = data["language"] or "en"
    cues = build_cues(data["words"], lang, data.get("sounds"), data.get("duration"))
    folder = os.path.join(job["out"], v["id"])
    write_files(folder, v["id"], lang, cues, quiet=quiet)
    write_json(os.path.join(video_dir(job, v), f"cues.{lang}.json"), {"language": lang, "cues": cues})
    done, todo = [lang], []
    for tl in job["translations"]:
        if base_lang(tl) == base_lang(lang):
            continue
        tcues, path, emph = translation(job, v, tl, cues, lang, data.get("duration"))
        if tcues is None:
            todo.append(rel(path))
            continue
        write_files(folder, v["id"], tl, tcues, translated=True, quiet=quiet)
        write_json(os.path.join(video_dir(job, v), f"cues.{tl}.json"),
                   {"language": tl, "cues": tcues, "emphasis": emph})
        done.append(tl)
    if not quiet:
        proof = "" if data.get("proofread") else " (not proofread: no fixes.json)"
        print(f"{v['id']}: {len(cues)} cues; subtitles in {', '.join(done)} -> {rel(folder)}/{proof}")
        for p in todo:
            print(f"  translate: fill in {p}, then run captions.py again")
    return todo


def main():
    ap = argparse.ArgumentParser(description="Write SRT, VTT and transcript files, and translation templates.")
    ap.add_argument("job")
    ap.add_argument("--only")
    a = ap.parse_args()
    job = load_job(a.job)
    todo = []
    for v in selected(job, a.only):
        todo += run_video(job, v)
    if todo:
        print(f"{len(todo)} translation file(s) to fill in before render.py can make those versions.")


if __name__ == "__main__":
    guard(main)
