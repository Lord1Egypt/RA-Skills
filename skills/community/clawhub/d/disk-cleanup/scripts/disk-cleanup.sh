#!/bin/bash
# openclaw-disk-cleanup.sh — Generic OpenClaw disk cleanup
# Works for any OpenClaw deployment. Cleans up common space consumers:
#   1. Memory SQLite orphaned tmp files (failed reindex residue)
#   2. Memory SQLite VACUUM (reclaim fragmentation)
#   3. Docker unused images, volumes, containers, build cache
#   4. OpenClaw log rotation & old logs
#   5. /tmp OpenClaw-related temp files older than 24h
#   6. Workspace backup artifacts (*.prebind.*, *.bak, *.orig)
#   7. Delivery queue old entries
#   8. Systemd journal vacuum (journald log bloat)
#   9. Package manager caches (npm, yarn, pnpm, bun)
#  10. System log rotation cleanup (rotated syslogs, btmp)
#  11. Git workspace gc (large .git from frequent auto-commits)
#  12. Stale migration artifacts (QMD models after backend switch, etc.)
#
# Usage:
#   openclaw-disk-cleanup.sh [--dry-run] [--aggressive] [--quiet]
#
# Options:
#   --dry-run      Show what would be cleaned without deleting
#   --aggressive   Also VACUUM large SQLite DBs + git gc aggressive
#   --quiet        Only output summary line (for cron)
#
# Exit codes:
#   0 = success (with or without cleanup)
#   1 = error during cleanup

set -euo pipefail

# ─── Args ───
DRY_RUN=false
AGGRESSIVE=false
QUIET=false
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --aggressive) AGGRESSIVE=true ;;
    --quiet) QUIET=true ;;
    *) echo "Unknown arg: $arg"; exit 1 ;;
  esac
done

# ─── Detect OpenClaw home ───
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
if [[ ! -d "$OPENCLAW_HOME" ]]; then
  echo "ERROR: OpenClaw home not found at $OPENCLAW_HOME"
  exit 1
fi

WORKSPACE="${OPENCLAW_WORKSPACE:-$(pwd)}"
TOTAL_FREED=0
ACTIONS=()

log() {
  if [[ "$QUIET" == "false" ]]; then
    echo "$1"
  fi
}

bytes_to_human() {
  local bytes=$1
  if [[ $bytes -ge 1073741824 ]]; then
    echo "$(awk "BEGIN{printf \"%.1f\", $bytes/1073741824}")GB"
  elif [[ $bytes -ge 1048576 ]]; then
    echo "$(awk "BEGIN{printf \"%.0f\", $bytes/1048576}")MB"
  elif [[ $bytes -ge 1024 ]]; then
    echo "$(awk "BEGIN{printf \"%.0f\", $bytes/1024}")KB"
  else
    echo "${bytes}B"
  fi
}

safe_rm() {
  local target="$1"
  local size
  size=$(du -sb "$target" 2>/dev/null | cut -f1 || echo 0)
  if [[ "$DRY_RUN" == "true" ]]; then
    log "  [DRY-RUN] Would delete: $target ($(bytes_to_human "$size"))"
  else
    rm -rf "$target"
    log "  Deleted: $target ($(bytes_to_human "$size"))"
  fi
  TOTAL_FREED=$((TOTAL_FREED + size))
}

log "🧹 OpenClaw Disk Cleanup"
log "   Home: $OPENCLAW_HOME"
log "   Mode: $(if $DRY_RUN; then echo 'DRY-RUN'; else echo 'LIVE'; fi)$(if $AGGRESSIVE; then echo ' + AGGRESSIVE'; fi)"
log ""

# ═══════════════════════════════════════════════════════════════
# SECTION A: OpenClaw-specific cleanup
# ═══════════════════════════════════════════════════════════════

# ─── 1. Memory SQLite orphaned tmp files ───
log "━━━ 1. Memory SQLite temp files ━━━"
MEMORY_DIR="$OPENCLAW_HOME/memory"
TMP_COUNT=0
if [[ -d "$MEMORY_DIR" ]]; then
  while IFS= read -r -d '' tmpfile; do
    TMP_COUNT=$((TMP_COUNT + 1))
    safe_rm "$tmpfile"
  done < <(find "$MEMORY_DIR" -name "*.sqlite.tmp-*" -print0 2>/dev/null)
