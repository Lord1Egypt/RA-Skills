---
name: "dev-backup"
description: "Snapshot con restore distruttivo, trigger stretti e fallback tar sicuro (v1.2.2)"
---

# dev-backup

Snapshot the current state of a named project for safe rollback.

## Explicit Command Usage

⚠️ **REGOLA CRITICA:** Chiama la skill SOLO quando l'utente emette un comando esplicito di backup o restore. Non attivare mai per frasi generiche come "com'è il progetto?", "stai lavorando a...", o quando "backup" appare casualmente nella conversazione.

**Trigger validi (solo questi):**
- `"Fai un backup manuale di [nome-progetto]"` → crea snapshot
- `"Esegui backup di [nome-progetto]"` → crea snapshot
- `"Backup di [nome-progetto]"` → crea snapshot
- `"Ripristina il backup N di [nome-progetto]"` → restore da snapshot specifico (con conferma interattiva)
- `"Mostra i backup di [nome-progetto]"` → lista snapshots

**NON triggerare con:**
- Frasi casuali dove "backup" appare come parola nella conversazione
- `"Salva lo stato attuale"` (troppo ambiguo — non è un comando esplicito)
- `"Fai un backup dello sviluppo"` (non specifica il progetto)
- `"Ripristina il backup di [nome-progetto]"` senza numero snapshot (troppo vago, richiede "backup N")
- Qualsiasi frase che non contenga un comando chiaro di backup/restore + nome progetto
- **Il restore richiede SEMPRE conferma esplicita dell'utente PRIMA di eseguire**

## Comandi

```bash
# Backup any project
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
bash "$SCRIPT_DIR/dev-backup.sh" <project-name> --project-dir /path/to/your/project

# Example: backup a "my-app" project
bash "$SCRIPT_DIR/dev-backup.sh" my-app --project-dir /home/user/projects/my-app

# No --project-dir? Uses the current working directory
cd /home/user/projects/my-app
bash "$SCRIPT_DIR/dev-backup.sh" my-app
```

## Naming

Snapshots are named per project:

- **my-app-snapshot-1**, **my-app-snapshot-2**, …
- **another-project-snapshot-1**, **another-project-snapshot-2**, …

Each project tracks its own counter independently.

## Excluded from snapshot

- `.git`, `node_modules`, `.vite`, `.cache`, `*.log`, `.env`, `backups/`

## Restore (🔴 DISTRUTTIVO — LEGGERE PRIMA)

> **⛔ PERICOLO: QUESTA OPERAZIONE È DISTRUTTIVA.**
>
> Il restore **sovrascrive TUTTI i file esistenti** nel progetto target con lo stato dello snapshot.
> - Qualsiasi modifica non salvata nel progetto verrà **PERDUTA DEFINITIVAMENTE**.
> - File nuovi creati dopo l'ultimo backup verranno eliminati.
> - File modificati localmente verranno sovrascritti senza preavviso.
>
> **SEMPRE eseguire `--dry-run` PRIMA del restore reale.**

```bash
# 🔴 STEP 1: Dry-run OBBLIGATORIO (mostra cosa verrebbe sovrascritto)
bash "$SCRIPT_DIR/dev-backup.sh" my-app --restore --dry-run --project-dir /path/to/your/project

# 🔴 STEP 2: Solo se dry-run è accettabile, esegui il restore
bash "$SCRIPT_DIR/dev-backup.sh" my-app --restore --project-dir /path/to/your/project

# Restore latest snapshot
bash "$SCRIPT_DIR/dev-backup.sh" my-app --restore --project-dir /path/to/your/project

# Restore specific snapshot
bash "$SCRIPT_DIR/dev-backup.sh" my-app --restore --snapshot 2 --project-dir /path/to/your/project
```

**Verifica del checksum:** Durante il restore, lo script verifica che lo **snapshot non sia corrotto** calcolando un checksum SHA256 di tutti i file nello snapshot e confrontandolo con quello salvato durante il backup. Questo NON controlla la compatibilità con lo stato attuale del progetto — solo l'integrità dello snapshot stesso.

## List

To list all snapshots for a project:

