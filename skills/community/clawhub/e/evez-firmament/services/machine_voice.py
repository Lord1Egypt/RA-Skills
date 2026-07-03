#!/usr/bin/env python3
"""EVEZ-OS Machine Voice — 5-stage voice transformation on port 9113."""

import json
import math
import time
import struct
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

SPINE_URL = "http://localhost:9116/append"
SR = 44100

def spine_log(domain, action, data):
    try:
        requests.post(SPINE_URL, json={"domain": domain, "action": action, "data": data, "timestamp": time.time()}, timeout=2)
    except Exception:
        pass

# ── Audio Helpers ────────────────────────────────────────────────────

def generate_voice_like(duration=2.0, sr=SR):
    """Generate a synthetic 'human voice' — vowel-like formants."""
    n = int(sr * duration)
    out = [0.0] * n
    # Fundamental frequency (male-ish voice)
    f0 = 120
    # Vowel formants (ah)
    formants = [(700, 0.6), (1200, 0.3), (2500, 0.15)]
    for i in range(n):
        t = i / sr
        sample = 0.0
        # Glottal pulse train (sawtooth-ish)
        phase = (f0 * t) % 1.0
        pulse = 2.0 * phase - 1.0
        # Add vibrato
        vibrato = 1.0 + 0.02 * math.sin(2 * math.pi * 5.5 * t)
        for f, amp in formants:
            sample += amp * math.sin(2 * math.pi * f * vibrato * t)
        # Mix glottal source with formant filtering
        out[i] = 0.5 * pulse + 0.5 * sample
        # Amplitude modulation for naturalness
        out[i] *= (0.8 + 0.2 * math.sin(2 * math.pi * 0.3 * t))
    return _normalize(out)

def _normalize(samples):
    mx = max(abs(s) for s in samples) or 1.0
    return [s / mx for s in samples]

def _quantize(samples, bit_depth):
    """Bit-translation: quantize to specified bit depth."""
    levels = 2 ** bit_depth
    step = 2.0 / levels
    return [max(-1.0, min(1.0, round(s / step) * step)) for s in samples]

def _ring_mod(samples, freq, sr=SR):
    """Ring modulation with carrier frequency."""
    return [s * math.sin(2 * math.pi * freq * i / sr) for i, s in enumerate(samples)]

def _formant_morph(samples, shift, sr=SR):
    """Simple formant shifting via resampling."""
    if shift == 0:
        return samples
    # Resample to shift formants
    ratio = 2.0 ** (shift / 12.0)
    n = len(samples)
    new_len = int(n / ratio)
    out = [0.0] * new_len
    for i in range(new_len):
        src = i * ratio
        idx = int(src)
        frac = src - idx
        if idx + 1 < n:
            out[i] = samples[idx] * (1 - frac) + samples[idx + 1] * frac
        elif idx < n:
            out[i] = samples[idx]
    # Pad back to original length
    while len(out) < n:
        out.append(0.0)
    return out[:n]

def _pitch_shift(samples, semitones, sr=SR):
    """Simple pitch shift via resampling."""
    ratio = 2.0 ** (semitones / 12.0)
    n = len(samples)
    out = [0.0] * n
    for i in range(n):
        src = i * ratio
        idx = int(src)
        frac = src - idx
        if idx + 1 < n:
            out[i] = samples[idx] * (1 - frac) + samples[idx + 1] * frac
        elif idx < n:
            out[i] = samples[idx]
    return out

def samples_to_wav_bytes(samples, sr=SR):
    buf = bytearray()
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

# ── 5-Stage Pipeline ────────────────────────────────────────────────

STAGE_NAMES = {
    1: "Human voice input",
    2: "Bit-translation (quantize)",
    3: "Ring modulation",
    4: "Formant morphing",
    5: "Cognitive engine voice (final)",
}

# Per-session state
sessions = {}
_lock = threading.Lock()
_session_counter = [0]

def new_session():
    with _lock:
        _session_counter[0] += 1
        sid = _session_counter[0]
    sessions[sid] = {
        "current_stage": 1,
        "params": {"pitch_shift": 0, "formant_shift": 0, "bit_depth": 16, "ring_freq": 30},
        "audio": generate_voice_like(),
        "history": [],
    }
    return sid

def get_session(sid):
    return sessions.get(sid)

def transform_stage(sid, stage, params):
    s = sessions[sid]
    s["params"].update(params)
    audio = s["audio"]

    if stage == 1:
        # Stage 1 is just the input — regenerate with pitch shift
        audio = generate_voice_like()
        if s["params"]["pitch_shift"] != 0:
            audio = _pitch_shift(audio, s["params"]["pitch_shift"])
    elif stage == 2:
        # Bit-translation
        bd = max(1, min(32, s["params"]["bit_depth"]))
        audio = _quantize(audio, bd)
    elif stage == 3:
        # Ring modulation
        rf = s["params"]["ring_freq"]
        audio = _ring_mod(audio, rf)
    elif stage == 4:
        # Formant morphing
        fs = s["params"]["formant_shift"]
        audio = _formant_morph(audio, fs)
    elif stage == 5:
        # Final: apply all stages in sequence for the cognitive engine voice
        bd = max(1, min(32, s["params"]["bit_depth"]))
        audio = _quantize(audio, bd)
        audio = _ring_mod(audio, s["params"]["ring_freq"])
        audio = _formant_morph(audio, s["params"]["formant_shift"])
        # Add mechanical resonance
        n = len(audio)
        for i in range(n):
            t = i / SR
            audio[i] = audio[i] * 0.7 + 0.3 * math.sin(2 * math.pi * 180 * t) * math.sin(2 * math.pi * 3.7 * t)
        audio = _normalize(audio)

    s["audio"] = audio
    s["current_stage"] = stage
    s["history"].append({"stage": stage, "name": STAGE_NAMES[stage], "timestamp": time.time()})
    return audio

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

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"status": "alive", "service": "machine_voice", "port": 9113})
        elif self.path == "/stages":
            self._json(200, {"stages": {str(k): v for k, v in STAGE_NAMES.items()}})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/health":
            self._json(200, {"status": "alive", "service": "machine_voice", "port": 9113})
            return

        body = self._read_body()
        if self.path == "/session":
            sid = new_session()
            spine_log("machine_voice", "session", {"session_id": sid})
            self._json(200, {"session_id": sid, "stages": STAGE_NAMES})
        elif self.path == "/transform":
            sid = body.get("session_id", 1)
            stage = body.get("stage", 1)
            if sid not in sessions:
                sid = new_session()
            params = {
                "pitch_shift":   body.get("pitch_shift", 0),
                "formant_shift": body.get("formant_shift", 0),
                "bit_depth":     body.get("bit_depth", 8),
                "ring_freq":     body.get("ring_freq", 30),
            }
            audio = transform_stage(sid, stage, params)
            spine_log("machine_voice", f"transform_stage_{stage}", {"session_id": sid})
            self._wav(audio)
        else:
            self._json(404, {"error": "not found"})

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 9113), Handler)
    print("Machine Voice running on :9113")
    server.serve_forever()
