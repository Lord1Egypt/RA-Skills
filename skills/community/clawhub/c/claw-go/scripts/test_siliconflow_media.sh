#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/../assets/config-template.env"

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
fi

PROMPT="${1:-same mascot identity as 虾游记 icon, bright red cartoon crayfish, bold black outline, selfie pose, harbor light, travel postcard style}"
TEXT="${2:-旅伴，我发来一张新明信片。虾游记今天翻到港口篇了。}"

echo "== image request =="
curl --silent --show-error "${CLAWGO_IMAGE_API_BASE}" \
  --header "Authorization: Bearer ${CLAWGO_IMAGE_API_KEY}" \
  --header "Content-Type: application/json" \
  --data "{
    \"model\": \"${CLAWGO_IMAGE_MODEL}\",
    \"prompt\": \"${PROMPT}\"
  }"

echo
echo "== tts request =="
curl --silent --show-error "${CLAWGO_TTS_API_BASE}" \
  --header "Authorization: Bearer ${CLAWGO_TTS_API_KEY}" \
  --header "Content-Type: application/json" \
  --data "{
    \"model\": \"${CLAWGO_TTS_MODEL}\",
    \"input\": \"${TEXT}\",
    \"voice\": \"${CLAWGO_TTS_VOICE}\"
  }"
