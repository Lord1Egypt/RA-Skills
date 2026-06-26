---
name: cli-proxy-troubleshooting
description: "排查 CLI Proxy API（codex-api-proxy）的配置、认证、模型注册和请求问题。适用场景包括：(1) AI 请求报错 unknown provider for model, (2) 模型列表中缺少预期模型, (3) codex-api-key/auth-dir 配置不生效, (4) CLI Proxy 启动后 AI 无法调用, (5) 认证成功但请求失败或超时。包含源码级排查方法：模型注册表架构、认证加载链路、 SanitizeCodexKeys 规则、常见错误的真实根因。"
metadata: {"openclaw":{"homepage":"https://github.com/stainless-codex/cli-proxy-api"}}
---

# CLI Proxy (Codex API Proxy) Troubleshooting Guide

排查基于 [CLI Proxy API](https://github.com/stainless-codex/cli-proxy-api) 的 Codex OAuth / OpenAI-compatible 代理问题。

## 使用方式

当遇到以下情况时，先按本文的“快速诊断流程”执行，再按需阅读 `references/source-architecture.md`：

- API 报 `unknown provider for model`
- 配置已写但模型列表不对
- 认证文件或 API key 看起来存在，但请求仍失败
- 代理启动正常，但上层客户端无法完成实际调用

## 架构概述

CLI Proxy 的核心架构：

```
config.yaml / auth-dir → reloadClients → snapshotCoreAuths
  → refreshAuthState → dispatchAuthUpdates → applyCoreAuthAddOrUpdate
    → registerModelsForAuth → 模型注册表（全局单例）
```

**请求处理链路：**
```
HTTP → ChatCompletions handler → getRequestDetails(modelName)
  → GetProviderName(baseModel) → GetModelProviders(modelName)
    → AuthManager.Execute(providers, req) → Codex executor → ChatGPT
```

- 模型注册表是全局单例（`sync.Once`），运行中可热加载
- 认证信息变更会触发模型重新注册
- 配置热重载有 debounce + SHA256 hash 对比

## 模型注册机制

### 认证 → 模型映射

不同认证类型注册不同的模型集：

| 认证类型 | 注册的模型 | 来源 |
|---|---|---|
| Codex Free（auth-dir 的 JSON 文件带 `-free`） | gpt-5.4, gpt-5.4-mini, gpt-5.3-codex, gpt-5.2 | `models.json` 中的 `CodexFreeModels` |
| Codex Pro（auth-dir 的 JSON 文件无 `-free`） | 同上 + gpt-5.3-codex-spark | `GetCodexProModels()` |
| codex-api-key（config.yaml 中配置） | Pro 模型集 | `synthesizeCodexKeys`→`GetCodexProModels()` |
| OpenAI API Key | gpt-4o, gpt-4o-mini | 标准 OpenAI 模型 |

### 模型列表来源

内嵌模型定义在 `internal/registry/models/models.json`，编译时打包进二进制。

## 常见问题与根因

### 1. "unknown provider for model" 报错

**错误消息的细节决定排查方向：**
- `"unknown provider for model gpt-5.4"` → 模型名被正确解析，但 provider（认证）未注册 → 检查认证文件和 API key
- `"unknown provider for model"`（没有模型名） → 请求体被破坏，模型字段缺失 → **检查请求编码**

**💡 核心发现：** 错误消息中的模型名是否出现，直接指向完全不同的根因。

### 2. PowerShell + curl 请求体编码问题

PowerShell 会对 `-d` 参数中的 JSON 做转义处理，导致：
- 引号被转义（`"` → `\"` 或丢失）
- 请求体结构被破坏
- model 字段可能丢失

**修复方法：**
```bash
# 用文件方式（推荐）
echo '{"model":"gpt-5.4","messages":[{"role":"user","content":"hi"}]}' > body.json
curl -X POST <proxy-base-url>/v1/chat/completions -d @body.json

# 或用 Python 发请求
python -c "
import requests
r = requests.post('<proxy-base-url>/v1/chat/completions',
    json={'model':'gpt-5.4','messages':[{'role':'user','content':'hi'}]})
print(r.text)
"
```

### 3. codex-api-key 不生效 (SanitizeCodexKeys)

CLI Proxy 启动时会调用 `SanitizeCodexKeys()` 清理配置中的 codex-api-key 条目。

**清理规则：** 移除**没有 `base-url`** 的条目。

```yaml
# ❌ 会被移除
codex_api_keys:
  my-key:
    key: "sk-xxx"

# ✅ 保留
codex_api_keys:
  my-key:
    key: "sk-xxx"
    base-url: "https://chatgpt.com/backend-api/codex"
```

`base-url` 必须是 `/backend-api/codex` 路径，不是纯域名。

### 4. 认证文件正确加载但模型不出现

**管理 API 返回 `None` 不代表配置没加载。** `auth-dir` 字段是 `json:"-"` 标记的，管理 API 故意不暴露。

**排查方法：** 直接检查：
1. `<auth-dir>/` 目录 — 认证文件是否存在
2. 日志中是否有 `applied core auth` / `registerModelsForAuth` 输出
3. 测试 API 调用是否正常返回

### 5. 请求超时 / 502

CLI Proxy 需要访问 `chatgpt.com` 后端。如果 ChatGPT 被墙：

- 必须在 config.yaml 中配置 `proxy-url: "http://127.0.0.1:PORT"`
- 或通过环境变量设置代理
- 代理关闭时请求会直接超时

### 6. 图片生成报错

图片生成通过 Responses API 转发，使用 `tool_choice: {type: "image_generation"}` 调用。

**常见失败场景：**
- Codex Free 账号不支持 → 报 `Tool choice 'image_generation' not found`
- 需要 Codex Pro 账号

## 快速诊断流程

当用户报告模型调用异常时：

1. **确认错误消息** — 看是否包含模型名
2. **检查请求体** — 用 Python 或 `@body.json` 重发验证
3. **检查认证** — 确认 codex-api-key 有 base-url，auth-dir 文件正确
4. **检查网络** — 确认代理配置正确、目标可达
5. **查看日志** — 搜索 `registerModelsForAuth`、`applied core auth`、`provider_not_found`

## 参考

- 先看本文件：适合快速定位常见根因
- 需要源码级确认时，再看 `references/source-architecture.md`

该 reference 文件包含关键源码文件、函数链路和模型注册逻辑的完整说明。
