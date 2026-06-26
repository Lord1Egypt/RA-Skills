# Provider 信息表 (Provider Configuration Matrix)

> 以下为 Claude Code 兼容的第三方 API Provider 完整配置信息。
> 认证方式说明：`ANTHROPIC_AUTH_TOKEN` 用于 Bearer Token 认证（DeepSeek/Kimi 等），`ANTHROPIC_API_KEY` 用于 x-api-key 认证（OpenRouter 等）。

---

## 1. DeepSeek ⭐ 最推荐

| 字段 | 值 |
|---|---|
| **Base URL** | `https://api.deepseek.com/anthropic` |
| **认证方式** | `ANTHROPIC_AUTH_TOKEN` |
| **推荐主模型** | `deepseek-v4-pro[1m]` |
| **推荐轻量模型** | `deepseek-v4-flash` |
| **上下文** | 1M (需 `[1m]` 后缀) |
| **API Key 获取** | https://platform.deepseek.com/api_keys |
| **计费** | 按量计费（极低，flash 更便宜） |
| **特点** | 国内速度最快，V4 Pro 推理能力强，中文优秀 |

**环境变量模板**:
```bash
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_AUTH_TOKEN="sk-your-key"
export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
```

**注意**: `AUTH_TOKEN` 不是 `API_KEY`。如果用后者会 401。

---

## 2. Kimi (月之暗面)

| 字段 | 值 |
|---|---|
| **Base URL** | `https://api.moonshot.cn/anthropic` |
| **认证方式** | `ANTHROPIC_AUTH_TOKEN` |
| **推荐主模型** | `kimi-k2[1m]` |
| **推荐轻量模型** | `kimi-k2` |
| **上下文** | 1M (需 `[1m]` 后缀) |
| **API Key 获取** | https://platform.moonshot.cn |
| **计费** | 按量计费 |

**环境变量模板**:
```bash
export ANTHROPIC_BASE_URL="https://api.moonshot.cn/anthropic"
export ANTHROPIC_AUTH_TOKEN="sk-your-key"
export ANTHROPIC_MODEL="kimi-k2[1m]"
export ANTHROPIC_DEFAULT_OPUS_MODEL="kimi-k2[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL="kimi-k2[1m]"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="kimi-k2"
export CLAUDE_CODE_SUBAGENT_MODEL="kimi-k2"
```

---

## 3. Qwen (阿里通义千问)

| 字段 | 值 |
|---|---|
| **Base URL** | `https://dashscope.aliyuncs.com/compatible-mode/anthropic` (待验证) |
| **认证方式** | `ANTHROPIC_AUTH_TOKEN` |
| **推荐模型** | `qwen3-coder-plus` |
| **上下文** | 128K |
| **API Key 获取** | https://dashscope.console.aliyun.com/apiKey |

**环境变量模板**:
```bash
export ANTHROPIC_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/anthropic"
export ANTHROPIC_AUTH_TOKEN="sk-your-key"
export ANTHROPIC_MODEL="qwen3-coder-plus"
```

> ⚠️ Qwen 的 Anthropic 兼容端点地址可能有变化，建议使用前查阅最新文档。

---

## 4. SiliconFlow (硅基流动)

| 字段 | 值 |
|---|---|
| **Base URL** | `https://api.siliconflow.cn/anthropic` |
| **认证方式** | `ANTHROPIC_API_KEY` |
| **推荐模型** | `deepseek-ai/DeepSeek-V3` |
| **上下文** | 64K |
| **API Key 获取** | https://siliconflow.cn |
| **计费** | 部分模型免费额度 |

**环境变量模板**:
```bash
export ANTHROPIC_BASE_URL="https://api.siliconflow.cn/anthropic"
export ANTHROPIC_API_KEY="sk-your-key"
export ANTHROPIC_MODEL="deepseek-ai/DeepSeek-V3"
```

> ⚠️ SiliconFlow 的 Anthropic 端点可能有格式差异，建议实际测试。

---

## 5. OpenRouter

| 字段 | 值 |
|---|---|
| **Base URL** | `https://openrouter.ai/api/v1` |
| **认证方式** | `ANTHROPIC_API_KEY` |
| **推荐模型** | `deepseek/deepseek-chat` |
| **上下文** | 取决于所选模型 |
| **API Key 获取** | https://openrouter.ai/keys |
| **计费** | 按量计费（需海外信用卡或 USDT） |

**环境变量模板**:
```bash
export ANTHROPIC_BASE_URL="https://openrouter.ai/api/v1"
export ANTHROPIC_API_KEY="sk-or-v1-xxx"
export ANTHROPIC_MODEL="deepseek/deepseek-chat"
```

> ⚠️ OpenRouter 不是纯 Anthropic 兼容端点，某些 Claude Code 高级特性可能不可用。

---

## 6. 魔搭 ModelScope

| 字段 | 值 |
|---|---|
| **Base URL** | `https://api-inference.modelscope.cn/anthropic` (待验证) |
| **认证方式** | `ANTHROPIC_AUTH_TOKEN` |
| **推荐模型** | 待用户自行选择 |
| **上下文** | 取决于所选模型 |
| **API Key 获取** | https://modelscope.cn |

> ⚠️ ModelScope 的 Anthropic 兼容端点信息需要用户自行从官方网站确认。

---

## 7. 百川 Baichuan

| 字段 | 值 |
|---|---|
| **Base URL** | 待验证 |
| **认证方式** | `ANTHROPIC_AUTH_TOKEN` (待确认) |
| **API Key 获取** | https://platform.baichuan-ai.com |

---

## 8. 智谱 GLM

| 字段 | 值 |
|---|---|
| **Base URL** | `https://open.bigmodel.cn/api/paas/v4` |
| **认证方式** | `ANTHROPIC_AUTH_TOKEN` |
| **推荐模型** | `glm-5v` |
| **上下文** | 200K |
| **API Key 获取** | https://open.bigmodel.cn |

> ⚠️ 智谱的 Anthropic 兼容端点不完全保证 Claude Code 所有功能可用。建议使用前运行 `/status` 验证。

---

## 9. 字节豆包

| 字段 | 值 |
|---|---|
| **Base URL** | 待验证 |
| **认证方式** | 待确认 |
| **API Key 获取** | https://console.volcengine.com |

---

## 10. 自定义 Provider

用户自行提供：
- `ANTHROPIC_BASE_URL`
- 认证方式（`ANTHROPIC_AUTH_TOKEN` 或 `ANTHROPIC_API_KEY`）
- 模型名
- 上下文限制

Creator 按用户提供的信息生成配置。

---

## Provider 选择建议

| 场景 | 推荐 Provider |
|---|---|
| 国内 + 便宜 + 编程 | **DeepSeek** (deepseek-v4-pro + flash) |
| 超长上下文 | **Kimi** (kimi-k2 + 1M) |
| 想要多模型切换 | **OpenRouter** (但需要海外支付) |
| 免费试用 | **SiliconFlow** (有免费额度) |
| 企业级 | **Qwen** (阿里云生态) |
