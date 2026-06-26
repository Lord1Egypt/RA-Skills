---
name: ai-cost-optimizer-cn
description: AI 模型成本优化器 - 自动计算 API 费用，推荐最优模型，对比 DeepSeek/智谱/通义/GPT 成本。省钱必备工具。
version: 1.0.0
author: OpenClaw CN
tags:
  - ai
  - cost
  - optimization
  - deepseek
  - pricing
  - calculator
---

# AI 成本优化器

智能对比 AI 模型 API 成本，推荐最优模型，帮你省 90%+ API 费用。

## 功能

- 💰 **成本计算** - 实时计算不同模型的 API 费用
- 📊 **价格对比** - 一键对比 10+ 主流模型
- 🎯 **智能推荐** - 根据场景推荐最优模型
- 📈 **费用预估** - 预估使用 10 万 tokens 花多少钱
- 💡 **省钱建议** - 告诉你如何优化成本

## 安装

```bash
npx clawhub@latest install ai-cost-optimizer
```

## 使用方法

### 1. 对比模型价格

```bash
node ~/.openclaw/skills/ai-cost-optimizer/compare.js
```

输出示例：
```
📊 AI 模型价格对比
┌─────────────┬──────────┬──────────┬─────────────┐
│ 模型        │ 输入     │ 输出     │ 每10万tokens │
├─────────────┼──────────┼──────────┼─────────────┤
│ DeepSeek V3 │ ¥0.27/M  │ ¥1.08/M  │ ¥1.35      │
│ 智谱 GLM-4  │ ¥0.10/M  │ ¥0.10/M  │ ¥0.50      │
│ 通义千问    │ ¥0.30/M  │ ¥0.60/M  │ ¥1.80      │
│ GPT-4o      │ ¥35/M    │ ¥105/M   │ ¥140       │
│ Claude 3.5  │ ¥17.50/M │ ¥52.50/M │ ¥70        │
└─────────────┴──────────┴──────────┴─────────────┘

💡 推荐选择：
   日常使用 → DeepSeek V3（省 99% 费用）
   中文内容 → 智谱 GLM-4（省 99.5% 费用）
   复杂推理 → Claude 3.5（省 50% 费用）
```

### 2. 计算使用费用

```bash
# 计算特定模型的费用
node ~/.openclaw/skills/ai-cost-optimizer/calculate.js deepseek 500000

# 输出：使用 50 万 tokens 花费 ¥6.75

# 交互式计算
node ~/.openclaw/skills/ai-cost-optimizer/calculate.js
```

### 3. 智能推荐

```bash
node ~/.openclaw/skills/ai-cost-optimizer/recommend.js
```

会询问你的使用场景，然后推荐最优模型：
```
❓ 主要用途？
  1. 日常对话/写作
  2. 编程/代码生成
  3. 中文内容创作
  4. 复杂推理/分析
  5. 多模态（图文）

❓ 每天大约调用次数？
  1. < 100 次
  2. 100-1000 次
  3. 1000-10000 次
  4. > 10000 次

💡 推荐：DeepSeek V3
   - 性价比最高
   - 预估每月费用：¥27（1000次/天）
   - 同等使用 GPT-4o：¥2800（省 99%）
```

### 4. 生成成本报告

```bash
node ~/.openclaw/skills/ai-cost-optimizer/report.js --model deepseek --tokens 1000000
```

生成详细成本分析报告：
- 各模型费用对比
- 省钱潜力分析
- 使用建议

## 支持的模型

| 模型 | 输入价格 | 输出价格 | 推荐场景 |
|------|----------|----------|----------|
| DeepSeek V3 | ¥0.27/M | ¥1.08/M | 日常对话、编程、写作 |
| DeepSeek Coder | ¥0.27/M | ¥1.08/M | 代码生成、代码审查 |
| 智谱 GLM-4 | ¥0.10/M | ¥0.10/M | 中文内容创作 |
| 智谱 GLM-3-Turbo | ¥0.05/M | ¥0.05/M | 高频调用 |
| 通义千问 Plus | ¥0.30/M | ¥0.60/M | 多模态任务 |
| 通义千问 Turbo | ¥0.10/M | ¥0.10/M | 快速响应 |
| GPT-4o | ¥35/M | ¥105/M | 复杂推理（企业级） |
| GPT-4o-mini | ¥3.50/M | ¥10.50/M | 中等任务 |
| Claude 3.5 Sonnet | ¥17.50/M | ¥52.50/M | 长文本、代码 |
| Claude 3.5 Haiku | ¥0.18/M | ¥0.54/M | 快速对话 |

