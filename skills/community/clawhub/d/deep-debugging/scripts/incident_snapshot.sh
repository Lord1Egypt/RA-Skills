#!/usr/bin/env bash
set -euo pipefail

# Safe local diagnostic snapshot for debugging/incident triage.
# It prints metadata and environment KEY NAMES only. It must never print env values.

redact_path() {
  sed -E "s#${HOME}#~#g"
}

section() {
  printf '\n## %s\n' "$1"
}

section "time"
date -u '+utc=%Y-%m-%dT%H:%M:%SZ'
date '+local=%Y-%m-%dT%H:%M:%S%z' 2>/dev/null || true

section "system"
printf 'pwd=%s\n' "$(pwd | redact_path)"
printf 'kernel=%s\n' "$(uname -srm 2>/dev/null || true)"
command -v node >/dev/null 2>&1 && printf 'node=%s\n' "$(node -v)"
command -v npm >/dev/null 2>&1 && printf 'npm=%s\n' "$(npm -v)"
command -v pnpm >/dev/null 2>&1 && printf 'pnpm=%s\n' "$(pnpm -v)"
command -v yarn >/dev/null 2>&1 && printf 'yarn=%s\n' "$(yarn -v)"
command -v python3 >/dev/null 2>&1 && printf 'python3=%s\n' "$(python3 --version 2>&1)"

section "git"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf 'branch=%s\n' "$(git branch --show-current 2>/dev/null || true)"
  printf 'commit=%s\n' "$(git rev-parse --short HEAD 2>/dev/null || true)"
  printf 'dirty_files=%s\n' "$(git status --short 2>/dev/null | wc -l | tr -d ' ')"
  echo 'recent_commits='
  git log --oneline -5 2>/dev/null || true
else
  echo 'not_a_git_repo=true'
fi

section "project_files"
for f in package.json pnpm-lock.yaml package-lock.json yarn.lock tsconfig.json next.config.js next.config.mjs prisma/schema.prisma Dockerfile docker-compose.yml railway.json vercel.json; do
  [ -e "$f" ] && printf '%s\n' "$f"
done

section "env_key_names"
# Print only names likely relevant to runtime/debugging. Never values.
env | cut -d= -f1 | grep -E '(^NODE_ENV$|^APP_ENV$|^PORT$|DATABASE|REDIS|JWT|AUTH|COOKIE|CORS|API|WEBHOOK|STRIPE|OPENAI|ANTHROPIC|RAILWAY|VERCEL|NEXT_PUBLIC)' | sort -u || true

section "listening_ports"
if command -v lsof >/dev/null 2>&1; then
  lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null | awk 'NR==1 || /node|python|bun|deno|next|npm|pnpm/ {print $1,$2,$9}' || true
else
  echo 'lsof_unavailable=true'
fi

section "notes"
echo 'Secrets, tokens, cookies, env values, and customer data intentionally omitted.'
