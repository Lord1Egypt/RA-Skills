# 测试执行管理模块使用指南

## 📖 概述

测试执行管理模块提供企业级的测试执行资源管理：
- 执行器管理（API/UI测试机）
- 任务队列调度（优先级队列）
- 智能任务分配
- 执行器监控（心跳、状态）
- 执行统计与分析

## 🚀 快速开始

### 1. 创建执行器

**创建API测试执行器：**

```bash
POST http://localhost:8000/api/execution/executor

{
  "name": "api-executor-1",
  "type": "api",
  "capacity": 5,
  "max_tasks": 100,
  "config": {
    "environment": "dev",
    "base_url": "http://localhost:8000"
  }
}
```

**创建UI测试执行器：**

```bash
POST http://localhost:8000/api/execution/executor

{
  "name": "ui-executor-1",
  "type": "ui",
  "capacity": 3,
  "max_tasks": 50,
  "config": {
    "browser": "chromium",
    "headless": true,
    "viewport": {
      "width": 1920,
      "height": 1080
    }
  }
}
```

### 2. 查看执行器列表

```bash
GET http://localhost:8000/api/execution/executor/list?type=api
```

**响应示例：**

```json
{
  "code": 200,
  "msg": "查询成功",
  "data": [
    {
      "id": 1,
      "name": "api-executor-1",
      "type": "api",
      "status": "idle",
      "capacity": 5,
      "current_load": 0,
      "max_tasks": 100,
      "completed_tasks": 0,
      "last_heartbeat": null,
      "create_time": "2026-03-23 10:00:00"
    }
  ]
}
```

### 3. 调度测试任务

**立即执行：**

```bash
POST http://localhost:8000/api/execution/task/schedule
Authorization: Bearer your_auth_code

{
  "script_id": 1,
  "script_type": "api",
  "priority": 5,
  "max_retries": 2,
  "config": {
    "environment": "dev"
  }
}
```

**定时执行：**

```bash
POST http://localhost:8000/api/execution/task/schedule

{
  "script_id": 2,
  "script_type": "ui",
  "priority": 3,
  "scheduled_time": "2026-03-24T02:00:00",
  "max_retries": 2
}
```

**优先级说明：**
- 1-3：高优先级（紧急任务）
- 4-6：中优先级（正常任务）
- 7-10：低优先级（后台任务）

### 4. 获取执行统计

```bash
GET http://localhost:8000/api/execution/stats
```

**响应示例：**

```json
{
  "code": 200,
  "msg": "查询成功",
  "data": {
    "total_executors": 2,
    "active_executors": 2,
    "idle_executors": 1,
    "busy_executors": 1,
    "offline_executors": 0,
    "total_tasks": 15,
    "pending_tasks": 5,
    "running_tasks": 2,
    "completed_tasks": 8,
    "failed_tasks": 0
  }
}
```

### 5. 查看任务列表

```bash
GET http://localhost:8000/api/execution/task/list?status=running&limit=50
```

### 6. 取消任务

```bash
POST http://localhost:8000/api/execution/task/cancel

{
  "task_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 7. 执行器心跳

执行器需要定期发送心跳以保持活跃状态：

```bash
POST http://localhost:8000/api/execution/executor/1/heartbeat?current_load=2
```

**说明：**
- `current_load`: 当前正在执行的任务数
- 心跳间隔建议：10-60秒
- 如果心跳超时，执行器会被标记为离线

### 8. 自动调度

系统会自动将待执行任务分配给空闲执行器：

```bash
POST http://localhost:8000/api/execution/auto-schedule
```

**响应：**
```json
{
  "code": 200,
  "msg": "自动调度完成，分配了3个任务",
  "data": {"scheduled_count": 3}
}
```

### 9. 清理过期任务

```bash
POST http://localhost:8000/api/execution/cleanup?hours=24
```

## 🔧 核心概念

### 执行器状态

| 状态 | 描述 | 行为 |
|------|------|------|
| `idle` | 空闲 | 可以接收新任务 |
| `busy` | 忙碌 | 已达到容量上限 |
| `offline` | 离线 | 不接收任务 |

### 任务状态

| 状态 | 描述 | 转换条件 |
|------|------|----------|
| `pending` | 等待执行 | → running（分配给执行器） |
| `running` | 执行中 | → completed（成功）或failed（失败） |
| `completed` | 已完成 | 最终状态 |
| `failed` | 失败 | 最终状态 |

### 调度规则

1. **优先级优先**：优先执行优先级高的任务
2. **类型匹配**：API任务分配给API执行器，UI任务分配给UI执行器
3. **容量限制**：执行器负载不能超过容量
4. **重试机制**：失败任务自动重试（最多2次）

## 💡 使用场景

### 场景1：CI/CD集成

```bash
# 构建完成后，回归测试
# 1. 调度套件中的所有API测试脚本
for script_id in 1 2 3 4 5; do
    # 使用高优先级（立即执行）
    curl -X POST "http://localhost:8000/api/execution/task/schedule" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"script_id\": $script_id,
            \"script_type\": \"api\",
            \"priority\": 1
        }"
done

# 2. 等待所有任务完成
sleep 300

# 3. 查看执行统计
curl http://localhost:8000/api/execution/stats
```

### 场景2：定时任务

```bash
# 每天凌晨2点执行全量回归测试
# 使用Cron或Jenkins配置
# 调度时设置scheduled_time为次日凌晨2点
```

### 场景3：负载均衡

```bash
# 创建多个执行器
curl -X POST "http://localhost:8000/api/execution/executor" \
    -d '{
        "name": "api-executor-1",
        "type": "api",
        "capacity": 5
    }'

curl -X POST "http://localhost:8000/api/execution/executor" \
    -d '{
        "name": "api-executor-2",
        "type": "api",
        "capacity": 5
    }'

# 调度任务会自动分配到负载较轻的执行器
```

## 📊 监控指标

### 关键指标

1. **执行器利用率**
   - 理想值：70-90%
   - 过低：资源浪费
   - 过高：可能影响性能

2. **任务队列长度**
   - 理想值：<50
   - 过高：需要增加执行器

3. **任务完成率**
   - 理想值：>95%
   - 过低：需要优化脚本或执行器

4. **平均执行时间**
   - 用于评估性能趋势

## 🚨 故障排查

### 执行器离线

**可能原因：**
1. 网络断开
2. 心跳超时
3. 服务崩溃

**解决方法：**
1. 检查网络连接
2. 检查服务状态
3. 重启执行器服务

### 任务堆积

**可能原因：**
1. 执行器容量不足
2. 执行器离线
3. 任务调度失败

**解决方法：**
1. 增加执行器数量
2. 检查执行器状态
3. 手动调用`/auto-schedule`

### 任务执行超时

**可能原因：**
1. 脚本逻辑错误
2. 资源不足
3. 网络延迟

**解决方法：**
1. 检查执行日志
2. 增加超时时间
3. 优化脚本性能

## 🔄 完整工作流程

```
创建执行器 → 心跳保持活跃
      ↓
调度任务 → 进入队列
      ↓
自动调度 → 分配给空闲执行器
      ↓
执行任务 → 更新进度
      ↓
完成任务 → 更新执行器状态
      ↓
生成报告 → AI分析（可选）
```

## 📖 相关文档

- **使用指南**：`docs/EXECUTION_GUIDE.md`
- **API文档**：http://localhost:8000/docs
- **执行统计API**：`/api/execution/stats`

---

**版本：** v1.0.0
**更新时间：** 2026-03-23
