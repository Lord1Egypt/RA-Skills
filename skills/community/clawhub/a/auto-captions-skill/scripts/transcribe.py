#!/usr/bin/env python3
"""Transcribe videos with a time for every word.

    python3 scripts/transcribe.py job.json                 # every video in the job, best route available
    python3 scripts/transcribe.py job.json --engine local --model turbo
    python3 scripts/transcribe.py clip.mp4 --out work/clip  # one video, no job file
    python3 scripts/transcribe.py job.json --only intro --force

Routes ("auto" picks the first that works):
  from  - the video's own subtitles: a .srt or .vtt next to it (same name) or "subtitles" in the job.
          Free and instant; word times are estimated inside each cue.
  groq  - GROQ_API_KEY set: whisper-large-v3-turbo, about $0.04 per hour of audio. Audio is sent to Groq.
  deepgram - DEEPGRAM_API_KEY set: nova-3, labels speakers. Audio is sent to Deepgram.
  mlx   - Apple Silicon with mlx-whisper installed (pip install mlx-whisper): fast and private.
  local - faster-whisper on the CPU (pip install faster-whisper): free and private. The model is
          downloaded once. "small" (default) suits most clips; "turbo" is more accurate and slower.
  openai - OPENAI_API_KEY, only with --engine openai (whisper-1, retiring in February 2027).

Names from the job's "vocab" list are passed to the engine so it spells them right more often.
Writes work/<video id>/transcript.json (words with start, end and, when the engine gives it,
confidence) and transcript.txt (numbered lines the agent proofreads).
"""
import argparse, json, os, platform, shutil, subprocess, sys, tempfile, uuid
import urllib.error, urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aclib import (die, load_job, need_ffmpeg, probe, read_json, rel, selected, short, video_dir,  # noqa: E402
                   write_json, joiner, base_lang, split_text, guard, warn)

API_LIMIT = 24 * 1024 * 1024
CHUNK_SECONDS = 20 * 60
LOW_CONFIDENCE = 0.6


def extract_audio(src, dst, start=None, length=None, bitrate="48k"):
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-i", src, "-map", f"0:a:{probe(src)['audio_index']}"]  # the same track render.py keeps
    if length is not None:
        cmd += ["-t", f"{length:.3f}"]
    cmd += ["-vn", "-ac", "1", "-ar", "16000", "-c:a", "libmp3lame", "-b:a", bitrate, dst]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or not os.path.exists(dst):
        die(f"could not read the audio of {src}; does it have a sound track?")


def pcm16k(src):
    """The audio as 16 kHz mono float samples, decoded by ffmpeg (what Whisper models take)."""
    import numpy as np
    cmd = ["ffmpeg", "-v", "error", "-i", src, "-map", f"0:a:{probe(src)['audio_index']}", "-vn", "-ac", "1",
           "-ar", "16000", "-f", "f32le", "-"]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0 or not r.stdout:
        die(f"could not read the audio of {src}; does it have a sound track?")
    return np.frombuffer(r.stdout, dtype=np.float32).copy()


# ---------- routes ----------

SCRIPTS = [("ja", "\u3040-\u30ff"), ("ko", "\uac00-\ud7af"), ("zh", "\u4e00-\u9fff"), ("ar", "\u0600-\u06ff"),
           ("he", "\u0590-\u05ff"), ("th", "\u0e00-\u0e7f"), ("hi", "\u0900-\u097f"), ("ru", "\u0400-\u04ff"),
           ("el", "\u0370-\u03ff")]


def detect_script(text):
    """A language code from the writing system, for subtitle files given without a language.
    Latin-script text returns None (it can't be told apart by its letters)."""
    import re
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return None
    for code, rng in SCRIPTS:  # kana before Han: Japanese uses both
        n = len(re.findall(f"[{rng}]", text))
        if n >= max(3, 0.2 * len(letters)):
            return code
    return None


