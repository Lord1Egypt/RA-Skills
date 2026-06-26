# 错误分类与处理策略

## 错误分类体系

### L1: 工具调用错误

| 错误类型 | 示例 | 处理策略 |
|---------|------|---------|
| **认证失败** | 401 Unauthorized | 检查 API Key/Token，提示更新 |
| **权限不足** | 403 Forbidden | 检查权限配置，申请授权 |
| **资源不存在** | 404 Not Found | 验证 ID/路径，检查拼写 |
| **限流** | 429 Too Many Requests | 指数退避重试，检查配额 |
| **服务器错误** | 5xx | 重试或等待，记录到日志 |
| **超时** | Timeout | 增加超时或优化请求 |
| **参数错误** | Invalid parameters | 修正参数格式 |

### L2: 工作流错误

| 错误类型 | 示例 | 处理策略 |
|---------|------|---------|
| **Cron 失败** | 任务未执行/执行报错 | 检查 schedule/payload/sessionTarget |
| **子 Agent 异常** | spawn 失败/超时 | 检查参数/资源/权限 |
| **消息发送失败** | 投递失败/格式错误 | 检查 channel/target/format |
| **会话中断** | Session 丢失 | 重建会话，恢复上下文 |

### L3: 系统错误

| 错误类型 | 示例 | 处理策略 |
|---------|------|---------|
| **内存不足** | OOM Killer | 减少并发，使用轻量模式 |
| **磁盘满** | No space left | 清理临时文件，清理旧日志 |
| **网络断开** | Connection refused | 检查网络，重试或降级 |
| **配置损坏** | 解析错误 | 从备份恢复，检查语法 |

## 诊断决策树

```
错误发生
│
├─ 是工具调用错误？
│   ├─ 认证问题 → 检查凭证
│   ├─ 权限问题 → 检查授权
│   ├─ 限流问题 → 退避重试
│   └─ 参数问题 → 修正格式
│
├─ 是工作流错误？
│   ├─ Cron 问题 → 检查 job 配置
│   ├─ 子 Agent 问题 → 检查 spawn 参数
│   └─ 消息问题 → 检查 channel 配置
│
└─ 是系统错误？
    ├─ 资源问题 → 释放资源
    └─ 配置问题 → 恢复备份
```

## 常见错误模式库

### Cron 相关

#### 错误：sessionTarget 与 payload.kind 不匹配
```
症状: "sessionTarget='main' requires payload.kind='systemEvent'"
修复: 
  - main → systemEvent
  - isolated/current → agentTurn
```

#### 错误：Cron 任务超时
```
症状: "Task timed out after X seconds"
修复:
  - 增加 payload.timeoutSeconds
  - 优化任务内容，减少复杂度
  - 使用子 Agent 处理重型任务
```

#### 错误：Cron 未触发
```
症状: 任务到时间未执行
诊断:
  1. cron list 检查 enabled 状态
  2. 检查 schedule 表达式
  3. 检查 timezone 配置
  4. 检查 Gateway 运行状态
```

### 飞书相关

#### 错误：权限不足
```
症状: "Permission denied" 或 "insufficient scope"
修复:
  1. feishu_app_scopes 检查当前权限
  2. 确认所需 scope
  3. 在飞书开放平台申请额外权限
```

#### 错误：Token 过期
```
症状: "Token expired" 或 "Invalid token"
修复:
  1. 刷新访问令牌
  2. 检查 token 刷新机制
  3. 重新认证
```

### 网络相关

#### 错误：连接超时
```
症状: "Connection timeout"
诊断:
  1. ping 测试目标主机
  2. 检查 DNS 解析
  3. 检查防火墙规则
  4. 尝试备用端点
```

## 自动修复规则

### 可自动修复
- ✅ Cron 任务 disabled → 重新启用
- ✅ 临时文件清理
- ✅ 重试限流错误（最多 3 次）
- ✅ 更新心跳状态文件

### 需确认后修复
- ⚠️ 修改 Cron 配置
- ⚠️ 重启服务
- ⚠️ 修改系统配置
- ⚠️ 删除大量数据

### 不可自动修复
- ❌ 修改核心身份文件
- ❌ 发送外部消息（邮件、飞书）
- ❌ 删除不可恢复的数据
- ❌ 安装新软件/依赖
