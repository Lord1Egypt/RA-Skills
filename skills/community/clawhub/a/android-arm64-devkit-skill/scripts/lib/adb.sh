#!/usr/bin/env bash
# Shared adb helpers. Source this file; do not execute it.
#
# Optional environment:
#   ADB_BIN          local adb binary            (default: adb)
#   ADB_REMOTE_HOST  ssh alias of the machine that owns the device
#   ADB_REMOTE_BIN   adb binary path on that machine (default: adb)
#
# Why this exists: `adb -s <dev> ...` must receive "-s" and "<dev>" as SEPARATE
# argv entries. Passing them as one string ("-s dev") fails locally but happens
# to work when the command is rebuilt as a remote shell string — a trap that
# only shows up when you switch transports.

# adb_call <args...>
adb_call() {
  if [ -n "${ADB_REMOTE_HOST:-}" ]; then
    local bin="${ADB_REMOTE_BIN:-adb}" q="" a
    # quote the binary only if its path contains spaces (Windows cmd does not
    # understand single quotes, so unquoted is the portable default)
    case "$bin" in *" "*) bin="\"$bin\"" ;; esac
    for a in "$@"; do q="$q $(printf '%q' "$a")"; done
    ssh -o BatchMode=yes "$ADB_REMOTE_HOST" "$bin$q"
  else
    "${ADB_BIN:-adb}" "$@"
  fi
}

# adb_text <args...>
# Like adb_call, but normalises line endings. A Windows-hosted adb server answers
# with CRLF; a stray \r silently breaks exact comparisons such as
# `[ "$state" = device ]` — which is exactly how "device" read as "offline".
adb_text() { adb_call "$@" | tr -d '\r'; }

# capture_to_file <local-dest> <remote-tmp> <adb args...>
# Binary-safe: PowerShell's ">" redirection re-encodes to UTF-16 and corrupts
# binaries, so on a remote Windows host the redirect runs inside cmd.
capture_to_file() {
  local dest="$1" rtmp="$2"; shift 2
  if [ -n "${ADB_REMOTE_HOST:-}" ]; then
    local bin="${ADB_REMOTE_BIN:-adb}" q="" a
    case "$bin" in *" "*) bin="\"$bin\"" ;; esac
    for a in "$@"; do q="$q $(printf '%q' "$a")"; done
    ssh -o BatchMode=yes "$ADB_REMOTE_HOST" "cmd /c \"$bin$q > $rtmp\"" >/dev/null
    scp -q -o BatchMode=yes "$ADB_REMOTE_HOST:$rtmp" "$dest"
  else
    "${ADB_BIN:-adb}" "$@" > "$dest"
  fi
}
