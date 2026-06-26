#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
JSON_INPUT="${JSON_INPUT:-${1:-${SCRIPT_DIR}/../generated_caption.json}}"
JSON_IMAGES="${JSON_IMAGES:-${2:-}}"
IMAGES="${IMAGES:-}"
XHS_MCP_URL="${XHS_MCP_URL:-http://localhost:18060/mcp}"

if [[ -z "${JSON_INPUT}" ]]; then
  echo "Usage: JSON_INPUT=path/to/generated_caption.json [JSON_IMAGES=path/to/images.json] [IMAGES='a.png,b.png'] $0"
  echo "   or: $0 path/to/generated_caption.json [path/to/images.json]"
  exit 1
fi

read_images_from_json() {
  "${PYTHON_BIN}" - "$1" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
if not path.exists():
    raise SystemExit(1)
data = json.loads(path.read_text(encoding="utf-8"))
if isinstance(data, dict):
    data = data.get("images", [])
if not isinstance(data, list):
    raise SystemExit(1)
for item in data:
    s = str(item).strip()
    if s:
        print(s)
PY
}

image_list=()
if [[ -n "${IMAGES}" ]]; then
  IFS=',' read -r -a raw_images <<< "${IMAGES}"
  for img in "${raw_images[@]}"; do
    trimmed="$(printf '%s' "${img}" | xargs)"
    if [[ -n "${trimmed}" ]]; then
      image_list+=("${trimmed}")
    fi
  done
fi

if [[ ${#image_list[@]} -eq 0 && -n "${JSON_IMAGES}" ]]; then
  while IFS= read -r line; do
    [[ -n "${line}" ]] && image_list+=("${line}")
  done < <(read_images_from_json "${JSON_IMAGES}")
fi

if [[ ${#image_list[@]} -eq 0 ]]; then
  while IFS= read -r line; do
    [[ -n "${line}" ]] && image_list+=("${line}")
  done < <(find "${SCRIPT_DIR}/../generated_images" -maxdepth 1 -name '*.png' | sort)
fi

if [[ ${#image_list[@]} -eq 0 ]]; then
  echo "未找到可发布图片，请传 JSON_IMAGES 或 IMAGES"
  exit 1
fi

cmd=("${PYTHON_BIN}" "${SCRIPT_DIR}/publish_to_xhs.py" "--caption-file" "${JSON_INPUT}" "--images")
for img in "${image_list[@]}"; do
  cmd+=("${img}")
done

export XHS_MCP_URL
printf 'Running:'
printf ' %q' "${cmd[@]}"
printf '
'
"${cmd[@]}"
