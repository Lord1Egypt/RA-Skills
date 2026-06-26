#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUNTIME_DIR="${AIONIS_RUNTIME_DIR:-${SKILL_DIR}/.runtime}"
ENV_FILE="${RUNTIME_DIR}/aionis.env"
CLAWBOT_ENV_FILE="${RUNTIME_DIR}/clawbot.env"

AIONIS_CONTAINER_NAME="${AIONIS_CONTAINER_NAME:-aionis-standalone-local}"
AIONIS_IMAGE="${AIONIS_IMAGE:-ghcr.io/cognary/aionis:standalone-v0.2.5}"
AIONIS_PORT="${AIONIS_PORT:-3001}"
AIONIS_VOLUME="${AIONIS_VOLUME:-aionis-standalone-data}"

EMBEDDING_PROVIDER="${EMBEDDING_PROVIDER:-fake}"
MINIMAX_API_KEY="${MINIMAX_API_KEY:-}"
MINIMAX_GROUP_ID="${MINIMAX_GROUP_ID:-}"
MINIMAX_EMBED_MODEL="${MINIMAX_EMBED_MODEL:-embo-01}"
MINIMAX_EMBED_TYPE="${MINIMAX_EMBED_TYPE:-db}"
MINIMAX_EMBED_ENDPOINT="${MINIMAX_EMBED_ENDPOINT:-https://api.minimax.chat/v1/embeddings}"

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "missing required command: $1" >&2
    exit 1
  }
}

random_token() {
  need openssl
  openssl rand -base64 48 | tr '+/' '-_' | tr -d '=' | cut -c1-64
}

extract_api_key() {
  local raw="$1"
  printf "%s" "$raw" | sed -E 's/^\{"([^"]+)".*/\1/'
}

wait_health() {
  local url="$1"
  local max_tries=30
  local try=1
  while [[ $try -le $max_tries ]]; do
    if curl -fsS "$url" >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
    try=$((try + 1))
  done
  return 1
}

write_env_file() {
  local memory_api_key="$1"
  local admin_token="$2"

  {
    echo "NODE_ENV=production"
    echo "APP_ENV=prod"
    echo "AIONIS_MODE=service"
    echo "PORT=3001"
    echo "TRUST_PROXY=false"
    echo
    echo "MEMORY_AUTH_MODE=api_key"
    echo "MEMORY_API_KEYS_JSON={\"${memory_api_key}\":{\"tenant_id\":\"default\",\"agent_id\":\"clawbot\",\"team_id\":\"default\"}}"
    echo "ADMIN_TOKEN=${admin_token}"
    echo
    echo "EMBEDDING_PROVIDER=${EMBEDDING_PROVIDER}"
    echo "EMBEDDING_DIM=1536"
    if [[ "${EMBEDDING_PROVIDER}" == "minimax" ]]; then
      echo "MINIMAX_API_KEY=${MINIMAX_API_KEY}"
      echo "MINIMAX_GROUP_ID=${MINIMAX_GROUP_ID}"
      echo "MINIMAX_EMBED_MODEL=${MINIMAX_EMBED_MODEL}"
      echo "MINIMAX_EMBED_TYPE=${MINIMAX_EMBED_TYPE}"
      echo "MINIMAX_EMBED_ENDPOINT=${MINIMAX_EMBED_ENDPOINT}"
    fi
    echo
    echo "CORS_ALLOW_ORIGINS="
    echo "CORS_ADMIN_ALLOW_ORIGINS="
  } >"$ENV_FILE"
}

write_clawbot_env_file() {
  local memory_api_key="$1"
  local admin_token="$2"
  {
    echo "AIONIS_BASE_URL=http://127.0.0.1:${AIONIS_PORT}"
    echo "AIONIS_API_KEY=${memory_api_key}"
    echo "AIONIS_ADMIN_TOKEN=${admin_token}"
    echo "AIONIS_TENANT_ID=default"
    echo "AIONIS_SCOPE_PREFIX=clawbot"
  } >"$CLAWBOT_ENV_FILE"
}

need docker
need curl

if ! docker info >/dev/null 2>&1; then
  echo "docker daemon is not running or not accessible" >&2
  exit 1
fi

if [[ "${EMBEDDING_PROVIDER}" == "minimax" ]]; then
  if [[ -z "${MINIMAX_API_KEY}" || -z "${MINIMAX_GROUP_ID}" ]]; then
    echo "EMBEDDING_PROVIDER=minimax requires MINIMAX_API_KEY and MINIMAX_GROUP_ID" >&2
    exit 1
  fi
fi

mkdir -p "$RUNTIME_DIR"

memory_api_key=""
admin_token=""

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  memory_api_key="$(extract_api_key "${MEMORY_API_KEYS_JSON:-}")"
  admin_token="${ADMIN_TOKEN:-}"
fi

if [[ -z "$memory_api_key" ]]; then
  memory_api_key="${AIONIS_MEMORY_API_KEY:-$(random_token)}"
fi

if [[ -z "$admin_token" ]]; then
  admin_token="${AIONIS_ADMIN_TOKEN:-$(random_token)}"
fi

write_env_file "$memory_api_key" "$admin_token"
write_clawbot_env_file "$memory_api_key" "$admin_token"

if ! docker image inspect "$AIONIS_IMAGE" >/dev/null 2>&1; then
  if ! docker pull "$AIONIS_IMAGE" >/dev/null; then
    echo "failed to pull image: ${AIONIS_IMAGE}" >&2
    echo "hint: set AIONIS_IMAGE to an available local image, or run docker login for private registry" >&2
    exit 1
  fi
fi

docker rm -f "$AIONIS_CONTAINER_NAME" >/dev/null 2>&1 || true

docker run -d \
  --name "$AIONIS_CONTAINER_NAME" \
  --restart unless-stopped \
  -p "127.0.0.1:${AIONIS_PORT}:3001" \
  --env-file "$ENV_FILE" \
  -v "${AIONIS_VOLUME}:/var/lib/postgresql/data" \
  "$AIONIS_IMAGE" >/dev/null

if ! wait_health "http://127.0.0.1:${AIONIS_PORT}/health"; then
  echo "aionis standalone failed health check; inspect logs:" >&2
  echo "docker logs ${AIONIS_CONTAINER_NAME}" >&2
  exit 1
fi

echo "Aionis standalone is running."
echo "Container: ${AIONIS_CONTAINER_NAME}"
echo "Base URL: http://127.0.0.1:${AIONIS_PORT}"
echo "Skill env file: ${CLAWBOT_ENV_FILE}"
echo
echo "Export for current shell:"
echo "source ${CLAWBOT_ENV_FILE}"
