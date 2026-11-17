#!/usr/bin/env bash
# loudness.sh — mide y normaliza loudness de un archivo de audio/video.
#
# Uso:
#   ./loudness.sh medir <archivo>
#   ./loudness.sh normalizar <archivo> [destino_lufs] [salida]
#
# Ejemplos:
#   ./loudness.sh medir mezcla.wav
#   ./loudness.sh normalizar mezcla.wav -14 out/mezcla_web.wav
#   ./loudness.sh normalizar master.mov -23 out/master_broadcast.mov
set -euo pipefail

CMD="${1:-}"
IN="${2:-}"
TARGET="${3:--14}"
OUT="${4:-}"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg no está instalado. Instálalo con: brew install ffmpeg | sudo apt install ffmpeg" >&2
  exit 1
fi

if [[ -z "$CMD" || -z "$IN" ]]; then
  sed -n '2,14p' "$0"
  exit 1
fi

case "$CMD" in
  medir)
    echo "▸ Midiendo loudness de: $IN"
    ffmpeg -hide_banner -nostats -i "$IN" \
      -af "ebur128=peak=true" -f null - 2>&1 \
      | awk '/Summary:/{f=1} f' \
      | grep -Ei "I:|LRA:|Peak:" \
      | sed 's/^ *//'
    echo
    echo "Objetivos:  web/social -14 LUFS · podcast -16 · broadcast -23 · true peak ≤ -1 dBTP"
    ;;
  normalizar)
    if [[ -z "$OUT" ]]; then
      OUT="$(basename "${IN%.*}")_norm_${TARGET}LUFS.${IN##*.}"
    fi
    mkdir -p "$(dirname "$OUT")"
    echo "▸ Normalizando a ${TARGET} LUFS (TP -1.5) → $OUT"
    ffmpeg -hide_banner -y -i "$IN" \
      -af "loudnorm=I=${TARGET}:TP=-1.5:LRA=11:print_format=summary" \
      -c:v copy -c:a aac -b:a 192k -ar 48000 "$OUT"
    echo
    echo "▸ Verificación:"
    ffmpeg -hide_banner -nostats -i "$OUT" -af "ebur128=peak=true" -f null - 2>&1 \
      | awk '/Summary:/{f=1} f' | grep -Ei "I:|Peak:" | sed 's/^ *//'
    ;;
  *)
    echo "Comando desconocido: $CMD (usa: medir | normalizar)" >&2
    exit 1
    ;;
esac
