#!/usr/bin/env python3
"""Proofread step: list what to check, then apply the agent's corrections with word times kept.

    python3 scripts/fix.py job.json --report     # unsure words, near-misses of vocab names, odd numbers
    python3 scripts/fix.py job.json              # apply every work/<id>/fixes.json -> words.json

fixes.json (the agent writes one per video, next to transcript.txt; all keys optional):
{
  "lines": {"3": "The corrected text of line L3, exactly as it should read on screen."},
  "replace": {"Nicole": "Nichole", "wont": "won't"},    whole words, everywhere in this video
  "emphasis": ["17,500", "16 times"],                  words or phrases the style colours as keywords
  "fillers": "remove",                                 remove (default) or keep: um, uh, erm, hmm
  "profanity": "keep",                                 keep (default), mask (f***) or remove
  "sounds": {"4.2": "[laughter]"}                      a sound tag shown at that second (accessible captions)
}
A corrected line keeps the times of every unchanged word; new or changed words share the time of
the words they replace. Never edit transcript.json itself: transcribing again would overwrite it.
"""
import argparse, difflib, os, re, sys, unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import math  # noqa: E402
from aclib import (die, guard, joiner, load_job, read_json, rel, selected, short, split_text, video_dir,  # noqa: E402
                   warn, write_json)
from transcribe import LOW_CONFIDENCE, lines_of  # noqa: E402

FILLERS = {"um", "uh", "uhm", "umm", "erm", "er", "hmm", "mm", "mhm", "ah", "eh"}
PROFANE = {"fuck", "fucking", "fucked", "fucker", "motherfucker", "shit", "shitty", "bullshit", "bitch",
           "asshole", "cunt", "dick", "dickhead", "bastard", "piss", "pissed", "crap", "goddamn", "damn"}
KEYS = {"lines", "replace", "emphasis", "fillers", "profanity", "sounds"}


def norm(t):
    t = unicodedata.normalize("NFKC", t).lower()
    return re.sub(r"[^\w]", "", t)


def load_fixes(folder):
    path = os.path.join(folder, "fixes.json")
    if not os.path.exists(path):
        return {}, None
    fx = read_json(path)
    if not isinstance(fx, dict):
        die(f"{rel(path)} must be a JSON object")
    unknown = set(fx) - KEYS
    if unknown:
        die(f"{rel(path)}: unknown key(s) {', '.join(sorted(unknown))}; use {', '.join(sorted(KEYS))}")
    for k, typ in (("lines", dict), ("replace", dict), ("emphasis", list), ("sounds", dict)):
        if k in fx and not isinstance(fx[k], typ):
            die(f"{rel(path)}: '{k}' must be a {'list' if typ is list else 'object'}")
    if fx.get("fillers", "remove") not in ("remove", "keep"):
        die(f"{rel(path)}: 'fillers' is remove or keep")
    if fx.get("profanity", "keep") not in ("keep", "mask", "remove"):
        die(f"{rel(path)}: 'profanity' is keep, mask or remove")
    for k, v in (fx.get("lines") or {}).items():
        if not isinstance(v, str) or not v.strip():
            die(f"{rel(path)}: line {k} must be the corrected text")
    for k, v in (fx.get("replace") or {}).items():
        if not isinstance(v, str) or not k.strip():
            die(f"{rel(path)}: replace \"{k}\" must map one word to its corrected text")
    if not all(isinstance(e, str) for e in fx.get("emphasis") or []):
        die(f"{rel(path)}: 'emphasis' must be a list of words or phrases")
    for k, v in (fx.get("sounds") or {}).items():
        try:
            at = float(k)
        except ValueError:
            at = float("nan")
        if not math.isfinite(at) or at < 0 or not isinstance(v, str) or not v.strip():
            die(f"{rel(path)}: sounds must look like {{\"4.2\": \"[laughter]\"}} (seconds, then the tag)")
    return fx, path


