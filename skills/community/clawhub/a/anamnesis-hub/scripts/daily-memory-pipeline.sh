#!/bin/bash
# daily-memory-pipeline.sh — 统一日终记忆管道
#
# 替代三个独立 cron 任务，统一编排整个记忆管线。
# 流程：sync-pull → auto-memory → sync-push+reindex → session-extract → decay
#
# 用法:
#   bash daily-memory-pipeline.sh full          # 全量运行（生产模式）
#   bash daily-memory-pipeline.sh sync-only     # 仅同步
#   bash daily-memory-pipeline.sh extract-only  # 仅提取
#   bash daily-memory-pipeline.sh status        # 查看状态

set -euo pipefail

WORKSPACE="${HOME}/.openclaw/workspace"
SCRIPTS_DIR="${WORKSPACE}/user_workspace/scripts"
MEMS_CACHE="${WORKSPACE}/user_workspace/memos-cloud-cache"
LOG_FILE="${WORKSPACE}/memory/.pipeline-run-$(date +%Y-%m-%d).log"

log() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$LOG_FILE"; }
fail() { log "❌ $*"; exit 1; }

# ─── 阶段参数 ─────────────────────────────────────────────────────────────
STAGE=${1:-full}

log "📋 daily-memory-pipeline start — stage: ${STAGE}"

# ─── 阶段 1: Cloud → 本地拉取 ──────────────────────────────────────────
pull_cloud() {
    log "↓ 阶段1: sync-pull (Cloud → local)"
    if [ -f "${SCRIPTS_DIR}/sync-cloud-pull.py" ]; then
        python3 "${SCRIPTS_DIR}/sync-cloud-pull.py" >> "$LOG_FILE" 2>&1 || log "⚠️ sync-pull 非致命错误"
    else
        log "⚠️ sync-cloud-pull.py 不存在，跳过"
    fi
}

# ─── 阶段 2: 记忆提取（两阶段管道）──────────────────────────────────────
run_auto_memory() {
    log "🧠 阶段2: auto-memory v3 (ARCHIVE.md archive → MEMORY.md summary)"
    if [ -f "${SCRIPTS_DIR}/auto_memory_extract.py" ]; then
        result=$(python3 "${SCRIPTS_DIR}/auto_memory_extract.py" --mode full 2>&1 || true)
        echo "$result" >> "$LOG_FILE"
        
        # 解析结果
        added=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('summary',{}).get('added_after_dedup',0))" 2>/dev/null || echo "0")
        skipped=$(echo "$result" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('summary',{}).get('duplicates_skipped',0))" 2>/dev/null || echo "0")
        log "  归档: ${added} 新增 / ${skipped} 重复跳过"
    else
        log "⚠️ auto_memory_extract.py 不存在，跳过"
    fi
}

# ─── 阶段 3: 本地 → Cloud 推送 + Vector 重建 ───────────────────────────
push_cloud() {
    log "↑ 阶段3: sync-push + reindex"
    if [ -f "${SCRIPTS_DIR}/sync-cloud-push.py" ]; then
        python3 "${SCRIPTS_DIR}/sync-cloud-push.py" >> "$LOG_FILE" 2>&1 || log "⚠️ sync-push 非致命错误"
    fi
    
    log "   memory index rebuild..."
    openclaw memory index --force >> "$LOG_FILE" 2>&1 || log "⚠️ index rebuild 非致命错误"
}

# ─── 阶段 4: 会话提取 (两遍: Error → Learning → Memory) ──────────────────
run_session_extract() {
    log "📊 阶段4: session-extract (JSONL scan → .learnings/ + memory/)"
    if [ -f "${SCRIPTS_DIR}/session-extract.py" ]; then
        result=$(python3 "${SCRIPTS_DIR}/session-extract.py" --full 2>&1 || true)
        echo "$result" >> "$LOG_FILE"
        errors=$(echo "$result" | grep -c "ERROR\|Error" 2>/dev/null || echo "0")
        lessons=$(echo "$result" | grep -c "LESSON\|Lesson" 2>/dev/null || echo "0")
        log "  提取: ${errors} errors / ${lessons} lessons"
    else
        log "⚠️ session-extract.py 不存在，跳过"
    fi
}

