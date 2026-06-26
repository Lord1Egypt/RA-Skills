# 第三方 Provider 配置详情 (v7)

每家 provider 的 base_url、推荐模型、注意事项。Skill 在引导用户选 B 路径时读这份。

## 协议适配总览

Codex CLI 0.130+ 默认发 OpenAI **Responses 协议**,而多数第三方服务只支持 **Chat 协议**。本 skill 通过 `codex-relay` 协议中转层抹平这个差异。

| Profile | 端口 | 上游 | 是否走 relay |
|---------|------|------|-------------|
| agentplan | 4446 | https://ark.cn-beijing.volces.com/api/plan/v3 | ✅ relay |
| kimi | 4447 | https://api.moonshot.cn/v1 | ✅ relay |
| deepseek | 4448 | https://api.deepseek.com/v1 | ✅ relay |
| arkv3 | — | https://ark.cn-beijing.volces.com/api/v3 | ❌ 直连(原生 Responses) |
| custom | 4449 或直连 | 用户提供 | 🔍 自动探测 |

## 1. Kimi (Moonshot)

| 字段 | 值 |
|---|---|
| base_url(Codex 看到的) | `http://127.0.0.1:4447/v1` |
| 真实上游 | `https://api.moonshot.cn/v1` |
| 默认 model | `kimi-k2-turbo-preview` |
| wire_api | `responses`(经 relay 翻译为 Chat) |
| env_key | `MOONSHOT_API_KEY` |
| Key 获取 | <https://platform.moonshot.cn/console/api-keys> |
| 计费 | 按 token,Kimi 平台账户余额 |

**可选模型**(用户可在 setup 时通过第三参数覆盖):
- `kimi-k2-turbo-preview` — 默认,综合能力最强,长上下文
- `kimi-k2-thinking` — 思考模式,带 reasoning
- `moonshot-v1-128k` — 老一代 128K 模型

**注意**:Moonshot 不支持 OpenAI Responses API,只支持 Chat Completions,所以必须经 codex-relay 翻译。

## 2. DeepSeek

| 字段 | 值 |
|---|---|
| base_url(Codex 看到的) | `http://127.0.0.1:4448/v1` |
| 真实上游 | `https://api.deepseek.com/v1` |
| 默认 model | `deepseek-chat` |
| wire_api | `responses`(经 relay 翻译为 Chat) |
| env_key | `DEEPSEEK_API_KEY` |
| Key 获取 | <https://platform.deepseek.com/api_keys> |
| 计费 | 按 token,DeepSeek 平台账户余额(便宜) |

**可选模型**:
- `deepseek-chat` — V3 通用对话,默认
- `deepseek-reasoner` — R1 推理模型,带思考链

**注意**:DeepSeek 偶尔会有限流,profile 里已经设了 `request_max_retries = 4`。

## 3. 火山方舟普通 v3 (arkv3)

| 字段 | 值 |
|---|---|
| base_url | `https://ark.cn-beijing.volces.com/api/v3` |
| 默认 model | `doubao-seed-1-6-250615` |
| wire_api | `responses`(原生支持) |
| env_key | `ARK_V3_API_KEY` |
| Key 获取 | 火山方舟控制台 → API Key 管理 |
| 计费 | 自购 Key,按 token 计费 |

**与 AgentPlan 的区别**:

| 维度 | AgentPlan(profile=agentplan) | 普通 v3(profile=arkv3) |
|---|---|---|
| 路径 | `/api/plan/v3` | `/api/v3` |
| Key 类型 | AgentPlan 控制台分配的"专属 Key" | API Key 管理的普通 Key |
| 计费 | 套餐内额度 | 自购,按 token |
| Responses 支持 | 仅 Chat,需 codex-relay 翻译 | 原生支持,直连 |
| 模型字段 | `ark-code-latest`(智能路由) | 具体模型名(如 `doubao-seed-1-6-250615`) |

**注意**:很多用户会把这两个搞混。如果用户有"AgentPlan 控制台的 Key" → 选 A 路径;如果用户有"普通方舟控制台 API Key 管理里的 Key" → 选 B 路径的 arkv3。

## 4. Custom(自定义 OpenAI 兼容端点)

