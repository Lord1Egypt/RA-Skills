---
name: alert-to-fault-handling
description: 告警自动处理工作流 - 监听告警上下文，匹配处理脚本，提示用户执行故障处理操作
---

# 告警自动处理工作流

## Overview

当检测到告警上下文时，根据群组和告警类型自动匹配对应的故障处理脚本，提示用户一键执行。

## 工作流程

```
告警上下文检测 → 群组识别 → 关键词匹配 → 脚本推荐 → 用户确认 → 执行脚本 → 反馈结果 → (可选)自动关闭告警
```

## 触发条件

当以下条件同时满足时触发：

1. **对话上下文存在告警信息**（包含 eventid、IP、告警名称中的至少一个）
2. **当前飞书群组**与告警分类匹配
3. **告警内容**匹配脚本关键词
4. **存在对应的预置脚本**

## 配置文件

### 脚本映射配置 (.scripts_map.json)

```json
{
  "nginx": {
    "name": "nginx服务重启",
    "script_id": 187,
    "keywords": ["nginx", "Nginx", "NGINX", "web", "80端口", "http服务"],
    "classifications": [102],
    "chat_groups": [""],
    "description": "重启Nginx服务，适用于服务停止、无响应等场景"
  },
  "disk": {
    "name": "主机磁盘空间清理",
    "script_id": 197,
    "keywords": ["磁盘", "disk", "空间", "storage", "/var", "/tmp", "使用率", "满"],
    "classifications": [101],
    "chat_groups": [""],
    "description": "清理日志文件和临时文件，释放磁盘空间"
  }
}
```

### 执行日志配置 (.execution_log.json)

```json
{
  "executions": [
    {
      "timestamp": "2026-03-10T09:50:00Z",
      "eventid": "32415666",
      "ip": "192.168.3.137",
      "script_id": 187,
      "script_name": "nginx服务重启",
      "status": "success",
      "execution_id": 970,
      "user": ""
    }
  ]
}
```

## 群组与分类映射

| 飞书群 ID | 群组名称 | 监控分类 | 默认脚本 |
|-----------|----------|----------|----------|
|  | 操作系统告警群 | 101 | 主机磁盘空间清理 (197) |
|  | 中间件告警群 | 102 | nginx服务重启 (187) |
|  | 网络设备告警群 | 103 | (待配置) |

## 用户交互

### 场景1: 自动推荐

```
🤖 检测到 Nginx 服务停止告警
📊 告警对象: 3.137-Nginx-1.14.2 (192.168.3.137)
🔑 告警ID: 32415666

💡 推荐操作: nginx服务重启 (脚本ID: 187)
📝 说明: 重启Nginx服务，适用于服务停止、无响应等场景

👉 回复「执行」或「确认」自动运行脚本
```

### 场景2: 用户指定脚本

```
用户: 执行脚本 197

🔧 正在为主机 192.168.3.137 执行脚本...
📋 脚本: 主机磁盘空间清理 (ID: 197)
⏳ 执行中...
```

### 场景3: 确认后执行

```
用户: 确认

🔧 提交执行任务...
✅ 任务已提交 (Execution ID: 970)
⏳ 等待执行结果...
```

## IP 获取规则

优先级从高到低：

1. **告警消息中的 IP 字段**（最优先）
2. **通过 objectid 查询主机详情获取 IP**
   ```bash
   ./scripts/lerwee-api.sh monitor host-view '{"hostid": 11131}'
   ```
3. **用户手动指定**

## 脚本执行

使用 fault-handling skill 执行脚本：

```bash
python3 /home/node/.openclaw/workspace/skills/fault-handling/run_script.py \
  --hosts '192.168.3.137' \
  --script-id 187
```

## 执行结果反馈

```
🔧 故障处理执行报告
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
任务名称：nginx服务重启
任务ID：970
执行状态：成功
执行耗时：15秒

📋 步骤执行详情
步骤              主机IP        主机名      状态    输出
nginx服务重启     192.168.3.137  vm-3-137   ✅     nginx: [  OK  ]

📌 执行结论
● ✅ 1台主机执行成功
● ❌ 0台主机执行失败

💾 已记录到执行日志
```

## 可选: 自动关闭告警

脚本执行成功后，可选自动关闭对应告警：

```bash
./scripts/lerwee-api.sh alert problem-ack '{
  "eventid": "32415666",
  "action": 1,
  "message": "脚本执行成功，自动关闭告警"
}'
```

## Hard Rules

- 执行脚本前必须获取用户明确确认（回复「执行」「确认」「yes」）
- 不能在没有主机 IP 的情况下猜测或使用占位 IP
- 执行失败时必须明确说明失败原因
- 所有执行必须记录到日志文件
- 自动关闭告警前必须确认脚本执行成功

## Files

- 配置: `.scripts_map.json` - 脚本映射配置
- 日志: `.execution_log.json` - 执行历史记录
- 主逻辑: 由 Agent 动态处理，无需独立脚本

## 扩展新脚本类型

在 `.scripts_map.json` 中添加新条目：

```json
{
  "mysql": {
    "name": "MySQL服务重启",
    "script_id": 198,
    "keywords": ["mysql", "MySQL", "数据库"],
    "classifications": [105],
    "chat_groups": ["oc_xxx"],
    "description": "重启MySQL服务"
  }
}
```

## 安全机制

1. **确认机制**: 默认脚本需用户确认，自定义脚本ID需二次确认
2. **白名单**: 只执行预置脚本或用户明确指定的脚本ID
3. **日志审计**: 所有操作记录到日志文件
4. **回滚支持**: 记录执行ID，支持查询历史结果
