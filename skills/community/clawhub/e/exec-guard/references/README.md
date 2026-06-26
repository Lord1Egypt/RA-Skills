# exec-guard - AI Agent Command Execution Module (TypeScript)

[中文文档](#中文文档)

## Overview

**exec-guard** is an infrastructure module that provides safe and reliable system command execution capabilities for AI Agents. It addresses the core challenges AI Agents face when executing system commands:

- **Timeout Control**: Prevents resource occupation from infinite command execution
- **Memory Protection**: Prevents memory overflow from large outputs (Head-Tail Ring Buffer)
- **Process Management**: Supports background process startup, monitoring, and termination
- **Cross-Platform Compatibility**: Unified interface for Windows/Linux/macOS

This is the TypeScript/Node.js implementation of the original [Go version](https://github.com/cypress927/exec-guard).

---

## Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| Synchronous Execution | Execute commands and wait for results with timeout control |
| Background Execution | Start background processes with status query and log retrieval |
| Watch Window | Observe for N seconds after background startup to determine success |
| Dual-End Buffer | Head-Tail ring buffer, max 8KB, prevents OOM |
| Environment Variables | Inherits host environment variables with custom overrides |
| Process Group Management | Terminates all child processes when killing a process |

### Running Modes

- **CLI Mode**: Reads JSON requests from stdin, outputs JSON responses
- **HTTP Service Mode**: Provides RESTful API for remote invocation and multi-agent sharing

---

## Installation & Build

### Requirements

- Node.js 18+
- npm or yarn

### Installation

```bash
npm install
```

### Build

```bash
npm run build
```

### Run Tests

```bash
npm test
```

---

## Usage

### CLI Mode

Reads JSON requests from stdin, executes commands and outputs JSON responses:

```bash
# Basic usage
echo '{"command": "echo hello"}' | node dist/index.js

# With timeout
echo '{"command": "sleep 5", "timeoutSeconds": 3}' | node dist/index.js

# Background execution
echo '{"command": "long_task", "runInBackground": true}' | node dist/index.js

# Custom environment variables
echo '{"command": "node app.js", "env": {"NODE_ENV": "production"}}' | node dist/index.js
```

### HTTP Service Mode

Starts an HTTP server providing RESTful API:

```bash
# Default port 8080
node dist/index.js --server

# Custom port
node dist/index.js --server --port 9000

# Limit max background processes
node dist/index.js --server --port 8080 --max-processes 50
```

---

## API Documentation

### Execute Command

**POST** `/exec`

Executes system commands, supporting both synchronous and background modes.

#### Request Parameters

```json
{
  "command": "string, required - system command to execute",
  "workingDir": "string, optional - working directory, defaults to current directory",
  "timeoutSeconds": "number, optional - timeout in seconds, default 30",
  "runInBackground": "boolean, optional - run in background, default false",
  "watchDurationSeconds": "number, optional - watch window duration in seconds, background mode only",
  "env": "object, optional - custom environment variables"
}
```

#### Response Structure

```json
{
  "status": "string - success/failed/timeout/killed/running",
  "exitCode": "number - process exit code, -1 for exception or running",
  "stdout": "string - standard output (Head-Tail dual-end buffer)",
  "stderr": "string - standard error (Head-Tail dual-end buffer)",
  "systemMessage": "string - system message/error details"
}
```

#### Examples

**Synchronous Execution**

```bash
curl -X POST http://localhost:8080/exec \
  -H "Content-Type: application/json" \
  -d '{"command": "ls -la", "timeoutSeconds": 10}'
```

Response:
```json
{
  "status": "success",
  "exitCode": 0,
  "stdout": "total 32\n...",
  "stderr": "",
  "systemMessage": "command executed successfully"
}
```

**Background Execution**

```bash
curl -X POST http://localhost:8080/exec \
  -H "Content-Type: application/json" \
  -d '{"command": "python train.py", "runInBackground": true}'
```

Response:
```json
{
  "status": "running",
  "exitCode": -1,
  "stdout": "",
  "stderr": "",
  "systemMessage": "process started with PID 12345"
}
```

**Watch Window Mode**

```bash
curl -X POST http://localhost:8080/exec \
  -H "Content-Type: application/json" \
  -d '{
    "command": "java -jar app.jar",
    "runInBackground": true,
    "watchDurationSeconds": 5
  }'
```

- If process exits within 5 seconds → returns `status: "failed"` + exit code + output
- If process still running after 5 seconds → returns `status: "running"` + initialization logs

---

### Query Process Status

**GET** `/process/:pid`

Queries the current status of a background process.

#### Response Structure

```json
{
  "pid": 12345,
  "status": "running/completed/failed",
  "exitCode": 0,
  "command": "python train.py",
  "startTime": "2024-01-15T10:30:00Z",
  "endTime": "",
  "watchDurationSeconds": 0,
  "watchCompleted": false
}
```

#### Example

```bash
curl http://localhost:8080/process/12345
```

---

### Get Process Logs

**GET** `/process/:pid/logs`

Gets complete information about a background process, including output logs.

#### Response Structure

```json
{
  "pid": 12345,
  "status": "running",
  "exitCode": -1,
  "command": "python train.py",
  "startTime": "2024-01-15T10:30:00Z",
  "stdout": "Training started...\nEpoch 1: loss=0.5",
  "stderr": ""
}
```

#### Example

```bash
curl http://localhost:8080/process/12345/logs
```

---

### Terminate Process

**DELETE** `/process/:pid`

Terminates the specified background process and all its child processes.

#### Response Structure

```json
{
  "status": "success",
  "message": "process 12345 terminated"
}
```

#### Example

```bash
curl -X DELETE http://localhost:8080/process/12345
```

---

### List All Processes

**GET** `/processes`

Lists all background processes.

#### Example

```bash
curl http://localhost:8080/processes
```

---

### Health Check

**GET** `/health`

Checks if the service is running normally.

#### Response Structure

```json
{
  "status": "healthy"
}
```

#### Example

```bash
curl http://localhost:8080/health
```

---

## Core Design Details

### Head-Tail Ring Buffer

**Problem Background**: Some programs produce infinite log output (e.g., Java exception stack traces), and reading all at once causes memory overflow.

**Solution**: Use Head-Tail dual-end buffering strategy, strictly limiting memory usage to ≤ 8KB.

```
┌─────────────────────────────────────────────────────────────┐
│                Dual-End Buffer Structure (Max 8KB)           │
├──────────────────┬─────────────────────┬───────────────────┤
│   Head Buffer    │   Discarded Area    │   Tail Buffer     │
│   (First 4KB)    │   (Middle Data)     │   (Last 4KB)      │
│                  │                     │                   │
│  Root Cause      │   Auto-discarded    │   Latest State    │
│  Evidence        │                     │                   │
└──────────────────┴─────────────────────┴───────────────────┘
```

**Design Principles**:

| Region | Size | Purpose |
|--------|------|---------|
| Head Buffer | 4KB fixed | Preserves initial output at program startup for root cause diagnosis |
| Tail Buffer | 4KB ring | Circular overwrite preserves latest output for current state monitoring |
| Middle Data | Auto-discarded | Does not occupy memory, auto-truncated when exceeding 8KB |

**Truncation Notice**: When total output > 8KB, inserts at splice point:

```
... [TRUNCATED: 10240 bytes omitted] ...
```

---

### Watch Window Mode (watchDurationSeconds)

**Use Case**: When starting background services (e.g., Java applications, web servers), need to confirm successful startup.

**Workflow**:

```
Process Start ──────────────┬──────────────────────> Time
                             │
                             ▼
                  Wait watchDurationSeconds
                             │
               ┌─────────────┴─────────────┐
               ▼                           ▼
        Process Exited              Process Still Running
               │                           │
               ▼                           ▼
      Return status: failed        Return status: running
           exit_code: X                + initialization logs
           + full output               Process continues in background
```

**Advantages**:

- Avoids undetected startup failures
- Captures initialization phase logs (e.g., startup errors, configuration issues)
- Confirms service is running normally before returning

---

### Timeout Control & Process Group Management

**Timeout Mechanism**:

- Uses `setTimeout` with `Promise.race` for timeout control
- Thoroughly terminates process and all child processes after timeout

**Process Group Management**:

| Platform | Implementation |
|----------|----------------|
| Windows | `tree-kill` library |
| Linux/macOS | `process.kill(-pid)` kills entire process group |

**Purpose**: Prevents orphan process residue.

---

### Environment Variable Inheritance & Override

**Default Behavior**: Child processes inherit all host environment variables.

**Override Rule**: Variables in the `env` object override host variables with the same name.

```json
{
  "command": "node app.js",
  "env": {
    "NODE_ENV": "production",
    "API_KEY": "secret123"
  }
}
```

---

## Configuration Parameters

### Constants

| Constant | Default | Description |
|----------|---------|-------------|
| `DEFAULT_TIMEOUT_SECONDS` | 30 | Default timeout in seconds |
| `MAX_OUTPUT_BYTES` | 8192 (8KB) | Maximum output bytes |
| `TRUNCATE_HEAD_BYTES` | 4096 (4KB) | Head buffer size |
| `TRUNCATE_TAIL_BYTES` | 4096 (4KB) | Tail buffer size |
| `DEFAULT_HTTP_PORT` | 8080 | HTTP service default port |
| `DEFAULT_MAX_PROCESSES` | 100 | Maximum background processes |

### Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--server` | Start HTTP service mode | false |
| `--port` | HTTP service port | 8080 |
| `--max-processes` | Maximum background processes | 100 |
| `-h, --help` | Show help information | - |

---

## Status Codes

### Execution Status

| Status | Description |
|--------|-------------|
| `success` | Command executed successfully, exit code 0 |
| `failed` | Command execution failed, exit code non-zero |
| `timeout` | Command execution timed out, process terminated |
| `killed` | Process manually terminated |
| `running` | Process running in background |

### Process Status

| Status | Description |
|--------|-------------|
| `running` | Process is running |
| `completed` | Process completed normally |
| `failed` | Process exited abnormally or was terminated |

---

## Error Handling

### Predefined Errors

| Error | Description |
|-------|-------------|
| `EmptyCommandError` | Empty command |
| `ProcessNotFoundError` | Process not found |
| `TimeoutExceededError` | Execution timeout |
| `ProcessAlreadyExistsError` | Process already exists (PID conflict) |
| `InvalidWorkingDirError` | Invalid working directory |
| `MaxProcessesReachedError` | Maximum process limit reached |

### HTTP Error Response

```json
{
  "error": "process not found"
}
```

| HTTP Status Code | Description |
|------------------|-------------|
| 400 | Request parameter error |
| 404 | Process not found |
| 500 | Internal error |

---

## Best Practices

### 1. Choose the Right Execution Mode

| Scenario | Recommended Mode |
|----------|------------------|
| Quick commands (ls, echo) | Synchronous execution |
| Long-running tasks (model training) | Background execution |
| Service startup (Web Server) | Background + Watch window |

### 2. Set Reasonable Timeout

```json
{
  "command": "npm install",
  "timeoutSeconds": 300
}
```

### 3. Use Watch Window to Confirm Startup

```json
{
  "command": "java -jar app.jar",
  "runInBackground": true,
  "watchDurationSeconds": 10
}
```

### 4. Multi-Agent Sharing via HTTP Service

Start the HTTP service and let multiple agents connect to the same endpoint:

```bash
# Start service
node dist/index.js --server --port 8080

# All agents use the same endpoint
curl http://localhost:8080/exec ...
curl http://localhost:8080/processes ...
```

---

## Project Structure

```
exec-guard-ts/
├── src/
│   ├── index.ts              # Main entry
│   ├── types.ts              # Type definitions
│   ├── constants.ts          # Constants
│   ├── ringbuf.ts            # Ring buffer implementation
│   ├── executor.ts           # Command executor
│   ├── process-manager.ts    # Background process manager
│   ├── platform.ts           # Cross-platform handling
│   ├── server.ts             # HTTP server
│   └── cli.ts                # CLI mode
├── tests/
│   ├── ringbuf.test.ts       # RingBuffer tests
│   ├── executor.test.ts      # Executor tests
│   └── process-manager.test.ts # ProcessManager tests
├── package.json
├── tsconfig.json
├── jest.config.js
├── README.md
└── AGENT_GUIDE.md            # AI Agent usage guide
```

---

## Related Projects

- [exec-guard (Go version)](https://github.com/cypress927/exec-guard) - Original Go implementation

---

## License

MIT License

---

# 中文文档

## 项目概述

**exec-guard** 是一个为 AI Agent 提供安全、可靠系统命令执行能力的基础设施模块。它解决了 AI Agent 在执行系统命令时面临的核心挑战：

- **超时控制**：防止命令无限执行导致资源占用
- **内存保护**：防止大输出导致内存溢出（双端环形缓冲）
- **进程管理**：支持后台进程启动、监控、终止
- **跨平台兼容**：统一接口，Windows/Linux/macOS 无缝切换

这是原始 [Go 版本](https://github.com/cypress927/exec-guard) 的 TypeScript/Node.js 实现。

---

## 功能特性

### 核心能力

| 特性 | 说明 |
|------|------|
| 同步执行 | 执行命令并等待结果，支持超时控制 |
| 后台执行 | 启动后台进程，支持状态查询和日志获取 |
| 监控窗口 | 后台启动后观察 N 秒，判断是否成功启动 |
| 双端缓冲 | Head-Tail 环形缓冲，最大 8KB，防止 OOM |
| 环境变量 | 继承宿主机环境变量，支持自定义覆盖 |
| 进程组管理 | 杀死进程时连带终止所有子进程 |

### 运行模式

- **CLI 模式**：从标准输入读取 JSON 请求，输出 JSON 响应
- **HTTP 服务模式**：提供 RESTful API，支持远程调用和多 Agent 共享

---

## 安装与构建

### 环境要求

- Node.js 18+
- npm 或 yarn

### 安装

```bash
npm install
```

### 构建

```bash
npm run build
```

### 运行测试

```bash
npm test
```

---

## 使用方式

### CLI 模式

从标准输入读取 JSON 请求，执行命令后输出 JSON 响应：

```bash
# 基础用法
echo '{"command": "echo hello"}' | node dist/index.js

# 带超时
echo '{"command": "sleep 5", "timeoutSeconds": 3}' | node dist/index.js

# 后台执行
echo '{"command": "long_task", "runInBackground": true}' | node dist/index.js

# 自定义环境变量
echo '{"command": "node app.js", "env": {"NODE_ENV": "production"}}' | node dist/index.js
```

### HTTP 服务模式

启动 HTTP 服务器，提供 RESTful API：

```bash
# 默认端口 8080
node dist/index.js --server

# 自定义端口
node dist/index.js --server --port 9000

# 限制最大后台进程数
node dist/index.js --server --port 8080 --max-processes 50
```

---

## API 文档

### 执行命令

**POST** `/exec`

执行系统命令，支持同步和后台两种模式。

#### 请求参数

```json
{
  "command": "string，必填 - 要执行的系统命令",
  "workingDir": "string，可选 - 工作目录，默认当前目录",
  "timeoutSeconds": "number，可选 - 超时时间（秒），默认 30",
  "runInBackground": "boolean，可选 - 是否后台运行，默认 false",
  "watchDurationSeconds": "number，可选 - 监控窗口时长（秒），仅后台模式",
  "env": "object，可选 - 自定义环境变量"
}
```

#### 响应结构

```json
{
  "status": "string - success/failed/timeout/killed/running",
  "exitCode": "number - 进程退出码，-1 表示异常或运行中",
  "stdout": "string - 标准输出（Head-Tail 双端缓冲）",
  "stderr": "string - 标准错误（Head-Tail 双端缓冲）",
  "systemMessage": "string - 系统消息/错误详情"
}
```

---

### 查询进程状态

**GET** `/process/:pid`

查询后台进程的当前状态。

### 获取进程日志

**GET** `/process/:pid/logs`

获取后台进程的完整信息，包含输出日志。

### 终止进程

**DELETE** `/process/:pid`

终止指定的后台进程及其所有子进程。

### 列出所有进程

**GET** `/processes`

列出所有后台进程。

### 健康检查

**GET** `/health`

检查服务是否正常运行。

---

## 项目结构

```
exec-guard-ts/
├── src/
│   ├── index.ts              # 主入口
│   ├── types.ts              # 类型定义
│   ├── constants.ts          # 常量定义
│   ├── ringbuf.ts            # 环形缓冲区实现
│   ├── executor.ts           # 命令执行器
│   ├── process-manager.ts    # 后台进程管理器
│   ├── platform.ts           # 跨平台处理
│   ├── server.ts             # HTTP 服务
│   └── cli.ts                # CLI 模式
├── tests/
│   ├── ringbuf.test.ts       # RingBuffer 测试
│   ├── executor.test.ts      # 执行器测试
│   └── process-manager.test.ts # 进程管理器测试
├── package.json
├── tsconfig.json
├── jest.config.js
├── README.md
└── AGENT_GUIDE.md            # AI Agent 使用指南
```

---

## 相关项目

- [exec-guard (Go 版本)](https://github.com/cypress927/exec-guard) - 原始 Go 实现

---

## 许可证

MIT License