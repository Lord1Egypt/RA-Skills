#!/usr/bin/env python3
"""Voices for dubbing: which voice speaks which language, downloads, and speech synthesis.

    python3 scripts/voices.py list                 every language and its voices
    python3 scripts/voices.py list es              the voices for one language
    python3 scripts/voices.py sample dub.json es   each voice for that language says the first
                                                   translated line; listen and pick one
    python3 scripts/voices.py say es kokoro:em_alex "Hola" -o hola.wav

Engines:
  kokoro      free, on this computer (pip install kokoro-onnx soundfile). English, Spanish,
              French, Italian, Portuguese (Brazil), Hindi. Model files download once (~120 MB).
  piper       free, on this computer (pip install piper-tts). German, Dutch, Polish, Russian,
              Ukrainian, Czech, Danish, Finnish, Hungarian, Romanian, Greek, Persian, Norwegian,
              Swedish, Vietnamese. Each voice downloads once (~60-120 MB). Only voices whose
              licence allows commercial use are listed.
  elevenlabs  the user's own ElevenLabs key (ELEVENLABS_API_KEY) and voice ID: any language
              ElevenLabs speaks (Japanese, Chinese, Korean, Turkish, Arabic, Indonesian...), and
              the user's own cloned voice. Text is sent to ElevenLabs and uses the user's credits.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile, wave

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aclib import base_lang, cache_dir, die, guard, load_job, read_json, rel, video_dir  # noqa: E402

KOKORO_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/"
KOKORO_FILES = {"kokoro-v1.0.int8.onnx": 80_000_000, "voices-v1.0.bin": 20_000_000}
PIPER_URL = "https://huggingface.co/rhasspy/piper-voices/resolve/main/"

# language -> (engine's language code, [(voice, label)]). Kokoro: Apache-2.0 model weights.
KOKORO = {
    "en": ("en-us", [("af_heart", "woman, US"), ("am_michael", "man, US"), ("af_bella", "woman, US"),
                     ("am_fenrir", "man, US")]),
    "en-GB": ("en-gb", [("bf_emma", "woman, UK"), ("bm_george", "man, UK")]),
    "es": ("es", [("ef_dora", "woman"), ("em_alex", "man")]),
    "fr": ("fr-fr", [("ff_siwis", "woman")]),
    "it": ("it", [("if_sara", "woman"), ("im_nicola", "man")]),
    "pt": ("pt-br", [("pf_dora", "woman, Brazil"), ("pm_alex", "man, Brazil")]),
    "hi": ("hi", [("hf_alpha", "woman"), ("hm_omega", "man")]),
}
# language -> [(voice, label, licence)]. Licences from each voice's MODEL_CARD; non-commercial,
# share-alike and unknown-licence voices are left out on purpose.
PIPER = {
    "de": [("de_DE-thorsten-high", "man", "CC0"), ("de_DE-kerstin-medium", "woman", "CC0")],
    "nl": [("nl_NL-pim-medium", "man, Netherlands", "CC0"), ("nl_NL-ronnie-medium", "man, Netherlands", "CC0"),
           ("nl_BE-nathalie-medium", "woman, Belgium", "CC0")],
    "pl": [("pl_PL-gosia-medium", "woman", "CC0"), ("pl_PL-darkman-medium", "man", "CC0")],
    "ru": [("ru_RU-denis-medium", "man", "CC0"), ("ru_RU-dmitri-medium", "man", "CC0")],
    "uk": [("uk_UA-tetiana-high", "woman", "Apache-2.0"), ("uk_UA-mykyta-high", "man", "Apache-2.0")],
    "cs": [("cs_CZ-jirka-medium", "man", "CC0")],
    "da": [("da_DK-talesyntese-medium", "man", "CC0")],
    "fi": [("fi_FI-harri-medium", "man", "CC0")],
    "hu": [("hu_HU-anna-medium", "woman", "CC0"), ("hu_HU-imre-medium", "man", "CC0")],
    "ro": [("ro_RO-mihai-medium", "man", "CC0")],
    "el": [("el_GR-rapunzelina-medium", "woman", "CC0")],
    "fa": [("fa_IR-amir-medium", "man", "CC0"), ("fa_IR-ganji-medium", "man", "CC0")],
    "no": [("no_NO-talesyntese-medium", "man", "CC0")],
    "sv": [("sv_SE-nst-medium", "man", "CC0")],
    "vi": [("vi_VN-vais1000-medium", "woman", "CC BY 4.0: credit \"VAIS-1000 dataset\" in the post or description")],
}
NAMES = {"en": "English", "en-GB": "English (UK)", "es": "Spanish", "fr": "French", "it": "Italian",
         "pt": "Portuguese (Brazil)", "hi": "Hindi", "de": "German", "nl": "Dutch", "pl": "Polish",
         "ru": "Russian", "uk": "Ukrainian", "cs": "Czech", "da": "Danish", "fi": "Finnish", "hu": "Hungarian",
         "ro": "Romanian", "el": "Greek", "fa": "Persian", "no": "Norwegian", "sv": "Swedish", "vi": "Vietnamese"}
OWN_KEY_ONLY = "Japanese, Chinese, Korean, Turkish, Arabic, Indonesian and every other language ElevenLabs speaks"
ELEVEN_MODELS = {"eleven_multilingual_v2", "eleven_flash_v2_5", "eleven_turbo_v2_5", "eleven_v3"}
ELEVEN_LANG_ENFORCE = {"eleven_flash_v2_5", "eleven_turbo_v2_5"}
SR = 24000  # every voice is resampled to this for fitting; the mix is 48 kHz


def norm_lang(lang):
    """The catalogue key for a language code: en-GB stays, pt-BR -> pt, es-MX -> es."""
    if lang in KOKORO or lang in PIPER:
        return lang
    if lang.lower() in ("en-gb", "en-uk"):
        return "en-GB"
    return base_lang(lang)


def local_voices(lang):
    """[(spec, label, licence)] for a language, best first."""
    k = norm_lang(lang)
    out = []
    if k in KOKORO:
        out += [(f"kokoro:{v}", lab, "Apache-2.0 (Kokoro-82M)") for v, lab in KOKORO[k][1]]
    if k in PIPER:
        out += [(f"piper:{v}", lab, lic) for v, lab, lic in PIPER[k]]
    return out


def default_voice(lang):
    v = local_voices(lang)
    return v[0][0] if v else None


def parse(spec):
    eng, _, name = spec.partition(":")
    if eng not in ("kokoro", "piper", "elevenlabs") or not name:
        die(f"voice {spec!r}: write it as kokoro:<voice>, piper:<voice> or elevenlabs:<voice ID>")
    return eng, name


def check_voice(spec, lang):
    """Die with a clear message when a voice can't speak this language (local engines only)."""
    eng, name = parse(spec)
    k = norm_lang(lang)
    if eng == "kokoro":
        if k not in KOKORO:
            die(f"Kokoro doesn't speak {lang}. " + hint(lang))
        if name not in {v for v, _ in KOKORO[k][1]}:
            die(f"kokoro:{name} is not a {NAMES.get(k, lang)} voice. Choose from: "
                + ", ".join(f"kokoro:{v} ({lab})" for v, lab in KOKORO[k][1]))
    elif eng == "piper":
        if k not in PIPER or name not in {v for v, _, _ in PIPER[k]}:
            ok = PIPER.get(k)
            die(f"piper:{name} is not a listed {NAMES.get(k, lang)} voice. "
                + ("Choose from: " + ", ".join(f"piper:{v} ({lab})" for v, lab, _ in ok) if ok else hint(lang))
                + " (only voices whose licence allows commercial use are listed)")


