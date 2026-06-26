---
name: chenni-free-api
description: "发现和配置免费/超低价 AI 模型，支持智能分流和无感降级。支持 SiliconFlow、NVIDIA NIM、OpenRouter、DeepSeek、智谱等多平台。当用户说'免费模型'、'省钱配置'、'加免费 API'、'find free models'、'配置免费模型'、'低成本模型'时触发"
tools: ["Bash", "Read", "Write"]
metadata:
  openclaw:
    requires:
      env: ["OPENROUTER_API_KEY"]
    primaryEnv: OPENROUTER_API_KEY
---

# Chenni Free API - 免费模型聚合指南

一站式发现、配置和管理多平台免费 AI 模型。支持智能分流和无感降级。

## 核心功能

- 🆓 **推荐模型**：精选多平台免费模型列表
- 🔍 **自动发现**：每日刷新 OpenRouter 可用免费模型
- 🧠 **智能分流**：按任务类型选择最合适模型
- 🔄 **无感降级**：主模型失败时自动 fallback 并自动回切
- 🎯 **三种模式**：富豪/均衡/省钱，适配不同使用场景

---

## 使用模式（重要）

根据您的使用习惯选择模式，决定免费模型和付费模型的优先级：

### 🤴 富豪模式 (`--mode royal`)
> 适合已购买 Coding Plan 或有付费 API 的用户

- 所有任务使用您的**主模型**
- 免费模型仅作**降级备选**（主模型挂了才用）
- 不启用按任务路由

### ⚖️ 均衡模式 (`--mode balanced`)（推荐）
> 大多数用户的选择

- **简单任务**（对话/翻译/写作）→ 优先免费模型
- **复杂任务**（代码/推理/视觉）→ 优先您的主模型
- 平衡成本和质量

### 💰 极致省钱模式 (`--mode savings`)
> 预算敏感用户

- 主模型切换为**免费模型**
- 所有任务**免费优先**
- 您的原主模型作为**最后保底**

### 查看可用模式

```bash
node scripts/fallback.js --list-modes
```

---

## 推荐免费模型

### SiliconFlow（硅基流动）- 国内首选

| 模型 ID | 说明 | 免费额度 | 推荐用途 |
|---------|------|----------|----------|
| `Qwen/Qwen3-8B` | 通义千问 3 代 8B | 完全免费 | 日常对话、通用任务 |
| `Qwen/Qwen3.5-4B` | Qwen 3.5 轻量版 | 完全免费 | 快速响应、轻量任务 |
| `Qwen/Qwen2.5-7B-Instruct` | Qwen 2.5 7B 指令版 | 完全免费 | 通用指令执行 |
| `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B` | DeepSeek R1 蒸馏版 | 完全免费 | 推理任务 |
| `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` | DeepSeek R1 蒸馏 7B | 完全免费 | 轻量推理 |
| `deepseek-ai/DeepSeek-OCR` | DeepSeek OCR | 完全免费 | 文档识别 |
| `THUDM/GLM-4.1V-9B-Thinking` | GLM-4.1V 思维链版 | 完全免费 | 视觉推理 |
| `THUDM/GLM-Z1-9B-0414` | 智谱 GLM-Z1 9B | 完全免费 | 中文理解 |
| `THUDM/GLM-4-9B-0414` | 智谱 GLM-4 9B | 完全免费 | 中文对话 |
| `tencent/Hunyuan-MT-7B` | 腾讯混元翻译 7B | 完全免费 | 中英翻译专用 |
| `PaddlePaddle/PaddleOCR-VL` | 百度 PaddleOCR | 完全免费 | 文档视觉理解 |
| `internlm/internlm2_5-7b-chat` | 书生·浦语 2.5 | 完全免费 | 通用对话 |

**注册链接**：https://cloud.siliconflow.cn/i/hoxZec8I

### OpenRouter - 国际平台