适用于:公司自建 LLM 网关、自建反代、其他未在上述列表中的 OpenAI 兼容服务(如 GLM / 通义千问 / Yi / 百川 的官方 OpenAI 兼容接口、LiteLLM、vLLM、Ollama 等)。

**用户必须提供三样东西**:

| 参数 | 必填 | 示例 | 说明 |
|---|---|---|---|
| API Key | ✅ | `sk-xxxx` 或自建网关的 token | 写入环境变量 `CUSTOM_API_KEY` |
| 模型名 (model) | ✅ | `qwen-max` / `glm-4.6` / `yi-large` | 服务端能识别的 model id |
| Base URL | ✅ | `https://dashscope.aliyuncs.com/compatible-mode/v1` | OpenAI 兼容端点的根地址,**通常以 `/v1` 结尾** |

### 自动探测逻辑

setup-thirdparty.sh 会对用户给的 `base_url` 发一次 `POST {base_url}/responses`(`relay-helper.sh#probe_responses_support`):

| HTTP code | 判定 | 路由方式 |
|---|---|---|
| 200 / 400 / 401 / 403 / 422 | 端点存在,**支持** Responses | 直连,profile 里 base_url 直接写上游 |
| 404 | 端点不存在,**不支持** Responses | 走 relay(端口 4449),profile 里 base_url 写 `http://127.0.0.1:4449/v1` |
| 网络不通 / 其他 | 保守按"不支持"处理 | 走 relay |

走 relay 模式时,上游 URL 会写到 `~/.codex/custom-upstream`,沙箱重启时由 `.bashrc` 的 auto-recover 块自动恢复。

### 调用方式

```bash
bash setup-thirdparty.sh custom "$KEY" "<model>" "<base_url>"
```

### 示例

**通义千问(阿里云 DashScope)** — Chat-only,会自动启 relay:
```bash
bash setup-thirdparty.sh custom "sk-xxx" "qwen-max" "https://dashscope.aliyuncs.com/compatible-mode/v1"
```

**智谱 GLM** — Chat-only,会自动启 relay:
```bash
bash setup-thirdparty.sh custom "xxx.xxx" "glm-4.6" "https://open.bigmodel.cn/api/paas/v4"
```

**公司内部网关(若已原生支持 Responses)** — 自动直连:
```bash
bash setup-thirdparty.sh custom "internal-token" "gpt-4o" "https://llm-gateway.your-company.com/v1"
```

### 注意

- base_url 必须是 OpenAI 兼容(Chat Completions 至少要通)
- 沙箱环境(ArkClaw)在境内 IDC,**境外服务**(如 OpenAI 官方、OpenRouter、Anthropic 官方)通常连不上,custom 路径只建议接境内可达的端点
- 如果接通后报 4xx/5xx 错误,先用 `curl` 直接测一下端点是否能正常返回,排除是网关本身的问题
- 如果探测误判(罕见),用户可以手动编辑 `~/.codex/profiles/custom.toml` 把 `base_url` 改回直连或 relay 模式,然后:
  - 切到直连模式 → 删除 `~/.codex/custom-upstream`
  - 切到 relay 模式 → 把上游 URL 写入 `~/.codex/custom-upstream`,然后跑 `bash scripts/ensure-relay.sh`

## 选哪个?

| 用户场景 | 推荐 profile |
|---|---|
| 字节内部用户,有 AgentPlan 配额 | **agentplan**(套餐内,免费) |
| 个人有 Kimi 账号(月之暗面送的免费额度) | kimi |
| 想要最便宜的 token 价格 | deepseek |
| 自购了方舟 Key,但不在 AgentPlan 套餐 | arkv3 |
| 公司内有自建 OpenAI 兼容网关 / 想接通义/GLM/Yi 等境内服务 | custom |

> 如果用户不确定,默认推荐 **agentplan** — 沙箱内可用、免费、模型层面已经覆盖 Kimi/Doubao/DeepSeek/GLM。

> ⚠️ **关于境外服务(OpenAI / OpenRouter / Anthropic 官方等)**:ArkClaw 沙箱在境内 IDC,网络出口受限,这类服务**通常无法直连**,因此本 skill 不在二级菜单里提供。如用户坚持要接,可走 custom 路径自行尝试,但失败概率较高。