def hint(lang):
    loc = local_voices(lang)
    if loc:
        return "Free voices for it: " + ", ".join(s for s, _, _ in loc)
    return (f"No free local voice speaks {lang} well enough to post. Use the user's own ElevenLabs key: "
            f"\"voices\": {{\"{lang}\": \"elevenlabs:<voice ID>\"}} with ELEVENLABS_API_KEY set.")


# ---------- downloads ----------

def fetch(url, path, min_bytes):
    """Download once into the cache. urllib first, then curl (some Python installs lack certificates)."""
    if os.path.exists(path) and os.path.getsize(path) >= min_bytes:
        return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    part = path + ".part"
    print(f"  downloading {os.path.basename(path)} (once)...", flush=True)
    done = False
    try:
        import urllib.request
        urllib.request.urlretrieve(url, part)
        done = os.path.getsize(part) >= min_bytes
    except Exception:
        done = False
    if not done and shutil.which("curl"):
        subprocess.run(["curl", "-sfL", "--retry", "3", url, "-o", part], check=False)
        done = os.path.exists(part) and os.path.getsize(part) >= min_bytes
    if not done:
        try:
            os.remove(part)
        except OSError:
            pass
        die(f"couldn't download {url}. Check the internet connection and run again (downloads go to "
            f"{os.path.dirname(path)}).")
    os.replace(part, path)
    return path


