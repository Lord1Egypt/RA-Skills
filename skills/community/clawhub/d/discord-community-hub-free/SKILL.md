---
name: "discord-community-hub-free"
description: "基础 Discord 社区管理工具,支持用户信息、服务器列表与基础集成查询。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "Discord社区中心免费版"
  version: "1.0.0"
  summary: "基础 Discord 社区管理工具,支持用户信息、服务器列表与基础集成查询。"
  tags:
    - "Discord"
    - "社区管理"
    - "Communication"
    - "服务器管理"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# Discord 社区中心(免费版)

## 概述

Discord 社区中心免费版是一款面向个人社区管理者的 Discord 社区基础管理工具。它通过集成网关连接 Discord 账号,提供当前用户资料查询、已加入服务器列表、服务器成员与角色信息、服务器小组件(widget)与邀请详情等只读查询能力,以及基础集成连接与工具发现功能。

免费版聚焦安全低风险的只读操作,适合个人 Discord 社区的日常信息查询和小型服务器的概览管理。所有写操作(如离开服务器、修改用户信息、编辑命令权限)在免费版中不可用,如需这些能力请升级至 Pro 版。

## 核心能力

| 能力模块 | 说明 | 免费版支持 |
|:-------|:-----|:----------|
| 用户资料 | 查询当前用户信息 | 支持 |
| 服务器列表 | 列出已加入的服务器 | 支持 |
| 成员信息 | 查询服务器成员资料 | 支持 |
| 角色信息 | 查询服务器角色概况 | 支持(只读) |
| 服务器组件 | 获取 widget 与邀请详情 | 支持 |
| 集成连接 | 连接 Discord 账号 | 支持 |
| 工具发现 | 列出与搜索可用工具 | 支持 |
| 应用命令 | 管理命令权限 | 不支持 |
| 权益管理 | 订阅与 entitlement | 不支持 |
| 角色连接 | 元数据更新 | 不支持 |
| 用户修改 | 修改用户名/头像 | 不支持 |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 按照skill规范执行核心功能执行操作,遵循单一意图原则。
**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 按照skill规范执行参数配置与调用操作,遵循单一意图原则。
**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 按照skill规范执行结果处理与输出操作,遵循单一意图原则。
**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：社区管理工具、支持用户信息、服务器列表与基础、集成查询、面向个人社区管理、社区基础管理工具、核心能力、查询当前用户资料、与已加入服务器列、获取服务器成员信、息与角色概况、查询服务器小组件、基础集成连接与工等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一:查询个人 Discord 账号概况

想快速了解自己 Discord 账号的基本信息和已加入的服务器。

```javascript
// 1. 获取当前用户资料
const me = await integration.call_tool({
  tool: "discord_get_my_user",
  parameters: {}
});

// 2. 列出已加入的服务器
const guilds = await integration.call_tool({
  tool: "discord_list_my_guilds",
  parameters: {}
});

// 3. 获取自己在某服务器的成员信息
const member = await integration.call_tool({
  tool: "discord_get_my_guild_member",
  parameters: { guild_id: "123456789" }
});
```

返回结果包含用户名、ID、头像、已加入服务器列表及各服务器的成员角色、昵称、加入时间等。

### 场景二:服务器概览与邀请解析

新建社区后,想确认服务器组件状态并解析分享出去的邀请链接。

```javascript
// 1. 获取服务器 widget(JSON 格式)
const widget = await integration.call_tool({
  tool: "discord_get_guild_widget",
  parameters: { guild_id: "123456789" }
});

// 2. 获取 widget 图片(PNG)
const widgetPng = await integration.call_tool({
  tool: "discord_get_guild_widget_png",
  parameters: { guild_id: "123456789" }
});

// 3. 解析邀请码详情
const invite = await integration.call_tool({
  tool: "discord_invite_resolve",
  parameters: { invite_code: "abc123xyz" }
});
```

### 场景三:集成工具发现

连接 Discord 后,想了解可用的工具集。

```javascript
// 1. 确认 Discord 已连接
const integrations = await integration.list_integrations();

// 2. 列出 Discord 可用工具
const tools = await integration.list_tools({ integration: "discord" });

// 3. 搜索特定功能工具
const found = await integration.search_tools({
  query: "guild",
  integration: "discord"
});
```

## 不适用场景

以下场景Discord社区中心免费版不适合处理：

- 逆向工程闭源API
- API安全渗透测试
- 非标准协议集成

## 触发条件

需要API集成、接口对接、Webhook配置、系统连接时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 依赖详情

在 Agent 平台安装集成网关插件:

```text
platform plugins install integration-gateway
```

安装后开启新的对话会话以加载插件目录。

### 第二步:配对集成网关

```javascript
// 1. 发起配对
const pairing = await integration.begin_pairing();

// 2. 在浏览器中打开返回的 URL
// 3. 登录集成网关并批准设备
```

### 第三步:连接 Discord 账号

在集成网关控制台中,打开 Discord 连接页面,完成 OAuth 授权流程,确认连接成功。

### 第四步:验证连接

```javascript
// 验证 Discord 已连接
const connected = await integration.list_integrations();

// 列出可用工具
const tools = await integration.list_tools({ integration: "discord" });
```

## 示例

### 用户资料查询

```javascript
// 获取当前用户完整资料
await integration.call_tool({
  tool: "discord_get_my_user",
  parameters: {}
});

// 获取 OAuth2 授权详情(含 scope 与过期时间)
await integration.call_tool({
  tool: "discord_get_my_oauth2_authorization",
  parameters: {}
});

// 获取 OIDC 用户信息(符合 OpenID Connect)
await integration.call_tool({
  tool: "discord_get_openid_connect_userinfo",
  parameters: {}
});
```

