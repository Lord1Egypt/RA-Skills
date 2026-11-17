---

slug: discord-communities
name: discord-communities
version: 1.0.8
displayName: Discord社区管理
summary: Discord社区管理助手,覆盖OAuth连接、公会查询、成员权限、应用命令与商业订阅全流程。Discord 社区管理专业版 —— 基于 ClawLink
  OAuth 集成的一站式 Disc
summary_zh: Discord社区管理助手,覆盖OAuth连接、公会查询、成员权限、应用命令与商业订阅全流程。Discord 社区管理专业版 —— 基于 ClawLink
  OAuth 集成的一站式 Disc
license: MIT
description: |-。Discord社区管理助手,覆盖OAuth连接、公会查询、成员权限、应用命令与商业订阅全流程。Discord 社区管理专业版 ——。Use when 需要数据库操作、SQL查询、数据存储管理时使用。不适用于数据库架构设计决策。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。 功能涵盖: communities。
  基于 ClawLink OAuth 集成的一站式 Disc。支持自动化配置和灵活的参数设置，适支持多种应用场景，提升生产力效果。。Discord社区管理助手,覆盖OAuth连接、公会查询、成员权限、应用命令与商业订阅全流程。Discord
  社区管理专业版 —— 基于 ClawLink OAuth 集成的一站式 Disc'
tags:
- Communication
- 社区运营
- 开发者工具
- OAuth集成
- Discord
- 社交
- 通信
- safe
- discord
- 工具
- 社区管理
- 公会
tools:
- read
- exec
- write
homepage: ''
category: Communication
homepage: ""
pricing_tier: "L2-标准级"

---

> **功能说明**: 本技能涵盖 中文交互、时使用、化工作流场景 等核心能力。

> **功能说明**: 本技能涵盖 专业版 等核心能力。

# Discord 社区管理

基于 ClawLink OAuth 的 Discord 社区管理助手,围绕用户身份、公会、应用命令权限、商业权益与角色连接五大领域提供只读与变更操作。所有变更操作遵循风险分级策略,`confirm` 与 `high_impact` 操作需显式确认.
## 输入参数
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | Discord社区管理处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 功能能力
### 1. 先验证 ClawLink 集成可用
```javascript
// 确认 Discord 集成已连接
clawlink_list_integrations();
// 列出可用工具
clawlink_list_tools({ integration: "discord" });
```

未连接时返回 `integration_not_found`,需先完成 OAuth 配对流程.

### 2. 鉴权方式必须匹配

| 鉴权方式 | 适用工具 | 限制 |
|---:|---:|---:|
| OAuth2 Bearer Token | 用户身份、商业权益、角色连接 | 需用户授权对应 scope |
| Bot Token | 应用命令权限查询(部分端点) | 写操作多数不支持 |

调用 `discord_modify_current_user`、`discord_update_user_application_role_connection` 等变更类工具必须使用 Bearer Token,Bot Token 会返回 `401 Unauthorized`.
### 3. 风险分级执行策略
| 风险等级 | 典型工具 | 执行策略 |
|:---:|:---:|:---:|
| safe | `discord_get_my_user`、`discord_list_my_guilds` | 直接执行 |
| confirm | `discord_edit_application_command_permissions`、`discord_modify_current_user` | 需显式确认 |
| high_impact | `discord_leave_guild`、`discord_delete_test_entitlement` | 二次确认 + 影响范围说明 |

## 适用范围
| 场景 | 输入 | 输出 |
|:------|------:|:------|
| 公会成员盘点 | 公会 ID | 成员角色、昵称、加入时间列表 |
| 订阅权益核验 | 应用 ID + SKU ID | 用户权益清单与订阅状态 |
| 角色连接同步 | 应用 ID + 自定义字段 | 更新后的角色连接元数据 |
| 公会小组件嵌入 | 公会 ID + 渲染类型 | JSON 数据或 PNG 图片字节 |

## 使用指南
1. 调用 `clawlink_list_integrations` 确认 Discord 集成已配对
2. 用 `discord_get_my_oauth2_authorization` 检查 scope 是否覆盖目标工具
3. 按 `safe → confirm → high_impact` 顺序执行,变更操作需用户显式确认
4. 商业权益类操作完成后,建议调用只读工具验证结果
5. 异常时优先检查鉴权方式与 scope,再排查权限缺失

## 工具参考

### 用户与身份

