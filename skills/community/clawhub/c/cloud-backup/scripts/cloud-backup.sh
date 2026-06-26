#!/usr/bin/env bash
# OpenClaw Cloud Backup v2 — the cloud layer for OpenClaw's native backup.
# Wraps `openclaw backup create` (consistent SQLite snapshots, manifest, multi-dir
# coverage), then GPG-encrypts, uploads to S3-compatible storage, applies
# retention, and verifies. Staged restores; strictly opt-in scheduling.
#
# Config: skills.entries.cloud-backup.config.* in openclaw.json (non-secret only).
# Credentials: AWS named profile / process env / passphrase file — see
# references/credentials.md. Plaintext skills.entries.cloud-backup.env.* from v1
# still works but is DEPRECATED and warns on every run.
set -uo pipefail

VERSION="2.0.1"

# --- locations ---------------------------------------------------------------
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
CONFIG_FILE="${OPENCLAW_CONFIG:-${OPENCLAW_CONFIG_PATH:-$STATE_DIR/openclaw.json}}"
LEGACY_BACKUPS="$STATE_DIR/backups"   # v1 local store (inside state dir — recursion hazard)
MAX_LOCAL=7                           # hard cap on local archive sets per mode

# --- exit codes (documented in SKILL.md; cron agents key off these) ----------
E_OK=0; E_WARN=3; E_USAGE=4
E_LOCK=10; E_DEPS=11; E_DISK=12; E_CLOUD=13; E_PASSPHRASE=14
E_CREATE=20; E_FILTER=21; E_ENCRYPT=22; E_UPLOAD=23; E_REMOTE_VERIFY=24; E_VERIFY=25
E_RESTORE=30

# --- lean excludes (state-dir-relative globs; ** crosses /, * does not) ------
# Junk that bloats archives without restoration value. config.exclude appends,
# config.include carves out, --everything drops all but the non-negotiables.
DEFAULT_EXCLUDES=(
  "agents/*/agent/codex-home/logs_*.sqlite*"
  "agents/*/agent/codex-home/cache/**"
  "agents/*/agent/codex-home/skills/**"
  "agents/*/agent/codex-home/.tmp/**"
  "agents/*/agent/codex-home/models_cache.json"
  "agents/*/agent/codex-home/sessions/**"
  "agents/*/sessions/**"
  "archive/**"
  "tools/**"
  "media/**"
  "logs/**"
  "cache/**"
  ".cache/**"
  "npm/**"
  "tmp/**"
  "completions/**"
  "openclaw.json.bak*"
  "openclaw.json.clobbered*"
  "*.bak"
  "*.bak.*"
  "**/*.bak"
  "**/*.bak.*"
  "migration-backup-*/**"
)
# Enforced even with --everything: never swallow archives into archives.
NONNEGOTIABLE_EXCLUDES=("backups/**")

# --- output helpers -----------------------------------------------------------
info() { if [ "${JSON_OUT:-false}" = "true" ]; then echo ":: $*" >&2; else echo ":: $*"; fi; }
warn() { echo "WARN: $*" >&2; WARNINGS+=("$*"); }
err()  { echo "ERROR: $*" >&2; }
fail() { local code="$1"; shift; err "$*"; exit "$code"; }
die()  { fail "$E_USAGE" "$@"; }
has()  { command -v "$1" >/dev/null 2>&1; }
need() { local b; for b in "$@"; do has "$b" || fail "$E_DEPS" "missing dependency: $b"; done; }

WARNINGS=()
JSON_OUT=false

# shellcheck disable=SC2088  # matching literal tildes from config values on purpose
expand_path() { case "$1" in "~") echo "$HOME" ;; "~/"*) echo "$HOME/${1#\~/}" ;; *) echo "$1" ;; esac; }

as_uint() { # $1 value $2 default — sanitize numeric config values
  case "${1:-}" in
    ''|*[!0-9]*) echo "$2" ;;
    *) echo "$1" ;;
  esac
}

# --- config -------------------------------------------------------------------
cfg() { # cfg <config|env> <key>
  has jq && [ -f "$CONFIG_FILE" ] || return 0
  jq -r ".skills.entries[\"cloud-backup\"].$1.$2 | if . == null then empty else tostring end" \
    "$CONFIG_FILE" 2>/dev/null || true
}
cfg_array() { # cfg_array <key> — newline-separated config.<key>[] entries
  has jq && [ -f "$CONFIG_FILE" ] || return 0
  jq -r ".skills.entries[\"cloud-backup\"].config.$1 // [] | .[]" "$CONFIG_FILE" 2>/dev/null || true
}

