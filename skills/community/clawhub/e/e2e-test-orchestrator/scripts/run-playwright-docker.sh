#!/usr/bin/env bash
set -euo pipefail

# 用法：
#   ./scripts/run-playwright-docker.sh [grep过滤词]
# 示例：
#   ./scripts/run-playwright-docker.sh "@smoke"

FILTER="${1:-}"
IMAGE="${PW_DOCKER_IMAGE:-mcr.microsoft.com/playwright:v1.58.2-jammy}"
TS="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_DIR="test-results/$TS"
mkdir -p "$OUT_DIR"

GREP_ARG=""
if [[ -n "$FILTER" ]]; then
  GREP_ARG="--grep '$FILTER'"
fi

echo "[run][docker] 镜像: $IMAGE"
echo "[run][docker] 输出目录: $OUT_DIR"

docker run --rm -t \
  -v "$PWD":/work \
  -w /work \
  "$IMAGE" \
  bash -lc "npm ci || npm i; npx playwright test --reporter=line,html --output='$OUT_DIR' $GREP_ARG" | tee "$OUT_DIR/run.log"

echo "[done][docker] 产物目录: $OUT_DIR"
