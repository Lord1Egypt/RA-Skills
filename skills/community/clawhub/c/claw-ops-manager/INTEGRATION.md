# Claw 运营管理中心 - 自动记录集成指南

## 问题说明

目前 Claw 运营管理中心已经安装并运行，但是**OpenClaw 的工具调用不会自动记录**到审计系统。

## 原因

审计系统需要一个集成层来捕获 OpenClaw 的所有工具调用（exec, read, write 等）。

## 解决方案

### 方案 1：Shell 别名集成（推荐，简单快速）

在你的 shell 配置文件（`~/.zshrc` 或 `~/.bashrc`）中添加：

```bash
# Claw 审计记录别名
alias claw-exec='~/.openclaw/workspace/skills/claw-ops-manager/scripts/audit_wrapper.sh'
```

使用：
```bash
# 替代普通命令
claw-exec 'rm -rf ~/Desktop/截图'
claw-exec 'mv ~/Desktop/duyu ~/Downloads/duyu'
```

### 方案 2：Python 脚本使用（推荐给 Python 用户）

在你的 Python 脚本中：

```python
import sys
sys.path.insert(0, "~/.openclaw/workspace/skills/claw-ops-manager")

from scripts.auto_audit import audited_exec

# 所有命令自动记录
audited_exec("ls -la")
audited_exec("rm -rf ~/Desktop/截图")
```

### 方案 3：OpenClaw 技能集成（需要配置）

将以下代码添加到 OpenClaw 的工具执行流程中：

```python
from scripts.auto_audit import AuditedToolCall

auditor = AuditedToolCall()

# 包装每个工具调用
result = auditor.log_and_execute(
    tool_name="exec",
    action="run_command",
    parameters={"command": "ls -la"},
    execute_func=lambda: execute_command("ls -la")
)
```

## 快速测试

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/claw-ops-manager

# 测试自动记录
python3 scripts/auto_audit.py

# 访问 Web UI 查看记录
open http://localhost:8080
```

## 当前状态

✅ Web UI 运行中：http://localhost:8080
✅ 数据库已创建：~/.openclaw/audit.db
✅ 权限规则已配置
✅ 手动记录功能可用
⚠️  自动记录需要集成（选择上述方案之一）

## 推荐工作流程

1. **立即使用**：通过 Web UI 手动记录重要操作
2. **短期方案**：使用 shell 别名 `claw-exec`
3. **长期方案**：将集成代码添加到 OpenClaw 核心流程

## 手动记录操作

如果临时需要记录某个操作：

```bash
cd ~/.openclaw/workspace/skills/claw-ops-manager

python3 << 'EOF'
from scripts.logger import OperationLogger

logger = OperationLogger()
logger.log_operation(
    tool_name="exec",
    action="run_command",
    parameters={"command": "你的命令"},
    success=True,
    duration_ms=100,
    user="牢大"
)
EOF
```

## 查看 Web UI

访问 http://localhost:8080 可以：
- 查看所有操作记录
- 筛选和搜索
- 管理权限规则
- 创建快照
- 处理告警

## 下一步

需要我帮你：
1. 设置 shell 别名？
2. 创建完整的 OpenClaw 集成？
3. 添加自动记录到现有工作流？
