#!/usr/bin/env bash
# Model Router - 配置多模型分级策略
# 用法: bash setup-models.sh

set -euo pipefail

G=$'\033[0;32m' Y=$'\033[1;33m' B=$'\033[1m' C=$'\033[0;36m' N=$'\033[0m'

CONFIG="$HOME/.openclaw/openclaw.json"

echo -e "${B}🎯 模型分级配置向导${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 读取当前配置
echo -e "\n${C}当前配置:${NC}"
if [[ -f "$CONFIG" ]]; then
    primary=$(grep -o '"primary"[[:space:]]*:[[:space:]]*"[^"]*"' "$CONFIG" | head -1 | sed 's/.*"primary"[[:space:]]*:[[:space:]]*"//' | sed 's/"//')
    fallbacks=$(grep -o '"fallbacks"[[:space:]]*:[[:space:]]*\[[^]]*\]' "$CONFIG" 2>/dev/null || echo "未设置")
    echo "  主模型: $primary"
    echo "  备用模型: $fallbacks"
else
    echo "  配置文件不存在"
    exit 1
fi

echo -e "\n${B}推荐分级策略:${NC}"
cat << 'EOF'

┌─────────────────────────────────────────────────┐
│  简单任务 (闲聊、翻译、格式化)                      │
│  → 便宜快速: qwen-turbo / deepseek-v3            │
│                                                   │
│  中等任务 (写作、分析、代码)                        │
│  → 性价比: gpt-4o-mini / claude-haiku             │
│                                                   │
│  复杂任务 (推理、架构、长文创作)                     │
│  → 能力强: gpt-4o / claude-opus / mimo-v2-pro     │
└─────────────────────────────────────────────────┘

实现方式:
1. 配置 fallback 链（自动降级）
2. 不同 agent 用不同主模型（按角色分）
3. 手动 /model 切换（临时调整）

EOF

echo -e "${B}你目前用的是: ${primary}${NC}"
echo ""
echo "下一步:"
echo "  1. 想加 fallback？告诉我你想加什么模型"
echo "  2. 想按角色分模型？告诉我法务/编辑/产品各用什么"
echo "  3. 只想省钱？加一个便宜的 fallback 就行"
