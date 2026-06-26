#!/bin/bash
# Submit the latest pending MIS draft after explicit user confirmation.

set -euo pipefail

export PATH="/usr/bin:/bin:/usr/local/bin:/home/linuxbrew/.linuxbrew/bin:${PATH:-}"
export HOME="${HOME:-/root}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAILY_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# shellcheck source=./common.sh
source "$SCRIPT_DIR/common.sh"

WORKSPACE="$(resolve_workspace "$DAILY_DIR")"
MIS_DIR="${MIS_SKILL_DIR:-$(resolve_peer_skill_dir "$WORKSPACE" "$DAILY_DIR" "mis-logbook-submit")}"
PENDING_DIR="$WORKSPACE/reports/pending"
export OPENCLAW_WORKSPACE="$WORKSPACE"

TARGET_DATE=""

usage() {
    echo "Usage: $0 [--date YYYY-MM-DD]" >&2
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --date)
            TARGET_DATE="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage
            exit 1
            ;;
    esac
done

resolve_pending_file() {
    if [ -n "$TARGET_DATE" ]; then
        local requested="$PENDING_DIR/mis-logbook-$TARGET_DATE.json"
        if [ -f "$requested" ]; then
            printf '%s\n' "$requested"
            return 0
        fi
        return 1
    fi

    shopt -s nullglob
    local files=("$PENDING_DIR"/mis-logbook-*.json)
    local idx
    for (( idx=${#files[@]}-1; idx>=0; idx-- )); do
        local file="${files[$idx]}"
        local status
        status=$(jq -r '.status // empty' "$file")
        if [ "$status" = "pending" ] || [ "$status" = "submit-failed" ]; then
            printf '%s\n' "$file"
            return 0
        fi
    done
    return 1
}

if ! PENDING_FILE=$(resolve_pending_file); then
    echo "Tidak ada draft logbook MIS yang menunggu konfirmasi." >&2
    exit 1
fi

CURRENT_STATUS=$(jq -r '.status // empty' "$PENDING_FILE")
PENDING_DATE=$(jq -r '.date // empty' "$PENDING_FILE")
TODAY_LABEL=$(TZ=Asia/Jakarta date -d "$PENDING_DATE" +"%d %B %Y" 2>/dev/null || printf '%s' "$PENDING_DATE")

case "$CURRENT_STATUS" in
    submitted)
        echo "ℹ️ Draft logbook MIS untuk $TODAY_LABEL sudah pernah disubmit sebelumnya."
        exit 0
        ;;
    duplicate)
        echo "ℹ️ Draft logbook MIS untuk $TODAY_LABEL sudah terdeteksi ada di MIS, jadi tidak perlu submit ulang."
        exit 0
        ;;
    pending|submit-failed)
        ;;
    *)
        echo "Status draft logbook tidak dikenali: $CURRENT_STATUS" >&2
        exit 1
        ;;
esac

MIS_ACTIVITY=$(jq -r '.activity // empty' "$PENDING_FILE")
if [ -z "$MIS_ACTIVITY" ] || [ "$MIS_ACTIVITY" = "null" ]; then
    echo "Draft logbook tidak punya aktivitas yang bisa dikirim ke MIS." >&2
    exit 1
fi

MIS_RESULT_FILE=$(mktemp)
MIS_ERROR_FILE=$(mktemp)
cleanup() {
    rm -f "$MIS_RESULT_FILE" "$MIS_ERROR_FILE"
}
trap cleanup EXIT

update_pending_state() {
    local next_status="$1"
    local now="$2"
    local tmp_file
    tmp_file=$(mktemp)
    if [ -s "$MIS_RESULT_FILE" ]; then
        jq --slurpfile result "$MIS_RESULT_FILE" \
           --arg status "$next_status" \
           --arg updatedAt "$now" \
           '.status = $status
            | .updatedAt = $updatedAt
            | .misResult = $result[0]
            | del(.lastError)' \
           "$PENDING_FILE" > "$tmp_file"
    else
        jq --arg status "$next_status" \
           --arg updatedAt "$now" \
           --arg lastError "$(tr '\n' ' ' < "$MIS_ERROR_FILE" | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//')" \
           '.status = $status
            | .updatedAt = $updatedAt
            | .lastError = $lastError' \
           "$PENDING_FILE" > "$tmp_file"
    fi
    mv "$tmp_file" "$PENDING_FILE"
}

if ! printf '%s' "$MIS_ACTIVITY" | node "$MIS_DIR/scripts/submit-logbook.js" > "$MIS_RESULT_FILE" 2> "$MIS_ERROR_FILE"; then
    NOW=$(date --iso-8601=seconds)
    update_pending_state "submit-failed" "$NOW"
    ERROR_MESSAGE=$(tr '\n' ' ' < "$MIS_ERROR_FILE" | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//')
    echo "Submit logbook MIS gagal: ${ERROR_MESSAGE:-silakan cek automasi logbook harian}." >&2
    exit 1
fi

RESULT_STATUS=$(jq -r '.status // empty' "$MIS_RESULT_FILE")
NOW=$(date --iso-8601=seconds)

case "$RESULT_STATUS" in
    success)
        update_pending_state "submitted" "$NOW"
        ROW_TEXT=$(jq -r '.row // empty' "$MIS_RESULT_FILE")
        SAVE_MESSAGE=$(jq -r '.saveMessage // empty' "$MIS_RESULT_FILE")
        DELETE_NOISE=$(jq -r '.deleteNoise // false' "$MIS_RESULT_FILE")
        cat <<EOF
✅ Logbook MIS berhasil disubmit.

Tanggal: $TODAY_LABEL
Jam: 07:30-16:00
Status: ${SAVE_MESSAGE:-Tersimpan}

Aktivitas yang dikirim:
$MIS_ACTIVITY
EOF
        if [ -n "$ROW_TEXT" ] && [ "$ROW_TEXT" != "null" ]; then
            printf '\nBaris logbook: %s\n' "$ROW_TEXT"
        fi
        if [ "$DELETE_NOISE" = "true" ]; then
            printf '\nCatatan: halaman MIS juga menampilkan pesan "Hapus Data Gagal", tapi entri baru terverifikasi muncul di tabel.\n'
        fi
        ;;
    duplicate)
        update_pending_state "duplicate" "$NOW"
        ROW_TEXT=$(jq -r '.row // empty' "$MIS_RESULT_FILE")
        cat <<EOF
ℹ️ Logbook MIS untuk $TODAY_LABEL sudah ada, jadi saya tidak submit ulang.

Aktivitas yang seharusnya dikirim:
$MIS_ACTIVITY
EOF
        if [ -n "$ROW_TEXT" ] && [ "$ROW_TEXT" != "null" ]; then
            printf '\nBaris yang sudah ada: %s\n' "$ROW_TEXT"
        fi
        ;;
    *)
        printf 'Status submitter MIS tidak dikenali: %s\n' "$RESULT_STATUS" > "$MIS_ERROR_FILE"
        : > "$MIS_RESULT_FILE"
        update_pending_state "submit-failed" "$NOW"
        echo "Submit logbook MIS gagal karena respons submitter tidak dikenali." >&2
        exit 1
        ;;
esac
