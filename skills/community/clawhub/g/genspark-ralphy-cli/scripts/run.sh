#!/bin/sh
set -eu
ralphy_skill_dir=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
if [ -f "$ralphy_skill_dir/.repo-path" ]; then
  IFS= read -r ralphy_repo < "$ralphy_skill_dir/.repo-path"
else
  ralphy_repo=$(CDPATH='' cd -- "$ralphy_skill_dir/../.." && pwd)
fi
if [ ! -x "$ralphy_repo/bin/ralphy-claw" ]; then
  echo 'ralphy-claw repository unavailable. Reinstall this skill with bun run install-skill.' >&2
  exit 1
fi
exec "$ralphy_repo/bin/ralphy-claw" "$@"
