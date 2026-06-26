#!/bin/bash
# Codex Runner - Stop command

echo "=== 停止 Codex 进程 ==="
pkill -f "codex.*exec"

echo "已停止所有 Codex 进程"
