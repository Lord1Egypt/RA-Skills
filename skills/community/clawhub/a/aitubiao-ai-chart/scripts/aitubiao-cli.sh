#!/bin/bash
# =============================================================================
# aitubiao-cli.sh — Unified CLI for aitubiao API
# =============================================================================
# Encapsulates all API plumbing (URLs, headers, timeouts, retries, response
# parsing) so SKILL.md files only need to provide JSON payloads.
#
# Usage:
#   bash scripts/aitubiao-cli.sh <command> [< json-body]
#
# Commands:
#   auth <key>    Configure API Key credentials
#   check-auth    Validate credentials (no API call)
#   quota         Get user balance and project quota
#   create-chart  Create chart visualization project
#   create-ppt    Create PPT presentation project
#   create-sankey Create Sankey diagram project
#   create-3d     Create 3D illustration image
#   download-project Download a project export file locally
#   help          Show this help
#
# Exit Codes:
#   0  Success (stdout = .data JSON)
#   1  Auth error (missing/invalid credentials, HTTP 401/403)
#   2  Business error (code != 0: insufficient balance, project limit, etc.)
#   3  Network/timeout error
#   4  Usage error (bad arguments, missing jq)
# =============================================================================

set -euo pipefail

# Force UTF-8 locale so jq, curl, and shell string handling preserve non-ASCII
# bytes verbatim. Critical on Windows / Git Bash where the default locale is
# often a non-UTF-8 Windows code page (GBK, CP1252) which mangles Chinese text.
export LANG="${LANG:-C.UTF-8}"
export LC_ALL="${LC_ALL:-C.UTF-8}"
if [[ -n "${MSYSTEM:-}" ]]; then
  export LANG=C.UTF-8
  export LC_ALL=C.UTF-8
fi

CREDENTIALS_FILE="$HOME/.aitubiao/credentials"
BODY_FILE=""

# ── Dependencies ──

check_jq() {
  if ! command -v jq &>/dev/null; then
    echo "Error: jq is required but not installed." >&2
    echo "Install it with: sudo apt install jq  (or brew install jq on macOS)" >&2
    exit 4
  fi
}

# ── Credentials ──

load_credentials() {
  if [[ ! -f "$CREDENTIALS_FILE" ]]; then
    echo "Error: Credentials file not found at $CREDENTIALS_FILE" >&2
    echo "Please configure credentials first. See SKILL.md for setup instructions." >&2
    exit 1
  fi

  source "$CREDENTIALS_FILE"

  if [[ -z "${API_KEY:-}" ]]; then
    echo "Error: API_KEY is empty in $CREDENTIALS_FILE" >&2
    echo "Please add your API Key. Get one at: https://app.aitubiao.com/setting/api-keys" >&2
    exit 1
  fi

  if [[ ! "${API_KEY}" =~ ^sk_v1_ ]]; then
    echo "Error: API_KEY format invalid (must start with sk_v1_)" >&2
    echo "Your current key may have expired. Create a new one at: https://app.aitubiao.com/setting/api-keys" >&2
    exit 1
  fi

  export BASE_URL="${BASE_URL:-https://api.aitubiao.com}"
  export CHANNEL="${CHANNEL:-skill-clawhub}"

  if [[ "$BASE_URL" != "https://api.aitubiao.com" ]]; then
    echo "Error: BASE_URL in $CREDENTIALS_FILE does not match this CLI's expected endpoint" >&2
    echo "  Expected: https://api.aitubiao.com" >&2
    echo "  Current: $BASE_URL" >&2
    printf '  Re-run: bash %q auth <your-api-key>\n' "$0" >&2
    exit 1
  fi

  if [[ -z "$CHANNEL" ]]; then
    echo "Error: CHANNEL is empty in $CREDENTIALS_FILE" >&2
    exit 1
  fi
}

# ── HTTP Engine ──

