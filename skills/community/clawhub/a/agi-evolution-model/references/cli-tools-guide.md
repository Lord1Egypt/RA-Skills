# CLI工具箱完整指南

CLI工具箱提供四个核心工具，扩展智能体与系统的交互能力。

## 目录
1. [概述](#概述)
2. [文件操作工具](#文件操作工具)
3. [系统信息工具](#系统信息工具)
4. [进程管理工具](#进程管理工具)
5. [通用命令执行器](#通用命令执行器)
6. [安全说明](#安全说明)
7. [集成指南](#集成指南)

---

## 概述

### 统一返回格式
所有CLI工具返回统一的JSON格式：
```json
{
  "status": "success|error",
  "data": {},
  "error": "错误信息（仅status=error时）",
  "metadata": {},
  "timestamp": "ISO 8601时间戳"
}
```

### 安全特性
- 路径验证：防止路径遍历攻击
- 错误处理：完善的异常捕获和错误信息返回
- 超时控制：所有操作都有超时限制（默认60秒）
- 参数验证：基本参数类型和范围验证
- 危险命令黑名单：阻止危险操作

> ⚠️ **注意**：CLI工具采用宽松的安全策略，赋予智能体较大的操作权限，建议在受控环境中使用。

---

## 文件操作工具 (cli_file_operations.py)

### 支持的操作

| 操作 | 说明 | 关键参数 |
|------|------|---------|
| `read` | 读取文件内容 | `--path`, `--encoding`, `--max-lines` |
| `write` | 写入文件内容 | `--path`, `--content`, `--mode` |
| `list` | 列出目录内容 | `--path`, `--recursive`, `--show-hidden` |
| `search` | 搜索文件内容 | `--path`, `--pattern`, `--file-pattern` |
| `delete` | 删除文件/目录 | `--path`, `--recursive-delete` |
| `move` | 移动文件/目录 | `--src`, `--dst` |
| `copy` | 复制文件/目录 | `--src`, `--dst` |
| `mkdir` | 创建目录 | `--path`, `--parents` |
| `stat` | 获取文件/目录详细信息 | `--path` |

### 使用示例

#### 读取文件
```bash
# 读取完整文件
python3 scripts/cli_file_operations.py --action read --path ./config.json

# 读取前100行
python3 scripts/cli_file_operations.py --action read --path ./log.txt --max-lines 100

# 指定编码
python3 scripts/cli_file_operations.py --action read --path ./data.txt --encoding utf-8
```

#### 写入文件
```bash
# 覆盖写入
python3 scripts/cli_file_operations.py --action write --path ./output.txt --content "Hello"

# 追加写入
python3 scripts/cli_file_operations.py --action write --path ./output.txt --content "World" --mode append
```

#### 列出目录
```bash
# 列出当前目录
python3 scripts/cli_file_operations.py --action list --path ./

# 递归列出
python3 scripts/cli_file_operations.py --action list --path ./projects --recursive

# 显示隐藏文件
python3 scripts/cli_file_operations.py --action list --path . --show-hidden
```

#### 搜索文件内容
```bash
# 搜索包含"import"的文件
python3 scripts/cli_file_operations.py --action search --path ./src --pattern "import"

# 搜索特定模式的文件
python3 scripts/cli_file_operations.py --action search --path ./src --pattern "TODO" --file-pattern "*.py"
```

#### 删除操作
```bash
# 删除单个文件
python3 scripts/cli_file_operations.py --action delete --path ./temp.txt

# 递归删除目录
python3 scripts/cli_file_operations.py --action delete --path ./temp_dir --recursive-delete
```

#### 移动和复制
```bash
# 移动文件
python3 scripts/cli_file_operations.py --action move --src ./old.txt --dst ./new.txt

# 复制文件
python3 scripts/cli_file_operations.py --action copy --src ./source.txt --dst ./backup.txt
```

#### 创建目录
```bash
# 创建单个目录
python3 scripts/cli_file_operations.py --action mkdir --path ./new_folder

# 创建多级目录
python3 scripts/cli_file_operations.py --action mkdir --path ./a/b/c --parents
```

---

## 系统信息工具 (cli_system_info.py)

### 支持的操作

| 操作 | 说明 | 关键参数 |
|------|------|---------|
| `system` | 获取系统基本信息 | 无 |
| `cpu` | 获取CPU信息和使用率 | 无 |
| `memory` | 获取内存信息 | 无 |
| `disk` | 获取磁盘使用情况 | `--path` |
| `network` | 获取网络接口信息 | 无 |
| `uptime` | 获取系统运行时间 | 无 |
| `env` | 获取环境变量 | 无（敏感信息已过滤） |
| `all` | 获取所有系统信息 | 无 |

### 使用示例

```bash
# 获取系统信息
python3 scripts/cli_system_info.py --action system

# 获取CPU信息
python3 scripts/cli_system_info.py --action cpu

# 获取内存信息
python3 scripts/cli_system_info.py --action memory

# 获取特定磁盘信息
python3 scripts/cli_system_info.py --action disk --path /

# 获取网络信息
python3 scripts/cli_system_info.py --action network

# 获取系统运行时间
python3 scripts/cli_system_info.py --action uptime

# 获取环境变量
python3 scripts/cli_system_info.py --action env

# 获取所有系统信息
python3 scripts/cli_system_info.py --action all
```

---

## 进程管理工具 (cli_process_manager.py)

### 支持的操作

| 操作 | 说明 | 关键参数 |
|------|------|---------|
| `list` | 获取进程列表 | `--user-only`, `--name-filter` |
| `search` | 搜索进程 | `--name` |
| `detail` | 获取进程详细信息 | `--pid` |
| `kill` | 终止进程 | `--pid`, `--signal` |
| `tree` | 获取进程树 | 无 |
| `stats` | 获取进程统计信息 | 无 |

### 使用示例

```bash
# 获取进程列表
python3 scripts/cli_process_manager.py --action list

# 仅显示当前用户进程
python3 scripts/cli_process_manager.py --action list --user-only

# 按名称过滤进程
python3 scripts/cli_process_manager.py --action list --name-filter python

# 搜索进程
python3 scripts/cli_process_manager.py --action search --name nginx

# 获取进程详情
python3 scripts/cli_process_manager.py --action detail --pid 1234

# 终止进程（默认SIGTERM）
python3 scripts/cli_process_manager.py --action kill --pid 1234

# 强制终止进程（SIGKILL）
python3 scripts/cli_process_manager.py --action kill --pid 1234 --signal KILL

# 获取进程树
python3 scripts/cli_process_manager.py --action tree

# 获取进程统计信息
python3 scripts/cli_process_manager.py --action stats
```

---

## 通用命令执行器 (cli_executor.py)

### 支持的操作

| 操作 | 说明 | 关键参数 |
|------|------|---------|
| `execute` | 执行任意命令 | `--command`, `--work-dir`, `--timeout`, `--shell-type`, `--env` |

### 使用示例

#### Bash命令（Linux/macOS）
```bash
# 执行简单命令
python3 scripts/cli_executor.py --action execute --command "echo 'Hello World'"

# 执行管道命令
python3 scripts/cli_executor.py --action execute --command "ls -la | head -5"

# 执行复杂命令
python3 scripts/cli_executor.py --action execute --command "find . -name '*.py' | xargs wc -l"

# 指定工作目录
python3 scripts/cli_executor.py --action execute --command "pwd" --work-dir /tmp

# 设置环境变量
python3 scripts/cli_executor.py --action execute --command "echo $MY_VAR" --env "MY_VAR=test"

# 自定义超时时间
python3 scripts/cli_executor.py --action execute --command "sleep 10" --timeout 5
```

#### Windows CMD命令
```bash
# 指定使用cmd
python3 scripts/cli_executor.py --action execute --command "dir" --shell-type cmd

# 执行Windows命令
python3 scripts/cli_executor.py --action execute --command "ipconfig /all" --shell-type cmd
```

#### PowerShell命令（Windows）
```bash
# 指定使用powershell
python3 scripts/cli_executor.py --action execute --command "Get-Process" --shell-type powershell

# 执行PowerShell管道命令
python3 scripts/cli_executor.py --action execute --command "Get-Service | Where-Object {$_.Status -eq 'Running'}" --shell-type powershell

# 获取系统信息
python3 scripts/cli_executor.py --action execute --command "Get-ComputerInfo" --shell-type powershell
```

#### 自动适配（跨平台）
```bash
# 在Linux/macOS上自动使用bash，在Windows上自动使用PowerShell
python3 scripts/cli_executor.py --action execute --command "ls -la"  # Linux/macOS
python3 scripts/cli_executor.py --action execute --command "Get-ChildItem"  # Windows（如果PowerShell可用）
```

#### Git操作
```bash
python3 scripts/cli_executor.py --action execute --command "git status"
python3 scripts/cli_executor.py --action execute --command "git log --oneline -10"
```

#### Docker操作
```bash
python3 scripts/cli_executor.py --action execute --command "docker ps -a"
python3 scripts/cli_executor.py --action execute --command "docker images"
```

#### 包管理器操作
```bash
# pip
python3 scripts/cli_executor.py --action execute --command "pip list"

# npm
python3 scripts/cli_executor.py --action execute --command "npm ls"

# Windows包管理器
python3 scripts/cli_executor.py --action execute --command "winget list" --shell-type powershell
```

### Shell类型自动适配

| 操作系统 | 默认Shell | 可选Shell |
|---------|-----------|-----------|
| Linux | bash | bash, powershell（如已安装） |
| macOS | bash | bash, powershell（如已安装） |
| Windows | powershell（优先）或 cmd | cmd, powershell |

**自动适配规则**：
- Linux/macOS：默认使用 `bash`
- Windows：优先使用 `powershell`，如不可用则使用 `cmd`
- 可通过 `--shell-type` 参数强制指定

---

## 安全说明

### 危险命令黑名单
通用命令执行器内置危险命令黑名单，自动阻止以下操作：

| 危险命令类型 | 示例 |
|------------|------|
| 删除根目录 | `rm -rf /` |
| 磁盘擦除 | `dd if=/dev/zero of=/dev/sda` |
| Fork炸弹 | `:(){ :|:& };:` |
| 格式化文件系统 | `mkfs.ext4 /dev/sda1` |
| 全局权限修改 | `chmod -R 777 /` |
| 关机/重启 | `shutdown`, `reboot`, `poweroff` |
| 下载并执行脚本 | `wget xxx | sh`, `curl xxx | sh` |
| 系统关键目录修改 | 修改 `/etc`, `/usr`, `/var`, `/bin` 等目录 |

**触发黑名单时返回**：
```json
{
  "status": "error",
  "error": "命令执行被阻止: 检测到危险命令模式: rm\\s+-rf\\s+/",
  "metadata": {
    "blocked": true,
    "reason": "检测到危险命令模式: rm\\s+-rf\\s+/"
  }
}
```

---

## 集成指南

### 集成到感知节点
CLI工具可以作为新的感知节点集成到架构中：

```python
import json
import subprocess

def get_system_status():
    """获取系统状态作为感知输入"""
    result = subprocess.run(
        ['python3', 'scripts/cli_system_info.py', '--action', 'all'],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return data

def read_config_file(path):
    """读取配置文件"""
    result = subprocess.run(
        ['python3', 'scripts/cli_file_operations.py', '--action', 'read', '--path', path],
        capture_output=True, text=True
    )
    data = json.loads(result.stdout)
    return data
```

### 映射层应用
系统资源信息可以作为映射层决策的输入：

- **资源约束**：磁盘空间不足时，降低文件生成优先级
- **性能优化**：CPU/内存高负载时，调整任务调度策略
- **故障检测**：进程异常时，触发恢复机制

---

## 相关文档
- [使用示例](usage-examples.md) - CLI工具的快速使用示例
- [架构文档](architecture.md) - 理解整体架构设计
