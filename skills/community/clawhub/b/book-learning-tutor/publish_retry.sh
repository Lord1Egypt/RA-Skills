#!/usr/bin/env bash
# publish_retry.sh — publish Book Learning Tutor to ClawHub with TLS-retry resilience.
# Background: Node/OpenSSL TLS to clawhub.ai intermittently drops the handshake
# ("Client network socket disconnected before secure TLS connection was established").
# Browser/schannel reach it fine, so auth uses a token (generated in the web UI),
# and the publish upload is retried until it lands.
set -u

# Use Windows-style path (E:/...) — Node mis-resolves Git-Bash /e/... as E:\e\...
PUBDIR="$(cd "$(dirname "$0")" && pwd -W)"
cd "$PUBDIR"

TOKEN="${CLAWHUB_TOKEN:-}"
SLUG="book-learning-tutor"
VERSION="0.1.3"
CHANGELOG="Restore full tools/ engine; align with GitHub fangyuan-3149/book-learning-tutor @ e2d099f (v0.1.3)."
REGISTRY="${CLAWHUB_REGISTRY:-https://clawhub.ai}"
SITE="${CLAWHUB_SITE:-https://clawhub.ai}"
MAX=30
SLEEP=5

store_token() {
  [ -z "$TOKEN" ] && { echo "[login] no token provided; relying on CLAWHUB_TOKEN env at publish time"; return 0; }
  for ((i=1;i<=MAX;i++)); do
    echo "[login] attempt $i/$MAX"
    if CLAWHUB_TOKEN="$TOKEN" CLAWDHUB_TOKEN="$TOKEN" \
       npx --yes clawhub@latest login --token "$TOKEN" --label "sandbox-publish" 2>&1; then
      echo "[login] token stored"; return 0
    fi
    read -t "$SLEEP" </dev/null 2>/dev/null || true
  done
  echo "[login] could not store token via network; publish will try CLAWHUB_TOKEN env directly"
}

publish() {
  for ((i=1;i<=MAX;i++)); do
    echo "[publish] attempt $i/$MAX"
    if CLAWHUB_TOKEN="$TOKEN" CLAWDHUB_TOKEN="$TOKEN" \
       CLAWHUB_REGISTRY="$REGISTRY" CLAWHUB_SITE="$SITE" \
       npx --yes clawhub@latest skill publish "$PUBDIR" \
         --slug "$SLUG" --name "Book Learning Tutor" --version "$VERSION" --changelog "$CHANGELOG" \
         --source-repo "https://github.com/fangyuan-3149/book-learning-tutor" \
         --source-commit "e2d099f" \
         --json 2>&1; then
      echo "[publish] SUCCESS"
      return 0
    fi
    echo "[publish] failed (likely TLS drop); retrying in ${SLEEP}s"
    read -t "$SLEEP" </dev/null 2>/dev/null || true
  done
  echo "[publish] FAILED after $MAX attempts"
  return 1
}

store_token
publish
