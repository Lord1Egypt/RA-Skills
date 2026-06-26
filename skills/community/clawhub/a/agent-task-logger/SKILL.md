# Agent Task Logger - Agent 任务日志系统

一个类似 Tomcat catalina.out 的实时任务日志系统，**自动检测 Agent 工作空间**，用于记录和展示 Agent 执行任务的进度。

## 🚀 快速使用

### 1. 初始化日志系统（自动检测工作空间）
```
初始化日志系统
```

### 2. 初始化日志系统（手动指定工作空间）
```
初始化日志系统 workspace=/path/to/workspace
```

### 2. 记录任务开始
```
记录任务开始 task-id=task-001 task-name="停止 Tomcat 8" estimated-time=5s
```

### 3. 记录执行命令
```
记录执行命令 task-id=task-001 command="cd /path && ./shutdown.sh"
```

### 4. 记录任务状态
```
记录任务状态 task-id=task-001 status="成功" actual-time=3.5s
```

### 5. 查看实时日志
```bash
tail -f /Users/openclaw/.openclaw/workspace/logs/agent-task.log
```

## 📋 参数说明

### 初始化日志系统
| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `workspace` | ❌ | 自动检测 | 工作空间根目录（可选，自动检测） |
| `log-dir` | ❌ | `logs` | 日志目录（相对于 workspace） |
| `log-file` | ❌ | `agent-task.log` | 日志文件名 |

### 工作空间自动检测

Skill 会自动检测 Agent 的工作空间位置，检测顺序：

1. `WORKSPACE` 环境变量
2. `OPENCLAW_WORKSPACE` 环境变量
3. 脚本所在目录的父目录
4. `~/.openclaw/workspace`
5. 当前目录

**无需手动指定工作空间，开箱即用！**

### 记录任务开始
| 参数 | 必填 | 说明 |
|------|------|------|
| `task-id` | ✅ | 任务唯一标识 |
| `task-name` | ✅ | 任务描述 |
| `estimated-time` | ❌ | 预估处理时间 |

### 记录执行命令
| 参数 | 必填 | 说明 |
|------|------|------|
| `task-id` | ✅ | 关联的任务 ID |
| `command` | ✅ | 执行的 shell 命令 |

### 记录任务状态
| 参数 | 必填 | 说明 |
|------|------|------|
| `task-id` | ✅ | 关联的任务 ID |
| `status` | ✅ | 任务状态（成功/失败/等待中） |
| `actual-time` | ❌ | 实际处理时间 |

## 💡 触发词

- 初始化日志系统
- 记录任务开始
- 记录执行命令
- 记录任务状态
- 记录任务完成
- 记录错误信息
- 查看任务日志

## 📝 日志格式

参考 Tomcat catalina.out 格式，中文显示：

```
04-3 月 -2026 17:38:00.000 INFO [agent-task-1] com.openclaw.agent.TaskExecutor.execute 任务：停止 Tomcat 8
04-3 月 -2026 17:38:00.100 INFO [agent-task-1] com.openclaw.agent.TaskExecutor.execute 执行命令：cd /path && ./shutdown.sh
04-3 月 -2026 17:38:03.500 INFO [agent-task-1] com.openclaw.agent.TaskExecutor.execute 状态：Tomcat 8 关闭完成
04-3 月 -2026 17:38:03.600 INFO [agent-task-1] com.openclaw.agent.TaskExecutor.execute 预估时间：5 秒 | 实际时间：3.5 秒
04-3 月 -2026 17:38:03.700 INFO [agent-task-1] com.openclaw.agent.TaskExecutor.execute 结果：成功
```

## 🔧 使用示例

### 示例 1：完整任务流程（自动检测工作空间）

```bash
# 1. 初始化（自动检测工作空间）
初始化日志系统

# 2. 开始任务
记录任务开始 task-id=deploy-001 task-name="部署 Java 项目" estimated-time=60s

# 3. 执行命令
记录执行命令 task-id=deploy-001 command="mvn clean package"

# 4. 记录状态
记录任务状态 task-id=deploy-001 status="成功" actual-time=45s

# 5. 完成任务
记录任务完成 task-id=deploy-001
```

### 示例 2：多任务并行

```bash
# 任务 1：编译后端
记录任务开始 task-id=backend-compile task-name="编译后端项目" estimated-time=30s
记录执行命令 task-id=backend-compile command="mvn compile"
记录任务状态 task-id=backend-compile status="成功" actual-time=25s

# 任务 2：打包前端
记录任务开始 task-id=frontend-build task-name="打包前端项目" estimated-time=45s
记录执行命令 task-id=frontend-build command="npm run build"
记录任务状态 task-id=frontend-build status="成功" actual-time=40s
```

### 示例 3：错误处理

```bash
记录任务开始 task-id=deploy-app task-name="部署应用" estimated-time=30s
记录执行命令 task-id=deploy-app command="./deploy.sh"
记录错误信息 task-id=deploy-app error="权限不足，需要 sudo"
记录任务状态 task-id=deploy-app status="失败" actual-time=5s
```

## 📊 日志级别

| 级别 | 说明 | 使用场景 |
|------|------|---------|
| `INFO` | 普通信息 | 任务开始、命令执行、状态更新 |
| `WARN` | 警告信息 | 非致命错误、性能警告 |
| `ERROR` | 错误信息 | 任务失败、异常 |
| `DEBUG` | 调试信息 | 详细调试输出 |

## 🛠️ 高级功能

### 查看任务统计
```bash
# 查看所有任务状态
grep "结果：" /Users/openclaw/.openclaw/workspace/logs/agent-task.log

# 查看失败任务
grep "结果：失败" /Users/openclaw/.openclaw/workspace/logs/agent-task.log

# 查看任务耗时
grep "实际时间：" /Users/openclaw/.openclaw/workspace/logs/agent-task.log
```

### 日志轮转
```bash
# 按日期归档日志
mv /Users/openclaw/.openclaw/workspace/logs/agent-task.log \
   /Users/openclaw/.openclaw/workspace/logs/agent-task-$(date +%Y%m%d).log
```

## ⚠️ 注意事项

1. **日志文件权限**：确保日志目录可写
2. **日志大小**：建议定期归档，避免文件过大
3. **并发写入**：支持多任务并发记录
4. **时间格式**：使用 24 小时制，精确到毫秒

## 📁 文件结构

```
workspace/
├── logs/
│   ├── agent-task.log          # 主日志文件
│   ├── agent-task-20260304.log # 归档日志
│   └── ...
└── skills/
    └── agent-task-logger/
        ├── SKILL.md            # 技能说明
        └── scripts/
            └── logger.sh       # 日志工具脚本
```

## 🔄 更新日志

- v1.0 - 初始版本，支持基本任务记录
- v1.1 - 添加中文支持
- v1.2 - 添加任务统计功能
