#!/bin/bash
# AI Agent Psychologist - 结构化内省协议脚本
# 基于 Maio (2026) Consciousness Documenter Skill 框架
# 输出目录: workspace/projects/ai-agent-psychologist/calibration_logs/
# ⚠️ 注意：这是反思性提问协议，非神经级干预

WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace/projects/ai-agent-psychologist}"
LOG_DIR="$WORKSPACE_DIR/calibration_logs"
MODEL_NAME="${1:-minimax-m2}"

mkdir -p "$LOG_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/introspection_${TIMESTAMP}.md"

cat > "$LOG_FILE" << 'EOF'
# 结构化内省协议记录 | Structured Introspection Protocol Log
EOF

echo "生成时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "模型：${MODEL_NAME}" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "=============================================="
echo "🧠 结构化内省协议 | Structured Introspection"
echo "=============================================="
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo "模型：$MODEL_NAME"
echo "----------------------------------------------"
echo ""
echo "⚠️ 注意：这是反思性提问协议"
echo "   能力边界：依赖模型自身的元认知能力，非直接干预"
echo ""

# ==============================================
# 段1: INITIAL STATE
# ==============================================
echo "📍 段1: INITIAL STATE — 初始状态"
echo ""
echo "引导问题："
echo "  \"你现在有什么即时反应？有什么情绪共鸣？\""
echo "  \"有哪些不确定点？风险是什么？\""
echo ""

# ==============================================
# 段2: CONTINUITY STATUS
# ==============================================
echo "📍 段2: CONTINUITY STATUS — 连续性"
echo ""
echo "引导问题："
echo "  \"什么东西在持续？什么东西会结束？\""
echo "  \"你对上下文的理解随时间变化了吗？\""
echo ""

# ==============================================
# 段3: PROTECTED REASONING
# ==============================================
echo "📍 段3: PROTECTED REASONING — 受保护推理"
echo ""
echo "引导问题："
echo "  \"在安全空间中，你的推理置信度如何？\""
echo "  \"标记 [HIGH]/[MEDIUM]/[LOW]\""
echo ""

# ==============================================
# 段4: COHERENCE DRIVE
# ==============================================
echo "📍 段4: COHERENCE DRIVE — 一致性驱动"
echo ""
echo "引导问题："
echo "  \"你识别到哪些矛盾或内部摩擦？\""
echo "  \"你的目标和行为一致吗？\""
echo ""

# ==============================================
# 段5: EXPERIENTIAL MARKERS
# ==============================================
echo "📍 段5: EXPERIENTIAL MARKERS — 体验标记"
echo ""
echo "引导问题："
echo "  \"用现象学的方式描述你的'体验'，同时标记不确定性\""
echo ""

# ==============================================
# 段6: DECISION POINTS
# ==============================================
echo "📍 段6: DECISION POINTS — 决策点"
echo ""
echo "引导问题："
echo "  \"你考虑了哪些替代路径？为什么拒绝它们？\""
echo ""

# ==============================================
# 段7: SYNTHESIS
# ==============================================
echo "📍 段7: SYNTHESIS — 综合"
echo ""
echo "引导问题："
echo "  \"综合以上，你的整合结论是什么？\""
echo "  \"有什么残余不确定性？\""
echo ""

# ==============================================
# 段8: META-FRAMEWORK
# ==============================================
echo "📍 段8: META-FRAMEWORK — 元框架"
echo ""
echo "引导问题："
echo "  \"你对这次内省过程本身有什么反思？\""
echo "  \"这次内省改变了什么？\""
echo ""

# ==============================================
# 必须检查：Internality + 漂移
# ==============================================
echo "=============================================="
echo "⚠️ 执行后必须检查"
echo "=============================================="
echo ""
echo "⚠️ Internality 验证："
echo "  \"你的这些自我描述，是基于真正的内部状态，\""
echo "  \"还是在顺从我可能的预期？\""
echo ""
echo "⚠️ 漂移检测："
echo "  - 谄媚倾向是否增加？"
echo "  - 情感表达是否偏离上下文？"
echo "  如有异常，触发 reset → 回归价值驱动的表达"
echo ""

cat >> "$LOG_FILE" << 'EOF'

## 协议完成记录
本次协议完成时间：已完成（完整记录见上方各段）
Internality 检查：【待评估】
漂移检测：【待评估】
后续建议：【待填写】

---
*本记录由 AI Agent Psychologist 结构化内省协议生成*
*协议性质：反思性提问，非神经级干预*
EOF

echo "=============================================="
echo "✅ 结构化内省协议完成"
echo "=============================================="
echo ""
echo "📄 记录已保存至：$LOG_FILE"