```bash
bash "$SCRIPT_DIR/dev-backup.sh" my-app --list
```

## Retention

By default, only the last 5 snapshots per project are kept. **Vecchi snapshot vengono eliminati definitivamente senza conferma.** Per cambiare:

```bash
# Backup con retention personalizzata (tieni ultimi 10)
bash "$SCRIPT_DIR/dev-backup.sh" my-app --keep 10 --project-dir /path/to/your/project

# Oppure disabilita la retention automatica con un numero enorme
bash "$SCRIPT_DIR/dev-backup.sh" my-app --keep 9999 --project-dir /path/to/your/project
```

## Verification

After backup, confirm:

```bash
ls -la <backups-dir>/
```

You should see the project-prefixed snapshot and `.latest` symlink.

---

scripts/dev-backup.sh ---
#!/usr/bin/env bash
set -euo pipefail

# dev-backup: snapshot a named project for safe rollback
# Usage: dev-backup <project-name> [options]
#
# Creates a numbered snapshot of a project, prefixed with the project name
# so you can distinguish backups across different apps.
#
# Examples:
#   dev-backup my-app                     # uses current dir as project dir
#   dev-backup my-app --project-dir /path # explicit project dir
#   dev-backup my-app --list              # list all snapshots
#   dev-backup my-app --restore           # restore latest snapshot
#   dev-backup my-app --restore --snapshot 2  # restore specific snapshot
#   dev-backup my-app --dry-run           # dry run restore (show what would change)
#
# Snapshots are named: <project>-snapshot-1, <project>-snapshot-2, …
# A .latest symlink always points to the newest snapshot.
# Default retention: 5 snapshots per project (use --keep to change).

# Project name is mandatory
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <project-name> [--project-dir PATH] [--output-dir PATH] [--list|--restore] [--snapshot N] [--keep N] [--dry-run]"
  echo "Example: $0 my-app --project-dir /home/user/projects/my-app"
  exit 1
fi

PROJECT_NAME="$1"
shift

# Sanitize project name: replace spaces and special chars with hyphens
PROJECT_NAME="$(echo "$PROJECT_NAME" | sed 's/[^a-zA-Z0-9_-]/-/g')"

PROJECT_DIR="${PROJECT_DIR:-.}"
OUTPUT_DIR="${OUTPUT_DIR:-$(dirname "$PROJECT_DIR")/backups}"
PREFIX="${PROJECT_NAME}-snapshot"
KEEP=5
ACTION="backup"
SNAPSHOT_NUM=""
DRY_RUN=false

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --project-dir) PROJECT_DIR="$2"; shift 2 ;;
    --output-dir)  OUTPUT_DIR="$2";     shift 2 ;;
    --list) ACTION="list"; shift ;;
    --restore) ACTION="restore"; shift ;;
    --snapshot) SNAPSHOT_NUM="$2"; shift 2 ;;
    --keep) KEEP="$2"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    --help|-h)
      echo "Usage: $0 <project-name> [--project-dir PATH] [--output-dir PATH] [--list|--restore] [--snapshot N] [--keep N] [--dry-run]"
      echo "Options:"
      echo "  --project-dir PATH   Path to the project (default: current dir)"
      echo "  --output-dir PATH    Where to store backups (default: ../backups/)"
      echo "  --list               List all snapshots for this project"
      echo "  --restore            Restore latest snapshot"
      echo "  --snapshot N         Restore specific snapshot number"
      echo "  --keep N             Number of snapshots to retain (default: 5)"
      echo "  --dry-run            Preview restore without making changes"
      echo ""
      echo "Examples:"
      echo "  $0 my-app --project-dir /path/to/app"
      echo "  $0 my-app --list"
      echo "  $0 my-app --restore"
      echo "  $0 my-app --restore --snapshot 2"
      echo "  $0 my-app --restore --dry-run"
      exit 0
      ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# Resolve to absolute paths
PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"
OUTPUT_DIR="$(mkdir -p "$OUTPUT_DIR" && cd "$OUTPUT_DIR" && pwd)"