load_config() {
  BUCKET="$(cfg config bucket)"
  REGION="$(cfg config region)";         REGION="${REGION:-us-east-1}"
  ENDPOINT="$(cfg config endpoint)"
  UPLOAD="$(cfg config upload)";         UPLOAD="${UPLOAD:-true}"
  ENCRYPT="$(cfg config encrypt)";       ENCRYPT="${ENCRYPT:-true}"   # v2 default: true
  KEEP="$(as_uint "$(cfg config retentionCount)" 10)"
  DAYS="$(as_uint "$(cfg config retentionDays)" 30)"
  LOCAL_COUNT="$(as_uint "$(cfg config localCount)" 3)"
  [ "$LOCAL_COUNT" -gt "$MAX_LOCAL" ] && LOCAL_COUNT=$MAX_LOCAL

  LOCAL_DIR="$(cfg config localDir)"
  LOCAL_DIR="$(expand_path "${LOCAL_DIR:-$HOME/.local/share/openclaw-backups}")"
  case "$LOCAL_DIR" in
    "$STATE_DIR"/*|"$STATE_DIR") die "config.localDir must live outside the OpenClaw state dir ($STATE_DIR)" ;;
  esac

  PREFIX="$(cfg config prefix)"
  if [ -z "$PREFIX" ]; then
    PREFIX="openclaw-backups/$(hostname -s 2>/dev/null || hostname)/"
  fi
  case "$PREFIX" in */) ;; *) PREFIX="$PREFIX/" ;; esac

  PASSFILE="$(cfg config passphraseFile)"; PASSFILE="$(expand_path "$PASSFILE")"
  EXCLUDE_SECRETS="$(cfg config excludeSecrets)"; EXCLUDE_SECRETS="${EXCLUDE_SECRETS:-false}"
  EVERYTHING_CFG="$(cfg config everything)"; EVERYTHING_CFG="${EVERYTHING_CFG:-false}"
  VERIFY_AFTER="$(cfg config verifyAfterBackup)"; VERIFY_AFTER="${VERIFY_AFTER:-quick}"

  # S3 credentials. Precedence: process env > profile (recommended) > DEPRECATED
  # v1 plaintext config. Source is tracked for `status` and deprecation warnings.
  local orig_ak="${AWS_ACCESS_KEY_ID:-}" orig_sk="${AWS_SECRET_ACCESS_KEY:-}"
  DEP_S3=false; DEP_GPG=false
  if [ -n "$(cfg env ACCESS_KEY_ID)" ] || [ -n "$(cfg env SECRET_ACCESS_KEY)" ]; then DEP_S3=true; fi
  if [ -n "$(cfg env GPG_PASSPHRASE)" ]; then DEP_GPG=true; fi
  # OpenClaw secret-store refs (between process env and profile in precedence).
  # A configured-but-unresolvable ref is an error, never a silent fallthrough.
  S3_REF_ERROR=""
  local ref_ak ref_sk ref_st akj skj stj
  akj="$(cfg_ref accessKeyRef)"; skj="$(cfg_ref secretKeyRef)"; stj="$(cfg_ref sessionTokenRef)"
  if { [ -z "$orig_ak" ] || [ -z "$orig_sk" ]; } && { [ -n "$akj" ] || [ -n "$skj" ]; }; then
    if [ -n "$akj" ] && [ -n "$skj" ]; then
      if ref_ak="$(resolve_secret_ref "$akj")" && ref_sk="$(resolve_secret_ref "$skj")"; then
        AWS_ACCESS_KEY_ID="$ref_ak"; AWS_SECRET_ACCESS_KEY="$ref_sk"
        if [ -n "$stj" ]; then
          ref_st="$(resolve_secret_ref "$stj")" && AWS_SESSION_TOKEN="$ref_st"
        fi
        S3_REF_SOURCE=true
      else
        S3_REF_ERROR="config.accessKeyRef/secretKeyRef configured but unresolvable"
      fi
    else
      S3_REF_ERROR="configure BOTH config.accessKeyRef and config.secretKeyRef (only one is set)"
    fi
  fi

  : "${AWS_ACCESS_KEY_ID:=$(cfg env ACCESS_KEY_ID)}"
  : "${AWS_SECRET_ACCESS_KEY:=$(cfg env SECRET_ACCESS_KEY)}"
  : "${AWS_SESSION_TOKEN:=$(cfg env SESSION_TOKEN)}"
  : "${AWS_PROFILE:=$(cfg config profile)}"
  export AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN

  S3_SOURCE="not configured"
  if [ -n "$orig_ak" ] && [ -n "$orig_sk" ]; then S3_SOURCE="process env (operator-managed)"
  elif [ "${S3_REF_SOURCE:-false}" = "true" ]; then S3_SOURCE="OpenClaw secret refs (config.accessKeyRef/secretKeyRef)"
  elif [ -n "$S3_REF_ERROR" ]; then S3_SOURCE="secret refs UNRESOLVABLE: $S3_REF_ERROR"
  elif [ -n "$AWS_PROFILE" ]; then S3_SOURCE="aws profile '$AWS_PROFILE'"
  elif [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; then S3_SOURCE="PLAINTEXT in openclaw.json (DEPRECATED)"
  fi

  PARTIAL_KEYS=false
  if { [ -n "$AWS_ACCESS_KEY_ID" ] && [ -z "$AWS_SECRET_ACCESS_KEY" ]; } || \
     { [ -z "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; }; then
    PARTIAL_KEYS=true
  fi

  CLOUD=false
  if [ "$PARTIAL_KEYS" != "true" ] && [ -n "$BUCKET" ] && has aws && \
     { [ -n "$AWS_PROFILE" ] || { [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; }; }; then
    CLOUD=true
  fi
  # Broken refs are an error state, not a fallthrough to weaker tiers.
  [ -n "$S3_REF_ERROR" ] && CLOUD=false

  mkdir -p "$LOCAL_DIR/.staging"
  chmod 700 "$LOCAL_DIR" 2>/dev/null || true
}

print_deprecations() {
  if [ "$DEP_S3" = "true" ]; then
    {
      echo "WARN: DEPRECATED: S3 credentials found in plaintext in openclaw.json"
      echo "WARN:   (skills.entries.cloud-backup.env.ACCESS_KEY_ID / SECRET_ACCESS_KEY)."
      echo "WARN:   Your backups archive openclaw.json — every archive carries these keys."
      echo "WARN:   Migrate: aws configure --profile openclaw-backup; then"
      echo "WARN:     openclaw config patch 'skills.entries.cloud-backup.config.profile=\"openclaw-backup\"'"
      echo "WARN:     and remove skills.entries.cloud-backup.env.* (see references/credentials.md)."
      echo "WARN:   This fallback is removed in v3."
    } >&2
    WARNINGS+=("DEPRECATED: plaintext S3 credentials in openclaw.json")
  fi
  if [ "$DEP_GPG" = "true" ]; then
    {
      echo "WARN: DEPRECATED: GPG passphrase found in plaintext in openclaw.json"
      echo "WARN:   (skills.entries.cloud-backup.env.GPG_PASSPHRASE). Migrate to a passphrase file:"
      echo "WARN:     umask 077 && openssl rand -base64 32 > ~/.openclaw/credentials/cloud-backup.passphrase"
      echo "WARN:     openclaw config patch 'skills.entries.cloud-backup.config.passphraseFile=\"~/.openclaw/credentials/cloud-backup.passphrase\"'"
      echo "WARN:   (Keep the OLD passphrase somewhere safe — older archives still need it.)"
      echo "WARN:   This fallback is removed in v3."
    } >&2
    WARNINGS+=("DEPRECATED: plaintext GPG passphrase in openclaw.json")
  fi
}

# --- OpenClaw secret-store integration (config.*Ref keys) ----------------------
# The skill can consume the INSTANCE's secret storage instead of separate files:
# config.accessKeyRef / secretKeyRef / sessionTokenRef / passphraseRef accept
# OpenClaw SecretRef objects ({source: env|file|exec, provider, id}) or
# $NAME / ${NAME} env templates, resolved against .secrets.providers in
# openclaw.json with the same semantics the gateway uses (file providers:
# JSON-pointer ids by default; exec providers: protocolVersion-1 stdin/stdout).

cfg_ref() { # $1 key → compact JSON of config.<key> (object or string), empty if absent
  has jq && [ -f "$CONFIG_FILE" ] || return 0
  jq -c ".skills.entries[\"cloud-backup\"].config.$1 // empty" "$CONFIG_FILE" 2>/dev/null || true
}

resolve_secret_ref() { # $1 = compact JSON (SecretRef object or string); echoes value
  local input="$1" t
  t="$(jq -r 'type' <<<"$input" 2>/dev/null)" || { err "invalid secret ref"; return 1; }

  if [ "$t" = "string" ]; then
    local s n
    s="$(jq -r . <<<"$input")"
    case "$s" in
      '${'*'}') n="${s:2}"; n="${n%\}}" ;;
      '$'*)     n="${s#\$}" ;;
      *)
        # Literal secret in a *Ref key: works, but it is plaintext in config —
        # the sensitivity verdict will flag it. Prefer a real ref.
        printf '%s' "$s"; return 0 ;;
    esac
    [ -n "${!n:-}" ] || { err "env var \$$n (from secret ref) is unset"; return 1; }
    printf '%s' "${!n}"
    return 0
  fi

  [ "$t" = "object" ] || { err "secret ref must be an object or string"; return 1; }
  local source provider id pconf
  source="$(jq -r '.source // empty' <<<"$input")"
  provider="$(jq -r '.provider // "default"' <<<"$input")"
  id="$(jq -r '.id // empty' <<<"$input")"
  if [ -z "$source" ] || [ -z "$id" ]; then
    err "secret ref needs source and id"; return 1
  fi

  case "$source" in
    env)
      [ -n "${!id:-}" ] || { err "env var \$$id (secret ref, provider '$provider') is unset"; return 1; }
      printf '%s' "${!id}"
      ;;
    file)
      pconf="$(jq -c --arg p "$provider" '.secrets.providers[$p] // empty' "$CONFIG_FILE" 2>/dev/null)"
      [ -n "$pconf" ] || { err "secret provider '$provider' is not configured (.secrets.providers)"; return 1; }
      local fpath fmode v
      fpath="$(expand_path "$(jq -r '.path // empty' <<<"$pconf")")"
      fmode="$(jq -r '.mode // "json"' <<<"$pconf")"
      [ -f "$fpath" ] || { err "secret store file not found: $fpath"; return 1; }
      if [ "$fmode" = "singleValue" ]; then
        v="$(cat "$fpath")"
        [ -n "$v" ] || { err "secret store file is empty: $fpath"; return 1; }
        printf '%s' "$v"
      else
        # id is a JSON pointer (e.g. /cloudBackup/gpgPassphrase); unescape ~1 → / and ~0 → ~
        v="$(jq -er --arg ptr "$id" \
          'getpath($ptr | ltrimstr("/") | split("/") | map(gsub("~1"; "/") | gsub("~0"; "~"))) | select(type == "string")' \
          "$fpath" 2>/dev/null)" \
          || { err "pointer '$id' not found (or not a string) in $fpath"; return 1; }
        printf '%s' "$v"
      fi
      ;;
    exec)
      pconf="$(jq -c --arg p "$provider" '.secrets.providers[$p] // empty' "$CONFIG_FILE" 2>/dev/null)"
      [ -n "$pconf" ] || { err "secret provider '$provider' is not configured (.secrets.providers)"; return 1; }
      if jq -e '.pluginIntegration' <<<"$pconf" >/dev/null 2>&1; then
        err "exec provider '$provider' uses a plugin integration — only resolvable inside the gateway runtime"
        return 1
      fi
      local cmd jsononly out v
      cmd="$(jq -r '.command // empty' <<<"$pconf")"
      [ -n "$cmd" ] || { err "exec provider '$provider' has no command"; return 1; }
      jsononly="$(jq -r 'if .jsonOnly == false then "false" else "true" end' <<<"$pconf")"
      local -a args=()
      while IFS= read -r a; do args+=("$a"); done < <(jq -r '.args // [] | .[]' <<<"$pconf")
      out="$(jq -nc --arg p "$provider" --arg id "$id" '{protocolVersion: 1, provider: $p, ids: [$id]}' \
        | "$cmd" "${args[@]}")" || { err "exec provider '$provider' ($cmd) failed"; return 1; }
      if v="$(jq -er --arg id "$id" 'select(.protocolVersion == 1) | .values[$id] | select(type == "string")' <<<"$out" 2>/dev/null)"; then
        printf '%s' "$v"
      elif [ "$jsononly" = "false" ] && [ -n "$out" ]; then
        printf '%s' "$out"   # raw single-value response (jsonOnly: false)
      else
        err "exec provider '$provider' returned no value for id '$id'"; return 1
      fi
      ;;
    *)
      err "unsupported secret ref source: $source"; return 1
      ;;
  esac
}