fi
if [[ $TMP_COUNT -eq 0 ]]; then
  log "  No orphaned tmp files found"
else
  ACTIONS+=("Cleaned $TMP_COUNT memory SQLite tmp files")
fi
log ""

# ─── 2. Memory SQLite VACUUM (aggressive mode) ───
log "━━━ 2. Memory SQLite optimization ━━━"
if [[ "$AGGRESSIVE" == "true" && -d "$MEMORY_DIR" ]]; then
  while IFS= read -r -d '' dbfile; do
    DBSIZE_BEFORE=$(stat -c%s "$dbfile" 2>/dev/null || echo 0)
    if [[ $DBSIZE_BEFORE -lt 52428800 ]]; then
      log "  Skip $(basename "$dbfile") ($(bytes_to_human "$DBSIZE_BEFORE"), <50MB)"
      continue
    fi
    FREELIST=$(sqlite3 "$dbfile" "PRAGMA freelist_count;" 2>/dev/null || echo 0)
    PAGECOUNT=$(sqlite3 "$dbfile" "PRAGMA page_count;" 2>/dev/null || echo 1)
    FRAG_PCT=$((FREELIST * 100 / PAGECOUNT))
    if [[ $FRAG_PCT -lt 5 && "$DRY_RUN" == "false" ]]; then
      log "  Skip VACUUM $(basename "$dbfile") (fragmentation ${FRAG_PCT}% < 5%)"
      continue
    fi
    if [[ "$DRY_RUN" == "true" ]]; then
      log "  [DRY-RUN] Would VACUUM $(basename "$dbfile") ($(bytes_to_human "$DBSIZE_BEFORE"), ${FRAG_PCT}% fragmented)"
    else
      log "  VACUUM $(basename "$dbfile") ($(bytes_to_human "$DBSIZE_BEFORE"))..."
      sqlite3 "$dbfile" "VACUUM;" 2>/dev/null && {
        DBSIZE_AFTER=$(stat -c%s "$dbfile" 2>/dev/null || echo "$DBSIZE_BEFORE")
        SAVED=$((DBSIZE_BEFORE - DBSIZE_AFTER))
        if [[ $SAVED -gt 0 ]]; then
          TOTAL_FREED=$((TOTAL_FREED + SAVED))
          ACTIONS+=("VACUUM $(basename "$dbfile"): saved $(bytes_to_human "$SAVED")")
          log "  → Saved $(bytes_to_human "$SAVED")"
        else
          log "  → No space recovered (already compact)"
        fi
      } || log "  ⚠️ VACUUM failed for $(basename "$dbfile")"
    fi
  done < <(find "$MEMORY_DIR" -name "*.sqlite" -print0 2>/dev/null)

  # Also VACUUM lcm.db if present and large
  LCM_DB="$OPENCLAW_HOME/lcm.db"
  if [[ -f "$LCM_DB" ]]; then
    LCMSIZE=$(stat -c%s "$LCM_DB" 2>/dev/null || echo 0)
    if [[ $LCMSIZE -ge 52428800 ]]; then
      LCM_FREE=$(sqlite3 "$LCM_DB" "PRAGMA freelist_count;" 2>/dev/null || echo 0)
      LCM_PAGES=$(sqlite3 "$LCM_DB" "PRAGMA page_count;" 2>/dev/null || echo 1)
      LCM_FRAG=$((LCM_FREE * 100 / LCM_PAGES))
      if [[ $LCM_FRAG -ge 5 ]]; then
        if [[ "$DRY_RUN" == "true" ]]; then
          log "  [DRY-RUN] Would VACUUM lcm.db ($(bytes_to_human "$LCMSIZE"), ${LCM_FRAG}% fragmented)"
        else
          log "  VACUUM lcm.db ($(bytes_to_human "$LCMSIZE"))..."
          sqlite3 "$LCM_DB" "VACUUM;" 2>/dev/null && {
            LCMSIZE_AFTER=$(stat -c%s "$LCM_DB" 2>/dev/null || echo "$LCMSIZE")
            LCM_SAVED=$((LCMSIZE - LCMSIZE_AFTER))
            if [[ $LCM_SAVED -gt 0 ]]; then
              TOTAL_FREED=$((TOTAL_FREED + LCM_SAVED))
              ACTIONS+=("VACUUM lcm.db: saved $(bytes_to_human "$LCM_SAVED")")
            fi
          } || log "  ⚠️ VACUUM lcm.db failed"
        fi
      fi
    fi
  fi