# ─── 阶段 5: facts.db 衰减 ───────────────────────────────────────────────
run_decay() {
    log "⏳ 阶段5: activation decay (facts.db)"
    python3 -c "
import sqlite3
from pathlib import Path
db = Path.home() / '.openclaw' / 'memory' / 'facts.sqlite'
if not db.exists():
    print('facts.db not found, skip decay')
else:
    conn = sqlite3.connect(str(db))
    cursor = conn.execute('UPDATE facts SET activation = activation * 0.95 WHERE permanent = 0 AND activation > 0.01')
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    print(f'Decay applied: {affected} facts updated')
" >> "$LOG_FILE" 2>&1
}

# ─── 阶段 6: 健康检查 ────────────────────────────────────────────────────
run_healthcheck() {
    log "🏥 阶段6: healthcheck"
    
    # MEMORY.md 行数检查
    mem_lines=$(wc -l < "${WORKSPACE}/MEMORY.md")
    if [ "$mem_lines" -gt 100 ]; then
        log "⚠️ MEMORY.md: ${mem_lines} 行 (阈值: 100)"
    else
        log "   MEMORY.md: ${mem_lines} 行 ✅"
    fi
    
    # ARCHIVE.md 行数检查
    arc_lines=$(wc -l < "${WORKSPACE}/ARCHIVE.md")
    if [ "$arc_lines" -gt 250 ]; then
        log "⚠️ ARCHIVE.md: ${arc_lines} 行 (阈值: 250)"
    else
        log "   ARCHIVE.md: ${arc_lines} 行 ✅"
    fi
    
    # facts.db 统计
    python3 -c "
import sqlite3
from pathlib import Path
db = Path.home() / '.openclaw' / 'memory' / 'facts.sqlite'
if db.exists():
    conn = sqlite3.connect(str(db))
    facts = conn.execute('SELECT COUNT(*) FROM facts').fetchone()[0]
    hot = conn.execute(\"SELECT COUNT(*) FROM facts WHERE activation > 2.0\").fetchone()[0]
    cool = conn.execute(\"SELECT COUNT(*) FROM facts WHERE activation < 0.02\").fetchone()[0]
    conn.close()
    print(f'   facts.db: {facts} total / {hot} HOT / {cool} COOL')
else:
    print('   facts.db: not initialized')
" >> "$LOG_FILE" 2>&1
}

# ─── 主控 ─────────────────────────────────────────────────────────────────
case $STAGE in
    full)
        pull_cloud
        run_auto_memory
        push_cloud
        run_session_extract
        run_decay
        run_healthcheck
        ;;
    sync-only)
        pull_cloud
        push_cloud
        ;;
    extract-only)
        run_auto_memory
        run_session_extract
        ;;
    status)
        echo "=== 管道状态 ==="
        echo "日志: ${LOG_FILE}"
        echo "MEMORY.md: $(wc -l < "${WORKSPACE}/MEMORY.md") 行"
        echo "ARCHIVE.md: $(wc -l < "${WORKSPACE}/ARCHIVE.md") 行"
        python3 -c "
from pathlib import Path
db = Path.home() / '.openclaw' / 'memory' / 'facts.sqlite'
if db.exists():
    import sqlite3
    conn = sqlite3.connect(str(db))
    n = conn.execute('SELECT COUNT(*) FROM facts').fetchone()[0]
    e = conn.execute('SELECT COUNT(DISTINCT entity) FROM facts').fetchone()[0]
    conn.close()
    print(f'facts.db: {n} facts / {e} entities')
else:
    print('facts.db: not initialized')
"
        ;;
    *)
        echo "用法: $0 {full|sync-only|extract-only|status}"
        exit 1
        ;;
esac

log "✅ pipeline complete — stage: ${STAGE}"
