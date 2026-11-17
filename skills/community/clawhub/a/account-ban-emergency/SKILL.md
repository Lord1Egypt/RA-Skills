---
name: account-ban-emergency
version: 1.0.0
description: 闲鱼封号专项应急预案(DEF-37)，7步应急流程：封号检测→自动暂停→客户通知→备用切换→商品恢复→封号申诉→事后分析。触发：unsent_retryer检测到account_banned/ban-detection-polling Cron检测到登录异常
tools: [read, exec]
dependencies: [account-manager]
metadata:
  layer: plugin
  priority: P0
  category: ecom-ops
  openclaw:
    emoji: "🚨"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      env: ["SILICONFLOW_API_KEY"]
      config:
        - mcp.servers.fishclaw-mcp
        - mcp.servers.xianyu-agent-mcp
---

# 闲鱼封号专项应急预案

**版本**: v1.0 | **优先级**: P0 | **状态**: 🟢 可用 | **来源**: DEF-37封号应急预案缺失

## 与cookie-manager紧急修复的区别

| 维度 | cookie-manager(紧急修复) | account-ban-emergency |
|:-----|:-----------------|:----------------------|
| 触发条件 | Cookie批量失效(≥2个) | 账号被封(不可逆) |
| 恢复方式 | 重新登录/扫码恢复(30分钟内) | 切换到备用账号(持续数天) |
| 影响范围 | 临时降级，Cookie恢复后复原 | 需要重新发布商品，重建客户关系 |
| 数据丢失 | 无 | 被封账号的商品/评价/粉丝不可恢复 |

## 使用场景

1. unsent_retryer检测到account_banned关键词→自动触发
2. ban-detection-polling Cron检测到登录异常→自动触发
3. 人工发现账号被封→手动触发
4. 多账号同时被封→分别处理，互不影响

## 工作流

### 主流程: 封号应急响应(7步)

1. **封号检测**
   - 接收封号事件: {account_id, platform, banned_reason, detected_at, detection_source}
   - 验证封号状态: 调用fishclaw-mcp check_cookie_validity确认
   - 记录封号信息到data/ban_events/{account_id}_{timestamp}.json
   - 执行: `python d:/JueJin/skills/account-ban-emergency/scripts/ban_handler.py --action detect --account-id {account_id} --reason "{banned_reason}"`

2. **自动暂停**
   - 暂停该账号的所有Cron发布任务
   - 暂停该账号的xianyu-auto-reply客服回复
   - 暂停该账号的auto-delivery自动发货
   - 记录暂停状态到data/ban_events/{account_id}_paused.json
   - 执行: `python d:/JueJin/skills/account-ban-emergency/scripts/ban_handler.py --action pause --account-id {account_id}`

3. **客户通知**
   - 通过QQBot发送封号告警给管理员
   - 告警内容: 封号账号/影响范围/当前状态/预计恢复时间
   - 告警模板: "🚨 闲鱼账号被封: {account_id}, 原因: {reason}, 已暂停该账号所有自动化操作。正在启动备用账号切换..."
   - 执行: `python d:/JueJin/scripts/notification.py send_alert --level CRITICAL --message "告警内容"`

4. **备用切换**
   - 激活account-manager执行账号切换
   - 选择备用账号: 从data/account_pool.json中选择健康度最高的备用账号
   - 切换间隔≥17分钟(来源:01手册§十10.1多账号发布间隔)
   - 更新tenant_cookie_map.json映射
   - 执行: `python d:/JueJin/skills/account-ban-emergency/scripts/ban_handler.py --action switch --account-id {account_id} --backup-account {backup_id}`

5. **商品恢复**
   - 在备用账号重新发布核心商品(优先级P0商品)
   - **R6-014修复说明**: exec脚本(action_republish)返回success:False+next_action=call_fishclaw_publish指引,**不直接调用MCP**(遵循R56层间依赖方向)。LLM编排器收到指引后调用fishclaw-mcp publish_item发布商品
   - 发布间隔≥17分钟(来源:01手册§十10.1)
   - 目标: 2小时内在备用账号重新发布核心商品
   - 执行: `python d:/JueJin/skills/account-ban-emergency/scripts/ban_handler.py --action republish --backup-account {backup_id}` → 返回REQUIRES_LLM_ORCHESTRATION → LLM编排调用fishclaw-mcp

