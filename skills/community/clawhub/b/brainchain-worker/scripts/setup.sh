#!/bin/sh
# Builds the sandbox image the worker's tools run in, once.
set -eu
command -v docker >/dev/null || { echo "Docker is required: the worker runs its shell in a container." >&2; exit 1; }
docker image inspect openclaw-sandbox:bookworm-slim >/dev/null 2>&1 && { echo "Sandbox image present."; exit 0; }
docker build -t openclaw-sandbox:bookworm-slim - <<'DOCKERFILE'
FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
  bash ca-certificates curl git jq python3 ripgrep \
  && rm -rf /var/lib/apt/lists/*
RUN useradd --create-home --shell /bin/bash sandbox
USER sandbox
WORKDIR /home/sandbox
CMD ["sleep", "infinity"]
DOCKERFILE
echo "Sandbox image built."
