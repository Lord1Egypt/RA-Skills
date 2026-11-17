---
slug: "discord-communities-free"
name: "discord-communities-free"
version: "1.0.0"
displayName: "Discord社区免费"
summary: "Discord社区只读查询助手,提供用户身份、公会列表与邀请解析基础能力。Discord 社区管理助手(免费版),基于 ClawLink OAuth 提供只读访问能力. 覆盖当前用户资料、公"
summary_zh: "Discord社区只读查询助手,提供用户身份、公会列表与邀请解析基础能力。Discord 社区管理助手(免费版),基于 ClawLink OAuth 提供只读访问能力. 覆盖当前用户资料、公"
license: "MIT"
description: "|-. 适用于需要discord communities相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  Discord 社区管理助手(免费版),基于 ClawLink OAuth 提供只读访问能力.
  覆盖当前用户资料、公会列表、成员信息、邀请解析与公钥查询等基础场景.
  核心能力:
  - 用户身份:获取当前用户资料与 OIDC 声明
  - 公会查询:列出当前用户所在公会、获取成员信息
  - 邀请解析:解析邀请 code 获取详情
  - 工具查询:获取 WebSocket 网关 URL 与 OAuth2 公钥

  不含商业权益管理(SKU/订阅/消耗)、应用命令权限编辑、角色连接元数据更新等
  高级功能。如需完整能力请升级付费版.
  适用于个人开发者快速核验 Discord 身份与公会信息.
  不适用于商业应用权益核验与角色连接同步场景.
tags:
  - Communication
  - discord
  - communities
  - automation
  - productivity
  - 社区运营
  - 社交
  - 通信
  - scope
  - oauth2
tools:
  - read
  - exec
  - write
homepage: ""
category: "Communication"
pricing_tier: free
---
# Discord 社区管理 (免费版)

基于 ClawLink OAuth 的 Discord 只读查询助手,提供用户身份、公会列表与邀请解析基础能力。所有操作均为 `safe` 风险等级,无需额外确认.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Discord社区免费处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 核心能力
### 1. 先验证 ClawLink 集成可用
```javascript
// 确认 Discord 集成已连接
clawlink_list_integrations();
// 列出可用工具
clawlink_list_tools({ integration: "discord" });
```

未连接时返回 `integration_not_found`,需先完成 OAuth 配对流程.

### 2. 仅使用 OAuth2 Bearer Token
免费版仅支持只读操作,所有调用均使用 Bearer Token。Bot Token 不适用本 skill 任何工具.

- 参考`仅使用 OAuth2 Bearer Token`的配置文档进行参数调优
### 3. 仅执行 safe 级别操作
免费版不包含 `confirm` 与 `high_impact` 级别工具(如退出公会、修改用户名、删除测试权益)。变更类操作请升级付费版.
**处理**: 解析 safe 级别指令的输入参数,完成核心逻辑,返回结构化响应和状态.
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 适用场景

| 场景 | 输入 | 输出 |
|:-----|:-----|:-----|
| 用户身份核验 | 无参数 | 当前用户资料、OIDC 声明、scope 列表 |
| 公会列表查询 | 无参数 | 当前用户所在公会清单 |
| 邀请解析 | 邀请 code | 邀请详情(公会名、人数、过期时间) |

**不适用于**: 商业权益核验、应用命令权限编辑、角色连接元数据同步(需升级付费版).
## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 使用流程

1. 调用 `clawlink_list_integrations` 确认 Discord 集成已配对
2. 用 `discord_get_my_oauth2_authorization` 检查 scope 是否包含 `identify` 与 `guilds`
3. 按需调用只读工具,所有操作均安全无副作用
4. 异常时优先检查鉴权方式与 scope

**结果验证**: 任务完成后,查看输出确认状态。成功时返回摘要和数据;失败时根据错误信息排查,参考恢复章节获取修复步骤.
## 工具参考

| 工具 | 用途 |
|:---:|:---:|
| `discord_get_my_user` | 获取当前用户资料(含 email,如授权) |
| `discord_get_user` | 按 ID 获取任意用户(`@me` 表示当前用户) |
| `discord_get_openid_connect_userinfo` | 获取 OIDC 声明(sub/email/picture/locale) |
| `discord_get_my_oauth2_authorization` | 获取授权详情、scope、过期时间 |
| `discord_list_my_guilds` | 列出当前用户所在公会(部分字段) |
| `discord_get_my_guild_member` | 获取当前用户在指定公会的成员信息 |
| `discord_invite_resolve` | 解析邀请 code 获取详情 |
| `discord_get_gateway` | 获取 WebSocket 网关 URL |
| `discord_get_public_keys` | 获取 OAuth2 公钥(用于验签外部 JWT) |