else
  log "  Skipped (use --aggressive to enable VACUUM)"
fi
log ""

# ─── 3. Docker cleanup ───
log "━━━ 3. Docker cleanup ━━━"
if command -v docker &>/dev/null; then
  DANGLING=$(docker images -f "dangling=true" -q 2>/dev/null | wc -l)
  if [[ $DANGLING -gt 0 ]]; then
    if [[ "$DRY_RUN" == "true" ]]; then
      log "  [DRY-RUN] Would remove $DANGLING dangling images"
    else
      PRUNE_OUT=$(docker image prune -f 2>/dev/null || true)
      RECLAIMED=$(echo "$PRUNE_OUT" | grep -oP 'reclaimed \K[^)]+' || echo "unknown")
      log "  Removed $DANGLING dangling images (reclaimed: $RECLAIMED)"
      ACTIONS+=("Docker: pruned $DANGLING dangling images")
    fi
  else
    log "  No dangling images"
  fi

  UNUSED_VOLS=$(docker volume ls -f "dangling=true" -q 2>/dev/null | wc -l)
  if [[ $UNUSED_VOLS -gt 0 ]]; then
    if [[ "$DRY_RUN" == "true" ]]; then
      log "  [DRY-RUN] Would remove $UNUSED_VOLS unused volumes"
    else
      docker volume prune -f 2>/dev/null >/dev/null
      log "  Removed $UNUSED_VOLS unused volumes"
      ACTIONS+=("Docker: pruned $UNUSED_VOLS unused volumes")
    fi
  else
    log "  No unused volumes"
  fi

  OLD_CONTAINERS=$(docker ps -a --filter "status=exited" --format "{{.ID}}" 2>/dev/null | wc -l)
  if [[ $OLD_CONTAINERS -gt 0 ]]; then
    if [[ "$DRY_RUN" == "true" ]]; then
      log "  [DRY-RUN] Would remove $OLD_CONTAINERS stopped containers"
    else
      docker container prune -f --filter "until=48h" 2>/dev/null >/dev/null
      log "  Pruned stopped containers older than 48h"
      ACTIONS+=("Docker: pruned stopped containers")
    fi
  else
    log "  No stopped containers to clean"
  fi

  if [[ "$DRY_RUN" == "false" ]]; then
    docker builder prune -f --filter "until=72h" 2>/dev/null >/dev/null && \
      log "  Pruned build cache older than 72h" || true
  fi
else
  log "  Docker not available, skipping"
fi
log ""

# ─── 4. OpenClaw logs cleanup ───
log "━━━ 4. OpenClaw log cleanup ━━━"
LOG_COUNT=0

# Gateway logs in /tmp/openclaw/
if [[ -d "/tmp/openclaw" ]]; then
  while IFS= read -r -d '' logfile; do
    LOG_COUNT=$((LOG_COUNT + 1))
    safe_rm "$logfile"
  done < <(find /tmp/openclaw -name "*.log" -mtime +3 -print0 2>/dev/null)
fi

# Workspace logs
WORKSPACE_LOG_DIR="${WORKSPACE}/logs"
if [[ -d "$WORKSPACE_LOG_DIR" ]]; then
  while IFS= read -r -d '' logfile; do
    LOG_COUNT=$((LOG_COUNT + 1))
    safe_rm "$logfile"
  done < <(find "$WORKSPACE_LOG_DIR" -name "*.log" -mtime +14 -print0 2>/dev/null)
fi

# Agent workspace logs
while IFS= read -r -d '' logdir; do
  while IFS= read -r -d '' logfile; do
    LOG_COUNT=$((LOG_COUNT + 1))
    safe_rm "$logfile"
  done < <(find "$logdir" -name "*.log" -mtime +7 -print0 2>/dev/null)