def from_subtitles(path, lang=None):
    import re
    text = open(path, encoding="utf-8-sig", errors="replace").read().replace("\r", "")
    detected = None if lang else detect_script(re.sub(r"[\d:,.>-]+", " ", text))
    lang = lang or detected
    st = r"(\d+:)?(\d{1,2}):(\d{2})[.,](\d{3})"
    cue = re.compile(st + r"\s*-->\s*" + st + r"[^\n]*\n(.*?)(?:\n\s*\n|\Z)", re.S)

    def secs(h, m, s, ms):
        return int((h or "0:")[:-1] or 0) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    words, prev = [], []
    for m in cue.finditer(text):
        a, b = secs(*m.group(1, 2, 3, 4)), secs(*m.group(5, 6, 7, 8))
        body = re.sub(r"<[^>]+>|\{[^}]*\}", "", m.group(9)).replace("\n", " ").strip()
        toks = split_text(body, lang)
        if not toks or b <= a:
            continue
        # rolling captions (auto-generated subtitles) repeat the end of the previous cue: skip it
        k = next((n for n in range(min(len(prev), len(toks)), 0, -1) if prev[-n:] == toks[:n]), 0)
        prev = list(toks)
        if k >= len(toks):
            continue
        toks = toks[k:]
        total = sum(len(t) for t in toks) or 1
        t = a
        for tok in toks:  # spread the cue's time over its words by length
            d = (b - a) * len(tok) / total
            words.append({"w": tok, "start": round(t, 3), "end": round(t + d, 3)})
            t += d
    if not words:
        die(f"no captions found in {path}")
    return words, "subtitles file (word times estimated)", detected


def post_multipart(url, headers, fields, file_path):
    boundary = uuid.uuid4().hex
    body = bytearray()
    for name, value in fields:
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n{value}\r\n".encode()
    body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"audio.mp3\"\r\n"
             "Content-Type: audio/mpeg\r\n\r\n").encode()
    with open(file_path, "rb") as fh:
        body += fh.read()
    body += f"\r\n--{boundary}--\r\n".encode()
    return http(url, dict(headers, **{"Content-Type": f"multipart/form-data; boundary={boundary}"}),
                bytes(body), file_path, fields)


def http(url, headers, data, file_path=None, fields=None):
    req = urllib.request.Request(url, data=data, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=900) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        die(f"transcription API error {e.code}: {e.read().decode(errors='replace')[:400]}")
    except urllib.error.URLError as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e.reason) and shutil.which("curl"):
            cmd = ["curl", "-sS", "-X", "POST", url]
            for k, v in headers.items():
                if k != "Content-Type" or fields is None:
                    cmd += ["-H", f"{k}: {v}"]
            if fields is not None:
                cmd += ["-F", f"file=@{file_path}"]
                for name, value in fields:
                    cmd += ["-F", f"{name}={value}"]
            else:
                cmd += ["--data-binary", f"@{file_path}"]
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
            try:
                return json.loads(r.stdout)
            except json.JSONDecodeError:
                die(f"transcription API returned: {r.stdout[:300]} {r.stderr[:200]}")
        die(f"could not reach the transcription API: {e.reason}")


def chunks(src, tmp):
    total = probe(src)["duration"]
    start = 0.0
    while start < total - 0.05:
        length = min(CHUNK_SECONDS, total - start)
        part = os.path.join(tmp, f"chunk-{int(start)}.mp3")
        extract_audio(src, part, start, length, "32k")
        if os.path.getsize(part) > API_LIMIT:
            extract_audio(src, part, start, length, "16k")
        yield start, length, part
        start += length


def via_whisper_api(src, engine, tmp, lang, vocab):
    url, env, model = {
        "groq": ("https://api.groq.com/openai/v1/audio/transcriptions", "GROQ_API_KEY", "whisper-large-v3-turbo"),
        "openai": ("https://api.openai.com/v1/audio/transcriptions", "OPENAI_API_KEY", "whisper-1"),
    }[engine]
    key = os.environ.get(env)
    if not key:
        die(f"{env} is not set")
    words, detected = [], None
    for start, length, part in chunks(src, tmp):
        print(f"  sending {short(start)} to {short(start + length)} to {engine}...", flush=True)
        fields = [("model", model), ("response_format", "verbose_json"),
                  ("timestamp_granularities[]", "word"), ("timestamp_granularities[]", "segment")]
        if lang:
            fields.append(("language", base_lang(lang)))
        if vocab:
            fields.append(("prompt", ", ".join(vocab)[:600]))  # the prompt is limited to 224 tokens
        r = post_multipart(url, {"Authorization": f"Bearer {key}"}, fields, part)
        detected = detected or r.get("language")
        got = [{"w": str(w["word"]).strip(), "start": round(float(w["start"]) + start, 3),
                "end": round(float(w["end"]) + start, 3)} for w in r.get("words") or [] if str(w.get("word", "")).strip()]
        words += punctuate(got, " ".join(str(sg.get("text", "")) for sg in r.get("segments") or []))
    if not words:
        die(f"{engine} returned no word times")
    return words, f"{engine} ({model})", detected


