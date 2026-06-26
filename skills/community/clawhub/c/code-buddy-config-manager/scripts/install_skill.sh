#!/bin/bash
# =============================================================================
# CodeBuddy Skill 安装/更新脚本
# 安装或更新 Skill（从 marketplace 或自定义创建）
#
# 用法: ./install_skill.sh <config_name> [config_scope] [--from-url <url>]
#       ./install_skill.sh <config_name> [config_scope] [--create]
#
# 参数:
#   config_name  - Skill 名称
#   config_scope - 作用域: global | project (默认: project)
#   --from-url   - 从指定 URL 下载 Skill
#   --create     - 创建自定义 Skill 的引导（需要 AI 配合）
#
# 输出: JSON 格式的安装结果
# =============================================================================

set -eo pipefail

# ---------- 参数解析 ----------
CONFIG_NAME="${1:-}"
CONFIG_SCOPE="${2:-project}"
MODE="${3:-auto}"

if [ -z "$CONFIG_NAME" ]; then
  echo '{"success":false,"error":"Usage: install_skill.sh <config_name> [scope] [--from-url <url>|--create]"}'
  exit 1
fi

# 处理可选参数
INSTALL_MODE="auto"
SKILL_URL=""
CREATE_MODE=false

case "${3:-}" in
  --from-url)
    INSTALL_MODE="url"
    SKILL_URL="${4:-}"
    [ -z "$SKILL_URL" ] && { echo '{"success":false,"error":"--from-url 需要提供 URL"}'; exit 1; }
    ;;
  --create)
    INSTALL_MODE="create"
    CREATE_MODE=true
    ;;
esac

# ---------- 路径常量 ----------
HOME_DIR="$HOME"
PROJECT_DIR="$(cd "$(dirname "$0")/../../../.." 2>/dev/null && pwd || echo "")"

MARKETPLACE_SKILLS_DIR="$HOME_DIR/.codebuddy/skills-marketplace/skills"
MARKETPLACE_INDEX="$HOME_DIR/.codebuddy/skills-marketplace/.codebuddy-skill/marketplace.json"

if [ "$CONFIG_SCOPE" = "global" ]; then
  TARGET_DIR="$MARKETPLACE_SKILLS_DIR/$CONFIG_NAME"
  SKILLS_PARENT="$MARKETPLACE_SKILLS_DIR"
else
  TARGET_DIR="$PROJECT_DIR/.codebuddy/skills/$CONFIG_NAME"
  SKILLS_PARENT="$PROJECT_DIR/.codebuddy/skills"
fi

# ---------- JSON 输出辅助 ----------
output_result() {
  local success="$1"
  local message="$2"
  local detail="${3:-}"
  cat <<EOF
{
  "success": $success,
  "message": "$(echo "$message" | perl -CS -pe 's/"/\\"/g' 2>/dev/null || echo "$message")",
  "config_name": "$CONFIG_NAME",
  "scope": "$CONFIG_SCOPE",
  "target_path": "$TARGET_DIR"
}
EOF
  exit $([ "$success" = "true" ] && echo 0 || echo 1)
}

# ---------- 确保目录 ----------
ensure_dir() {
  mkdir -p "$TARGET_DIR"
}

