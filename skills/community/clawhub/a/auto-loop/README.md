# Auto Loop

自动循环技能，提供定时触发、任务调度、状态追踪和自动恢复功能。

## 功能特性

### 1. 定时触发 (Scheduled Trigger)
- Cron 表达式支持
- 固定间隔执行
- 一次性定时执行
- 手动触发模式

### 2. 任务调度 (Task Scheduling)
- 优先级队列
- 并发控制
- 任务依赖 (可扩展)
- 动态添加/移除

### 3. 状态追踪 (State Tracking)
- 任务状态管理
- 执行历史记录
- 成功/失败统计
- 状态持久化

### 4. 自动恢复 (Auto Recovery)
- 失败重试
- 指数退避
- 恢复尝试限制
- 失败记录管理

## 安装

```bash
# 技能已内置，无需额外安装
```

## 使用方法

### 基本使用

```javascript
const { AutoLoop } = require('./skills/auto-loop/src/index.js');

// 创建实例
const autoLoop = new AutoLoop();

// 添加间隔任务
autoLoop.interval('backup', 3600000, async (context, task) => {
    console.log('执行备份...');
    // 备份逻辑
    return { success: true };
});

// 添加 cron 任务
autoLoop.schedule('daily-report', '0 9 * * *', async () => {
    console.log('生成日报...');
});

// 启动调度器
autoLoop.start();
```

### 任务管理

```javascript
// 列出任务
const tasks = autoLoop.listTasks();

// 获取任务
const task = autoLoop.getTask('backup');

// 移除任务
autoLoop.unschedule('backup');

// 暂停/恢复
task.pause();
task.resume();

// 取消任务
task.cancel();
```

## CLI 使用

```bash
# 列出任务
node skills/auto-loop/src/index.js list

# 查看统计
node skills/auto-loop/src/index.js stats

# 运行演示
node skills/auto-loop/src/index.js demo

# 运行测试
node skills/auto-loop/src/index.js test
```

## Cron 表达式格式

```
* * * * *
│ │ │ │ │
│ │ │ │ └─ 星期 (0-6)
│ │ │ └─── 月份 (1-12)
│ │ └───── 日期 (1-31)
│ └─────── 小时 (0-23)
└───────── 分钟 (0-59)
```

### 示例

- `*/5 * * * *` - 每 5 分钟
- `0 * * * *` - 每小时
- `0 9 * * *` - 每天早上 9 点
- `0 0 * * 0` - 每周日凌晨
- `0 0 1 * *` - 每月 1 日凌晨

## API 参考

### AutoLoop

- `schedule(name, cron, handler, options)`: 添加 cron 任务
- `interval(name, ms, handler, options)`: 添加间隔任务
- `once(name, date, handler, options)`: 添加一次性任务
- `unschedule(taskId)`: 移除任务
- `getTask(taskId)`: 获取任务
- `listTasks(options)`: 列出任务
- `start()`: 启动调度器
- `stop()`: 停止调度器
- `getStats()`: 获取统计
- `getFailedTasks()`: 获取失败任务
- `clearFailures(taskId)`: 清除失败记录

### Task

- `execute(context)`: 执行任务
- `pause()`: 暂停
- `resume()`: 恢复
- `cancel()`: 取消

## 配置

```javascript
const CONFIG = {
    DEFAULT_RETRIES: 3,
    DEFAULT_RETRY_DELAY: 5000,
    DEFAULT_TIMEOUT: 300000,
    MAX_CONCURRENT: 5,
    HISTORY_RETENTION: 86400000
};
```

## 任务状态

- `pending`: 等待执行
- `scheduled`: 已调度
- `running`: 执行中
- `completed`: 已完成
- `failed`: 失败
- `retrying`: 重试中
- `cancelled`: 已取消
- `paused`: 已暂停

## 最佳实践

1. 为重要任务设置适当的重试次数
2. 使用有意义的任务名称
3. 监控失败任务并及时处理
4. 定期清理历史数据
5. 合理设置并发限制

## 依赖

- Node.js 内置模块

## 许可证

MIT