# --- passphrase ---------------------------------------------------------------
# Resolution: GPG_PASSPHRASE env > CLOUD_BACKUP_GPG_PASSPHRASE env (OpenClaw
# secret-ref via skill apiKey/primaryEnv) > config.passphraseFile > DEPRECATED
# v1 plaintext config. The passphrase NEVER appears on a command line.
PASSPHRASE=""
PASS_SOURCE="not configured"
PASS_ERROR=""
resolve_passphrase() { # [$1=soft] — soft mode reports broken refs instead of exiting
  if [ -n "${GPG_PASSPHRASE:-}" ]; then
    PASSPHRASE="$GPG_PASSPHRASE"; PASS_SOURCE="env GPG_PASSPHRASE (operator-managed)"; return 0
  fi
  if [ -n "${CLOUD_BACKUP_GPG_PASSPHRASE:-}" ]; then
    PASSPHRASE="$CLOUD_BACKUP_GPG_PASSPHRASE"; PASS_SOURCE="env CLOUD_BACKUP_GPG_PASSPHRASE (OpenClaw apiKey ref)"; return 0
  fi
  local prefj
  prefj="$(cfg_ref passphraseRef)"
  if [ -n "$prefj" ]; then
    # Configured ref must resolve — never fall through to a weaker tier.
    if ! PASSPHRASE="$(resolve_secret_ref "$prefj")" || [ -z "$PASSPHRASE" ]; then
      PASS_ERROR="config.passphraseRef is configured but could not be resolved"
      [ "${1:-}" = "soft" ] && return 1
      fail "$E_PASSPHRASE" "$PASS_ERROR"
    fi
    PASS_SOURCE="OpenClaw secret ref (config.passphraseRef)"
    return 0
  fi
  if [ -n "$PASSFILE" ]; then
    local mode perm
    if [ ! -f "$PASSFILE" ]; then
      PASS_ERROR="passphrase file not found: $PASSFILE"
      [ "${1:-}" = "soft" ] && return 1
      fail "$E_PASSPHRASE" "$PASS_ERROR"
    fi
    mode="$(stat -c %a "$PASSFILE" 2>/dev/null || stat -f %Lp "$PASSFILE" 2>/dev/null || echo "")"
    if [ -n "$mode" ]; then
      perm=$(( 8#$mode ))
      if (( perm & 0007 )); then
        PASS_ERROR="passphrase file is world-readable — refusing. Fix: chmod 600 $PASSFILE"
        [ "${1:-}" = "soft" ] && return 1
        fail "$E_PASSPHRASE" "$PASS_ERROR"
      elif (( perm & 0070 )); then
        warn "passphrase file $PASSFILE has mode $mode; expected 600"
      fi
    fi
    PASSPHRASE="$(cat "$PASSFILE")"
    if [ -z "$PASSPHRASE" ]; then
      PASS_ERROR="passphrase file is empty: $PASSFILE"
      [ "${1:-}" = "soft" ] && return 1
      fail "$E_PASSPHRASE" "$PASS_ERROR"
    fi
    PASS_SOURCE="file $PASSFILE (mode ${mode:-?})"
    return 0
  fi
  local dep; dep="$(cfg env GPG_PASSPHRASE)"
  if [ -n "$dep" ]; then
    PASSPHRASE="$dep"; PASS_SOURCE="PLAINTEXT in openclaw.json (DEPRECATED)"; return 0
  fi
  return 1
}

gpg_enc_file() { # $1 in, $2 out — symmetric AES256, passphrase via fd (never argv)
  if [ -n "$PASSPHRASE" ]; then
    gpg --batch --yes --quiet --pinentry-mode loopback --passphrase-fd 3 \
      --symmetric --cipher-algo AES256 -o "$2" "$1" 3< <(printf '%s' "$PASSPHRASE")
  else
    gpg --yes --symmetric --cipher-algo AES256 -o "$2" "$1"
  fi
}
gpg_dec_stdout() { # $1 in (.gpg) → plaintext on stdout
  if [ -n "$PASSPHRASE" ]; then
    gpg --batch --yes --quiet --pinentry-mode loopback --passphrase-fd 3 \
      -d "$1" 3< <(printf '%s' "$PASSPHRASE")
  else
    gpg --quiet -d "$1"
  fi
}

# --- checksums / archive safety -------------------------------------------------
sha_cmd() { if has sha256sum; then echo sha256sum; elif has shasum; then echo "shasum -a 256"; else fail "$E_DEPS" "need sha256sum or shasum"; fi; }
sha_make()  { local d; d="$(dirname "$1")"; (cd "$d" && $(sha_cmd) "$(basename "$1")" > "$(basename "$1").sha256"); }
sha_check() { [ -f "$1.sha256" ] || return 2; local d; d="$(dirname "$1")"; (cd "$d" && $(sha_cmd) -c "$(basename "$1").sha256" >/dev/null 2>&1); }
sha_of()    { $(sha_cmd) "$1" | awk '{print $1}'; }

tar_safe_listing() { # reads a member listing on stdin; dies on traversal-hostile paths
  local bad
  bad="$(grep -E '^/|^\.\.(/|$)|/\.\.(/|$)' || true)"
  [ -z "$bad" ] || { echo "$bad" >&2; fail "$E_VERIFY" "unsafe paths in archive"; }
}

safe_rm() {
  local p
  for p in "$@"; do
    [ -n "$p" ] || continue
    [ "$p" != "/" ] || die "refusing to delete root path"
    rm -f "$p"
  done
}

# --- s3 -------------------------------------------------------------------------
s3() {
  local a=(aws)
  [ -n "${AWS_PROFILE:-}" ] && a+=(--profile "$AWS_PROFILE")
  [ -n "$REGION" ]   && a+=(--region "$REGION")
  [ -n "$ENDPOINT" ] && a+=(--endpoint-url "$ENDPOINT")
  "${a[@]}" s3 "$@"
}
s3api() {
  local a=(aws)
  [ -n "${AWS_PROFILE:-}" ] && a+=(--profile "$AWS_PROFILE")
  [ -n "$REGION" ]   && a+=(--region "$REGION")
  [ -n "$ENDPOINT" ] && a+=(--endpoint-url "$ENDPOINT")
  "${a[@]}" s3api "$@"
}

remote_keys() { # archive keys under the configured prefix, oldest first
  s3 ls "s3://$BUCKET/$PREFIX" --recursive 2>/dev/null \
    | awk '{print $4}' | grep -E '\.tar\.gz(\.gpg)?$' | sort || true
}

# --- staging / lock / sweep ------------------------------------------------------
STAGING=""
cleanup_staging() { [ -n "$STAGING" ] && rm -rf "$STAGING"; }

sweep_stale_staging() {
  local d pid
  for d in "$LOCAL_DIR/.staging"/run-*; do
    [ -d "$d" ] || continue
    pid="${d##*-}"
    if [[ "$pid" =~ ^[0-9]+$ ]] && kill -0 "$pid" 2>/dev/null; then
      # owner still alive; reap anyway if older than a day (pid reuse)
      [ -n "$(find "$d" -maxdepth 0 -mmin +1440 2>/dev/null)" ] || continue
    fi
    info "Sweeping stale staging dir: $d"
    rm -rf "$d"
  done
}

acquire_lock() {
  need flock
  exec 9>"$LOCAL_DIR/.lock" || fail "$E_LOCK" "cannot open lock file"
  flock -n 9 || fail "$E_LOCK" "another cloud-backup run holds the lock ($LOCAL_DIR/.lock)"
  printf '%s %s\n' "$$" "$(date -Is)" >&9 2>/dev/null || true
}

new_staging() {
  STAGING="$LOCAL_DIR/.staging/run-$(date +%Y%m%d%H%M%S)-$$"
  mkdir -m 700 "$STAGING" || fail "$E_DISK" "cannot create staging dir"
  trap 'cleanup_staging' EXIT INT TERM
}

# --- secrets-in-archive verdict ---------------------------------------------------
# refs-only      → archive carries SecretRef pointers, not secret material
# secret-material → archive would contain real secrets; encryption is mandatory
VERDICT="refs-only"
VERDICT_REASONS=()
SECRET_STORE_RELS=()  # state-relative paths of detected secret stores (for excludeSecrets)

secrets_verdict() {
  VERDICT="refs-only"; VERDICT_REASONS=(); SECRET_STORE_RELS=()
  local p rel f

  # 1. file-provider secret stores inside the archive scope
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    p="$(expand_path "$p")"
    case "$p" in
      "$STATE_DIR"/*)
        rel="${p#"$STATE_DIR"/}"
        VERDICT_REASONS+=("file-provider secret store in scope: $rel")
        SECRET_STORE_RELS+=("$rel") ;;
    esac
  done < <(jq -r '.secrets.providers // {} | to_entries[] | select(.value.source=="file") | .value.path // empty' "$CONFIG_FILE" 2>/dev/null || true)

  # 2. credentials directory
  if [ -d "$STATE_DIR/credentials" ] && [ -n "$(ls -A "$STATE_DIR/credentials" 2>/dev/null)" ]; then
    VERDICT_REASONS+=("credentials/ directory is non-empty")
    SECRET_STORE_RELS+=("credentials/**")
  fi

  # 3. legacy auth-profile remnants
  for f in "$STATE_DIR"/agents/*/agent/auth-profiles.json* "$STATE_DIR"/agents/*/agent/auth-state.json*; do
    [ -e "$f" ] || continue
    VERDICT_REASONS+=("legacy auth profile files under agents/*/agent/")
    SECRET_STORE_RELS+=("agents/*/agent/auth-profiles.json*" "agents/*/agent/auth-state.json*")
    break
  done

  # 4. plaintext secrets in openclaw.json (heuristic: secret-ish keys holding
  #    literal strings that are neither $ENV templates nor {source,...} refs)
  local n_plain
  n_plain="$(jq '[.. | objects | to_entries[]
      | select(.value | type == "string")
      | select(.key | test("(?i)(token|secret|password|passphrase|api[-_]?key|access[-_]?key)"))
      | select(.key | test("(?i)(file|path|dir)$") | not)
      | select(.value | test("^\\$") | not)
      | select(.value | length > 0)] | length' "$CONFIG_FILE" 2>/dev/null || echo 0)"
  local n_skill_env
  n_skill_env="$(jq '[.skills.entries // {} | to_entries[] | .value.env // {} | to_entries[]
      | select(.value | type == "string") | select(.value | length > 0)] | length' "$CONFIG_FILE" 2>/dev/null || echo 0)"
  if [ "${n_plain:-0}" -gt 0 ] 2>/dev/null || [ "${n_skill_env:-0}" -gt 0 ] 2>/dev/null; then
    VERDICT_REASONS+=("openclaw.json contains plaintext secret values (run: openclaw secrets audit)")
  fi

  [ ${#VERDICT_REASONS[@]} -gt 0 ] && VERDICT="secret-material"
}

# --- exclude matching ---------------------------------------------------------------
glob_to_ere() { # state-relative glob → anchored-fragment ERE (** crosses /, * does not)
  local g="$1" out="" i ch
  for ((i = 0; i < ${#g}; i++)); do
    ch="${g:i:1}"
    case "$ch" in
      '*')
        if [ "${g:i+1:1}" = "*" ]; then out+=".*"; i=$((i + 1)); else out+="[^/]*"; fi ;;
      '?') out+="[^/]" ;;
      '.' | '+' | '(' | ')' | '[' | ']' | '{' | '}' | '^' | '$' | '|' | '\\') out+="\\$ch" ;;
      *) out+="$ch" ;;
    esac
  done
  printf '%s\n' "$out"
}

active_excludes() { # echoes the effective exclude globs for this run
  local g
  if [ "$EVERYTHING" = "true" ]; then
    printf '%s\n' "${NONNEGOTIABLE_EXCLUDES[@]}"
  else
    printf '%s\n' "${NONNEGOTIABLE_EXCLUDES[@]}" "${DEFAULT_EXCLUDES[@]}"
    cfg_array exclude
  fi
  if [ "$EXCLUDE_SECRETS" = "true" ] && [ ${#SECRET_STORE_RELS[@]} -gt 0 ]; then
    printf '%s\n' "${SECRET_STORE_RELS[@]}"
  fi
}

# Rewrites $1 (a native-engine .tar.gz) in place, dropping file members under the
# state-dir payload prefix that match the active excludes. Directory entries are
# left in place (harmless empty dirs on restore; avoids GNU tar --delete
# directory-recursion ambiguity). Sets FILTERED_COUNT.
FILTERED_COUNT=0
apply_lean_filter() {
  local arc="$1"
  FILTERED_COUNT=0

  local members="$STAGING/members.txt" exf="$STAGING/ex.ere" inf="$STAGING/in.ere"
  local nonf="$STAGING/nonneg.ere" dl="$STAGING/delete.list"
  tar -tzf "$arc" > "$members" || return 1
  local root prefix
  root="$(head -n1 "$members" | cut -d/ -f1)"
  [ -n "$root" ] || return 1
  prefix="$root/payload/posix$STATE_DIR/"

  : > "$exf"; : > "$inf"; : > "$nonf"
  local g
  while IFS= read -r g; do
    [ -n "$g" ] || continue
    printf '^%s$\n' "$(glob_to_ere "$g")" >> "$exf"
  done < <(active_excludes)
  while IFS= read -r g; do
    [ -n "$g" ] || continue
    printf '^%s$\n' "$(glob_to_ere "$g")" >> "$inf"
  done < <([ "$EVERYTHING" = "true" ] || cfg_array include)
  for g in "${NONNEGOTIABLE_EXCLUDES[@]}"; do
    printf '^%s$\n' "$(glob_to_ere "$g")" >> "$nonf"
  done

  awk -v prefix="$prefix" -v exf="$exf" -v inf="$inf" -v nonf="$nonf" '
    BEGIN {
      ne = ni = nn = 0
      while ((getline l < exf)  > 0) ex[++ne]  = l; close(exf)
      while ((getline l < inf)  > 0) inc[++ni] = l; close(inf)
      while ((getline l < nonf) > 0) non[++nn] = l; close(nonf)
    }
    {
      if (index($0, prefix) != 1) next            # only state-dir payload members
      if (substr($0, length($0), 1) == "/") next  # files only; keep dir entries
      rel = substr($0, length(prefix) + 1)
      hit = 0
      for (i = 1; i <= ne; i++) if (rel ~ ex[i]) { hit = 1; break }
      if (hit) for (i = 1; i <= ni; i++) if (rel ~ inc[i]) { hit = 0; break }
      if (!hit) { for (i = 1; i <= nn; i++) if (rel ~ non[i]) { hit = 1; break } }
      if (hit) print $0
    }' "$members" > "$dl" || return 1

  FILTERED_COUNT="$(wc -l < "$dl" | tr -d ' ')"
  [ "$FILTERED_COUNT" -gt 0 ] || return 0

  # Pick a rewrite engine: GNU tar --delete works as a pure stream filter.
  local gnu=""
  if tar --version 2>/dev/null | grep -qi 'gnu tar'; then gnu=tar
  elif has gtar && gtar --version 2>/dev/null | grep -qi 'gnu tar'; then gnu=gtar; fi

  if [ -n "$gnu" ]; then
    # GNU tar --delete removes PAX long-name members correctly but mis-marks
    # them in its "found" bookkeeping, yielding spurious "Not found in archive"
    # errors and exit 2. Don't trust the exit code: require zcat/gzip success,
    # surface only non-spurious stderr, and prove correctness below by exact
    # entry count.
    gzip -dc "$arc" | "$gnu" --delete --no-wildcards --files-from="$dl" -f - 2>"$STAGING/delete.err" | gzip -c > "$arc.lean"
    local rcs=("${PIPESTATUS[@]}")
    grep -Ev 'Not found in archive|Exiting with failure status' "$STAGING/delete.err" >&2 || true
    if [ "${rcs[0]}" -ne 0 ] || [ "${rcs[2]}" -ne 0 ]; then
      rm -f "$arc.lean"; return 1
    fi
  elif has bsdtar; then
    # Best effort: bsdtar rewrites from @archive with -X exclusion file.
    if ! bsdtar -czf "$arc.lean" -X "$dl" @"$arc"; then
      rm -f "$arc.lean"; return 1
    fi
  else
    warn "no GNU tar (or gtar/bsdtar) available to filter the archive — keeping the unfiltered archive (install gnu-tar to enable lean backups)"
    FILTERED_COUNT=0
    return 0
  fi

  local expected actual
  expected=$(( $(wc -l < "$members") - FILTERED_COUNT ))
  actual="$(tar -tzf "$arc.lean" | wc -l | tr -d ' ')"
  if [ "$actual" -ne "$expected" ]; then
    err "filtered archive has $actual entries, expected $expected — keeping nothing"
    rm -f "$arc.lean"; return 1
  fi
  mv -f "$arc.lean" "$arc"
}

# --- archive production --------------------------------------------------------------
arc_name() { # $1 mode → openclaw_<mode>_<ts>_<host>.tar.gz
  local host; host="$(hostname -s 2>/dev/null || hostname)"
  echo "openclaw_${1}_$(date +%Y%m%d_%H%M%S)_${host//[^a-zA-Z0-9._-]/_}.tar.gz"
}
arc_ts()   { basename "$1" | sed -n 's/.*_\([0-9]\{8\}_[0-9]\{6\}\)_.*/\1/p' | tr -d _; }
arc_mode() { basename "$1" | sed -n 's/^openclaw_\([a-z]*\)_[0-9].*/\1/p'; }

write_skill_manifest() { # $1 mode → path of cloud-backup-manifest.json in staging
  local out="$STAGING/cloud-backup-manifest.json"
  jq -n --arg v "$VERSION" --arg mode "$1" --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --arg host "$(hostname -s 2>/dev/null || hostname)" --arg state "$STATE_DIR" \
    --argjson secretsExcluded "$([ "$EXCLUDE_SECRETS" = "true" ] && echo true || echo false)" \
    '{schema: 2, skill: "cloud-backup", version: $v, mode: $mode, createdAt: $ts,
      host: $host, stateDir: $state, secretsExcluded: $secretsExcluded}' > "$out"
  echo "$out"
}

native_create() { # full mode engine; echoes created archive path
  need openclaw
  local out="$STAGING/native-create.json" errf="$STAGING/native-create.err" arc=""
  if ! openclaw backup create --output "$STAGING/" --json > "$out" 2> "$errf"; then
    sed 's/^/  /' "$errf" >&2
    return 1
  fi
  arc="$(jq -r '.archivePath // empty' "$out" 2>/dev/null)"
  if [ -z "$arc" ]; then # tolerate non-JSON noise before the payload
    arc="$(sed -n '/^{/,$p' "$out" | jq -r '.archivePath // empty' 2>/dev/null)"
  fi
  [ -n "$arc" ] && [ -f "$arc" ] || return 1
  echo "$arc"
}

settings_paths() { # state-relative allowlist for `backup settings`
  local f rel
  [ -f "$STATE_DIR/openclaw.json" ] && echo "openclaw.json"
  [ -f "$STATE_DIR/openclaw.local.json" ] && echo "openclaw.local.json"
  for rel in "${SECRET_STORE_RELS[@]:-}"; do
    case "$rel" in *"*"*) continue ;; esac  # concrete file paths only
    [ -e "$STATE_DIR/$rel" ] && echo "$rel"
  done
  [ -d "$STATE_DIR/credentials" ] && echo "credentials"
  for f in "$STATE_DIR"/agents/*/agent/auth-profiles.json* "$STATE_DIR"/agents/*/agent/auth-state.json*; do
    [ -e "$f" ] && echo "${f#"$STATE_DIR"/}"
  done
}

workspace_dirs() { # absolute workspace dirs (config-declared + default), deduped
  {
    jq -r '.agents.list // [] | .[] | .workspace // empty' "$CONFIG_FILE" 2>/dev/null || true
    echo "$STATE_DIR/workspace"
  } | while IFS= read -r d; do d="$(expand_path "$d")"; [ -d "$d" ] && echo "$d"; done | sort -u
}

build_settings_archive() { # echoes archive path
  local arc
  arc="$STAGING/$(arc_name settings)"
  write_skill_manifest settings >/dev/null
  local -a rels=()
  while IFS= read -r p; do [ -n "$p" ] && rels+=("$p"); done < <(settings_paths | sort -u)
  [ ${#rels[@]} -gt 0 ] || { err "nothing to back up (settings)"; return 1; }
  tar -czf "$arc" -C "$STATE_DIR" "${rels[@]}" -C "$STAGING" cloud-backup-manifest.json || return 1
  if [ "$CONFIG_FILE" != "$STATE_DIR/openclaw.json" ] && [ -f "$CONFIG_FILE" ]; then
    warn "config file lives outside the state dir ($CONFIG_FILE) — included under its basename"
  fi
  echo "$arc"
}

build_workspace_archive() { # echoes archive path
  local arc d
  arc="$STAGING/$(arc_name workspace)"
  write_skill_manifest workspace >/dev/null
  local -a args=()
  while IFS= read -r d; do
    [ -n "$d" ] || continue
    args+=(-C "$(dirname "$d")" "$(basename "$d")")
  done < <(workspace_dirs)
  [ ${#args[@]} -gt 0 ] || { err "no workspace directories found"; return 1; }
  tar -czf "$arc" "${args[@]}" -C "$STAGING" cloud-backup-manifest.json || return 1
  echo "$arc"
}

# --- backup pipeline ------------------------------------------------------------------
human() { numfmt --to=iec --suffix=B "$1" 2>/dev/null || echo "${1}B"; }

preflight() { # $1 mode, $2 do_upload(bool)
  need tar jq gzip awk
  [ "$1" = "full" ] && need openclaw
  [ "$DO_ENCRYPT" = "true" ] && need gpg
  [ "$2" = "true" ] && need aws

  # disk: rough estimate from the newest artifact of this mode (2.2x), 500M floor
  local est=0 newest avail
  newest="$(ls -1t "$LOCAL_DIR"/openclaw_"$1"_*.tar.gz* 2>/dev/null | head -n1 || true)"
  [ -n "$newest" ] && est="$(stat -c %s "$newest" 2>/dev/null || stat -f %z "$newest" 2>/dev/null || echo 0)"
  local needbytes=$(( est > 0 ? est * 22 / 10 : 524288000 ))
  avail=$(( $(df -Pk "$LOCAL_DIR" | awk 'NR==2 {print $4}') * 1024 ))
  if [ "$avail" -lt "$needbytes" ]; then
    fail "$E_DISK" "insufficient disk in $LOCAL_DIR: $(human "$avail") free, need ~$(human "$needbytes")"
  fi

  if [ "$2" = "true" ]; then
    [ -z "$S3_REF_ERROR" ] || fail "$E_CLOUD" "S3 secret refs are configured but broken: $S3_REF_ERROR"
    # prefix-scoped first (works with prefix-scoped tokens), then bucket root
    s3 ls "s3://$BUCKET/$PREFIX" >/dev/null 2>&1 || s3 ls "s3://$BUCKET/" >/dev/null 2>&1 || \
      fail "$E_CLOUD" "cloud unreachable or bad credentials (bucket: $BUCKET, source: $S3_SOURCE)"
  fi
}

decide_encryption() { # $1 mode; sets DO_ENCRYPT + enforces the secrets policy
  local required=false
  case "$1" in
    full) [ "$VERDICT" = "secret-material" ] && required=true ;;
    settings) required=true ;;  # 100% secret material by construction
    workspace) ;;
  esac
  DO_ENCRYPT="$ENCRYPT"
  [ "$required" = "true" ] && DO_ENCRYPT=true
  if [ "$1" = "workspace" ] && [ "$NO_ENCRYPT" = "true" ] && [ "$required" != "true" ]; then
    DO_ENCRYPT=false
  fi

  if [ "$DO_ENCRYPT" = "true" ]; then
    if ! resolve_passphrase "$([ "$DRY_RUN" = "true" ] && echo soft)"; then
      if [ "$DRY_RUN" = "true" ]; then
        warn "${PASS_ERROR:-no passphrase configured} — a real run would FAIL (exit $E_PASSPHRASE)"
      elif [ "$required" = "true" ] && [ "$FORCE_PLAINTEXT" = "true" ] && [ -t 0 ]; then
        warn "FORCED PLAINTEXT for a secret-material scope (interactive --force-plaintext)"
        DO_ENCRYPT=false
      else
        err "this backup scope contains secret material:"
        local r; for r in "${VERDICT_REASONS[@]:-}"; do err "  - $r"; done
        fail "$E_PASSPHRASE" "encryption is required but no passphrase is configured. Set config.passphraseFile (see references/credentials.md), or use config.excludeSecrets."
      fi
    fi
  elif [ "$VERDICT" = "secret-material" ] && [ "$1" != "workspace" ]; then
    if [ "$DRY_RUN" = "true" ]; then
      warn "encryption disabled but scope contains secret material — a real run would FAIL (exit $E_PASSPHRASE)"
    else
      fail "$E_PASSPHRASE" "encryption disabled but scope contains secret material — refusing"
    fi
  else
    warn "Encryption is disabled — backup will be stored in plaintext."
  fi
}

cmd_backup() {
  local mode="$1"
  case "$mode" in
    full|settings|workspace) ;;
    skills) warn "mode 'skills' is deprecated; using 'workspace'"; mode=workspace ;;
    *) die "mode must be one of: full, settings, workspace" ;;
  esac

  print_deprecations
  secrets_verdict
  decide_encryption "$mode"

  local do_upload=false
  [ "$UPLOAD" = "true" ] && [ "$CLOUD" = "true" ] && [ "$NO_UPLOAD" != "true" ] && do_upload=true
  if [ "$UPLOAD" = "true" ] && [ "$NO_UPLOAD" != "true" ] && [ -n "$S3_REF_ERROR" ] && [ "$DRY_RUN" != "true" ]; then
    fail "$E_CLOUD" "S3 secret refs are configured but broken: $S3_REF_ERROR"
  fi
  if [ "$UPLOAD" = "true" ] && [ "$CLOUD" != "true" ] && [ "$NO_UPLOAD" != "true" ]; then
    warn "Cloud storage is not configured — backup will be local only."
  fi

  if [ "$DRY_RUN" = "true" ]; then
    backup_plan "$mode" "$do_upload"
    return 0
  fi

  # Lock BEFORE sweeping: a previous run's child (e.g. openclaw backup create)
  # may have survived its parent and still hold the inherited lock fd while
  # writing into its staging dir — never sweep under live work.
  acquire_lock
  sweep_stale_staging
  preflight "$mode" "$do_upload"
  new_staging

  # 1. produce the plaintext archive in staging
  local arc=""
  case "$mode" in
    full)
      info "Creating native OpenClaw backup (openclaw backup create)"
      arc="$(native_create)" || fail "$E_CREATE" "openclaw backup create failed"
      info "Applying lean filter"
      apply_lean_filter "$arc" || fail "$E_FILTER" "archive filtering failed"
      [ "$FILTERED_COUNT" -gt 0 ] && info "Excluded $FILTERED_COUNT file(s) from the archive"
      local named
      named="$STAGING/$(arc_name full)"
      mv -f "$arc" "$named"; arc="$named"
      ;;
    settings)  info "Creating settings backup";  arc="$(build_settings_archive)"  || fail "$E_CREATE" "settings archive failed" ;;
    workspace) info "Creating workspace backup"; arc="$(build_workspace_archive)" || fail "$E_CREATE" "workspace archive failed" ;;
  esac

  # 2. structural verify (pre-encryption) + entry count
  local entries_pre
  entries_pre="$(tar -tzf "$arc" | wc -l | tr -d ' ')" || fail "$E_VERIFY" "archive is unreadable"
  if [ "$mode" = "full" ] && has openclaw; then
    openclaw backup verify "$arc" >/dev/null 2>&1 || fail "$E_VERIFY" "openclaw backup verify rejected the archive"
  fi

  # 3. encrypt (plaintext never leaves staging)
  local payload="$arc"
  if [ "$DO_ENCRYPT" = "true" ]; then
    info "Encrypting (AES256)"
    gpg_enc_file "$arc" "$arc.gpg" || fail "$E_ENCRYPT" "encryption failed"
    rm -f "$arc"
    payload="$arc.gpg"
  fi

  # 4. checksum + quick verification (decrypt-to-stdout; no plaintext on disk)
  sha_make "$payload"
  local sha; sha="$(awk '{print $1}' "$payload.sha256")"
  if [ "$VERIFY_AFTER" != "off" ] && [ "$DO_ENCRYPT" = "true" ]; then
    info "Verifying (decrypt + list)"
    local entries_post
    entries_post="$(gpg_dec_stdout "$payload" | tar -tzf - | wc -l | tr -d ' ')" \
      || fail "$E_VERIFY" "post-encryption verification failed (decrypt/list)"
    [ "$entries_post" = "$entries_pre" ] \
      || fail "$E_VERIFY" "entry count mismatch after encryption ($entries_pre vs $entries_post)"
  fi

  # 5. upload + remote verification
  local remote_key=""
  if [ "$do_upload" = "true" ]; then
    remote_key="$PREFIX$(basename "$payload")"
    info "Uploading to s3://$BUCKET/$remote_key"
    s3 cp "$payload" "s3://$BUCKET/$remote_key" --metadata "sha256=$sha" >/dev/null \
      || fail "$E_UPLOAD" "upload failed"
    s3 cp "$payload.sha256" "s3://$BUCKET/$remote_key.sha256" >/dev/null \
      || warn "checksum sidecar upload failed"
    local head size_local size_remote sha_remote
    size_local="$(stat -c %s "$payload" 2>/dev/null || stat -f %z "$payload")"
    if ! head="$(s3api head-object --bucket "$BUCKET" --key "$remote_key" 2>/dev/null)"; then
      fail "$E_REMOTE_VERIFY" "uploaded object not found on HEAD check"
    fi
    size_remote="$(jq -r '.ContentLength // 0' <<<"$head")"
    sha_remote="$(jq -r '.Metadata.sha256 // empty' <<<"$head")"
    if [ "$size_remote" != "$size_local" ] || { [ -n "$sha_remote" ] && [ "$sha_remote" != "$sha" ]; }; then
      s3 rm "s3://$BUCKET/$remote_key" >/dev/null 2>&1 || true
      fail "$E_REMOTE_VERIFY" "remote object mismatch (size $size_remote vs $size_local)"
    fi
  fi

  # 6. publish to the local store (same filesystem → atomic), then retention
  mv "$payload" "$payload.sha256" "$LOCAL_DIR/"
  local published
  published="$LOCAL_DIR/$(basename "$payload")"
  info "Backup complete: $published ($(human "$(stat -c %s "$published" 2>/dev/null || stat -f %z "$published")"))"
  [ -n "$remote_key" ] && info "Uploaded to: s3://$BUCKET/$remote_key (verified)"

  local rc=$E_OK
  retention_local "$mode" || { warn "local retention failed"; rc=$E_WARN; }
  if [ "$do_upload" = "true" ]; then
    retention_remote "$mode" || { warn "remote retention failed"; rc=$E_WARN; }
  fi
  [ ${#WARNINGS[@]} -gt 0 ] && rc=$E_WARN

  if [ "$JSON_OUT" = "true" ]; then
    jq -n --arg mode "$mode" --arg artifact "$published" --arg sha "$sha" \
      --arg remote "${remote_key:+s3://$BUCKET/$remote_key}" \
      --argjson encrypted "$([ "$DO_ENCRYPT" = "true" ] && echo true || echo false)" \
      --argjson entries "$entries_pre" --argjson excluded "${FILTERED_COUNT:-0}" \
      --arg verdict "$VERDICT" \
      --argjson warnings "$(printf '%s\n' "${WARNINGS[@]:-}" | jq -R . | jq -s 'map(select(length>0))')" \
      '{ok: true, mode: $mode, artifact: $artifact, sha256: $sha, encrypted: $encrypted,
        entries: $entries, excludedFiles: $excluded, remote: (if $remote == "" then null else $remote end),
        sensitivity: $verdict, warnings: $warnings}'
  fi
  exit "$rc"
}

