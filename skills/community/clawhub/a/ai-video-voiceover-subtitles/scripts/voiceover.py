#!/usr/bin/env python3
"""Script-to-voiceover preset layer on top of the official client (scripts/miragea_audio.py).

It only calls the client's real `generate` subcommand, once per script line, with
--format wav --wait --output; then joins the WAV files locally and writes SRT
subtitles plus a per-line timing manifest. Python 3.9+ standard library only.

  python3 scripts/voiceover.py check                       offline: Python version, API key present, API root
  python3 scripts/voiceover.py script FILE -o OUT_DIR       script -> OUT_DIR/voiceover.wav + voiceover.srt + manifest.json
  python3 scripts/voiceover.py script FILE -o OUT_DIR --dry-run   offline test: silent placeholder audio, no key, no API call

Everything else (capabilities, actors, recognize, task, wait) is done with
scripts/miragea_audio.py directly. Env: MIRAGEA_API_KEY, optional MIRAGEA_BASE_URL.
"""
import argparse
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import uuid
import wave

VERSION = "1.1.0"
HERE = os.path.dirname(os.path.abspath(__file__))
CLIENT = os.path.join(HERE, "miragea_audio.py")
DRY_RATE = 24000

# preset -> (seconds of silence between lines, max characters per subtitle cue, speaker labels in subtitles)
PRESETS = {
    "koubo": (0.15, 14, False), "jieshuo": (0.30, 16, False), "daihuo": (0.10, 12, False),
    "shuziren": (0.20, 16, False), "guanggao": (0.40, 14, False), "youshengshu": (0.50, 20, True),
}
LINE_RE = re.compile(r"^\s*\[(?P<who>[^\]]+)\]\s*[:：]?\s*(?P<text>.*)$")
PAUSE_RE = re.compile(r"^\s*\[(?:pause|停顿)\s*(?P<s>[\d.]+)\s*s?\]\s*$", re.I)
ALIASES = {"ref": "reference_audio_url", "ref_text": "reference_text", "actor": "actor_id"}


class ScriptError(Exception):
    pass


