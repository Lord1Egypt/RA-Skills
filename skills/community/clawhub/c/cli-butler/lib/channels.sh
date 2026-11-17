#!/usr/bin/env bash
# shellcheck disable=SC1091,SC2016,SC2153  # sibling-source vars; dpkg -f fmt & word-split name list stay literal
# cli-butler channel library: per-channel enumerate/describe/route + ownership resolution.
# Enumerations and prefixes are cached per-run in eval-globals (bash 3.2: no assoc arrays).
# shellcheck disable=SC2034  # ENUM_*/CASK_*/PFX_* globals are built via eval indirection

. "$(dirname "${BASH_SOURCE[0]}")/common.sh"

# map channel id -> probe/query binary
channel_bin() {
  case "$1" in
    brew) printf 'brew\n' ;;
    npm) printf 'npm\n' ;;
    pnpm) printf 'pnpm\n' ;;
    pipx) printf 'pipx\n' ;;
    uv) printf 'uv\n' ;;
    cargo) printf 'cargo\n' ;;
    gem) printf 'gem\n' ;;
    apt) printf 'dpkg-query\n' ;;
    *) return 1 ;;
  esac
}

channel_available() {
  local b
  b=$(channel_bin "$1") || return 1
  have "$b"
}

# --- per-channel probes: emit "name<TAB>version" lines ---

_enum_namever() { # whitespace "name version" lines (strip tree glyph prefixes, C locale byte-wise)
  LC_ALL=C awk '{ v=$NF; $NF=""; line=$0
    sub(/^[^A-Za-z@\/]*/, "", line); sub(/ +$/, "", line)
    if (v != "" && line != "") printf "%s\t%s\n", line, v }'
}

_probe_brew() {
  local f c
  f=$(probe 15 brew list --versions)
  c=$(probe 15 brew list --cask --versions)
  printf '%s\n%s\n' "$f" "$c" | LC_ALL=C awk 'NF >= 2 { printf "%s\t%s\n", $1, $2 }'
}

_probe_npm() {
  probe 20 npm ls -g --depth=0 | LC_ALL=C awk '{
    line=$0; sub(/^[^A-Za-z@\/]*/, "", line)
    if (match(line, /@[^@]*$/)) {
      name=substr(line, 1, RSTART - 1); v=substr(line, RSTART + 1)
      if (name != "npm" && name != "" && v ~ /^[0-9]/) printf "%s\t%s\n", name, v } }'
}

_probe_pnpm() { probe 20 pnpm ls -g --depth=0 | _enum_namever; }

_probe_pipx() { probe 15 pipx list --short | grep -v '^nothing has been installed' | _enum_namever; }

_probe_uv() { probe 15 uv tool list | _enum_namever; }

_probe_cargo() { probe 15 cargo install --list | LC_ALL=C awk 'NF >= 2 {
  v=$2; sub(/^v/, "", v); sub(/:$/, "", v); printf "%s\t%s\n", $1, v }'; }

_probe_gem() { probe 15 gem list | LC_ALL=C sed -E 's/^(.*) \(([0-9][^)]*)\)$/\1\t\2/'; }

_probe_apt() { probe 15 dpkg-query -W -f='${db:Status-Abbrev}|${binary:Package}|${Version}\n' \
    | LC_ALL=C awk -F'|' '$1 ~ /^ii/ { name=$1; sub(/^i+ */, "", name)
      if (name != "") printf "%s\t%s\n", name, $2 }'; }

channel_enumerate() { # <id> -> "name<TAB>version" lines; cached per-run
  local id="$1" out
  case "$id" in brew|npm|pnpm|pipx|uv|cargo|gem|apt) ;; *) return 1 ;; esac
  eval "out=\"\${ENUM_$id:-}\""
  if [ -z "$out" ]; then
    channel_available "$id" || return 1
    out=$("_probe_$id")
    eval "ENUM_$id=\$out"
  fi
  [ -n "$out" ] && printf '%s\n' "$out"
  return 0
}

_is_cask() { # <name> -> true if brew cask (direct probe; route ops are rare)
  channel_available brew || return 1
  probe 15 brew list --cask --versions 2>/dev/null \
    | LC_ALL=C awk -v n="$1" 'NF >= 2 && $1==n{f=1} END{exit !f}'
}

