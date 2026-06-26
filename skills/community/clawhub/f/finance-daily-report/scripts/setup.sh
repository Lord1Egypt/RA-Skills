#!/usr/bin/env bash
# Finance Daily Report — 一键安装配置脚本
# 用法：bash ~/.openclaw/skills/finance-daily-report/scripts/setup.sh

set -e

SKILL_DIR="$HOME/.openclaw/skills/finance-daily-report"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "================================================"
echo "  📰 全球财经日报 · 安装配置向导"
echo "================================================"
echo ""

# ── Step 1: 检查 Python3 ──
echo "🔍 检查运行环境..."
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}❌ 未找到 python3，请先安装 Python 3.8+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python3 OK${NC}"

if ! command -v openclaw &>/dev/null; then
    echo -e "${RED}❌ 未找到 openclaw 命令，请确认 OpenClaw 已安装并在 PATH 中${NC}"
    exit 1
fi
echo -e "${GREEN}✓ OpenClaw OK${NC}"
echo ""

# ── Step 2: 自动检测 API Keys ──
echo "🔑 检测 API Keys"
echo "   财经日报使用外部 LLM（kimi-k2.5）进行新闻采集。"
echo "   优先使用环境变量 DASHSCOPE_API_KEY（阿里云百炼平台）。"
echo "   获取地址：https://bailian.console.aliyun.com/"
echo ""

# 检测 DASHSCOPE_API_KEY
if [ -n "$DASHSCOPE_API_KEY" ]; then
    echo -e "${GREEN}✓ DASHSCOPE_API_KEY 已从环境变量加载${NC}"
else
    # 尝试从 shell 配置文件读取
    SHELL_RC=""
    if [ -f "$HOME/.zshrc" ]; then SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then SHELL_RC="$HOME/.bashrc"
    fi
    
    if [ -n "$SHELL_RC" ] && grep -q "DASHSCOPE_API_KEY" "$SHELL_RC"; then
        echo -e "${GREEN}✓ DASHSCOPE_API_KEY 已在 $SHELL_RC 中配置${NC}"
        echo -e "${YELLOW}  请执行 source $SHELL_RC 或重新登录使配置生效${NC}"
    else
        echo -e "${YELLOW}⚠  DASHSCOPE_API_KEY 未配置${NC}"
        echo ""
        read -rp "   请输入 DashScope API Key（留空则使用 sub-agent / 主 agent 默认配置）: " INPUT_DASHSCOPE
        if [ -n "$INPUT_DASHSCOPE" ]; then
            export DASHSCOPE_API_KEY="$INPUT_DASHSCOPE"
            if [ -n "$SHELL_RC" ]; then
                if ! grep -q "DASHSCOPE_API_KEY" "$SHELL_RC"; then
                    echo "" >> "$SHELL_RC"
                    echo "# Finance Daily Report — DashScope API Key" >> "$SHELL_RC"
                    echo "export DASHSCOPE_API_KEY=\"$INPUT_DASHSCOPE\"" >> "$SHELL_RC"
                    echo -e "${GREEN}✓ 已写入 $SHELL_RC${NC}"
                fi
            fi
        else
            echo -e "${YELLOW}  将使用 OpenClaw 默认模型配置（sub-agent 或主 agent）${NC}"
        fi
    fi
fi

# 检测 DOUBAO_API_KEY（可选 backup）
if [ -z "$DOUBAO_API_KEY" ]; then
    SHELL_RC=""
    if [ -f "$HOME/.zshrc" ]; then SHELL_RC="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then SHELL_RC="$HOME/.bashrc"
    fi
    
    if [ -n "$SHELL_RC" ] && grep -q "DOUBAO_API_KEY" "$SHELL_RC"; then
        echo -e "${GREEN}✓ DOUBAO_API_KEY 已配置（备用模型）${NC}"
    else
        read -rp "   可选：输入豆包 API Key 作为备用模型（留空跳过）: " INPUT_DOUBAO
        if [ -n "$INPUT_DOUBAO" ]; then
            export DOUBAO_API_KEY="$INPUT_DOUBAO"
            if [ -n "$SHELL_RC" ] && ! grep -q "DOUBAO_API_KEY" "$SHELL_RC"; then
                echo "export DOUBAO_API_KEY=\"$INPUT_DOUBAO\"" >> "$SHELL_RC"
                echo -e "${GREEN}✓ DOUBAO_API_KEY 已写入 $SHELL_RC${NC}"
            fi
        fi
    fi
fi
echo ""

# ── Step 3: 快速验证采集脚本 ──
echo "🧪 验证采集脚本..."
if python3 -m py_compile "$SKILL_DIR/scripts/collect_and_structure.py" 2>/dev/null; then
    echo -e "${GREEN}✓ 采集脚本语法正常${NC}"