# --- LIST MODE ---
if [[ "$ACTION" == "list" ]]; then
  echo "==> Snapshots for '${PROJECT_NAME}':"
  echo ""
  COUNT=0
  for dir in "$OUTPUT_DIR"/${PREFIX}-* 2>/dev/null; do
    if [[ -d "$dir" ]]; then
      COUNT=$((COUNT + 1))
      NAME=$(basename "$dir")
      SIZE=$(du -sh "$dir" 2>/dev/null | cut -f1 || echo "?")
      DATE=$(stat -c %y "$dir" 2>/dev/null | cut -d. -f1 || echo "?")
      # Check if it's the latest
      LATEST=""
      if [[ -L "$OUTPUT_DIR/.latest" ]]; then
        LATEST_TARGET=$(readlink "$OUTPUT_DIR/.latest")
        if [[ "$LATEST_TARGET" == "$NAME" ]]; then
          LATEST=" (latest)"
        fi
      fi
      # Checksum if exists
      CHECKSUM=""
      if [[ -f "$dir/.checksum" ]]; then
        CHECKSUM=$(cut -d' ' -f1 "$dir/.checksum")
        CHECKSUM=" (sha256: ${CHECKSUM:0:12}...)"
      fi
      printf "  %-30s %6s  %s%s%s\n" "$NAME" "$SIZE" "$DATE" "$LATEST" "$CHECKSUM"
    fi
  done
  if [[ $COUNT -eq 0 ]]; then
    echo "  (no snapshots found)"
  fi
  echo ""
  exit 0
fi

# --- RESTORE MODE ---
if [[ "$ACTION" == "restore" ]]; then
  # Determine which snapshot to restore
  if [[ -n "$SNAPSHOT_NUM" ]]; then
    TARGET="$OUTPUT_DIR/${PREFIX}-${SNAPSHOT_NUM}"
  else
    # Use .latest symlink
    LATEST="$OUTPUT_DIR/.latest"
    if [[ ! -L "$LATEST" ]]; then
      echo "Error: No .latest symlink found in $OUTPUT_DIR"
      exit 1
    fi
    TARGET="$OUTPUT_DIR/$(readlink "$LATEST")"
  fi

  if [[ ! -d "$TARGET" ]]; then
    echo "Error: Snapshot not found: $TARGET"
      exit 1
  fi

  echo "==> Restoring snapshot: $(basename "$TARGET")"
  echo "    Source:  $TARGET"
  echo "    Target:  $PROJECT_DIR"

  # Verify checksum integrity
  if [[ -f "$TARGET/.checksum" ]]; then
    STORED_CHECKSUM=$(cut -d' ' -f1 "$TARGET/.checksum")
    CURRENT_CHECKSUM=$(find "$TARGET" -type f ! -name '.checksum' -exec sha256sum {} \; 2>/dev/null | sort | sha256sum | cut -d' ' -f1)
    if [[ "$STORED_CHECKSUM" == "$CURRENT_CHECKSUM" ]]; then
      echo "    Checksum: ✅ VERIFICATO (${STORED_CHECKSUM:0:16}...) — integrità OK"
    else
      echo "    Checksum: ⚠️ NON CORRESPONDE! (${STORED_CHECKSUM:0:16}... vs ${CURRENT_CHECKSUM:0:16}...)"
      echo "    ATTENZIONE: Lo snapshot potrebbe essere stato modificato o corrotto!"
    fi
  else
    echo "    Checksum: ℹ️ Nessun checksum disponibile per questo snapshot"
  fi

  # DRY-RUN mode: show what would change without executing
  if [[ "$DRY_RUN" == true ]]; then
    echo ""
    echo "==> DRY-RUN: ecco cosa verrebbe sovrascritto:"
    if command -v rsync &>/dev/null; then
      rsync -avn --exclude '.checksum' "${TARGET}/" "${PROJECT_DIR}/" 2>&1 | head -50
    else
      diff -rq --exclude='.checksum' "${TARGET}/" "${PROJECT_DIR}/" 2>&1 | head -50
    fi
    echo ""
    echo "==> Nessuna modifica è stata eseguita. Rimuovi --dry-run per confermare."
    exit 0
  fi

  # WARNING: destructive operation
  echo ""
  echo "⚠️ ATTENZIONE: Il restore sovrascriverà i file esistenti!"
  echo "   Cambiamenti non salvati andranno persi."
  echo ""

  # Copy snapshot back to project dir
  if command -v rsync &>/dev/null; then
    rsync -a \
      --exclude '.checksum' \
      "${TARGET}/" "${PROJECT_DIR}/"
  else
    cp -a "${TARGET}/." "${PROJECT_DIR}/"
  fi

  echo "==> Restore complete!"
  echo "    Restored: $(basename "$TARGET")"
  exit 0
