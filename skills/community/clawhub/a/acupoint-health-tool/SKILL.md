---
name: acupoint-health-tool
description: 当用户咨询经络穴位、中医按摩养生问题，或需要调用 AI_Health 网站的 MCP 服务（工具：acupoint_consult 穴位咨询、share_create/share_get 分享读写、list_reference_books 列出古籍）时使用本技能。内容涵盖 Streamable HTTP（/mcp）与旧版 SSE（/mcp/sse）两种连接方式、多轮意图澄清流程、基于本机数字指纹自动生成唯一客户端 ID 的"注册"规则。触发词："穴位咨询"、"经络按摩"、"AI_Health MCP"、"调用养生助手"。
agent_created: true
---

# AI_Health 经络穴位 MCP 服务使用指南

## 概述

acupoint-health-tool 是一个连接 AI_Health 经络穴位养生 MCP 服务（https://health.geeyo.com）的 Agent 技能，让任何 MCP 客户端一句话即可获得有古籍依据的中医穴位按摩建议。

核心价值：

- **有据可查的中医咨询**：回答严格出自《玉龙歌》《玉龙赋》《百症赋》《马丹阳天星十二穴治杂病歌》四部针灸古籍，每条穴位推荐附出处与选穴原理，拒绝无来源的养生泛谈
- **开箱即用，零门槛接入**：同时支持 Streamable HTTP 与旧版 SSE 双传输，新老 MCP 客户端一个 URL 即连，无需部署任何本地组件
- **免注册的身份体系**：基于本机数字指纹派生客户端 ID——无需账号密码，同一台机器的咨询历史自动归属同一身份，且只上送哈希、不泄露原始指纹，隐私安全
- **智能多轮澄清**：描述不清时服务端主动追问（部位/性质/诱因，最多 3 轮），本技能内置完整流程指引，按图索骥即可跑通对话，避免答非所问
- **咨询结果可分享**：一键生成分享链接，把完整问答过程发给家人朋友查看

适用场景：头痛失眠、颈肩腰腿不适等日常病痛的穴位按摩自助咨询；健康类 Agent 产品快速集成中医穴位能力。

本技能指导三件事：如何连接该服务、如何完成基于本地数字指纹的自动"注册"、如何正确走多轮澄清对话流程。

## 连接方式

服务与网站同端口同进程，生产地址为 `https://health.geeyo.com`（本地开发时替换为 `http://localhost:3000`）。支持两种传输，**优先使用 Streamable HTTP**：

| 传输 | 端点 | 说明 |
|---|---|---|
| Streamable HTTP（推荐） | `POST/GET/DELETE {BASE_URL}/mcp` | 有状态；初始化后从响应头取 `mcp-session-id`，后续请求携带该头 |
| 旧版 HTTP+SSE（兼容） | `GET {BASE_URL}/mcp/sse` + `POST {BASE_URL}/mcp/messages?sessionId=` | 先建 SSE 长连接，从 `endpoint` 事件获取消息投递地址 |

MCP 客户端配置示例：

```json
{ "mcpServers": { "ai-health": { "url": "https://health.geeyo.com/mcp" } } }
```

老客户端只支持 SSE 时改用 `https://health.geeyo.com/mcp/sse`。

握手/请求的原始 JSON-RPC 与 curl 示例见 `references/protocol_examples.md`（仅在需要手工调试 HTTP 层时加载）。

## 自动注册：基于本地数字指纹生成唯一 ID

该服务**没有**账号注册接口。客户端身份由 Agent 自行生成：根据本机数字指纹派生一个**稳定且唯一**的客户端 ID，作为业务会话 `sessionId` 的前缀，使同一台机器的咨询历史可以归属到同一"账号"。

生成规则（必须遵循）：

1. 采集本机指纹源（按平台取其一，再拼接 hostname 与用户名增强唯一性）：
   - Windows：注册表 `HKLM\SOFTWARE\Microsoft\Cryptography` 的 `MachineGuid`
     （`reg query "HKLM\SOFTWARE\Microsoft\Cryptography" /v MachineGuid`）
   - Linux：`/etc/machine-id`
   - macOS：`ioreg -rd1 -c IOPlatformExpertDevice` 中的 `IOPlatformUUID`
