#!/usr/bin/env bash
# Skill Organizer - 自动分类 skills 到全局/专属目录
# 用法: bash organize-skills.sh

set -euo pipefail

# 颜色
G='\033[0;32m' Y='\033[1;33m' C='\033[0;36m' B='\033[1m' N='\033[0m'

SKILLS_DIR="$HOME/.openclaw/skills"
WORKSPACE_DIR="$HOME/.openclaw/workspace"

# ──────────────────────────────────────
# 共享 skill 名单（所有人都用得上的）
# 在这里定义，不在列表里的默认归为专属
# ──────────────────────────────────────
SHARED_SKILLS=(
    "agent-quantizer"
    "context-manager"
    "mimo-omni"
    "summarize"
    "weather"
    "chart-image"
    "svg-draw"
    "excel-xlsx"
    "word-docx"
    "powerpoint-pptx"
)

# ──────────────────────────────────────
# 检查当前状态
# ──────────────────────────────────────
echo -e "${B}📦 Skill 分类工具${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 列出全局 skills
echo -e "\n${C}全局 Skills (${SKILLS_DIR}):${NC}"
if [[ -d "$SKILLS_DIR" ]]; then
    for d in "$SKILLS_DIR"/*/; do
        [[ -d "$d" ]] && echo "  ✅ $(basename "$d")"
    done
else
    echo "  (目录不存在)"
fi

# 列出所有 workspace skills
echo -e "\n${C}各 Agent Workspace Skills:${NC}"
for ws in "$HOME/.openclaw/workspace"*; do
    if [[ -d "$ws/skills" ]]; then
        ws_name=$(basename "$ws")
        echo -e "  ${Y}${ws_name}:${NC}"
        for d in "$ws/skills"/*/; do
            [[ -d "$d" ]] && echo "    📁 $(basename "$d")"
        done
    fi
done

# ──────────────────────────────────────
# 分析建议
# ──────────────────────────────────────
echo -e "\n${B}🔍 分析结果${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 找出 workspace 里应该移到全局的
echo -e "\n${Y}可以移到全局的 skill（多人共用）:${NC}"
for ws in "$HOME/.openclaw/workspace"*; do
    if [[ -d "$ws/skills" ]]; then
        ws_name=$(basename "$ws")
        for shared in "${SHARED_SKILLS[@]}"; do
            if [[ -d "$ws/skills/$shared" ]]; then
                echo "  → $shared (${ws_name} → 全局)"
            fi
        done
    fi
done

# 找出全局里可能是专属的
echo -e "\n${Y}可能是专属的 skill（只有特定角色用）:${NC}"
if [[ -d "$SKILLS_DIR" ]]; then
    for d in "$SKILLS_DIR"/*/; do
        [[ -d "$d" ]] || continue
        name=$(basename "$d")
        is_shared=false
        for shared in "${SHARED_SKILLS[@]}"; do
            [[ "$name" == "$shared" ]] && is_shared=true && break
        done
        if ! $is_shared; then
            echo "  → $name (检查是否只有特定 agent 用)"
        fi
    done
fi

# ──────────────────────────────────────
# 执行移动
# ──────────────────────────────────────
echo -e "\n${B}要执行移动吗？(y/N)${NC}"
read -r confirm

if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "跳过。以上是建议，你可以手动调整。"
    exit 0
fi

moved=0
for ws in "$HOME/.openclaw/workspace"*; do
    [[ -d "$ws/skills" ]] || continue
    ws_name=$(basename "$ws")

    for shared in "${SHARED_SKILLS[@]}"; do
        src="$ws/skills/$shared"
        dst="$SKILLS_DIR/$shared"

        if [[ -d "$src" ]] && [[ ! -d "$dst" ]]; then
            echo -e "  ${G}移动:${NC} $shared ($ws_name → 全局)"
            mv "$src" "$dst"
            ((moved++))
        elif [[ -d "$src" ]] && [[ -d "$dst" ]]; then
            echo -e "  ${Y}跳过:${NC} $shared (全局已存在)"
        fi
    done
done

echo -e "\n${G}✅ 完成！移动了 ${moved} 个 skill 到全局目录${NC}"
echo "重启生效: openclaw gateway restart"