def punctuate(words, text):
    """The word list of some APIs has no punctuation; take each word's written form from the
    segment text (same words, in order), so captions can break at sentence ends and commas."""
    import re
    if not text.strip() or any(re.search(r"[.,?!]", w["w"]) for w in words):
        return words
    toks = text.split()
    norm = lambda t: re.sub(r"[^\w]", "", t.lower())
    j = 0
    for w in words:
        for k in range(j, min(j + 4, len(toks))):
            if norm(toks[k]) == norm(w["w"]):
                w["w"] = toks[k]
                j = k + 1
                break
    return words


def via_deepgram(src, tmp, lang, vocab):
    key = os.environ.get("DEEPGRAM_API_KEY")
    if not key:
        die("DEEPGRAM_API_KEY is not set")
    import urllib.parse
    words, detected = [], None
    part = os.path.join(tmp, "audio.mp3")
    extract_audio(src, part, bitrate="32k")  # one request: Deepgram takes long files, speakers stay numbered
    for start in (0.0,):
        print("  sending the audio to Deepgram...", flush=True)
        q = [("model", "nova-3"), ("smart_format", "true"), ("punctuate", "true"), ("diarize", "true")]
        q.append(("language", lang) if lang else ("detect_language", "true"))
        for term in (vocab or [])[:50]:
            q.append(("keyterm", term))
        url = "https://api.deepgram.com/v1/listen?" + urllib.parse.urlencode(q)
        with open(part, "rb") as fh:
            data = fh.read()
        r = http(url, {"Authorization": f"Token {key}", "Content-Type": "audio/mpeg"}, data, part)
        ch = ((r.get("results") or {}).get("channels") or [{}])[0]
        detected = detected or ch.get("detected_language")
        alt = (ch.get("alternatives") or [{}])[0]
        for w in alt.get("words") or []:
            item = {"w": (w.get("punctuated_word") or w["word"]).strip(), "start": round(w["start"] + start, 3),
                    "end": round(w["end"] + start, 3), "p": round(float(w.get("confidence", 1)), 3)}
            if "speaker" in w:
                item["speaker"] = int(w["speaker"])
            words.append(item)
    if not words:
        die("Deepgram returned no words")
    return words, "deepgram (nova-3)", detected


def via_mlx(src, tmp, model, lang, vocab):
    import mlx_whisper
    audio = os.path.join(tmp, "audio.mp3")
    extract_audio(src, audio, bitrate="64k")
    repo = {"turbo": "mlx-community/whisper-large-v3-turbo", "small": "mlx-community/whisper-small-mlx",
            "base": "mlx-community/whisper-base-mlx", "medium": "mlx-community/whisper-medium-mlx",
            "large-v3": "mlx-community/whisper-large-v3-mlx", "tiny": "mlx-community/whisper-tiny-mlx"}.get(model, model)
    print(f"  transcribing with mlx-whisper {repo} (first run downloads the model)...", flush=True)
    kw = {"path_or_hf_repo": repo, "word_timestamps": True, "condition_on_previous_text": False,
          "hallucination_silence_threshold": 2.0}  # fewer invented lines over music and silence
    if lang:
        kw["language"] = base_lang(lang)
    if vocab:
        kw["initial_prompt"] = ", ".join(vocab)
    r = mlx_whisper.transcribe(audio, **kw)
    words = []
    for seg in r.get("segments", []):
        for w in seg.get("words", []):
            words.append({"w": w["word"].strip(), "start": round(w["start"], 3), "end": round(w["end"], 3),
                          "p": round(float(w.get("probability", 1)), 3)})
    return words, f"mlx-whisper ({model})", r.get("language")


def via_local(src, tmp, model, lang, vocab):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        die("Local transcription needs faster-whisper: pip install faster-whisper\n"
            "Or set GROQ_API_KEY or DEEPGRAM_API_KEY, or give the video's own .srt/.vtt subtitles.")
    audio = pcm16k(src)  # decoded by ffmpeg, so faster-whisper's own decoder (PyAV) is never needed
    name = "large-v3-turbo" if model == "turbo" else model
    print(f"  transcribing locally with faster-whisper '{name}' (first run downloads the model)...", flush=True)
    m = WhisperModel(name, device="cpu", compute_type="int8")
    kw = {"word_timestamps": True, "vad_filter": True, "condition_on_previous_text": False}
    if lang:
        kw["language"] = base_lang(lang)
    if vocab:
        kw["hotwords"] = " ".join(vocab)
    segments, info = m.transcribe(audio, **kw)
    words, last = [], 0
    for seg in segments:
        for w in seg.words or []:
            words.append({"w": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3),
                          "p": round(float(w.probability), 3)})
        if seg.end - last > 120:
            print(f"  {seg.end / (info.duration or 1):.0%}", flush=True)
            last = seg.end
    return words, f"faster-whisper ({name})", info.language


