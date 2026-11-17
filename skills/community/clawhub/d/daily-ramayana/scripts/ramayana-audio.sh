#!/usr/bin/env bash
# Usage: ramayana-audio.sh <read.txt> <out.mp3> [--no-bed]
# Chinese TTS (edge-tts, zh-CN-XiaoxiaoNeural, -10%) + optional quiet tanpura-style drone bed.
# stdout: RAMAUDIO_OK | RAMAUDIO_SKIP (NO_TTS set) | RAMAUDIO_WARN (voice ok, bed failed) | RAMAUDIO_ERR
set -u
IN="${1:-}"; OUT="${2:-}"; BED=1
[ "${3:-}" = "--no-bed" ] && BED=0
if [ -n "${NO_TTS:-}" ]; then echo "RAMAUDIO_SKIP"; exit 0; fi
if [ -z "$IN" ] || [ -z "$OUT" ] || [ ! -s "$IN" ]; then echo "RAMAUDIO_ERR missing input"; exit 0; fi
VOICE="${RAMA_VOICE:-zh-CN-XiaoxiaoNeural}"; RATE="${RAMA_RATE:--10%}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$(dirname "$OUT")"
if ! timeout 300 uvx edge-tts --voice "$VOICE" --rate="$RATE" --file "$IN" --write-media "$TMP/voice.mp3" >/dev/null 2>"$TMP/tts.err"; then
  echo "RAMAUDIO_ERR tts failed: $(tail -1 "$TMP/tts.err")"; exit 0
fi
if [ "$BED" = 0 ] || ! command -v ffmpeg >/dev/null; then
  cp "$TMP/voice.mp3" "$OUT"; echo "RAMAUDIO_OK $OUT (no bed)"; exit 0
fi
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMP/voice.mp3" 2>/dev/null | cut -d. -f1)
DUR=$(( ${DUR:-60} + 4 ))
# Tanpura-like drone: Sa (D3) + Pa (A3) + Sa' (D4), slow tremolo, low volume, ducked under the voice.
if ffmpeg -y -v error \
  -f lavfi -i "sine=f=146.83:d=$DUR" -f lavfi -i "sine=f=220:d=$DUR" -f lavfi -i "sine=f=293.66:d=$DUR" \
  -i "$TMP/voice.mp3" \
  -filter_complex "[0][1][2]amix=inputs=3,tremolo=f=0.25:d=0.5,aecho=0.8:0.7:60:0.3,lowpass=f=1200,volume=0.09,afade=t=in:d=3,afade=t=out:st=$((DUR-3)):d=3[bed];[3]adelay=1500|1500,apad=pad_dur=2.5[v];[v]asplit[v1][v2];[bed][v1]sidechaincompress=threshold=0.03:ratio=6:attack=50:release=600[ducked];[ducked][v2]amix=inputs=2:duration=shortest:normalize=0,volume=1.0" \
  -ac 2 -ar 44100 -b:a 128k "$OUT" 2>"$TMP/ff.err"; then
  echo "RAMAUDIO_OK $OUT"
else
  cp "$TMP/voice.mp3" "$OUT"; echo "RAMAUDIO_WARN bed failed, voice only: $(tail -1 "$TMP/ff.err")"
fi