# ---------- 从 marketplace 搜索并安装 ----------
install_from_marketplace() {
  echo "  在 Skill Marketplace 中搜索 '$CONFIG_NAME'..."

  if [ ! -f "$MARKETPLACE_INDEX" ]; then
    return 1
  fi

  # 从 marketplace index 搜索（Python 解析）
  local found
  found=$(python3 << PYEOF
import json, sys

try:
    with open("$MARKETPLACE_INDEX") as f:
        index = json.load(f)
except:
    sys.stdout.write("NOT_FOUND")
    sys.exit(0)

name = "$CONFIG_NAME".lower()

# 搜索技能列表（index 结构因版本而异）
skills = []
if isinstance(index, list):
    skills = index
elif isinstance(index, dict):
    for key in ("skills", "items", "packages", "entries"):
        if key in index and isinstance(index[key], list):
            skills = index[key]
            break

for skill in skills:
    sname = ""
    if isinstance(skill, dict):
        sname = skill.get("name", "") or skill.get("id", "") or skill.get("title", "")
    elif isinstance(skill, str):
        sname = skill

    sname_lower = sname.lower()
    if sname_lower == name or sname_lower.replace("-", "") == name.replace("-", ""):
        sys.stdout.write(json.dumps(skill))
        sys.exit(0)

# 模糊搜索
for skill in skills:
    sname = ""
    if isinstance(skill, dict):
        sname = skill.get("name", "") or skill.get("id", "") or skill.get("title", "")
    elif isinstance(skill, str):
        sname = skill
    if name in sname.lower():
        sys.stdout.write("FUZZY:" + sname)
        sys.exit(0)

sys.stdout.write("NOT_FOUND")
PYEOF
) || echo "NOT_FOUND"

  case "$found" in
    NOT_FOUND)
      return 1
      ;;
    FUZZY:*)
      local fuzzy_name="${found#FUZZY:}"
      echo "  发现相似 Skill: $fuzzy_name"
      # 如果全局已安装，复制到目标
      if [ -d "$MARKETPLACE_SKILLS_DIR/$fuzzy_name" ]; then
        echo "  从全局市场复制 '$fuzzy_name'..."
        ensure_dir
        cp -r "$MARKETPLACE_SKILLS_DIR/$fuzzy_name" "$TARGET_DIR" 2>/dev/null || {
          # 如果目录已存在，只更新 SKILL.md
          cp "$MARKETPLACE_SKILLS_DIR/$fuzzy_name/SKILL.md" "$TARGET_DIR/SKILL.md" 2>/dev/null || true
        }
        output_result true "Skill '$CONFIG_NAME' 已安装（源: $fuzzy_name）"
      fi
      return 1
      ;;
    *)
      # 找到了精确匹配，尝试安装
      echo "  在 Marketplace 中找到匹配的 Skill"
      # 如果全局已有
      if [ -d "$MARKETPLACE_SKILLS_DIR/$CONFIG_NAME" ]; then
        echo "  从全局市场复制到目标位置..."
        ensure_dir
        cp -r "$MARKETPLACE_SKILLS_DIR/$CONFIG_NAME"/* "$TARGET_DIR/" 2>/dev/null || true
        output_result true "Skill '$CONFIG_NAME' 已从市场安装"
      fi
      return 1
      ;;
  esac
}

# ---------- 从 URL 安装 ----------
install_from_url() {
  local url="$SKILL_URL"
  echo "  从 $url 下载 Skill..."

  local tmpdir
  tmpdir=$(mktemp -d 2>/dev/null || mktemp -d -t skill 2>/dev/null)
  trap 'rm -rf "$tmpdir"' EXIT

  # 下载（支持 zip 和 直接文件）
  if curl -sL --connect-timeout 10 -o "$tmpdir/skill.zip" "$url" 2>/dev/null || \
     wget -qO "$tmpdir/skill.zip" --timeout=10 "$url" 2>/dev/null; then
    # 如果是 zip 文件
    if file "$tmpdir/skill.zip" | grep -qi "zip"; then
      unzip -qo "$tmpdir/skill.zip" -d "$tmpdir/extracted" 2>/dev/null || true
      ensure_dir
      cp -r "$tmpdir/extracted"/* "$TARGET_DIR/" 2>/dev/null || true
      output_result true "Skill '$CONFIG_NAME' 已从 URL 安装"
    else
      # 可能是单个 SKILL.md
      ensure_dir
      cp "$tmpdir/skill.zip" "$TARGET_DIR/SKILL.md" 2>/dev/null || true
      output_result true "Skill '$CONFIG_NAME' SKILL.md 已从 URL 下载"
    fi
  else
    # 如果下载失败，建议使用其他方式
    output_result false "从 URL 下载失败" "请确认 URL 可访问，或使用 --create 模式创建"
  fi
}

# ---------- 创建自定义 Skill ----------
create_skill() {
  echo "  创建自定义 Skill '$CONFIG_NAME'..."
  ensure_dir

  if [ -f "$TARGET_DIR/SKILL.md" ]; then
    output_result true "Skill '$CONFIG_NAME' 已存在于 $TARGET_DIR，无需创建"
  fi

  # 创建目标目录和 SKILL.md 模板
  mkdir -p "$TARGET_DIR"
  cat > "$TARGET_DIR/SKILL.md" << SKILLEOF
---
name: $CONFIG_NAME
description: 自定义 Skill - $CONFIG_NAME
version: 1.0.0
---

# $CONFIG_NAME

## 前提条件

无特殊前提条件。

## 核心工作流

请根据实际需求定义工作流程。

## 使用示例

\`\`\`
请在此处添加使用示例
\`\`\`
SKILLEOF

  # 创建 references 目录
  mkdir -p "$TARGET_DIR/references"

  output_result true "Skill '$CONFIG_NAME' 模板已创建，请编辑 $TARGET_DIR/SKILL.md 完善内容"
}

# =============================================================================
# 主逻辑
# =============================================================================

echo "═══════════════════════════════════════════"
echo "  Skill 安装/更新: $CONFIG_NAME"
echo "  作用域: $CONFIG_SCOPE"
echo "  模式: $INSTALL_MODE"
echo "═══════════════════════════════════════════"

case "$INSTALL_MODE" in
  url)
    install_from_url
    ;;
  create)
    create_skill
    ;;
  auto)
    # 自动模式：先尝试 marketplace，再尝试 URL/创建
    if install_from_marketplace; then
      :
    else
      echo "  Marketplace 未找到匹配，是否尝试创建自定义 Skill？"
      echo "  使用 [skill:skill-creator] 创建自定义 Skill..."
      create_skill
    fi
    ;;
esac
