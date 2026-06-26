#!/bin/bash
# run-claude.sh — Roda Claude Code e retorna o output para a FAYE reportar ao utilizador
#
# Uso:
#   run-claude.sh "prompt"              → nova sessão no workdir padrão
#   run-claude.sh "prompt" /workdir     → nova sessão no workdir indicado
#   run-claude.sh --continue "prompt"   → continua a última sessão do workdir padrão
#   run-claude.sh --continue "prompt" /workdir → continua a última sessão do workdir indicado

CONTINUE=""
if [ "$1" = "--continue" ] || [ "$1" = "-c" ]; then
  CONTINUE="--continue"
  shift
fi

PROMPT="$1"
WORKDIR="${2:-/home/xmanel/.openclaw/workspace}"

if [ -z "$PROMPT" ]; then
  echo "Uso: run-claude.sh [--continue] 'prompt' [workdir]"
  exit 1
fi

cd "$WORKDIR" 2>/dev/null || cd /home/xmanel/.openclaw/workspace

# env -u CLAUDECODE evita erro de nested session
OUTPUT=$(env -u CLAUDECODE claude \
  --permission-mode bypassPermissions \
  --print \
  $CONTINUE \
  "$PROMPT" 2>&1)

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "$OUTPUT"
else
  echo "[ERRO $EXIT_CODE]"
  echo "$OUTPUT"
fi
