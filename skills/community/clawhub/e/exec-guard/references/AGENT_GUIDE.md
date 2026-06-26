# exec-guard - AI Agent 能力指南

本文档面向 AI Agent，介绍 exec-guard 提供的能力、使用场景和最佳实践。

---

## exec-guard 是什么？

exec-guard 是一个**安全的命令执行服务**，让 AI Agent 能够：

1. **执行系统命令** - 运行 shell 命令并获取结果
2. **管理后台进程** - 启动、监控、终止长时间运行的任务
3. **多 Agent 共享** - 多个 Agent 实例可以共享同一个服务，查看彼此启动的进程

---

## 核心能力

### 1. 同步命令执行

执行命令并等待结果返回。

**适用场景**：
- 查看文件列表：`ls -la`
- 读取文件内容：`cat file.txt`
- 运行测试：`npm test`
- 编译代码：`go build`
- Git 操作：`git status`

**示例请求**：
```json
{
  "command": "ls -la",
  "timeoutSeconds": 10
}
```

**响应**：
```json
{
  "status": "success",
  "exitCode": 0,
  "stdout": "total 32\ndrwxr-xr-x  5 user  ...",
  "stderr": "",
  "systemMessage": "command executed successfully"
}
```

---

### 2. 后台进程执行

启动长时间运行的任务，立即返回 PID，后续可查询状态和日志。

**适用场景**：
- 训练机器学习模型：`python train.py`
- 运行开发服务器：`npm run dev`
- 执行耗时脚本：`./long_running_task.sh`
- 数据处理任务：`node process_data.js`

**示例请求**：
```json
{
  "command": "python train.py",
  "runInBackground": true
}
```

**响应**：
```json
{
  "status": "running",
  "exitCode": -1,
  "stdout": "",
  "stderr": "",
  "systemMessage": "process started with PID 12345"
}
```

**后续操作**：
- 查询状态：`GET /process/12345`
- 获取日志：`GET /process/12345/logs`
- 终止进程：`DELETE /process/12345`

---

### 3. 监控窗口模式

启动后台进程后，等待 N 秒观察是否成功启动。

**适用场景**：
- 启动 Web 服务器，确认是否成功监听端口
- 启动数据库服务，确认是否成功启动
- 启动 Java 应用，捕获启动错误

**示例请求**：
```json
{
  "command": "java -jar app.jar",
  "runInBackground": true,
  "watchDurationSeconds": 5
}
```

**可能的结果**：

| 情况 | 响应 |
|------|------|
| 5 秒内进程退出 | `status: "failed"` + 退出码 + 错误日志 |
| 5 秒后仍在运行 | `status: "running"` + 初始化日志 |

**优势**：可以立即发现启动失败的问题，而不是等到用户报告才发现。

---

### 4. 多 Agent 共享

多个 Agent 实例连接同一个 exec-guard 服务，可以：
- 查看所有正在运行的进程
- 查看其他 Agent 启动的任务
- 终止失控的进程

**示例**：
```bash
# Agent A 启动训练任务
POST /exec {"command": "python train.py", "runInBackground": true}
# 返回 PID 12345

# Agent B 查看所有进程
GET /processes
# 可以看到 PID 12345 正在运行

# Agent B 查看训练日志
GET /process/12345/logs
# 获取训练进度

# Agent B 终止训练任务
DELETE /process/12345
```

---

## 何时使用 exec-guard

### ✅ 应该使用的场景

| 场景 | 原因 |
|------|------|
| 需要执行系统命令 | exec-guard 提供安全的命令执行环境 |
| 命令可能运行很久 | 后台模式 + 超时控制，防止资源占用 |
| 命令输出可能很大 | Head-Tail 缓冲，防止内存溢出 |
| 需要启动服务并确认成功 | 监控窗口模式，捕获启动错误 |
| 多个 Agent 需要协作 | HTTP 服务支持多 Agent 共享进程状态 |
| 不确定命令是否安全 | 超时控制 + 进程终止，可随时中断 |

### ❌ 不应该使用的场景

| 场景 | 替代方案 |
|------|----------|
| 简单的文件读写 | 直接使用文件系统 API |
| 需要实时交互的命令 | 使用 PTY 终端模拟 |
| 需要 sudo 权限的命令 | 配置 sudoers 或使用其他方案 |

---

## API 快速参考

### 执行命令

```
POST /exec
Content-Type: application/json

{
  "command": "string, required",
  "workingDir": "string, optional",
  "timeoutSeconds": "number, optional, default 30",
  "runInBackground": "boolean, optional, default false",
  "watchDurationSeconds": "number, optional",
  "env": {"KEY": "value"}
}
```

### 查询进程状态

