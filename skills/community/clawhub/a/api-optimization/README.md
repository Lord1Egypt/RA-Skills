# Chenni Free API - OpenClaw 免费模型配置指南

一站式发现、配置和管理多平台免费 AI 模型。支持智能分流和无感降级。

## 核心功能

- 🆓 **推荐模型**：精选 SiliconFlow、NVIDIA NIM、OpenRouter、DeepSeek、智谱等多平台免费模型
- 🔍 **自动发现**：每日刷新 OpenRouter 可用免费模型
- 🧠 **智能分流**：按任务类型（代码、推理、翻译等）选择最合适模型
- 🔄 **无感降级**：主模型失败时自动 fallback 并自动回切
- 🎯 **三种模式**：富豪/均衡/省钱，适配不同使用场景

---

## 基础设置 - 增加模型和 API

### 1. BigModel（智谱）

```bash
# 注册：https://open.bigmodel.cn/
# 获取 API Key
```

| 项目 | 值 |
|------|------|
| Provider 名称 | `zhipu` |
| API 协议 | `openai-completions` |
| Base URL | `https://open.bigmodel.cn/api/paas/v4/` |
| 认证方式 | Bearer Token (API Key) |

**验证 API Key 和查看剩余额度**：
```bash
curl https://open.bigmodel.cn/api/paas/v4/balance -H "Authorization: Bearer $API_KEY"
```

**免费额度**：GLM-4 每月 100 万 tokens

### 2. 硅基流动 SiliconFlow

SiliconFlow（硅基流动）是国内领先的 AI 模型推理平台，提供 98+ 个 chat 模型，涵盖 Qwen、DeepSeek、Kimi、GLM、MiniMax 等主流系列。

如果还没有 SiliconFlow 账号，请通过邀请链接注册（双方均获赠额度）：
👉 **https://cloud.siliconflow.cn/i/hoxZec8I**

| 项目 | 值 |
|------|------|
| Provider 名称 | `siliconflow` |
| API 协议 | `openai-completions` |
| Base URL | `https://api.siliconflow.cn/v1` |
| 认证方式 | Bearer Token (API Key) |

**验证 API Key 和查看剩余额度**：
```bash
curl -s 'https://api.siliconflow.cn/v1/user/info' -H 'Authorization: Bearer <YOUR_API_KEY>'
```

### 3. OpenRouter

| 项目 | 值 |
|------|------|
| Provider 名称 | `openrouter` |
| API 协议 | `openai-completions` |
| Base URL | `https://openrouter.ai/api/v1` |
| 认证方式 | Bearer Token (API Key) |

**注册链接**：https://openrouter.ai/settings/keys

### 4. NVIDIA NIM

| 项目 | 值 |
|------|------|
| Provider 名称 | `nvidia` |
| API 协议 | `openai-completions` |
| Base URL | `https://integrate.api.nvidia.com/v1` |
| 认证方式 | Bearer Token (API Key) |

**注册链接**：https://build.nvidia.com

---

## 推荐模型

### SiliconFlow 免费模型（无限使用）

| 模型 ID | 说明 | 推荐别名 |
|---------|------|----------|
| `Qwen/Qwen3-8B` | 通义千问 3 代 8B，综合能力强 | `sf-qwen3-8b` |
| `Qwen/Qwen3.5-4B` | Qwen 3.5 轻量版，响应快 | `sf-qwen35-4b` |
| `Qwen/Qwen2.5-7B-Instruct` | Qwen 2.5 7B 指令版 | `sf-qwen25-7b` |
| `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B` | DeepSeek R1 推理蒸馏版 | `sf-r1-8b` |
| `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` | DeepSeek R1 蒸馏 7B | `sf-r1-distill-7b` |
| `deepseek-ai/DeepSeek-OCR` | DeepSeek OCR 文档识别 | `sf-ocr` |
| `THUDM/GLM-4.1V-9B-Thinking` | GLM-4.1V 思维链版，支持视觉 | `sf-glm41v` |
| `THUDM/GLM-Z1-9B-0414` | 智谱 GLM-Z1 9B | `sf-glm-z1` |
| `THUDM/GLM-4-9B-0414` | 智谱 GLM-4 9B | `sf-glm4` |
| `tencent/Hunyuan-MT-7B` | 腾讯混元翻译，中英翻译专用 | `sf-hunyuan-mt` |
| `PaddlePaddle/PaddleOCR-VL` | 百度 PaddleOCR 视觉理解 | `sf-paddleocr` |
| `internlm/internlm2_5-7b-chat` | 书生·浦语 2.5 | `sf-internlm` |