def pick_engine(want, has_subs):
    if want != "auto":
        return want
    if has_subs:
        return "from"
    if os.environ.get("GROQ_API_KEY"):
        return "groq"
    if os.environ.get("DEEPGRAM_API_KEY"):
        return "deepgram"
    if platform.system() == "Darwin" and platform.machine() == "arm64":
        try:
            import mlx_whisper  # noqa: F401
            return "mlx"
        except ImportError:
            pass
    return "local"


# ---------- output ----------

CONTRACTION = ("'s", "'ve", "'re", "'ll", "'d", "'m", "'t", "n't")


def tidy(words, lang, engine="local"):
    """Join pieces an engine split: a number ("17" + ",500") and, for the API routes, contractions
    ("we" + "'ve"). Real words that start with an apostrophe or a dash ("'90s", "-5") stay apart."""
    out = []
    for w in words:
        t = str(w["w"]).strip()
        if not t:
            continue
        w = dict(w, w=t)
        low = t.lower().replace("’", "'")
        number_tail = engine != "from" and out and out[-1]["w"][-1:].isdigit() and len(t) > 1 and t[0] in ",." \
            and t[1].isdigit()
        contraction = engine in ("groq", "openai") and out and joiner(lang) and low.rstrip(".,?!") in CONTRACTION
        if number_tail or contraction:
            prev = out[-1]
            merged = dict(prev, w=prev["w"] + t, end=w["end"])
            if "p" in prev or "p" in w:
                merged["p"] = min(prev.get("p", 1), w.get("p", 1))
            out[-1] = merged
        else:
            out.append(w)
    for i in range(1, len(out)):  # times never run backwards
        if out[i]["start"] < out[i - 1]["start"]:
            out[i]["start"] = out[i - 1]["start"]
        if out[i]["end"] < out[i]["start"]:
            out[i]["end"] = out[i]["start"]
    return out


def lines_of(words, lang, max_gap=0.7, max_words=30):
    """Sentence-sized lines (or a pause), numbered for the agent's fixes."""
    out, cur = [], []
    j = joiner(lang)
    for i, w in enumerate(words):
        cur.append(i)
        nxt = words[i + 1] if i + 1 < len(words) else None
        end = w["w"][-1:] in ".?!。？！"
        if nxt is None or end or nxt["start"] - w["end"] > max_gap or len(cur) >= max_words:
            out.append({"n": len(out) + 1, "first": cur[0], "last": cur[-1], "start": words[cur[0]]["start"],
                        "end": words[cur[-1]]["end"], "text": j.join(words[k]["w"] for k in cur)})
            cur = []
    return out