backup_plan() { # --dry-run: show exactly what would happen, create nothing
  local mode="$1" do_upload="$2"
  echo "cloud-backup v$VERSION — dry run"
  echo
  echo "Mode:        $mode$([ "$EVERYTHING" = "true" ] && echo ' (--everything)')"
  case "$mode" in
    full)      echo "Engine:      openclaw backup create (native; consistent SQLite snapshots) + lean filter" ;;
    settings)  echo "Engine:      allowlist tar (config, secret stores, credentials)" ;;
    workspace) echo "Engine:      tar of workspace directories" ;;
  esac
  echo "Encryption:  $([ "$DO_ENCRYPT" = "true" ] && echo "AES256 (passphrase: $PASS_SOURCE)" || echo "OFF")"
  echo "Local store: $LOCAL_DIR"
  echo "Upload:      $([ "$do_upload" = "true" ] && echo "s3://$BUCKET/$PREFIX (creds: $S3_SOURCE)" || echo "no")"
  echo
  echo "Archive sensitivity: $VERDICT"
  local r; for r in "${VERDICT_REASONS[@]:-}"; do [ -n "$r" ] && echo "  - $r"; done
  if [ "$mode" = "full" ]; then
    echo
    echo "Excludes (state-relative):"
    active_excludes | sed 's/^/  - /'
    if has openclaw; then
      echo
      echo "Native backup plan (openclaw backup create --dry-run):"
      openclaw backup create --dry-run 2>/dev/null | sed 's/^/  /' || echo "  (unavailable)"
    fi
  elif [ "$mode" = "settings" ]; then
    echo
    echo "Paths (state-relative):"
    settings_paths | sort -u | sed 's/^/  - /'
  else
    echo
    echo "Workspace directories:"
    workspace_dirs | sed 's/^/  - /'
  fi
  echo
  echo "Dry run only — nothing was created."
}

