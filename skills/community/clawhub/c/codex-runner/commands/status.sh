#!/bin/bash
# Codex Runner - Status command

echo "=== Codex 进程状态 ==="
ps aux | grep -i codex | grep -v grep

echo ""
echo "=== 进程数量 ==="
ps aux | grep -i codex | grep -v grep | wc -l