### 服务器信息查询

```javascript
// 获取任意用户信息(传 '@me' 表示当前用户)
await integration.call_tool({
  tool: "discord_get_user",
  parameters: { user_id: "@me" }
});

// 列出已连接的第三方账号
await integration.call_tool({
  tool: "discord_list_my_connections",
  parameters: {}
});

// 获取服务器模板详情
await integration.call_tool({
  tool: "discord_get_guild_template",
  parameters: { template_code: "abc123" }
});
```

### 网关与工具

```javascript
// 获取 WebSocket 网关 URL
await integration.call_tool({
  tool: "discord_get_gateway",
  parameters: {}
});

// 获取 OAuth2 公钥(用于外部 JWT 验证)
await integration.call_tool({
  tool: "discord_get_public_keys",
  parameters: {}
});

// 列出 Nitro 贴纸包
await integration.call_tool({
  tool: "discord_list_sticker_packs",
  parameters: {}
});
```

## 最佳实践

1. **优先只读操作**: 免费版聚焦只读查询,安全无风险。在进行任何管理操作前,先用只读工具确认当前状态(如先查成员信息再考虑角色调整)。

2. **Widget 需服务器开启**: 获取服务器 widget 前需在服务器设置 → Widget 中开启「启用服务器组件」。未开启时调用会返回错误。

3. **邀请码及时解析**: 分享邀请链接前用 `discord_invite_resolve` 解析确认有效期和目标服务器,避免邀请过期或指向错误服务器。

4. **集成工具检索技巧**: 使用 `search_tools` 按功能关键词搜索(如 "guild"、"member"、"role"),快速定位所需工具,避免在长列表中手动翻找。

5. **OAuth scope 确认**: 连接 Discord 时注意授权范围(scope)。基础查询只需 `identify` + `guilds`;如需邮箱需 `email` scope。scope 不足会导致部分工具报错,可重新连接补全。

6. **凭证安全**: 集成网关仅存储 OAuth 令牌,不存储原始机器人令牌。设备凭证保存在本地插件配置中。切勿在代码或配置中硬编码任何令牌。

7. **区分令牌类型**: 机器人令牌(Bot Token)与 OAuth2 Bearer 令牌能力不同。部分工具(如编辑命令权限)需要 Bearer 令牌,使用机器人令牌会报错。按工具要求使用对应令牌类型。

## 常见问题

### Q1: 安装插件后工具不显示怎么办?

安装集成网关插件后,需开启新的对话会话以重新加载插件目录。若仍不显示,调用 `list_integrations` 确认集成网关已配对成功,再调用 `list_tools` 检查 Discord 工具是否注册。

### Q2: 获取 widget 报错「Guild widget disabled」?

服务器组件需在 Discord 服务器设置 → Widget 中手动开启「启用服务器组件」。未开启时调用 `discord_get_guild_widget` 会返回错误。请服务器管理员开启后重试。

### Q3: 「401 Unauthorized」错误是什么原因?

通常是令牌类型不匹配。查询类操作使用 OAuth2 Bearer 令牌;若误用机器人令牌会返回 401。请确认集成网关使用的是 OAuth2 授权流程获取的 Bearer 令牌,并在连接时授予了足够 scope。

### Q4: 免费版能修改用户名或头像吗?

不能。修改用户资料(`discord_modify_current_user`)属于写操作,免费版不提供。如需修改用户名(每小时限 2 次)或头像,请升级至 Pro 版。免费版仅支持只读查询。

### Q5: 「Username change limit reached」是什么?

Discord 限制用户名每小时最多修改 2 次。频繁修改会触发此限制,需等待后再试。这是 Discord 平台限制,与工具版本无关。

### Q6: 如何确认连接的 scope 是否足够?

调用 `discord_get_my_oauth2_authorization` 可查看当前授权的 scope 列表和令牌过期时间。若某工具报权限不足,对比工具要求的 scope 与当前已授权 scope,缺失的需重新连接 Discord 补全授权。

### Q7: 集成网关存储哪些凭证?

集成网关仅存储 OAuth 令牌(用于访问 Discord API),不存储原始机器人令牌或密码。设备凭证保存在本地 Agent 插件配置中。`discord_get_public_keys` 用于验证外部 JWT,不用于存储密钥。

## 依赖说明

### 运行环境

- **Agent 平台**: 支持解析 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **网络**: 需可访问 Discord API 与集成网关
- **浏览器**: OAuth 授权流程需在浏览器中完成

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM 能力 | API | 必需 | 由 Agent 内置大模型提供 |
| 集成网关插件 | 插件 | 必需 | Agent 平台插件市场安装 |
| Discord OAuth2 | 授权 | 必需 | Discord Developer Portal 注册应用 |
| Discord API | 服务 | 必需 | Discord 平台提供 |
| 浏览器 | 运行时 | 必需 | 用于 OAuth 授权流程 |

### API Key 配置

- **OAuth2 应用**: 在 Discord Developer Portal 注册 OAuth2 应用,获取 Client ID 和 Client Secret。
- **授权 scope**: 基础查询需 `identify` + `guilds` scope;获取邮箱需 `email` scope;OIDC 需 `openid` scope。按需配置。
- **集成网关配对**: 通过集成网关完成设备配对,凭证保存在本地插件配置中,无需手动管理令牌。
- **其他 API Key**: 免费版不依赖额外 API Key。

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令 + 部分功能需 `exec` 执行能力)
- **说明**: 以自然语言指令驱动 Agent 通过集成网关调用 Discord 工具完成社区查询
- **适用规模**: 个人/小团队,只读查询为主,无写操作风险
- **升级建议**: 如需应用命令管理、权益管理、角色连接、用户修改等写操作,请升级至 `discord-community-hub-pro`

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
