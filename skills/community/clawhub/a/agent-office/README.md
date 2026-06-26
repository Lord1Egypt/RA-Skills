# Agent Office

一句话加员工，构建本地 AI office、office worker、AI employee 团队。员工以独立 HTTP Worker 形式运行，支持 `openclaw`、`hermes`、`deerflow`、`cli`、`external`、`stub` 六种引擎。

## 包名与目录名

- ClawHub / 技能市场发布名：`agent-office`
- 本地目录名：`agent-office`

## 前置要求

- `openclaw`：用于 `openclaw` 引擎
- `hermes`：用于 `hermes` 引擎
- `git`：用于首次拉取或更新共享 DeerFlow runtime
- `uv`：用于安装 / 更新共享 DeerFlow runtime 依赖
- `lsof`：用于移除员工时查进程
- 如需 `cli` 员工：本机需已安装对应 CLI

示例安装：

```bash
pip install openclaw
pip install hermes-ai
```

说明：

- `deerflow` 员工不需要你先手工维护一套外部 DeerFlow 网关
- 首次添加 `deerflow` 员工时，技能会自动安装或复用办公室共享 DeerFlow runtime
- 后续如需跟进官方更新，可直接运行 `bash scripts/update_deerflow_runtime.sh`

## 快速开始

先进入技能目录：

```bash
cd /path/to/agent-office
```

添加员工：

```bash
bash scripts/add_worker.sh 小龙 openclaw research
bash scripts/add_worker.sh 小扣 cli code --cli-profile codex
bash scripts/add_worker.sh 小D deerflow complex
bash scripts/add_worker.sh 外挂小龙 external general --external-upstream-port 18750
```

应用团队预设：

```bash
# 查看可用预设
bash scripts/apply_preset.sh --list

# 一键创建出版公司
bash scripts/apply_preset.sh 出版公司

# 只预览，不真正创建
bash scripts/apply_preset.sh 编程公司 --dry-run
```

查看团队：

```bash
bash scripts/list_workers.sh
```

健康检查：

```bash
bash scripts/demo.sh
```

移除员工：

```bash
bash scripts/remove_worker.sh 小龙
# 或
bash scripts/remove_worker.sh xiaolong
```

## 引擎说明

| 引擎 | 用途 | 实际行为 |
|------|------|----------|
| `openclaw` | 通用执行、代码、调研、设计 | 以 `worker_id` 调用 `openclaw agent --agent {worker_id}` |
| `hermes` | Hermes 生态任务 | 通过 `hermes agent` 执行，并在员工工作目录运行 |
| `deerflow` | 外包型复杂任务 | 自动安装或复用共享 DeerFlow runtime，并以单个员工身份调起内嵌 DeerFlow 团队执行链 |
| `cli` | 接主流本地 CLI 员工 | 按 profile 调用对应 CLI，可接 Codex / Claude Code / Aider / Gemini CLI / OpenCode |
| `external` | 接入已在运行的现有 agent / worker | 保留上游原设定和记忆不动，在办公室里挂一个桥接员工并注入共享记忆上下文 |
| `stub` | 测试 / 占位 | 不启动真实进程，直接返回模拟结果 |

## CLI 员工

`cli` 引擎适合把大多数主流命令行代理接成办公室员工，不需要为每个 CLI 单独做一套 worker 实现。

当前内置 profile：

| profile | 工具 | 说明 |
|------|------|------|
| `codex` | OpenAI Codex CLI | 默认走 `codex exec --skip-git-repo-check`，适合后台 worker 非交互调用 |
| `claude-code` | Claude Code | 走标准输入 |
| `aider` | Aider | 使用 `--message` 传任务 |
| `gemini-cli` | Gemini CLI | 走标准输入 |
| `opencode` | OpenCode | 走标准输入 |

先看支持列表：

```bash
python3 scripts/add_worker.py --list-cli-profiles
```

直接添加内置 CLI 员工：

```bash
bash scripts/add_worker.sh 小扣 cli code --cli-profile codex
bash scripts/add_worker.sh 小克 cli code --cli-profile claude-code --workspace ~/projects/demo
bash scripts/add_worker.sh 小助 cli general --cli-profile aider
```

Codex 员工的默认接法已经内置为：

```text
codex exec --skip-git-repo-check
```

原因：

- worker_server 是后台 HTTP worker，不能依赖交互式 TTY，所以不能直接跑裸 `codex`
- 员工工作目录通常不是 trusted git repo，默认补 `--skip-git-repo-check` 更稳
- 如需指定模型，只需要追加你自己的参数，例如 `--cli-args "--model gpt-5.4"`

