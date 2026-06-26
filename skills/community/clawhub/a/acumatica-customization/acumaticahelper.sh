#!/bin/bash
#
# acumaticahelper.sh — Acumatica Customization Management Helper
#
# Manages Acumatica customization projects via the CustomizationApi web API.
# All API calls follow the official "Managing Customization Projects by Using
# the Web API" reference (Acumatica ERP documentation).
#
# Commands:
#   acumaticahelper.sh list
#   acumaticahelper.sh export   <project-name> [output-dir]
#   acumaticahelper.sh import   <project.zip>  [project-name] [description]
#   acumaticahelper.sh validate <project-name> [project-name2 ...]
#   acumaticahelper.sh publish  <project-name> [project-name2 ...]
#   acumaticahelper.sh unpublish [Current|All]
#   acumaticahelper.sh delete   <project-name>
#   acumaticahelper.sh status
#
# Configuration — stored in acumatica.conf (same directory as this script):
#   ACUMATICA_URL=http://host/instance
#   ACUMATICA_USERNAME=admin
#   ACUMATICA_PASSWORD=secret
#
# Requirements: curl, jq, base64
#
# API endpoints used (all POST):
#   /entity/auth/login            — sign in, receive session cookie
#   /entity/auth/logout           — sign out
#   /CustomizationApi/getPublished  — list published projects + items
#   /CustomizationApi/getProject    — export project as Base64 ZIP
#   /CustomizationApi/import        — import project from Base64 ZIP
#   /CustomizationApi/publishBegin  — start publish or validation
#   /CustomizationApi/publishEnd    — poll publish/validation completion
#   /CustomizationApi/unpublishAll  — unpublish all projects
#   /CustomizationApi/delete        — delete an unpublished project
#
# Maintenance Mode (endpoint: Lock, version: V1):
#   PUT /entity/Lock/1/ApplyUpdate/scheduleLockoutCommand — enable maintenance mode
#   PUT /entity/Lock/1/ApplyUpdate/stopLockoutCommand     — disable maintenance mode

set -euo pipefail

# =============================================================================
# CONFIGURATION — loaded from acumatica.conf
# =============================================================================

# Resolve conf file relative to this script, not the caller's working directory
_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_CONF_FILE="${_SCRIPT_DIR}/acumatica.conf"

if [[ ! -f "$_CONF_FILE" ]]; then
    echo "Error: configuration file not found: $_CONF_FILE" >&2
    echo "Create it with the following content:" >&2
    echo "" >&2
    echo "  ACUMATICA_URL=http://host/instance" >&2
    echo "  ACUMATICA_USERNAME=admin" >&2
    echo "  ACUMATICA_PASSWORD=secret" >&2
    exit 1
fi

