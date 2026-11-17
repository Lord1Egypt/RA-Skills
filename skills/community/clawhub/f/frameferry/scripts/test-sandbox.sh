#!/usr/bin/env bash
set -euo pipefail
repo=$(cd "$(dirname "$0")/.." && pwd -P)
if ! command -v bwrap >/dev/null 2>&1; then echo "bwrap not found; refusing unsandboxed test:sandbox" >&2; exit 1; fi
if [ ! -d "$repo/node_modules" ]; then echo "node_modules missing; run npm ci first" >&2; exit 1; fi
node_path=$(command -v node)
work=$(mktemp -d "${TMPDIR:-/tmp}/instacognito-sandbox.XXXXXX")
cleanup(){ rm -rf "$work"; }
trap cleanup EXIT
mkdir -p "$work/work"
# Copy only public synthetic source/test/docs, never .git, reports, archives, home, logs, drives, sockets, or secrets.
for item in package.json package-lock.json SKILL.md README.md LICENSE SECURITY.md CHANGELOG.md bin src scripts test; do
  cp -a "$repo/$item" "$work/work/"
done
args=(--die-with-parent --unshare-all --unshare-cgroup-try --new-session --clearenv --cap-drop ALL)
for d in /usr /bin /lib /lib64 /etc/ssl /etc/alternatives; do
  if [ -e "$d" ]; then args+=(--ro-bind "$d" "$d"); fi
done
args+=(--dir /tmp --tmpfs /tmp --proc /proc --dev /dev)
args+=(--bind "$work/work" /work --ro-bind "$repo/node_modules" /work/node_modules --chdir /work)
args+=(--setenv HOME /tmp/home --dir /tmp/home --setenv PATH /usr/local/bin:/usr/bin:/bin --setenv NODE_ENV test --setenv CI 1 --setenv NODE_OPTIONS --max-old-space-size=512 --setenv INSTACOGNITO_SANDBOX bwrap-copy-no-net)
chromium_real=""
if [ -x /usr/bin/chromium ]; then chromium_real=$(readlink -f /usr/bin/chromium); fi
if [ -n "$chromium_real" ] && [ -x "$chromium_real" ]; then
  chromium_dir=$(dirname "$chromium_real")
  # Create empty mount-point parents inside the sandbox without binding the real home/cache tree.
  parent=""
  IFS=/ read -r -a parts <<< "${chromium_dir#/}"
  for part in "${parts[@]}"; do
    parent="$parent/$part"
    [ "$parent" = "$chromium_dir" ] && break
    args+=(--dir "$parent")
  done
  args+=(--ro-bind "$chromium_dir" "$chromium_dir")
  args+=(--setenv PLAYWRIGHT_CHROMIUM_EXECUTABLE "$chromium_real")
fi
echo "sandbox: bwrap isolated copied tree, no network namespace, clearenv, cap-drop, cgroup MemoryMax=1G, node heap cap 512MiB" >&2
if command -v systemd-run >/dev/null 2>&1 && systemd-run --user --scope --quiet -p MemoryMax=1G -p TasksMax=512 true 2>/dev/null; then
  systemd-run --user --scope --quiet -p MemoryMax=1G -p TasksMax=512 bwrap "${args[@]}" "$node_path" --test
  exit_code=$?
  exit "$exit_code"
fi
echo "warning: systemd-run user scope unavailable; using bwrap namespace plus Node heap cap only" >&2
bwrap "${args[@]}" "$node_path" --test
exit_code=$?
exit "$exit_code"
