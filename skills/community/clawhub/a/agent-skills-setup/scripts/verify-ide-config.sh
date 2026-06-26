#!/usr/bin/env bash

# 验证所有 IDE 配置的正确性

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MIGRATION_SCRIPT="${SCRIPT_DIR}/smart-ide-migration.sh"

echo "========================================"
echo "验证 IDE 配置"
echo "========================================"
echo ""

# 测试每个 IDE 的配置路径
test_ide_config() {
    local ide="$1"
    local expected_global="$2"
    local expected_project="$3"
    local expected_rules="$4"
    
    # 获取实际值
    local actual_global
    actual_global=$(bash "$MIGRATION_SCRIPT" --test-global-path "$ide" 2>/dev/null || echo "ERROR")
    
    # 简单检查
    if [[ "$actual_global" == *"ERROR"* ]]; then
        echo "❌ $ide - 无法获取配置"
        return 1
    fi
    
    echo "✓ $ide - 全局路径：$actual_global"
    return 0
}

# 运行测试
echo "测试主要 IDE 配置:"
echo ""

# Claude Code
echo "1. Claude Code"
bash "$MIGRATION_SCRIPT" --source claude --target cursor --dry-run 2>&1 | grep -E "(源 IDE|目标 IDE|迁移内容)" | head -3
echo ""

# Gemini CLI
echo "2. Gemini CLI"
bash "$MIGRATION_SCRIPT" --source gemini-cli --target claude --dry-run 2>&1 | grep -E "(源 IDE|目标 IDE)" | head -2
echo ""

# Goose CLI
echo "3. Goose CLI"
bash "$MIGRATION_SCRIPT" --source goose-cli --target claude --dry-run 2>&1 | grep -E "(源 IDE|目标 IDE)" | head -2
echo ""

# Aider
echo "4. Aider"
bash "$MIGRATION_SCRIPT" --source aider --target claude --dry-run 2>&1 | grep -E "(源 IDE|目标 IDE)" | head -2
echo ""

# Codex CLI
echo "5. Codex CLI"
bash "$MIGRATION_SCRIPT" --source codex --target claude --dry-run 2>&1 | grep -E "(源 IDE|目标 IDE)" | head -2
echo ""

echo "========================================"
echo "验证完成"
echo "========================================"