done < <(find "$OPENCLAW_HOME" -path "*/workspace-*/logs" -type d -print0 2>/dev/null)

if [[ $LOG_COUNT -eq 0 ]]; then
  log "  No old logs to clean"
else
  ACTIONS+=("Cleaned $LOG_COUNT old log files")
fi
log ""

# ─── 5. /tmp OpenClaw temp files ───
log "━━━ 5. Temp files cleanup ━━━"
TMP_CLEANED=0
for pattern in "clawd_*" "openclaw_*" "patrol_*" "board_*" "cron-list*.json" "board-effect.log"; do
  while IFS= read -r -d '' tmpfile; do
    TMP_CLEANED=$((TMP_CLEANED + 1))
    safe_rm "$tmpfile"
  done < <(find /tmp -maxdepth 1 -name "$pattern" -mtime +1 -print0 2>/dev/null)
done

for cache_dir in "/tmp/tsx-"* "/tmp/node-compile-cache" "/tmp/jiti"; do
  if [[ -d "$cache_dir" ]]; then
    CACHE_AGE=$(find "$cache_dir" -maxdepth 0 -mtime +7 -print 2>/dev/null | wc -l)
    if [[ $CACHE_AGE -gt 0 ]]; then
      TMP_CLEANED=$((TMP_CLEANED + 1))
      safe_rm "$cache_dir"
    fi
  fi
done

if [[ $TMP_CLEANED -eq 0 ]]; then
  log "  No stale temp files"
else
  ACTIONS+=("Cleaned $TMP_CLEANED temp files/dirs")
fi
log ""

# ─── 6. Workspace backup artifacts ───
log "━━━ 6. Workspace backup artifacts ━━━"
BACKUP_COUNT=0

while IFS= read -r -d '' prebind; do
  if [[ $(find "$prebind" -maxdepth 0 -mtime +7 -print 2>/dev/null | wc -l) -gt 0 ]]; then
    BACKUP_COUNT=$((BACKUP_COUNT + 1))
    safe_rm "$prebind"
  fi
done < <(find "$WORKSPACE" -maxdepth 1 -name "*.prebind.*" -print0 2>/dev/null)

while IFS= read -r -d '' origfile; do
  if [[ $(find "$origfile" -maxdepth 0 -mtime +7 -print 2>/dev/null | wc -l) -gt 0 ]]; then
    BACKUP_COUNT=$((BACKUP_COUNT + 1))
    safe_rm "$origfile"
  fi
done < <(find "$WORKSPACE/scripts" -name "*.orig" -print0 2>/dev/null)

if [[ $BACKUP_COUNT -eq 0 ]]; then
  log "  No stale backups found"
else
  ACTIONS+=("Cleaned $BACKUP_COUNT backup artifacts")
fi
log ""

# ─── 7. Delivery queue old entries ───
log "━━━ 7. Delivery queue cleanup ━━━"
DQ_DIR="$OPENCLAW_HOME/delivery-queue"
DQ_COUNT=0
if [[ -d "$DQ_DIR" ]]; then
  while IFS= read -r -d '' dqfile; do
    DQ_COUNT=$((DQ_COUNT + 1))
    safe_rm "$dqfile"
  done < <(find "$DQ_DIR" -type f -mtime +7 -print0 2>/dev/null)
fi
if [[ $DQ_COUNT -eq 0 ]]; then
  log "  No old delivery queue entries"
else
  ACTIONS+=("Cleaned $DQ_COUNT old delivery queue entries")
fi
log ""

# ═══════════════════════════════════════════════════════════════
# SECTION B: System-level cleanup (common on VPS running OpenClaw)
# ═══════════════════════════════════════════════════════════════