### SiliconFlow 性价比模型（便宜好用）

| 模型 ID | 输入/输出 (¥/M tokens) | 说明 | 推荐别名 |
|---------|----------------------|------|----------|
| `Qwen/Qwen3-30B-A3B` | 0.7 / 2.8 | MoE 架构，性价比极高 | `sf-qwen3-30b` |
| `Qwen/Qwen3-Coder-30B-A3B-Instruct` | 0.7 / 2.8 | 编码专用 30B | `sf-coder-30b` |
| `deepseek-ai/DeepSeek-V3.2` | 2.0 / 3.0 | DeepSeek 最新版 | `sf-dsv3` |
| `Pro/deepseek-ai/DeepSeek-V3.2` | 2.0 / 3.0 | Pro 加速版 | `sf-dsv3-pro` |

### SiliconFlow 旗舰模型（重要任务）

| 模型 ID | 输入/输出 (¥/M tokens) | 说明 | 推荐别名 |
|---------|----------------------|------|----------|
| `deepseek-ai/DeepSeek-R1` | 4.0 / 16.0 | 推理模型 | `sf-r1` |
| `Pro/moonshotai/Kimi-K2.5` | 4.0 / 21.0 | 月之暗面最强模型 | `sf-kimi` |
| `Qwen/Qwen3-Coder-480B-A35B-Instruct` | 8.0 / 16.0 | 编码旗舰 480B MoE | `sf-coder-480b` |

### OpenRouter 免费/低价模型

| 模型 ID | 说明 | 价格 |
|---------|------|------|
| `google/gemini-3.1-flash-lite` | Gemini Flash Lite | ~免费 |
| `qwen/qwen3.5-flash-02-23` | Qwen 3.5 Flash | ~免费 |
| `x-ai/grok-4.1-fast` | Grok Fast | 极低价 |

### NVIDIA NIM 免费模型（完全免费）

| 模型 ID | 上下文 | 类型 | 说明 |
|---------|--------|------|------|
| `qwen/qwen3.5-397b-a17b` | 128k | text+image | Qwen 3.5 大参数版本 |
| `stepfun-ai/step-3.5-flash` | 256k | text+image | 阶跃星辰，超长上下文 |
| `moonshotai/kimi-k2.5` | 256k | text+image | Kimi，超长上下文 |
| `z-ai/glm4.7` | 128k | text+image | 智谱 GLM 4.7 |
| `z-ai/glm5` | 128k | text+image | 智谱 GLM 5 |
| `minimaxai/minimax-m2.5` | 192k | text+image | MiniMax |

---

## 脚本使用说明

### discover.js - 自动发现免费模型

```bash
# 发现所有平台免费模型
node scripts/discover.js --platform all

# 只发现 OpenRouter
node scripts/discover.js --platform openrouter

# 只发现 SiliconFlow
node scripts/discover.js --platform siliconflow

# 只发现 NVIDIA NIM
node scripts/discover.js --platform nvidia

# 输出为 JSON
node scripts/discover.js --platform all --json > models.json
```

### router.js - 智能分流

```bash
# 根据任务类型推荐模型
node scripts/router.js --task coding
node scripts/router.js --task reasoning
node scripts/router.js --task translation

# 自动检测任务类型
node scripts/router.js --detect "帮我写一段代码"

# 生成分流配置
node scripts/router.js --generate-config

# 指定模式生成配置
node scripts/router.js --generate-config --mode royal
node scripts/router.js --generate-config --mode balanced
node scripts/router.js --generate-config --mode savings

# 列出所有模式
node scripts/router.js --list-modes
```

### fallback.js - 无感降级

```bash
# 测试降级链
node scripts/fallback.js --test
node scripts/fallback.js --test --chain all

# 按模式测试
node scripts/fallback.js --test --mode royal

# 监控模型状态
node scripts/fallback.js --monitor

# 检查单个模型
node scripts/fallback.js --check siliconflow/Qwen/Qwen3-8B

# 生成配置（按模式）
node scripts/fallback.js --generate-config --mode royal
node scripts/fallback.js --generate-config --mode balanced
node scripts/fallback.js --generate-config --mode savings

# 生成完整配置（路由 + 降级）
node scripts/fallback.js --generate-full-config --mode balanced > config.json

# 列出所有模式
node scripts/fallback.js --list-modes
```

