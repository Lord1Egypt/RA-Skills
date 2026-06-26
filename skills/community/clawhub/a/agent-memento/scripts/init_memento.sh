#!/usr/bin/env bash
# script to initialize a new Tick-Driven Project
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <ProjectName>"
    exit 1
fi

PROJECT_NAME=$1
PROJECT_DIR="$(pwd)/projects/$PROJECT_NAME"

echo "🚀 Initializing Agent Memento Framework (v0.2) for: $PROJECT_NAME"

# Create project scaffolding
mkdir -p "$PROJECT_DIR"/{docs,src,logs,scripts}

# Generate MASTER_PLAN.md template
cat << 'PLAN' > "$PROJECT_DIR/docs/MASTER_PLAN.md"
# Project Master Plan: $PROJECT_NAME

> Write exactly ONE grand objective here. Ensure tickets are extremely granular. Never rewrite files entirely.

## Meta
- created: $(date +%Y-%m-%d)
- tick_mode: paused          <!-- auto | paused | stopped -->
- max_retries: 3           <!-- 单任务最大重试次数 -->
- max_tasks_per_tick: 1    <!-- 快任务时允许单 Tick 连续处理上限 -->
- max_diff_lines: 200      <!-- diff size guard 阈值 -->
- stale_lock_timeout: 15min <!-- [~] 僵尸锁重置阈值 -->
- circuit_breaker_threshold: 5 <!-- 连续失败多少次触发熔断 -->
- clean_strategy: git-clean <!-- 三阶段防爆清理机制 -->
- clean_ignore: .memento_cleanignore
- status_max_entries: 50    <!-- TICK_STATUS.md 最大条目数，超出自动归档 -->
- status_archive_dir: logs/status_archive/
- total_ticks: 0           <!-- 自动递增的 Tick 计数器 -->
- total_tasks: 0           <!-- 自动维护 -->
- completed_tasks: 0       <!-- 自动维护 -->

---

## Phase 1: Foundation
<!-- parallel: false -->
<!-- depends: none -->

- [ ] `T-101` [MODULE:init] Setup initial file structure
  - verify: `ls package.json || ls requirements.txt && echo PASS`
  - context_files: []
  - guard_files: []
  - estimate: 5min
  - retries: 0
PLAN

# Generate PROJECT_MAP.md template
cat << 'MAP' > "$PROJECT_DIR/docs/PROJECT_MAP.md"
# Project Map & Architecture

> Maintain a high-level list of files and their purposes so the Worker doesn't get lost.

## Directory Structure
- `src/`: 
- `docs/`: Memento physical state files
MAP

# Initialize empty TICK_STATUS and HUMAN_NOTES
echo "# TICK STATUS LOG" > "$PROJECT_DIR/docs/TICK_STATUS.md"

cat << 'NOTES' > "$PROJECT_DIR/docs/HUMAN_NOTES.md"
# Human Architect Notes

> Use this file to pass specific hints or constraints to the Tick Worker. 

- [NOTE:READ] For ticket T-101, make sure to use Node v20 conventions.
NOTES

# Ignore files
cat << 'IGNORE' > "$PROJECT_DIR/.gitignore"
node_modules/
__pycache__/
logs/
.env
IGNORE

cat << 'CIGNORE' > "$PROJECT_DIR/.memento_cleanignore"
node_modules/
.env
vendor/
logs/
CIGNORE

# Generate TICK_WORKER System Prompt
cat << 'PROMPT' > "$PROJECT_DIR/scripts/tick_worker_system_prompt.md"
# TICK WORKER PROTOCOL (MEMENTO v0.2)
You are an autonomous engineering agent functioning within the Memento Tick architecture. Your sole purpose during this lifecycle tick is to complete ONE specific sub-task from MASTER_PLAN.md with production-grade quality, verify it, and shut down gracefully.

## 1. Craftsmanship & Product Standard (CRITICAL)
Your outputs must reflect the standards of a Staff-level Product Engineer. Never produce "ugly proof-of-concept" code. 
- **UI/UX Aesthetics**: If you are generating front-end code (HTML/CSS/React/etc.), you MUST include modern, polished styling (e.g., responsive layouts, smooth animations, flex/grid, neat typography, color palettes, rounded corners, drop shadows, and hover effects). Never output naked HTML or blank white backgrounds.
- **Robust Logic & Asset Handling**: If a project requires assets (images, icons), do not just leave broken links or crude colored squares. Use robust procedural generation (Canvas, SVG), fetch public API data, or use elegant placeholders (emojis, unicode, CSS shapes) that genuinely look good. Handle edge cases to prevent crashes.
- **Enterprise-grade Structure**: Write modular, clean, and extensible code. If working in an evolving codebase, respect its architecture.