# ─── 8. Systemd journal vacuum ───
# journald logs grow unbounded on most VPS defaults.
# Any Linux VPS running OpenClaw will accumulate GB of journal logs.
log "━━━ 8. Systemd journal vacuum ━━━"
if command -v journalctl &>/dev/null; then
  JOURNAL_BYTES=$(journalctl --disk-usage 2>/dev/null | grep -oP '[\d.]+[GMKT]' | head -1 || echo "")
  # Parse to MB for threshold check
  JOURNAL_MB=0
  if [[ "$JOURNAL_BYTES" =~ ([0-9.]+)G ]]; then
    JOURNAL_MB=$(awk "BEGIN{printf \"%d\", ${BASH_REMATCH[1]}*1024}")
  elif [[ "$JOURNAL_BYTES" =~ ([0-9.]+)M ]]; then
    JOURNAL_MB=${BASH_REMATCH[1]%.*}
  fi

  if [[ $JOURNAL_MB -gt 500 ]]; then
    if [[ "$DRY_RUN" == "true" ]]; then
      log "  [DRY-RUN] Would vacuum journal from ${JOURNAL_BYTES} to 500M"
    else
      VACUUM_OUT=$(journalctl --vacuum-size=500M 2>&1 || true)
      FREED=$(echo "$VACUUM_OUT" | grep -oP 'freed \K[\d.]+[GMKT]+' || echo "")
      if [[ -n "$FREED" ]]; then
        log "  Vacuumed journal: freed $FREED (was ${JOURNAL_BYTES})"
        ACTIONS+=("Journal vacuum: freed $FREED")
      else
        log "  Vacuumed journal to 500M (was ${JOURNAL_BYTES})"
        ACTIONS+=("Journal vacuum: ${JOURNAL_BYTES} → 500M")
      fi
    fi
  else
    log "  Journal size OK (${JOURNAL_BYTES:-unknown})"
  fi

  # Also set persistent limit to prevent regrowth
  JOURNAL_CONF="/etc/systemd/journald.conf.d/openclaw-limit.conf"
  if [[ ! -f "$JOURNAL_CONF" && "$DRY_RUN" == "false" ]]; then
    mkdir -p /etc/systemd/journald.conf.d
    cat > "$JOURNAL_CONF" <<'JEOF'
# Installed by openclaw-disk-cleanup.sh
# Prevents journal from growing beyond 500M
[Journal]
SystemMaxUse=500M
SystemKeepFree=1G
MaxFileSec=1week
JEOF
    systemctl restart systemd-journald 2>/dev/null || true
    log "  Installed journal size limit (500M max)"
    ACTIONS+=("Installed journald 500M limit")
  fi
else
  log "  journalctl not available, skipping"
fi
log ""

# ─── 9. Package manager caches ───
# npm, yarn, pnpm, bun all accumulate multi-GB caches from
# OpenClaw plugin installs, skill installs, and sandbox builds.
log "━━━ 9. Package manager caches ━━━"
PKG_CLEANED=0
PKG_FREED=0

# npm cache (_cacache grows unbounded)
NPM_CACHE="$HOME/.npm/_cacache"
if [[ -d "$NPM_CACHE" ]]; then
  NPM_SIZE=$(du -sb "$NPM_CACHE" 2>/dev/null | cut -f1 || echo 0)
  if [[ $NPM_SIZE -gt 104857600 ]]; then  # >100MB
    if [[ "$DRY_RUN" == "true" ]]; then
      log "  [DRY-RUN] Would clean npm cache ($(bytes_to_human "$NPM_SIZE"))"
    else
      npm cache clean --force 2>/dev/null || rm -rf "$NPM_CACHE"
      PKG_FREED=$((PKG_FREED + NPM_SIZE))
      PKG_CLEANED=$((PKG_CLEANED + 1))
      log "  Cleaned npm cache ($(bytes_to_human "$NPM_SIZE"))"
    fi
  fi
fi

# npm _npx cache (old npx executions)
NPX_CACHE="$HOME/.npm/_npx"
if [[ -d "$NPX_CACHE" ]]; then
  NPX_SIZE=$(du -sb "$NPX_CACHE" 2>/dev/null | cut -f1 || echo 0)
  if [[ $NPX_SIZE -gt 52428800 ]]; then  # >50MB
    PKG_CLEANED=$((PKG_CLEANED + 1))
    PKG_FREED=$((PKG_FREED + NPX_SIZE))
    if [[ "$DRY_RUN" == "false" ]]; then
      rm -rf "$NPX_CACHE"
      log "  Cleaned npx cache ($(bytes_to_human "$NPX_SIZE"))"
    else
      log "  [DRY-RUN] Would clean npx cache ($(bytes_to_human "$NPX_SIZE"))"
    fi
  fi