# --- retention -----------------------------------------------------------------------
# A complete set = artifact + .sha256 sidecar. Sets are keyed (mode, ts, host) and
# counted per mode. Plaintext artifacts with an encrypted sibling, or artifacts
# missing their sidecar, are failure debris — flagged here, deleted by prune.
local_sets() { # $1 mode → newline list of artifact paths (complete sets), oldest first
  local f
  for f in "$LOCAL_DIR"/openclaw_"$1"_*.tar.gz "$LOCAL_DIR"/openclaw_"$1"_*.tar.gz.gpg; do
    [ -f "$f" ] || continue
    [ -f "$f.sha256" ] || continue
    case "$f" in
      *.tar.gz) [ -f "$f.gpg" ] && continue ;;  # plaintext shadowed by encrypted sibling
    esac
    echo "$f"
  done | sort
}

local_debris() { # plaintext leftovers + sidecar-less artifacts, local store + legacy v1 dir
  local f
  for f in "$LOCAL_DIR"/openclaw_*.tar.gz "$LEGACY_BACKUPS"/openclaw_*.tar.gz; do
    [ -f "$f" ] || continue
    if [ -f "$f.gpg" ] || [ ! -f "$f.sha256" ]; then echo "$f"; fi
  done
  for f in "$LOCAL_DIR"/openclaw_*.tar.gz.gpg "$LEGACY_BACKUPS"/openclaw_*.tar.gz.gpg; do
    [ -f "$f" ] || continue
    [ -f "$f.sha256" ] || echo "$f"
  done
}

