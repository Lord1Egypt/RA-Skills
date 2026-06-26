#!/usr/bin/env bash
# =============================================================================
# usage.sh — Query Anthropic Admin API for token usage reports
# =============================================================================
# Usage:
#   bash scripts/usage.sh [--daily] [--weekly] [--monthly] [--breakdown]
#
# Flags can be combined, e.g.:
#   bash scripts/usage.sh --weekly --breakdown
#
# Requirements: curl, jq
# =============================================================================

set -euo pipefail

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------

# Anthropic API endpoint for usage reports.
API_BASE="https://api.anthropic.com/v1/organizations/usage_report/messages"

# The API version header required by Anthropic.
API_VERSION="2023-06-01"

# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------

# Print an error message to stderr and exit with a non-zero status.
die() {
  echo "ERROR: $*" >&2
  exit 1
}

# Print usage/help text.
usage() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Query the Anthropic Admin API for token usage reports.

Options:
  --daily       Show today's usage
  --weekly      Show the past 7 days of usage (default)
  --monthly     Show the past 30 days of usage
  --breakdown   Group results by model
  --check       Verify the API key is valid (no usage data fetched)
  --help        Show this help message

Examples:
  $(basename "$0") --daily
  $(basename "$0") --weekly --breakdown
  $(basename "$0") --monthly --breakdown
EOF
}

# Check that a required command is available on PATH.
require_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "'$1' is required but not installed. Please install it and retry."
}

# -----------------------------------------------------------------------------
# DATE UTILITIES (GNU/BSD compatible)
# -----------------------------------------------------------------------------
# Linux ships with GNU coreutils; macOS ships with BSD date.
# Their flags for date arithmetic are different, so we detect which one we have.

# Returns an RFC3339 timestamp (e.g. 2024-03-01T00:00:00Z) for N days ago.
# Usage: date_n_days_ago <N>
date_n_days_ago() {
  local n="$1"
  if date --version >/dev/null 2>&1; then
    # GNU date (Linux)
    date -u -d "${n} days ago" '+%Y-%m-%dT00:00:00Z'
  else
    # BSD date (macOS)
    date -u -v"-${n}d" '+%Y-%m-%dT00:00:00Z'
  fi
}

# Returns today's date as an RFC3339 timestamp at midnight UTC.
today_utc() {
  date -u '+%Y-%m-%dT00:00:00Z'
}

# Returns tomorrow's date (exclusive end of today's range) in RFC3339.
tomorrow_utc() {
  if date --version >/dev/null 2>&1; then
    # GNU date
    date -u -d "tomorrow" '+%Y-%m-%dT00:00:00Z'
  else
    # BSD date
    date -u -v+1d '+%Y-%m-%dT00:00:00Z'
  fi
}

# -----------------------------------------------------------------------------
# NUMBER FORMATTING
# -----------------------------------------------------------------------------

# Add comma separators to a number (e.g. 1234567 → 1,234,567).
# Uses awk for portability (no LC_ALL tricks needed).
format_number() {
  echo "$1" | awk '{
    n = int($1); s = ""
    while (n >= 1000) { s = "," sprintf("%03d", n % 1000) s; n = int(n / 1000) }
    print n s
  }'
}

# -----------------------------------------------------------------------------
# API CALL
# -----------------------------------------------------------------------------

# Temp file used by _curl_usage; created once and cleaned up on exit.
_BODY_TMP=$(mktemp)
trap 'rm -f "${_BODY_TMP}"' EXIT

