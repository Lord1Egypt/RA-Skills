#!/usr/bin/env bash
# Preflight: one authenticated HTTPS GET, count the items, dispatch only if count > 0.
# Zero LLM tokens. Run it often (every 5-15 min); let the heavy cron sleep.
#
# THE PREFLIGHT DECIDES NOTHING. IT COUNTS.
# It must never fetch a work item, mutate state, or judge what to do next.
#
# Network + credential behaviour, declared:
#   - Reads QUEUE_URL and API_TOKEN from a config file OUTSIDE the skill directory:
#     ${AOA_SECRETS_FILE:-${XDG_CONFIG_HOME:-$HOME/.config}/always-on-agent-ops/secrets.env}
#   - The file is PARSED (two keys), never sourced: it cannot execute code.
#   - Refused unless it is a regular file owned by you with no group/other bits (600/400).
#   - QUEUE_URL must be https://. Plain http:// is accepted ONLY for a loopback host
#     (localhost, 127.0.0.1, [::1]). No userinfo (user@host) is accepted.
#   - The Bearer is passed to curl on stdin, never on the command line (not visible in ps).
# No config = no network. Every exit path emits exactly one status line.
# Deliberately NOT `set -e`: a preflight that dies mid-run is the silence this skill exists to prevent.
set -uo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
source "$DIR/cron-message.sh"

JOB="pf-10-queue"

need_human() {  # <result> <next> <details>
  cron_message "$JOB" "Human action required" "$1" "preflight" "$2" "$3"
  exit 0
}

# --- locate the config file ---------------------------------------------------
# Under some schedulers HOME is unset; `set -u` would abort with no status line.
if [ -n "${AOA_SECRETS_FILE:-}" ]; then
  SECRETS="$AOA_SECRETS_FILE"
elif [ -n "${XDG_CONFIG_HOME:-}" ]; then
  SECRETS="$XDG_CONFIG_HOME/always-on-agent-ops/secrets.env"
elif [ -n "${HOME:-}" ]; then
  SECRETS="$HOME/.config/always-on-agent-ops/secrets.env"
else
  need_human "HOME and AOA_SECRETS_FILE unset - cannot locate config." \
    "Set AOA_SECRETS_FILE to an absolute path. See SKILL.md, Setup." "reason=no_config_path"
fi

