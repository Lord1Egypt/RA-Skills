#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [ -n "${CMCC_NEWMSG_HOME:-}" ]; then
  STATE_DIR="$(cd "$(dirname "$CMCC_NEWMSG_HOME")" 2>/dev/null && pwd)/$(basename "$CMCC_NEWMSG_HOME")" 2>/dev/null || STATE_DIR="$CMCC_NEWMSG_HOME"
elif [ -n "${HERMES_HOME:-}" ]; then
  STATE_DIR="$HERMES_HOME/cmcc-newmsg"
else
  STATE_DIR="$HOME/.cmcc-newmsg"
fi

VENV_DIR="$STATE_DIR/venv"
mkdir -p "$STATE_DIR"

if [ ! -x "$VENV_DIR/bin/python" ]; then
  "$PYTHON_BIN" -m venv "$VENV_DIR" || {
    echo "创建 Python venv 失败。Ubuntu/Debian 可先安装 python3-venv；Termux 请确认 python 包完整。" >&2
    exit 1
  }
fi

"$VENV_DIR/bin/python" -m pip install -q --upgrade pip
"$VENV_DIR/bin/python" -m pip install -q -r "$SCRIPT_DIR/requirements.txt"
CMCC_NEWMSG_HOME="$STATE_DIR" "$VENV_DIR/bin/python" "$SCRIPT_DIR/scripts/cmcc_newmsg.py" init

printf '\n安装完成。\n'
printf '状态目录: %s\n' "$STATE_DIR"
printf '1. 编辑 API Key: %s/.env\n' "$STATE_DIR"
printf '2. 本地检查: sh %s/scripts/run.sh check\n' "$SCRIPT_DIR"
printf '3. 联网认证: sh %s/scripts/run.sh doctor\n' "$SCRIPT_DIR"