2. 计算 `SHA-256(machineId + "|" + hostname + "|" + username)`，取十六进制前 32 位作为 `clientId`。
3. 业务会话 ID 用 `"{clientId}-{短随机串}"` 格式；每个新咨询话题换一个随机串，`clientId` 部分保持不变。
4. **隐私约束**：只上送哈希结果，绝不发送原始 MachineGuid、MAC 地址、用户名等明文指纹；不落盘缓存原始指纹，只可缓存派生出的 `clientId`。

Node 一行式示例：

```bash
node -e "const c=require('crypto'),os=require('os'),{execSync}=require('child_process');const mid=execSync('reg query \"HKLM\\\\SOFTWARE\\\\Microsoft\\\\Cryptography\" /v MachineGuid').toString().match(/\{[0-9a-f-]+\}/i)[0];console.log(c.createHash('sha256').update(mid+'|'+os.hostname()+'|'+os.userInfo().username).digest('hex').slice(0,32))"
```

注意：MCP 传输层自身的会话（`mcp-session-id` 头 / SSE sessionId）由服务器生成，与上述业务 `sessionId` 是两回事，不要混用。

## 工具清单与使用要点

### 1. acupoint_consult — 穴位咨询（核心工具，多轮流程）

入参：`message`（病痛描述，必填）、`sessionId`（可选，多轮时必传）。
返回 JSON 字段：`reply`、`isFinal`、`sessionId`，可能有 `rejected`、`followupCount`。

多轮流程（必须按此处理）：

1. 首次调用：`sessionId` 传 `"{clientId}-{随机串}"`；`message` 尽量一次给全三要素——**部位、疼痛性质、诱因/伴随症状**（如"前额胀痛，受凉后加重，伴轻微恶心"），可显著减少追问轮数。
2. `isFinal=false` 且无 `rejected`：`reply` 是追问。回答追问内容后**携带同一 `sessionId`** 再次调用，直到 `isFinal=true`。最多追问 3 轮，超限服务端自动强制作答。
3. `isFinal=true`：`reply` 为最终 Markdown 回答（推荐穴位/定位/手法/选穴原理/古籍出处/免责声明），直接呈现给用户，不要删减免责声明。
4. `rejected=true`：问题与中医穴位无关被拒。不要重试同一问题；如确属健康问题，改写为身体不适描述再试。
5. 最终回答生成后该会话即完结；新话题必须换新的随机串生成新 `sessionId`，不要复用已完结会话。

注意：最终回答由 LLM 生成，单次调用可能需要 30–120 秒，设置足够的客户端超时。

### 2. share_create / share_get — 分享读写

- `share_create`：入参 `messages`（`[{role: "user"|"assistant", content}]`，至少 1 条）、`title`（可选，缺省取首条用户消息前 40 字）。返回 `shareId`。分享页地址为 `{BASE_URL}/?share={shareId}`（注意：参数名为 `share` 而非 `id`，路径为站点根 `/` 而非 `/share.html`；前端 `app.js` 仅读取 `?share=` 参数，用错格式会回退成初始提问页）。
- `share_get`：入参 `shareId`，返回 `{title, messages, createdAt}`；不存在时返回 `isError`。服务端最多保留 200 条分享，旧的会被淘汰，`shareId` 不保证永久有效。

### 3. list_reference_books — 列出参考古籍

无入参。返回本服务回答所依据的古籍名列表。用户质疑答案依据时先调用它说明知识边界；古籍未覆盖的病症，回答中会声明"选择最接近的"。

## 错误处理

| 现象 | 处理 |
|---|---|
| POST /mcp 返回 400 "无效或缺失的 mcp-session-id" | 传输层会话已失效，重新走 initialize 建会话 |
| SSE 连接断开 | 重连 `/mcp/sse`，取新 endpoint，重新 initialize |
| 工具返回超时 | acupoint_consult 属长耗时调用，增大超时后重试一次；仍失败则报告用户 |
| `分享不存在或已过期` | shareId 已被淘汰，告知用户无法恢复 |