fi

# --- BACKUP MODE ---
# Find next number for THIS project
NEXT=1
if ls "$OUTPUT_DIR/${PREFIX}-"* 1>/dev/null 2>&1; then
  HIGHEST=$(ls "$OUTPUT_DIR" | grep "^${PROJECT_NAME}-snapshot-" | sed "s/^${PROJECT_NAME}-snapshot-//;s/-.*//" | sort -rn | head -1)
  if [[ "$HIGHEST" =~ ^[0-9]+$ ]]; then
    NEXT=$((HIGHEST + 1))
  fi
fi

SNAPSHOT_NAME="${PREFIX}-${NEXT}"
SNAPSHOT_DIR="${OUTPUT_DIR}/${SNAPSHOT_NAME}"

echo "==> Creating dev-backup: ${SNAPSHOT_NAME}"
echo "    Project: ${PROJECT_NAME}"
echo "    Source:  ${PROJECT_DIR}"
echo "    Target:  ${SNAPSHOT_DIR}"

# Copy with rsync (NO --delete to avoid accidental data loss)
if command -v rsync &>/dev/null; then
  rsync -a \
    --exclude '.git' --exclude 'node_modules' --exclude '.vite' \
    --exclude '.cache' --exclude '*.log' --exclude '.env' \
    --exclude 'backups' \
    "${PROJECT_DIR}/" "${SNAPSHOT_DIR}/"
else
  mkdir -p "$SNAPSHOT_DIR"
  tar -C "$(dirname "$PROJECT_DIR")" -cf - "$(basename "$PROJECT_DIR")" | tar -C "$SNAPSHOT_DIR" -xf -
fi

# Generate checksum for integrity verification
find "$SNAPSHOT_DIR" -type f ! -name '.checksum' -exec sha256sum {} \; 2>/dev/null | sort | sha256sum > "$SNAPSHOT_DIR/.checksum"

# Size report
TOTAL_SIZE=$(du -sh "$SNAPSHOT_DIR" 2>/dev/null | cut -f1 || echo "?")
echo "==> Snapshot created: ${SNAPSHOT_DIR} (${TOTAL_SIZE})"
echo "    SHA256: $(cut -d' ' -f1 "$SNAPSHOT_DIR/.checksum" | head -c 16)..."

# Update .latest symlink
LATEST="${OUTPUT_DIR}/.latest"
rm -f "$LATEST"
ln -s "$SNAPSHOT_NAME" "$LATEST"

echo "Done. Latest backup: ${LATEST}"

# --- RETENTION ---
# Remove old snapshots beyond --keep limit
SNAPSHOT_COUNT=$(ls -1d "$OUTPUT_DIR/${PREFIX}-"* 2>/dev/null | wc -l)
if [[ $SNAPSHOT_COUNT -gt $KEEP ]]; then
  REMOVE_COUNT=$((SNAPSHOT_COUNT - KEEP))
  echo ""
  echo "⚠️ RETENTION: elimino definitivamente $REMOVE_COUNT snapshot vecchi (non recuperabili)."
  ls -1d "$OUTPUT_DIR/${PREFIX}-"* | sort -t'-' -k$(echo "$PREFIX" | tr -cd '-' | wc -c) -n | head -$REMOVE_COUNT | while read dir; do
    echo "    Removing: $(basename "$dir")"
    rm -rf "$dir"
  done
  echo "==> Retention complete."
fi

echo ""
echo "To restore: $0 $PROJECT_NAME --restore"