fi

# yarn berry cache
YARN_CACHE="$HOME/.yarn/berry"
if [[ -d "$YARN_CACHE" ]]; then
  YARN_SIZE=$(du -sb "$YARN_CACHE" 2>/dev/null | cut -f1 || echo 0)
  if [[ $YARN_SIZE -gt 104857600 ]]; then
    PKG_CLEANED=$((PKG_CLEANED + 1))
    PKG_FREED=$((PKG_FREED + YARN_SIZE))
    if [[ "$DRY_RUN" == "false" ]]; then
      rm -rf "$YARN_CACHE"
      log "  Cleaned yarn cache ($(bytes_to_human "$YARN_SIZE"))"
    else
      log "  [DRY-RUN] Would clean yarn cache ($(bytes_to_human "$YARN_SIZE"))"
    fi
  fi
fi

# pnpm cache
PNPM_CACHE="$HOME/.cache/pnpm"
if [[ -d "$PNPM_CACHE" ]]; then
  PNPM_SIZE=$(du -sb "$PNPM_CACHE" 2>/dev/null | cut -f1 || echo 0)
  if [[ $PNPM_SIZE -gt 52428800 ]]; then
    PKG_CLEANED=$((PKG_CLEANED + 1))
    PKG_FREED=$((PKG_FREED + PNPM_SIZE))
    if [[ "$DRY_RUN" == "false" ]]; then
      rm -rf "$PNPM_CACHE"
      log "  Cleaned pnpm cache ($(bytes_to_human "$PNPM_SIZE"))"
    else
      log "  [DRY-RUN] Would clean pnpm cache ($(bytes_to_human "$PNPM_SIZE"))"
    fi
  fi
fi

# bun install cache
for BUN_DIR in "$HOME/.bun/install/cache" "$WORKSPACE/.bun"; do
  if [[ -d "$BUN_DIR" ]]; then
    BUN_SIZE=$(du -sb "$BUN_DIR" 2>/dev/null | cut -f1 || echo 0)
    if [[ $BUN_SIZE -gt 52428800 ]]; then
      PKG_CLEANED=$((PKG_CLEANED + 1))
      PKG_FREED=$((PKG_FREED + BUN_SIZE))
      if [[ "$DRY_RUN" == "false" ]]; then
        rm -rf "$BUN_DIR"
        log "  Cleaned bun cache: $BUN_DIR ($(bytes_to_human "$BUN_SIZE"))"
      else
        log "  [DRY-RUN] Would clean bun cache: $BUN_DIR ($(bytes_to_human "$BUN_SIZE"))"
      fi
    fi
  fi
done

# Workspace-local .npm and .cache (created by sandbox or agent installs)
for WS_CACHE in "$WORKSPACE/.npm" "$WORKSPACE/.cache"; do
  if [[ -d "$WS_CACHE" ]]; then
    WC_SIZE=$(du -sb "$WS_CACHE" 2>/dev/null | cut -f1 || echo 0)
    if [[ $WC_SIZE -gt 52428800 ]]; then
      PKG_CLEANED=$((PKG_CLEANED + 1))
      PKG_FREED=$((PKG_FREED + WC_SIZE))
      if [[ "$DRY_RUN" == "false" ]]; then
        rm -rf "$WS_CACHE"
        log "  Cleaned workspace cache: $WS_CACHE ($(bytes_to_human "$WC_SIZE"))"
      else
        log "  [DRY-RUN] Would clean workspace cache: $WS_CACHE ($(bytes_to_human "$WC_SIZE"))"
      fi
    fi
  fi
done

