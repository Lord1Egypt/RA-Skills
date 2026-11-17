#!/usr/bin/env bash
# OAuth expiry heuristic for an always-on agent.
# Subscription-style OAuth tokens expire in DAYS and do NOT refresh headless:
# the daemon just starts failing every turn, quietly. This detects it early.
#
# Strategy: (1) if the auth profile carries an epoch expiry field, use the
#               EARLIEST one - one file can hold several profiles, and the
#               weakest link is the one that takes the agent down;
#           (2) ONLY if the file parses and genuinely carries no expiry field,
#               fall back to the file mtime as a proxy for "last login".
#
# THE RULE: "I could not determine the expiry" is NEVER "ok". Corrupt JSON, no
# python3, or an expiry we cannot read all emit status=warn. A monitor that says
# ok when it does not know is worse than no monitor: it manufactures silence.
# Prints JSON on stdout: {"status":"ok|warn|missing", ...}. NEVER fails (exit 0)
# — a monitor that can crash is a monitor that stops monitoring.
set -u

HOME_DIR="${OPENCLAW_HOME:-$HOME/.openclaw}"
AGENT_ID="${OPENCLAW_AGENT_ID:-main}"
AUTH="$HOME_DIR/agents/$AGENT_ID/agent/auth-profiles.json"
WARN_DAYS="${OAUTH_WARN_DAYS:-2}"     # warn when <= N days remain
MTIME_WARN_DAYS="${OAUTH_MTIME_WARN_DAYS:-3}"  # proxy threshold when no expiry field

# Every "cannot verify" path lands here. Never `ok`.
warn_unresolved() {
  printf '{"status":"warn","source":"unresolved","reason":"%s","note":"Cannot verify token expiry - treating as suspect. Inspect the profile or relogin: openclaw auth login."}\n' "$1"
  exit 0
}

if [ ! -f "$AUTH" ]; then
  printf '{"status":"missing","file":"%s","note":"auth profile absent - login never completed?"}\n' "$AUTH"
  exit 0
fi

now=$(date +%s)

# No python3 = no way to read the profile = we do not know = warn (not ok).
command -v python3 >/dev/null 2>&1 || warn_unresolved "no_python3"

# (1) Look for an epoch expiry anywhere in the profile (seconds or milliseconds).
# The probe prints exactly one sentinel so bash can tell "absent" from "unreadable".
rc=0
raw=$(python3 - "$AUTH" 2>/dev/null <<'PY'
import json, sys
KEYS = ("expires_at", "expiresat", "exp", "expiry", "expire_at")
try:
    d = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception:
    print("BADPARSE"); sys.exit(0)          # unreadable credential != healthy credential
def norm(v):
    if isinstance(v, bool):
        return None                          # bool is an int subclass - reject explicitly
    if isinstance(v, (int, float)):
        f = float(v)
    elif isinstance(v, str):
        try:
            f = float(v.strip())             # epochs are commonly serialised as strings
        except ValueError:
            return None                      # ISO-8601 or junk: unresolved, NOT absent
    else:
        return None
    return f / 1000.0 if f > 1e12 else f     # ms -> s, normalised before comparing
good, bad = [], []
leaves = 0                                   # any scalar anywhere == the store holds something
def walk(o, path=""):
    global leaves
    if isinstance(o, dict):
        for k, v in o.items():
            p = (path + "." + k) if path else k
            if k.lower() in KEYS:
                f = norm(v)
                (good if f is not None else bad).append((f, p))
            walk(v, p)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, "%s[%d]" % (path, i))
    elif o is not None:
        leaves += 1                          # scalar leaf: a profile actually carries data
walk(d)
# Only key PATHS are ever printed - never a token value. Keys are data from the file:
# whitelist their characters so a hostile key cannot break the JSON line or inject text.
import re
clean = lambda p: re.sub(r"[^A-Za-z0-9_.\[\]-]", "_", p)[:200]
if good:
    # min, not max: a fresh profile must never mask an expired one, and a
    # long-lived refresh token must never mask a dead access token.
    v, p = min(good, key=lambda t: t[0])
    print("EPOCH|%d|%s" % (int(v), clean(p)))
elif bad:
    print("UNREADABLE_FIELD|%s" % clean(bad[0][1]))
elif leaves == 0:
    # {}, [], null, {"profiles":{}} : parses, but carries no profile data at all. Same
    # condition as a missing file - login never completed, or the store was wiped. The mtime
    # proxy would call a freshly-emptied store "ok" for MTIME_WARN_DAYS while every turn fails.
    print("EMPTYPROFILE")
else:
    print("NOFIELD")                         # a real profile, genuinely no expiry field
PY
) || rc=$?
[ "$rc" -eq 0 ] || warn_unresolved "python_failed"

case "$raw" in
  EPOCH\|*)
    rest="${raw#EPOCH|}"
    expires_at="${rest%%|*}"
    field="${rest#*|}"
    # Never feed an unvalidated string to $(( )): under `set -u` a non-numeric word is read
    # as a variable name and aborts the script with NO status line - a crash-shaped silence.
    case "${expires_at#-}" in
      ''|*[!0-9]*) warn_unresolved "bad_epoch_from_probe" ;;
    esac
    remaining=$(( (expires_at - now) / 86400 ))
    if [ "$expires_at" -le "$now" ] || [ "$remaining" -le "$WARN_DAYS" ]; then
      printf '{"status":"warn","source":"expires_at","field":"%s","remaining_days":%s,"note":"Token expired or expiring. Human relogin required: openclaw auth login."}\n' "$field" "$remaining"
    else
      printf '{"status":"ok","source":"expires_at","field":"%s","remaining_days":%s}\n' "$field" "$remaining"
    fi
    exit 0
    ;;
  UNREADABLE_FIELD\|*) warn_unresolved "non_numeric_expiry_at_${raw#UNREADABLE_FIELD|}" ;;
  BADPARSE)            warn_unresolved "corrupt_json" ;;
  EMPTYPROFILE)        warn_unresolved "empty_profile_store" ;;   # parses, holds nothing: login never completed?
  NOFIELD)             ;;   # fall through: valid JSON, a real profile, genuinely no expiry field
  *)                   warn_unresolved "unexpected_probe_output" ;;   # incl. empty
esac

# (2) Fallback: file age as a proxy for the last successful login. Reached ONLY
# when the profile parsed cleanly and carries no expiry field at all.
m=$(stat -f %m "$AUTH" 2>/dev/null || stat -c %Y "$AUTH" 2>/dev/null || echo "")
case "$m" in ''|*[!0-9]*) warn_unresolved "mtime_unreadable" ;; esac
age=$(( (now - m) / 86400 ))
if [ "$age" -ge "$MTIME_WARN_DAYS" ]; then
  printf '{"status":"warn","source":"mtime","age_days":%s,"note":"Auth profile older than threshold (mtime proxy). Verify or relogin: openclaw auth login."}\n' "$age"
else
  printf '{"status":"ok","source":"mtime","age_days":%s}\n' "$age"
fi
exit 0
