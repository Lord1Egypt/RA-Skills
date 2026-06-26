---
name: feishu-process-feedback
description: |
  飞书消息自动处理与进度反馈技能。安装后后台运行，监听飞书任务消息并自动创建独立进程处理。
  在处理前后发送实时进度反馈（任务确认、进度百分比、完成通知）。
  支持任务类型识别、智能解析、错误重试、并发控制、状态持久化。
  使用场景：飞书自动化工作流、任务进度追踪、批量任务处理、需要实时反馈的场景。
---

# 飞书进程反馈技能

实时任务处理进度反馈系统，为飞书任务提供完整的状态追踪。

## 核心功能

### 1. 自动后台监听
- 持续运行，轮询监听飞书新消息
- 智能识别任务消息（关键词：帮我、处理、创建、生成、分析等）
- 状态持久化，重启后继续处理

### 2. 即时确认反馈
- 收到任务后 5 秒内回复确认消息
- 包含任务 ID、类型识别、子任务数量
- 显示当前队列状态

### 3. 进度实时追踪
- 每个子任务处理前后发送进度更新
- 百分比格式（33%、66%、100%）
- 支持成功/失败状态标记

### 4. 进程隔离管理
- 每个任务独立 Node.js 进程
- 并发控制（默认最多 5 个并发）
- 超时自动终止（默认 5 分钟）
- 优雅关闭处理

### 5. 错误容错处理
- 自动重试机制（默认 3 次）
- 错误日志记录
- 失败任务标记通知

## 工作流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 飞书消息    │ →  │ 任务识别    │ →  │ 创建进程    │
└─────────────┘    └─────────────┘    └─────────────┘
                                              ↓
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 完成通知    │ ←  │ 进度反馈    │ ←  │ 发送确认    │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 安装方式

### 本地安装

```bash
# 克隆或复制技能到本地
git clone <repo-url> ~/.openclaw/skills/feishu-process-feedback

# 或使用 clawhub（发布后）
clawhub install feishu-process-feedback
```

### 启动服务

```bash
cd ~/.openclaw/skills/feishu-process-feedback
node scripts/listener.js
```

### 后台运行（推荐）

```bash
# Windows (PowerShell)
Start-Process node -ArgumentList "scripts/listener.js" -WindowStyle Hidden

# Linux/Mac (systemd 或 screen)
screen -dmS feishu-listener node scripts/listener.js
```

## 配置选项

通过环境变量配置：

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `FEISHU_POLL_INTERVAL` | 轮询间隔（毫秒） | 5000 |
| `FEISHU_MAX_RETRIES` | 最大重试次数 | 3 |
| `FEISHU_RETRY_DELAY` | 重试延迟（毫秒） | 1000 |
| `FEISHU_MAX_CONCURRENT` | 最大并发进程数 | 5 |
| `FEISHU_PROCESS_TIMEOUT` | 进程超时（毫秒） | 300000 |
| `FEISHU_TASK_DELAY` | 子任务处理延迟（毫秒） | 500 |
| `FEISHU_VERBOSE` | 启用详细日志 | false |

示例：

```bash
export FEISHU_POLL_INTERVAL=3000
export FEISHU_MAX_CONCURRENT=10
export FEISHU_VERBOSE=true
node scripts/listener.js
```

## 反馈格式

### 任务确认
```
📋 任务收到，开始处理...
任务 ID: #1
类型：🛠️ create
共 3 个子任务
主任务：帮我创建一个 Excel 数据表...
当前队列：1 个任务
```

### 进度更新
```
⏳ 进度 33% - 正在处理：设计表格结构...
✅ 完成 33% - 设计表格结构...
```

### 完成通知
```
🎉 任务完成！
任务 ID: #1
状态：全部完成
成功：3 | 失败：0
耗时：2.45 秒
进度：100%
```

### 错误处理
```
⚠️ 失败 66% - 生成报告：API 超时
❌ 任务处理失败
任务 ID: #1
错误：网络连接失败
请联系管理员或重试
```

## 任务类型识别

自动识别任务类型并采用相应处理策略：

| 类型 | 关键词 | 图标 | 处理策略 |
|------|--------|------|----------|
| create | 创建、build、create | 🛠️ | 设计→创建→验证 |
| analyze | 分析、analyze | 🔍 | 收集→分析→结论 |
| calculate | 计算、calculate | 🧮 | 准备→计算→验证 |
| query | 查询、search、find | 🔎 | 构建→搜索→整理 |
| simple | 其他 | ⚙️ | 直接处理 |

## 日志文件

技能运行产生以下日志文件：

- `.listener.log` - 监听器日志
- `.tasks.log` - 任务处理日志
- `.listener_state.json` - 状态持久化文件

位置：`~/.openclaw/skills/feishu-process-feedback/`

## 状态查看

监听器每 5 分钟自动输出状态：

```
==================================================
📊 FeishuListener 状态
==================================================
运行时间：2h 15m 30s
活跃进程：2/5
总任务数：47
最后消息：om_xxx
轮询间隔：5000ms
==================================================
```

## 优雅关闭

支持 SIGINT/SIGTERM 信号：

```bash
# 发送终止信号
kill -SIGTERM <pid>

# 或 Ctrl+C（前台运行时）
```

关闭时会：
1. 停止接收新任务
2. 等待当前任务完成（最多 30 秒）
3. 保存状态
4. 发送通知消息

## 扩展开发

### 添加自定义任务处理器

编辑 `scripts/process_task.js` 中的 `executeSubtask()` 函数：

```javascript
async function executeSubtask(subtask, index, total) {
  // 根据任务类型调用不同处理器
  if (subtask.includes('Excel')) {
    return await handleExcelTask(subtask);
  } else if (subtask.includes('分析')) {
    return await handleAnalysisTask(subtask);
  }
  // ...
}
```

### 集成飞书 API

在 `scripts/listener.js` 的 `getLatestMessage()` 中集成飞书开放平台 API：

```javascript
async function getLatestMessage() {
  const response = await fetch('https://open.feishu.cn/open-apis/im/v1/messages', {
    headers: { 'Authorization': `Bearer ${ACCESS_TOKEN}` }
  });
  return await response.json();
}
```

## 故障排查

### 监听器未启动

```bash
# 检查 Node.js 版本
node --version  # 需要 v14+

# 检查依赖
ls -la scripts/

# 手动启动测试
node scripts/listener.js
```

### 消息未发送

1. 检查 OpenClaw 飞书通道配置
2. 查看 `.listener.log` 错误信息
3. 测试手动发送：`openclaw message send --channel feishu --message "test"`

### 任务处理超时

- 增加超时时间：`export FEISHU_PROCESS_TIMEOUT=600000`
- 减少并发数：`export FEISHU_MAX_CONCURRENT=3`
- 查看详细日志：`export FEISHU_VERBOSE=true`

## 依赖

- Node.js v14+
- OpenClaw 飞书通道
- 飞书应用权限（im:message）

## 版本历史

### v1.0.0 (2026-03-10)
- 初始版本
- 基础监听和反馈功能
- 任务类型识别
- 错误重试机制
- 状态持久化

## 许可证

MIT License

## 作者

Carl Zhao

## 支持

遇到问题？
- 查看日志文件：`.listener.log` 和 `.tasks.log`
- 提交 Issue 到项目仓库
- 联系 OpenClaw 社区
