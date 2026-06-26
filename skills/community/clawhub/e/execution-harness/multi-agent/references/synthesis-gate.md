# Synthesis Gate

## Problem

Coordinator 收到 worker 的 research 结果后，直接把原始结果传给下一个 worker——"Based on the findings above, implement the fix." 这违反了 Anthropic 的核心原则：coordinator 变成了传话筒，下游 worker 在没有综合理解的情况下工作，产出质量差且方向可能错误。

## Solution

在 Research 和 Implementation 阶段之间设置强制 synthesis gate。Coordinator 必须自己消化所有 research 结果，产出一份 synthesis 文档，才能启动下一阶段。Gate 的检查机制：synthesis 文档必须存在、长度达标、包含关键结构（结论、依据、行动计划）。

## Implementation

1. Research 阶段完成后，worker 将结果写入 `.coordination/research/`
2. Coordinator 执行 synthesis（这一步不可委派）
3. Gate 脚本检查 synthesis 质量

```bash
SYNTHESIS=".coordination/synthesis.md"

# 检查 1：文件存在且非空
if [ ! -s "$SYNTHESIS" ]; then
  echo "GATE FAILED: synthesis.md 不存在或为空"
  exit 1
fi

# 检查 2：最小长度（synthesis 不能是一句话）
LINES=$(wc -l < "$SYNTHESIS")
if [ "$LINES" -lt 10 ]; then
  echo "GATE FAILED: synthesis.md 只有 ${LINES} 行，不足以覆盖 research 结论"
  exit 1
fi

# 检查 3：必须包含关键结构
for SECTION in "结论\|Conclusion" "行动计划\|Action Plan\|Implementation Plan" "依据\|Evidence\|Rationale"; do
  if ! grep -qiE "$SECTION" "$SYNTHESIS"; then
    echo "GATE FAILED: synthesis.md 缺少必要节: ${SECTION}"
    exit 1
  fi
done

echo "GATE PASSED: synthesis ready for implementation phase"
```

4. Gate 通过后，将 synthesis.md 作为 implementation worker 的输入

```bash
claude -p --max-turns 50 \
  "根据以下 synthesis 执行实现。$(cat .coordination/synthesis.md)"
```

## Tradeoffs

- **Pro**: 强制 coordinator 理解而非传话，显著提升下游 worker 产出质量
- **Pro**: Synthesis 文档成为可审计的决策记录
- **Con**: 增加一个串行步骤，总耗时增加
- **Con**: 结构化检查是浅层验证——coordinator 可能写出满足格式但内容空洞的 synthesis

## Source

Anthropic "Building multi-agent systems" 博客的核心原则。本项目蒸馏实践中发现的 coordinator-as-passthrough 反模式。