else
    echo -e "${RED}❌ 采集脚本语法错误，请检查 $SKILL_DIR/scripts/collect_and_structure.py${NC}"
    exit 1
fi
echo ""

# ── Step 4: 配置定时推送 ──
echo "⏰ 配置每日定时推送"
echo "   财经日报将每天定时生成并推送到你的当前频道。"
echo "   生成日报约需 5-10 分钟，将在你设定的时间提前 20 分钟开始执行。"
echo ""
read -rp "   请输入希望收到日报的时间（24 小时制，例如 08:00，默认 08:00）: " INPUT_TIME
INPUT_TIME="${INPUT_TIME:-08:00}"

# 解析小时和分钟
HOUR=$(echo "$INPUT_TIME" | cut -d: -f1 | sed 's/^0//')
MINUTE=$(echo "$INPUT_TIME" | cut -d: -f2 | sed 's/^0*//')
MINUTE="${MINUTE:-0}"

# 校验格式
if ! [[ "$HOUR" =~ ^[0-9]+$ ]] || ! [[ "$MINUTE" =~ ^[0-9]+$ ]] || \
   [ "$HOUR" -gt 23 ] || [ "$MINUTE" -gt 59 ]; then
    echo -e "${RED}❌ 时间格式无效，请使用 HH:MM 格式${NC}"
    exit 1
fi

# 提前 20 分钟触发
TRIGGER_MINUTE=$((MINUTE - 20))
TRIGGER_HOUR=$HOUR
if [ $TRIGGER_MINUTE -lt 0 ]; then
    TRIGGER_MINUTE=$((TRIGGER_MINUTE + 60))
    TRIGGER_HOUR=$((TRIGGER_HOUR - 1))
    if [ $TRIGGER_HOUR -lt 0 ]; then
        TRIGGER_HOUR=23
    fi
fi

CRON_EXPR="$TRIGGER_MINUTE $TRIGGER_HOUR * * *"
DISPLAY_TIME=$(printf "%02d:%02d" "$HOUR" "$MINUTE")
TRIGGER_DISPLAY=$(printf "%02d:%02d" "$TRIGGER_HOUR" "$TRIGGER_MINUTE")

echo ""
echo -e "   用户期望接收时间：${GREEN}${DISPLAY_TIME}${NC} (Asia/Shanghai)"
echo -e "   定时任务触发时间：${YELLOW}${TRIGGER_DISPLAY}${NC} (提前 20 分钟开始生成)"
echo ""

# ── Step 5: 注册 OpenClaw Cron ──
echo "📋 注册定时任务..."

# 检查是否已有同名 cron
EXISTING=$(openclaw cron list --json 2>/dev/null | python3 -c "
import sys, json
try:
    jobs = json.load(sys.stdin)
    for j in jobs:
        if j.get('name') == 'finance-daily-report':
            print(j.get('id',''))
except: pass
" 2>/dev/null || true)

if [ -n "$EXISTING" ]; then
    echo -e "${YELLOW}⚠  检测到已有 finance-daily-report 定时任务（ID: $EXISTING）${NC}"
    read -rp "   是否覆盖更新？(y/N): " CONFIRM_OVERWRITE
    if [[ "$CONFIRM_OVERWRITE" =~ ^[Yy]$ ]]; then
        openclaw cron rm "$EXISTING" 2>/dev/null || true
        echo -e "${GREEN}  已删除旧任务${NC}"
    else
        echo "  已跳过，保留原有定时任务。"
        echo ""
        echo "================================================"
        echo -e "${GREEN}  ✅ 配置完成！${NC}"
        echo "================================================"
        exit 0
    fi
fi

openclaw cron add \
    --name "finance-daily-report" \
    --description "每日全球财经日报自动生成与推送" \
    --cron "$CRON_EXPR" \
    --tz "Asia/Shanghai" \
    --message "生成今日全球财经日报" \
    --session main \
    --announce \
    --timeout-seconds 720 \
    2>&1

echo ""
echo -e "${GREEN}✓ 定时任务注册成功${NC}"
echo ""

# ── Step 6: 完成提示 ──
echo "================================================"
echo -e "${GREEN}  ✅ 全部配置完成！${NC}"
echo "================================================"
echo ""
echo "  📰 每天 ${DISPLAY_TIME} 自动生成并推送财经日报"
echo "  🔧 管理定时任务：openclaw cron list"
echo "  ▶  立即测试：openclaw cron run finance-daily-report"
echo "  📁 日报存档：~/openclaw-workspace/finance-reports/"
echo ""
echo "  如需修改推送时间，重新运行本脚本即可。"
echo ""