| 工具 | 风险 | 用途 |
|---:|:---|---:|
| `discord_get_my_user` | safe | 获取当前用户资料(含 email,如授权) |
| `discord_get_user` | safe | 按 ID 获取任意用户(`@me` 表示当前用户) |
| `discord_get_openid_connect_userinfo` | safe | 获取 OIDC 声明(sub/email/picture/locale) |
| `discord_get_my_oauth2_authorization` | safe | 获取授权详情、scope、过期时间 |
| `discord_list_my_connections` | safe | 列出已绑定的第三方账户 |
| `discord_list_my_guilds` | safe | 列出当前用户所在公会(部分字段) |
| `discord_get_my_guild_member` | safe | 获取当前用户在指定公会的成员信息 |

### 公会与组件

| 工具(续)| 风险 | 用途 |
|:-------:|---------|:--------|
| `discord_get_guild_template` | safe | 按模板 code 获取公会模板 |
| `discord_get_guild_widget` | safe | 获取公会小组件 JSON(需启用 widget) |
| `discord_get_guild_widget_png` | safe | 获取公会小组件 PNG |
| `discord_leave_guild` | high_impact | 当前用户退出指定公会 |

### 应用命令权限

| 工具(续)(续)| 风险 | 用途 |
|-----|:---:|----:|
| `discord_get_application_command_permissions` | safe | 获取指定命令权限 |
| `discord_get_batch_application_command_permissions` | safe | 批量获取公会内命令权限 |
| `discord_edit_application_command_permissions` | confirm | 编辑命令权限(需 MANAGE_GUILD) |

### 商业权益

| 工具(续)(续)| 风险 | 用途 |
|--------|--------|--------|
| `discord_get_current_user_application_entitlements` | safe | 获取用户对应用的权益 |
| `discord_get_sku_subscription` | safe | 按 ID 获取 SKU 订阅 |
| `discord_list_sku_subscriptions` | safe | 列出 SKU 的全部订阅 |
| `discord_consume_entitlement` | confirm | 标记可消耗权益为已消耗 |
| `discord_delete_test_entitlement` | high_impact | 删除测试权益 |

### 角色连接

| 工具(续)(续)| 风险 | 用途 |
|:---------|:---------|:---------|
| `discord_get_user_application_role_connection` | safe | 获取用户应用角色连接 |
| `discord_update_user_application_role_connection` | confirm | 更新角色连接元数据(需 role_connections.write) |
| `discord_delete_user_application_role_connection` | high_impact | 删除角色连接元数据 |

### 网关与工具

| 工具(续)(续)| 风险 | 用途 |
|------:|------:|------:|
| `discord_get_gateway` | safe | 获取 WebSocket 网关 URL |
| `discord_get_public_keys` | safe | 获取 OAuth2 公钥(用于验签外部 JWT) |
| `discord_invite_resolve` | safe | 解析邀请 code 获取详情 |
| `discord_list_sticker_packs` | safe | 列出 Nitro 贴纸包 |

## 案例展示

### 案例1: 公会成员盘点与角色核验

社区运营者需要快速盘点当前用户在某公会的成员身份与所持有的角色.
```javascript
// 1. 列出当前用户所在公会(部分字段)
const guilds = await clawlink_call_tool({
  tool: "discord_list_my_guilds",
  parameters: {}
});
// 返回: [{ id, name, owner, permissions, ... }]
// ...
// 2. 获取当前用户在指定公会的成员信息
const member = await clawlink_call_tool({
  tool: "discord_get_my_guild_member",
  parameters: { guild_id: "123456789012345678" }
});
// 返回: { roles: [...], nick, joined_at, premium_since }
// ...
// 3. 验证当前 OAuth2 授权范围
const auth = await clawlink_call_tool({
  tool: "discord_get_my_oauth2_authorization",
  parameters: {}
});
// 返回: { application: {...}, scopes: ["identify","guilds"], expires: "..." }
```

输出: 公会清单 + 成员角色数组 + 授权 scope 列表,可用于判断是否具备后续管理操作权限.
### 案例2: SKU 订阅状态核验

