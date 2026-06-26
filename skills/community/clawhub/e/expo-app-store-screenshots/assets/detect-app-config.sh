#!/usr/bin/env bash
# Detect the deep-link scheme, iOS bundle ID, and Android package from an Expo app.
#
# Usage:
#   bash detect-app-config.sh [PROJECT_DIR]
#
# Prints KEY=VALUE lines to stdout (sourceable):
#   APP_SCHEME=myapp
#   IOS_BUNDLE_ID=com.example.myapp
#   ANDROID_PACKAGE=com.example.myapp
#
# Resolution order:
#   1. `app.json` parsed with jq (fast, no JS execution)
#   2. `npx expo config --type public --json` (handles app.config.ts/.js, slower)
#
# Exits non-zero if nothing could be detected.

set -euo pipefail

project_dir="${1:-.}"
cd "$project_dir"

scheme=""
ios_bundle=""
android_pkg=""

read_from_jq() {
  local file="$1"
  if ! command -v jq >/dev/null 2>&1; then return 1; fi
  if [[ ! -f "$file" ]]; then return 1; fi
  scheme=$(jq -r '.expo.scheme // empty' "$file" 2>/dev/null || true)
  # `scheme` may be an array; pick the first if so
  if [[ -z "$scheme" ]]; then
    scheme=$(jq -r '.expo.scheme[0] // empty' "$file" 2>/dev/null || true)
  fi
  ios_bundle=$(jq -r '.expo.ios.bundleIdentifier // empty' "$file" 2>/dev/null || true)
  android_pkg=$(jq -r '.expo.android.package // empty' "$file" 2>/dev/null || true)
  [[ -n "$scheme" || -n "$ios_bundle" || -n "$android_pkg" ]]
}

read_from_expo_cli() {
  if ! command -v npx >/dev/null 2>&1; then return 1; fi
  local json
  json=$(npx --no-install expo config --type public --json 2>/dev/null) || return 1
  if ! command -v jq >/dev/null 2>&1; then return 1; fi
  scheme=$(printf '%s' "$json" | jq -r '.scheme // empty' 2>/dev/null || true)
  if [[ -z "$scheme" ]]; then
    scheme=$(printf '%s' "$json" | jq -r '.scheme[0] // empty' 2>/dev/null || true)
  fi
  ios_bundle=$(printf '%s' "$json" | jq -r '.ios.bundleIdentifier // empty' 2>/dev/null || true)
  android_pkg=$(printf '%s' "$json" | jq -r '.android.package // empty' 2>/dev/null || true)
  [[ -n "$scheme" || -n "$ios_bundle" || -n "$android_pkg" ]]
}

read_from_jq app.json || read_from_expo_cli || {
  echo "error: could not detect app config in $project_dir" >&2
  echo "       expected app.json with .expo.scheme/.expo.ios.bundleIdentifier/.expo.android.package," >&2
  echo "       or a working 'npx expo config --type public --json'" >&2
  exit 1
}

printf 'APP_SCHEME=%s\n' "$scheme"
printf 'IOS_BUNDLE_ID=%s\n' "$ios_bundle"
printf 'ANDROID_PACKAGE=%s\n' "$android_pkg"
