#!/usr/bin/env bash
set -euo pipefail

TEXT="${*:-}"
if [[ -z "$TEXT" && -f docs/cccc/state.json ]]; then
  TEXT="$(jq -r '.task // empty' docs/cccc/state.json 2>/dev/null || true)"
fi

python3 - "$TEXT" <<'PY'
import re, sys
text = sys.argv[1] if len(sys.argv) > 1 else ""
if re.search(r"用中文|中文回答|Chinese|zh-CN", text, re.I):
    print("zh-CN")
elif re.search(r"English|英文|respond in English", text, re.I):
    print("en")
else:
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin = len(re.findall(r"[A-Za-z]+", text))
    print("zh-CN" if cjk >= latin and cjk > 0 else "en")
PY