如果你的机器上用了自定义包装命令，也可以覆盖：

```bash
bash scripts/add_worker.sh 小试 cli code --cli-cmd "codex exec --skip-git-repo-check" --cli-args "--model gpt-5.4" --workspace ~/projects/demo
```

说明：

- `--workspace` 控制 CLI 真正工作的目录，不填时默认用员工目录
- `--cli-timeout` 可覆盖默认超时
- `--cli-cmd` 适合你本机已经封装好命令的情况
- `cli` 员工不会注册成 openclaw agent，而是由 `worker_server.py` 直接调本地 CLI

## 外挂现有员工

`external` 引擎适合把已经在本机跑起来的现有 agent / worker 直接挂进 Agent Office，当成一名办公室员工来派单。

典型场景：

- 你本机 `18750` 端口已经跑着一个 openclaw / 其他兼容 worker
- 你不想改它原有的 workspace、系统提示、长期记忆
- 但你想让办公室给它派单，并在派单时附带共享记忆上下文

使用方式：

```bash
bash scripts/add_worker.sh 外挂小龙 external general --external-upstream-port 18750
# 或
bash scripts/add_worker.sh 外挂小龙 external general --external-upstream-url http://127.0.0.1:18750
```

说明：

- `external` 员工是办公室里的桥接代理，不会重写上游 agent 的设置
- 共享记忆只在办公室转发任务时作为附加上下文注入
- 移除 `external` 员工时，只会删除办公室这层代理，不会动上游进程
- 上游需要兼容 `GET /health`、`POST /tasks`、`GET /tasks/{id}` 这套 HTTP 协议

## DeerFlow 员工

`deerflow` 引擎适合“外包团队型”员工。对办公室来说它仍然只是一个员工，但员工内部会以 DeerFlow 2.0 团队方式接任务、拆任务、汇总结果。

核心设计：

- 办公室只维护一套共享 DeerFlow runtime，默认放在 `~/.hermes/office/deerflow-runtime/deer-flow`
- 每个 DeerFlow 员工有自己独立的 `home`、`config`、线程与工作目录，互不串线
- 默认模型是 `gpt-5.4`，默认 `reasoning_effort=medium`
- 员工创建时可选先更新官方 runtime，后续也可单独执行更新脚本

常用命令：

```bash
bash scripts/add_worker.sh 小D deerflow complex
bash scripts/add_worker.sh 小D deerflow complex --deerflow-update-runtime
bash scripts/update_deerflow_runtime.sh
```

如果你想固定到自己的 DeerFlow fork，也可以在创建前指定：

```bash
export AGENT_OFFICE_DEERFLOW_REPO_URL=https://github.com/your-org/deer-flow.git
```

如果你希望每次新增 DeerFlow 员工前都自动拉一次最新官方代码：

```bash
export AGENT_OFFICE_DEERFLOW_UPDATE_ON_ADD=1
```

## 团队预设

当前内置两组预设：

| 预设 | 适合场景 | 典型员工 |
|------|----------|----------|
| `出版公司` | 选题、编辑、校对、封设、发行 | 主编、策划、校对、封设、发行 |
| `编程公司` | 需求、设计、前后端开发、测试、项目推进 | 产品、前端、后端、设计、测试、项目 |

预设文件位于 `presets/` 目录，后续你可以继续扩展新的公司模板。

## 真实运行流程

执行 `add_worker.py` 时会做这些事：

1. 中文名字转 `worker_id`，并分配端口。
2. 在 `templates/` 中选模板，渲染成员工专属 `SOUL.md`。
3. 为 `openclaw` / `hermes` 员工注册对应 agent workspace；`cli` 员工写入 CLI 配置；`deerflow` 员工自动准备共享 runtime、独立 home 与 runtime config；`external` 员工写入上游桥接配置。
4. 启动 `worker_server.py`。
5. 严格检查 `http://127.0.0.1:{port}/health` 是否返回 `200` 且 `{"status":"ok"}`。
6. 写入 `office_state.json`。

## 目录结构

默认办公室目录：

```text
~/.hermes/office/
├── deerflow-runtime/
│   ├── deer-flow/
│   └── homes/
│       └── {worker_id}/
├── state/
│   └── office_state.json
└── workers/
    └── {worker_id}/
        ├── SOUL.md
        ├── config.json
        └── logs/
            └── worker.log
```

说明：

