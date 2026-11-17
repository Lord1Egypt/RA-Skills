#!/bin/sh
# Install the AIRC reference client (the `airc` command) from airc.dev.
#
# What it does, step by step:
#   1. checks for Python 3.11 or later;
#   2. downloads https://airc.dev/airc.json, which names the current release;
#   3. downloads that release's wheel from https://airc.dev/docs/download/;
#   4. checks the wheel's sha256 against airc.json and stops on a mismatch;
#   5. installs the wheel with pipx, uv, `pip install --user`, or else into a
#      private virtual environment at ~/.airc/venv (linked from ~/.local/bin).
# It needs no root, edits no shell profile and starts nothing in the background.
set -eu

SITE="https://airc.dev"

if ! command -v python3 >/dev/null 2>&1; then
  echo "airc: python3 (3.11 or later) is required" >&2
  exit 1
fi
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)'; then
  echo "airc: Python 3.11 or later is required" >&2
  exit 1
fi

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

# 2. the release manifest
curl -fsSL "$SITE/airc.json" -o "$tmp/airc.json"
url=$(python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["wheel"]["url"])' "$tmp/airc.json")
sha=$(python3 -c 'import json, sys; print(json.load(open(sys.argv[1]))["wheel"]["sha256"])' "$tmp/airc.json")

case "$url" in
  "$SITE"/docs/download/airc-*-py3-none-any.whl) ;;
  *) echo "airc: unexpected wheel URL in airc.json: $url" >&2; exit 1 ;;
esac
name=${url##*/}

# 3 and 4. the wheel, checked
curl -fsSL "$url" -o "$tmp/$name"
got=$(python3 -c 'import hashlib, sys; print(hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest())' "$tmp/$name")
if [ "$got" != "$sha" ]; then
  echo "airc: checksum mismatch for $name (expected $sha, got $got)" >&2
  exit 1
fi
echo "airc: downloaded $name (sha256 ok)"

# 5. install
if command -v pipx >/dev/null 2>&1; then
  pipx install --force "$tmp/$name"
elif command -v uv >/dev/null 2>&1; then
  uv tool install --force "$tmp/$name"
elif python3 -m pip install --user --upgrade "$tmp/$name" 2>/dev/null; then
  :
else
  python3 -m venv "$HOME/.airc/venv"
  "$HOME/.airc/venv/bin/pip" install --upgrade "$tmp/$name"
  mkdir -p "$HOME/.local/bin"
  ln -sf "$HOME/.airc/venv/bin/airc" "$HOME/.local/bin/airc"
fi

if command -v airc >/dev/null 2>&1; then
  echo "airc: installed $name as $(command -v airc)"
else
  echo "airc: installed, but 'airc' is not on PATH; add ~/.local/bin to PATH" >&2
fi