def realign(old, new_tokens, t0, t1):
    """Give new tokens times: unchanged words keep theirs; replaced words share the time of the words
    they replace; an inserted word takes the silence before the next word, or the start of the next
    word's time when there is no silence (never the end of the previous word, which would show it early)."""
    old = [dict(w) for w in old]
    a = [norm(w["w"]) for w in old]
    b = [norm(t) for t in new_tokens]
    out = []

    def spread(toks, s, e):
        span = max(e - s, 0.04 * len(toks))
        total = sum(max(len(t), 1) for t in toks)
        t = s
        for tok in toks:
            d = span * max(len(tok), 1) / total
            out.append({"w": tok, "start": round(t, 3), "end": round(t + d, 3), "edited": True})
            t += d

    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal":
            for i, j in zip(range(i1, i2), range(j1, j2)):
                out.append(dict(old[i], w=new_tokens[j]))
        elif tag == "replace":
            spread(new_tokens[j1:j2], old[i1]["start"], old[i2 - 1]["end"])
        elif tag == "insert":
            toks = new_tokens[j1:j2]
            s = out[-1]["end"] if out else t0
            e = old[i1]["start"] if i1 < len(old) else t1
            if e - s >= 0.12 * len(toks):
                spread(toks, s, e)
            elif i1 < len(old):
                nxt = old[i1]
                cut = round(nxt["start"] + (nxt["end"] - nxt["start"]) * 0.45, 3)
                spread(toks, nxt["start"], cut)
                nxt["start"] = cut
            elif out:
                prev = out.pop()
                spread([prev["w"]] + toks, prev["start"], prev["end"])
            else:
                spread(toks, t0, t1)
    for i in range(1, len(out)):  # times never run backwards
        if out[i]["start"] < out[i - 1]["start"]:
            out[i]["start"] = out[i - 1]["start"]
        if out[i]["end"] < out[i]["start"]:
            out[i]["end"] = out[i]["start"]
    return out


def tokens_of(text, lang):
    return split_text(text, lang)  # words, or one token per character in languages without spaces


def mask(word):
    core = re.match(r"^(\W*)(\w)(\w*)(\W*)$", word)
    if not core:
        return word
    return core.group(1) + core.group(2) + "*" * len(core.group(3)) + core.group(4)


def apply(job, v, quiet=False):
    """transcript.json + fixes.json -> words.json. Returns the words."""
    folder = video_dir(job, v)
    tr_path = os.path.join(folder, "transcript.json")
    if not os.path.exists(tr_path):
        die(f"{v['id']}: no transcript yet; run transcribe.py first")
    tr = read_json(tr_path)
    ok = isinstance(tr, dict) and isinstance(tr.get("words"), list) and \
        isinstance(tr.get("duration"), (int, float)) and not isinstance(tr.get("duration"), bool) and \
        all(isinstance(w, dict) and isinstance(w.get("w"), str) and
            all(isinstance(w.get(k), (int, float)) and not isinstance(w.get(k), bool) for k in ("start", "end"))
            for w in tr["words"] if isinstance(tr.get("words"), list))
    if not ok:
        die(f"{rel(tr_path)} is damaged (it is written by transcribe.py, not by hand). Run "
            "transcribe.py again with --force; fixes.json is kept.")
    lang = tr.get("language") or job.get("language") or "en"
    words = [dict(w) for w in tr["words"]]
    fx, fx_path = load_fixes(folder)
    lines = lines_of(words, lang)
    by_n = {ln["n"]: ln for ln in lines}
    for key, text in (fx.get("lines") or {}).items():
        n = int(str(key).lstrip("Ll")) if str(key).lstrip("Ll").isdigit() else None
        if n not in by_n:
            die(f"{rel(fx_path)}: line {key} doesn't exist (lines L1 to L{len(lines)} in transcript.txt)")
        if not isinstance(text, str) or not text.strip():
            die(f"{rel(fx_path)}: line {key} must be the corrected text")
    out = []
    for ln in lines:
        seg = words[ln["first"]:ln["last"] + 1]
        new = (fx.get("lines") or {}).get(str(ln["n"])) or (fx.get("lines") or {}).get(f"L{ln['n']}")
        if new is not None:
            toks = tokens_of(new.strip(), lang)
            if len(toks) < 0.6 * len(seg) and len(seg) - len(toks) >= 3:
                die(f"{rel(fx_path)}: line {ln['n']} has {len(seg)} words in transcript.txt but {len(toks)} in "
                    "fixes.json. A line fix replaces the whole line: write all of it, as it was said.")
            same = difflib.SequenceMatcher(None, [norm(w["w"]) for w in seg], [norm(t) for t in toks],
                                           autojunk=False).ratio()
            letters = difflib.SequenceMatcher(None, "".join(norm(w["w"]) for w in seg),
                                              "".join(norm(t) for t in toks), autojunk=False).ratio()
            if same < 0.5 and letters < 0.6:  # a name fix on a short line changes words, not letters
                die(f"{rel(fx_path)}: line {ln['n']} was written for a different transcript. It now reads: "
                    f"\"{joiner(lang).join(w['w'] for w in seg)[:160]}\". Proofread that line again.")
            seg = realign(seg, toks, ln["start"], ln["end"])
        out.extend(seg)
    rep = fx.get("replace") or {}
    if rep:
        used = set()
        for w in out:
            m = re.match(r"^(\W*)(.*?)(\W*)$", w["w"])
            for wrong, right in rep.items():
                if m.group(2) == wrong:
                    w["w"] = m.group(1) + right + m.group(3)
                    w["edited"] = True
                    used.add(wrong)
        for wrong in set(rep) - used:
            warn(f"{v['id']}: replace '{wrong}' matched no word (replace works on single whole words; "
                 "fix phrases with 'lines')")
    if fx.get("fillers", "remove") == "remove":
        out = [w for w in out if norm(w["w"]) not in FILLERS]
    prof = fx.get("profanity", "keep")
    if prof != "keep":
        kept = []
        for w in out:
            if norm(w["w"]) in PROFANE:
                if prof == "remove":
                    continue
                w = dict(w, w=mask(w["w"]))
            kept.append(w)
        out = kept
    emph = [e for e in fx.get("emphasis") or [] if isinstance(e, str) and e.strip()]
    for phrase in emph:
        toks = [norm(t) for t in tokens_of(phrase, lang)]
        hit = False
        for i in range(len(out) - len(toks) + 1):
            if [norm(out[i + k]["w"]) for k in range(len(toks))] == toks:
                for k in range(len(toks)):
                    out[i + k]["k"] = 1
                hit = True
        if not hit:
            warn(f"{v['id']}: emphasis '{phrase}' is not in the transcript")
    sounds = []
    for at, tag in (fx.get("sounds") or {}).items():
        try:
            if float(at) >= (tr.get("duration") or float("inf")):
                warn(f"{v['id']}: sound tag at {at} s is after the end of the video; left out")
                continue
            sounds.append({"at": float(at), "text": str(tag)})
        except ValueError:
            die(f"{rel(fx_path)}: sounds keys are seconds, like \"4.2\"")
    data = {"video": tr["video"], "language": lang, "source": tr["source"], "duration": tr["duration"],
            "width": tr.get("width"), "height": tr.get("height"), "timing": tr.get("timing", "measured"),
            "proofread": bool(fx), "words": out, "sounds": sounds}
    write_json(os.path.join(folder, "words.json"), data)
    if not quiet:
        edited = sum(1 for w in out if w.get("edited"))
        print(f"{v['id']}: {len(out)} words{f', {edited} corrected' if edited else ''}"
              f"{', not proofread (no fixes.json)' if not fx else ''} -> {rel(folder)}/words.json")
    return data