- `SOUL.md`：员工身份与任务规范，由模板渲染生成
- `config.json`：员工配置快照
- `worker.log`：启动和运行日志
- `deerflow-runtime/`：办公室共享 DeerFlow runtime，以及各 DeerFlow 员工独立 home

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `HERMES_OFFICE_DIR` | `~/.hermes/office` | 办公室状态与员工目录 |
| `MEMORY_CLI` | 空 | 启用共享记忆 CLI 路径 |
| `AGENT_OFFICE_DEERFLOW_REPO_URL` | `https://github.com/bytedance/deer-flow.git` | DeerFlow runtime 来源仓库 |
| `AGENT_OFFICE_DEERFLOW_UPDATE_ON_ADD` | `0` | 设为 `1` 时，每次新增 DeerFlow 员工前都先更新共享 runtime |

## 故障排除

| 问题 | 常见原因 | 处理方式 |
|------|----------|----------|
| 员工状态是 `not_ready` | 进程启动了，但健康检查没通过 | 查看 `workers/{worker_id}/logs/worker.log` |
| 添加时报 `openclaw 未安装` | CLI 未安装或不在 PATH | 先执行 `pip install openclaw` |
| 添加时报 `hermes 未安装` | CLI 未安装或不在 PATH | 先执行 `pip install hermes-ai` |
| 添加 `deerflow` 员工时报缺少自动安装依赖 | 本机没有 `git` 或 `uv` | 先安装 `git` / `uv`，再重试 |
| DeerFlow 员工能启动但任务失败 | DeerFlow runtime 配置或上游模型配置有误 | 查看 `workers/{worker_id}/logs/worker.log`，必要时执行 `bash scripts/update_deerflow_runtime.sh` 后重试 |
| 添加 `cli` 员工时报 profile 不可用 | 对应 CLI 不在 PATH，或命令覆盖写错 | 先执行 `python3 scripts/add_worker.py --list-cli-profiles`，再检查 `which codex` / `which claude` 等 |
| 添加 `external` 员工时报无法连通上游 | 上游端口未启动，或不兼容 HTTP worker 协议 | 先检查上游 `GET /health` 是否返回 `{"status":"ok"}` |
| 添加时报 `没有可用端口` | 5011-5020 端口池耗尽 | 先移除不用的员工 |
| 员工能创建但任务失败 | `worker_id` / agent 未注册完整 | 重新添加该员工，让脚本重新注册 |

## 当前约束

- 没有默认员工，团队成员由用户显式添加。
- `deerflow` 员工本质上仍是办公室里的单个外包入口，但底层已改为技能内嵌的 DeerFlow runtime 团队执行链。
- 共享记忆是可选功能，未配置 `MEMORY_CLI` 时不会影响主流程。

## 版本历史

| 版本 | 日期 | 更新 |
|------|------|------|
| 1.5.0 | 2026-04-16 | 新增 `external` 引擎，可把已在运行的现有 agent / worker 作为桥接员工接入办公室；保留上游设定与记忆不动，并在办公室侧注入共享记忆 |
| 1.4.2 | 2026-04-14 | 修复 DeerFlow 沙箱挂载范围过宽导致可能串读其他员工目录的问题；当前只暴露 `/mnt/workspace` 与 `/mnt/worker`，并补充隔离验证 |
| 1.4.1 | 2026-04-13 | 修正 `1.4.0` 中误写到 DeerFlow 模板与文档里的旧调试说明；恢复与当前内嵌 runtime 架构一致的 DeerFlow 员工说明 |
| 1.3.0 | 2026-04-13 | `deerflow` 引擎改为技能内嵌 DeerFlow runtime；支持共享 runtime、每员工独立 home/config、`update_deerflow_runtime` 更新脚本；不再依赖外部 `deerflow-worker` 网关 |
| 1.2.0 | 2026-04-13 | 新增 `cli` 引擎，支持主流 CLI 员工接入；内置 `codex`、`claude-code`、`aider`、`gemini-cli`、`opencode` profiles；支持自定义 `--cli-cmd` / `--workspace` |
| 1.1.0 | 2026-04-13 | 新增团队预设：支持 `出版公司` 与 `编程公司` 一键建组；补充 `apply_preset` 脚本与测试 |
| 1.0.1 | 2026-04-13 | 优化搜索可见性：补充 `agent office`、`office worker`、`AI employee` 等关键词与标签 |
| 1.0.0 | 2026-04-13 | 首个稳定可发布版本；修复 `worker_id` 调用错误；严格化健康检查；接通模板渲染；统一 shell/python 入口；同步 README 与实现 |