# Parse key=value lines; ignore blank lines and comments (#)
while IFS= read -r _line || [[ -n "$_line" ]]; do
    [[ "$_line" =~ ^[[:space:]]*$ || "$_line" =~ ^[[:space:]]*# ]] && continue
    if [[ "$_line" =~ ^([A-Za-z_][A-Za-z0-9_]*)=(.*)$ ]]; then
        declare -g "${BASH_REMATCH[1]}"="${BASH_REMATCH[2]}"
    fi
done < "$_CONF_FILE"

ACUMATICA_URL="${ACUMATICA_URL:-}"
ACUMATICA_USERNAME="${ACUMATICA_USERNAME:-}"
ACUMATICA_PASSWORD="${ACUMATICA_PASSWORD:-}"

# Poll interval and max attempts for publishEnd
PUBLISH_POLL_INTERVAL="${PUBLISH_POLL_INTERVAL:-30}"   # seconds between polls
PUBLISH_MAX_ATTEMPTS="${PUBLISH_MAX_ATTEMPTS:-10}"     # 10 × 30s = 5 min

# =============================================================================
# INTERNAL STATE
# =============================================================================

_COOKIE_FILE=""

# =============================================================================
# INTERNAL HELPERS
# =============================================================================

# Create a temp file for the session cookie
_init_cookie() {
    if [[ -z "$_COOKIE_FILE" ]]; then
        _COOKIE_FILE=$(mktemp /tmp/acumatica_cookie.XXXXXX)
    fi
}

# Remove the temp cookie file
_cleanup() {
    if [[ -n "$_COOKIE_FILE" && -f "$_COOKIE_FILE" ]]; then
        rm -f "$_COOKIE_FILE"
        _COOKIE_FILE=""
    fi
}

# Verify required config is set
_check_config() {
    local missing=()
    [[ -z "$ACUMATICA_URL"      ]] && missing+=("ACUMATICA_URL")
    [[ -z "$ACUMATICA_USERNAME" ]] && missing+=("ACUMATICA_USERNAME")
    [[ -z "$ACUMATICA_PASSWORD" ]] && missing+=("ACUMATICA_PASSWORD")
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "Error: Missing required configuration: ${missing[*]}" >&2
        echo "Add them to: $_CONF_FILE" >&2
        return 1
    fi
}

# Guard: verify response is JSON ({...} or [...]), otherwise print raw + fail
_require_json() {
    local response="$1"
    local context="${2:-}"
    local trimmed
    trimmed=$(echo "$response" | sed 's/^[[:space:]]*//')
    if [[ "$trimmed" == "{"* || "$trimmed" == "["* ]]; then
        echo "$response"
        return 0
    fi
    echo "Error${context:+: $context} — unexpected non-JSON response:" >&2
    echo "$response" >&2
    return 1
}

# Pretty-print the log[] array present in every API response
# Format: [logType] message
_print_log() {
    local response="$1"
    echo "$response" | jq -r '.log[]? | "  [\(.logType)] \(.message)"'
}

# =============================================================================
# AUTH
# =============================================================================

# Sign in via POST /entity/auth/login — stores session cookie
# Note: OAuth 2.0 is NOT supported for the CustomizationApi (per official docs)
_login() {
    _check_config || return 1
    _init_cookie

    local payload
    payload=$(jq -n \
        --arg name     "$ACUMATICA_USERNAME" \
        --arg password "$ACUMATICA_PASSWORD" \
        '{name: $name, password: $password}')

    local response_body http_code
    response_body=$(curl -s -w "\n%{http_code}" \
        -c "$_COOKIE_FILE" \
        -X POST \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "$payload" \
        "${ACUMATICA_URL}/entity/auth/login")

    # Last line is the HTTP status code, everything before is the body
    http_code=$(echo "$response_body" | tail -n1)
    response_body=$(echo "$response_body" | sed '$d')

    if [[ "$http_code" != "200" && "$http_code" != "204" ]]; then
        echo "Error: Login failed (HTTP $http_code)" >&2
        echo "URL:  ${ACUMATICA_URL}/entity/auth/login" >&2
        echo "User: ${ACUMATICA_USERNAME}" >&2
        if [[ -n "$response_body" ]]; then
            echo "Response:" >&2
            # Pretty-print if JSON, otherwise print raw
            if echo "$response_body" | jq . >/dev/null 2>&1; then
                echo "$response_body" | jq . >&2
            else
                echo "$response_body" >&2
            fi
        fi
        _cleanup
        return 1
    fi
}

# Sign out via POST /entity/auth/logout
_logout() {
    [[ -z "$_COOKIE_FILE" || ! -f "$_COOKIE_FILE" ]] && return 0
    curl -s -o /dev/null \
        -b "$_COOKIE_FILE" \
        -X POST \
        "${ACUMATICA_URL}/entity/auth/logout" || true
    _cleanup
}

# =============================================================================
# COMMANDS
# =============================================================================

# -----------------------------------------------------------------------------
# list — retrieve published projects and their customization items
#
# POST /CustomizationApi/getPublished
# Request body: (none)
# Response:
#   {
#     "projects": [ { "name": "..." }, ... ],
#     "items":    [ { "key": "...", "screenId": "...", "type": "..." }, ... ],
#     "log":      []
#   }
# -----------------------------------------------------------------------------
cmd_list() {
    _login || return 1

    echo "Querying published customization projects on ${ACUMATICA_URL}..."

    local response
    response=$(curl -s \
        -b "$_COOKIE_FILE" \
        -X POST \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "{}" \
        "${ACUMATICA_URL}/CustomizationApi/getPublished")

    _require_json "$response" "getPublished" > /dev/null || return 1

    echo ""
    echo "Published projects:"
    local count
    count=$(echo "$response" | jq '.projects | length')
    if [[ "$count" -eq 0 ]]; then
        echo "  (none)"
    else
        echo "$response" | jq -r '.projects[] | "  \(.name)"'
    fi

    echo ""
    echo "Published items (${count} project(s), $(echo "$response" | jq '.items | length') item(s)):"
    if [[ "$(echo "$response" | jq '.items | length')" -eq 0 ]]; then
        echo "  (none)"
    else
        echo "$response" | jq -r '.items[] | "  [\(.type)] \(.screenId // "-")  \(.key)"'
    fi

    _print_log "$response"
}

# -----------------------------------------------------------------------------
# export — retrieve a project's ZIP contents as a local file
#
# POST /CustomizationApi/getProject
# Request:
#   {
#     "projectName":            "<name>",   -- required
#     "IsAutoResolveConflicts": true         -- auto-merge file system changes
#   }
# Response:
#   {
#     "projectContentBase64": "<base64-zip>",
#     "hasConflicts":          false,
#     "log":                   []
#   }
# -----------------------------------------------------------------------------
cmd_export() {
    local project_name="${1:-}"
    local output_dir="${2:-.}"

    if [[ -z "$project_name" ]]; then
        echo "Usage: $0 export <project-name> [output-dir]" >&2
        return 1
    fi

    _login || return 1

    local payload
    payload=$(jq -n \
        --arg name "$project_name" \
        '{projectName: $name, IsAutoResolveConflicts: true}')

    echo "Exporting project '$project_name'..."

    local response
    response=$(curl -s \
        -b "$_COOKIE_FILE" \
        -X POST \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "$payload" \
        "${ACUMATICA_URL}/CustomizationApi/getProject")

    _require_json "$response" "getProject" > /dev/null || return 1

    local b64
    b64=$(echo "$response" | jq -r '.projectContentBase64 // empty')
    if [[ -z "$b64" ]]; then
        echo "Error: response contained no projectContentBase64" >&2
        echo "$response" | jq . >&2
        return 1
    fi

    mkdir -p "$output_dir"
    local output_file="${output_dir}/${project_name}.zip"
    local tmp_file
    tmp_file=$(mktemp "${output_dir}/.${project_name}_XXXXXX.zip")

    # Decode to a temp file first — avoids leaving a corrupt zip on failure
    if ! echo "$b64" | base64 -d > "$tmp_file" 2>/dev/null; then
        rm -f "$tmp_file"
        echo "Error: base64 decode failed — export aborted, no file written" >&2
        return 1
    fi

    # Verify the decoded file is a valid zip before keeping it
    if ! python3 -c "import zipfile, sys; zipfile.ZipFile(sys.argv[1])" "$tmp_file" 2>/dev/null; then
        rm -f "$tmp_file"
        echo "Error: decoded file is not a valid ZIP — export aborted, no file written" >&2
        return 1
    fi

    # Atomically replace any previous export
    mv -f "$tmp_file" "$output_file"
    echo "Saved: $output_file ($(du -h "$output_file" | cut -f1))"

    local has_conflicts
    has_conflicts=$(echo "$response" | jq -r '.hasConflicts // false')
    if [[ "$has_conflicts" == "true" ]]; then
        echo "Warning: hasConflicts=true — file system changes were auto-merged into the package."
    fi

    _print_log "$response"
}

# -----------------------------------------------------------------------------
# import — upload a ZIP file as a customization project
#
# POST /CustomizationApi/import
# Request:
#   {
#     "projectName":          "<name>",      -- required
#     "projectDescription":   "<desc>",
#     "projectLevel":         1,
#     "isReplaceIfExists":    true,
#     "projectContentBase64": "<base64-zip>" -- required
#   }
# Response: { "log": [] }
# -----------------------------------------------------------------------------
cmd_import() {
    local project_zip="${1:-}"
    local project_name="${2:-}"
    local project_desc="${3:-Imported by acumaticahelper.sh}"

    if [[ -z "$project_zip" || ! -f "$project_zip" ]]; then
        echo "Usage: $0 import <project.zip> [project-name] [description]" >&2
        return 1
    fi

    if [[ -z "$project_name" ]]; then
        project_name=$(basename "$project_zip" .zip)
    fi

    _login || return 1

    echo "Reading $project_zip..."
    local b64
    b64=$(base64 < "$project_zip" | tr -d '\n')

    local payload
    payload=$(jq -n \
        --arg name    "$project_name" \
        --arg desc    "$project_desc" \
        --arg content "$b64" \
        '{
            projectName:          $name,
            projectDescription:   $desc,
            projectLevel:         1,
            isReplaceIfExists:    true,
            projectContentBase64: $content
        }')

    echo "Importing '$project_name'..."

    local response
    response=$(curl -s \
        -b "$_COOKIE_FILE" \
        -X POST \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "$payload" \
        "${ACUMATICA_URL}/CustomizationApi/import")

    _require_json "$response" "import" > /dev/null || return 1
    _print_log "$response"
}

# -----------------------------------------------------------------------------
# validate — validate project(s) without publishing
#
# POST /CustomizationApi/publishBegin  { isOnlyValidation: true }
# then poll POST /CustomizationApi/publishEnd until isCompleted=true
# -----------------------------------------------------------------------------
cmd_validate() {
    if [[ $# -eq 0 ]]; then
        echo "Usage: $0 validate <project-name> [project-name2 ...]" >&2
        return 1
    fi

    _login || return 1

    local names_json
    names_json=$(printf '%s\n' "$@" | jq -R . | jq -s .)

    local payload
    payload=$(jq -n \
        --argjson names "$names_json" \
        '{
            isMergeWithExistingPackages:       false,
            isOnlyValidation:                  true,
            isOnlyDbUpdates:                   false,
            isReplayPreviouslyExecutedScripts: false,
            projectNames:                      $names,
            tenantMode:                        "Current"
        }')

    echo "Starting validation for: $*"

    local response
    response=$(curl -s \
        -b "$_COOKIE_FILE" \
        -X POST \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "$payload" \
        "${ACUMATICA_URL}/CustomizationApi/publishBegin")

    _require_json "$response" "publishBegin" > /dev/null || return 1
    _print_log "$response"

    echo "Polling publishEnd every ${PUBLISH_POLL_INTERVAL}s (max $((PUBLISH_POLL_INTERVAL * PUBLISH_MAX_ATTEMPTS))s)..."
    _poll_publish_end
}

# -----------------------------------------------------------------------------
# publish — publish one or more customization projects
#
# POST /CustomizationApi/publishBegin  { isOnlyValidation: false }
# then poll POST /CustomizationApi/publishEnd until isCompleted=true
#
# Per the docs: calling publishEnd is REQUIRED — it triggers plug-in execution.
# Without it, publication cannot complete.
# -----------------------------------------------------------------------------
cmd_publish() {
    if [[ $# -eq 0 ]]; then
        echo "Usage: $0 publish <project-name> [project-name2 ...]" >&2
        return 1
    fi

    _login || return 1

    local names_json
    names_json=$(printf '%s\n' "$@" | jq -R . | jq -s .)

    local payload
    payload=$(jq -n \
        --argjson names "$names_json" \
        '{
            isMergeWithExistingPackages:       false,
            isOnlyValidation:                  false,
            isOnlyDbUpdates:                   false,
            isReplayPreviouslyExecutedScripts: false,
            projectNames:                      $names,
            tenantMode:                        "Current"
        }')

    echo "Starting publish for: $*"

    local response
    response=$(curl -s \
        -b "$_COOKIE_FILE" \
        -X POST \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "$payload" \
        "${ACUMATICA_URL}/CustomizationApi/publishBegin")

    _require_json "$response" "publishBegin" > /dev/null || return 1
    _print_log "$response"

    echo "Polling publishEnd every ${PUBLISH_POLL_INTERVAL}s (max $((PUBLISH_POLL_INTERVAL * PUBLISH_MAX_ATTEMPTS))s)..."
    _poll_publish_end
}

# Poll POST /CustomizationApi/publishEnd until isCompleted=true
# Response: { "isCompleted": bool, "isFailed": bool, "log": [] }
_poll_publish_end() {
    local attempt=0

    while [[ $attempt -lt $PUBLISH_MAX_ATTEMPTS ]]; do
        sleep "$PUBLISH_POLL_INTERVAL"
        (( attempt++ ))

        local result
        result=$(curl -s \
            -b "$_COOKIE_FILE" \
            -X POST \
            -H "Content-Type: application/json" \
            -H "Accept: application/json" \
            -d "{}" \
            "${ACUMATICA_URL}/CustomizationApi/publishEnd")

        if ! _require_json "$result" > /dev/null 2>&1; then
            echo "  Warning: non-JSON from publishEnd, retrying... (${attempt}/${PUBLISH_MAX_ATTEMPTS})"
            continue
        fi

        local is_completed
        is_completed=$(echo "$result" | jq -r '.isCompleted // false')

        if [[ "$is_completed" == "true" ]]; then
            local is_failed
            is_failed=$(echo "$result" | jq -r '.isFailed // false')
            if [[ "$is_failed" == "true" ]]; then
                echo "Result: FAILED"
            else
                echo "Result: Success"
            fi
            _print_log "$result"
            [[ "$is_failed" == "true" ]] && return 1
            return 0
        fi

        echo "  Still in progress... (${attempt}/${PUBLISH_MAX_ATTEMPTS})"
    done

    echo "Timed out waiting for completion. Check the Acumatica instance manually." >&2
    return 1
}

# -----------------------------------------------------------------------------
# status — one-shot poll of publishEnd to check current state
#
# POST /CustomizationApi/publishEnd
# Request body: (none)
# Response: { "isCompleted": bool, "isFailed": bool, "log": [] }
# -----------------------------------------------------------------------------
cmd_status() {
    _login || return 1

    echo "Checking publish/validation status..."

    local response
    response=$(curl -s \
        -b "$_COOKIE_FILE" \
        -X POST \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "{}" \
        "${ACUMATICA_URL}/CustomizationApi/publishEnd")

    _require_json "$response" "publishEnd" > /dev/null || return 1

    echo "  isCompleted : $(echo "$response" | jq -r '.isCompleted // "unknown"')"
    echo "  isFailed    : $(echo "$response" | jq -r '.isFailed    // "unknown"')"
    _print_log "$response"
}

# -----------------------------------------------------------------------------
# unpublish — unpublish all customization projects
#
# POST /CustomizationApi/unpublishAll
# Request:
#   {
#     "tenantMode": "Current" | "All" | "List"   -- required
#   }
# Response: { "log": [] }
# -----------------------------------------------------------------------------
cmd_unpublish() {
    local tenant_mode="${1:-Current}"

    case "$tenant_mode" in
        Current|All|List) ;;
        *)
            echo "Error: tenantMode must be Current, All, or List (got: '$tenant_mode')" >&2
            return 1
            ;;
    esac

    _login || return 1

    local payload
    payload=$(jq -n --arg mode "$tenant_mode" '{tenantMode: $mode}')

    echo "Unpublishing all projects (tenantMode: $tenant_mode)..."

    local response
    response=$(curl -s \
        -b "$_COOKIE_FILE" \
        -X POST \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "$payload" \
        "${ACUMATICA_URL}/CustomizationApi/unpublishAll")

    _require_json "$response" "unpublishAll" > /dev/null || return 1
    _print_log "$response"
}

# -----------------------------------------------------------------------------
# delete — delete an unpublished customization project
#
# POST /CustomizationApi/delete
# Request:  { "projectName": "<name>" }   -- required
# Response: { "log": [] }
#
# Note: the project must NOT be currently published before deleting.
# The platform deletes project data and item data from the database, but does
# NOT delete files/objects added from the database (site map nodes, reports, etc.)
# -----------------------------------------------------------------------------
cmd_delete() {
    local project_name="${1:-}"

    if [[ -z "$project_name" ]]; then
        echo "Usage: $0 delete <project-name>" >&2
        return 1
    fi

    _login || return 1

    local payload
    payload=$(jq -n --arg name "$project_name" '{projectName: $name}')

    echo "Deleting project '$project_name'..."

    local response
    response=$(curl -s \
        -b "$_COOKIE_FILE" \
        -X POST \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "$payload" \
        "${ACUMATICA_URL}/CustomizationApi/delete")

    _require_json "$response" "delete" > /dev/null || return 1
    _print_log "$response"
}

# -----------------------------------------------------------------------------
# maintenance-on — put the instance into maintenance mode
#
# PUT /entity/Lock/1/ApplyUpdate/scheduleLockoutCommand
# Endpoint name: Lock  |  Version: V1
# Request body: (none)
# Response: HTTP 204 No Content on success
# -----------------------------------------------------------------------------
cmd_maintenance_on() {
    _login || return 1

    local url="${ACUMATICA_URL}/entity/Lock/1/ApplyUpdate/scheduleLockoutCommand"
    echo "Enabling maintenance mode..."
    echo "  Request : PUT $url"

    local response_body http_code
    response_body=$(curl -s -w "\n%{http_code}" \
        -b "$_COOKIE_FILE" \
        -X PUT \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "" \
        "$url")

    http_code=$(echo "$response_body" | tail -n1)
    response_body=$(echo "$response_body" | sed '$d')

    echo "  Response: HTTP $http_code"

    if [[ "$http_code" == "204" || "$http_code" == "200" ]]; then
        echo "Maintenance mode enabled."
    else
        echo "Error: Failed to enable maintenance mode." >&2
        echo "  URL          : $url" >&2
        echo "  Method       : PUT" >&2
        echo "  HTTP code    : $http_code" >&2
        echo "  Request body : (empty)" >&2
        if [[ -n "$response_body" ]]; then
            echo "  Response body:" >&2
            if echo "$response_body" | jq . >/dev/null 2>&1; then
                echo "$response_body" | jq . >&2
            else
                echo "$response_body" >&2
            fi
        else
            echo "  Response body: (empty)" >&2
        fi
        return 1
    fi
}

# -----------------------------------------------------------------------------
# maintenance-off — take the instance out of maintenance mode
#
# PUT /entity/Lock/1/ApplyUpdate/stopLockoutCommand
# Endpoint name: Lock  |  Version: V1
# Request body: (none)
# Response: HTTP 204 No Content on success
# -----------------------------------------------------------------------------
cmd_maintenance_off() {
    _login || return 1

    local url="${ACUMATICA_URL}/entity/Lock/1/ApplyUpdate/stopLockoutCommand"
    echo "Disabling maintenance mode..."
    echo "  Request : PUT $url"

    local response_body http_code
    response_body=$(curl -s -w "\n%{http_code}" \
        -b "$_COOKIE_FILE" \
        -X PUT \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -d "" \
        "$url")

    http_code=$(echo "$response_body" | tail -n1)
    response_body=$(echo "$response_body" | sed '$d')

    echo "  Response: HTTP $http_code"

    if [[ "$http_code" == "204" || "$http_code" == "200" ]]; then
        echo "Maintenance mode disabled."
    else
        echo "Error: Failed to disable maintenance mode." >&2
        echo "  URL          : $url" >&2
        echo "  Method       : PUT" >&2
        echo "  HTTP code    : $http_code" >&2
        echo "  Request body : (empty)" >&2
        if [[ -n "$response_body" ]]; then
            echo "  Response body:" >&2
            if echo "$response_body" | jq . >/dev/null 2>&1; then
                echo "$response_body" | jq . >&2
            else
                echo "$response_body" >&2
            fi
        else
            echo "  Response body: (empty)" >&2
        fi
        return 1
    fi
}

# =============================================================================
# USAGE
# =============================================================================

usage() {
    cat <<EOF
Acumatica Customization Management Helper

Usage: $0 <command> [options]

Commands:
  list                               List published projects and their items
  export  <project-name> [dir]       Export project to a ZIP file (default dir: .)
  import  <file.zip> [name] [desc]   Import a ZIP as a customization project
  validate <name> [name2 ...]        Validate project(s) without publishing
  publish  <name> [name2 ...]        Publish project(s)
  unpublish [Current|All]            Unpublish all projects (default: Current)
  delete  <project-name>             Delete an unpublished project
  status                             Check current publish/validation status
  maintenance-on                     Enable maintenance mode (Lock endpoint V1)
  maintenance-off                    Disable maintenance mode (Lock endpoint V1)

Configuration (acumatica.conf):
  ACUMATICA_URL       Base URL of the instance (e.g. http://host/sandbox)
  ACUMATICA_USERNAME  Login username — must have the Customizer role
  ACUMATICA_PASSWORD  Login password

Optional tuning:
  PUBLISH_POLL_INTERVAL  Seconds between publishEnd polls (default: 30)
  PUBLISH_MAX_ATTEMPTS   Max poll attempts before timeout  (default: 10)

Examples:
  $0 list
  $0 export  MyProject ./backups
  $0 import  MyProject.zip MyProject "Initial import"
  $0 validate MyProject
  $0 publish  MyProject AnotherProject
  $0 unpublish Current
  $0 delete  MyProject
  $0 status
  $0 maintenance-on
  $0 maintenance-off
EOF
}

# =============================================================================
# ENTRY POINT
# =============================================================================

# Single logout guard — fires on ALL exit paths:
# normal completion, set -e abort, unhandled error, or signal (Ctrl-C).
# Each cmd_* function calls _login; _logout is always guaranteed to run.
trap '_logout' EXIT

case "${1:-}" in
    list)                       cmd_list ;;
    export)   shift;            cmd_export   "$@" ;;
    import)   shift;            cmd_import   "$@" ;;
    validate) shift;            cmd_validate "$@" ;;
    publish)  shift;            cmd_publish  "$@" ;;
    unpublish) shift;           cmd_unpublish "$@" ;;
    delete)   shift;            cmd_delete   "$@" ;;
    status)                     cmd_status ;;
    maintenance-on)             cmd_maintenance_on ;;
    maintenance-off)            cmd_maintenance_off ;;
    -h|--help|help|"")          usage; exit 0 ;;
    *)
        echo "Error: unknown command '${1}'" >&2
        echo "" >&2
        usage >&2
        exit 1
        ;;
esac