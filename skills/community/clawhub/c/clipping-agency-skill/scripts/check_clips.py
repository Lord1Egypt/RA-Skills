#!/usr/bin/env python3
"""Check one episode batch before the client sees it: every clip against the platforms, the client's
file and every other client's clips.

    python3 scripts/check_clips.py clients/<client>/episodes/<episode>/batch.json

Per clip: the reason the moment was picked; the file's length, size and format for each of the client's
platforms; 9:16; a caption for every platform within its limits (Instagram's 5 hashtags, the YouTube
title); names the client's dictionary marks as wrong (in captions, title and hook); the client's no-go
topics (in what is said in the clip, the hook and the captions); a sponsor segment inside the clip (the
captions must say it is paid, and the platform labels are set); a sponsor read that wasn't marked; the
episode's guest release; possible music (a hint from the captions' [MUSIC] cues, the episode's marked
music and stretches with sound but no words: never a guarantee either way). Across clips and clients:
the same file twice in the batch, or a file that already went to another client (the ledger and every
other client's clips in this folder) or to another episode of this client. Exit code 0 when there are no
errors.

Listening: when faster-whisper is installed (pip install faster-whisper), check_clips.py transcribes
every cut clip from start to end (before the end card) and compares what it heard with the episode's
own words for that stretch. It warns on any word that isn't heard (a word cut out inside the clip),
on a first word that isn't the clip's first planned word (cut off), and on a last word after the last
planned one (the next sentence starting). A transcriber mishears old or noisy audio, so a warning means
listen to that spot; no warning is a strong hint, never a guarantee. The result is kept in
clips/listen.json per file, so it runs once per cut. AGENCY_LISTEN_MODEL picks the model (default
base; small hears better). Without faster-whisper it says so and skips this check; listen to each
clip yourself then.
"""
import argparse, json, os, re, subprocess, sys, tempfile

sys.dont_write_bytecode = True   # nothing is ever written into the skill's own folder
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agencylib import (DISCLOSURE_WORDS, LIMITS, MAX_CLIPS, PLATFORMS, SPONSOR_READ, accounts_of,  # noqa: E402
                       captions_of, clean_ranges, client_ids, clip_hash, connected_id, die, file_issues, guard,
                       hashtags, is_num, ledger_path, load_ledger, overlap_seconds, probe, read_json, rel, sha256,
                       stamp, text_length, topic_hits, workspace_of, wrong_names, batch_fp, valid_id, cut_spec, write_json)
import client as client_mod  # noqa: E402
from make_clips import load_batch  # noqa: E402

MUSIC_CUE = re.compile(r"(?i)\b(?:music|song|singing|jingle)\b|♪")


class Issues:
    def __init__(self):
        self.items = []

    def add(self, level, where, msg):
        if (level, where, msg) not in self.items:
            self.items.append((level, where, msg))

    def errors(self):
        return [i for i in self.items if i[0] == "error"]


def _starts_in(w, a, b):
    """A word starts in [a, b), or the range starts inside the word with most of the word after it (a word
    the transcriber timed too early; make_clips.py captions it the same way)."""
    s, e = w.get("start", -1), w.get("end", -1)
    if a - 0.05 <= s < b:
        return True
    return s < a < e and (e - a) > 0.5 * (e - s)


def words_in(words, ranges):
    return [w for w in words if any(_starts_in(w, a, b) for a, b in ranges)]