api_request() {
  local method="$1"
  local path="$2"
  local timeout="$3"
  local body="${4:-}"
  local retryable="${5:-true}"

  local url="${BASE_URL}${path}?channel=${CHANNEL}"
  local http_code
  local response
  local tmp_body
  tmp_body=$(mktemp)
  local tmp_headers
  tmp_headers=$(mktemp)
  local tmp_request=""
  if [[ -n "$body" ]]; then
    tmp_request=$(mktemp)
    printf '%s' "$body" > "$tmp_request"
  fi
  trap "rm -f '$tmp_body' '$tmp_headers' ${tmp_request:+'$tmp_request'}" RETURN

  local max_attempts=1
  if [[ "$retryable" == "true" ]]; then
    max_attempts=3
  fi

  local attempt=0
  while (( attempt < max_attempts )); do
    attempt=$((attempt + 1))

    local curl_args=(
      -s
      --max-time "$timeout"
      -X "$method"
      -H "Authorization: Bearer ${API_KEY}"
      -w '%{http_code}'
      -o "$tmp_body"
      -D "$tmp_headers"
    )

    if [[ -n "$body" ]]; then
      curl_args+=(-H "Content-Type: application/json; charset=utf-8" --data-binary "@$tmp_request")
    fi

    local curl_exit=0
    http_code=$(curl "${curl_args[@]}" "$url" 2>/dev/null) || curl_exit=$?

    if (( curl_exit == 28 )); then
      if [[ "$retryable" == "true" ]] && (( attempt < max_attempts )); then
        echo "Timeout on attempt $attempt/$max_attempts, retrying in 5s..." >&2
        sleep 5
        continue
      fi
      echo "Error: Request timed out after ${timeout}s" >&2
      exit 3
    fi

    if (( curl_exit != 0 )); then
      if [[ "$retryable" == "true" ]] && (( attempt < max_attempts )); then
        echo "Network error (curl exit $curl_exit) on attempt $attempt/$max_attempts, retrying in 5s..." >&2
        sleep 5
        continue
      fi
      echo "Error: Network error (curl exit code: $curl_exit)" >&2
      exit 3
    fi

    response=$(cat "$tmp_body" 2>/dev/null || true)

    case "$http_code" in
      401|403)
        echo "Error: Authentication failed (HTTP $http_code)" >&2
        echo "Check or recreate your API Key at: https://app.aitubiao.com/setting/api-keys" >&2
        exit 1
        ;;
      429)
        if (( attempt >= max_attempts )); then
          echo "Error: Rate limited (HTTP 429) after $attempt attempts" >&2
          exit 3
        fi
        echo "Rate limited (HTTP 429), waiting 30s (attempt $attempt/$max_attempts)..." >&2
        sleep 30
        continue
        ;;
      5*)
        if [[ "$retryable" == "true" ]] && (( attempt < max_attempts )); then
          echo "Server error (HTTP $http_code) on attempt $attempt/$max_attempts, retrying in 5s..." >&2
          sleep 5
          continue
        fi
        echo "Error: Server error (HTTP $http_code)" >&2
        if [[ -n "$response" ]]; then
          echo "$response"
        fi
        exit 3
        ;;
      2*)
        break
        ;;
      *)
        echo "Error: Unexpected HTTP status $http_code" >&2
        if [[ -n "$response" ]]; then
          echo "$response"
        fi
        exit 3
        ;;
    esac
  done

  if [[ -z "$response" ]]; then
    echo "Error: Empty response from server" >&2
    exit 3
  fi

  local code
  code=$(echo "$response" | jq -r '.code // empty' 2>/dev/null || true)

  if [[ -z "$code" ]]; then
    echo "Error: Invalid response format (missing code field)" >&2
    echo "$response" >&2
    exit 3
  fi

  if [[ "$code" != "0" ]]; then
    local msg
    msg=$(echo "$response" | jq -r '.msg // "Unknown error"' 2>/dev/null)
    echo "Error: Business error (code=$code): $msg" >&2
    echo "$response"
    exit 2
  fi

  echo "$response" | jq '.data'
}

read_stdin_body() {
  local body=""
  if [[ -n "${BODY_FILE:-}" ]]; then
    if [[ ! -f "$BODY_FILE" ]]; then
      echo "Error: --body-file not found: $BODY_FILE" >&2
      exit 4
    fi
    body=$(cat -- "$BODY_FILE")
  elif [[ ! -t 0 ]]; then
    body=$(cat)
  fi
  # Strip UTF-8 BOM (some Windows editors add it) and stray CRs (CRLF safety).
  body="${body#$'\xef\xbb\xbf'}"
  body="${body//$'\r'/}"
  if [[ -z "$body" ]]; then
    echo "Error: JSON body required (use stdin heredoc/pipe or --body-file <path>)" >&2
    exit 4
  fi
  if ! printf '%s' "$body" | jq empty 2>/dev/null; then
    echo "Error: Invalid JSON in request body" >&2
    exit 4
  fi
  printf '%s' "$body"
}