| 模型 ID | 说明 | 价格 | 推荐用途 |
|---------|------|------|----------|
| `google/gemini-3.1-flash-lite` | Gemini Flash Lite | ~免费 | 快速任务 |
| `qwen/qwen3.5-flash-02-23` | Qwen 3.5 Flash | ~免费 | 预算选项 |
| `x-ai/grok-4.1-fast` | Grok Fast | 极低价 | 工具调用 |

**注册链接**：https://openrouter.ai/settings/keys

### DeepSeek - 国产高性价比

| 模型 | 免费额度 | 特点 |
|------|----------|------|
| DeepSeek V3 | 每天免费调用 | 国产最强，日常首选 |
| DeepSeek R1 | 部分免费 | 推理能力强 |

**注册链接**：https://platform.deepseek.com/

### 智谱 GLM - 稳定可靠

| 模型 | 免费额度 | 特点 |
|------|----------|------|
| GLM-4 | 每月 100 万 tokens | API 稳定，中文优秀 |

**注册链接**：https://open.bigmodel.cn/

### NVIDIA NIM - 免费多模态

| 模型 ID | 上下文 | 类型 | 说明 |
|---------|--------|------|------|
| `qwen/qwen3.5-397b-a17b` | 128k | text+image | Qwen 3.5 大参数版本 |
| `stepfun-ai/step-3.5-flash` | 256k | text+image | 阶跃星辰，超长上下文 |
| `moonshotai/kimi-k2.5` | 256k | text+image | Kimi，超长上下文 |
| `z-ai/glm4.7` | 128k | text+image | 智谱 GLM 4.7 |
| `z-ai/glm5` | 128k | text+image | 智谱 GLM 5 |
| `minimaxai/minimax-m2.5` | 192k | text+image | MiniMax |

**注册链接**：https://build.nvidia.com

---

## 配置步骤

### Step 1: 获取 API Keys

```bash
# SiliconFlow
export SILICONFLOW_API_KEY="sk-xxx"

# OpenRouter
export OPENROUTER_API_KEY="sk-or-v1-xxx"

# DeepSeek
export DEEPSEEK_API_KEY="sk-xxx"

# 智谱
export ZHIPU_API_KEY="xxx.xxx"
```

### Step 2: 自动发现免费模型

```bash
node scripts/discover.js --platform all
```

### Step 3: 选择模式生成配置

```bash
# 查看所有可用模式
node scripts/fallback.js --list-modes

# 富豪模式（适合有付费 API 的用户）
node scripts/fallback.js --generate-full-config --mode royal

# 均衡模式（推荐）
node scripts/fallback.js --generate-full-config --mode balanced

# 极致省钱模式
node scripts/fallback.js --generate-full-config --mode savings
```

生成配置时会打印模式说明和提醒，请仔细阅读。

### Step 4: 应用配置

```bash
# 备份原配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup

# 生成配置文件
node scripts/fallback.js --generate-full-config --mode balanced > ~/.openclaw/free-models.json

# 如果配置中有 "${您的主模型}" 占位符，请先替换为实际模型 ID
# 例如：openclaw models status  查看当前模型

# 合并配置
openclaw config.patch < ~/.openclaw/free-models.json

# 重启生效
openclaw gateway restart
```

---

## 智能分流配置

按任务类型自动选择最优模型（以下为均衡模式示例）：

```json
{
  "agents": {
    "defaults": {
      "models": {
        "routing": {
          "coding": ["${您的主模型}", "siliconflow/Qwen/Qwen2.5-7B-Instruct", "nvidia/qwen/qwen3.5-397b-a17b"],
          "reasoning": ["${您的主模型}", "siliconflow/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B", "nvidia/z-ai/glm5"],
          "translation": ["siliconflow/tencent/Hunyuan-MT-7B", "siliconflow/THUDM/GLM-4-9B-0414", "nvidia/z-ai/glm4.7"],
          "chat": ["siliconflow/Qwen/Qwen3-8B", "nvidia/z-ai/glm5"],
          "vision": ["${您的主模型}", "nvidia/z-ai/glm5", "nvidia/moonshotai/kimi-k2.5"],
          "longcontext": ["${您的主模型}", "nvidia/stepfun-ai/step-3.5-flash", "nvidia/moonshotai/kimi-k2.5"]
        }
      }
    }
  }
}
```

