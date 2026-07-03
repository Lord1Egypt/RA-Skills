#!/usr/bin/env python3
"""EVEZ-OS DAW Agent — Pure-math audio synthesis on port 9112."""

import json
import math
import time
import struct
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

SPINE_URL = "http://localhost:9116/append"
SR = 44100  # sample rate

def spine_log(domain, action, data):
    try:
        requests.post(SPINE_URL, json={"domain": domain, "action": action, "data": data, "timestamp": time.time()}, timeout=2)
    except Exception:
        pass

# ── Pure Math Synthesis ─────────────────────────────────────────────

def generate_sine(freq, duration, sr=SR):
    n = int(sr * duration)
    return [math.sin(2 * math.pi * freq * i / sr) for i in range(n)]

def generate_noise(duration, sr=SR):
    import random
    n = int(sr * duration)
    return [random.uniform(-1, 1) for _ in range(n)]

def apply_adsr(samples, a=0.01, d=0.05, s=0.6, r=0.05, sr=SR):
    n = len(samples)
    out = [0.0] * n
    for i in range(n):
        t = i / sr
        if t < a:
            env = t / a
        elif t < a + d:
            env = 1.0 - (1.0 - s) * ((t - a) / d)
        elif t < (n / sr) - r:
            env = s
        else:
            env = s * max(0, ((n / sr) - t) / r)
        out[i] = samples[i] * env
    return out

def clip_and_norm(samples):
    mx = max(abs(s) for s in samples) or 1.0
    return [s / mx for s in samples]

def mix(*lists):
    maxlen = max(len(l) for l in lists)
    out = [0.0] * maxlen
    for l in lists:
        for i in range(len(l)):
            out[i] += l[i]
    mx = max(abs(s) for s in out) or 1.0
    return [s / mx for s in out]

def samples_to_wav_bytes(samples, sr=SR):
    buf = bytearray()
    # WAV header
    data_size = len(samples) * 2
    buf += b'RIFF'
    buf += struct.pack('<I', 36 + data_size)
    buf += b'WAVE'
    buf += b'fmt '
    buf += struct.pack('<IHHIIHH', 16, 1, 1, sr, sr * 2, 2, 16)
    buf += b'data'
    buf += struct.pack('<I', data_size)
    for s in samples:
        val = max(-32768, min(32767, int(s * 32767)))
        buf += struct.pack('<h', val)
    return bytes(buf)

# ── Synthesis Engines ──────────────────────────────────────────────

def synth_drums(bpm, style, duration_bars=4):
    beat = 60.0 / bpm
    total = int(SR * beat * duration_bars * 4)
    out = [0.0] * total

    # kick on 1 and 3
    for bar in range(duration_bars):
        for beat_idx in [0, 2]:
            pos = int(((bar * 4) + beat_idx) * beat * SR)
            kick = generate_sine(60, 0.15)
            kick = apply_adsr(kick, a=0.001, d=0.05, s=0.3, r=0.1)
            for i in range(min(len(kick), total - pos)):
                out[pos + i] += kick[i] * 0.8

    # snare on 2 and 4
    for bar in range(duration_bars):
        for beat_idx in [1, 3]:
            pos = int(((bar * 4) + beat_idx) * beat * SR)
            snare = generate_noise(0.1)
            snare = apply_adsr(snare, a=0.001, d=0.02, s=0.2, r=0.05)
            for i in range(min(len(snare), total - pos)):
                out[pos + i] += snare[i] * 0.5

    # hi-hat
    step = int(beat * SR / 2)
    if style == "breakcore":
        step = int(beat * SR / 4)  # faster hats
    for pos in range(0, total, step):
        hh = generate_noise(0.03)
        hh = apply_adsr(hh, a=0.001, d=0.005, s=0.1, r=0.01)
        for i in range(min(len(hh), total - pos)):
            out[pos + i] += hh[i] * 0.25

    return clip_and_norm(out)