```
GET /process/:pid
```

### 获取进程日志

```
GET /process/:pid/logs
```

### 终止进程

```
DELETE /process/:pid
```

### 列出所有进程

```
GET /processes
```

### 健康检查

```
GET /health
```

---

## 响应状态说明

| status | 含义 | 后续操作 |
|--------|------|----------|
| `success` | 命令成功完成 | 无需后续操作 |
| `failed` | 命令执行失败 | 检查 stderr 了解错误原因 |
| `timeout` | 命令超时被终止 | 考虑增加 timeoutSeconds 或优化命令 |
| `killed` | 进程被手动终止 | 正常情况，无需处理 |
| `running` | 进程正在后台运行 | 可通过 /process/:pid 查询状态 |

---

## 最佳实践

### 1. 始终设置合理的超时

```json
{
  "command": "npm install",
  "timeoutSeconds": 300
}
```

**原因**：防止命令无限执行占用资源。

### 2. 启动服务时使用监控窗口

```json
{
  "command": "npm run dev",
  "runInBackground": true,
  "watchDurationSeconds": 5
}
```

**原因**：可以立即发现启动失败，而不是等到用户报告。

### 3. 长时间任务使用后台模式

```json
{
  "command": "python train.py --epochs 100",
  "runInBackground": true,
  "timeoutSeconds": 86400
}
```

**原因**：训练可能需要数小时，后台模式让 Agent 可以继续处理其他请求。

### 4. 定期检查后台进程状态

```
GET /processes
```

**原因**：了解系统资源使用情况，及时发现异常进程。

### 5. 任务完成后清理进程

```
DELETE /process/:pid
```

**原因**：释放资源，保持系统整洁。

---

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `command cannot be empty` | 未提供 command 参数 | 检查请求参数 |
| `process not found` | PID 不存在或进程已结束 | 使用 /processes 查看有效 PID |
| `execution timeout exceeded` | 命令执行超时 | 增加 timeoutSeconds 或优化命令 |
| `invalid working directory` | 工作目录不存在 | 检查路径是否正确 |
| `max process limit reached` | 后台进程数达到上限 | 终止不需要的进程 |

### 错误响应格式

```json
{
  "error": "process not found"
}
```

---

## 示例场景

### 场景 1：编译并运行项目

```json
// 1. 安装依赖
POST /exec {"command": "npm install", "timeoutSeconds": 120}

// 2. 编译项目
POST /exec {"command": "npm run build", "timeoutSeconds": 60}

// 3. 运行测试
POST /exec {"command": "npm test", "timeoutSeconds": 60}
```

### 场景 2：启动开发服务器

```json
// 启动服务器并确认成功
POST /exec {
  "command": "npm run dev",
  "runInBackground": true,
  "watchDurationSeconds": 5
}

// 如果返回 running，说明启动成功
// 后续可以查看日志
GET /process/12345/logs
```

### 场景 3：训练机器学习模型

```json
// 启动训练
POST /exec {
  "command": "python train.py --epochs 100",
  "runInBackground": true,
  "timeoutSeconds": 86400
}

// 定期检查进度
GET /process/12345/logs

// 训练完成后终止
DELETE /process/12345
```

### 场景 4：多 Agent 协作

```json
// Agent A: 启动数据预处理
POST /exec {"command": "node preprocess.js", "runInBackground": true}
// 返回 PID 11111

// Agent B: 查看预处理进度
GET /process/11111/logs

// Agent A: 预处理完成后启动训练
POST /exec {"command": "python train.py", "runInBackground": true}
// 返回 PID 22222

// Agent B: 查看所有任务
GET /processes
// 返回 [PID 11111, PID 22222]
```

---

## 启动服务

### 方式 1：直接运行

```bash
node dist/index.js --server --port 8080
```

### 方式 2：使用 PM2（生产环境推荐）

```bash
pm2 start dist/index.js --name exec-guard -- --server --port 8080
```

### 方式 3：使用 Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY dist ./dist
EXPOSE 8080
CMD ["node", "dist/index.js", "--server", "--port", "8080"]
```

---

## 总结

exec-guard 为 AI Agent 提供：

| 能力 | 价值 |
|------|------|
| 安全的命令执行 | 超时控制、内存保护，防止系统崩溃 |
| 后台进程管理 | 支持长时间任务，可查询状态和日志 |
| 监控窗口模式 | 立即发现启动失败，提升可靠性 |
| 多 Agent 共享 | 多个 Agent 协作，共享进程状态 |
| 跨平台兼容 | Windows/Linux/macOS 统一接口 |

**一句话总结**：exec-guard 让 AI Agent 能够安全、可靠地执行系统命令，管理后台进程，并支持多 Agent 协作。