def silent_sound(levels, words, ranges, min_run=4):
    """Stretches of at least min_run seconds inside the clip with sound near the usual level but no words:
    music, applause or noise. [(start, end)] in source seconds."""
    if len(levels) < 10:
        return []
    med = sorted(v for _, v in levels)[len(levels) // 2]
    spoken = [(w["start"], w["end"]) for w in words]
    runs, cur = [], None
    for t, v in levels:
        if not any(a <= t and t + 1 <= b for a, b in ranges):
            if cur:
                runs.append(cur)
                cur = None
            continue
        talk = any(s < t + 1 and e > t for s, e in spoken)
        if not talk and v > med - 6:
            cur = [t, t + 1] if cur is None else [cur[0], t + 1]
        else:
            if cur:
                runs.append(cur)
            cur = None
    if cur:
        runs.append(cur)
    return [(a, b) for a, b in runs if b - a >= min_run]


def other_client_files(ws, cid):
    """{sha256: (client, episode, clip)} for every clip manifest of every other client in this folder."""
    out = {}
    for o in client_ids(ws):
        if o == cid:
            continue
        root = os.path.join(ws, "clients", o, "episodes")
        if not os.path.isdir(root):
            continue
        for ep in sorted(os.listdir(root)):
            mp = os.path.join(root, ep, "clips", "manifest.json")
            if os.path.isfile(mp):
                try:
                    m = read_json(mp)
                except SystemExit:
                    continue
                for c in (m.get("clips") or []) if isinstance(m, dict) else []:
                    if isinstance(c, dict) and isinstance(c.get("sha256"), str):
                        out[c["sha256"]] = (o, ep, c.get("id"))
    return out


EDGE_S = 2.5


def norm_word(w):
    return re.sub(r"[^a-z0-9']", "", str(w).lower())


def edge_problems(heard_head, heard_tail, want_head, want_tail):
    """Warnings from what a transcriber heard at a clip's edges against the words the clip should start and end
    with. heard_*: words heard in the first and last seconds; want_*: the first and last planned words."""
    out = []
    word = lambda w: norm_word(w) if re.search(r"[a-z]", norm_word(w)) else ""  # noqa: E731  (noise heard as digits)
    hh = [word(w) for w in heard_head if word(w)]
    ht = [word(w) for w in heard_tail if word(w)]
    heard_head = [w for w in heard_head if word(w)]
    heard_tail = [w for w in heard_tail if word(w)]
    wh = [norm_word(w) for w in want_head if norm_word(w)][:3]
    wt = [norm_word(w) for w in want_tail if norm_word(w)][-3:]
    if hh and wh and hh[0] not in wh:
        out.append(f"opens on \"{heard_head[0]}\" where the clip should open on \"{want_head[0]}\": a first word cut off?"
                   " Listen to the first second. If a word is cut, start the clip at another sentence: a cut starts at the "
                   "first word the transcript has, so a word it missed can't be kept")
    if ht and wt and ht[-1] not in wt:
        out.append(f"ends on \"{heard_tail[-1]}\" after the last planned word \"{want_tail[-1]}\": the start of the next "
                   "word may be in the clip. Listen to the last second, and end a little earlier if so")
    return out


FILLER_WORDS = {"um", "uh", "uhm", "erm", "hmm", "mm", "ah", "er"}


def _tokens(ws):
    out = []
    for w in ws:
        for part in re.split(r"[-\s]+", str(w)):
            t = norm_word(part)
            if t and re.search(r"[a-z]", t) and t not in FILLER_WORDS and not (out and out[-1] == t):
                out.append(t)  # a word said twice in a row counts once: make_clips may cut the stutter
    return out


def missing_words(heard, wanted):
    """Words of the episode that a full listen of the clip didn't hear, each with a few words around it:
    ["'place' (as a place as a direction), heard as 'this'"]. Fewer words heard than spoken always count;
    a word heard as another counts when it has 4 letters or more and the two clearly differ (a short
    word misheard, "as" for "is", doesn't)."""
    import difflib
    want, got = _tokens(wanted), _tokens(heard)
    if not want or not got:
        return []
    out = []
    sm = difflib.SequenceMatcher(None, want, got, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        lost = []
        if op == "delete":
            lost = want[i1:i2]
        elif op == "replace" and (i2 - i1) > (j2 - j1):
            lost = want[i1:i2]
        elif op == "replace":   # as many words heard as spoken: only a clearly different longer word counts
            lost = [x for x, y in zip(want[i1:i2], got[j1:j2])
                    if len(x) >= 4 and difflib.SequenceMatcher(None, x, y).ratio() < 0.8]
        if lost:
            ctx = " ".join(want[max(0, i1 - 3):min(len(want), i2 + 3)])
            heard_as = " ".join(got[j1:j2])
            out.append(f"'{' '.join(lost)}' ({ctx})" + (f", heard as '{heard_as}'" if heard_as else ""))
    return out


def listener():
    """faster-whisper's model for the edge check, or None when it isn't installed."""
    try:
        from faster_whisper import WhisperModel  # noqa: F401
        import numpy  # noqa: F401
    except ImportError:
        return None
    from faster_whisper import WhisperModel
    return WhisperModel(os.environ.get("AGENCY_LISTEN_MODEL", "base"), device="cpu", compute_type="int8")


def hear(model, path, start, length):
    import numpy as np
    fd, tmp = tempfile.mkstemp(suffix=".f32")
    os.close(fd)
    try:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0.0, start):.3f}", "-t", f"{length:.3f}", "-i", path,
                        "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", tmp], capture_output=True)
        audio = np.fromfile(tmp, dtype=np.float32)
    finally:
        os.remove(tmp)
    if not len(audio):
        return []
    segs, _ = model.transcribe(audio, word_timestamps=True, vad_filter=False, language="en",
                               condition_on_previous_text=False, beam_size=5)
    return [w.word.strip() for s in segs for w in (s.words or []) if w.word.strip()]