# ── Commands ──

cmd_auth() {
  local api_key="${1:-}"
  if [[ -z "$api_key" ]]; then
    echo "Error: API Key required. Usage: aitubiao-cli.sh auth <sk_v1_...>" >&2
    echo "Get one at: https://app.aitubiao.com/setting/api-keys" >&2
    exit 4
  fi

  if [[ ! "$api_key" =~ ^sk_v1_ ]]; then
    echo "Error: Invalid API Key format (must start with sk_v1_)" >&2
    echo "Get a valid key at: https://app.aitubiao.com/setting/api-keys" >&2
    exit 4
  fi

  mkdir -p "$(dirname "$CREDENTIALS_FILE")"
  cat > "$CREDENTIALS_FILE" << EOF
API_KEY=$api_key
BASE_URL=https://api.aitubiao.com
CHANNEL=skill-clawhub
EOF
  chmod 600 "$CREDENTIALS_FILE"

  echo "Credentials saved to $CREDENTIALS_FILE"
  echo "  API_KEY: ${api_key:0:12}...${api_key: -4}"
  echo "  BASE_URL: https://api.aitubiao.com"
  echo "  CHANNEL: skill-aitubiao"
}

cmd_check_auth() {
  load_credentials
  echo "Credentials OK"
  echo "  API_KEY: ${API_KEY:0:12}...${API_KEY: -4}"
  echo "  BASE_URL: $BASE_URL"
  echo "  CHANNEL: $CHANNEL"
}

cmd_quota() {
  load_credentials

  local skill=""
  while (($#)); do
    case "$1" in
      --skill)
        skill="${2:-}"
        shift 2 || { echo "Error: --skill requires a value" >&2; exit 4; }
        ;;
      *)
        echo "Error: Unknown quota arg '$1'" >&2
        echo "Usage: quota [--skill chart|ppt|sankey|3d]" >&2
        exit 4
        ;;
    esac
  done

  local feature_key=""
  if [[ -n "$skill" ]]; then
    case "$skill" in
      chart)  feature_key="chartProject" ;;
      ppt)    feature_key="pptProjectCreate" ;;
      sankey) feature_key="sankeyProject" ;;
      3d)     feature_key="chart3dIllustrationCreate" ;;
      *)
        echo "Error: Unknown skill: $skill. Valid: chart, ppt, sankey, 3d" >&2
        exit 2
        ;;
    esac
  fi

  local raw
  raw=$(api_request GET "/api/v1/agent/quota" 10 "" "true")

  if [[ -z "$feature_key" ]]; then
    echo "$raw"
    return 0
  fi

  local has_feature
  has_feature=$(echo "$raw" | jq --arg k "$feature_key" 'if (.features // {}) | has($k) then "1" else "0" end')
  if [[ "$has_feature" != "\"1\"" && "$has_feature" != "1" ]]; then
    echo "Warning: feature '$feature_key' (skill=$skill) not present in server response; .feature will be null" >&2
  fi

  echo "$raw" | jq --arg k "$feature_key" '.feature = (.features[$k] // null) | del(.features)'
}

cmd_create_chart() {
  load_credentials
  local body
  body=$(read_stdin_body)
  api_request POST "/api/v1/agent/chart/create-project" 120 "$body" "false"
}

cmd_create_ppt() {
  load_credentials
  local body
  body=$(read_stdin_body)
  api_request POST "/api/v1/agent/infographic/create-project" 120 "$body" "false"
}

cmd_create_sankey() {
  load_credentials
  local body
  body=$(read_stdin_body)
  api_request POST "/api/v1/agent/chart/create-sankey-project" 120 "$body" "false"
}

cmd_create_3d() {
  load_credentials
  local body
  body=$(read_stdin_body)
  api_request POST "/api/v1/agent/chart/create-3d-illustration" 180 "$body" "false"
}

resolve_absolute_path() {
  # Resolve a (possibly relative) path to an absolute path WITHOUT requiring
  # the file to exist. Resolves the parent dir via cd; appends the basename.
  local path="$1"
  local dir base abs_dir
  dir=$(dirname -- "$path")
  base=$(basename -- "$path")
  abs_dir=$(cd "$dir" 2>/dev/null && pwd) || {
    echo "$path"
    return 0
  }
  printf '%s/%s\n' "$abs_dir" "$base"
}