## 省钱案例

### 案例 1：个人开发者
- **使用场景**：每天 AI 写代码 + 写博客
- **原方案**：GPT-4o，每月 100 万 tokens → ¥1400
- **优化后**：DeepSeek V3，每月 100 万 tokens → ¥13.5
- **节省**：**¥1386.5/月（99%）**

### 案例 2：初创公司
- **使用场景**：客服 Bot，每月 5000 万 tokens
- **原方案**：GPT-4o-mini → ¥17500/月
- **优化后**：DeepSeek V3 → ¥675/月
- **节省**：**¥16825/月（96%）**

### 案例 3：中文内容团队
- **使用场景**：写文章、营销文案，每月 3000 万 tokens
- **原方案**：GPT-4o → ¥42000/月
- **优化后**：智谱 GLM-4 + DeepSeek 组合 → ¥450/月
- **节省**：**¥41550/月（99%）**

## 混合策略（最优解）

根据不同任务使用不同模型：

| 任务类型 | 推荐模型 | 原因 |
|----------|----------|------|
| 简单对话 | DeepSeek V3 | 便宜 |
| 代码生成 | DeepSeek Coder | 代码能力强 |
| 中文写作 | 智谱 GLM-4 | 中文能力强 |
| 复杂推理 | Claude 3.5 | 推理强 |
| 多模态 | 通义千问 Plus | 图文处理 |

**预期节省**：50-99%（根据任务分布）

## 价格数据来源

- DeepSeek: https://platform.deepseek.com
- 智谱 AI: https://open.bigmodel.cn
- 通义千问: https://dashscope.aliyun.com
- OpenAI: https://openai.com/pricing
- Anthropic: https://www.anthropic.com/pricing

**注意**：价格可能变动，以官方为准。

## 常见问题

### Q: DeepSeek 和 GPT-4 差多少？
A: 日常任务（写作、编程、问答）几乎没差。复杂推理（数学证明、多步逻辑）GPT-4 略好，但贵 100 倍。

### Q: 可以混用多个模型吗？
A: 可以！推荐策略：
- 80% 用 DeepSeek/智谱（便宜）
- 20% 用 GPT/Claude（复杂任务）
- 预期节省 70-80%

### Q: 如何切换模型？
A: 编辑 `~/.openclaw/config.json`：
```json
{
  "model": {
    "provider": "deepseek",
    "model": "deepseek-chat"
  }
}
```

### Q: 这些价格准确吗？
A: 官方价格，2026-03 更新。价格可能变动，请以官方为准。

## 配置 OpenClaw 使用不同模型

### 方式 1：配置文件
编辑 `~/.openclaw/config.json`：
```json
{
  "model": {
    "provider": "deepseek",
    "model": "deepseek-chat"
  }
}
```

### 方式 2：环境变量
```bash
export DEFAULT_MODEL_PROVIDER=deepseek
export DEFAULT_MODEL_ID=deepseek-chat
```

### 方式 3：使用 openclaw-cn-installer
```bash
npx clawhub@latest install openclaw-cn-installer
node ~/.openclaw/skills/openclaw-cn-installer/setup-ai.js deepseek
```

## 相关资源

- [OpenClaw 中文安装助手](https://clawhub.ai/skill/openclaw-cn-installer)
- [DeepSeek 官网](https://deepseek.com)
- [智谱 AI 官网](https://bigmodel.cn)
- [OpenClaw 文档](https://docs.openclaw.ai)

---

## 💬 Pro 版本（¥199）

### 免费版（当前）
- 模型价格对比
- 基础费用计算
- 场景推荐

### Pro 版（¥199）
- ✅ 批量分析（100+ 模型）
- ✅ 历史趋势图表
- ✅ 自动化成本报告
- ✅ API 集成（自动统计）
- ✅ 团队协作功能
- ✅ 1年更新支持

### 联系方式
- **QQ**: 1002378395（中国用户）
- **Telegram**: `待注册`（海外用户）

> 添加 QQ 1002378395，发送"AI成本优化"获取 Pro 版信息

---

## License

MIT（免费版）
Pro 版：付费后可用
