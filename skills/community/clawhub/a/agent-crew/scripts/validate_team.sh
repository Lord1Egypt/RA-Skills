#!/usr/bin/env bash
# validate_team.sh — 验证 Agent Team Builder 团队目录结构完整性
#
# Usage: ./validate_team.sh <team_dir>
#   team_dir: .claude/teams/<team_name> 目录路径
#
# Exit codes:
#   0 — 所有检查通过
#   1 — 存在错误（输出详情）

set -euo pipefail

TEAM_DIR="${1:-}"

if [[ -z "$TEAM_DIR" ]]; then
  echo "ERROR: 用法: $0 <team_dir>"
  echo "  示例: $0 .claude/teams/my_team"
  exit 1
fi

if [[ ! -d "$TEAM_DIR" ]]; then
  echo "ERROR: 团队目录不存在: $TEAM_DIR"
  exit 1
fi

ERRORS=0

# 1. 检查 team_charter.md
if [[ ! -f "$TEAM_DIR/team_charter.md" ]]; then
  echo "ERROR: 缺失 team_charter.md"
  ERRORS=$((ERRORS + 1))
fi

# 2. 检查每个角色子目录
for ROLE_DIR in "$TEAM_DIR"/*/; do
  # 跳过非目录项
  [[ -d "$ROLE_DIR" ]] || continue
  # 跳过非角色目录（如已存在的 workspace 顶级目录等）
  ROLE_NAME="$(basename "$ROLE_DIR")"

  # 2a. 检查 workspace/
  if [[ ! -d "$ROLE_DIR/workspace" ]]; then
    echo "ERROR: 角色 '$ROLE_NAME' 缺失 workspace/ 目录"
    ERRORS=$((ERRORS + 1))
  fi

  # 2b. 检查 skills/
  if [[ ! -d "$ROLE_DIR/skills" ]]; then
    echo "ERROR: 角色 '$ROLE_NAME' 缺失 skills/ 目录"
    ERRORS=$((ERRORS + 1))
  fi

  # 2c. 检查 memory.md
  if [[ ! -f "$ROLE_DIR/memory.md" ]]; then
    echo "ERROR: 角色 '$ROLE_NAME' 缺失 memory.md"
    ERRORS=$((ERRORS + 1))
  fi

  # 2d. 检查 progress.md
  if [[ ! -f "$ROLE_DIR/progress.md" ]]; then
    echo "ERROR: 角色 '$ROLE_NAME' 缺失 progress.md"
    ERRORS=$((ERRORS + 1))
  fi

  # 2e. 检查 .claude/agents/<role_name>.md
  AGENT_CONFIG=".claude/agents/${ROLE_NAME}.md"
  if [[ ! -f "$AGENT_CONFIG" ]]; then
    echo "ERROR: 角色 '$ROLE_NAME' 缺失 .claude/agents/${ROLE_NAME}.md 配置"
    ERRORS=$((ERRORS + 1))
  fi

  # 2f. 验证 agent 配置 frontmatter 必填字段
  if [[ -f "$AGENT_CONFIG" ]]; then
    for FIELD in name description type; do
      if ! grep -q "^${FIELD}:" "$AGENT_CONFIG"; then
        echo "ERROR: 角色 '$ROLE_NAME' 的 agent 配置缺失 frontmatter 字段 '$FIELD'"
        ERRORS=$((ERRORS + 1))
      fi
    done
  fi
done

# 3. 结果输出
if [[ $ERRORS -gt 0 ]]; then
  echo ""
  echo "验证失败: 共 $ERRORS 个错误"
  exit 1
else
  echo "验证通过: 团队结构完整"
  exit 0
fi