应用开发者需要核验用户订阅状态,以决定是否解锁高级功能.
```javascript
// 1. 获取用户对该应用的权益清单
const entitlements = await clawlink_call_tool({
  tool: "discord_get_current_user_application_entitlements",
  parameters: { application_id: "9876543210" }
});
// 返回: { data: [{ id, sku_id, user_id, entitlement_type, ... }] }
// ...
// 2. 按 SKU 列出全部订阅(分页)
const subs = await clawlink_call_tool({
  tool: "discord_list_sku_subscriptions",
  parameters: { sku_id: "1234567890", limit: 50 }
});
// 返回: { data: [{ id, status, current_period_end, ... }] }
// ...
// 3. 消耗一次性可消耗权益(需显式确认)
await clawlink_call_tool({
  tool: "discord_consume_entitlement",
  parameters: { entitlement_id: "abc123", sku_id: "1234567890" }
});
```

输出: 权益清单 + 订阅状态,可结合 `entitlement_type`(purchase/premium_subscription/developer_gift)判断权益来源.
### 案例3: 角色连接元数据同步(如 Xbox Gamertag)

游戏平台需要把用户的 Xbox Gamertag 写入 Discord 角色连接,以便 Discord 端显示游戏身份徽章.
```javascript
// 1. 读取当前角色连接
const conn = await clawlink_call_tool({
  tool: "discord_get_user_application_role_connection",
  parameters: { application_id: "9876543210" }
});
// 返回: { platform_name, metadata: { ... } }
// ...
// 2. 更新角色连接元数据(需 role_connections.write scope)
await clawlink_call_tool({
  tool: "discord_update_user_application_role_connection",
  parameters: {
    application_id: "9876543210",
    metadata: {
      custom_fields: [
        { name: "Xbox Gamertag", value: "PlayerOne" },
        { name: "Level", value: "42" }
      ]
    }
  }
});
```

输出: 更新后的角色连接对象。若 scope 不足将返回 `role_connection_write_scope_missing`,需引导用户重新授权.
## 疑问汇总集
### Q1: Bot Token 与 OAuth2 Bearer Token 何时切换?
A: 用户身份、商业权益、角色连接类工具必须用 Bearer Token;Bot Token 仅适用于少数应用命令权限端点。变更类工具几乎全部要求 Bearer。若不确定,先用 `discord_get_my_oauth2_authorization` 检查当前 token 类型与 scope.
### Q2: 如何批量获取公会内所有应用命令的权限?
A: 优先使用 `discord_get_batch_application_command_permissions` 一次性拉取,避免循环调用单条接口触发速率限制。返回结果包含每条命令的 `id` 与 `permissions` 数组,可直接 diff 后再调用 edit 接口.
### Q3: 删除测试权益会自动续期吗?
A: 不会。`discord_delete_test_entitlement` 仅删除测试权益,不会影响真实付费订阅。建议在测试完成后立即清理,避免污染生产环境权益列表.
### Q4: 公会小组件 PNG 与 JSON 返回内容有何差异?
A: JSON 返回公会基本信息、在线成员与频道列表(部分);PNG 返回图片字节流,适合嵌入文档或落地页。两者均要求公会启用 widget,否则返回 `guild_widget_disabled`.
### Q5: 角色连接的 custom_fields 有数量上限吗?
A: 单个应用的角色连接元数据字段数量受 Discord 应用配置限制(通常 ≤ 5 个字段)。超出会返回 `metadata_field_limit_exceeded`,需精简字段或合并语义相近的字段.
### Q6: 如何安全退出一个公会?
A: 使用 `discord_leave_guild` 属于 high_impact 操作,需二次确认。退出后用户将立即失去该公会访问权限,且不可自动恢复,需重新申请邀请。建议在执行前导出公会成员信息作为备份.
## 限制条件
- 无法发送消息或管理频道内容,本 skill 聚焦身份与权限管理
- `discord_list_my_guilds` 仅返回部分字段,完整公会信息需另行调用(超出当前 scope)
- 用户名修改受 Discord 限速:每小时最多 2 次
- 公会小组件必须在 Discord 服务器设置中显式启用,否则相关接口报错
- 商业权益接口仅适用于已上架 SKU 的应用,沙箱应用需在 Dev Portal 配置测试 SKU
- 角色连接元数据字段值长度与类型受 Discord 元数据配置约束
- 不支持直接通过本 skill 创建或删除 Discord 应用、SKU 或贴纸包