---

## 智能分流配置

按任务类型自动选择最优模型：

```json
{
  "agents": {
    "defaults": {
      "models": {
        "routing": {
          "coding": ["siliconflow/Qwen/Qwen2.5-7B-Instruct", "nvidia/qwen/qwen3.5-397b-a17b"],
          "reasoning": ["siliconflow/deepseek-ai/DeepSeek-R1-0528-Qwen3-8B", "nvidia/z-ai/glm5"],
          "translation": ["siliconflow/tencent/Hunyuan-MT-7B", "siliconflow/THUDM/GLM-4-9B-0414"],
          "chat": ["siliconflow/Qwen/Qwen3-8B", "nvidia/z-ai/glm5"],
          "vision": ["nvidia/z-ai/glm5", "nvidia/moonshotai/kimi-k2.5"],
          "longcontext": ["nvidia/stepfun-ai/step-3.5-flash", "nvidia/moonshotai/kimi-k2.5"]
        }
      }
    }
  }
}
```

---

## 无感降级配置

主模型失败时自动切换到备用模型：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "siliconflow/Qwen/Qwen3-8B",
        "fallbacks": [
          "nvidia/qwen/qwen3.5-397b-a17b",
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

---

## 省钱策略

### 分层使用

| 任务类型 | 推荐模型 | 原因 |
|----------|----------|------|
| 日常对话 | Qwen3-8B (免费) | 完全免费，响应快 |
| 代码生成 | Qwen2.5-7B-Instruct (免费) | 指令执行好 |
| 推理任务 | DeepSeek-R1-Qwen3-8B (免费) | 推理能力强 |
| 翻译任务 | Hunyuan-MT-7B (免费) | 翻译专用 |
| 文档识别 | DeepSeek-OCR (免费) | OCR 专用 |
| 视觉推理 | GLM-4.1V-9B-Thinking (免费) | 支持思维链+视觉 |
| 长文本处理 | NVIDIA Step-3.5-Flash (免费) | 256k 超长上下文 |
| 图像理解 | NVIDIA GLM5 (免费) | 支持多模态 |
| 重要任务 | DeepSeek-V3.2 (付费) | 质量最高 |

### 成本对比

**场景：每天 100 条消息**

| 模型 | 月成本 |
|------|--------|
| 全用免费模型 | ¥0 |
| NVIDIA NIM 免费模型 | ¥0 |
| SiliconFlow 性价比模型 | ~¥30 |
| GPT-4o | ¥90 |
| Claude Sonnet | ¥180 |

---

## 环境变量

| 变量 | 说明 | 必需 |
|------|------|------|
| `OPENROUTER_API_KEY` | OpenRouter API Key | 是 |
| `SILICONFLOW_API_KEY` | SiliconFlow API Key | 否 |
| `NVIDIA_API_KEY` | NVIDIA NIM API Key | 否 |
| `DEEPSEEK_API_KEY` | DeepSeek API Key | 否 |
| `ZHIPU_API_KEY` | 智谱 API Key | 否 |

---

## 帮助链接

- **SiliconFlow 注册**：https://cloud.siliconflow.cn/i/hoxZec8I
- **SiliconFlow 文档**：https://docs.siliconflow.cn
- **SiliconFlow 定价**：https://siliconflow.cn/pricing
- **NVIDIA NIM**：https://build.nvidia.com
- **OpenRouter**：https://openrouter.ai
- **OpenClaw**：https://github.com/openclaw/openclaw
- **OpenClaw 文档**：https://docs.openclaw.ai
- **OpenClaw 模型文档**：https://docs.openclaw.ai/providers

---

## 注意事项

1. **免费模型有 QPS 限制**：免费模型的并发数可能受限，适合 fallback 和低频任务和日常对话
2. **模型 ID 区分大小写**：必须严格匹配，如 `Qwen/Qwen3-8B` 不能写成 `qwen/qwen3-8b`
3. **cost 字段单位**：¥/百万 tokens (1M tokens)
4. **API Key 安全**：不要将 API Key 提交到代码仓库

---

创建：2026-04-02