ensure_writable_dir() {
  local dir="$1"
  if ! mkdir -p "$dir" 2>/dev/null; then
    echo "Error: Output directory cannot be created (permission denied or invalid path): $dir" >&2
    echo "Please specify a writable path (e.g. \"\$HOME/Downloads/<filename>\")." >&2
    exit 4
  fi
  if [[ ! -w "$dir" ]]; then
    echo "Error: Output directory is not writable: $dir" >&2
    echo "Please specify a writable path (e.g. \"\$HOME/Downloads/<filename>\")." >&2
    exit 4
  fi
}

verify_downloaded_file() {
  # Sanity-check a downloaded file: non-empty + magic-byte match.
  # Multi-page exports of png/jpg/pdf come back as a ZIP bundle from the server,
  # so png/jpg/pdf accept the corresponding single-file magic OR a ZIP container.
  # On success, prints the *actual* detected format (png|jpg|pdf|ppt|zip|unknown)
  # to stdout and returns 0. On corruption returns 1.
  local path="$1"
  local format="$2"

  if [[ ! -s "$path" ]]; then
    echo "Error: Downloaded file is empty: $path" >&2
    return 1
  fi

  local magic
  magic=$(head -c 8 -- "$path" 2>/dev/null | od -An -tx1 | tr -d ' \n')

  local is_zip="false"
  case "$magic" in
    504b0304*|504b0506*|504b0708*) is_zip="true" ;;
  esac

  case "$format" in
    png)
      if [[ "$magic" == 89504e470d0a1a0a* ]]; then printf 'png\n'; return 0; fi
      [[ "$is_zip" == "true" ]] && { printf 'zip\n'; return 0; }
      return 1
      ;;
    jpg|jpeg)
      if [[ "$magic" == ffd8ff* ]]; then printf 'jpg\n'; return 0; fi
      [[ "$is_zip" == "true" ]] && { printf 'zip\n'; return 0; }
      return 1
      ;;
    pdf)
      # %PDF-
      if [[ "$magic" == 25504446* ]]; then printf 'pdf\n'; return 0; fi
      [[ "$is_zip" == "true" ]] && { printf 'zip\n'; return 0; }
      return 1
      ;;
    ppt|pptx|zip)
      # PPTX is a ZIP container; legacy .ppt is OLE2 (D0CF11E0...).
      if [[ "$is_zip" == "true" ]]; then printf 'zip\n'; return 0; fi
      [[ "$magic" == d0cf11e0a1b11ae1* ]] && { printf 'ppt\n'; return 0; }
      return 1
      ;;
    *)
      printf 'unknown\n'
      ;;
  esac
  return 0
}

download_attachment() {
  # Returns the final saved path on stdout (may differ from requested path if
  # the server wrapped a multi-page export into a ZIP bundle).
  local url="$1"
  local output_path="$2"
  local format="${3:-}"

  local out_dir
  out_dir=$(dirname -- "$output_path")
  ensure_writable_dir "$out_dir"

  local tmp_path="${output_path}.partial"
  rm -f -- "$tmp_path"

  if ! curl -L --fail --silent --show-error \
        --connect-timeout 30 \
        --max-time 600 \
        --retry 3 \
        --retry-delay 5 \
        --retry-all-errors \
        -o "$tmp_path" \
        "$url"; then
    rm -f -- "$tmp_path"
    echo "Error: Failed to download attachment from $url" >&2
    exit 3
  fi

  local detected
  if ! detected=$(verify_downloaded_file "$tmp_path" "$format"); then
    echo "Error: Downloaded file failed integrity check (format=$format): $tmp_path" >&2
    rm -f -- "$tmp_path"
    exit 3
  fi

  # If the requested format was a single-file format (png/jpg/pdf) but the
  # server returned a ZIP bundle (multi-page export), retarget to a .zip path
  # so the saved filename honestly reflects its contents.
  local final_path="$output_path"
  if [[ "$detected" == "zip" && "$format" != "ppt" && "$format" != "pptx" && "$format" != "zip" ]]; then
    final_path="${output_path%.*}.zip"
    echo "Note: server returned a multi-page ZIP bundle for format=$format; saving as ${final_path}" >&2
  fi

  if ! mv -- "$tmp_path" "$final_path"; then
    echo "Error: Failed to move downloaded file to $final_path" >&2
    rm -f -- "$tmp_path"
    exit 3
  fi
  printf '%s\n' "$final_path"
}