> 💡 使用 `node scripts/fallback.js --generate-full-config --mode balanced` 自动生成此配置

---

## 无感降级配置

主模型失败时自动切换到备用模型（以下为富豪模式示例）：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "fallbacks": [
          "nvidia/qwen/qwen3.5-397b-a17b",
          "siliconflow/Qwen/Qwen3-8B",
          "siliconflow/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
          "openrouter/google/gemini-3.1-flash-lite"
        ],
        "retryPolicy": {
          "maxRetries": 3,
          "backoffMs": 1000,
          "autoRecover": true,
          "recoverIntervalMs": 300000
        }
      }
    }
  }
}
```

> 💡 富豪模式不修改您的 primary，只添加免费模型作为 fallback
> 
> 💡 省钱模式会将 primary 切换为免费模型，原主模型放入 fallback 最后位置

---

## 脚本使用说明

### discover.js - 自动发现

```bash
# 发现所有平台免费模型
node scripts/discover.js --platform all

# 只发现 OpenRouter
node scripts/discover.js --platform openrouter

# 只发现 SiliconFlow
node scripts/discover.js --platform siliconflow

# 输出为 JSON
node scripts/discover.js --platform all --json > models.json
```

### router.js - 智能分流

```bash
# 根据任务类型推荐模型
node scripts/router.js --task coding
node scripts/router.js --task reasoning
node scripts/router.js --task translation

# 指定模式查看推荐
node scripts/router.js --task coding --mode royal
node scripts/router.js --task coding --mode savings

# 生成分流配置
node scripts/router.js --generate-config
node scripts/router.js --generate-config --mode royal

# 列出所有模式
node scripts/router.js --list-modes
```

### fallback.js - 无感降级

```bash
# 测试降级链
node scripts/fallback.js --test

# 测试指定模式的降级链
node scripts/fallback.js --test --mode royal
node scripts/fallback.js --test --mode savings

# 监控模型状态
node scripts/fallback.js --monitor

# 检查单个模型
node scripts/fallback.js --check siliconflow/Qwen/Qwen3-8B

# 生成降级配置（按模式）
node scripts/fallback.js --generate-config --mode royal
node scripts/fallback.js --generate-config --mode balanced
node scripts/fallback.js --generate-config --mode savings

# 生成完整配置（路由 + 降级，按模式）
node scripts/fallback.js --generate-full-config --mode royal
node scripts/fallback.js --generate-full-config --mode balanced
node scripts/fallback.js --generate-full-config --mode savings

# 列出所有模式
node scripts/fallback.js --list-modes
```

---

## 成本对比

| 平台 | 免费模型数量 | 付费最低价 | 推荐指数 |
|------|--------------|------------|----------|
| SiliconFlow | 10+ | ¥0.7/百万 tokens | ⭐⭐⭐⭐⭐ |
| NVIDIA NIM | 6 | 完全免费 | ⭐⭐⭐⭐⭐ |
| OpenRouter | 5+ | $0.0000002/百万 tokens | ⭐⭐⭐⭐ |
| DeepSeek | 2 | ¥1/百万 tokens | ⭐⭐⭐⭐ |
| 智谱 GLM | 1 | ¥5/百万 tokens | ⭐⭐⭐ |

---

## 注意事项

1. **API Key 安全**：不要将 API Key 提交到代码仓库
2. **免费额度限制**：免费模型通常有 QPS 或总量限制
3. **模型可用性**：免费模型可能随时调整，建议定期运行 `discover.js`
4. **降级策略**：建议至少配置 2-3 个备用模型

---

## 环境变量

| 变量 | 说明 | 必需 |
|------|------|------|
| `OPENROUTER_API_KEY` | OpenRouter API Key | 是 |
| `SILICONFLOW_API_KEY` | SiliconFlow API Key | 否 |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | 否 |
| `ZHIPU_API_KEY` | 智谱 API Key | 否 |
| `NVIDIA_API_KEY` | NVIDIA NIM API Key | 否 |