# Make a single HTTP request to the Anthropic usage API.
# Prints the response body to stdout on success, or exits with an error on failure.
# Arguments:
#   $1 — full URL (including query string)
_curl_usage() {
  local url="$1"
  local http_code

  # --connect-timeout: abort if TCP handshake takes longer than 10 s.
  # --max-time: abort the entire request (including response body) after 30 s.
  # Writing the body to a temp file avoids the fragile "strip last newline" pattern
  # that would otherwise corrupt JSON bodies ending with a newline character.
  # The set +x guard prevents the API key from leaking into shell trace output.
  { set +x
    http_code=$(curl -s -o "${_BODY_TMP}" -w "%{http_code}" \
      --connect-timeout 10 \
      --max-time 30 \
      -H "x-api-key: ${ANTHROPIC_ADMIN_API_KEY}" \
      -H "anthropic-version: ${API_VERSION}" \
      "${url}")
  } 2>/dev/null || die "Network error: curl failed (timed out or connection refused). Check your internet connection."

  case "$http_code" in
    200) ;;
    401) die "401 Unauthorized — your API key is invalid or has been revoked. Re-generate it in the Anthropic Console and set ANTHROPIC_ADMIN_API_KEY." ;;
    403) die "403 Forbidden — your key lacks Admin permissions, or your account is not on an Anthropic Organization plan. Usage reports require an Organization account." ;;
    404) die "404 Not Found — the usage report endpoint was not found. The API URL may have changed; please check for an updated version of this script." ;;
    429) die "429 Too Many Requests — you are being rate-limited. Wait a moment and try again." ;;
    5*)  die "Server error (HTTP ${http_code}) — the Anthropic API returned an unexpected error. Try again in a few minutes." ;;
    *)   die "Unexpected HTTP status ${http_code}. Response: $(cat "${_BODY_TMP}")" ;;
  esac

  cat "${_BODY_TMP}"
}

# Call the Anthropic usage API, following pagination until all buckets are
# collected. Returns a single JSON object with a "data" array that merges
# every page: { "data": [ ...all buckets... ] }
#
# Arguments:
#   $1 — starting_at (RFC3339)
#   $2 — ending_at   (RFC3339)
#   $3 — group_by    ("model" or "" for no grouping)
fetch_usage() {
  local starting_at="$1"
  local ending_at="$2"
  local group_by="$3"

  # Base query string. bucket_width=1d gives per-day granularity.
  local base_query="starting_at=${starting_at}&ending_at=${ending_at}&bucket_width=1d"
  if [[ -n "$group_by" ]]; then
    base_query="${base_query}&group_by%5B%5D=${group_by}"
  fi

  # With bucket_width=1d the API returns at most 31 buckets per page.
  # A 30-day window therefore needs at most 1 page; 100 is a hard ceiling
  # that guards against an infinite loop if the API misbehaves.
  local MAX_PAGES=100

  # Accumulate all data buckets across pages into a JSON array.
  local all_data="[]"
  local page_token=""
  local page_num=0

  while true; do
    if (( page_num >= MAX_PAGES )); then
      die "Pagination safety limit reached (${MAX_PAGES} pages). The API may be returning unexpected results."
    fi

    local query="$base_query"
    if [[ -n "$page_token" ]]; then
      query="${query}&page=${page_token}"
    fi

    local body
    body=$(_curl_usage "${API_BASE}?${query}")
    page_num=$(( page_num + 1 ))

    # Validate that the response contains a "data" array before merging.
    # jq exits non-zero and prints to stderr if the field is missing or not an array,
    # which causes the || die branch to fire with a clear message.
    if ! echo "$body" | jq -e '.data | arrays' > /dev/null 2>&1; then
      die "Malformed API response on page ${page_num}: missing or invalid 'data' field. Response: ${body}"
    fi

    # Merge this page's buckets into the accumulated array.
    all_data=$(printf '%s\n%s' "$all_data" "$body" \
      | jq -s '.[0] + .[1].data')

    # Check for more pages.
    local has_more next_page
    has_more=$(echo "$body" | jq -r '.has_more // false')
    next_page=$(echo "$body" | jq -r '.next_page // ""')

    if [[ "$has_more" != "true" || -z "$next_page" ]]; then
      break
    fi

    page_token="$next_page"
  done

  # Emit a single envelope with the complete data array.
  jq -n --argjson data "$all_data" '{"data": $data}'
}

# -----------------------------------------------------------------------------
# RENDERING
# -----------------------------------------------------------------------------