## 案例展示

### 案例1: 用户身份与公会信息核验

新用户接入后,需要快速核验 Discord 身份并列出所在公会.
```javascript
// 1. 获取当前用户资料
const me = await clawlink_call_tool({
  tool: "discord_get_my_user",
  parameters: {}
});
// 返回: { id, username, discriminator, email, avatar, ... }
// ...
// 2. 列出当前用户所在公会
const guilds = await clawlink_call_tool({
  tool: "discord_list_my_guilds",
  parameters: {}
});
// 返回: [{ id, name, owner, permissions, ... }]
// ...
// 3. 验证当前 OAuth2 授权范围
const auth = await clawlink_call_tool({
  tool: "discord_get_my_oauth2_authorization",
  parameters: {}
});
// 返回: { application: {...}, scopes: ["identify","guilds"], expires: "..." }
```

输出: 用户资料 + 公会清单 + 授权 scope,可用于判断是否具备后续付费版操作的权限基础.
### 案例2: 邀请解析与网关查询

落地页需要展示邀请对应的公会信息与 WebSocket 网关地址.
```javascript
// 1. 解析邀请 code
const invite = await clawlink_call_tool({
  tool: "discord_invite_resolve",
  parameters: { invite_code: "abc123xyz" }
});
// 返回: { guild: { name, ... }, approximate_member_count, expires_at }
// ...
// 2. 获取 WebSocket 网关 URL
const gateway = await clawlink_call_tool({
  tool: "discord_get_gateway",
  parameters: {}
});
// 返回: { url: "wss://gateway.discord.gg" }
```

输出: 邀请详情 + 网关 URL,可用于构建自定义客户端连接.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| `401 Unauthorized` | Bot Token 用于需 Bearer 的端点 | 改用 OAuth2 Bearer Token,确保 scope 包含 `identify` 与 `guilds` |
| `Missing Access` | 用户未加入目标公会 | 核对公会 ID,引导用户先加入公会再查询 |
| `Invite code invalid or expired` | 邀请码已失效或被删除 | 提示用户重新生成邀请,并用 `discord_invite_resolve` 验证 |
| `Unauthorized scope` | OAuth2 未授权对应 scope | 重新发起授权流程,带上 `identify`、`guilds` 等基础 scope |
| `Rate limit exceeded` | 短时间内调用过频 | 检查网络连接和配置后重试,避免循环调用 `discord_list_my_guilds` |

## 常见问题

### Q1: 免费版与付费版有何区别?
A: 免费版仅提供只读访问(用户身份、公会列表、邀请解析);付费版增加商业权益管理(SKU/订阅/消耗)、应用命令权限编辑、角色连接元数据同步、公会小组件嵌入等高级能力,并提供风险分级执行策略与完整错误诊断.
### Q2: 如何获取当前用户的 Discord email?
A: 调用 `discord_get_my_user`,需 OAuth2 授权包含 `email` scope。若仅授权 `identify`,返回的 email 字段为空。免费版不支持修改用户信息,如需修改请升级付费版.
### Q3: 为什么 `discord_list_my_guilds` 返回的字段不完整?
A: 该接口仅返回公会的基本信息(id、name、owner 等),完整公会信息(成员列表、频道列表)需额外 scope 与权限,免费版不涉及。如需完整公会管理能力请升级付费版.
### Q4: 邀请解析返回的 `expires_at` 为 null 是什么含义?
A: 表示该邀请为永久邀请,无过期时间。临时邀请会返回具体 ISO8601 时间戳.
## 已知限制

- 仅支持只读操作,无法修改用户资料、退出公会或管理角色连接
- `discord_list_my_guilds` 仅返回公会部分字段,完整信息需付费版工具
- 不含商业权益(SKU/订阅/消耗)查询与管理能力
- 不含应用命令权限查询与编辑能力
- 不含公会小组件(JSON/PNG)嵌入能力
- 依赖 ClawLink 插件与有效 OAuth2 Bearer Token

## 升级提示

> 本免费版提供基础只读查询能力。如需商业权益管理(SKU/订阅/消耗)、应用命令权限编辑、
> 角色连接元数据同步(如 Xbox Gamertag)、公会小组件嵌入、风险分级执行策略与
> 完整错误诊断(8+ 场景)等高级能力,请升级至 **Discord 社区管理付费版**.
## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "Discord社区免费处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "discord-communities"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