# Prisma engine cache (downloaded per version, stacks up)
PRISMA_CACHE="$HOME/.cache/prisma"
if [[ -d "$PRISMA_CACHE" ]]; then
  PRISMA_SIZE=$(du -sb "$PRISMA_CACHE" 2>/dev/null | cut -f1 || echo 0)
  if [[ $PRISMA_SIZE -gt 52428800 ]]; then
    PKG_CLEANED=$((PKG_CLEANED + 1))
    PKG_FREED=$((PKG_FREED + PRISMA_SIZE))
    if [[ "$DRY_RUN" == "false" ]]; then
      rm -rf "$PRISMA_CACHE"
      log "  Cleaned prisma engine cache ($(bytes_to_human "$PRISMA_SIZE"))"
    else
      log "  [DRY-RUN] Would clean prisma cache ($(bytes_to_human "$PRISMA_SIZE"))"
    fi
  fi
fi

# node-gyp cache (native addon build artifacts)
NODEGYP_CACHE="$HOME/.cache/node-gyp"
if [[ -d "$NODEGYP_CACHE" ]]; then
  GYSIZE=$(du -sb "$NODEGYP_CACHE" 2>/dev/null | cut -f1 || echo 0)
  if [[ $GYSIZE -gt 52428800 ]]; then
    PKG_CLEANED=$((PKG_CLEANED + 1))
    PKG_FREED=$((PKG_FREED + GYSIZE))
    if [[ "$DRY_RUN" == "false" ]]; then
      rm -rf "$NODEGYP_CACHE"
      log "  Cleaned node-gyp cache ($(bytes_to_human "$GYSIZE"))"
    else
      log "  [DRY-RUN] Would clean node-gyp cache ($(bytes_to_human "$GYSIZE"))"
    fi
  fi
fi

TOTAL_FREED=$((TOTAL_FREED + PKG_FREED))
if [[ $PKG_CLEANED -eq 0 ]]; then
  log "  Package caches OK (all < threshold)"
else
  ACTIONS+=("Cleaned $PKG_CLEANED package caches ($(bytes_to_human "$PKG_FREED"))")
fi
log ""

# ─── 10. System log rotation cleanup ───
# Rotated syslogs and btmp (SSH brute-force log) grow on public VPS.
log "━━━ 10. System log rotation ━━━"
SYSLOG_FREED=0

# Rotated syslogs older than current + 1
for rotlog in /var/log/syslog.[2-9]* /var/log/auth.log.[2-9]*; do
  if [[ -f "$rotlog" ]]; then
    RSIZE=$(stat -c%s "$rotlog" 2>/dev/null || echo 0)
    SYSLOG_FREED=$((SYSLOG_FREED + RSIZE))
    if [[ "$DRY_RUN" == "false" ]]; then
      rm -f "$rotlog"
    fi
  fi
done

# btmp: SSH brute-force attempts log. Can grow huge on public VPS.
# Truncate instead of delete (system expects it to exist).
BTMP="/var/log/btmp"
if [[ -f "$BTMP" ]]; then
  BTMP_SIZE=$(stat -c%s "$BTMP" 2>/dev/null || echo 0)
  if [[ $BTMP_SIZE -gt 10485760 ]]; then  # >10MB
    SYSLOG_FREED=$((SYSLOG_FREED + BTMP_SIZE))
    if [[ "$DRY_RUN" == "false" ]]; then
      : > "$BTMP"
      log "  Truncated btmp ($(bytes_to_human "$BTMP_SIZE"))"
    else
      log "  [DRY-RUN] Would truncate btmp ($(bytes_to_human "$BTMP_SIZE"))"
    fi
  fi
fi

TOTAL_FREED=$((TOTAL_FREED + SYSLOG_FREED))
if [[ $SYSLOG_FREED -gt 0 ]]; then
  log "  Cleaned rotated system logs ($(bytes_to_human "$SYSLOG_FREED"))"
  ACTIONS+=("System logs: cleaned $(bytes_to_human "$SYSLOG_FREED")")
else
  log "  System logs OK"
fi
log ""