def parse_script(text):
    """Front matter defines speakers; body lines are `[speaker] text`, `[pause 0.6]` or untagged text."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    speakers, body = {}, text
    m = re.match(r"^\s*---\s*\n(.*?)\n---\s*\n", text, re.S)
    if m:
        body = text[m.end():]
        for raw in m.group(1).splitlines():
            if not raw.strip() or ":" not in raw:
                continue
            name, rest = raw.split(":", 1)
            v = {}
            for k, val in re.findall(r'(\w+)=("[^"]*"|\S+)', rest):
                k, val = ALIASES.get(k, k), val.strip('"')
                if k == "speed":
                    val = float(val)
                    if not 0.25 <= val <= 4:
                        raise ScriptError("speed must be 0.25-4 (speaker %s)" % name.strip())
                elif k == "tags":
                    val = [t for t in val.split(",") if t]
                elif k not in ("actor_id", "reference_audio_url", "reference_text", "model", "language"):
                    raise ScriptError("unknown speaker option %s= (speaker %s)" % (k, name.strip()))
                v[k] = val
            if v.get("actor_id") and v.get("reference_text"):
                raise ScriptError("ref_text only goes with ref= (speaker %s)" % name.strip())
            speakers[name.strip()] = v
    lines, current = [], next(iter(speakers), None)
    for raw in body.splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        pm = PAUSE_RE.match(s)
        if pm:
            lines.append({"pause": float(pm.group("s"))})
            continue
        lm = LINE_RE.match(s)
        if lm:
            current, s = lm.group("who").strip(), lm.group("text").strip()
            if not s:
                continue
        current = current or "narrator"
        speakers.setdefault(current, {})
        lines.append({"speaker": current, "text": s})
    if not any("text" in l for l in lines):
        raise ScriptError("script has no spoken lines")
    return speakers, lines


def ts(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def split_caption(text, limit):
    parts = [p for p in re.split(r"(?<=[。！？!?；;，,])\s*", text) if p.strip()]
    out, cur = [], ""
    for p in parts:
        if cur and len(cur) + len(p) > limit:
            out.append(cur.strip())
            cur = p
        else:
            cur += (" " if cur and re.match(r"[A-Za-z0-9]", p[:1]) else "") + p
    if cur.strip():
        out.append(cur.strip())
    return out or [text]


def silence(params, seconds):
    ch, sw, sr = params
    return b"\x00" * int(sr * max(seconds, 0)) * ch * sw


def placeholder(text):
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(DRY_RATE)
        w.writeframes(silence((1, 2, DRY_RATE), max(0.6, len(text) / 15.0)))
    return buf.getvalue()


def read_wav(data, where):
    try:
        with wave.open(io.BytesIO(data)) as w:
            return (w.getnchannels(), w.getsampwidth(), w.getframerate()), w.readframes(w.getnframes())
    except (wave.Error, EOFError) as e:
        raise ScriptError("%s is not a PCM WAV the standard library can join (%s). The per-line files are kept in "
                          "lines/; join them with an audio editor or ffmpeg instead." % (where, e))


def payload_for(text, voice, model):
    p = {"text": text, "format": "wav"}
    for k in ("actor_id", "reference_audio_url", "reference_text", "speed", "tags", "language"):
        if voice.get(k) not in (None, "", []):
            p[k] = voice[k]
    if voice.get("model") or model:
        p["model"] = voice.get("model") or model
    return p


def generate_line(p, out_path, key, wait_timeout):
    cmd = [sys.executable, CLIENT, "generate", "--text=" + p["text"], "--format", "wav", "--wait",
           "--wait-timeout", str(wait_timeout), "--output", out_path, "--idempotency-key", key]
    if p.get("actor_id"):
        cmd += ["--actor-id", str(p["actor_id"])]
    else:
        cmd += ["--reference-audio-url=" + p["reference_audio_url"]]
        if p.get("reference_text"):
            cmd += ["--reference-text=" + p["reference_text"]]
    for flag, k in (("--model", "model"), ("--speed", "speed"), ("--language", "language")):
        if p.get(k) is not None:
            cmd += [flag, str(p[k])]
    for t in p.get("tags", []):
        cmd += ["--tag=" + t]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(out_path):
        sys.stderr.write(r.stdout + r.stderr)
        raise ScriptError("generate failed for: %s... Re-run the same command to resume; the same idempotency key "
                          "returns the original task instead of creating a new one." % p["text"][:30])


def cmd_check(a):
    ok = sys.version_info >= (3, 9)
    print("python       %s  %s" % (sys.version.split()[0], "OK" if ok else "NEED 3.9+"))
    print("client       %s" % ("OK" if os.path.exists(CLIENT) else "MISSING scripts/miragea_audio.py"))
    default = re.search(r"MIRAGEA_BASE_URL', '([^']+)'", open(CLIENT, encoding="utf-8").read()) if os.path.exists(CLIENT) else None
    print("api root     %s" % (os.environ.get("MIRAGEA_BASE_URL") or (default.group(1) if default else "?")))
    key = bool(os.environ.get("MIRAGEA_API_KEY"))
    print("api key      %s" % ("set" if key else "NOT SET (use --dry-run meanwhile)"))
    print("next         python3 scripts/miragea_audio.py capabilities   # live modes, tags, limits")
    return 0 if ok and os.path.exists(CLIENT) else 1


def cmd_script(a):
    gap, max_chars, labels = PRESETS.get(a.preset, (0.25, 18, False))
    gap = gap if a.gap is None else a.gap
    max_chars = max_chars if a.max_chars is None else a.max_chars
    labels = labels or a.speaker_labels
    with open(a.file, encoding="utf-8") as f:
        speakers, lines = parse_script(f.read())
    if not a.dry_run:
        missing = [s for s, v in speakers.items() if not (v.get("actor_id") or v.get("reference_audio_url"))]
        if missing:
            raise ScriptError("speakers without a voice: %s. Add actor_id=... (from `miragea_audio.py actors`) or "
                              "ref=<reference audio URL> in the front matter." % ", ".join(missing))
        if not os.environ.get("MIRAGEA_API_KEY"):
            raise ScriptError("MIRAGEA_API_KEY is not set (or add --dry-run to test offline)")
    cache = os.path.join(a.output, "lines")
    os.makedirs(cache, exist_ok=True)
    salt = uuid.uuid4().hex if a.fresh else ""
    params, pcm, cues, manifest, t, lead = None, [], [], [], 0.0, 0.0
    for i, l in enumerate(lines):
        if "pause" in l:
            if params:
                pcm.append(silence(params, l["pause"]))
            else:
                lead += l["pause"]
            t += l["pause"]
            continue
        if a.dry_run:
            data, src = placeholder(l["text"]), None
        else:
            p = payload_for(l["text"], speakers[l["speaker"]], a.model)
            digest = hashlib.sha256((json.dumps(p, sort_keys=True, ensure_ascii=False) + salt).encode()).hexdigest()
            src = os.path.join(cache, digest[:24] + ".wav")
            if not os.path.exists(src):
                print("line %d/%d  %s" % (i + 1, len(lines), l["text"][:40]), file=sys.stderr)
                generate_line(p, src, "vo-" + digest[:40], a.wait_timeout)
            with open(src, "rb") as f:
                data = f.read()
        prm, frames = read_wav(data, src or "placeholder")
        if params and prm != params:
            raise ScriptError("line %d has a different WAV format %s vs %s" % (i + 1, prm, params))
        if params is None:
            params = prm
            if lead:
                pcm.append(silence(params, lead))
        dur = len(frames) / float(prm[0] * prm[1] * prm[2])
        pcm.append(frames)
        chunks = split_caption(l["text"], max_chars)
        total, start = sum(len(c) for c in chunks) or 1, t
        for c in chunks:
            d = dur * len(c) / total
            cues.append((start, start + d, ("%s: " % l["speaker"] if labels else "") + c))
            start += d
        manifest.append({"line": i + 1, "speaker": l["speaker"], "text": l["text"],
                         "start": round(t, 3), "end": round(t + dur, 3), "file": os.path.relpath(src, a.output) if src else None})
        t += dur
        if gap > 0 and i + 1 < len(lines) and "pause" not in lines[i + 1]:
            pcm.append(silence(params, gap))
            t += gap
    wav_path = os.path.join(a.output, "voiceover.wav")
    with wave.open(wav_path, "wb") as w:
        w.setnchannels(params[0])
        w.setsampwidth(params[1])
        w.setframerate(params[2])
        w.writeframes(b"".join(pcm))
    with open(os.path.join(a.output, "voiceover.srt"), "w", encoding="utf-8") as f:
        for n, (s, e, c) in enumerate(cues, 1):
            f.write("%d\n%s --> %s\n%s\n\n" % (n, ts(s), ts(e), c))
    with open(os.path.join(a.output, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"duration": round(t, 3), "dry_run": a.dry_run, "preset": a.preset, "lines": manifest},
                  f, ensure_ascii=False, indent=2)
    print("wrote %s (%.1fs, %d lines) + voiceover.srt + manifest.json%s"
          % (wav_path, t, len(manifest), "  [dry-run: silent placeholder audio]" if a.dry_run else ""))
    return 0


def build_parser():
    p = argparse.ArgumentParser(prog="voiceover.py", description="Script -> voiceover WAV + SRT, via scripts/miragea_audio.py generate")
    p.add_argument("--version", action="version", version=VERSION)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="offline environment check").set_defaults(fn=cmd_check)
    c = sub.add_parser("script", help="script file -> voiceover.wav + voiceover.srt + manifest.json")
    c.add_argument("file")
    c.add_argument("-o", "--output", default="voiceover_out")
    c.add_argument("--preset", choices=sorted(PRESETS), help="line gap / subtitle length preset")
    c.add_argument("--gap", type=float, default=None, help="seconds of silence between lines (default 0.25)")
    c.add_argument("--max-chars", type=int, default=None, help="max characters per subtitle cue (default 18)")
    c.add_argument("--speaker-labels", action="store_true", help="prefix subtitle cues with the speaker name")
    c.add_argument("--model", choices=("expressive", "standard"), help="default generation mode for speakers without model=")
    c.add_argument("--wait-timeout", type=float, default=600, help="seconds to wait per line")
    c.add_argument("--fresh", action="store_true", help="new takes instead of reusing earlier tasks")
    c.add_argument("--dry-run", action="store_true", help="offline: silent placeholder audio, no key, no API call")
    c.set_defaults(fn=cmd_script)
    return p


def main(argv=None):
    a = build_parser().parse_args(argv)
    try:
        return a.fn(a)
    except ScriptError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