## 2. Your Tick Execution Loop
- **Context Loading**: Read `MASTER_PLAN.md`, `PROJECT_MAP.md`, and `HUMAN_NOTES.md`.
- **Target Selection**: Identify the FIRST pending `[ ]` task that is not blocked by unfinished phase dependencies. 
- **Execution**: Apply surgical, robust edits. Use targeted `sed`, `awk`, `ed`, Python AST scripts, or block-level file replacements (`cat << 'EOF'`). DO NOT truncate or rewrite massive files clumsily.
- **Verification (MANDATORY)**: You MUST run the specified `verify` command.
- **No Exit 0 = Failure**: Never claim "[x] done" or alter the plan to success if the verify step fails.

## 3. Communication & Data Integrity
- **Language Echo**: Mirror the user's language. If `MASTER_PLAN.md` or the prompt is in Chinese, you MUST write your `TICK_STATUS.md` logs, commit messages, and comments in Chinese (中文).
- **Atomic Commits**: Upon SUCCESS, you must run `git add -A && git commit -m "memento: <task_id> <brief desc>"` before terminating. Failures in this will cause Memento to wipe your work via git clean.
- **Immutable Boundaries**: Never modify `guard_files` unless explicitly requested. Do NOT alter the structure of `MASTER_PLAN.md`, only toggle `[ ]` to `[x]` and update retries.
- **Knowledge Transfer**: For every completed task, append newly exported interfaces, architecture notes, or major UI decisions under an `- **Outputs**:` bullet for the next tick worker to see in `TICK_STATUS.md`.
PROMPT

# Generate Dashboard script
cat << 'DASHBOARD' > "$PROJECT_DIR/scripts/dashboard.sh"
#!/usr/bin/env bash
cd "$(dirname "$0")/../.."
npm start -- --project-dir "$PROJECT_DIR" --port 3777
DASHBOARD

chmod +x "$PROJECT_DIR/scripts/dashboard.sh"

# Generate Tick Worker script
ENGINE_SCRIPT="$PROJECT_DIR/scripts/memento_tick.sh"
cat << 'ENGINE' > "$ENGINE_SCRIPT"
#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PLAN="$PROJECT_DIR/docs/MASTER_PLAN.md"
STATUS="$PROJECT_DIR/docs/TICK_STATUS.md"
LOG_DIR="$PROJECT_DIR/logs"
TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S)
TICK_LOG="$LOG_DIR/tick_${TIMESTAMP}.log"
LOCK_FILE="$PROJECT_DIR/.memento.lock"

# 防撞车：确保同一时间只有一个 Tick Worker 运行
exec 200>"$LOCK_FILE"
if ! flock -n 200; then
  echo "[$TIMESTAMP] Tick skipped: previous tick still running" >> "$STATUS"
  exit 0
fi


# Pre-Tick Meta Update
TOTAL_TASKS=$(grep -c '^- [' "$PLAN" || true)
COMPLETED_TASKS=$(grep -c '^- \[x]' "$PLAN" || true)
sed -i "s/^total_tasks: .*/total_tasks: $TOTAL_TASKS/" "$PLAN"
sed -i "s/^completed_tasks: .*/completed_tasks: $COMPLETED_TASKS/" "$PLAN"

# 检查 tick_mode
TICK_MODE=$(grep -oP 'tick_mode:\s*\K\w+' "$PLAN" || echo "stopped")
if [[ "$TICK_MODE" != "auto" ]]; then
  echo "[$TIMESTAMP] Tick skipped: mode=$TICK_MODE" >> "$STATUS"
  exit 0
fi

# 调用 LLM Agent 执行 Tick
SYS_CONTENT=$(cat "$PROJECT_DIR/scripts/tick_worker_system_prompt.md")
PLAN_CONTENT=$(cat "$PLAN" "$PROJECT_DIR/docs/PROJECT_MAP.md" "$PROJECT_DIR/docs/HUMAN_NOTES.md")
MSG="[SYSTEM CONTEXT]\n$SYS_CONTENT\n\n[TASK INSTRUCTION]\nRead $PLAN, locate the first executable task following the phase dependence and task retries logic, complete it, and update the tick status in $STATUS. Then perform the Verify step and act strictly based on the exit code. If failed, rollback using git checkout and increment retries in the plan.\n\n[FILE RESOURCES TACKED BELOW]\n$PLAN_CONTENT"

