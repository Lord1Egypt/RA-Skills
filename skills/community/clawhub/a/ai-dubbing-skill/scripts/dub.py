#!/usr/bin/env python3
"""Make the dubbed audio for every video and translated language.

    python3 scripts/dub.py dub.json                 every video, every finished translation
    python3 scripts/dub.py dub.json --only intro --lang es
    python3 scripts/dub.py dub.json --force         keep lines that are too long (sped up and cut)

Reads work/<id>/cues.<lang>.json (written by captions.py from the filled translate.<lang>.json),
groups the cues into spoken lines, speaks each line with the language's voice, fits it into the
time the speaker took in the original, and mixes it over the original sound. Writes:

  work/<id>/dub.<lang>.wav     the finished soundtrack (48 kHz stereo), used by render.py
  work/<id>/voice.<lang>.wav   the dubbed voice alone
  work/<id>/dub.<lang>.json    every line: its time, how much it was sped up, and anything too long

A line that doesn't fit even at the job's max_speed is listed with how much shorter it must be;
nothing is mixed until those lines are shortened in translate.<lang>.json (and captions.py runs
again), unless --force. Lines already spoken are cached, so a rerun only redoes what changed.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aclib import (base_lang, die, guard, load_job, need_ffmpeg, probe, read_json, rel, selected,  # noqa: E402
                   video_dir, warn, write_json, WARNINGS)
import voices  # noqa: E402

MIX_SR = 48000
END = re.compile(r"[.!?…。！？؟]['\")\]»”]*$")
DUB_VERSION = 2


def need_numpy():
    try:
        import numpy  # noqa: F401
        return numpy
    except ImportError:
        die("dub.py needs numpy: pip install numpy")


def lines_of(cues, duration, max_len=8.0):
    """Translated cues -> spoken lines: cues joined until a sentence ends, a pause, or ~8 s, so each
    line starts where the speaker started it and stays close to the captions."""
    out, cur = [], None
    for c in cues:
        t = (c.get("text") or "").strip()
        if not t:
            continue
        if cur and (c["start"] - cur["end"] < 0.35) and not END.search(cur["text"]) \
                and c["end"] - cur["start"] <= max_len:
            cur["text"] += " " + t
            cur["end"] = c["end"]
            cur["cues"].append(c["i"])
        else:
            cur = {"start": c["start"], "end": c["end"], "text": t, "cues": [c["i"]]}
            out.append(cur)
    for n, ln in enumerate(out):
        nxt = out[n + 1]["start"] if n + 1 < len(out) else duration
        ln["slot"] = round(max(0.3, nxt - ln["start"] - 0.06), 3)
        ln["n"] = n + 1
    return out


def speak(job, v, lang, spec, ln, prev, nxt, tmp_dir):
    """Speak one line so it fits its slot. Returns (wav path, seconds, speed, fits)."""
    folder = os.path.join(video_dir(job, v), "voice-cache", lang)
    os.makedirs(folder, exist_ok=True)
    model = job["dub"].get("model")
    ctx = {"previous_text": prev, "next_text": nxt} if spec.startswith("elevenlabs:") else None

    def at(speed):
        key = voices.cache_key(spec, lang, ln["text"], speed, model)
        path = os.path.join(folder, key + ".wav")
        if not os.path.exists(path):
            part = os.path.join(tmp_dir, key + ".wav")
            voices.synth(spec, lang, ln["text"], part, speed, model, ctx)
            shutil.move(part, path)
        return path, voices.seconds(path)

    path, d = at(1.0)
    span = ln["end"] - ln["start"]
    if d < 0.8 * span and d <= ln["slot"]:  # much shorter than the speaker took: a touch slower, never below 0.9x
        speed = round(max(0.9, d / (0.9 * span)), 3)
        if speed < 0.995:
            path, d = at(speed)
            return path, d, speed, d <= ln["slot"] + 0.02
    if d <= ln["slot"]:
        return path, d, 1.0, True
    need = d / ln["slot"]
    top = job["dub"]["max_speed"]
    speed = round(min(top, need * 1.03), 3)
    path, d2 = at(speed)
    if d2 <= ln["slot"]:
        return path, d2, speed, True
    if d2 / ln["slot"] <= 1.06 and speed < top:  # engines don't scale exactly; nudge once
        speed = round(min(top, speed * d2 / ln["slot"] * 1.02), 3)
        path, d2 = at(speed)
    return path, d2, speed, d2 <= ln["slot"] + 0.02


def decode(np, src, args, sr=MIX_SR, ch=2):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", src] + args + ["-ac", str(ch), "-ar", str(sr),
                       "-f", "s16le", "-"], capture_output=True)
    if r.returncode != 0:
        die(f"ffmpeg couldn't read {rel(src)}: {r.stderr.decode('utf-8', 'replace').strip()[-300:]}")
    a = np.frombuffer(r.stdout, np.int16).astype(np.float32) / 32768.0
    return a.reshape(-1, ch)


def write_wav(np, path, a, sr=MIX_SR):
    import wave
    pcm = (np.clip(a, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(a.shape[1])
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def envelope(np, n, spans, low, ramp=0.08):
    """Gain per sample: `low` inside the spans, 1 outside, with short ramps (no clicks)."""
    g = np.ones(n, np.float32)
    r = int(ramp * MIX_SR)
    for s, e in spans:
        a, b = max(0, int(s * MIX_SR)), min(n, int(e * MIX_SR))
        if b <= a:
            continue
        g[a:b] = low
        lo, hi = max(0, a - r), a
        if hi > lo:
            g[lo:hi] = np.minimum(g[lo:hi], np.linspace(1, low, hi - lo, dtype=np.float32))
        lo, hi = b, min(n, b + r)
        if hi > lo:
            g[lo:hi] = np.minimum(g[lo:hi], np.linspace(low, 1, hi - lo, dtype=np.float32))
    return g


def merge(spans, gap=0.6):
    out = []
    for s, e in sorted(spans):
        if out and s - out[-1][1] < gap:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out


def background(np, job, v, info, tmp):
    """The original sound without the voice (demucs), or None to duck the original instead."""
    mode = job["dub"]["background"]
    if mode != "separate":
        return None
    cached = os.path.join(video_dir(job, v), "background.wav")
    if os.path.exists(cached) and os.path.getmtime(cached) >= os.path.getmtime(v["file"]):
        return decode(np, cached, [])
    try:
        import demucs  # noqa: F401
    except ImportError:
        die("dub.background \"separate\" needs demucs: pip install demucs (about 2 GB with PyTorch). "
            "Or use \"voiceover\" (the original sound, turned down under the new voice).")
    src = os.path.join(tmp, "orig.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", v["file"], "-map", f"0:a:{info['audio_index']}",
                    "-ac", "2", "-ar", "44100", src], check=True)
    print(f"  {v['id']}: separating the voice from the background (demucs; about the video's length "
          "or longer on a laptop)...", flush=True)
    r = subprocess.run([sys.executable, "-m", "demucs", "--two-stems=vocals", "-n", "htdemucs", "-o", tmp, src],
                       capture_output=True, text=True)
    stem = os.path.join(tmp, "htdemucs", "orig", "no_vocals.wav")
    if r.returncode != 0 or not os.path.exists(stem):
        die("demucs failed: " + (r.stderr or r.stdout).strip()[-400:])
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", stem, "-ar", str(MIX_SR), cached], check=True)
    return decode(np, cached, [])


def dub_one(job, v, lang, src_lang, force, confirm_cost):
    np = need_numpy()
    folder = video_dir(job, v)
    cpath = os.path.join(folder, f"cues.{lang}.json")
    if not os.path.exists(cpath):
        print(f"  {v['id']}/{lang}: no translation yet; fill {rel(os.path.join(folder, f'translate.{lang}.json'))} "
              "and run captions.py")
        return "todo"
    spec = job["voices"].get(lang) or voices.default_voice(lang)
    if not spec:
        die(f"{v['id']}/{lang}: " + voices.hint(lang))
    voices.check_voice(spec, lang)
    info = probe(v["file"])
    duration = info["duration"]
    cues = read_json(cpath)["cues"]
    lines = lines_of(cues, duration)
    if not lines:
        warn(f"{v['id']}/{lang}: the translation is empty; nothing to dub")
        return "empty"
    if spec.startswith("elevenlabs:") and not confirm_cost:
        chars = sum(len(ln["text"]) for ln in lines)
        print(f"  {v['id']}/{lang}: {len(lines)} lines, {chars} characters for ElevenLabs (plus re-tries for lines "
              "that must be faster). That uses the user's ElevenLabs credits. Ask, then run with --confirm-cost.")
        return "cost"
    sig = json.dumps([DUB_VERSION, spec, job["dub"], [(ln["text"], ln["start"], ln["slot"]) for ln in lines],
                      os.path.getsize(v["file"]), round(os.path.getmtime(v["file"]))], sort_keys=True)
    out = os.path.join(folder, f"dub.{lang}.wav")
    report_path = os.path.join(folder, f"dub.{lang}.json")
    if os.path.exists(out) and os.path.exists(report_path):
        old = read_json(report_path)
        if old.get("signature") == sig and not old.get("too_long"):
            print(f"  {v['id']}/{lang}: up to date ({rel(out)})")
            return "ok"
    tmp = tempfile.mkdtemp()
    try:
        print(f"  {v['id']}/{lang}: speaking {len(lines)} lines with {spec}...", flush=True)
        placed, long_ = [], []
        for n, ln in enumerate(lines):
            prev = lines[n - 1]["text"] if n else ""
            nxt = lines[n + 1]["text"] if n + 1 < len(lines) else ""
            path, d, speed, fits = speak(job, v, lang, spec, ln, prev, nxt, tmp)
            ln.update(seconds=round(d, 2), speed=speed, fits=fits)
            if not fits:
                cut = 1 - ln["slot"] / d
                ln["shorten_by"] = f"{max(10, int(round(cut * 100 / 5.0)) * 5)}%"
                long_.append(ln)
            placed.append((ln, path))
        report = {"video": v["id"], "language": lang, "voice": spec, "signature": sig,
                  "lines": [{k: ln[k] for k in ("n", "cues", "start", "slot", "seconds", "speed", "text")
                             if k in ln} for ln in lines],
                  "too_long": [{"cues": ln["cues"], "slot": ln["slot"], "seconds": ln["seconds"],
                                "shorten_by": ln["shorten_by"], "text": ln["text"]} for ln in long_]}
        if long_ and not force:
            write_json(report_path, report)
            if os.path.exists(out):  # never leave an older dub that render.py would use
                os.remove(out)
            print(f"  {v['id']}/{lang}: {len(long_)} line(s) don't fit even at {job['dub']['max_speed']}x speed:")
            for ln in long_:
                print(f"    cues {','.join(map(str, ln['cues']))} ({ln['slot']:.1f} s available, {ln['seconds']:.1f} s "
                      f"spoken): shorten by about {ln['shorten_by']}: \"{ln['text'][:90]}\"")
            print(f"    Shorten those cues' text in translate.{lang}.json (same meaning, fewer words), run "
                  "captions.py, then dub.py again.")
            return "long"
        n = int(round(duration * MIX_SR))
        voice = np.zeros((n, 2), np.float32)
        spans = []
        for ln, path in placed:
            a = decode(np, path, [])
            a = a[: max(0, int(ln["slot"] * MIX_SR))] if not ln["fits"] else a
            if not ln["fits"] and len(a) > 400:  # --force: fade the cut so it doesn't click
                fade = min(len(a), int(0.08 * MIX_SR))
                a[-fade:] *= np.linspace(1, 0, fade, dtype=np.float32)[:, None]
            s = int(ln["start"] * MIX_SR)
            e = min(n, s + len(a))
            if e > s:
                voice[s:e] += a[: e - s]
                spans.append((ln["start"], ln["start"] + (e - s) / MIX_SR))
        write_wav(np, os.path.join(folder, f"voice.{lang}.wav"), voice)
        mode = job["dub"]["background"]
        if mode == "none" or not info["audio"]:
            bed = np.zeros_like(voice)
        else:
            bed = background(np, job, v, info, tmp)
            if bed is None:  # voiceover: the original, turned down wherever anyone speaks
                bed = decode(np, v["file"], ["-map", f"0:a:{info['audio_index']}"])
                src_spans = [(c["start"] - 0.12, c["end"] + 0.15)
                             for c in read_json(os.path.join(folder, f"cues.{src_lang}.json"))["cues"]
                             if not c.get("sound")] if os.path.exists(os.path.join(folder, f"cues.{src_lang}.json")) else []
                gain = envelope(np, len(bed), merge(src_spans + spans), job["dub"]["original_volume"])
                bed = bed * gain[:, None]
            if len(bed) < n:
                bed = np.concatenate([bed, np.zeros((n - len(bed), 2), np.float32)])
            bed = bed[:n]
        mix = os.path.join(tmp, "mix.wav")
        write_wav(np, mix, bed + voice)
        r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", mix, "-af",
                            "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(MIX_SR), "-ac", "2", out],
                           capture_output=True, text=True)
        if r.returncode != 0:
            die("ffmpeg couldn't mix the dub: " + r.stderr.strip()[-300:])
        if long_:
            report["forced"] = True
        write_json(report_path, report)
        fast = [ln for ln in lines if ln["speed"] > 1.0]
        note = f"; {len(fast)} line(s) sped up (at most {max(ln['speed'] for ln in fast):.2f}x)" if fast else ""
        cut = f"; {len(long_)} line(s) cut short (--force)" if long_ else ""
        print(f"  {v['id']}/{lang}: {rel(out)}{note}{cut}")
        return "ok"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description="Make the dubbed soundtrack for each translated language.")
    ap.add_argument("job")
    ap.add_argument("--only", help="video id(s), comma-separated")
    ap.add_argument("--lang", help="language(s), comma-separated")
    ap.add_argument("--force", action="store_true", help="keep lines that don't fit (sped up to max_speed, then cut)")
    ap.add_argument("--confirm-cost", action="store_true",
                    help="the user said yes to the ElevenLabs characters this uses")
    a = ap.parse_args()
    job = load_job(a.job)
    need_ffmpeg()
    langs = a.lang.split(",") if a.lang else job["translations"]
    if not langs:
        die("the job has no 'translations': add the languages to dub, like [\"es\", \"pt-BR\"]")
    states = []
    for v in selected(job, a.only):
        src = None
        for f in os.listdir(video_dir(job, v)) if os.path.isdir(video_dir(job, v)) else []:
            m = re.match(r"^cues\.(.+)\.json$", f)
            if m and m.group(1) not in job["translations"]:
                src = m.group(1)
        if not src:
            die(f"{v['id']}: run transcribe.py and captions.py first")
        for lang in langs:
            if base_lang(lang) == base_lang(src):
                continue
            states.append(dub_one(job, v, lang, src, a.force, a.confirm_cost))
    for w in WARNINGS:
        print(f"warning: {w}", file=sys.stderr)
    if "long" in states:
        print("Some lines are too long: shorten them, run captions.py, then dub.py again.")
        sys.exit(2)
    if "cost" in states:
        sys.exit(3)
    if "ok" in states:
        print("Next: listen to work/<id>/dub.<lang>.wav, then render.py --preview and render.py.")


if __name__ == "__main__":
    guard(main)
