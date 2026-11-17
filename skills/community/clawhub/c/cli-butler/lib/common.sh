#!/usr/bin/env bash
# cli-butler shared library: channel detection, provenance, journal, output.
# POSIX-ish bash; zero third-party deps. See docs/provenance.md for the model.

set -u
# shellcheck disable=SC1091  # sibling lib files are sourced at runtime

BUTLER_VERSION="0.1.1"
JOURNAL_DIR="${BUTLER_JOURNAL_DIR:-$HOME/.config/cli-butler}"
JOURNAL="$JOURNAL_DIR/journal.tsv"

die() { printf 'cli-butler: %s\n' "$*" >&2; exit 1; }

usage() {
  cat <<EOF
cli-butler v$BUTLER_VERSION — local CLI toolkit manager (agent skill)
usage: <script>.sh [options] [args]
docs: docs/REQUIREMENTS.md  status: skeleton, see docs/design.md
EOF
}

have() { command -v "$1" >/dev/null 2>&1; }

# Run a probe command with a timeout so one slow channel can't block listing.
probe() { # probe <timeout_s> <cmd...>; BUTLER_PROBE_TIMEOUT overrides (tests)
  # portable watchdog (macOS lacks coreutils timeout). Capture goes through a
  # temp FILE, not a pipe: a killed command can leave orphaned children holding
  # the capture pipe open, and command substitutions would block on their EOF.
  local t="$1" pid w; shift
  [ -n "${BUTLER_PROBE_TIMEOUT:-}" ] && t="$BUTLER_PROBE_TIMEOUT"
  [ -n "${PROBE_TMP:-}" ] || PROBE_TMP="${TMPDIR:-/tmp}/butler-probe.$$"
  : >"$PROBE_TMP"
  "$@" >"$PROBE_TMP" 2>/dev/null &
  pid=$!
  { sleep "$t" && kill "$pid" 2>/dev/null; } >/dev/null 2>&1 &
  w=$!
  wait "$pid" 2>/dev/null
  kill "$w" 2>/dev/null
  wait "$w" 2>/dev/null
  cat "$PROBE_TMP"
  return 0
}

# shellcheck disable=SC2034  # consumed by bin/list.sh and lib/channels.sh via source
WHW_RET="" # whatis_desc main-shell result (cache AW_$n + budget need main shell)
whatis_desc() { # <name> -> sets WHW_RET; one-line man description, local db only
  # cached (AW_$name) and budgeted: whatis costs ~1s/name on macOS, so callers
  # must NOT wrap this in command substitution (cache/counter would be lost)
  local n="$1" key cached d
  WHW_RET=""
  # eval-global keys must be valid identifiers (@, -, /, dots are common in names)
  key="${n//_/__}"; key="${key//[^A-Za-z0-9_]/_Q}"
  eval "cached=\"\${AW_$key+x}\""
  if [ -n "$cached" ]; then eval "WHW_RET=\"\${AW_$key}\""; return 0; fi
  [ -n "${WHATIS_LEFT:-}" ] || WHATIS_LEFT="${BUTLER_WHATIS_BUDGET:-20}"
  [ "$WHATIS_LEFT" -gt 0 ] || return 0
  WHATIS_LEFT=$((WHATIS_LEFT - 1))
  d=$(probe 5 whatis "$n" 2>/dev/null | LC_ALL=C awk -F' - ' 'NF >= 2 { print $2; exit }')
  eval "AW_$key=\$d"
  # shellcheck disable=SC2034  # consumed by callers in the same shell
  WHW_RET="$d"
}

# Channels in probe order; each entry "id|probe-cmd".
# shellcheck disable=SC2034  # consumed by bin/* and lib/channels.sh via source
CHANNELS="brew:brew npm:npm pnpm:pnpm pipx:pipx uv:uv cargo:cargo gem:gem apt:apt"

# --- platform & path primitives (F1 foundation) ---

is_darwin() {
  local os="${BUTLER_OS_OVERRIDE:-$(uname -s 2>/dev/null)}"
  [ "$os" = "Darwin" ]
}

