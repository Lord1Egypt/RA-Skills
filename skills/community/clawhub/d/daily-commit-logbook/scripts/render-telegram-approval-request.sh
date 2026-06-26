#!/bin/bash
# Generate the daily report, store a pending MIS submission draft, and print a
# Telegram-ready approval request without submitting anything yet.

set -euo pipefail

export PATH="/usr/bin:/bin:/usr/local/bin:/home/linuxbrew/.linuxbrew/bin:${PATH:-}"
export HOME="${HOME:-/root}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DAILY_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
# shellcheck source=./common.sh
source "$SCRIPT_DIR/common.sh"

WORKSPACE="$(resolve_workspace "$DAILY_DIR")"
export OPENCLAW_WORKSPACE="$WORKSPACE"

PENDING_DATE=$(TZ=Asia/Jakarta date +%Y-%m-%d)
REPORT_DATE="$PENDING_DATE"
TODAY_LABEL=$(TZ=Asia/Jakarta date +"%d %B %Y")
REPORT_FILE="$WORKSPACE/reports/commit-report-$REPORT_DATE.md"
PENDING_DIR="$WORKSPACE/reports/pending"
PENDING_FILE="$PENDING_DIR/mis-logbook-$PENDING_DATE.json"

mkdir -p "$PENDING_DIR"

if [ -f "$PENDING_FILE" ]; then
    EXISTING_STATUS=$(jq -r '.status // empty' "$PENDING_FILE")
    if [ "$EXISTING_STATUS" = "submitted" ] || [ "$EXISTING_STATUS" = "duplicate" ]; then
        EXISTING_ACTIVITY=$(jq -r '.activity // empty' "$PENDING_FILE")
        echo "ℹ️ Draft logbook MIS untuk $TODAY_LABEL sudah pernah diproses sebelumnya (status: $EXISTING_STATUS)."
        if [ -n "$EXISTING_ACTIVITY" ] && [ "$EXISTING_ACTIVITY" != "null" ]; then
            printf '\nAktivitas tersimpan:\n%s\n' "$EXISTING_ACTIVITY"
        fi
        exit 0
    fi
fi

bash "$SCRIPT_DIR/generate-report.sh" >/dev/null

if [ ! -f "$REPORT_FILE" ]; then
    echo "Draft logbook harian gagal dibuat hari ini. Tolong cek generator logbook." >&2
    exit 1
fi

MIS_ACTIVITY=$(bash "$SCRIPT_DIR/extract-mis-activity.sh" "$REPORT_FILE")

if [ -z "$MIS_ACTIVITY" ]; then
    echo "Aktivitas logbook MIS gagal diekstrak dari laporan harian." >&2
    exit 1
fi

NOW=$(date --iso-8601=seconds)
CREATED_AT="$NOW"
if [ -f "$PENDING_FILE" ]; then
    CREATED_AT=$(jq -r '.createdAt // empty' "$PENDING_FILE")
    if [ -z "$CREATED_AT" ] || [ "$CREATED_AT" = "null" ]; then
        CREATED_AT="$NOW"
    fi
fi

TMP_FILE=$(mktemp)
jq -n \
  --arg date "$PENDING_DATE" \
  --arg status "pending" \
  --arg createdAt "$CREATED_AT" \
  --arg updatedAt "$NOW" \
  --arg source "telegram-approval" \
  --arg reportFile "$REPORT_FILE" \
  --arg activity "$MIS_ACTIVITY" \
  '{
      date: $date,
      status: $status,
      createdAt: $createdAt,
      updatedAt: $updatedAt,
      source: $source,
      reportFile: $reportFile,
      activity: $activity
   }' > "$TMP_FILE"
mv "$TMP_FILE" "$PENDING_FILE"

cat <<EOF
📝 Draft logbook MIS hari ini sudah siap.

Tanggal: $TODAY_LABEL
Aktivitas yang akan dikirim:
$MIS_ACTIVITY

Kalau sudah oke, balas: submit
Kalau mau saya revisi dulu, bilang saja apa yang perlu diubah.

Saya akan menunggu konfirmasi sebelum submit ke MIS.
EOF