# ─── 11. Git workspace gc ───
# Workspaces with frequent auto-commits (board-move, auto-commit-shared)
# accumulate large .git dirs. gc --auto is lightweight; --aggressive on flag.
log "━━━ 11. Git workspace gc ━━━"
GIT_FREED=0
for gitdir in "$WORKSPACE/.git"; do
  if [[ -d "$gitdir" ]]; then
    GIT_BEFORE=$(du -sb "$gitdir" 2>/dev/null | cut -f1 || echo 0)
    if [[ $GIT_BEFORE -lt 209715200 ]]; then  # <200MB
      log "  Skip .git gc ($(bytes_to_human "$GIT_BEFORE"), <200MB)"
    elif [[ "$DRY_RUN" == "true" ]]; then
      log "  [DRY-RUN] Would gc .git ($(bytes_to_human "$GIT_BEFORE"))"
    else
      REPO_DIR=$(dirname "$gitdir")
      if [[ "$AGGRESSIVE" == "true" ]]; then
        (cd "$REPO_DIR" && git gc --aggressive --prune=now 2>/dev/null) || true
      else
        (cd "$REPO_DIR" && git gc --auto --prune=now 2>/dev/null) || true
      fi
      GIT_AFTER=$(du -sb "$gitdir" 2>/dev/null | cut -f1 || echo 0)
      GIT_SAVED=$((GIT_BEFORE - GIT_AFTER))
      if [[ $GIT_SAVED -gt 0 ]]; then
        GIT_FREED=$((GIT_FREED + GIT_SAVED))
        log "  Git gc: saved $(bytes_to_human "$GIT_SAVED")"
      else
        log "  Git gc: no space recovered"
      fi
    fi
  fi
done
TOTAL_FREED=$((TOTAL_FREED + GIT_FREED))
if [[ $GIT_FREED -gt 0 ]]; then
  ACTIONS+=("Git gc: saved $(bytes_to_human "$GIT_FREED")")
fi
log ""

# ─── 12. Stale migration artifacts ───
# When switching backends (QMD→builtin, etc.), old model files remain.
# Also catches orphaned Python venvs from abandoned scripts.
log "━━━ 12. Stale migration artifacts ━━━"
MIGRATION_COUNT=0

# QMD models (only if memory backend is NOT qmd)
QMD_MODELS="$HOME/.cache/qmd/models"
if [[ -d "$QMD_MODELS" ]]; then
  # Check if QMD is still configured
  QMD_ACTIVE=false
  if grep -q '"qmd"' "$OPENCLAW_HOME/openclaw.json" 2>/dev/null; then
    QMD_ACTIVE=true
  fi
  if [[ "$QMD_ACTIVE" == "false" ]]; then
    MIGRATION_COUNT=$((MIGRATION_COUNT + 1))
    safe_rm "$HOME/.cache/qmd"
  else
    log "  QMD still active, keeping models"
  fi
fi

# Orphaned Python venvs in scripts/ (older than 30 days, not recently used)
while IFS= read -r -d '' venv; do
  VENV_AGE=$(find "$venv" -maxdepth 0 -mtime +30 -print 2>/dev/null | wc -l)
  if [[ $VENV_AGE -gt 0 ]]; then
    VENV_SIZE=$(du -sb "$venv" 2>/dev/null | cut -f1 || echo 0)
    if [[ $VENV_SIZE -gt 52428800 ]]; then  # >50MB
      MIGRATION_COUNT=$((MIGRATION_COUNT + 1))
      safe_rm "$venv"
    fi
  fi
done < <(find "$WORKSPACE/scripts" -maxdepth 2 -name "venv" -type d -print0 2>/dev/null)

if [[ $MIGRATION_COUNT -eq 0 ]]; then
  log "  No stale migration artifacts"
else
  ACTIONS+=("Cleaned $MIGRATION_COUNT migration artifacts")
fi
log ""

# ═══════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════

log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
DISK_NOW=$(df / --output=pcent 2>/dev/null | tail -1 | tr -d ' %')
if [[ ${#ACTIONS[@]} -eq 0 ]]; then
  log "✅ Nothing to clean — disk at ${DISK_NOW}%"
  echo "CLEAN|0|0B|${DISK_NOW}%"
else
  log "📊 Actions taken: ${#ACTIONS[@]}"
  for a in "${ACTIONS[@]}"; do
    log "  • $a"
  done
  log "💾 Estimated space freed: $(bytes_to_human "$TOTAL_FREED")"
  log "📀 Disk now: ${DISK_NOW}%"
  echo "CLEANED|${#ACTIONS[@]}|$(bytes_to_human "$TOTAL_FREED")|${DISK_NOW}%"
fi