def listen_batch(batch_path):
    """Listen to the edges of every cut clip of a batch; results in clips/listen.json. Returns a message."""
    model = listener()
    if model is None:
        return ("note: faster-whisper isn't installed, so the clips' first and last words weren't listened to. Listen to "
                "the start and end of each clip yourself, or pip install faster-whisper")
    batch, c, cdir, bdir = load_batch(batch_path)
    mp = os.path.join(bdir, "clips", "manifest.json")
    if not os.path.isfile(mp):
        return "note: nothing cut yet, so nothing to listen to"
    man = read_json(mp, "the clip manifest")
    lp = os.path.join(bdir, "clips", "listen.json")
    old = read_json(lp) if os.path.isfile(lp) else {}
    out = {}
    for cl in man.get("clips") or []:
        path = os.path.join(bdir, "clips", cl.get("file") or "")
        if not os.path.isfile(path):
            continue
        sha = sha256(path)
        model_name = os.environ.get("AGENCY_LISTEN_MODEL", "base")
        if (isinstance(old.get(cl["id"]), dict) and old[cl["id"]].get("sha256") == sha and "words" in old[cl["id"]]
                and old[cl["id"]].get("model") == model_name):
            out[cl["id"]] = old[cl["id"]]
            continue
        speech = float(cl.get("seconds") or probe(path)["duration"]) - float(cl.get("end_card_seconds") or 0)
        heard = hear(model, path, 0, speech)
        out[cl["id"]] = {"sha256": sha, "model": model_name, "words": heard,
                         "head": hear(model, path, 0, EDGE_S), "tail": hear(model, path, speech - EDGE_S, EDGE_S)}
    write_json(lp, out)
    return f"listened to {len(out)} clip(s) from start to end (clips/listen.json)"