def kokoro_files():
    d = cache_dir("voices")
    return [fetch(KOKORO_URL + f, os.path.join(d, f), n) for f, n in KOKORO_FILES.items()]


def piper_files(name):
    m = re.match(r"^([a-z]{2,3})_([A-Z]{2})-(.+)-(x_low|low|medium|high)$", name)
    if not m:
        die(f"piper voice {name!r} looks wrong; see voices.py list")
    fam, reg, spk, q = m.groups()
    d = os.path.join(cache_dir("voices"), "piper")
    base = f"{PIPER_URL}{fam}/{fam}_{reg}/{spk}/{q}/{name}"
    onnx = fetch(base + ".onnx", os.path.join(d, name + ".onnx"), 5_000_000)
    fetch(base + ".onnx.json", os.path.join(d, name + ".onnx.json"), 500)
    return onnx


# ---------- synthesis ----------

_KOKORO = None


def to_wav(src, dst, speed=1.0):
    """Any audio -> mono 24 kHz 16-bit WAV, optionally sped up (atempo keeps the pitch)."""
    af = f"atempo={speed:.4f}," if abs(speed - 1) > 0.004 else ""
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-af", f"{af}aresample={SR}", "-ac", "1",
                        "-sample_fmt", "s16", dst], capture_output=True, text=True)
    if r.returncode != 0:
        die("ffmpeg couldn't read the voice audio: " + r.stderr.strip()[-300:])


def trim_silence(path):
    """Cut leading and trailing silence so lines start on time."""
    tmp = path + ".t.wav"
    f = ("silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.02,"
         "areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.06,areverse")
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", path, "-af", f, tmp], capture_output=True)
    if r.returncode == 0 and os.path.exists(tmp) and seconds(tmp) > 0.1:
        os.replace(tmp, path)
    elif os.path.exists(tmp):
        os.remove(tmp)


def seconds(path):
    with wave.open(path) as w:
        return w.getnframes() / float(w.getframerate())


