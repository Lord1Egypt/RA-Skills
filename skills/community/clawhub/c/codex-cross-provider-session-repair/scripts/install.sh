#!/usr/bin/env sh
set -eu

destination=${1:-"$HOME/.agents/skills"}
source=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
name=$(basename "$source")
target="$destination/$name"

case "$target" in
  "$source") echo "Destination is the source checkout; install from a separate clone or package." >&2; exit 2 ;;
esac

mkdir -p "$destination"
if [ -e "$target" ]; then
  mv "$target" "$target.bak-$(date -u +%Y%m%d-%H%M%S)"
fi
mkdir -p "$target"
cp -R "$source"/. "$target"/
printf 'Installed %s from %s to %s\n' "$name" "$source" "$target"
