#!/usr/bin/env bash
# =============================================================================
# run.sh - ai-literacy-expert-v7.3 Linux/macOS entry point (never rename).
#
# Flow:
#   1. set -euo pipefail
#   2. Parse arguments (subcommand routing)
#   3. Hardware detection (Intel AIPC / MTL·LNL·ARL·PTL iGPU / dGPU whitelist)
#   4. Ensure Python environment
#   5. Route to pipeline script (bootstrap / prepare / analyze / select / compose / exchange)
#
# Usage:
#   ./run.sh bootstrap <course_dir>              # 一键准备 + 4 阶段流水线
#   ./run.sh prepare   <course_dir>              # 阶段 1: 工作区初始化
#   ./run.sh analyze   <workspace_dir>           # 阶段 2: 本地文本推理
#   ./run.sh select    <workspace_dir>           # 阶段 3: 知识点筛选
#   ./run.sh compose   <workspace_dir>           # 阶段 4: 合成课件
#   ./run.sh exchange  <request.json>            # 端云协议交换
#   ./run.sh validate  <request.json>            # 协议 schema 校验
#   ./run.sh check                                # 硬件 + Python 预检
#   ./run.sh --continue                           # 断点续传（恢复中断的下载）
#
# Exit codes:
#   0  Success
#   1  General error (bad args / unsupported hardware / env install failed)
#   2  Communication error (edge-cloud exchange failure)
#   3  Model downloading — rerun with --continue
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$SCRIPT_DIR"
SCRIPTS="$ROOT/scripts"

# --- 1. Parse subcommand ----------------------------------------------------
if [[ $# -eq 0 ]]; then
    echo "Usage: ./run.sh <command> [args]"
    echo "  bootstrap <course_dir>   一键准备 + 4 阶段流水线"
    echo "  prepare   <course_dir>   阶段 1: 工作区初始化"
    echo "  analyze   <workspace>    阶段 2: 本地文本推理"
    echo "  select    <workspace>    阶段 3: 知识点筛选"
    echo "  compose   <workspace>    阶段 4: 合成课件"
    echo "  exchange  <req.json>     端云协议交换"
    echo "  validate  <req.json>     协议 schema 校验"
    echo "  check                    硬件 + Python 预检"
    echo "  --continue               断点续传（恢复下载）"
    exit 1
fi

CMD="$1"
shift || true
CMD_ARGS=("$@")

# --- 2. Hardware detection (only for pipeline commands) ---------------------
HARDWARE_CMDS=("bootstrap" "prepare" "analyze" "select" "compose" "check")

is_hardware_cmd=false
for hc in "${HARDWARE_CMDS[@]}"; do
    if [[ "$CMD" == "$hc" ]]; then
        is_hardware_cmd=true
        break
    fi
done

if [[ "$is_hardware_cmd" == "true" ]]; then
    # Linux/macOS: check for Intel GPU via lspci / system_profiler
    # Note: Intel AIPC hardware check is informational on non-Windows platforms
    if command -v lspci &>/dev/null; then
        if ! lspci 2>/dev/null | grep -qi "intel"; then
            echo "[run.sh] ⚠ No Intel GPU detected via lspci. Continuing anyway..." >&2
        fi
    fi
    # Python version check
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "0.0")
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
    if [[ "$PYTHON_MAJOR" -lt 3 ]] || ([[ "$PYTHON_MAJOR" -eq 3 ]] && [[ "$PYTHON_MINOR" -lt 10 ]]); then
        echo "[run.sh] ✗ Python >= 3.10 required (found $PYTHON_VERSION). Exit 1." >&2
        exit 1
    fi
fi

# 'check' command stops here after hardware + python verification
if [[ "$CMD" == "check" ]]; then
    echo "[run.sh] ✓ All preflight checks passed."
    exit 0
fi

# --- 3. Ensure Python environment -------------------------------------------
# On Linux/macOS, use system Python3 or .venv if available
VENV_PYTHON="$ROOT/.venv/bin/python"
if [[ ! -f "$VENV_PYTHON" ]]; then
    # Try to create venv
    if command -v python3 &>/dev/null; then
        echo "[run.sh] Creating .venv..."
        python3 -m venv "$ROOT/.venv" 2>/dev/null || true
        if [[ -f "$ROOT/requirements.txt" ]] && [[ -f "$VENV_PYTHON" ]]; then
            "$VENV_PYTHON" -m pip install --upgrade pip -q 2>/dev/null || true
            "$VENV_PYTHON" -m pip install -r "$ROOT/requirements.txt" -q 2>/dev/null || true
        fi
    fi
fi

# Fall back to system python3 if venv not available
if [[ ! -f "$VENV_PYTHON" ]]; then
    VENV_PYTHON="python3"
    echo "[run.sh] ⚠ venv not found, using system python3: $VENV_PYTHON" >&2
fi

# --- 4. Route to pipeline script --------------------------------------------
case "$CMD" in
    bootstrap)
        exec "$VENV_PYTHON" "$SCRIPTS/bootstrap.py" "${CMD_ARGS[@]}"
        ;;
    prepare)
        exec "$VENV_PYTHON" "$SCRIPTS/prepare_workspace.py" "${CMD_ARGS[@]}"
        ;;
    analyze)
        exec "$VENV_PYTHON" "$SCRIPTS/analyze_courseware.py" "${CMD_ARGS[@]}"
        ;;
    select)
        exec "$VENV_PYTHON" "$SCRIPTS/select_knowledge.py" "${CMD_ARGS[@]}"
        ;;
    compose)
        exec "$VENV_PYTHON" "$SCRIPTS/compose_lesson.py" "${CMD_ARGS[@]}"
        ;;
    exchange)
        "$VENV_PYTHON" "$SCRIPTS/edge_cloud_dispatch.py" exchange "${CMD_ARGS[@]}"
        CODE=$?
        if [[ $CODE -eq 0 ]]; then exit 0; fi
        if [[ $CODE -eq 2 ]]; then exit 2; fi
        exit 1
        ;;
    validate)
        exec "$VENV_PYTHON" "$SCRIPTS/edge_cloud_dispatch.py" validate "${CMD_ARGS[@]}"
        ;;
    --continue)
        "$VENV_PYTHON" "$SCRIPTS/setup_text_model.py" --continue "${CMD_ARGS[@]}"
        CODE=$?
        if [[ $CODE -eq 3 ]]; then
            echo "[run.sh] 下载未完成，请再次运行 --continue 继续下载。"
            exit 3
        fi
        exit $CODE
        ;;
    *)
        echo "[run.sh] Unknown command: $CMD" >&2
        echo "Run './run.sh' without args to see usage." >&2
        exit 1
        ;;
esac
