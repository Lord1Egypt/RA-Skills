#!/usr/bin/env bash
set -euo pipefail

# file-issue.sh — create an issue on the forge with labels
#
# Usage: file-issue.sh --title TITLE --body BODY [--labels LABEL1,LABEL2] [--help]
#
# Required env: FORGE_TOKEN, FORGE_API

usage() {
    sed -n '3,8s/^# //p' "$0"
    exit 0
}

title=""
body=""
labels=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --title)  title="$2";  shift 2 ;;
        --body)   body="$2";   shift 2 ;;
        --labels) labels="$2"; shift 2 ;;
        --help|-h) usage ;;
        *) printf 'file-issue: unknown option: %s\n' "$1" >&2; exit 1 ;;
    esac
done

: "${FORGE_TOKEN:?FORGE_TOKEN is required}"
: "${FORGE_API:?FORGE_API is required}"

if [[ -z "$title" ]]; then
    echo "Error: --title is required" >&2
    exit 1
fi
if [[ -z "$body" ]]; then
    echo "Error: --body is required" >&2
    exit 1
fi

# --- Resolve label names to IDs ---
label_ids="[]"
if [[ -n "$labels" ]]; then
    all_labels=$(curl -sf -H "Authorization: token ${FORGE_TOKEN}" \
        -H "Accept: application/json" \
        "${FORGE_API}/labels?limit=50" 2>/dev/null) || {
        echo "Warning: could not fetch labels, creating issue without labels" >&2
        all_labels="[]"
    }
    label_ids="["
    first=true
    IFS=',' read -ra label_arr <<< "$labels"
    for lname in "${label_arr[@]}"; do
        lname=$(echo "$lname" | xargs)  # trim whitespace
        lid=$(echo "$all_labels" | jq -r --arg n "$lname" '.[] | select(.name == $n) | .id')
        if [[ -n "$lid" ]]; then
            if ! $first; then label_ids+=","; fi
            label_ids+="$lid"
            first=false
        else
            echo "Warning: label '${lname}' not found, skipping" >&2
        fi
    done
    label_ids+="]"
fi

# --- Secret scan (refuse to post bodies containing obvious secrets) ---
if echo "$body" | grep -qiE '(sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{36}|AKIA[A-Z0-9]{16}|-----BEGIN (RSA |EC )?PRIVATE KEY)'; then
    echo "Error: body appears to contain a secret — refusing to post" >&2
    exit 1
fi

# --- Create the issue ---
payload=$(jq -n \
    --arg t "$title" \
    --arg b "$body" \
    --argjson l "$label_ids" \
    '{title: $t, body: $b, labels: $l}')

response=$(curl -sf -X POST \
    -H "Authorization: token ${FORGE_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "$payload" \
    "${FORGE_API}/issues") || {
    echo "Error: failed to create issue" >&2
    exit 1
}

number=$(echo "$response" | jq -r '.number')
url=$(echo "$response" | jq -r '.html_url')
echo "Created issue #${number}: ${url}"