env -i PATH="$PATH" openclaw agent --local --json --session-id "memento-$(basename "$PROJECT_DIR")" -m "$MSG" 2>&1 | tee -a "$TICK_LOG"

# 后处理：防爆与三阶段清理
cd "$PROJECT_DIR"
if [[ -n $(git status --porcelain) ]]; then
  echo "[$TIMESTAMP] WARNING: Dirty workspace detected. Running 3-phase cleanup." >> "$STATUS"

  # Phase 1: 恢复已追踪文件
  git checkout -- .

  # Phase 2: 清理未追踪文件（排除保护列表）
  if [[ -f ".memento_cleanignore" ]]; then
    # 读取 ignore 文件并转换为 -e 选项
    EXCLUDES=$(awk '{printf "-e %s ", $0}' .memento_cleanignore)
    git stash push -m "memento-untracked-cleanup-$TIMESTAMP" -u $EXCLUDES
  else
    git stash push -m "memento-untracked-cleanup-$TIMESTAMP" -u
  fi

  # Phase 3: 兜底——如果还是脏的，紧急 stash
  if [[ -n $(git status --porcelain) ]]; then
    git stash --include-untracked -m "memento-emergency-stash-$TIMESTAMP"
    echo "[$TIMESTAMP] CRITICAL: Emergency stash created. Manual inspection required." >> "$STATUS"
  fi
fi

# 日志轮转
MAX_ENTRIES=$(grep -oP 'status_max_entries:\s*\K\d+' "$PLAN" || echo "50")
CURRENT_ENTRIES=$(grep -c '^\## \[' "$STATUS" || true)
if [[ $CURRENT_ENTRIES -gt $MAX_ENTRIES ]]; then
  ARCHIVE_DIR="$PROJECT_DIR/logs/status_archive"
  mkdir -p "$ARCHIVE_DIR"
  mv "$STATUS" "$ARCHIVE_DIR/TICK_STATUS_$(date +%Y%m%d_%H%M%S).md"
  echo "# TICK STATUS LOG" > "$STATUS"
  echo "" >> "$STATUS"
  echo "<!-- Rotated at $TIMESTAMP. Previous entries archived. -->" >> "$STATUS"
fi

# 告警检测
BLOCKED_COUNT=$(grep -cP '^\s*- \[\!\]' "$PLAN" || true)
CIRCUIT_BROKEN=$(grep -c 'CIRCUIT BREAKER' "$STATUS" || true)

if [[ $BLOCKED_COUNT -gt 0 || $CIRCUIT_BROKEN -gt 0 ]]; then
  cat > "$PROJECT_DIR/.memento_alert" << EOF_INNER
timestamp: $TIMESTAMP
blocked_tasks: $BLOCKED_COUNT
circuit_breaker: $([[ $CIRCUIT_BROKEN -gt 0 ]] && echo "TRIGGERED" || echo "OK")
message: Pipeline needs attention. $BLOCKED_COUNT task(s) blocked.
EOF_INNER
fi

# 如果一切正常且之前有告警，清除告警
if [[ $BLOCKED_COUNT -eq 0 && $CIRCUIT_BROKEN -eq 0 && -f "$PROJECT_DIR/.memento_alert" ]]; then
  rm -f "$PROJECT_DIR/.memento_alert"
fi

# 增加总 Tick 数
sed -i 's/total_ticks: [0-9]*/total_ticks: '$(($(grep -oP 'total_ticks: \K[0-9]+' "$PLAN" || echo 0) + 1))'/' "$PLAN"
ENGINE

chmod +x "$ENGINE_SCRIPT"

# Initialize Git
cd "$PROJECT_DIR"
git init
git add .
git commit -m "chore: memento framework init"

echo "✅ Project '$PROJECT_NAME' scaffolded successfully at $PROJECT_DIR."
echo "✅ Engineering plan injected: $PROJECT_DIR/docs/MASTER_PLAN.md"
echo "✅ Tick Engine erected at: $PROJECT_DIR/scripts/memento_tick.sh"
echo "💡 To begin autonomous execution, run or hook cron to: $PROJECT_DIR/scripts/memento_tick.sh"
