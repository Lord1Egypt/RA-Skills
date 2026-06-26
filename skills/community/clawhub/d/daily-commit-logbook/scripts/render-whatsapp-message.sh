#!/bin/bash
# Generate the daily report, submit the MIS logbook, and print a WhatsApp-ready confirmation.

set -euo pipefail

export PATH="/usr/bin:/bin:/usr/local/bin:/home/linuxbrew/.linuxbrew/bin:${PATH:-}"
export HOME="${HOME:-/root}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAILY_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# shellcheck source=./common.sh
source "$SCRIPT_DIR/common.sh"

WORKSPACE="$(resolve_workspace "$DAILY_DIR")"
MIS_DIR="${MIS_SKILL_DIR:-$(resolve_peer_skill_dir "$WORKSPACE" "$DAILY_DIR" "mis-logbook-submit")}"
export OPENCLAW_WORKSPACE="$WORKSPACE"

REPORT_FILE="$WORKSPACE/reports/commit-report-$(TZ=Asia/Jakarta date +%Y-%m-%d).md"
MIS_ACTIVITY_FILE=$(mktemp)
MIS_RESULT_FILE=$(mktemp)
cleanup() {
    rm -f "$MIS_ACTIVITY_FILE" "$MIS_RESULT_FILE"
}
trap cleanup EXIT

bash "$SCRIPT_DIR/generate-report.sh" >/dev/null

if [ ! -f "$REPORT_FILE" ]; then
    echo "Laporan harian gagal dibuat hari ini. Tolong cek generator logbook." >&2
    exit 1
fi

awk '
    /^### Versi 2/ { in_v2 = 1; next }
    in_v2 && /^\*\*Aktivitas:\*\*/ { capture = 1; next }
    capture && /^\*\*Hasil:\*\*/ { exit }
    capture { print }
' "$REPORT_FILE" \
| sed 's/^\*\*//; s/\*\*$//' \
| sed 's/^-[[:space:]]*//' \
| sed '/^[[:space:]]*$/d' \
| paste -sd ' ' - \
| sed -E 's/[[:space:]]+/ /g; s/[[:space:]]+\././g; s/[[:space:]]+,/,/g; s/^[[:space:]]+//; s/[[:space:]]+$//' \
> "$MIS_ACTIVITY_FILE"

if [ ! -s "$MIS_ACTIVITY_FILE" ]; then
    echo "Aktivitas logbook MIS gagal diekstrak dari laporan harian." >&2
    exit 1
fi

node "$MIS_DIR/scripts/submit-logbook.js" < "$MIS_ACTIVITY_FILE" > "$MIS_RESULT_FILE"

STATUS=$(jq -r '.status' "$MIS_RESULT_FILE")
MIS_ACTIVITY=$(cat "$MIS_ACTIVITY_FILE")
TODAY_LABEL=$(TZ=Asia/Jakarta date +"%d %B %Y")
TODAY_ROW=$(jq -r '.todayShort // empty' "$MIS_RESULT_FILE")
ROW_TEXT=$(jq -r '.row // empty' "$MIS_RESULT_FILE")
SAVE_MESSAGE=$(jq -r '.saveMessage // empty' "$MIS_RESULT_FILE")
DELETE_NOISE=$(jq -r '.deleteNoise // false' "$MIS_RESULT_FILE")

case "$STATUS" in
    success)
        cat <<EOF
✅ Logbook MIS hari ini berhasil disubmit.

Tanggal: $TODAY_LABEL
Jam: 07:30-16:00
Status: ${SAVE_MESSAGE:-Tersimpan}

Aktivitas yang dikirim:
$MIS_ACTIVITY
EOF
        if [ -n "$TODAY_ROW" ] && [ "$TODAY_ROW" != "null" ]; then
            printf '\nBaris logbook: %s\n' "$TODAY_ROW"
        fi
        if [ "$DELETE_NOISE" = "true" ]; then
            printf '\nCatatan: halaman MIS juga menampilkan pesan "Hapus Data Gagal", tapi entri baru terverifikasi muncul di tabel.\n'
        fi
        ;;
    duplicate)
        cat <<EOF
ℹ️ Logbook MIS untuk hari ini sudah ada, jadi saya tidak submit ulang.

Tanggal: $TODAY_LABEL
Aktivitas yang seharusnya dikirim:
$MIS_ACTIVITY
EOF
        if [ -n "$ROW_TEXT" ] && [ "$ROW_TEXT" != "null" ]; then
            printf '\nBaris yang sudah ada: %s\n' "$ROW_TEXT"
        fi
        ;;
    *)
        echo "Proses submit logbook MIS gagal. Tolong cek automasi logbook harian." >&2
        exit 1
        ;;
esac