retention_local() { # $1 mode
  local cap="$LOCAL_COUNT"
  [ "$cap" -gt "$MAX_LOCAL" ] && cap=$MAX_LOCAL
  local -a sets=()
  while IFS= read -r f; do [ -n "$f" ] && sets+=("$f"); done < <(local_sets "$1")
  if [ ${#sets[@]} -gt "$cap" ]; then
    local n=$(( ${#sets[@]} - cap )) i
    info "Local retention: pruning $n $1 set(s) (keep $cap)"
    for ((i = 0; i < n; i++)); do
      safe_rm "${sets[$i]}" "${sets[$i]}.sha256"
    done
  fi
}

retention_remote() { # $1 mode
  local -a rk=()
  local key
  while IFS= read -r key; do
    [ -n "$key" ] || continue
    [ "$(arc_mode "$key")" = "$1" ] && rk+=("$key")
  done < <(remote_keys)

  if [ ${#rk[@]} -gt "$KEEP" ]; then
    local n=$(( ${#rk[@]} - KEEP )) i
    info "Remote retention: pruning $n $1 archive(s) (keep $KEEP)"
    for ((i = 0; i < n; i++)); do
      s3 rm "s3://$BUCKET/${rk[$i]}" >/dev/null
      s3 rm "s3://$BUCKET/${rk[$i]}.sha256" >/dev/null 2>&1 || true
    done
  fi

  if [ "$DAYS" -gt 0 ] 2>/dev/null; then
    local cutoff=""
    if date -d "now" >/dev/null 2>&1; then cutoff="$(date -d "$DAYS days ago" +%Y%m%d%H%M%S)"
    elif date -v-1d >/dev/null 2>&1; then cutoff="$(date "-v-${DAYS}d" +%Y%m%d%H%M%S)"; fi
    [ -n "$cutoff" ] || return 0
    local ts
    for key in "${rk[@]}"; do
      ts="$(arc_ts "$key")"; [ -n "$ts" ] || continue
      if [ "$ts" -lt "$cutoff" ]; then
        s3 rm "s3://$BUCKET/$key" >/dev/null
        s3 rm "s3://$BUCKET/$key.sha256" >/dev/null 2>&1 || true
      fi
    done
  fi
}

cmd_prune() {
  print_deprecations
  local dry="$DRY_RUN" deleted=0
  local -a debris=()
  while IFS= read -r f; do [ -n "$f" ] && debris+=("$f"); done < <(local_debris)

  if [ ${#debris[@]} -gt 0 ]; then
    info "Failure debris (plaintext leftovers / incomplete sets):"
    local f
    for f in "${debris[@]}"; do
      if [ "$dry" = "true" ]; then echo "  would delete: $f"
      else safe_rm "$f" "$f.sha256"; echo "  deleted: $f"; deleted=$((deleted + 1)); fi
    done
  fi

  local mode
  for mode in full settings workspace; do
    local -a sets=()
    while IFS= read -r f; do [ -n "$f" ] && sets+=("$f"); done < <(local_sets "$mode")
    local cap="$LOCAL_COUNT"; [ "$cap" -gt "$MAX_LOCAL" ] && cap=$MAX_LOCAL
    if [ ${#sets[@]} -gt "$cap" ]; then
      local n=$(( ${#sets[@]} - cap )) i
      for ((i = 0; i < n; i++)); do
        if [ "$dry" = "true" ]; then echo "  would delete: ${sets[$i]}"
        else safe_rm "${sets[$i]}" "${sets[$i]}.sha256"; deleted=$((deleted + 1)); fi
      done
    fi
  done

  if [ "$CLOUD" = "true" ]; then
    if [ "$dry" = "true" ]; then
      info "Remote (s3://$BUCKET/$PREFIX): keep $KEEP per mode, drop older than $DAYS days"
      local -a rk=()
      while IFS= read -r f; do [ -n "$f" ] && rk+=("$f"); done < <(remote_keys)
      local total=${#rk[@]}
      echo "  $total remote archive(s) present; run without --dry-run to apply retention"
    else
      acquire_lock
      for mode in full settings workspace; do retention_remote "$mode" || warn "remote retention failed ($mode)"; done
    fi
  fi
  [ "$dry" = "true" ] || info "Prune done. Deleted $deleted local file(s)."
}

# --- list / status / setup -------------------------------------------------------------
cmd_list() {
  info "Local ($LOCAL_DIR):"
  local f count=0
  for f in "$LOCAL_DIR"/openclaw_*.tar.gz "$LOCAL_DIR"/openclaw_*.tar.gz.gpg; do
    [ -f "$f" ] || continue
    echo "  $(du -h "$f" | cut -f1)  $(basename "$f")"
    count=$((count + 1))
  done
  [ "$count" -gt 0 ] || echo "  (none)"

  if [ -d "$LEGACY_BACKUPS" ] && ls "$LEGACY_BACKUPS"/openclaw_* >/dev/null 2>&1; then
    echo
    info "Legacy v1 store ($LEGACY_BACKUPS) — migrate or prune:"
    for f in "$LEGACY_BACKUPS"/openclaw_*.tar.gz "$LEGACY_BACKUPS"/openclaw_*.tar.gz.gpg; do
      [ -f "$f" ] || continue
      local tag=""
      case "$f" in *.tar.gz) tag="  [PLAINTEXT]" ;; esac
      echo "  $(du -h "$f" | cut -f1)  $(basename "$f")$tag"
    done
  fi

  local -a debris=()
  while IFS= read -r f; do [ -n "$f" ] && debris+=("$f"); done < <(local_debris)
  if [ ${#debris[@]} -gt 0 ]; then
    echo
    warn "${#debris[@]} failure-debris file(s) detected — run 'prune' to remove them"
  fi

  if [ "$CLOUD" = "true" ]; then
    echo
    info "Remote (s3://$BUCKET/$PREFIX):"
    s3 ls "s3://$BUCKET/$PREFIX" --recursive 2>/dev/null || echo "  (unreachable)"
  fi
}

cmd_status() {
  secrets_verdict
  echo "OpenClaw Cloud Backup v$VERSION"
  echo
  echo "Backups"
  local newest=""
  newest="$(ls -1t "$LOCAL_DIR"/openclaw_*.tar.gz.gpg "$LOCAL_DIR"/openclaw_*.tar.gz 2>/dev/null | head -n1 || true)"
  if [ -n "$newest" ]; then
    local enc="plaintext"; case "$newest" in *.gpg) enc="encrypted ✓" ;; esac
    echo "  Last:    $(basename "$newest")"
    echo "           $(du -h "$newest" | cut -f1) · $enc · $(date -r "$newest" '+%Y-%m-%d %H:%M' 2>/dev/null || echo '?')"
  else
    echo "  Last:    (none in $LOCAL_DIR)"
  fi
  echo "  Local:   $LOCAL_DIR (keep $LOCAL_COUNT per mode, cap $MAX_LOCAL)"
  if [ "$CLOUD" = "true" ]; then
    echo "  Remote:  s3://$BUCKET/$PREFIX (keep $KEEP per mode, $DAYS days)"
  else
    echo "  Remote:  not configured (local-only)"
  fi
  if has openclaw; then
    local sched
    sched="$(openclaw cron list --json 2>/dev/null \
      | jq -r '(.jobs // .) | if type=="array" then .[] else empty end
               | select(((.name // "") | test("cloud-backup")) or ((.payload.message // "") | test("cloud-backup")))
               | "\(.name // .id)"' 2>/dev/null | head -n3 || true)"
    if [ -n "$sched" ]; then
      echo "  Schedule: $(echo "$sched" | tr '\n' ' ')(manage: openclaw cron list)"
    else
      echo "  Schedule: none — backups run only when you ask (use 'schedule' to see the opt-in command)"
    fi
  fi

  echo
  echo "Credentials"
  echo "  S3:          $S3_SOURCE"
  if resolve_passphrase soft 2>/dev/null; then
    echo "  Passphrase:  $PASS_SOURCE"
  elif [ -n "$PASS_ERROR" ]; then
    echo "  Passphrase:  UNRESOLVABLE ✗ — $PASS_ERROR"
  else
    echo "  Passphrase:  not configured ✗ (encryption unavailable)"
  fi
  if [ "$DEP_S3" = "true" ] || [ "$DEP_GPG" = "true" ]; then
    echo "  openclaw.json: contains plaintext secrets — migrate and remove ✗"
  else
    echo "  openclaw.json: no plaintext cloud-backup secrets ✓"
  fi

  echo
  echo "Archive scope (mode=full)"
  echo "  Sensitivity: $VERDICT$([ "$VERDICT" = "secret-material" ] && echo ' → encryption FORCED')"
  local r; for r in "${VERDICT_REASONS[@]:-}"; do [ -n "$r" ] && echo "    - $r"; done
  echo "  Default excludes: codex caches/logs, session transcripts, tools, media, logs, old backups"

  if [ -n "$BUCKET" ]; then
    echo
    echo "Cloud"
    echo "  Bucket:   $BUCKET · region $REGION · endpoint ${ENDPOINT:-<aws default>}"
    if [ "$CLOUD" = "true" ]; then
      if s3 ls "s3://$BUCKET/" >/dev/null 2>&1; then echo "  Reachable ✓"; else echo "  Reachable ✗ (check credentials/endpoint)"; fi
    else
      echo "  Not ready: $([ "$PARTIAL_KEYS" = "true" ] && echo 'partial credentials' || echo 'missing credentials or aws CLI')"
    fi
  fi

  echo
  echo "Dependencies"
  local b
  for b in openclaw tar jq gzip awk aws gpg flock; do
    if has "$b"; then echo "  $b ✓"; else echo "  $b ✗"; fi
  done

  print_deprecations
  if [ "$ENCRYPT" != "true" ] && [ "$VERDICT" = "secret-material" ]; then
    warn "Encryption disabled with a secret-material scope — 'backup full' will FAIL until fixed"
  fi
  if [ -d "$LEGACY_BACKUPS" ] && ls "$LEGACY_BACKUPS"/openclaw_* >/dev/null 2>&1; then
    warn "legacy v1 backup dir $LEGACY_BACKUPS still has archives (see 'list'; they are excluded from new backups)"
  fi
}

cmd_setup() {
  cat <<'EOF'
OpenClaw Cloud Backup v2 — setup checklist (this command never writes config)

1. Create a PRIVATE bucket with your provider (see references/providers/).
2. Create a least-privilege, bucket-scoped access key.
3. Store the key OUTSIDE OpenClaw config (run this yourself):
     aws configure --profile openclaw-backup
     chmod 600 ~/.aws/credentials
4. Point the skill at it (non-secret values only):
     openclaw config patch 'skills.entries.cloud-backup.config.bucket="my-bucket"'
     openclaw config patch 'skills.entries.cloud-backup.config.endpoint="https://..."'   # non-AWS only
     openclaw config patch 'skills.entries.cloud-backup.config.profile="openclaw-backup"'
5. Enable encryption with a generated passphrase file (then store a copy in your
   password manager — without it backups are unrecoverable):
     umask 077 && openssl rand -base64 32 > ~/.openclaw/credentials/cloud-backup.passphrase
     openclaw config patch 'skills.entries.cloud-backup.config.passphraseFile="~/.openclaw/credentials/cloud-backup.passphrase"'
6. First backup: backup full --dry-run, review, then backup full.
7. Optional: 'schedule' prints the opt-in cron command. Nothing is ever scheduled
   automatically.

NEVER put ACCESS_KEY_ID / SECRET_ACCESS_KEY / GPG_PASSPHRASE into openclaw.json —
backups archive that file (see references/credentials.md).
EOF
  echo
  cmd_status
  if [ "$CLOUD" = "true" ]; then
    echo
    echo "Testing connection..."
    if s3 ls "s3://$BUCKET/" >/dev/null 2>&1; then echo "✓ Connected (bucket reachable)"; else echo "✗ Failed — check credentials"; fi
  fi
}

cmd_schedule() {
  local tz; tz="$(timedatectl show -p Timezone --value 2>/dev/null || cat /etc/timezone 2>/dev/null || echo '<your-tz, e.g. Europe/Warsaw>')"
  cat <<EOF
Scheduling is strictly OPT-IN. Nothing is created by this command — it only
prints what the operator (or the agent, after your explicit confirmation)
would run:

  openclaw cron add \\
    --name cloud-backup-daily \\
    --cron "0 2 * * *" --tz "$tz" \\
    --session isolated --wake now \\
    --message "Unattended cloud-backup run (operator preconfirmed): use the cloud-backup skill to run 'backup full'. Report archive name, size, encrypted status, upload destination, and verification result. If anything fails, include the exact stderr. Do not restore, prune, change config, or create schedules." \\
    --announce --best-effort-deliver

Adjust the time, timezone, and delivery (--channel/--to) to your setup.
Remove later with: openclaw cron list && openclaw cron rm <id>
EOF
}

# --- verify ------------------------------------------------------------------------
resolve_artifact() { # $1 name|--latest → echoes local path (downloading if needed)
  local name="$1" src=""
  if [ "$name" = "--latest" ] || [ -z "$name" ]; then
    src="$(ls -1t "$LOCAL_DIR"/openclaw_*.tar.gz.gpg "$LOCAL_DIR"/openclaw_*.tar.gz 2>/dev/null | head -n1 || true)"
    [ -n "$src" ] || fail "$E_USAGE" "no local backups found in $LOCAL_DIR (pass a name or run 'list')"
    echo "$src"; return 0
  fi
  if [ -f "$name" ]; then echo "$name"; return 0; fi
  if [ -f "$LOCAL_DIR/$name" ]; then echo "$LOCAL_DIR/$name"; return 0; fi
  if [ -f "$LEGACY_BACKUPS/$name" ]; then echo "$LEGACY_BACKUPS/$name"; return 0; fi
  if [ "$CLOUD" = "true" ]; then
    local key="$name"
    case "$key" in */*) ;; *) key="$PREFIX$key" ;; esac
    src="$STAGING/$(basename "$key")"
    info "Downloading s3://$BUCKET/$key" >&2
    s3 cp "s3://$BUCKET/$key" "$src" >/dev/null || fail "$E_CLOUD" "download failed: $key"
    s3 cp "s3://$BUCKET/$key.sha256" "$src.sha256" >/dev/null 2>&1 || true
    echo "$src"; return 0
  fi
  fail "$E_USAGE" "'$name' not found locally and cloud is not configured"
}

cmd_verify() {
  local name="${1:---latest}"
  new_staging
  local src; src="$(resolve_artifact "$name")"
  info "Verifying $(basename "$src")"

  if sha_check "$src"; then
    info "Checksum: ✓"
  elif [ $? -eq 2 ]; then
    warn "no .sha256 sidecar — skipping checksum"
  else
    fail "$E_VERIFY" "checksum mismatch: $src"
  fi

  local listing="$STAGING/listing.txt"
  case "$src" in
    *.gpg)
      need gpg
      resolve_passphrase || [ -t 0 ] || fail "$E_PASSPHRASE" "no passphrase configured and no TTY to prompt"
      if [ "$DEEP" = "true" ]; then
        local plain
        plain="$STAGING/$(basename "${src%.gpg}")"
        gpg_dec_stdout "$src" > "$plain" || fail "$E_VERIFY" "decryption failed"
        tar -tzf "$plain" > "$listing" || fail "$E_VERIFY" "archive listing failed"
        if grep -qE '^[^/]+/manifest\.json$' "$listing" && has openclaw; then
          openclaw backup verify "$plain" >/dev/null 2>&1 \
            && info "openclaw backup verify: ✓" \
            || fail "$E_VERIFY" "openclaw backup verify rejected the archive"
        fi
      else
        gpg_dec_stdout "$src" | tar -tzf - > "$listing" || fail "$E_VERIFY" "decrypt/list failed"
      fi
      info "Decryption: ✓"
      ;;
    *)
      tar -tzf "$src" > "$listing" || fail "$E_VERIFY" "archive listing failed"
      if [ "$DEEP" = "true" ] && grep -qE '^[^/]+/manifest\.json$' "$listing" && has openclaw; then
        openclaw backup verify "$src" >/dev/null 2>&1 \
          && info "openclaw backup verify: ✓" \
          || fail "$E_VERIFY" "openclaw backup verify rejected the archive"
      fi
      ;;
  esac
  tar_safe_listing < "$listing"
  info "Entries: $(wc -l < "$listing" | tr -d ' ') · paths safe ✓"
  info "Verification passed."
}

# --- restore -------------------------------------------------------------------------
cmd_restore() {
  local name="$1"
  [ -n "$name" ] || die "restore needs a backup name (run 'list' first) or --latest"
  need tar
  print_deprecations
  new_staging

  local src; src="$(resolve_artifact "$name")"
  if sha_check "$src"; then :; elif [ $? -eq 2 ]; then warn "no .sha256 sidecar — skipping checksum"; else fail "$E_RESTORE" "checksum mismatch: $src"; fi

  local ext="$src"
  case "$src" in
    *.gpg)
      need gpg
      resolve_passphrase || [ -t 0 ] || fail "$E_PASSPHRASE" "no passphrase configured and no TTY to prompt"
      info "Decrypting"
      ext="$STAGING/$(basename "${src%.gpg}")"
      gpg_dec_stdout "$src" > "$ext" || fail "$E_RESTORE" "decryption failed"
      ;;
  esac

  local listing="$STAGING/listing.txt"
  tar -tzf "$ext" > "$listing" || fail "$E_RESTORE" "archive is unreadable"
  tar_safe_listing < "$listing"

  # flavor: native (openclaw backup create), skill (settings/workspace), or v1
  local flavor="v1" root="" native_state=""
  root="$(head -n1 "$listing" | cut -d/ -f1)"
  if grep -qE '^[^/]+/manifest\.json$' "$listing"; then
    flavor="native"
    native_state="$(tar -xzOf "$ext" "$root/manifest.json" 2>/dev/null | jq -r '.paths.stateDir // empty' 2>/dev/null || true)"
  elif grep -qE '(^|/)cloud-backup-manifest\.json$' "$listing"; then
    flavor="$(tar -xzOf "$ext" cloud-backup-manifest.json 2>/dev/null | jq -r '.mode // "skill"' 2>/dev/null || echo skill)"
  fi

  local -a only_args=()
  if [ ${#ONLY_GLOBS[@]} -gt 0 ]; then
    # tar errors out on wildcard patterns that match nothing, so anchor v1-flavor
    # patterns to whichever member style the archive actually uses.
    local g dotslash=""
    grep -q '^\./' "$listing" && dotslash="./"
    for g in "${ONLY_GLOBS[@]}"; do
      if [ "$flavor" = "native" ]; then
        only_args+=("$root/payload/posix${native_state:-$STATE_DIR}/$g")
      else
        only_args+=("$dotslash$g")
      fi
    done
  fi

  if [ "$DRY_RUN" = "true" ]; then
    info "Dry run — archive contents ($flavor flavor):"
    if [ ${#only_args[@]} -gt 0 ]; then
      tar -tzf "$ext" --wildcards "${only_args[@]}" 2>/dev/null || warn "no members match --only patterns"
    else
      cat "$listing"
    fi
    return 0
  fi

  local -a xtra=(--no-same-owner --no-same-permissions)
  [ ${#only_args[@]} -gt 0 ] && xtra+=(--wildcards "${only_args[@]}")

  if [ "$IN_PLACE" = "true" ]; then
    # In-place restores overwrite live state. Two explicit confirmations, or
    # --yes --force for non-interactive use.
    case "$flavor" in
      workspace) fail "$E_RESTORE" "workspace archives may span directories outside the state dir — restore to a staging dir (--target) and copy manually" ;;
      native)
        if [ -n "$native_state" ] && [ "$native_state" != "$STATE_DIR" ]; then
          fail "$E_RESTORE" "archive was taken from state dir '$native_state' but this host uses '$STATE_DIR' — cross-host restores must go through --target"
        fi ;;
    esac
    if [ "$ASSUME_YES" != "true" ] || [ "$FORCE" != "true" ]; then
      [ -t 0 ] || fail "$E_RESTORE" "non-interactive in-place restore needs --yes --force"
      echo "This will OVERWRITE live files under $STATE_DIR (and, for native archives, any backed-up workspace/config paths)."
      echo "Stop the gateway first: systemctl --user stop openclaw-gateway (or equivalent)."
      printf "Type 'restore' to continue: "
      local ans; read -r ans
      [ "$ans" = "restore" ] || { info "Cancelled."; return 0; }
    fi
    case "$flavor" in
      native) tar -xzf "$ext" -C / --strip-components=3 "${xtra[@]}" || fail "$E_RESTORE" "extraction failed" ;;
      *)      tar -xzf "$ext" -C "$STATE_DIR" "${xtra[@]}" || fail "$E_RESTORE" "extraction failed" ;;
    esac
    info "Restored in place. Restart the gateway and run 'openclaw doctor'."
    return 0
  fi

  # default: staged restore
  local target="${TARGET_DIR:-$HOME/openclaw-restore-$(date +%Y%m%d_%H%M%S)}"
  mkdir -m 700 -p "$target" || fail "$E_RESTORE" "cannot create $target"
  case "$flavor" in
    native)
      tar -xzf "$ext" -C "$target" --strip-components=3 "${xtra[@]}" || fail "$E_RESTORE" "extraction failed"
      tar -xzOf "$ext" "$root/manifest.json" > "$target/manifest.json" 2>/dev/null || true
      info "Staged restore complete: $target"
      info "Archive state dir: ${native_state:-unknown}"
      echo
      echo "Next steps (review first, then copy what you need):"
      echo "  1. systemctl --user stop openclaw-gateway   # or your equivalent"
      echo "  2. rsync -a --delete \"$target${native_state:-$STATE_DIR}/\" \"$STATE_DIR/\""
      echo "  3. systemctl --user start openclaw-gateway && openclaw doctor"
      ;;
    *)
      tar -xzf "$ext" -C "$target" "${xtra[@]}" || fail "$E_RESTORE" "extraction failed"
      info "Staged restore complete: $target"
      echo "Review the files, then copy what you need into $STATE_DIR (stop the gateway first)."
      ;;
  esac
}

# --- main ----------------------------------------------------------------------------
usage() {
  cat <<EOF
OpenClaw Cloud Backup v$VERSION — the cloud layer for 'openclaw backup'

Usage: $(basename "$0") <command> [args]

  backup [full|settings|workspace] [--everything] [--no-upload] [--no-encrypt]
         [--force-plaintext] [--dry-run] [--json]
                       Create archive (native engine for 'full'), encrypt, upload
  list                 Local + remote backups (flags failure debris)
  status [--json]      Health: last backup, credentials, sensitivity, schedule
  verify [name|--latest] [--deep]
                       Checksum + decrypt + listing (+'--deep': openclaw backup verify)
  restore <name|--latest> [--target DIR | --in-place] [--only GLOB]...
          [--dry-run] [--yes] [--force]
                       Staged restore by default; in-place needs confirmation
  prune [--dry-run]    Apply retention + remove failure debris (local and remote)
  schedule             Print the OPT-IN cron command (never creates anything)
  setup                Setup checklist + connection test (never writes config)

Exit codes: 0 ok · 3 ok-with-warnings · 4 usage · 10 lock · 11 deps · 12 disk ·
13 cloud · 14 passphrase/encryption-policy · 20-25 pipeline/verify · 30 restore
EOF
}

cmd="${1:-help}"; shift || true

# global flags
DRY_RUN=false; EVERYTHING=false; NO_UPLOAD=false; NO_ENCRYPT=false
FORCE_PLAINTEXT=false; DEEP=false; ASSUME_YES=false; FORCE=false; IN_PLACE=false
TARGET_DIR=""; ONLY_GLOBS=(); POSITIONAL=()
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=true ;;
    --json) JSON_OUT=true ;;
    --everything) EVERYTHING=true ;;
    --no-upload) NO_UPLOAD=true ;;
    --no-encrypt) NO_ENCRYPT=true ;;
    --force-plaintext) FORCE_PLAINTEXT=true ;;
    --deep) DEEP=true ;;
    --yes) ASSUME_YES=true ;;
    --force) FORCE=true ;;
    --in-place) IN_PLACE=true ;;
    --latest) POSITIONAL+=("--latest") ;;
    --target) shift; [ $# -gt 0 ] || die "--target needs a directory"; TARGET_DIR="$1" ;;
    --only) shift; [ $# -gt 0 ] || die "--only needs a glob"; ONLY_GLOBS+=("$1") ;;
    --help|-h) usage; exit 0 ;;
    --*) die "unknown flag: $1" ;;
    *) POSITIONAL+=("$1") ;;
  esac
  shift
done

load_config
[ "$EVERYTHING_CFG" = "true" ] && EVERYTHING=true

case "$cmd" in
  backup)   cmd_backup "${POSITIONAL[0]:-full}" ;;
  list)     cmd_list ;;
  status)   cmd_status ;;
  setup)    cmd_setup ;;
  verify)   cmd_verify "${POSITIONAL[0]:---latest}" ;;
  restore)  cmd_restore "${POSITIONAL[0]:-}" ;;
  prune)    cmd_prune ;;
  cleanup)  warn "'cleanup' is deprecated; use 'prune'"; cmd_prune ;;
  schedule) cmd_schedule ;;
  version|--version) echo "cloud-backup $VERSION" ;;
  help|-h|--help) usage ;;
  *) usage >&2; die "unknown command: $cmd" ;;
esac