realpath_safe() { # <path> -> absolute resolved path; falls back to input
  # canonical dirs are memoized per-run (DIRC_*): the scan feeds thousands of
  # candidates and cd+pwd per candidate is measurable; keys are bash-native
  local p="$1" out cur dir base key cached n=0 target
  case "$p" in
    /*) cur="$p" ;;
    *) cur=$(cd -- "$(dirname -- "$p")" 2>/dev/null && pwd -P) || { printf '%s\n' "$p"; return 0; }
       cur="$cur/$(basename -- "$p")" ;;
  esac
  while [ -L "$cur" ] && [ "$n" -lt 40 ]; do
    target=$(readlink -- "$cur") || break
    case "$target" in /*) cur="$target" ;; *) cur="$(dirname -- "$cur")/$target" ;; esac
    n=$((n + 1))
  done
  dir=${cur%/*}; [ -n "$dir" ] || dir=/  # candidates are absolute; no fork
  base=${cur##*/}
  # eval-global keys must be valid identifiers: escape specials bash-natively;
  # @ appears in node_modules/@scope paths — unescaped it is a bad substitution
  key="${dir//_/__}"; key="${key//\//_S}"; key="${key//./_D}"; key="${key// /_P}"; key="${key//-/_M}"
  key="${key//@/_AT}"; key="${key//[^A-Za-z0-9_]/_Q}" # _Q catch-all, same trade-off as whatis_desc
  eval "cached=\"\${DIRC_$key+x}\""
  if [ -n "${cached:-}" ]; then
    eval "out=\"\${DIRC_$key}\""
  else
    out=$(cd -- "$dir" 2>/dev/null && pwd -P) || { printf '%s\n' "$p"; return 0; }
    eval "DIRC_$key=\$out"
  fi
  printf '%s\n' "$out/$base"
}

is_system_path() { # <abs-path>; darwin-only SIP prefixes (see provenance.md)
  is_darwin || return 1
  local p pre prefixes="${BUTLER_SYSTEM_PREFIXES:-/usr/bin /bin /sbin /usr/sbin}"
  prefixes=$(printf '%s' "$prefixes" | tr ':' ' ')
  p=$(realpath_safe "$1")
  for pre in $prefixes; do
    case "$p" in "$pre"|"$pre"/*) return 0 ;; esac
  done
  return 1
}

kv_field() { # <k> <v> -> sanitized "k=v" + trailing TAB (values must never break TSV parsing)
  local v
  v=$(printf '%s' "${2-}" | tr '\t\r\n' '   ')
  printf '%s=%s\t' "$1" "$v"
}

du_size() { # <path> -> bytes (follows symlinks); dirs via du -sk; missing -> "-"
  local p="$1" s="-"
  if [ -f "$p" ]; then
    # group-level 2>/dev/null: an unopenable file (setuid binary under a sandbox)
    # makes the SHELL report the failed < redirect, which wc's own 2> misses
    s=$( { wc -c < "$p"; } 2>/dev/null) && s=${s//[[:space:]]/} || s="-"
  elif [ -d "$p" ]; then
    s=$(du -sk "$p" 2>/dev/null) && s=$(( ${s%%[[:space:]]*} * 1024 )) || s="-"
  fi
  [ -n "$s" ] || s="-"
  printf '%s' "$s"
}

hist_last_used() { # <name> -> max epoch from zsh-style history, or empty
  local f="${BUTLER_HIST_FILE:-${HISTFILE:-$HOME/.zsh_history}}" e
  [ -f "$f" ] || return 0
  # zsh extended format: ": <epoch>:0;cmd" (epoch 0 = no timestamp, skipped)
  e=$(LC_ALL=C awk -F':|;' -v n="$1" '{
    e=$2 + 0
    if (e > 0) { line=$0; sub(/^[^;]*;/, "", line)
      if (line ~ "(^|[ /])" n "( |$)" && e > m) m=e }
  } END { if (m) print m }' "$f")
  printf '%s' "${e:-}"
}

# journal.tsv lines: name<TAB>channel<TAB>installed_at_epoch<TAB>source<TAB>note
journal_get() { [ -f "$JOURNAL" ] && awk -F'\t' -v n="$1" '$1==n' "$JOURNAL" || true; }
journal_del() { [ -f "$JOURNAL" ] || return 0; local tmp; tmp=$(mktemp); awk -F'\t' -v n="$1" '$1!=n' "$JOURNAL" >"$tmp" && mv "$tmp" "$JOURNAL"; }
journal_add() { # name channel epoch source note
  mkdir -p "$JOURNAL_DIR"
  printf '%s\t%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" "${5:-}" >>"$JOURNAL"
}