channel_desc() { # <id> <name> -> one-line description via stdout, "" if unknown.
  # Local queries only (no network). Reads the bulk desc cache DESC_ALL_brew
  # warmed in the main shell by channel_desc_bulk.
  local id="$1" name="$2" d="" root all
  case "$id" in
    brew)
      eval "all=\"\${DESC_ALL_brew:-}\""
      if [ -n "$all" ]; then
        # bulk format "name: desc"; no regex so names stay literal
        d=$(printf '%s\n' "$all" | LC_ALL=C awk -v n="$name" '
          index($0, n ": ") == 1 && length($0) > length(n) + 2 { print substr($0, length(n) + 3); exit }')
      else
        d=$(probe 10 brew desc "$name" 2>/dev/null | sed -n 's/^[^:]*:[[:space:]]*//p' | head -1)
      fi ;;
    npm|pnpm)
      out=$(channel_prefixes "$id") || out=""
      if [ -n "$out" ]; then
        if [ "$id" = npm ]; then root="$out/lib/node_modules"; else root="${out##* }"; fi
        d=$(sed -n 's/.*"description"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
          "$root/$name/package.json" 2>/dev/null | head -1)
      fi ;;
    gem) d=$(probe 10 gem specification "$name" description 2>/dev/null | head -1) ;;
    apt) d=$(probe 10 dpkg-query -W -f='${Summary}\n' "$name" 2>/dev/null | head -1) ;;
  esac
  # whatis fallback lives in the caller (main shell) so the whatis budget and
  # name cache survive across rows; channel_desc just prints its own sources
  printf '%s' "$d"
}

# One-shot desc prefetch per channel (main shell). brew desc per-name costs
# ~1s on real installs (150+ rows -> minutes); one bulk call returns all.
channel_desc_bulk() { # <id>: fills DESC_ALL_<id>, "" on skip/failure
  local id="$1" enum names out
  eval "DESC_ALL_$id=\"\""
  [ "$id" = "brew" ] || return 0
  eval "enum=\"\${ENUM_brew:-}\""
  [ -n "$enum" ] || return 0
  names=$(printf '%s\n' "$enum" | awk -F'\t' '{ printf "%s ", $1 }')
  [ -n "$names" ] || return 0
  # shellcheck disable=SC2086  # space-joined name list
  out=$(probe 120 brew desc $names 2>/dev/null)
  eval "DESC_ALL_brew=\$out"
}

channel_prefixes() { # <id> -> space-separated install prefixes for realpath ownership
  # Cache sentinel must be +x (set vs unset), NOT :-MISSING: a failed probe
  # caches "" and :- treats empty as unset, re-probing on every call.
  local id="$1" out p cached
  eval "cached=\"\${PFX_$id+x}\""
  if [ -z "$cached" ]; then
    case "$id" in
      brew) out="/opt/homebrew /usr/local/Cellar /usr/local/Caskroom" ;;
      npm) out=$(probe 10 npm prefix -g 2>/dev/null) ;;
      pnpm) p=$(probe 10 pnpm root -g 2>/dev/null) && out="$(dirname "$p") $p" || out="" ;;
      pipx) out="${PIPX_HOME:-$HOME/.local/pipx}/venvs" ;;
      uv) p=$(probe 10 uv tool dir 2>/dev/null) && out="$p" || out="" ;;
      cargo) out="$HOME/.cargo/bin" ;;
      *) out="" ;;
    esac
    # ~/.local/bin is a SHARED shim dir (pipx, uv tools, uv itself, strays):
    # claim it only when the channel manages something, else an empty pipx
    # misroutes every stray there to `pipx uninstall` (observed on real machine)
    case "$id" in
      pipx|uv)
        eval "enum=\"\${ENUM_$id:-}\""
        [ -n "$enum" ] && out="$out $HOME/.local/bin" ;;
    esac
    eval "PFX_$id=\$out"
  else
    eval "out=\"\${PFX_$id}\""
  fi
  printf '%s\n' "$out"
}

