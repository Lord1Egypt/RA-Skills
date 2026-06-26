#!/usr/bin/env bash
# Deploy a built lookbook directory to Cloudflare Pages.
#
# Usage:
#   scripts/deploy-lookbook.sh <deploy-dir> <project-name> [flags]
#
# What it does:
#   1. Probes wrangler auth — fails loudly if unauthenticated.
#   2. Confirms the deploy with the user (skipped if --auto + the customer
#      has profile.md → preferred_lookbook_host_auto: true).
#   3. Idempotently creates the Pages project (Wrangler v4+ requires this
#      before first `pages deploy`).
#   4. (default) Bakes the voting capability into the deploy dir:
#         functions/api/vote.js + votes.js + wrangler.toml + favicons +
#         injects the thumbs-UI into index.html. Opt out via --no-voting.
#   5. Runs scripts/validate-lookbook.py against the local artifact.
#   6. Deploys.
#   7. Runs scripts/validate-lookbook.py against the deployed URL + smoke-
#      tests /api/votes when voting is on.
#   8. Prints the URL.
#
# Voting (on by default):
#   The deploy wraps the static lookbook with a thumbs up/down vote form per
#   look + per item. Needs a Cloudflare KV namespace id (one per account,
#   reused across lookbooks). Resolution order:
#     1. --kv-id <id>
#     2. $LOOKBOOK_VOTES_KV_ID env var
#     3. profile.md → lookbook_votes_kv_id (caller passes via --kv-id)
#   No id → the script errors out with the one-line `wrangler kv namespace
#   create` incantation. Suppress voting entirely with --no-voting.
#
#   Full architecture, schema, and security model: references/voting.md.

set -euo pipefail

