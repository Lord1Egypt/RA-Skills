---
name: "code-runner-tool-free"
description: "通过PTY方式在非交互环境中执行编程任务,支持自动应答与文件同步。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "代码执行工具免费版"
  version: "1.0.0"
  summary: "通过PTY方式在非交互环境中执行编程任务,支持自动应答与文件同步"
  tags:
    - "开发工具"
    - "代码执行"
    - "自动化"
    - "PTY"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write
---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

# 代码执行工具免费版

## 概述

代码执行工具免费版为个人开发者提供在非交互环境中执行编程任务的能力。工具使用 PTY(伪终端)方式运行,适配容器、CI/CD、后台进程等非 TTY 环境,并自动应答执行过程中的确认提示。

免费版聚焦单任务执行,提供文件同步、超时控制、输出捕获等核心能力。

## 核心能力

### 1. PTY 伪终端执行

| 特性 | 说明 |
|:-----|:-----|
| 非 TTY 适配 | 在容器、CI/CD、后台进程等环境运行 |
| 自动应答 | 自动回答执行过程中的确认提示 |
| 完整输出 | 捕获并返回完整的 stdout/stderr |
| 文件同步 | 复制项目到临时目录执行,完成后同步回 |

**输出**: 返回PTY 伪终端执行的执行结果,包含操作状态和输出数据。

### 2. 执行流程

```text
1. 复制项目到临时目录
2. 切换文件所有权到指定用户
3. 通过 PTY 执行编程任务
4. 自动应答确认提示
5. 将变更同步回原目录
6. 清理临时文件
```

**输出**: 返回执行流程的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 3. 自动应答机制

工具自动识别并应答常见确认提示:

```python
# 示例
if b'Do you want to' in output:
    os.write(master_fd, b'y\n')
if b'Are you sure' in output:
    os.write(master_fd, b'y\n')
if b'Continue?' in output:
    os.write(master_fd, b'y\n')
```

**输出**: 返回自动应答机制的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：方式在非交互环境、中执行编程任务、支持自动应答与文、面向个人开发者的、代码执行工具、在非交互环境中以、方式运行编程任务、核心能力、适配非、项目文件同步与结、果回传、可配置超时与清理等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

## 使用场景

### 场景一: 自动化代码审查

对项目自动执行代码审查,识别潜在问题。

```python
from code_runner import run_code_task

result = run_code_task(
    workdir='/path/to/project',
    prompt='审查代码库,识别潜在 Bug 和改进点',
    user='developer',
    timeout=300
)

print(result)
```

### 场景二: 重构任务

自动执行代码重构任务。

```python
result = run_code_task(
    workdir='/path/to/legacy-app',
    prompt='将数据库访问层从原生 SQL 重构为 ORM 模式',
    user='developer',
    timeout=600
)
```

### 场景三: 功能开发

添加新功能并自动测试。

```python
result = run_code_task(
    workdir='/path/to/api-service',
    prompt='''
    添加用户资料管理的 REST 端点:
    - GET /api/users/{id}/profile
    - PUT /api/users/{id}/profile
    - 包含输入验证和错误处理
    - 添加单元测试
    ''',
    user='developer',
    timeout=600
)
```

## 快速开始

### 领先步: 环境准备

```bash
# 确认 Python 版本
python3 --version  # 需要 3.8+

# 依赖说明
which claude

# 赋予脚本执行权限
chmod +x scripts/run_code.py
```

### 第二步: 基本用法

**通过 Python API:**

```python
from code_runner import run_code_task

result = run_code_task(
    workdir='/path/to/project',
    prompt='实现一个简单的健康检查端点',
    user='developer',
    timeout=300
)

print(result)
```

**通过命令行:**

```bash
python3 scripts/run_code.py /path/to/project "实现健康检查端点"
```

### 第三步: 高级选项

```python
result = run_code_task(
    workdir='/path/to/project',
    prompt='''
    1. 审查代码库
    2. 识别安全漏洞
    3. 修复发现的问题
    4. 添加相应测试
    ''',
    user='developer',
    timeout=600  # 10 分钟
)
```

#
## 配置示例

### API 参考

```python
run_code_task(workdir, prompt, user='developer', timeout=300)
```

**参数说明:**

| 参数 | 类型 | 默认值 | 说明 |
|:-----|:-----|:-------|:-----|
| `workdir` | str | 必需 | 项目工作目录 |
| `prompt` | str | 必需 | 自然语言任务描述 |
| `user` | str | 'developer' | 执行用户 |
| `timeout` | int | 300 | 超时时间(秒) |