def check_batch(batch_path, ledger_file=None):
    """Everything approve.py and schedule.py need: the client, the rows (one per clip) with their
    fingerprints, every issue, and the batch fingerprint."""
    batch, c, cdir, bdir = load_batch(batch_path)
    ws = os.path.dirname(os.path.dirname(cdir))
    cid = c.get("id")
    ck = Issues()
    lpath = ledger_path(ledger_file)
    ledger = load_ledger(lpath)
    for lv, f, msg in client_mod.validate(c, ws, os.path.basename(cdir), ledger):
        if lv == "error":
            ck.add("error", "client.json", f"{f}: {msg}")
    if c.get("status", "active") != "active":
        ck.add("error", "client.json", f"the client is {c.get('status')}: no pages or posts")
    ep = batch["episode"]
    if not valid_id(str(ep.get("id") or "")):
        ck.add("error", "episode.id", "lowercase letters, digits and single dashes (it names the folder and the page)")
    plats = [p.upper() for p in c.get("platforms") or [] if isinstance(p, str) and p.upper() in PLATFORMS]
    accs = accounts_of(c)
    names = c.get("names") if isinstance(c.get("names"), dict) else {}
    no_go = c.get("no_go") if isinstance(c.get("no_go"), list) else []
    # the episode: guests and their releases
    guests = ep.get("guests") if isinstance(ep.get("guests"), list) else []
    release = ep.get("guest_release", "unknown")
    contract = c.get("guest_release") == "covered_by_contract"
    if release not in ("on_file", "not_needed", "missing", "unknown"):
        ck.add("error", "episode.guest_release", "on_file, not_needed, missing or unknown")
    elif guests and release in ("missing", "unknown") and not contract:
        ck.add("error", "episode.guest_release", f"guest(s) {', '.join(map(str, guests))} and no release on file: a "
               "guest who agreed to the episode may not have agreed to short clips on social. Get the release (or the "
               "client's written word that it covers social clips) and set \"on_file\"")
    elif not guests and release == "unknown":
        ck.add("warning", "episode.guests", "no guests listed: if anyone besides the host is in the clips, list them and "
               "their release status")
    sponsors = []
    for s in ep.get("sponsor_segments") or []:
        if isinstance(s, dict) and is_num(s.get("start"), 0) and is_num(s.get("end"), 0) and s["end"] > s["start"]:
            sponsors.append((float(s["start"]), float(s["end"]), str(s.get("sponsor") or "a sponsor")))
        else:
            ck.add("error", "episode.sponsor_segments", "each is {\"start\": s, \"end\": s, \"sponsor\": \"Name\"} in "
                   "seconds of the episode")
    music_marked = clean_ranges(ep.get("music")) if ep.get("music") else []
    if ep.get("music") and music_marked is None:
        ck.add("error", "episode.music", "a list of [start, end] pairs in seconds of the episode")
        music_marked = []
    # the transcript, for what is said inside each clip
    tpath = os.path.join(bdir, ep.get("transcript") or os.path.join("work", "transcript.json"))
    tr = read_json(tpath, "the transcript") if os.path.isfile(tpath) else {}
    words = tr.get("words") if isinstance(tr, dict) and isinstance(tr.get("words"), list) else []
    events = tr.get("events") if isinstance(tr, dict) and isinstance(tr.get("events"), list) else []
    levels = [tuple(x) for x in (tr.get("levels") or []) if isinstance(x, list) and len(x) == 2] if isinstance(tr, dict) else []
    if not words:
        ck.add("warning", "transcript", f"{rel(tpath)} not found or empty: no-go topics and sponsor reads are checked in "
               "the captions only")
    # the cut clips
    mpath = os.path.join(bdir, "clips", "manifest.json")
    manifest = read_json(mpath, "the clip manifest") if os.path.isfile(mpath) else {}
    if manifest and manifest.get("client") not in (None, cid):
        ck.add("error", "clips/manifest.json", f"these clips were cut for client {manifest.get('client')}, not {cid}")
    mclips = {m.get("id"): m for m in manifest.get("clips", []) if isinstance(m, dict)} if isinstance(manifest, dict) else {}
    lpath_ = os.path.join(bdir, "clips", "listen.json")
    heard = read_json(lpath_) if os.path.isfile(lpath_) else {}
    heard = heard if isinstance(heard, dict) else {}
    clips = batch["clips"]
    if not clips:
        ck.add("error", "clips", "no clips in batch.json yet")
    if len(clips) > MAX_CLIPS:
        ck.add("error", "clips", f"{len(clips)} clips; at most {MAX_CLIPS} per episode. Fewer good clips beat padding")
    elif 0 < len(clips) < 3:
        ck.add("note", "clips", f"{len(clips)} clip(s): fine when the episode doesn't hold more strong moments; say so "
               "to the client")
    agreed = c.get("clips_per_episode")
    if isinstance(agreed, int) and len(clips) > agreed:
        ck.add("note", "clips", f"{len(clips)} clips, {agreed} agreed per episode")
    others = other_client_files(ws, cid)
    rows, seen_sha = [], {}
    for i, clip in enumerate(clips):
        if not isinstance(clip, dict) or not isinstance(clip.get("id"), (str, int)):
            ck.add("error", f"clip {i + 1}", "every clip needs an id")
            continue
        k = str(clip["id"]).zfill(2)
        where = f"clip {k}"
        row = {"id": k, "clip": clip, "issues": [], "sponsor": None, "music": []}

        def add(level, msg, where=where, row=row):
            row["issues"].append((level, msg))
            ck.add(level, where, msg)
        if not isinstance(clip.get("why"), str) or len(clip["why"].split()) < 4:
            add("error", "say why this moment was picked (\"why\"): it stands alone, opens on the point, and what it gives "
                "the viewer. The client reads it on the approval page")
        hook = clip.get("hook") if isinstance(clip.get("hook"), str) else ""
        if hook and len(hook.split()) > 10:
            add("warning", f"the hook has {len(hook.split())} words; 8 or fewer reads in time")
        m = mclips.get(k)
        if isinstance(clip.get("file"), str):
            path = clip["file"] if os.path.isabs(clip["file"]) else os.path.join(bdir, clip["file"])
            ranges = clean_ranges(clip.get("ranges")) or (
                [(float(clip["start"]), float(clip["end"]))] if is_num(clip.get("start"), 0) and is_num(clip.get("end"), 0)
                and clip["end"] > clip["start"] else None)
            if ranges is None:
                add("error", "a clip you cut yourself needs \"start\" and \"end\" (or \"ranges\") in seconds of the episode")
                ranges = []
        elif m:
            path = os.path.join(bdir, "clips", m.get("file") or f"clip-{k}.mp4")
            ranges = clean_ranges(m.get("ranges")) or []
        else:
            add("error", "not cut yet: run make_clips.py on this batch")
            rows.append(row)
            continue
        if not os.path.isfile(path):
            add("error", f"{rel(path)} isn't there: run make_clips.py again")
            rows.append(row)
            continue
        info = probe(path)
        sha = sha256(path)
        row.update(file=path, info=info, sha256=sha, ranges=ranges, manifest=m or {})
        cover = os.path.join(bdir, "clips", (m or {}).get("cover") or f"clip-{k}-cover.jpg")
        row["cover"] = cover if os.path.isfile(cover) else None
        if m and not isinstance(clip.get("file"), str) and m.get("spec") and m["spec"] != cut_spec(clip):
            add("error", "batch.json changed after this clip was cut (its times, hook or framing): run make_clips.py "
                "again so the file is what the batch says")
        if m and m.get("sha256") and m["sha256"] != sha:
            add("warning", "the file changed after make_clips.py wrote the manifest; cut it again so the manifest matches")
        if sha in seen_sha:
            add("error", f"the same file as clip {seen_sha[sha]}: one file, one clip")
        seen_sha[sha] = k
        rec = ledger["clips"].get(sha) or {}
        owner = rec.get("client")
        used = [e for e in list(ledger["posts"].values()) + list(ledger.get("planned", {}).values())
                if isinstance(e, dict) and e.get("sha256") == sha and e.get("client") == cid
                and (e.get("episode"), e.get("clip")) != (ep.get("id"), k) and e.get("status") not in ("cancelled", "failed")]
        if owner and owner != cid:
            add("error", f"this exact file already went to client {owner}. A clip is never used for two clients; "
                "cut this client's own")
        elif used or (owner == cid and (rec.get("episode"), rec.get("clip")) != (ep.get("id"), k)):
            o = used[0] if used else rec
            add("error", f"the same file as episode {o.get('episode')} clip {o.get('clip')} of this client. Nothing goes out "
                "twice on the same accounts")
        elif sha in others:
            o = others[sha]
            add("error", f"the same file as client {o[0]}'s clip {o[2]} (episode {o[1]}). A clip is never used for two "
                "clients")
        w, h = info["width"], info["height"]
        if abs(w / h - 9 / 16) > 0.02:
            add("error", f"{w}x{h} isn't vertical 9:16")
        elif w < 1080:
            add("note", f"{w}x{h}: fine for a draft or an example; for the client's posts cut at 1080x1920")
        caps = captions_of(clip)
        for p in plats:
            tmax = (accs.get("TIKTOK") or {}).get("max_video_s") if p == "TIKTOK" else None
            for lv, msg in file_issues(info, p, tmax):
                add(lv, f"{LIMITS[p]['label']}: {msg}")
            text = caps.get(p)
            if not text or not text.strip():
                add("error", f"no {LIMITS[p]['label']} caption (captions.{p})")
                continue
            n = text_length(p, text)
            lim = LIMITS[p].get("text") or LIMITS[p].get("text_bytes")
            if n > lim:
                add("error", f"{LIMITS[p]['label']} caption is {n} long; the limit is {lim}")
            if p == "INSTAGRAM" and len(hashtags(text)) > LIMITS[p]["tags_max"]:
                add("error", f"Instagram takes at most {LIMITS[p]['tags_max']} hashtags; this caption has {len(hashtags(text))}")
            if p == "YOUTUBE" and re.search(r"[<>]", text):
                add("error", "YouTube refuses < and > in the description")
            if p not in accs or not connected_id(accs.get(p)):
                add("note", f"{LIMITS[p]['label']} isn't connected: it's posted by hand until the client connects it")
        for p in caps:
            if p not in plats:
                add("warning", f"a caption for {p}, which isn't one of the client's platforms; it isn't used")
        if "YOUTUBE" in plats:
            title = clip.get("title")
            if not isinstance(title, str) or not title.strip():
                add("error", "no YouTube title (\"title\")")
            elif len(title) > LIMITS["YOUTUBE"]["title"] or re.search(r"[<>]", title):
                add("error", f"the YouTube title is {len(title)} characters (100 at most) or holds < or >")
        if clip.get("tags") is not None and not (isinstance(clip["tags"], list) and all(isinstance(t, str) for t in clip["tags"])):
            add("error", "tags is a list of words for YouTube")
        out_text = "\n".join([hook, clip.get("title") or ""] + list(caps.values()))
        for wrong, right in wrong_names(out_text, names):
            add("error", f"\"{wrong}\" is in the hook, title or a caption; the client spells it \"{right}\"")
        fixed = (m or {}).get("names_fixed") or []
        if fixed:
            add("note", "names spelled by the dictionary in the captions: " + ", ".join(
                sorted({f"{f.get('from')} -> {f.get('to')}" for f in fixed if isinstance(f, dict)})))
        said = " ".join(w.get("w", "") for w in words_in(words, ranges)) if ranges else ""
        hits = topic_hits(said + "\n" + out_text, no_go)
        if hits:
            why = clip.get("no_go_reviewed")
            if isinstance(why, str) and len(why.split()) >= 4:
                add("warning", f"touches the client's no-go list ({', '.join(hits)}); reviewed: {why}")
            else:
                add("error", f"touches the client's no-go list: {', '.join(hits)}. Drop the clip, or if it only mentions "
                    "the word in passing, say why in \"no_go_reviewed\" so the client sees it on the page")
        for a, b, who in sponsors:
            if overlap_seconds(ranges, [(a, b)]) > 0.5:
                row["sponsor"] = who
        if row["sponsor"]:
            for p in plats:
                if caps.get(p) and not DISCLOSURE_WORDS.search(caps[p]):
                    add("error", f"includes the sponsor segment for {row['sponsor']}: the {LIMITS[p]['label']} caption must "
                        "say it's paid (#ad, \"Sponsored by ...\" or \"Paid partnership with ...\")")
            add("note", f"paid partnership with {row['sponsor']}: TikTok's label goes on with the post; Instagram's paid "
                "partnership label and YouTube's paid promotion box are set in the apps (WoopSocial can't set them)")
        elif said and SPONSOR_READ.search(said):
            add("warning", f"sounds like a sponsor read (\"{SPONSOR_READ.search(said).group(0)}\"). If it is, add it to "
                "episode.sponsor_segments so the clip is labelled paid")
        if clip.get("promotes_client_business") is True:
            add("note", "promotes the client's own business: TikTok's \"Your brand\" label goes on")
        cues = [e for e in events if isinstance(e, dict) and MUSIC_CUE.search(str(e.get("text") or ""))
                and overlap_seconds(ranges, [(float(e.get("start", 0)), float(e.get("end", 0)))]) > 0.2]
        marked = [r for r in music_marked if overlap_seconds(ranges, [r]) > 0.2]
        quiet = silent_sound(levels, words, ranges) if levels else []
        for e in cues:
            row["music"].append(f"the captions mark [{e.get('text')}] at {stamp(e['start'])} of the episode")
        for a, b in marked:
            row["music"].append(f"music marked in the episode at {stamp(a)} to {stamp(b)}")
        for a, b in quiet:
            row["music"].append(f"{b - a:.0f} s with sound but no words at {stamp(a)} of the episode (music, applause "
                                "or noise)")
        if row["music"]:
            add("warning", "possible music: " + "; ".join(row["music"]) + ". Listen before the client approves: music "
                "the client doesn't hold the rights to can get the clip muted, claimed, or a Short over 60 s blocked. "
                "This is a hint, never a guarantee either way")
        h = heard.get(k)
        if isinstance(h, dict) and h.get("sha256") == sha and words and ranges:
            inside = [w.get("w", "") for w in words_in(words, ranges)]
            for msg in edge_problems(h.get("head") or [], h.get("tail") or [], inside[:3], inside[-3:]):
                add("warning", "clean edges: " + msg)
            if isinstance(h.get("words"), list):
                cuts = [(float(x), float(y)) for x, y in clip.get("cut") or [] if is_num(x, 0) and is_num(y, 0)]
                win = (m or {}).get("window") if isinstance((m or {}).get("window"), list) else None
                lo, hi = (float(win[0]), float(win[1])) if win else (min(x for x, _ in ranges), max(y for _, y in ranges))
                span_words = [w for w in words if _starts_in(w, lo, hi) and w.get("end", 0) <= hi + 0.15]
                want = [w.get("w", "") for w in span_words if not any(x - 0.02 <= w.get("start", -1) <= y for x, y in cuts)]
                lost = missing_words(h["words"], want)
                if lost:
                    add("warning", "a full listen didn't hear " + "; ".join(lost[:6]) + (" and more" if len(lost) > 6 else "")
                        + ". Listen to those spots: a word cut out inside a clip can change what the person said. "
                        "Cut again without tighten, or move the clip")
        if clip.get("reframe") == "stack":
            add("warning", "a stream clip: music under the talk (a game's or the stream's) isn't detected by any check here. "
                "Listen to the whole clip before the client sees it")
        row["hash"] = clip_hash(sha, clip)
        rows.append(row)
    ready = [r for r in rows if r.get("hash")]
    fp = batch_fp(cid, ep.get("id"), [(r["id"], r["hash"]) for r in ready]) if ready and len(ready) == len(rows) else None
    return {"batch": batch, "client": c, "cid": cid, "cdir": cdir, "bdir": bdir, "ws": ws, "ledger": ledger,
            "lpath": lpath, "rows": rows, "issues": ck.items, "fp": fp, "plats": plats, "episode": ep,
            "sponsors": sponsors, "batch_path": os.path.abspath(batch_path)}


def summary(m):
    lines = []
    for lv, where, msg in m["issues"]:
        lines.append(f"{lv}: {where}: {msg}")
    errs = sum(1 for i in m["issues"] if i[0] == "error")
    warns = sum(1 for i in m["issues"] if i[0] == "warning")
    return lines, errs, warns


def main():
    ap = argparse.ArgumentParser(description="Check an episode batch before the client sees it.")
    ap.add_argument("batch")
    ap.add_argument("--ledger")
    ap.add_argument("--no-listen", action="store_true", help="skip listening to the clips' first and last words")
    a = ap.parse_args()
    if not a.no_listen:
        print(listen_batch(a.batch))
    m = check_batch(a.batch, a.ledger)
    for r in m["rows"]:
        info = r.get("info")
        state = "blocked" if any(lv == "error" for lv, _ in r["issues"]) else "ok"
        print(f"clip {r['id']}" + (f" ({info['duration']:.1f} s)" if info else "") + f": {state}")
    lines, errs, warns = summary(m)
    if lines:
        print()
        print("\n".join(lines))
    print(f"\n{errs} error(s), {warns} warning(s)" + (f"; batch fingerprint {m['fp'][:8]}" if m["fp"] else ""))
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    guard(main)