_resolve_owner_ret() { # <name> <path> -> sets OWNER="channel|category"; order per provenance.md
  # must run in the caller's shell: channel/prefix caches live in shell vars
  local name="$1" path="$2" rp id pre pre_list pair out ch
  OWNER=""
  rp=$(realpath_safe "$path")
  # rule1: channel install prefixes (PFX_$id eval-cached; no per-call forks)
  for id in brew npm pnpm pipx uv cargo; do
    channel_prefixes "$id" >/dev/null 2>&1 || continue
    eval "pre_list=\${PFX_$id:-}"
    for pre in $pre_list; do
      [ -n "$pre" ] || continue
      case "$rp" in "$pre"|"$pre"/*) OWNER="$id|managed"; return 0 ;; esac
    done
  done
  if is_system_path "$rp"; then OWNER="system|system"; return 0; fi
  if have dpkg-query && out=$(probe 10 dpkg-query -S "$rp" 2>/dev/null) && [ -n "$out" ]; then
    OWNER="apt|managed"; return 0
  fi
  # rule3: caller-built name->channel index avoids re-enumerating per candidate
  if [ -n "${OWNED_INDEX+x}" ]; then
    ch=$(printf '%s\n' "$OWNED_INDEX" | LC_ALL=C awk -F'\t' -v n="$name" '$1==n{print $2; exit}')
    [ -n "$ch" ] && { OWNER="$ch|managed"; return 0; }
  else
    for pair in $CHANNELS; do
      id="${pair%%:*}"
      channel_enumerate "$id" >/dev/null 2>&1 || continue
      eval "out=\"\${ENUM_$id:-}\""
      [ -n "$out" ] || continue
      printf '%s\n' "$out" | LC_ALL=C awk -F'\t' -v n="$name" '$1==n{f=1} END{exit !f}' || continue
      OWNER="$id|managed"; return 0
    done
  fi
  # rule4: journal (JNAMES_CACHE = prewarmed name list; empty cache skips grep)
  if [ -n "${JNAMES_CACHE+x}" ]; then
    # zero-fork exact match (names are LF-delimited)
    if [ -n "$JNAMES_CACHE" ] && case "$LF$JNAMES_CACHE$LF" in *"$LF$name$LF"*) true ;; *) false ;; esac; then
      OWNER="manual|manual"; return 0
    fi
  elif [ -n "$(journal_get "$name")" ]; then
    OWNER="manual|manual"; return 0
  fi
  OWNER="manual|untracked"; return 0
}

resolve_owner() { # <name> <path> -> prints "channel|category" (also sets OWNER)
  _resolve_owner_ret "$@"
  printf '%s\n' "$OWNER"
}

# --- route builders: emit command strings, never execute ---

_route_flags() { # brew cask flag helper
  channel_enumerate brew >/dev/null 2>&1
  if _is_cask "$2"; then printf -- '--cask '; fi
}

channel_uninstall_cmd() { # <id> <name> -> full command string
  local id="$1" name="$2" f
  case "$id" in
    brew) f=$(_route_flags "$id" "$name"); printf 'brew uninstall %s%s\n' "$f" "$name" ;;
    npm) printf 'npm uninstall -g %s\n' "$name" ;;
    pnpm) printf 'pnpm remove -g %s\n' "$name" ;;
    pipx) printf 'pipx uninstall %s\n' "$name" ;;
    uv) printf 'uv tool uninstall %s\n' "$name" ;;
    cargo) printf 'cargo uninstall %s\n' "$name" ;;
    gem) printf 'gem uninstall %s\n' "$name" ;;
    apt) printf 'apt-get remove -y %s\n' "$name" ;;
    *) return 1 ;;
  esac
}

channel_upgrade_cmd() {
  local id="$1" name="$2" f
  case "$id" in
    brew) f=$(_route_flags "$id" "$name"); printf 'brew upgrade %s%s\n' "$f" "$name" ;;
    npm) printf 'npm install -g %s@latest\n' "$name" ;;
    pnpm) printf 'pnpm update -g %s\n' "$name" ;;
    pipx) printf 'pipx upgrade %s\n' "$name" ;;
    uv) printf 'uv tool upgrade %s\n' "$name" ;;
    cargo) printf 'cargo install %s\n' "$name" ;;
    gem) printf 'gem update %s\n' "$name" ;;
    apt) printf 'apt-get install -y %s\n' "$name" ;;
    *) return 1 ;;
  esac
}

channel_install_cmd() {
  local id="$1" name="$2" f
  case "$id" in
    brew) f=$(_route_flags "$id" "$name"); printf 'brew install %s%s\n' "$f" "$name" ;;
    npm) printf 'npm install -g %s\n' "$name" ;;
    pnpm) printf 'pnpm add -g %s\n' "$name" ;;
    pipx) printf 'pipx install %s\n' "$name" ;;
    uv) printf 'uv tool install %s\n' "$name" ;;
    cargo) printf 'cargo install %s\n' "$name" ;;
    gem) printf 'gem install %s\n' "$name" ;;
    apt) printf 'apt-get install -y %s\n' "$name" ;;
    *) return 1 ;;
  esac
}