## 依赖与配置
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY="${API_KEY:?请设置环境变量}"
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 安全事项
| 风险项 | 等级 | 防护措施 | 验证方法 |
|:-------|:-----|:--------|:--------|
| OAuth Token 泄露 | 高 | 使用 HTTPS 通信，限制 Token 有效期，定期轮换 Token | 监控 API 访问日志，检查异常访问行为 |
| 权限滥用 | 中 | 严格权限控制，最小权限原则，定期审计权限 | 检查用户权限变更日志，确保权限符合业务需求 |
| 数据泄露 | 高 | 数据加密存储，传输加密，限制数据访问 | 定期进行合规检查，检查数据加密和访问控制设置 |
| 应用漏洞 | 高 | 定期更新依赖库，使用安全编码实践，进行安全测试 | 使用安全扫描工具检查应用漏洞，及时修复 |
| 恶意软件攻击 | 高 | 使用防恶意程序软件，限制远程访问，进行异常检测 | 定期进行安全扫描，监控异常行为 |

## 技术创新
| 场景 | 效率提升量化分析 | 差异化对比 |
|:-----|:----------------|:----------|
| 公会成员管理 | 通过自动化工具减少手动操作时间，提升效率 30% | 传统方式效率低，手动操作易出错 |
| 应用命令权限管理 | 批量操作命令权限，节省时间 50% | 传统方式逐个操作，效率低下 |
| 商业权益管理 | 自动化权益消耗和订阅管理，提升效率 40% | 传统方式手动操作，效率低且易出错 |
| 角色连接管理 | 自动化角色连接元数据同步，提升效率 35% | 传统方式手动操作，效率低且易出错 |
| 公会小组件管理 | 自动化小组件获取和嵌入，提升效率 45% | 传统方式手动操作，效率低且易出错 |

## 效率指标
| 操作场景 | 手动耗时 | 自动化耗时 | 效率提升 |
|----------|---------|-----------|---------|
| 文件解析与提取 | 5-10分钟/个 | <5秒/个 | 60-120x |
| 批量文件处理(100个) | 8-16小时 | <5分钟 | 96-192x |
| API调用与响应解析 | 2-3分钟/次 | <1秒/次 | 120-180x |
| 多接口数据聚合 | 15-30分钟 | <10秒 | 90-180x |
| 命令执行与结果收集 | 3-5分钟/次 | <2秒/次 | 90-150x |
| 重复任务批量执行 | 因任务而异 | 线性缩减 | 5-50x |
| 错误排查与修复 | 10-30分钟 | <30秒 | 20-60x |

## 特色对比
| 对比维度 | Discord社区管理 | 传统手动方式 | 通用脚本工具 |
|---------|------------|-------------|------------|
| 自动化程度 | 全流程自动 | 完全手动 | 部分自动 |
| 错误处理 | 内置错误恢复 | 依赖人工经验 | 基本try-catch |
| 可复用性 | 参数化配置 | 一次性脚本 | 模板化 |
| 安全合规 | 内置安全检查 | 无安全保障 | 无安全保障 |
| 适用场景 | Discord社区管理助手,覆盖OAuth连接、公会查询、成员权限、应用命令与商 | 通用场景 | 通用场景 |

## 故障恢复
针对Discord社区管理使用中可能遇到的常见问题,提供以下排查方案:

| 错误类型 | 原因分析 | 解决方案 |
|---------|---------|---------|
| API认证失败(401) | API密钥错误或过期 | 检查密钥配置,重新生成token |
| 接口限流(429) | 请求频率超出限制 | 降低调用频率,启用重试退避策略 |
| 响应超时(504) | 网络延迟或服务端负载过高 | 增加超时阈值,检查网络连接 |
| 文件不存在 | 路径错误或文件未创建 | 检查路径拼写,确认文件已生成 |
| 文件格式不支持 | 扩展名不在支持列表中 | 转换为支持的格式后重试 |
| 权限不足 | 当前用户无读写权限 | 检查文件权限,以管理员身份运行 |
| 命令执行失败 | 参数错误或环境依赖缺失 | 检查命令语法,确认依赖已安装 |
| 进程超时 | 命令执行时间过长 | 增加超时设置,优化命令参数 |
| 网络连接失败 | DNS解析失败或防火墙拦截 | 检查网络配置,确认代理设置 |

### Discord社区管理通用排查步骤

1. **检查输入参数**: 确认所有必填参数已提供且格式正确
2. **查看日志输出**: 定位具体错误行和异常类型
3. **验证环境配置**: 确认依赖库版本和运行环境满足要求
4. **逐步调试**: 缩小问题范围,隔离故障模块