def synth(spec, lang, text, out, speed=1.0, model=None, context=None):
    """Speak `text` into `out` (mono 24 kHz WAV). speed > 1 is faster. Returns the engine used."""
    eng, name = parse(spec)
    tmp = tempfile.mkdtemp()
    try:
        raw = os.path.join(tmp, "raw.wav")
        native = True
        if eng == "kokoro":
            global _KOKORO
            try:
                import soundfile as sf
                from kokoro_onnx import Kokoro
            except ImportError:
                die("the free voices need: pip install kokoro-onnx soundfile")
            if _KOKORO is None:
                onnx, bin_ = kokoro_files()
                _KOKORO = Kokoro(onnx, bin_)
            code = KOKORO[norm_lang(lang)][0]
            samples, sr = _KOKORO.create(text, voice=name, speed=max(0.5, min(2.0, speed)), lang=code)
            sf.write(raw, samples, sr)
        elif eng == "piper":
            onnx = piper_files(name)
            try:
                import piper  # noqa: F401
            except ImportError:
                die("this voice needs: pip install piper-tts")
            r = subprocess.run([sys.executable, "-m", "piper", "-m", onnx, "-f", raw,
                                "--length-scale", f"{1 / max(0.5, min(2.0, speed)):.4f}"],
                               input=text, capture_output=True, text=True, encoding="utf-8")
            if r.returncode != 0 or not os.path.exists(raw):
                die("piper failed: " + (r.stderr or r.stdout).strip()[-400:])
        else:
            raw = os.path.join(tmp, "raw.mp3")
            eleven(name, lang, text, raw, speed, model, context)
            native = 0.7 <= speed <= 1.2
        to_wav(raw, out, 1.0 if native else speed)
        trim_silence(out)
        return eng
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def eleven(voice_id, lang, text, out, speed, model, context):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        die("this voice uses ElevenLabs: set ELEVENLABS_API_KEY (the user's own key) and run again")
    model = model or "eleven_multilingual_v2"
    if model not in ELEVEN_MODELS:
        die(f"dub.model {model!r}: use one of {', '.join(sorted(ELEVEN_MODELS))}")
    body = {"text": text, "model_id": model,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75,
                               "speed": round(max(0.7, min(1.2, speed)), 3)}}
    if model in ELEVEN_LANG_ENFORCE:
        body["language_code"] = base_lang(lang)
    if context and model != "eleven_v3":
        body.update({k: v for k, v in context.items() if v})
    url = (f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128")
    data = json.dumps(body).encode("utf-8")
    import urllib.request, urllib.error
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"xi-api-key": key, "Content-Type": "application/json",
                                          "Accept": "audio/mpeg"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            audio = r.read()
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", "replace")[:300]
        die(f"ElevenLabs said {e.code}: {msg}")
    except Exception:
        if not shutil.which("curl"):
            raise
        hdr = os.path.join(os.path.dirname(out), "h.txt")
        with open(hdr, "w") as fh:  # the key goes in a file, not the command line
            fh.write(f"xi-api-key: {key}\nContent-Type: application/json\nAccept: audio/mpeg\n")
        r = subprocess.run(["curl", "-sS", "-X", "POST", url, "-H", f"@{hdr}", "--data-binary", "@-",
                            "-o", out, "-w", "%{http_code}"], input=data, capture_output=True)
        os.remove(hdr)
        code = r.stdout.decode().strip()
        if code != "200":
            msg = open(out, "rb").read()[:300].decode("utf-8", "replace") if os.path.exists(out) else ""
            die(f"ElevenLabs said {code}: {msg}")
        return
    with open(out, "wb") as fh:
        fh.write(audio)


def cache_key(spec, lang, text, speed, model):
    return hashlib.sha1(json.dumps([spec, lang, text, round(speed, 3), model or ""]).encode()).hexdigest()[:16]


# ---------- command line ----------

def cmd_list(lang):
    langs = [lang] if lang else list(NAMES)
    for k in langs:
        vs = local_voices(k)
        if not vs:
            print(f"{k}: no free voice. " + hint(k))
            continue
        print(f"{NAMES.get(norm_lang(k), k)} ({k}):")
        for s, lab, lic in vs:
            print(f"  {s:34} {lab}  [{lic}]")
    if not lang:
        print(f"\nOwn ElevenLabs key: {OWN_KEY_ONLY}, and the user's own cloned voice (elevenlabs:<voice ID>).")


def cmd_sample(job_path, lang):
    job = load_job(job_path)
    v = job["videos"][0]
    path = os.path.join(video_dir(job, v), f"cues.{lang}.json")
    if not os.path.exists(path):
        die(f"no {lang} translation yet ({rel(path)}); fill work/{v['id']}/translate.{lang}.json and run captions.py")
    cues = read_json(path)["cues"]
    text = " ".join(c["text"] for c in cues[:3]).strip()
    specs = [s for s, _, _ in local_voices(lang)]
    if job["voices"].get(lang) and job["voices"][lang] not in specs:
        specs.insert(0, job["voices"][lang])
    if not specs:
        die(hint(lang))
    folder = os.path.join(job["out"], "voice-samples")
    os.makedirs(folder, exist_ok=True)
    for s in specs:
        if s.startswith("elevenlabs:"):
            print(f"  {s}: skipped (uses the user's ElevenLabs credits; it is made by dub.py)")
            continue
        out = os.path.join(folder, f"{lang}.{s.replace(':', '-')}.wav")
        synth(s, lang, text, out)
        print(f"  {s}: {rel(out)}")
    print(f"Listen and pick one; put it in the job file as \"voices\": {{\"{lang}\": \"<voice>\"}}")


def main():
    ap = argparse.ArgumentParser(description="Dubbing voices: list, sample and say.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list")
    p.add_argument("lang", nargs="?")
    p = sub.add_parser("sample")
    p.add_argument("job")
    p.add_argument("lang")
    p = sub.add_parser("say")
    p.add_argument("lang")
    p.add_argument("voice")
    p.add_argument("text")
    p.add_argument("-o", "--out", required=True)
    p.add_argument("--speed", type=float, default=1.0)
    a = ap.parse_args()
    if a.cmd == "list":
        cmd_list(a.lang)
    elif a.cmd == "sample":
        cmd_sample(a.job, a.lang)
    else:
        check_voice(a.voice, a.lang)
        synth(a.voice, a.lang, a.text, a.out, a.speed)
        print(f"{rel(a.out)}: {seconds(a.out):.2f} s")


if __name__ == "__main__":
    guard(main)
