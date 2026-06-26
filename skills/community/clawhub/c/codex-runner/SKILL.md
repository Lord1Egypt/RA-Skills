# codex-runner Skill

## 描述

使用 Codex CLI 在后台长时间运行编码任务，不受 OpenClaw 会话限制。

## ⚠️ 重要：异步执行

**此 skill 会立即返回，不阻塞主会话！**

任务在后台独立运行，你可以：
- 继续与 OpenClaw 对话
- 发送新消息
- 查看日志进度

## 使用场景

- 需要 Agent 整夜写代码
- 长时间运行的大型项目开发
- 不希望 OpenClaw 会话超时导致任务中断

## 前提条件

- 已安装 Codex CLI (`npm install -g @openai/codex`)
- 配置好代理（翻墙）
- 目标目录需要是 git 仓库（`git init`）

## 命令

### start

启动 Codex 后台任务（**异步执行，不阻塞会话**）

```bash
codex-runner start "实现一个 React TODO 应用" my-task /Users/tianyanan/my-project
```

**参数：**
- `$1`: 任务描述
- `$2`（可选）: 任务名称，用于日志文件命名，默认 `codex-task`
- `$3`（可选）: 目标目录路径，默认当前目录

**关键：必须使用 `background=true` 执行！**

由于 OpenClaw 默认同步等待命令完成，你需要这样调用：

```bash
# 在 skill 命令中使用 background 参数
```

或者直接使用 `sessions_spawn` 创建独立子会话：

```bash
# 让 Codex 在独立会话中运行，不影响主会话
```

### status

检查 Codex 进程状态

```bash
codex-runner status
```

### log

查看任务日志

```bash
codex-runner log my-task
```

参数：
- `$1`（可选）: 任务名称，默认 `codex-task`

### stop

停止 Codex 任务

```bash
codex-runner stop
```

## 解决方案：使用 sessions_spawn

由于 OpenClaw 主会话执行 exec 会被阻塞，最佳方案是使用 **sessions_spawn** 创建独立子会话来运行 Codex。

### 使用方法

直接让 AI 助手（我）使用 sessions_spawn 启动任务：

```bash
# 我会这样执行：
sessions_spawn {
  "runtime": "subagent",
  "task": "在 ~/my-project 实现一个简单的 Hello World",
  "label": "codex-hello"
}
```

### 示例：启动 Codex 任务

**你可以说**："用 codex 在桌面创建 test 文件夹，里面放一个 hello.txt"

**我会这样处理**：
1. 使用 sessions_spawn 创建独立子会话
2. 子会话中运行 Codex 执行任务
3. 主会话立即返回，继续响应你

---

## 旧版命令（会阻塞，仅作备用）

### start（已不推荐）

```bash
# 使用 --dangerously-bypass-approvals-and-sandbox 完全跳过沙箱
TASK_NAME=${2:-codex-task}
TARGET_DIR=${3:-.}

nohup bash -c "
  cd '$TARGET_DIR'
  
  export https_proxy=http://127.0.0.1:8118
  export http_proxy=http://127.0.0.1:8118
  
  codex --dangerously-bypass-approvals-and-sandbox exec '$1'
" > ~/.codex-logs/codex-$TASK_NAME.log 2>&1 &
```

### ⚠️ 关键参数

**必须使用 `--dangerously-bypass-approvals-and-sandbox`** 才能写入文件：

```bash
codex --dangerously-bypass-approvals-and-sandbox exec '任务描述'
```

| 参数 | 说明 |
|------|------|
| `--dangerously-bypass-approvals-and-sandbox` | 完全跳过沙箱和审批（必须） |
| `exec` | 非交互执行模式 |

### ⚠️ 注意

- 目标目录需要是 git 仓库（`git init`）
- 使用此参数会有安全风险，确保在安全环境下使用

## 开发任务模板（重要！）

建议在任务描述中包含以下流程要求：

```bash
codex-runner start "
实现一个用户管理系统，包含：
1. 用户增删改查 API
2. 用户列表页面

开发流程要求：
1. 先写单元测试，再写业务代码
2. 编码完成后执行单元测试：npm test
3. 如果单测失败，自动修复直到通过
4. 单测通过后执行构建：npm run build
5. 如果构建失败，自动修复直到通过
6. 单测和构建都通过后才算任务完成
" my-task /Users/tianyanan/my-project
```

### 开发流程规范

| 步骤 | 要求 |
|------|------|
| 1. 单元测试 | 先写测试，再写业务代码 |
| 2. 执行单测 | `npm test` 或 `npm run test` |
| 3. 修复单测 | 如果失败，自动修复直到通过 |
| 4. 执行构建 | `npm run build` |
| 5. 修复构建 | 如果失败，自动修复直到通过 |
| 6. 完成标志 | 单测 + 构建都通过 |

## 监控方法

```bash
# 查看进程
ps aux | grep codex | grep -v grep

# 实时日志
tail -f ~/.codex-logs/codex-my-task.log

# 检查完成标志
grep "已完成\|build\|test" ~/.codex-logs/codex-my-task.log
```

## 日志位置

- 默认: `~/.codex-logs/codex-<任务名>.log`

## 测试结果

- ✅ 持续运行稳定
- ✅ 可以写入文件（使用 --dangerously-bypass-approvals-and-sandbox）
- ✅ 生成完整 React 项目
- ✅ 构建验证通过

## 参考

- 源自 Eliason 的 Agent 整夜写代码方案
- 测试时间: 2026-03-04 ~ 2026-03-05
- 更新: 2026-03-05（增加开发流程规范）