def report(job, v):
    folder = video_dir(job, v)
    tr_path = os.path.join(folder, "transcript.json")
    if not os.path.exists(tr_path):
        die(f"{v['id']}: no transcript yet; run transcribe.py first")
    tr = read_json(tr_path)
    words = tr["words"]
    vocab = [str(x) for x in job.get("vocab", [])]
    vtoks = {norm(t): t for x in vocab for t in x.split() if len(norm(t)) > 2}
    print(f"\n== {v['id']} ({rel(folder)}/transcript.txt, {len(words)} words)")
    low = [w for w in words if w.get("p", 1) < LOW_CONFIDENCE]
    for w in low:
        print(f"  unsure  {short(w['start'])}  {w['w']} ({w['p']:.2f})")
    for w in words:
        n = norm(w["w"])
        if len(n) > 2 and n not in vtoks:
            close = difflib.get_close_matches(n, list(vtoks), n=1, cutoff=0.75)
            if close:
                print(f"  name?   {short(w['start'])}  {w['w']} -> {vtoks[close[0]]} (from vocab)")
    for i, w in enumerate(words):
        if re.search(r"\d", w["w"]) and i + 1 < len(words) and re.match(r"^[,.]?\d", words[i + 1]["w"]):
            print(f"  number  {short(w['start'])}  '{w['w']} {words[i + 1]['w']}' may be one number")
    text = " ".join(norm(w["w"]) for w in words)
    for phantom in ("thanks for watching", "thank you for watching", "subscribe", "subtitles by",
                    "please like", "see you in the next"):
        if phantom in text:
            print(f"  invented? '{phantom}' is a phrase transcription engines often make up over music or "
                  "silence; check it was really said")
    tri = [" ".join(norm(w["w"]) for w in words[i:i + 3]) for i in range(len(words) - 2)]
    seen = {}
    for i, t in enumerate(tri):
        if t in seen and i - seen[t] <= 6 and len(t) > 6:
            print(f"  repeat  {short(words[i]['start'])}  '{t}' repeats; engines sometimes loop, check it")
            break
        seen[t] = i
    if tr.get("timing") == "estimated":
        print("  timing  word times come from subtitles and are estimated; a word-highlight style will drift")
    print("  Then read every line of transcript.txt: names, numbers, brand terms, missing punctuation.")


def main():
    ap = argparse.ArgumentParser(description="Report what to proofread, or apply fixes.json.")
    ap.add_argument("job")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--only")
    a = ap.parse_args()
    job = load_job(a.job)
    for v in selected(job, a.only):
        report(job, v) if a.report else apply(job, v)


if __name__ == "__main__":
    guard(main)