6. **封号申诉**
   - 根据封号原因生成申诉建议(策略+文本+证据清单+成功率预估)
   - 记录申诉事件到data/ban_events/{account_id}_appeal_{timestamp}.json
   - **HL-009修复说明**: exec脚本(action_appeal)返回success:False+next_action=call_xianyu_appeal_channel指引,**不直接调用MCP**(遵循R56层间依赖方向)。LLM编排器收到指引后调用闲鱼申诉渠道(人工客服/API)
   - 申诉策略按封号原因分类: 导流→承认整改 / 刷单→举证否认 / 侵权→授权证明 / 骚扰→道歉承诺 / 频率→承认整改 / 其他→通用申诉
   - 执行: `python d:/JueJin/skills/account-ban-emergency/scripts/ban_handler.py --action appeal --account-id {account_id} [--reason "{banned_reason}"]` → 返回REQUIRES_LLM_ORCHESTRATION → LLM编排调用申诉渠道

7. **事后分析**
   - 记录封号原因+持续时间+影响范围
   - 分析风控策略是否需要调整
   - 更新MEMORY.md记录重大事件
   - 输出应急处理报告
   - 执行: `python d:/JueJin/skills/account-ban-emergency/scripts/ban_handler.py --action analyze --account-id {account_id}`

## 输入格式

```json
{
  "account_id": "account_1",
  "platform": "xianyu",
  "banned_reason": "违反用户协议",
  "detected_at": "2026-06-02T10:00:00",
  "detection_source": "unsent_retryer"
}
```

## 输出格式

```json
{
  "success": true,
  "data": {
    "banned_account": "account_1",
    "paused_services": ["cron-publish", "auto-reply", "auto-delivery"],
    "backup_account": "account_2",
    "republish_status": "in_progress",
    "republish_count": 5,
    "alert_sent": true,
    "analysis_report": "封号原因:违反用户协议,建议:降低发布频率"
  },
  "error": null,
  "code": null
}
```

## 异常处理

| 异常场景 | 处理方式 | code |
|:---------|:---------|:-----|
| 无备用账号可用 | CRITICAL告警+人工介入 | NO_BACKUP_ACCOUNT |
| 备用账号也被封 | 递归触发封号应急+升级告警 | BACKUP_ALSO_BANNED |
| fishclaw-mcp不可用 | 跳过商品恢复+记录待恢复列表 | MCP_UNAVAILABLE |
| 商品重新发布失败 | 重试3次+记录失败商品 | REPUBLISH_FAILED |
| 账号切换触发风控 | 立即停止+等待≥17分钟 | RATE_LIMITED |
| 申诉渠道不可用 | 记录待申诉+人工跟进 | APPEAL_CHANNEL_UNAVAILABLE |
| 申诉被拒 | 记录拒绝原因+升级人工 | APPEAL_REJECTED |

## 风控规则

| 规则 | 阈值 | 来源 |
|:-----|:-----|:-----|
| 封号后立即暂停所有操作 | 完全禁止 | 防止进一步触发风控 |
| 账号切换间隔 | ≥17分钟 | 01手册§十10.1多账号发布间隔 |
| 商品重新发布间隔 | ≥17分钟 | 01手册§十10.1 |
| 核心商品恢复时间 | ≤2小时 | 业务连续性保障 |
| 事后分析必做 | 封号后24小时内 | 风控策略持续改进 |
| 申诉发起时间 | 封号后≤1小时 | 提高申诉成功率 |
| 申诉策略匹配 | 6类封号原因分类 | 01手册§十风控规则 |

## 示例

**输入**: unsent_retryer检测到账号被封
```json
{
  "account_id": "account_1",
  "platform": "xianyu",
  "banned_reason": "违反用户协议",
  "detected_at": "2026-06-02T10:00:00",
  "detection_source": "unsent_retryer"
}
```

**输出**: 应急响应完成(暂停服务+切换备用账号+恢复商品)
```json
{
  "success": true,
  "data": {
    "banned_account": "account_1",
    "paused_services": ["cron-publish", "auto-reply", "auto-delivery"],
    "backup_account": "account_2",
    "republish_status": "completed",
    "republish_count": 5,
    "alert_sent": true,
    "analysis_report": "封号原因:违反用户协议,建议:降低发布频率至每账号≤3次/天"
  },
  "error": null,
  "code": null
}
```

**异常示例**: 无可用备用账号
```json
{
  "success": false,
  "data": {
    "banned_account": "account_1",
    "paused_services": ["cron-publish", "auto-reply", "auto-delivery"],
    "backup_account": null,
    "alert_sent": true
  },
  "error": "NO_BACKUP_ACCOUNT",
  "code": "NO_BACKUP_ACCOUNT"
}
```
