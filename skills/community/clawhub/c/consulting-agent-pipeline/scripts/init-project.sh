#!/bin/bash
# init-project.sh — 项目初始化脚本
# 用法：./init-project.sh <项目名称> <项目根目录> [项目类型]
# 示例：./init-project.sh "首钢吉泰安" "/Users/leroy/Desktop/项目/X" "consulting"
# 项目类型：consulting（咨询）| research（研究）| product（产品）

set -e

PROJECT_NAME="${1:-}"
PROJECT_ROOT="${2:-}"
PROJECT_TYPE="${3:-consulting}"

if [[ -z "$PROJECT_NAME" || -z "$PROJECT_ROOT" ]]; then
  echo "用法: $0 <项目名称> <项目根目录> [项目类型]"
  echo "示例: $0 \"首钢吉泰安\" \"/Users/leroy/Desktop/项目/X\" consulting"
  exit 1
fi

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATE_DIR="$SKILL_DIR/templates"

echo "=== 项目初始化: $PROJECT_NAME ==="
echo "项目根目录: $PROJECT_ROOT"
echo "项目类型: $PROJECT_TYPE"
echo ""

# 创建目录结构
mkdir -p "$PROJECT_ROOT/00_pipeline"
mkdir -p "$PROJECT_ROOT/00_pipeline/handoffs"
mkdir -p "$PROJECT_ROOT/00_pipeline/snapshots"

# 生成项目ID（前缀 + 随机4位hex）
PROJECT_ID=$(echo "$PROJECT_NAME" | sed 's/[^a-zA-Z0-9]//g' | cut -c1-4 | tr '[:upper:]' '[:lower:]')
PROJECT_ID="${PROJECT_ID}-$(date +%m%d)"

echo "项目ID: $PROJECT_ID"
echo ""

# 复制模板
echo "创建模板文件..."

# PROJECT_STATE.yaml
sed "s/PROJECT_NAME/$PROJECT_NAME/g; s/PROJECT_ID/$PROJECT_ID/g; s/PROJECT_TYPE/$PROJECT_TYPE/g" \
  "$TEMPLATE_DIR/PROJECT_STATE.yaml.template" > "$PROJECT_ROOT/00_pipeline/PROJECT_STATE.yaml"

# FORBIDDEN_TERMS.yaml（从模板复制）
cp "$TEMPLATE_DIR/FORBIDDEN_TERMS.yaml" "$PROJECT_ROOT/00_pipeline/FORBIDDEN_TERMS.yaml"

# AGENT_REGISTRY.yaml
cp "$TEMPLATE_DIR/AGENT_REGISTRY.yaml" "$PROJECT_ROOT/00_pipeline/AGENT_REGISTRY.yaml"

# DECISION_LOG.md
cp "$TEMPLATE_DIR/DECISION_LOG.md" "$PROJECT_ROOT/00_pipeline/DECISION_LOG.md"

# Phase README 模板
cp "$TEMPLATE_DIR/PHASE_README_TEMPLATE.md" "$PROJECT_ROOT/00_pipeline/PHASE_README.md"

echo "✅ 模板文件创建完成"
echo ""

# 输出目录结构
echo "=== 初始化完成 ==="
echo "项目目录结构:"
ls -la "$PROJECT_ROOT/00_pipeline/"

echo ""
echo "下一步："
echo "1. 编辑 $PROJECT_ROOT/00_pipeline/PROJECT_STATE.yaml，填写项目成员和Agent分配"
echo "2. 编辑 $PROJECT_ROOT/00_pipeline/AGENT_REGISTRY.yaml，注册所有参与的Agent"
echo "3. 编辑 $PROJECT_ROOT/00_pipeline/FORBIDDEN_TERMS.yaml，声明项目禁用词"
echo "4. 在 DECISION_LOG.md 中记录初始决策（如框架方向）"
echo "5. 运行 'openclaw skills install multi-agent-pipeline' 确保技能已激活"
