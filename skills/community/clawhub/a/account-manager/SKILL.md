---
name: account-manager
version: 1.1.0
description: 账号切换管理（封号换号），包括设备调度、好友迁移、账号状态管理、换号前好友筛选与通知。触发：封号检测/换号请求/风险预警
tools: [read, exec]
dependencies: [device-operations]

metadata:
  layer: plugin
  priority: P0
  category: "account-management"
  openclaw:
    emoji: "⚙️"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      config: ["mcp.servers.fishclaw-mcp", "mcp.servers.device-operations-mcp"]
      env: ["FISHCLAW_MCP_URL"]
---
# Account Manager Skill - 账号切换管理

**版本**: v1.1 | **优先级**: P0 | **状态**: 🟢 switch_account已实现 | **依赖MCP**: fishclaw-mcp, device-operations-mcp

> v1.1更新(2026-08-15): 实现switch_account动作(DEF-37增强),支持封号后账号切换+cookie映射更新+bound_accounts更新+迁移报告生成。exec脚本: `scripts/account_manager.py --action switch_account`

## 使用场景

1. 微信封号换号: 切换新号，继承好友档案和聊天记忆
2. 抖音封号换号: 切换新号，继承视频素材
3. 多平台同时封号: 分别处理，互不影响
4. 自动检测封号: 登录失败3次→触发封号预警
5. 封号后继续操作: 自动切换备用账号
6. 换号前好友筛选: 通过device-operations-mcp导出好友列表，按交互频率分类
7. 风险预警通知: 提前通知高价值好友备用联系方式

## 工作流

### 主流程：账号切换（封号换号）

1. **检测封号**: 接收封号通知(自动/手动)，验证封号状态，记录时间/原因/截图
2. **好友筛选**(P0关键步骤): 通过device-operations-mcp导出好友列表 → 按交互频率/标签自动分类(高价值/风险/低价值/普通)
3. **执行通知策略**: 高价值→1对1私信(换号前3-7天) / 普通→朋友圈公告 / 风险→通知CEO / 低价值→不通知
4. **标记旧账号banned**: 更新状态+执行`python skills/account-manager/scripts/save_account_status.py`持久化
5. **创建新账号档案**: 生成新account_id，绑定手机号，状态new
6. **执行设备登录**: 调用device-operations MCP，退出旧号→登录新号→验证
7. **数据迁移**: 通过device-operations-mcp导出/导入好友档案 + 聊天记忆(MEMORY.md)，不继承聊天记录/评价/粉丝
8. **更新配置**: 更新员工配置+设备配置+cron调度+通知CEO，执行save_account_status.py持久化
9. **完成切换**: 返回结果+记录日志+更新MEMORY.md

## 输入格式

```json
{"action": "switch_account", "agent_id": "agent_002", "platform": "wechat", "old_account": "wx_001", "new_account": "wx_002", "phone_number": "138****0002", "banned_reason": "频繁加人", "banned_date": "2026-04-15T10:30:00Z"}
```

> 完整输入/输出JSON格式、字段说明、错误码、测试用例、依赖关系详见 scripts/account_manager_reference.json

## 输出格式

```json
{
  "success": true,
  "data": {
    "action": "switch_account",
    "agent_id": "agent_002",
    "platform": "wechat",
    "old_account": {
      "account_id": "wx_001",
      "status": "banned",
      "banned_reason": "频繁加人",
      "banned_date": "2026-04-15T10:30:00Z"
    },
    "new_account": {
      "account_id": "wx_002",
      "status": "active",
      "phone_number": "138****0002",
      "login_status": "success"
    },
    "inherited_data": {
      "friends_count": 150,
      "memory_count": 5000,
      "tags_count": 12
    },
    "notification_sent": {
      "high_value": 8,
      "normal": 0,
      "risk": 2
    },
    "switched_at": "2026-04-15T11:00:00Z"
  },
  "error": null,
  "code": null
}
```

字段说明:
- `old_account.status`: 旧账号状态(banned/disabled)
- `new_account.status`: 新账号状态(active/login_failed)
- `inherited_data`: 数据迁移统计(好友数/记忆条数/标签数)
- `notification_sent`: 通知策略执行统计(高价值/普通/风险)
- `switched_at`: 切换完成时间(ISO 8601)

> 完整输出JSON格式详见 scripts/account_manager_reference.json

## 异常处理

| 异常 | 错误码 | 处理 |
|:-----|:-------|:-----|
| 旧账号不存在 | ACCOUNT_NOT_FOUND | 检查账号ID |
| 新账号已存在 | ACCOUNT_ALREADY_EXISTS | 使用其他ID |
| 设备登录失败 | DEVICE_LOGIN_FAILED | 重试或检查设备 |
| 数据迁移失败 | DATA_MIGRATION_FAILED | 部分迁移或手动 |
| 平台不支持 | PLATFORM_NOT_SUPPORTED | 添加平台支持 |
| MCP未连接 | MCP_NOT_CONNECTED | 检查配置重启Gateway |

> 完整8个错误码+返回示例详见 scripts/account_manager_reference.json

## 示例

### 微信封号换号

1. 输入: switch_account(agent_002, wechat, wx_001→wx_002, "频繁加人")
2. 好友筛选→通知策略→标记banned→创建新号→设备登录→数据迁移(继承好友150+记忆5000条)
3. 返回: `{success:true, old_account:{status:"banned"}, new_account:{status:"active"}, inherited_data:{friends_count:150}}`

> 更多示例(抖音换号/异常场景)和10个测试用例详见 scripts/account_manager_reference.json

## 变更历史

| 版本 | 日期 | 变更说明 |
|:-----|:-----|:---------|
| v1.0 | 2026-04-15 | 初始版本 |