# Print a markdown-friendly table of aggregated usage (no model breakdown).
#
# The API response structure (per bucket):
#   .data[] = { starting_at, ending_at, results: [ { uncached_input_tokens,
#               cache_read_input_tokens, cache_creation: { ephemeral_1h_input_tokens,
#               ephemeral_5m_input_tokens }, output_tokens,
#               server_tool_use: { web_search_requests }, ... } ] }
#
# "Input tokens" follows Anthropic's billing definition:
#   uncached input + cache reads + cache creation (both TTLs)
render_summary() {
  local label="$1"
  local json="$2"

  local total_uncached total_cache_read total_cache_creation total_output total_web_searches
  read -r total_uncached total_cache_read total_cache_creation total_output total_web_searches \
    < <(echo "$json" | jq -r '
      [
        ([.data[].results[].uncached_input_tokens // 0] | add // 0),
        ([.data[].results[].cache_read_input_tokens // 0] | add // 0),
        ([.data[].results[] |
            ((.cache_creation.ephemeral_1h_input_tokens // 0) +
             (.cache_creation.ephemeral_5m_input_tokens // 0))
          ] | add // 0),
        ([.data[].results[].output_tokens // 0] | add // 0),
        ([.data[].results[].server_tool_use.web_search_requests // 0] | add // 0)
      ] | @tsv
    ')

  local total_input
  total_input=$(( total_uncached + total_cache_read + total_cache_creation ))

  echo ""
  echo "## ${label}"
  echo ""
  echo "| Metric                  | Value                        |"
  echo "|-------------------------|------------------------------|"
  printf "| Uncached input tokens   | %-28s |\n" "$(format_number "$total_uncached")"
  printf "| Cache read tokens       | %-28s |\n" "$(format_number "$total_cache_read")"
  printf "| Cache creation tokens   | %-28s |\n" "$(format_number "$total_cache_creation")"
  printf "| Total input tokens      | %-28s |\n" "$(format_number "$total_input")"
  printf "| Output tokens           | %-28s |\n" "$(format_number "$total_output")"
  printf "| Total tokens            | %-28s |\n" "$(format_number "$(( total_input + total_output ))")"
  printf "| Web search requests     | %-28s |\n" "$(format_number "$total_web_searches")"
  echo ""
}

# Print a markdown-friendly table broken down by model.
render_breakdown() {
  local label="$1"
  local json="$2"

  echo ""
  echo "## ${label} — by model"
  echo ""
  echo "| Model                                    | Input tokens  | Output tokens | Web searches |"
  echo "|------------------------------------------|---------------|---------------|--------------|"

  # Aggregate per model across all buckets and pages.
  # Input = uncached + cache_read + cache_creation (both TTLs).
  echo "$json" | jq -r '
    reduce (.data[].results[]) as $r (
      {};
      ($r.model // "unknown") as $model |
      .[$model].input  += (($r.uncached_input_tokens // 0)
                          + ($r.cache_read_input_tokens // 0)
                          + (($r.cache_creation // {}).ephemeral_1h_input_tokens // 0)
                          + (($r.cache_creation // {}).ephemeral_5m_input_tokens // 0)) |
      .[$model].output += ($r.output_tokens // 0) |
      .[$model].searches += ($r.server_tool_use.web_search_requests // 0)
    )
    | to_entries
    | sort_by(-.value.input)
    | .[]
    | [.key, .value.input, .value.output, .value.searches]
    | @tsv
  ' | while IFS=$'\t' read -r model input output searches; do
      printf "| %-40s | %13s | %13s | %12s |\n" \
        "$model" \
        "$(format_number "$input")" \
        "$(format_number "$output")" \
        "$(format_number "$searches")"
    done

  echo ""
}

# -----------------------------------------------------------------------------
# ARGUMENT PARSING
# -----------------------------------------------------------------------------

OPT_DAILY=false
OPT_WEEKLY=false
OPT_MONTHLY=false
OPT_BREAKDOWN=false
OPT_CHECK=false

for arg in "$@"; do
  case "$arg" in
    --daily)     OPT_DAILY=true ;;
    --weekly)    OPT_WEEKLY=true ;;
    --monthly)   OPT_MONTHLY=true ;;
    --breakdown) OPT_BREAKDOWN=true ;;
    --check)     OPT_CHECK=true ;;
    --help|-h)   usage; exit 0 ;;
    *)           die "Unknown option: ${arg}. Run with --help to see available options." ;;
  esac
done

# If none of daily/weekly/monthly was selected, default to weekly (skip for check).
if ! $OPT_DAILY && ! $OPT_WEEKLY && ! $OPT_MONTHLY && ! $OPT_CHECK; then
  echo "No period flag specified — defaulting to --weekly. Use --help to see all options." >&2
  OPT_WEEKLY=true
fi

# -----------------------------------------------------------------------------
# PRE-FLIGHT CHECKS
# -----------------------------------------------------------------------------

require_cmd curl
require_cmd jq

# Ensure the env var is set.
if [[ -z "${ANTHROPIC_ADMIN_API_KEY:-}" ]]; then
  die "ANTHROPIC_ADMIN_API_KEY is not set.

  To set it, choose one of:

  Option 1 (recommended): Add it to ~/.openclaw/openclaw.json under
    skills.entries.anthropic-usage.apiKey

  Option 2 (via chat): Ask the agent to set it for you — just paste
    your key in the chat and the agent will save it automatically.

  You can generate an Admin key in the Anthropic Console under Settings → API Keys → Admin keys.
  Your account must be on an Organization plan to access usage reports."
fi

if [[ "$ANTHROPIC_ADMIN_API_KEY" != sk-ant-admin* ]]; then
  die "Invalid API key format. Anthropic Admin keys start with 'sk-ant-admin'. Check your ANTHROPIC_ADMIN_API_KEY."
fi

# If --check was requested, validate the key via GET /v1/models and exit.
# Note: /v1/models only confirms the key is syntactically valid and accepted by the API.
# Permissions for /v1/organizations/usage_report/messages are only verified when fetching data.
if $OPT_CHECK; then
  echo "Checking API key..."
  { set +x
    http_code=$(curl -s -o /dev/null -w "%{http_code}" \
      --connect-timeout 10 \
      --max-time 30 \
      -H "x-api-key: ${ANTHROPIC_ADMIN_API_KEY}" \
      -H "anthropic-version: ${API_VERSION}" \
      "https://api.anthropic.com/v1/models")
  } 2>/dev/null
  case "$http_code" in
    200) echo "OK — key is valid (verified via /v1/models). Note: usage endpoint permissions are only confirmed when fetching data." ; exit 0 ;;
    401) die "401 Unauthorized — key is invalid, expired, or has a typo. Re-generate it in the Anthropic Console." ;;
    403) die "403 Forbidden — key lacks the required permissions, or your account is not on an Organization plan." ;;
    000) die "Network error — could not reach api.anthropic.com. Check your internet connection." ;;
    *)   die "Unexpected HTTP ${http_code} — check the Anthropic API status at https://status.anthropic.com." ;;
  esac
fi

# -----------------------------------------------------------------------------
# GROUP_BY FLAG
# -----------------------------------------------------------------------------

# If --breakdown was requested, we pass group_by=model to the API.
GROUP_BY=""
if $OPT_BREAKDOWN; then
  GROUP_BY="model"
fi

# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------

echo "Querying Anthropic usage API..."

# Compute all boundary timestamps once so every period uses the same END and
# the same reference point, even if the clock ticks past midnight mid-run.
TODAY=$(date -u '+%Y-%m-%d')
END=$(tomorrow_utc)
START_DAILY=$(today_utc)
START_WEEKLY=$(date_n_days_ago 7)
START_MONTHLY=$(date_n_days_ago 30)

# ---- Daily ------------------------------------------------------------------
if $OPT_DAILY; then
  JSON=$(fetch_usage "$START_DAILY" "$END" "$GROUP_BY")

  if $OPT_BREAKDOWN; then
    render_breakdown "Today's usage (${TODAY})" "$JSON"
  else
    render_summary "Today's usage (${TODAY})" "$JSON"
  fi
fi

# ---- Weekly -----------------------------------------------------------------
if $OPT_WEEKLY; then
  JSON=$(fetch_usage "$START_WEEKLY" "$END" "$GROUP_BY")

  if $OPT_BREAKDOWN; then
    render_breakdown "Usage — past 7 days" "$JSON"
  else
    render_summary "Usage — past 7 days" "$JSON"
  fi
fi

# ---- Monthly ----------------------------------------------------------------
if $OPT_MONTHLY; then
  JSON=$(fetch_usage "$START_MONTHLY" "$END" "$GROUP_BY")

  if $OPT_BREAKDOWN; then
    render_breakdown "Usage — past 30 days" "$JSON"
  else
    render_summary "Usage — past 30 days" "$JSON"
  fi
fi

echo "Done."