show_help() {
  cat <<'HELP'
Usage: scripts/deploy-lookbook.sh <deploy-dir> <project-name> [flags]

Deploys a built lookbook directory to Cloudflare Pages with probe + idempotent
project-create + local + deployed validation gates. Voting is on by default.

Arguments:
  <deploy-dir>      Local directory containing index.html + og.jpg + assets.
                    Must already pass scripts/validate-lookbook.py --dir.
  <project-name>    Cloudflare Pages project name. Becomes the stable alias
                    URL: https://<project-name>.pages.dev/

Flags:
  --auto            Skip the per-publish "Proceed? [y/N]" confirmation prompt.
                    The caller is responsible for verifying that the customer
                    has set profile.md → preferred_lookbook_host_auto: true
                    upstream — this flag is just the wire.
  --no-overwrite    Refuse to deploy if the named project already has prior
                    deployments. Use on every customer-facing recurring run
                    so the stable alias URL is permanent. See
                    references/hosting-options.md § "URL stability".
  --dry-run         Build + run local validation; skip the actual deploy.
  --with-voting     Bake the voting capability (thumbs UI + Pages Functions
                    + KV binding) into the deploy. **On by default.**
                    Spec: references/voting.md.
  --no-voting       Suppress the voting capability — deploy a read-only
                    static lookbook with no /api/* endpoints and no form.
  --kv-id <id>      Cloudflare KV namespace id for vote storage. Required
                    when voting is on; create one once per account with:
                      CLOUDFLARE_ACCOUNT_ID=<acct> wrangler kv namespace create LOOKBOOK_VOTES
                    Resolution: --kv-id > $LOOKBOOK_VOTES_KV_ID env > error.
  --lookbook-id <s> Stable id used as the LOOKBOOK_ID env var inside the
                    Pages Functions (scopes the KV key prefix). Resolution:
                    --lookbook-id > <deploy-dir>/.lookbook_id > <project-name>
                    with the "buckmason-" prefix stripped.
  -h, --help        Show this help and exit.

Exit codes:
  0  success (or --dry-run completed)
  1  user aborted at confirmation prompt
  2  invalid arguments
  3  wrangler missing or unauthenticated
  4  --no-overwrite set but project has prior deployments
  5  voting on but no KV namespace id resolvable
  (validate failures bubble through the underlying validate-lookbook.py exit
  codes; see scripts/validate-lookbook.py --help)

Examples:
  # Default: voting baked in (needs $LOOKBOOK_VOTES_KV_ID set or --kv-id):
  bash scripts/deploy-lookbook.sh ./deploy buckmason-stylist-test \
       --kv-id 0e0b9122c04141f8b79b43d1081b3697

  # Read-only static lookbook (no voting, no /api):
  bash scripts/deploy-lookbook.sh ./deploy buckmason-stylist-test --no-voting

  # Production weekly newsletter (permanent project + voting on):
  LOOKBOOK_VOTES_KV_ID=0e0b9122c04141f8b79b43d1081b3697 \
  bash scripts/deploy-lookbook.sh \
       ~/.buck-mason-stylist/runs/2026-weekly-19/deploy \
       buckmason-nick-2026-weekly-19 \
       --auto --no-overwrite
HELP
}

# --help / -h before positional parsing so help works regardless of position.
for arg in "$@"; do
  if [ "$arg" = "--help" ] || [ "$arg" = "-h" ]; then
    show_help; exit 0
  fi
done

DEPLOY_DIR="${1:-}"
PROJECT="${2:-}"
AUTO=0
DRY_RUN=0
NO_OVERWRITE=0
WITH_VOTING=1                              # default on
KV_ID="${LOOKBOOK_VOTES_KV_ID:-}"
LOOKBOOK_ID=""
shift 2 || true
while [ $# -gt 0 ]; do
  case "$1" in
    --auto)            AUTO=1;          shift ;;
    --dry-run)         DRY_RUN=1;       shift ;;
    --no-overwrite)    NO_OVERWRITE=1;  shift ;;
    --with-voting)     WITH_VOTING=1;   shift ;;
    --no-voting)       WITH_VOTING=0;   shift ;;
    --kv-id)           KV_ID="$2";      shift 2 ;;
    --kv-id=*)         KV_ID="${1#*=}"; shift ;;
    --lookbook-id)     LOOKBOOK_ID="$2";      shift 2 ;;
    --lookbook-id=*)   LOOKBOOK_ID="${1#*=}"; shift ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
done

if [ -z "$DEPLOY_DIR" ] || [ -z "$PROJECT" ]; then
  echo "usage: $0 <deploy-dir> <project-name> [flags]" >&2
  echo "       --help for full reference" >&2
  exit 2
fi
if [ ! -d "$DEPLOY_DIR" ]; then
  echo "error: deploy dir not found: $DEPLOY_DIR" >&2
  exit 2
fi
if [ ! -f "$DEPLOY_DIR/index.html" ]; then
  echo "error: $DEPLOY_DIR has no index.html — run scripts/build-html-lookbook.py first" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TEMPLATES="$SKILL_ROOT/templates/voting"

# 1. Probe wrangler auth.
if ! command -v wrangler >/dev/null 2>&1; then
  echo "error: wrangler not installed. Run: npm i -g wrangler" >&2
  exit 3
fi
if ! wrangler whoami >/dev/null 2>&1; then
  echo "error: wrangler is not authenticated. Run: wrangler login" >&2
  exit 3
fi
echo "✓ wrangler authenticated as: $(wrangler whoami 2>&1 | grep -oE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+' | head -1)"

# 2. Confirmation gate.
PAGE_URL="https://${PROJECT}.pages.dev/"
if [ $AUTO -eq 0 ] && [ $DRY_RUN -eq 0 ]; then
  echo
  echo "About to deploy '$DEPLOY_DIR' to: $PAGE_URL"
  echo "This URL will be public (anyone with the link can view)."
  if [ $WITH_VOTING -eq 1 ]; then
    echo "Voting is ENABLED (--with-voting default). Anyone with the URL can submit votes."
  else
    echo "Voting is DISABLED (--no-voting)."
  fi
  printf "Proceed? [y/N] "
  read -r answer
  case "$answer" in
    y|Y|yes|YES) ;;
    *) echo "aborted by user."; exit 1 ;;
  esac
fi

# 3. Idempotent project create + URL-stability gate.
if wrangler pages project list 2>/dev/null | grep -qE "(^|[[:space:]])${PROJECT}([[:space:]]|$)"; then
  echo "✓ Pages project exists: $PROJECT"
  if [ $NO_OVERWRITE -eq 1 ]; then
    deploy_count=$(wrangler pages deployment list --project-name "$PROJECT" 2>/dev/null \
                   | grep -cE '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}' || echo 0)
    if [ "$deploy_count" -gt 0 ]; then
      echo "error: --no-overwrite set, but project '$PROJECT' has $deploy_count prior deployment(s)." >&2
      echo "       Deploying would overwrite the stable alias https://${PROJECT}.pages.dev/." >&2
      echo "       Use a fresh project name, or drop --no-overwrite for test/iteration deploys." >&2
      exit 4
    fi
  fi
else
  echo "Creating Pages project: $PROJECT"
  wrangler pages project create "$PROJECT" --production-branch main
fi

# 4. Bake voting into the deploy dir (default; --no-voting suppresses).
if [ $WITH_VOTING -eq 1 ]; then
  if [ -z "$KV_ID" ]; then
    cat <<EOF >&2
error: voting is enabled but no KV namespace id resolvable.

Provide via one of (highest precedence first):
  --kv-id <namespace-id>
  LOOKBOOK_VOTES_KV_ID=<namespace-id> $0 ...

To create the namespace (once per Cloudflare account):
  CLOUDFLARE_ACCOUNT_ID=<account-id> wrangler kv namespace create LOOKBOOK_VOTES
Save the returned id in profile.md as 'lookbook_votes_kv_id:' for reuse.

Or pass --no-voting to deploy a read-only static lookbook.
EOF
    exit 5
  fi
  # Resolve LOOKBOOK_ID: flag > marker file > project-name-derived.
  if [ -z "$LOOKBOOK_ID" ]; then
    if [ -f "$DEPLOY_DIR/.lookbook_id" ]; then
      LOOKBOOK_ID="$(tr -d '[:space:]' < "$DEPLOY_DIR/.lookbook_id")"
    else
      LOOKBOOK_ID="${PROJECT#buckmason-}"
    fi
  fi
  echo "✓ voting on — KV id: ${KV_ID:0:8}... · lookbook_id: $LOOKBOOK_ID"

  # 4a. Copy Pages Functions
  mkdir -p "$DEPLOY_DIR/functions/api"
  cp "$TEMPLATES/functions-api-vote.js"  "$DEPLOY_DIR/functions/api/vote.js"
  cp "$TEMPLATES/functions-api-votes.js" "$DEPLOY_DIR/functions/api/votes.js"

  # 4b. Render wrangler.toml from template (sed-substitute placeholders).
  sed -e "s|<PROJECT_NAME>|$PROJECT|g" \
      -e "s|<LOOKBOOK_ID>|$LOOKBOOK_ID|g" \
      -e "s|<KV_NAMESPACE_ID>|$KV_ID|g" \
      "$TEMPLATES/wrangler.toml.example" > "$DEPLOY_DIR/wrangler.toml"

  # 4c. Pull Buck Mason favicons (idempotent — skip if already present).
  if [ ! -f "$DEPLOY_DIR/favicon.ico" ]; then
    curl -sS -o "$DEPLOY_DIR/favicon-32.png"       "https://www.buckmason.com/favicon-32x32.png"  || true
    curl -sS -o "$DEPLOY_DIR/favicon-16.png"       "https://www.buckmason.com/icons/icon-48x48.png" || true
    curl -sS -o "$DEPLOY_DIR/apple-touch-icon.png" "https://www.buckmason.com/icons/icon-192x192.png" || true
    curl -sS -o "$DEPLOY_DIR/favicon.ico"          "https://www.buckmason.com/favicon.ico"        || true
  fi

  # 4d. Inject thumbs UI + favicon link tags into index.html.
  python3 "$SCRIPT_DIR/inject-voting-ui.py" --deploy-dir "$DEPLOY_DIR"
fi

# 5. Local validation.
echo
echo "Running local validation..."
python3 "$SCRIPT_DIR/validate-lookbook.py" --dir "$DEPLOY_DIR"
echo "✓ local validation passed"

if [ $DRY_RUN -eq 1 ]; then
  echo
  echo "--dry-run: skipping wrangler pages deploy"
  exit 0
fi

# 6. Deploy.
echo
echo "Deploying..."
if [ $WITH_VOTING -eq 1 ]; then
  # cd into the deploy dir so wrangler picks up our wrangler.toml + functions/.
  ( cd "$DEPLOY_DIR" && wrangler pages deploy . \
      --project-name "$PROJECT" \
      --branch main \
      --commit-dirty=true )
else
  wrangler pages deploy "$DEPLOY_DIR" \
    --project-name "$PROJECT" \
    --branch main \
    --commit-dirty=true
fi

# Give the CDN a few seconds to propagate before we curl it.
sleep 3

# 7. Deployed validation + voting smoke-test.
echo
echo "Running deployed validation against: $PAGE_URL"
python3 "$SCRIPT_DIR/validate-lookbook.py" --url "$PAGE_URL"
echo "✓ deployed validation passed"

if [ $WITH_VOTING -eq 1 ]; then
  if curl -sS -o /dev/null -w "%{http_code}" "${PAGE_URL}api/votes" | grep -q '^200$'; then
    echo "✓ voting endpoint live: ${PAGE_URL}api/votes"
  else
    echo "warn: voting endpoint did not return 200 (cold-start can take a few seconds)" >&2
  fi
fi

# 8. Print URL (the only thing that goes to stdout for headless callers).
echo
echo "$PAGE_URL"
