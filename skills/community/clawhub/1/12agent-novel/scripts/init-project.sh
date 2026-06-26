#!/usr/bin/env bash
#
# 12Agent Novel 项目初始化脚本
# 适用环境：Unix / Linux / macOS / Git Bash / WSL
# 依赖：bash、cp、sed、date
# 用法: ./init-project.sh <项目名称> [项目路径]
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

sedi() {
    if [[ "$OSTYPE" == darwin* ]]; then
        sed -i '' "$@"
    else
        sed -i "$@"
    fi
}

replace_token() {
    local file="$1"
    local token="$2"
    local value="$3"
    local escaped_value
    escaped_value=$(printf '%s' "$value" | sed 's/[\/&]/\\&/g')
    sedi "s/{{$token}}/$escaped_value/g" "$file"
}

replace_tokens_in_file() {
    local file="$1"
    shift

    if [ ! -f "$file" ]; then
        return
    fi

    while [ $# -gt 1 ]; do
        replace_token "$file" "$1" "$2"
        shift 2
    done
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DEFAULT_PROJECTS_DIR="$SKILL_DIR/projects"

show_help() {
    echo "用法: $0 <项目名称> [项目路径]"
    echo ""
    echo "参数:"
    echo "  项目名称    新项目的名称（必需）"
    echo "  项目路径    项目存放路径（可选，默认为 $DEFAULT_PROJECTS_DIR）"
    echo ""
    echo "示例:"
    echo "  $0 xiu-xian-zhuan"
    echo "  $0 xiu-xian-zhuan /home/user/novels"
    echo "  （Iron Rule：项目名禁止中文，请使用拼音，如 '修仙传' → 'xiu-xian-zhuan'）"
    exit 0
}

if [ $# -eq 0 ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_help
fi

PROJECT_NAME="$1"
PROJECTS_DIR="${2:-$DEFAULT_PROJECTS_DIR}"
PROJECT_DIR="$PROJECTS_DIR/$PROJECT_NAME"
CURRENT_DATE=$(date +%Y-%m-%d)
TARGET_SCOPE="待补充"

if [ -z "$PROJECT_NAME" ]; then
    echo -e "${RED}错误: 项目名称不能为空${NC}"
    exit 1
fi

if [[ ! "$PROJECT_NAME" =~ ^[a-zA-Z0-9_-]+$ ]]; then
    echo -e "${RED}错误: 项目名称只能包含英文字母、数字、下划线、连字符${NC}"
    echo -e "${YELLOW}提示: 中文名请转为拼音，例如 '修仙传' → 'xiu-xian-zhuan'${NC}"
    exit 1
fi

if [ -d "$PROJECT_DIR" ]; then
    echo -e "${RED}错误: 项目 '$PROJECT_NAME' 已存在于 $PROJECT_DIR${NC}"
    exit 1
fi

echo -e "${BLUE}正在创建项目: $PROJECT_NAME${NC}"
echo -e "${BLUE}项目路径: $PROJECT_DIR${NC}"

mkdir -p "$PROJECT_DIR"
cp -r "$SKILL_DIR/assets/project-template/." "$PROJECT_DIR/"

# 确保运行时写入目录存在（模板中的 .gitkeep 不会被 cp 遗漏，但显式补全以防万一）
mkdir -p "$PROJECT_DIR/archive/reader-feedback"
mkdir -p "$PROJECT_DIR/archive/milestone-audit"
mkdir -p "$PROJECT_DIR/chapters/history"

PROJECT_FILE="$PROJECT_DIR/meta/project.md"
METADATA_FILE="$PROJECT_DIR/meta/metadata.json"
CONFIG_FILE="$PROJECT_DIR/meta/config.md"
WORKFLOW_STATE_FILE="$PROJECT_DIR/meta/workflow-state.json"
REGISTRY_FILE="$PROJECT_DIR/meta/agent-registry.json"
ARCHIVE_FILE="$PROJECT_DIR/archive/archive.md"
STYLE_FILE="$PROJECT_DIR/meta/style-anchor.md"
SELECTED_STYLE_FILE="$PROJECT_DIR/meta/selected-style-sample.md"
STATE_FILE="$PROJECT_DIR/references/state-tracker.md"
RELATIONSHIP_FILE="$PROJECT_DIR/references/relationship-tracker.md"
PLOT_FILE="$PROJECT_DIR/references/plot-tracker.md"
ROLLING_FILE="$PROJECT_DIR/references/rolling-summary.md"
WORLD_FILE="$PROJECT_DIR/worldbuilding/world.md"
OUTLINE_FILE="$PROJECT_DIR/outline/outline.md"
CHAPTER_OUTLINE_FILE="$PROJECT_DIR/outline/chapter-outline.md"

replace_tokens_in_file "$METADATA_FILE" \
    "project_title" "$PROJECT_NAME" \
    "updated_at" "$CURRENT_DATE"

replace_tokens_in_file "$WORKFLOW_STATE_FILE" \
    "updated_at" "$CURRENT_DATE"

replace_tokens_in_file "$PROJECT_FILE" \
    "project_title" "$PROJECT_NAME" \
    "genre" "待补充" \
    "style_tags" "#待补充" \
    "target_scope" "$TARGET_SCOPE" \
    "tone" "待补充" \
    "created_at" "$CURRENT_DATE" \
    "updated_at" "$CURRENT_DATE" \
    "r18" "❌ 否" \
    "explicit" "❌ 否" \
    "be_ending" "❌ 默认HE" \
    "special_elements" "待补充" \
    "project_summary" "待补充"

replace_tokens_in_file "$CONFIG_FILE" \
    "worldbuilder_model" "provider/model-id" \
    "characterDesigner_model" "provider/model-id" \
    "outlinePlanner_model" "provider/model-id" \
    "chapterOutliner_model" "provider/model-id" \
    "mainWriter_model" "provider/model-id" \
    "oocGuardian_model" "provider/model-id" \
    "battleAgent_model" "provider/model-id" \
    "finalReviewer_model" "provider/model-id" \
    "readerSimulator_model" "provider/model-id" \
    "styleAnchorGenerator_model" "provider/model-id" \
    "rollingSummarizer_model" "provider/model-id" \
    "key_chapters" "（Phase 1 完成后填充）" \
    "act_boundaries" "（Phase 1 完成后填充）" \
    "total_chapters" "待补充"

replace_tokens_in_file "$REGISTRY_FILE" \
    "project_id" "$PROJECT_NAME" \
    "project_title" "$PROJECT_NAME" \
    "created_at" "$CURRENT_DATE" \
    "worldbuilder_model" "provider/model-id" \
    "characterDesigner_model" "provider/model-id" \
    "outlinePlanner_model" "provider/model-id" \
    "chapterOutliner_model" "provider/model-id" \
    "mainWriter_model" "provider/model-id" \
    "oocGuardian_model" "provider/model-id" \
    "battleAgent_model" "provider/model-id" \
    "finalReviewer_model" "provider/model-id" \
    "readerSimulator_model" "provider/model-id" \
    "styleAnchorGenerator_model" "provider/model-id" \
    "rollingSummarizer_model" "provider/model-id"

for file in "$ARCHIVE_FILE" "$STATE_FILE" "$RELATIONSHIP_FILE" "$PLOT_FILE" "$ROLLING_FILE" "$STYLE_FILE" "$SELECTED_STYLE_FILE" "$WORLD_FILE" "$OUTLINE_FILE" "$CHAPTER_OUTLINE_FILE"; do
    replace_tokens_in_file "$file" \
        "project_title" "$PROJECT_NAME" \
        "updated_at" "$CURRENT_DATE"
done

replace_tokens_in_file "$ARCHIVE_FILE" \
    "created_at" "$CURRENT_DATE"

replace_tokens_in_file "$STYLE_FILE" \
    "narrative_pov" "第三人称限知" \
    "style_keywords" "待补充" \
    "dialogue_style" "待补充" \
    "sense_1" "视觉" \
    "sense_2" "听觉" \
    "sense_3" "触觉" \
    "sense_4" "嗅觉"

replace_tokens_in_file "$SELECTED_STYLE_FILE" \
    "style_name" "待选定" \
    "selection_index" "（1-5）" \
    "style_traits" "（待选定）" \
    "selected_sample_content" "（待选定的 400 字样本正文）" \
    "selection_notes" "（用户的额外偏好或混合需求，如有）"

replace_tokens_in_file "$ROLLING_FILE" \
    "coverage_range" "ChX - ChY"

replace_tokens_in_file "$WORLD_FILE" \
    "world_name" "待补充" \
    "era_background" "待补充" \
    "geography_summary" "待补充"

replace_tokens_in_file "$OUTLINE_FILE" \
    "genre" "待补充" \
    "planned_chapters" "待补充" \
    "target_words" "待补充" \
    "tone" "待补充"

replace_tokens_in_file "$CHAPTER_OUTLINE_FILE" \
    "coverage_range" "第X章 - 第X章" \
    "word_count" "4000"

echo ""
echo -e "${GREEN}✅ 项目 '$PROJECT_NAME' 创建成功！${NC}"
echo ""
echo -e "${YELLOW}已创建关键目录:${NC}"
echo "  - meta/"
echo "  - worldbuilding/"
echo "  - characters/"
echo "  - outline/"
echo "  - chapters/"
echo "  - archive/"
echo "  - references/"
echo ""
echo -e "${YELLOW}下一步:${NC}"
echo "  1. 编辑 meta/project.md 填写项目基本信息"
echo "  2. 编辑 meta/config.md 配置 11 个子 Agent 的模型分工"
echo "  3. 开始 Phase 1: 世界观构建"
echo ""
echo -e "${BLUE}项目路径: $PROJECT_DIR${NC}"

exit 0
