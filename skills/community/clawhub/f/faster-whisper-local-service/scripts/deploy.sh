#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
VOICE_DIR="$WORKSPACE/voice-input"
VENV="${VENV_PATH:-$WORKSPACE/.venv-faster-whisper}"
SERVICE_FILE="$HOME/.config/systemd/user/openclaw-transcribe.service"
PYTHON_BIN="${PYTHON_BIN:-python3}"
TRANSCRIBE_PORT="${TRANSCRIBE_PORT:-18790}"
MODEL_SIZE="${WHISPER_MODEL_SIZE:-medium}"
DEVICE="${WHISPER_DEVICE:-cpu}"
COMPUTE_TYPE="${WHISPER_COMPUTE_TYPE:-int8}"
ALLOWED_ORIGIN="${TRANSCRIBE_ALLOWED_ORIGIN:-https://127.0.0.1:8443}"
LANGUAGE="${WHISPER_LANGUAGE:-auto}"
FW_VERSION="${FASTER_WHISPER_VERSION:-1.1.1}"
MAX_UPLOAD_MB="${MAX_UPLOAD_MB:-50}"

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "missing dependency: $1" >&2
    exit 2
  }
}

need_cmd "$PYTHON_BIN"
need_cmd gst-launch-1.0

mkdir -p "$VOICE_DIR" "$HOME/.config/systemd/user"

if [[ ! -d "$VENV" ]]; then
  "$PYTHON_BIN" -m venv "$VENV"
fi

"$VENV/bin/pip" install --upgrade pip >/dev/null
"$VENV/bin/pip" install "faster-whisper==${FW_VERSION}" >/dev/null

cat > "$VOICE_DIR/transcribe-server.py" <<PY
#!/usr/bin/env python3
import json, tempfile, os, subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from faster_whisper import WhisperModel

PORT=int(os.getenv('TRANSCRIBE_PORT','${TRANSCRIBE_PORT}'))
MODEL_SIZE=os.getenv('WHISPER_MODEL_SIZE','${MODEL_SIZE}')
DEVICE=os.getenv('WHISPER_DEVICE','${DEVICE}')
COMPUTE=os.getenv('WHISPER_COMPUTE_TYPE','${COMPUTE_TYPE}')
ALLOWED_ORIGIN=os.getenv('TRANSCRIBE_ALLOWED_ORIGIN','${ALLOWED_ORIGIN}')
LANGUAGE=os.getenv('WHISPER_LANGUAGE','${LANGUAGE}')
MAX_UPLOAD_MB=int(os.getenv('MAX_UPLOAD_MB','${MAX_UPLOAD_MB}'))

print(f'[transcribe] Loading model {MODEL_SIZE} ({DEVICE}/{COMPUTE})...')
model=WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE)
print(f'[transcribe] Model loaded.')
print(f'[transcribe] Language: {LANGUAGE} (auto = auto-detect)')
print(f'[transcribe] Listening on http://127.0.0.1:{PORT}')

GST_TIMEOUT=120  # seconds

def to_wav(src, dst):
    subprocess.check_call([
      'gst-launch-1.0','-q','filesrc',f'location={src}','!','decodebin','!','audioconvert','!','audioresample','!','wavenc','!','filesink',f'location={dst}'
    ], timeout=GST_TIMEOUT)

MAX_UPLOAD=MAX_UPLOAD_MB*1024*1024

# Known audio magic bytes (prefix → format)
AUDIO_SIGNATURES=[
  (b'RIFF',    'wav'),
  (b'OggS',    'ogg'),
  (b'fLaC',    'flac'),
  (b'ID3',     'mp3'),
  (b'\xff\xfb','mp3'),
  (b'\xff\xf3','mp3'),
  (b'\xff\xf2','mp3'),
  (b'\x1aE\xdf\xa3','webm'),
]
def _looks_like_audio(data: bytes) -> bool:
    # Check magic bytes or ftyp box (m4a/mp4)
    for sig, _ in AUDIO_SIGNATURES:
        if data[:len(sig)] == sig:
            return True
    if len(data) >= 12 and data[4:8] == b'ftyp':
        return True
    return False

class H(BaseHTTPRequestHandler):
    def _cors(self):
      self.send_header('Access-Control-Allow-Origin',ALLOWED_ORIGIN)
      self.send_header('Vary','Origin')
      self.send_header('Access-Control-Allow-Methods','POST, OPTIONS')
      self.send_header('Access-Control-Allow-Headers','Content-Type')
    def do_OPTIONS(self):
      self.send_response(204); self._cors(); self.end_headers()
    def do_POST(self):
      if self.path != '/transcribe':
        self.send_response(404); self.end_headers(); return
      n=int(self.headers.get('Content-Length','0'))
      if n <= 0:
        self.send_response(400); self._cors(); self.send_header('Content-Type','application/json'); self.end_headers()
        self.wfile.write(json.dumps({'error':'empty request body'}).encode()); return
      if n > MAX_UPLOAD:
        self.send_response(413); self._cors(); self.send_header('Content-Type','application/json'); self.end_headers()
        self.wfile.write(json.dumps({'error':f'upload exceeds {MAX_UPLOAD_MB} MB limit'}).encode()); return
      b=self.rfile.read(n)
      if not _looks_like_audio(b):
        self.send_response(415); self._cors(); self.send_header('Content-Type','application/json'); self.end_headers()
        self.wfile.write(json.dumps({'error':'unrecognized audio format'}).encode()); return
      with tempfile.TemporaryDirectory() as d:
        src=os.path.join(d,'in.bin'); wav=os.path.join(d,'in.wav')
        open(src,'wb').write(b)
        try:
          to_wav(src,wav)
          lang_arg={'language': LANGUAGE} if LANGUAGE != 'auto' else {}
          segs,info=model.transcribe(wav, **lang_arg)
          text=' '.join(s.text.strip() for s in segs).strip()
          out=json.dumps({'text':text}).encode()
          self.send_response(200); self._cors(); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(out)
        except subprocess.TimeoutExpired:
          out=json.dumps({'error':'audio conversion timed out'}).encode()
          self.send_response(504); self._cors(); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(out)
        except Exception:
          out=json.dumps({'error':'transcription failed'}).encode()
          self.send_response(500); self._cors(); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(out)

HTTPServer(('127.0.0.1',PORT),H).serve_forever()
PY
chmod +x "$VOICE_DIR/transcribe-server.py"

cat > "$SERVICE_FILE" <<UNIT
[Unit]
Description=OpenClaw Voice Transcription Server (faster-whisper)
After=network.target

[Service]
Type=simple
Environment=TRANSCRIBE_PORT=${TRANSCRIBE_PORT}
Environment=WHISPER_MODEL_SIZE=${MODEL_SIZE}
Environment=WHISPER_DEVICE=${DEVICE}
Environment=WHISPER_COMPUTE_TYPE=${COMPUTE_TYPE}
Environment=TRANSCRIBE_ALLOWED_ORIGIN=${ALLOWED_ORIGIN}
Environment=WHISPER_LANGUAGE=${LANGUAGE}
Environment=MAX_UPLOAD_MB=${MAX_UPLOAD_MB}
ExecStart=${VENV}/bin/python ${VOICE_DIR}/transcribe-server.py
Restart=always
RestartSec=2

[Install]
WantedBy=default.target
UNIT

systemctl --user daemon-reload
systemctl --user enable --now openclaw-transcribe.service
systemctl --user restart openclaw-transcribe.service

echo "deploy:ok workspace=${WORKSPACE} model=${MODEL_SIZE} port=${TRANSCRIBE_PORT}"