def write_outputs(folder, data):
    write_json(os.path.join(folder, "transcript.json"), data)
    words, lang = data["words"], data.get("language")
    with open(os.path.join(folder, "transcript.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"# {os.path.basename(data['video'])}: {len(words)} words via {data['source']}"
                 f"{', language ' + lang if lang else ''}\n")
        fh.write("# Fix mistakes in fixes.json (see references/proofreading.md), never in this file.\n")
        for ln in lines_of(words, lang):
            fh.write(f"L{ln['n']} [{short(ln['start'])}-{short(ln['end'])}] {ln['text']}\n")
        low = [w for w in words if w.get("p", 1) < LOW_CONFIDENCE]
        if low:
            fh.write(f"\n# Unsure words (confidence under {LOW_CONFIDENCE}): check these first\n")
            for w in low[:80]:
                fh.write(f"#  {short(w['start'])} {w['w']} ({w['p']:.2f})\n")


def transcribe_one(src, folder, engine, model, lang, vocab, subs, force):
    out = os.path.join(folder, "transcript.json")
    old = read_json(out) if os.path.exists(out) else None
    if not isinstance(old, dict):
        old = None
    if old and not force and old.get("video_bytes") == os.path.getsize(src):
        print(f"{rel(src)}: already transcribed ({old.get('source')}); --force to redo")
        return
    if engine == "from":
        print(f"  using {rel(subs)} instead of transcribing (word times are estimated, so highlight styles "
              "turn their highlight off; --engine local transcribes the speech instead)")
    info = probe(src)
    if not info["audio"] and engine != "from":
        die(f"{rel(src)} has no sound track. Give its subtitles (.srt/.vtt) instead.")
    os.makedirs(folder, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        if engine == "from":
            words, source, detected = from_subtitles(subs, lang)
        elif engine in ("groq", "openai"):
            words, source, detected = via_whisper_api(src, engine, tmp, lang, vocab)
        elif engine == "deepgram":
            words, source, detected = via_deepgram(src, tmp, lang, vocab)
        elif engine == "mlx":
            words, source, detected = via_mlx(src, tmp, model, lang, vocab)
        else:
            words, source, detected = via_local(src, tmp, model, lang, vocab)
    language = lang or detected
    words = tidy(words, language, engine)
    if not words:
        die(f"{rel(src)}: no speech found. If it is music only, there is nothing to caption.")
    data = {"video": os.path.abspath(src), "video_bytes": os.path.getsize(src), "source": source,
            "language": language, "duration": info["duration"], "width": info["width"],
            "height": info["height"], "words": words}
    if engine == "from":
        data["timing"] = "estimated"
    fixes = os.path.join(folder, "fixes.json")
    if old and os.path.exists(fixes) and [w.get("w") for w in old.get("words", [])] != [w["w"] for w in words]:
        os.replace(fixes, os.path.join(folder, "fixes.old.json"))
        print("  the transcript changed, so its proofreading must be redone: fixes.json moved to fixes.old.json")
    write_outputs(folder, data)
    low = sum(1 for w in words if w.get("p", 1) < LOW_CONFIDENCE)
    print(f"{rel(src)}: {len(words)} words via {source}, language {language or '?'}"
          f"{f', {low} unsure words' if low else ''} -> {rel(folder)}/transcript.txt")
    if not language:
        print("  no language set and none detected, so English is assumed. If it isn't English, set "
              "\"language\" in the job (es, de, pt-BR...) and run this again with --force")
    if language and lang and base_lang(detected or lang) != base_lang(lang):
        print(f"  note: the engine heard {detected}; you set {lang}")


def main():
    ap = argparse.ArgumentParser(description="Transcribe videos with word times.")
    ap.add_argument("job", help="job.json, or one video file")
    ap.add_argument("--out", help="output folder when transcribing one video (default work/<name>)")
    ap.add_argument("--engine", choices=["auto", "from", "local", "mlx", "groq", "deepgram", "openai"], default="auto")
    ap.add_argument("--model", default="small", help="local/mlx model: tiny, base, small, medium, turbo, large-v3")
    ap.add_argument("--language", help="spoken language code (en, es, pt...). Default: the job's, else detected")
    ap.add_argument("--subs", help="one video: its .srt or .vtt subtitles")
    ap.add_argument("--only", help="comma-separated video ids from the job")
    ap.add_argument("--force", action="store_true", help="transcribe again even if done")
    a = ap.parse_args()
    need_ffmpeg()
    if a.job.lower().endswith((".mp4", ".mov", ".m4v", ".webm", ".mkv", ".avi", ".mp3", ".wav", ".m4a")):
        stem = os.path.splitext(os.path.basename(a.job))[0]
        subs = a.subs or next((os.path.splitext(a.job)[0] + e for e in (".srt", ".vtt")
                               if os.path.exists(os.path.splitext(a.job)[0] + e)), None)
        eng = pick_engine(a.engine, bool(subs))
        if eng == "from" and not subs:
            die("--engine from needs --subs captions.srt")
        transcribe_one(a.job, a.out or os.path.join("work", stem), eng, a.model, a.language, [], subs, a.force)
        return
    job = load_job(a.job)
    vocab = [str(x) for x in job.get("vocab", []) if str(x).strip()]
    lang = a.language or job.get("language")
    for v in selected(job, a.only):
        subs = v.get("subtitles")
        if subs:
            subs = os.path.normpath(os.path.join(job["_base"], subs))
        else:
            subs = next((os.path.splitext(v["file"])[0] + e for e in (".srt", ".vtt")
                         if os.path.exists(os.path.splitext(v["file"])[0] + e)), None)
        eng = pick_engine(a.engine, bool(subs))
        if eng == "from" and not subs:
            die(f"{v['id']}: --engine from needs a 'subtitles' file in the job")
        transcribe_one(v["file"], video_dir(job, v), eng, a.model, v.get("language") or lang, vocab, subs, a.force)


if __name__ == "__main__":
    guard(main)
