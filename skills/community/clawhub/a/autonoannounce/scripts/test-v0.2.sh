#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
SCRIPTS="$ROOT/skills/autonoannounce/scripts"

echo "[test] setup-first-run dry-run (shell wrapper)"
json=$($SCRIPTS/setup-first-run.sh --noninteractive --dry-run --earcons y --style "test style" --backend auto --device "" --generate-starters n)
echo "$json" | python3 -c 'import json,sys; j=json.load(sys.stdin); assert j["earcons"]["enabled"] is True; assert "playback" in j; assert "device" in j["playback"]'

echo "[test] setup-first-run dry-run (python direct)"
json2=$(python3 "$SCRIPTS/setup_first_run.py" --noninteractive --dry-run --earcons y --style "test style" --backend auto --device "" --generate-starters n)
echo "$json2" | python3 -c 'import json,sys; j=json.load(sys.stdin); assert "playback" in j and "backend" in j["playback"]'

echo "[test] backend detect"
backend=$($SCRIPTS/backend-detect.sh || true)
[[ -n "$backend" ]] || { echo "backend empty" >&2; exit 1; }

echo "[test] playback validate"
$SCRIPTS/playback-validate.sh >/dev/null || true

echo "[test] playback probe"
$SCRIPTS/playback-probe.sh auto >/dev/null || true

echo "[test] preflight retry semantics (mock)"
pf=$(ELEVENLABS_PREFLIGHT_MOCK=1 ELEVENLABS_PREFLIGHT_MOCK_SFX_CODES=429,429,200 SFX_MAX_RETRIES=3 "$SCRIPTS/elevenlabs-preflight.sh")
echo "$pf" | python3 -c 'import json,sys; j=json.load(sys.stdin); assert j["sfx_status"]=="ok"; assert j["sfx_attempts"]>=3; assert j["mock_mode"] is True'

echo "[test] preflight terminal state (mock forbidden)"
pf2=$(ELEVENLABS_PREFLIGHT_MOCK=1 ELEVENLABS_PREFLIGHT_MOCK_SFX_CODES=403 "$SCRIPTS/elevenlabs-preflight.sh")
echo "$pf2" | python3 -c 'import json,sys; j=json.load(sys.stdin); assert j["sfx_status"]=="forbidden_or_missing_permission"'

echo "[test] earcon cache reuse sanity"
mkdir -p "$ROOT/.openclaw" "$ROOT/config"
cat > "$ROOT/config/tts-queue.json" <<EOF
{
  "earcons": {
    "enabled": true,
    "categories": {
      "start": "$ROOT/audio/earcons/existing-start.mp3",
      "end": "",
      "update": "",
      "important": "",
      "error": ""
    },
    "libraryPath": "$ROOT/.openclaw/earcon-library.json"
  },
  "playback": {"backend": "auto", "device": ""}
}
EOF
$SCRIPTS/earcon-library.sh init >/dev/null
missing=$($SCRIPTS/earcon-library.sh missing)
echo "$missing" | grep -q "end"

echo "[ok] tests passed"