def synth_bass(bpm, style, key_freq=55.0, duration_bars=4):
    beat = 60.0 / bpm
    total = int(SR * beat * duration_bars * 4)
    out = [0.0] * total

    note_len = int(beat * SR)
    if style == "dubstep":
        note_len = int(beat * 2 * SR)  # half-note wobble

    for bar in range(duration_bars):
        for beat_idx in range(4):
            pos = int(((bar * 4) + beat_idx) * beat * SR)
            if style == "dubstep":
                # wobble bass: FM synthesis
                mod_depth = 20 + 15 * math.sin(2 * math.pi * 3 * beat_idx / 4)
                bass = [math.sin(2 * math.pi * (key_freq + mod_depth * math.sin(2 * math.pi * 6 * i / SR)) * i / SR) for i in range(min(note_len, total - pos))]
            elif style == "phonk":
                # 808 slide — frequency drops over time
                note_len_clamped = min(note_len, total - pos)
                bass = [math.sin(2 * math.pi * key_freq * (1 + 0.5 * math.exp(-i / (SR * 0.3))) * i / SR) for i in range(note_len_clamped)]
            else:
                bass = generate_sine(key_freq, note_len / SR)
            bass = apply_adsr(bass, a=0.005, d=0.1, s=0.7, r=0.05)
            for i in range(len(bass)):
                if pos + i < total:
                    out[pos + i] += bass[i] * 0.6

    return clip_and_norm(out)

def synth_fx(bpm, style, duration_bars=4):
    beat = 60.0 / bpm
    total = int(SR * beat * duration_bars * 4)
    out = [0.0] * total

    if style == "breakcore":
        # glitch stutters
        import random
        for _ in range(duration_bars * 8):
            pos = random.randint(0, total - int(SR * 0.05))
            freq = random.uniform(800, 4000)
            fx = generate_sine(freq, 0.03)
            fx = apply_adsr(fx, a=0.001, d=0.005, s=0.2, r=0.01)
            for i in range(min(len(fx), total - pos)):
                out[pos + i] += fx[i] * 0.15

    elif style == "dubstep":
        # rising pitch sweep
        for i in range(total):
            t = i / SR
            freq = 200 + 3000 * (i / total)
            out[i] += math.sin(2 * math.pi * freq * t) * 0.1 * (i / total)

    return clip_and_norm(out)

def render_full(bpm, key, style, duration_bars=4):
    key_map = {"C": 32.7, "D": 36.7, "E": 41.2, "F": 43.7, "G": 49.0, "A": 55.0, "Bb": 58.3, "B": 61.7}
    key_freq = key_map.get(key, 55.0)

    drums = synth_drums(bpm, style, duration_bars)
    bass = synth_bass(bpm, style, key_freq, duration_bars)
    fx = synth_fx(bpm, style, duration_bars)

    # align lengths
    maxlen = max(len(drums), len(bass), len(fx))
    while len(drums) < maxlen: drums.append(0.0)
    while len(bass) < maxlen:  bass.append(0.0)
    while len(fx) < maxlen:   fx.append(0.0)

    mixed = mix(drums, [b * 0.7 for b in bass], [f * 0.4 for f in fx])
    return mixed

# ── Cache ───────────────────────────────────────────────────────────

cache = {"last_render": None, "last_params": None}

# ── HTTP Handler ─────────────────────────────────────────────────────

class Handler(BaseHTTPRequestHandler):
    def _json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _wav(self, samples):
        wav = samples_to_wav_bytes(samples)
        self.send_response(200)
        self.send_header("Content-Type", "audio/wav")
        self.send_header("Content-Length", str(len(wav)))
        self.end_headers()
        self.wfile.write(wav)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length:
            return json.loads(self.rfile.read(length))
        return {}

    def _params(self, body=None):
        body = body or {}
        return {
            "bpm":   body.get("bpm", 170),
            "key":   body.get("key", "A"),
            "style": body.get("style", "breakcore"),
        }

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"status": "alive", "service": "daw_agent", "port": 9112, "cost": "$0"})

    def do_POST(self):
        if self.path == "/health":
            self._json(200, {"status": "alive", "service": "daw_agent", "port": 9112, "cost": "$0"})
            return

        body = self._read_body()
        p = self._params(body)

        if p["style"] not in ("breakcore", "dubstep", "phonk", "404-architecture"):
            self._json(400, {"error": "invalid style", "valid": ["breakcore", "dubstep", "phonk", "404-architecture"]})
            return

        if self.path == "/drums":
            samples = synth_drums(p["bpm"], p["style"])
            spine_log("daw", "drums", p)
            self._wav(samples)
        elif self.path == "/bass":
            samples = synth_bass(p["bpm"], p["style"])
            spine_log("daw", "bass", p)
            self._wav(samples)
        elif self.path == "/fx":
            samples = synth_fx(p["bpm"], p["style"])
            spine_log("daw", "fx", p)
            self._wav(samples)
        elif self.path == "/render" or self.path == "/synthesize":
            samples = render_full(p["bpm"], p["key"], p["style"])
            cache["last_render"] = samples
            cache["last_params"] = p
            spine_log("daw", "render", p)
            self._wav(samples)
        else:
            self._json(404, {"error": "not found"})

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 9112), Handler)
    print("DAW Agent running on :9112")
    server.serve_forever()