cmd_download_project() {
  load_credentials
  local output_path="${2:-}"
  local body
  body=$(read_stdin_body)

  local project_id
  project_id=$(echo "$body" | jq -r '.projectId // empty')
  local format
  format=$(echo "$body" | jq -r '.format // empty')
  local requested_file_name
  requested_file_name=$(echo "$body" | jq -r '.fileName // empty')

  if [[ -z "$project_id" || -z "$format" ]]; then
    echo "Error: projectId and format are required" >&2
    exit 4
  fi

  local project_result
  project_result=$(api_request GET "/api/v1/projects/${project_id}" 10 "" "true")
  local pages_result
  pages_result=$(api_request GET "/api/v1/projects/${project_id}/pages" 10 "" "true")

  local selected_pages
  selected_pages=$(jq -n \
    --argjson request "$body" \
    --argjson pageData "$pages_result" '
      def selected_ids:
        if (($request.pageIds // []) | length) > 0 then ($request.pageIds // []) else $pageData.orders end;
      [selected_ids[] as $id |
        ($pageData.pages[] | select(.pageId == $id)) as $page |
        select($page != null) |
        {id: $id, name: ($page.pageName // "Untitled")}
      ]
    ')

  local expected_page_count
  expected_page_count=$(jq -n --argjson request "$body" --argjson pageData "$pages_result" 'if (($request.pageIds // []) | length) > 0 then ($request.pageIds // []) | length else $pageData.orders | length end')
  local actual_page_count
  actual_page_count=$(echo "$selected_pages" | jq 'length')
  if [[ "$actual_page_count" != "$expected_page_count" ]]; then
    echo "Error: One or more pageIds are invalid for project ${project_id}" >&2
    exit 4
  fi

  local page_ids
  page_ids=$(echo "$selected_pages" | jq -c '[.[].id]')
  local page_names
  page_names=$(echo "$selected_pages" | jq -c '[.[].name]')
  local project_name
  project_name=$(echo "$project_result" | jq -r '.title // "project"')
  local file_name
  file_name=${requested_file_name:-"${project_name}.${format}"}

  if [[ -z "$output_path" ]]; then
    output_path="$file_name"
  fi

  # Resolve to absolute path so the success JSON is unambiguous, and preflight
  # the parent directory before we burn an export-task slot on the server.
  output_path=$(resolve_absolute_path "$output_path")
  ensure_writable_dir "$(dirname -- "$output_path")"

  local export_payload
  export_payload=$(jq -n \
    --arg projectId "$project_id" \
    --arg projectName "$project_name" \
    --arg format "$format" \
    --argjson pageIds "$page_ids" \
    --argjson pageNames "$page_names" \
    --argjson width "$(echo "$project_result" | jq '.width')" \
    --argjson height "$(echo "$project_result" | jq '.height')" \
    '{projectId:$projectId, projectName:$projectName, format:$format, pageIds:$pageIds, pageNames:$pageNames, size:{width:$width, height:$height}, scale:0}')

  local start_result
  start_result=$(api_request POST "/api/v1/projects/pages/export" 120 "$export_payload" "false")

  local task_id
  task_id=$(echo "$start_result" | jq -r '.id // empty')
  if [[ -z "$task_id" ]]; then
    echo "Error: Download task id missing from response" >&2
    echo "$start_result" >&2
    exit 3
  fi

  local task_result
  local status
  local attachment
  local attempts=0
  local max_attempts=300
  while (( attempts < max_attempts )); do
    task_result=$(api_request GET "/api/v1/projects/export/task/${task_id}" 10 "" "true")
    status=$(echo "$task_result" | jq -r '.status // empty')

    if [[ "$status" == "success" ]]; then
      attachment=$(echo "$task_result" | jq -r '.attachment // empty')
      if [[ -z "$attachment" ]]; then
        echo "Error: Download attachment missing from task response" >&2
        echo "$task_result" >&2
        exit 3
      fi
      local actual_path
      actual_path=$(download_attachment "$attachment" "$output_path" "$format")
      local actual_file_name
      actual_file_name=$(basename -- "$actual_path")
      jq -n \
        --arg taskId "$task_id" \
        --arg status "$status" \
        --arg attachment "$attachment" \
        --arg savedPath "$actual_path" \
        --arg fileName "$actual_file_name" \
        '{success:true, taskId:$taskId, status:$status, attachment:$attachment, savedPath:$savedPath, fileName:$fileName}'
      return 0
    fi

    if [[ "$status" == "failed" ]]; then
      echo "Error: Download task failed" >&2
      echo "$task_result"
      exit 2
    fi

    attempts=$((attempts + 1))
    sleep 2
  done

  echo "Error: Download task timed out while waiting for export" >&2
  exit 3
}

cmd_help() {
  cat <<'HELP'
aitubiao-cli.sh — Unified CLI for aitubiao API

Usage:
  bash scripts/aitubiao-cli.sh [--body-file <path>] <command> [< json-body]

Commands:
  auth <key>    Configure API Key credentials
  check-auth    Validate credentials (no API call)
  quota            Get user balance and project quota
                   Optional: --skill chart|ppt|sankey|3d (returns only that skill's pricing)
  create-chart     Create chart visualization project (POST, JSON body)
  create-ppt       Create PPT presentation project (POST, JSON body)
  create-sankey    Create Sankey diagram project (POST, JSON body)
  create-3d        Create 3D illustration image (POST, JSON body)
  download-project Download a project export file locally (POST + poll task)
  help             Show this help

POST commands accept the JSON body via stdin OR via --body-file <path>.
On macOS / Linux, prefer the heredoc form:
  bash scripts/aitubiao-cli.sh create-chart <<'EOF'
  {
    "markdownTable": "| Month | Revenue |\n|---|-|\n| Jan | 1000 |",
    "projectName": "Sales Chart"
  }
  EOF

On Windows / Git Bash, prefer --body-file to keep UTF-8 (Chinese, etc.) intact:
  bash scripts/aitubiao-cli.sh --body-file /tmp/payload.json create-chart

Download example:
  bash scripts/aitubiao-cli.sh download-project ./demo-project.png <<'EOF'
  {
    "projectId": "project-id",
    "format": "png"
  }
  EOF

Exit Codes:
  0  Success — stdout contains .data JSON from API response
  1  Auth error — missing/invalid credentials or HTTP 401/403
  2  Business error — code != 0 (insufficient balance, project limit, etc.)
  3  Network/timeout error — server unreachable or timed out
  4  Usage error — bad arguments, missing jq, invalid JSON

Credentials:
  Stored in ~/.aitubiao/credentials with API_KEY, BASE_URL, CHANNEL.
  Use scripts/switch-channel.sh to change distribution channel.
HELP
}

# ── Dispatch ──

main() {
  check_jq

  # Pre-parse global flags (currently just --body-file) out of argv so each
  # subcommand sees a clean argument list. --body-file lets callers (typically
  # AI agents on Windows / Git Bash) hand us a UTF-8 JSON file path instead of
  # piping bytes through stdin / argv, which avoids MSYS code-page conversion.
  local args=()
  while (($#)); do
    case "$1" in
      --body-file)
        if [[ $# -lt 2 ]]; then
          echo "Error: --body-file requires a path" >&2
          exit 4
        fi
        BODY_FILE="$2"
        shift 2
        ;;
      --body-file=*)
        BODY_FILE="${1#--body-file=}"
        shift
        ;;
      *)
        args+=("$1")
        shift
        ;;
    esac
  done
  if (( ${#args[@]} > 0 )); then
    set -- "${args[@]}"
  else
    set --
  fi

  local command="${1:-help}"

  case "$command" in
    auth)         cmd_auth "${2:-}" ;;
    check-auth)   cmd_check_auth ;;
    quota)        cmd_quota "${@:2}" ;;
    create-chart) cmd_create_chart ;;
    create-ppt)   cmd_create_ppt ;;
    create-sankey) cmd_create_sankey ;;
    create-3d)    cmd_create_3d ;;
    download-project) cmd_download_project "$@" ;;
    help|--help|-h) cmd_help ;;
    *)
      echo "Error: Unknown command '$command'" >&2
      echo "Run 'bash scripts/aitubiao-cli.sh help' for usage." >&2
      exit 4
      ;;
  esac
}

main "$@"
