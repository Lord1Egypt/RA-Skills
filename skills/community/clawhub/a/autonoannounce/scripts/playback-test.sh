#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
TMP="$ROOT/.openclaw/playback-test-tone.wav"
mkdir -p "$(dirname "$TMP")"

# Generate short tone if missing (440Hz, 0.4s)
if ! [[ -f "$TMP" ]]; then
  ROOT_DIR="$ROOT" python3 - <<'PY'
import wave, math, struct, os
path=os.path.join(os.environ['ROOT_DIR'],'.openclaw','playback-test-tone.wav')
fr=44100
sec=0.4
amp=16000
freq=440.0
n=int(fr*sec)
with wave.open(path,'w') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(fr)
    for i in range(n):
        s=int(amp*math.sin(2*math.pi*freq*i/fr))
        w.writeframes(struct.pack('<h', s))
PY
fi

"$ROOT/skills/autonoannounce/scripts/play-local-audio.sh" "$TMP" "$@"

echo "If you heard the tone, playback path is good."
