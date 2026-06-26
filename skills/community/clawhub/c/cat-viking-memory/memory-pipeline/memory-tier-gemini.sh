#!/bin/bash
#
# memory-tier-gemini.sh
# 使用 Gemini CLI 执行记忆层级降级
# 包含遗忘算法和重要记忆保护
#

set -e

AGENTS="maojingli maoxiami maogongtou maozhuli global"
LOG_FILE="/tmp/memory-tier-gemini-$(date +%Y%m%d).log"

echo "=== 记忆层级降级 (Gemini) ===" | tee -a "$LOG_FILE"
echo "时间: $(date)" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

# 构建传递给 Gemini 的任务描述
GEMINI_TASK='执行记忆层级降级，按以下步骤：

## 1. 扫描记忆
扫描 ~/.openclaw/viking-{agent}/agent/memories/hot/ 目录下的 .md 文件
检查 frontmatter 中的 current_layer 和 created 时间

## 2. 遗忘算法（基于 viking-memory-system）
根据时间自动降级：
- L0 (0-1天) → L1 (2-7天): 生成核心轮廓
- L1 (2-7天) → L2 (8-30天): 提取关键词
- L2 (8-30天) → L3 (30-90天): 提取标签
- L3 (30-90天) → L4 (90天+): 归档

## 3. 重要记忆保护
如果 frontmatter 中 important: true 或 importance: high，
则跳过降级，保留完整记忆

## 4. 使用 LLM 压缩
调用本地 LLM (glm-4-flash) 生成压缩内容：
- L0→L1: 总结为 100 字轮廓
- L1→L2: 提取 5 个关键词
- L2→L3: 提取 3 个标签
- L3→L4: 仅保留标题

## 5. 更新文件
- 更新 frontmatter: current_layer, level, weight
- 在文件末尾添加压缩后的内容层级

## 处理以下 Agent:
1. maojingli
2. maoxiami
3. maogongtou  
4. maozhuli
5. global (全局记忆: ~/.openclaw/viking-global/)

## 输出格式
对每个 Agent 报告：
- 处理文件数
- 降级文件数
- 跳过的重要记忆数
- 任何错误

开始执行！'

# 调用 OpenClaw Agent (Step3.5Flash)
OPENCLAW_BIN="${OPENCLAW_BIN:-/home/xlous/.npm-global/bin/openclaw}"
echo "调用 OpenClaw Agent (Step3.5Flash)..." | tee -a "$LOG_FILE"
# 使用本地 Agent 执行记忆降级任务
"$OPENCLAW_BIN" agent --local --agent maoxiami --message "$GEMINI_TASK" 2>&1 | tee -a "$LOG_FILE"

echo "" | tee -a "$LOG_FILE"
echo "=== 降级完成 ===" | tee -a "$LOG_FILE"