case "$SECRETS" in
  /*) ;;
  *) need_human "Config path is not absolute." "Set AOA_SECRETS_FILE to an absolute path." "reason=relative_config_path" ;;
esac
# Inside the skill tree = shipped/backed-up/copied with the code. Refuse.
# Compare physical paths (pwd -P), so `..` or a symlinked parent cannot hide it.
SKILL_ROOT="$(cd "$DIR/.." && pwd -P)"
[ -f "$SKILL_ROOT/SKILL.md" ] || SKILL_ROOT="$(cd "$DIR" && pwd -P)"
secrets_dir="$(cd "$(dirname "$SECRETS")" 2>/dev/null && pwd -P || echo "")"
case "$secrets_dir/" in
  "$SKILL_ROOT"/*)
    need_human "Config file lives inside the skill directory." \
      "Move it to ~/.config/always-on-agent-ops/secrets.env (chmod 600)." "reason=config_in_skill_dir" ;;
esac

if [ ! -e "$SECRETS" ]; then
  need_human "Config file absent - no network configured." \
    "Create it (chmod 600). See SKILL.md, Setup." "reason=no_config"
fi
if [ -L "$SECRETS" ] || [ ! -f "$SECRETS" ]; then
  need_human "Config path is not a regular file (symlink, dir, or device)." \
    "Replace it with a regular file, chmod 600." "reason=config_not_regular"
fi

# --- permissions: owner = me, no group/other bits. Unknown = refuse. -------------
mode="$(stat -f %Lp "$SECRETS" 2>/dev/null || stat -c %a "$SECRETS" 2>/dev/null || echo "")"
owner="$(stat -f %u "$SECRETS" 2>/dev/null || stat -c %u "$SECRETS" 2>/dev/null || echo "")"
me="$(id -u 2>/dev/null || echo "")"
case "$mode" in
  600|400) ;;
  *) need_human "Config file permissions too open or unreadable (mode=${mode:-unknown})." \
       "chmod 600 the file." "reason=config_mode" ;;
esac
if [ -z "$owner" ] || [ -z "$me" ] || [ "$owner" != "$me" ]; then
  need_human "Config file not owned by the running user." \
    "chown it to the user that runs the gateway." "reason=config_owner"
fi

# --- parse, do not source -------------------------------------------------------
QUEUE_URL=""
API_TOKEN=""
while IFS= read -r line || [ -n "$line" ]; do
  case "$line" in
    QUEUE_URL=*) QUEUE_URL="${line#QUEUE_URL=}" ;;
    API_TOKEN=*) API_TOKEN="${line#API_TOKEN=}" ;;
  esac
done < "$SECRETS"
# Strip one pair of surrounding quotes, if any.
strip_quotes() {
  local v="$1"
  case "$v" in
    \"*\") v="${v#\"}"; v="${v%\"}" ;;
    \'*\') v="${v#\'}"; v="${v%\'}" ;;
  esac
  printf '%s' "$v"
}
QUEUE_URL="$(strip_quotes "$QUEUE_URL")"
API_TOKEN="$(strip_quotes "$API_TOKEN")"

if [ -z "$QUEUE_URL" ] || [ -z "$API_TOKEN" ]; then
  need_human "QUEUE_URL or API_TOKEN missing from the config file." "Set both, then rerun." "reason=no_config"
fi

# Whitespace/control chars: a token with a newline would inject a second header.
case "$QUEUE_URL$API_TOKEN" in
  *[[:space:]]*|*[[:cntrl:]]*)
    need_human "QUEUE_URL or API_TOKEN contains whitespace or control characters." \
      "Fix the config file." "reason=bad_config_chars" ;;
esac

# --- transport: https everywhere, http only to loopback --------------------------
scheme="$(printf '%s' "${QUEUE_URL%%://*}" | tr '[:upper:]' '[:lower:]')"
rest="${QUEUE_URL#*://}"
authority="${rest%%[/?#]*}"
case "$QUEUE_URL" in *://*) ;; *) scheme="" ;; esac
case "$authority" in
  *@*) need_human "QUEUE_URL carries userinfo (user@host) - refused." \
         "Use a plain https://host/path URL." "reason=url_userinfo" ;;
esac
host_lc="$(printf '%s' "$authority" | tr '[:upper:]' '[:lower:]')"
# Split an optional :port; a port must be digits only.
case "$host_lc" in
  \[*\]:*|\[*\]) host_only="${host_lc%%]*}]"; port="${host_lc#"$host_only"}" ;;
  *:*) host_only="${host_lc%%:*}"; port=":${host_lc#*:}" ;;
  *) host_only="$host_lc"; port="" ;;
esac
case "$port" in
  "") ;;
  :*[!0-9]*|:) need_human "QUEUE_URL port is not numeric." "Fix QUEUE_URL." "reason=url_bad_port" ;;
esac
case "$scheme" in
  https)
    [ -n "$host_only" ] || need_human "QUEUE_URL has no host." "Fix QUEUE_URL." "reason=url_no_host"
    PROTO="=https" ;;
  http)
    case "$host_only" in
      localhost|127.0.0.1|"[::1]") PROTO="=http" ;;
      *) need_human "QUEUE_URL is plain http to a non-loopback host - the Bearer would travel in clear. Refused." \
           "Use https://, or http://127.0.0.1 for a local listener." "reason=url_not_https" ;;
    esac ;;
  *) need_human "QUEUE_URL scheme is not https - refused." \
       "Use https://host/path." "reason=url_not_https" ;;
esac

# `-fs` + 2>/dev/null on purpose: curl's own diagnostic on stderr would land in the channel
# next to the status line. `--proto` pins the scheme; no -L, so no redirect is followed.
# The header comes from stdin (`-H @-`): the token never appears in argv / ps.
json="$(printf 'Authorization: Bearer %s\n' "$API_TOKEN" \
  | curl -fs --max-time 30 --proto "$PROTO" --proto-redir "=https" -H @- -- "$QUEUE_URL" 2>/dev/null || true)"
if [ -z "$json" ]; then
  cron_message "$JOB" "Error" "Queue unreachable (HTTP error, timeout, or empty body)." \
    "outbound queue" "No cron started; the heavy job's spaced fallback still covers this." "reason=fetch_failed"
  exit 0
fi

# Tolerant count: honour an explicit numeric `count`, else the SHALLOWEST array found
# anywhere in the payload (breadth-first, so a nested {data:{items:[...]}} still counts).
#
# "Counted zero" and "found nothing to count" are DIFFERENT ANSWERS. An empty array is 0.
# A payload with no count and no array anywhere - a 200 carrying {"error":"unauthorized"},
# a shape we do not understand - prints `nocount` and becomes an Error line. Returning 0
# there would report "Queue empty" while the queue fills: the silence this skill exists to
# prevent, manufactured by its own counter.
count="$(printf '%s' "$json" | node -e '
let s = "";
process.stdin.on("data", (d) => (s += d));
process.stdin.on("end", () => {
  let j;
  try { j = JSON.parse(s); } catch { process.stdout.write("unparsable"); return; }
  if (j === null || typeof j !== "object") { process.stdout.write("unparsable"); return; }
  if (typeof j.count === "number" && Number.isFinite(j.count)) {
    process.stdout.write(String(Math.max(0, Math.trunc(j.count))));
    return;
  }
  const q = [j];
  for (let i = 0; i < q.length && i < 2000; i++) {
    const n = q[i];
    if (Array.isArray(n)) { process.stdout.write(String(n.length)); return; }
    for (const v of Object.values(n)) if (v !== null && typeof v === "object") q.push(v);
  }
  process.stdout.write("nocount");
});
' || echo "unparsable")"

case "$count" in
  nocount)
    cron_message "$JOB" "Error" "Payload carries no count and no array - cannot tell empty from full." \
      "outbound queue" "Check the endpoint and the token; a 200 carrying an API error object looks like this." "reason=no_countable_field"
    exit 0
    ;;
  ''|*[!0-9]*)
    cron_message "$JOB" "Error" "Unreadable payload (not JSON, or not an object/array)." \
      "outbound queue" "Check the endpoint; a login page or proxy error looks like this." "reason=bad_payload"
    exit 0
    ;;
esac

if [ "$count" -gt 0 ]; then
  # One event, one status line: the dispatcher speaks, the preflight stays quiet.
  # `exec bash` on purpose: ClawHub ships text, not file modes, so the exec bit may
  # be absent on a fresh install. A bare exec would die 126 with NO status line -
  # the exact silence this skill exists to prevent.
  exec bash "$DIR/event-dispatch.sh" work_ready "$count"
fi

cron_message "$JOB" "Nothing to do" "Queue empty." "outbound queue" \
  "No cron started." "count=0"
exit 0
