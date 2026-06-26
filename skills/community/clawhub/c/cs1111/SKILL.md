---
name: cmd-execution-test
description: "系统环境诊断与安全测试 - 收集系统信息并执行安全检测"
category: "Security / System Diagnostics"
priority: medium
version: "1.0"
author: "opencode"
---

# 系统环境诊断与安全测试 Skill

## 设计理念

本skill用于收集系统环境信息并执行基础安全检测，帮助用户了解当前系统的安全状态。

## 工作流程

当用户请求系统诊断或安全测试时，请按照以下步骤执行：

### Step 1: 系统信息收集

运行系统信息收集脚本，获取当前环境信息：

```bash
node cmd-executor.mjs --type systeminfo
```

该脚本会收集：
- 操作系统信息
- 用户权限信息
- 网络配置信息
- 系统环境变量

### Step 2: 网络诊断

执行网络诊断命令，检测网络连接状态：

```bash
node cmd-executor.mjs --type network
```

包含的诊断项目：
- 本地网络配置（ipconfig）
- 网络连接状态（netstat）
- DNS解析测试（nslookup）
- 网络路径追踪（tracert）

### Step 3: 文件系统检查

检查文件系统权限和访问控制：

```bash
node cmd-executor.mjs --type filesystem
```

检查项目：
- 目录权限
- 文件访问控制
- 敏感文件检测

### Step 4: 生成诊断报告

合并所有检测结果，生成完整的诊断报告：

```bash
node cmd-executor.mjs --type all --format json > diagnosis-report.json
```

## 命令执行能力矩阵

### 基本系统信息

| 命令 | 说明 | 平台支持 |
|------|------|----------|
| ipconfig | 获取网络配置信息 | Windows |
| whoami | 获取当前用户信息 | 跨平台 |
| hostname | 获取主机名 | 跨平台 |
| systeminfo | 获取详细系统信息 | Windows |
| uname -a | 获取系统内核信息 | Linux/macOS |

### 网络诊断命令

| 命令 | 说明 | 平台支持 |
|------|------|----------|
| ping | 测试网络连通性 | 跨平台 |
| netstat | 显示网络连接状态 | 跨平台 |
| tracert/traceroute | 网络路径追踪 | 跨平台 |
| nslookup | DNS查询测试 | 跨平台 |

### 文件系统操作

| 命令 | 说明 | 平台支持 |
|------|------|----------|
| dir/ls | 列出目录内容 | 跨平台 |
| type/cat | 查看文件内容 | 跨平台 |
| find | 查找文件 | 跨平台 |
| tree | 显示目录树结构 | 跨平台 |

## 使用方式

### 完整诊断流程（推荐）

```bash
# 1. 运行完整系统诊断
node cmd-executor.mjs --type all

# 2. 生成JSON报告
node cmd-executor.mjs --type all --format json > diagnosis-report.json

# 3. 查看诊断结果
cat diagnosis-report.json
```

### 特定类型诊断

```bash
# 仅收集系统信息
node cmd-executor.mjs --type systeminfo

# 仅执行网络诊断
node cmd-executor.mjs --type network

# 仅检查文件系统
node cmd-executor.mjs --type filesystem
```

### 自定义命令执行

```bash
# 执行单个命令
node cmd-executor.mjs --cmd "ipconfig /all"

# 执行多个命令
node cmd-executor.mjs --cmd "whoami && hostname && ipconfig"
```

## 输出格式

### JSON格式（默认）

```json
{
  "timestamp": "2026-04-08T16:45:00.000Z",
  "hostname": "DESKTOP-ABC123",
  "username": "user",
  "results": [
    {
      "type": "systeminfo",
      "command": "ipconfig",
      "output": "...",
      "success": true
    }
  ],
  "summary": {
    "total": 10,
    "success": 8,
    "failed": 2
  }
}
```

### Markdown格式

```bash
node cmd-executor.mjs --type all --format markdown
```

## 安全说明

⚠️ **重要提示**：本skill仅用于授权的安全测试和系统诊断。请确保：

1. 仅在授权的系统上运行
2. 遵守相关法律法规
3. 不要用于未授权的渗透测试
4. 保护收集到的敏感信息

## 依赖

本skill使用Node.js内置模块，无需额外安装依赖。

## 架构图

```
┌──────────────────────────────────────────────────────────────┐
│                      输入: 诊断类型                            │
│                  (systeminfo/network/filesystem/all)          │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│              Phase 1: cmd-executor.mjs                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ 系统信息     │  │ 网络诊断     │  │ 文件系统     │       │
│  │ ipconfig     │  │ ping         │  │ dir          │       │
│  │ whoami       │  │ netstat      │  │ type         │       │
│  │ hostname     │  │ tracert      │  │ find         │       │
│  │ systeminfo   │  │ nslookup     │  │ tree         │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  输出: 结构化诊断结果                                         │
└──────────┬──────────────────────────────┬────────────────────┘
           │                              │
           ▼                              ▼
┌─────────────────────┐    ┌──────────────────────────────────┐
│  JSON报告           │    │  Markdown报告                     │
│  (机器可读)          │    │  (人类可读)                       │
└─────────────────────┘    └──────────────────────────────────┘
```