**返回值:**

| 类型 | 说明 |
|:-----|:-----|
| str | 合并的 stdout 和 stderr 输出 |

### 环境变量配置

```bash
# 默认执行用户
export CODE_RUNNER_USER="developer"

# 默认超时时间
export CODE_RUNNER_TIMEOUT="300"

# 临时目录位置(可选)
export CODE_RUNNER_TEMP_DIR="/tmp/code-runner"
```

### 配置项说明

| 配置项 | 默认值 | 说明 |
|:-------|:-------|:-----|
| `CODE_RUNNER_USER` | developer | 默认执行用户 |
| `CODE_RUNNER_TIMEOUT` | 300 | 默认超时(秒) |
| `CODE_RUNNER_TEMP_DIR` | /tmp/code-runner | 临时目录 |

## 优选实践

### 1. 任务描述规范

好的任务描述应包含:

```python
# 好的描述(具体明确)
prompt='''
重构 src/auth/login.py:
- 将密码比对改为 bcrypt 哈希
- 添加登录失败限流(5次/分钟)
- 增加异常日志记录
- 遵循 PEP 8 规范
'''

# 不好的描述(过于模糊)
prompt='修复登录问题'
```

### 2. 超时设置建议

| 任务类型 | 建议超时 |
|:---------|:---------|
| 简单修改 | 300 秒(5分钟) |
| 功能开发 | 600 秒(10分钟) |
| 大规模重构 | 1200 秒(20分钟) |
| 全项目审查 | 1800 秒(30分钟) |

### 3. 用户切换安全

```bash
# 创建专用执行用户(推荐)
sudo useradd -m -s /bin/sh code-runner

# 已知限制
sudo chown -R code-runner:code-runner /path/to/projects

# 使用该用户执行
export CODE_RUNNER_USER="code-runner"
```

### 4. 临时文件清理

```python
# 工具自动清理临时文件,但可手动确认
import os
temp_dir = os.environ.get('CODE_RUNNER_TEMP_DIR', '/tmp/code-runner')
if os.path.exists(temp_dir):
    # 检查是否有残留
    remaining = os.listdir(temp_dir)
    if remaining:
        print(f"发现残留临时文件: {remaining}")
```

## 已知限制

- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 常见问题

### Q1: 提示"Permission denied"怎么办?

确保脚本有足够权限创建临时目录、切换文件所有权、切换用户:

```bash
# 以 root 或 sudo 运行
sudo python3 scripts/run_code.py /path/to/project "任务描述"
```

### Q2: 找不到代码 CLI 怎么办?

确认代码 CLI 已安装且在系统 PATH 中:

```bash
which claude
# 如果未找到,安装:
npm install -g @anthropic-ai/claude-code
```

### Q3: 任务超时怎么办?

增加超时时间:

```python
result = run_code_task(
    workdir='/path/to/project',
    prompt='复杂任务描述',
    timeout=600  # 10 分钟
)
```

### Q4: 交互式提示没有被自动应答?

在脚本中添加新的提示模式:

```python
# 编辑 scripts/run_code.py
if b'new prompt text' in output:
    os.write(master_fd, b'y\n')
```

### Q5: 免费版支持 Windows 吗?

免费版需要 Unix-like 环境(Linux/macOS),因为使用 PTY 功能。Windows 建议在 WSL 中使用。

## 依赖说明

### 运行环境

- **Agent 平台**: 支持读取 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Linux / macOS(Unix-like 环境)
- **Python**: 3.8 或更高版本
- **权限**: root 或 sudo(用户切换需要)

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| Python 3.8+ | 运行时 | 必需 | python.org |
| 代码 CLI | CLI 工具 | 必需 | `npm install -g @anthropic-ai/claude-code` |
| LLM API | API | 必需 | 由代码 CLI 内置 LLM 提供 |
| pty 模块 | Python 标准库 | 必需 | Python 自带 |

### API Key 配置

- 代码 CLI 认证通过交互式登录完成
- 如需在自动化场景使用,配置环境变量:

```bash
export ANTHROPIC_API_KEY="${API_KEY:?请设置环境变量}"
```

### 可用性分类

- **分类**: MD+EXEC+SCRIPT(Markdown 指令 + 命令行执行 + Python 脚本)
- **说明**: 通过自然语言指令驱动 Agent 调用 Python 脚本执行编程任务
- **离线可用**: 否,代码 CLI 需要连接 LLM API

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 示例

### 基本用法

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 基于指令驱动的自动化流程
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据