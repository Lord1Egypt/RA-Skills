---
name: agent-office
description: "Agent Office：创建本地 AI 员工、office worker、AI employee 与 multi-agent office team。每个员工以独立 HTTP Worker 运行，支持 openclaw / hermes / deerflow / cli / external / stub 六种引擎，适合 office automation、agent worker 管理与团队协作。"
homepage: https://clawhub.com
tags: [productivity, automation, multi-agent, office, worker, ai-employee]
version: "1.5.1"
requirements:
  cli:
    - openclaw
    - hermes
  system:
    - lsof
    - git
    - uv
  optional:
    - memory-cli
ports:
  range: "5011-5020"
  purpose: "one per worker HTTP server"
directories:
  read:
    - "~/.openclaw/agents/"
    - "~/.hermes/office/"
  write:
    - "~/.hermes/office/workers/"
    - "~/.hermes/office/state/"
    - "~/.hermes/office/deerflow-runtime/"
daemon:
  background: true
  autostart: false
---

# Agent Office

## 技能定位

这个技能用于把“员工”作为本地 HTTP Worker 管理：

- 每个员工有自己的 `worker_id`
- 每个员工占用一个端口
- 每个员工有自己的 `SOUL.md` 和日志目录
- 主控通过 `/tasks` 下发任务，通过 `/health` 和 `/state` 查看状态

搜索关键词：

- `agent-office`
- `agent office`
- `office worker`
- `AI employee`
- `agent worker`
- `multi-agent office`

发布名和本地目录名统一为 `agent-office`。文档中一律优先使用相对路径 `scripts/...`，避免路径漂移。

## 内置团队预设

除了单个员工创建外，技能还支持一键套用团队预设：

| 预设 | 说明 |
|------|------|
| `出版公司` | 主编、策划、校对、封设、发行，适合内容与出版流程 |
| `编程公司` | 产品、前端、后端、设计、测试、项目，适合软件交付流程 |

命令示例：

```bash
bash scripts/apply_preset.sh --list
bash scripts/apply_preset.sh 出版公司
bash scripts/apply_preset.sh 编程公司 --dry-run
```

## 支持的引擎

| 引擎 | 适用场景 | 实际调用 |
|------|----------|----------|
| `openclaw` | 通用员工、代码、调研、设计 | `openclaw agent --agent {worker_id}` |
| `hermes` | Hermes 生态员工 | `hermes agent --json --message` |
| `deerflow` | 外包型复杂任务 | 复用共享 DeerFlow runtime，并以内嵌 DeerFlow 团队执行链完成任务 |
| `cli` | 接大多数本地 CLI 员工 | 按 profile 调用 `codex` / `claude` / `aider` / `gemini` / `opencode` |
| `external` | 接入已在运行的现有 agent / worker | 把现成 HTTP worker 桥接成员工，保留上游设定与记忆 |
| `stub` | 测试、占位 | 不启动真实进程 |

### CLI 员工说明

`cli` 引擎用于把主流本地命令行代理接成一个办公室员工，而不是把它们硬编码成单独实现。

内置 profile：

| profile | 实际工具 | 传参方式 |
|---------|----------|----------|
| `codex` | OpenAI Codex CLI | 标准输入，默认走 `codex exec --skip-git-repo-check` |
| `claude-code` | Claude Code | 标准输入 |
| `aider` | Aider | `--message` |
| `gemini-cli` | Gemini CLI | 标准输入 |
| `opencode` | OpenCode | 标准输入 |

支持两种接法：

- 用内置 profile：适合常见 CLI，直接复用预设命令与超时
- 用 `--cli-cmd` 覆盖：适合本机有自定义包装命令的场景

常用命令：

```bash
python3 scripts/add_worker.py --list-cli-profiles
bash scripts/add_worker.sh 小扣 cli code --cli-profile codex
bash scripts/add_worker.sh 小克 cli code --cli-profile claude-code --workspace ~/projects/demo
bash scripts/add_worker.sh 小助 cli general --cli-cmd "codex exec --skip-git-repo-check" --cli-args "--model gpt-5.4"
```

Codex 员工要点：

- 不直接跑裸 `codex`，而是默认使用非交互模式 `codex exec`
- 默认补 `--skip-git-repo-check`，避免员工工作目录不是 trusted git repo 时直接失败
- 需要指定模型时，只追加自己的参数，例如 `--cli-args "--model gpt-5.4"`

### External 员工说明

`external` 引擎用于接入已经在本机某个端口跑着的现有 worker / agent，而不是重新创建一个新员工内核。

它的运行规则是：

- 上游 worker 保持原本的身份、workspace、长期记忆与系统提示
- Agent Office 只在办公室侧创建一个桥接员工
- 派单时会附加只读共享记忆上下文，再转发给上游
- 移除桥接员工时，不会删除上游 worker

常用命令：

```bash
bash scripts/add_worker.sh 外挂小龙 external general --external-upstream-port 18750
bash scripts/add_worker.sh 外挂小龙 external general --external-upstream-url http://127.0.0.1:18750
```

### DeerFlow 员工说明

`deerflow` 引擎用于把一个完整 DeerFlow 2.0 团队封装成办公室里的单个“外包型员工”。

它的运行规则是：

- 办公室共享一套 DeerFlow runtime，避免每个 DeerFlow 员工重复安装
- 每个 DeerFlow 员工单独持有自己的 `home`、`config`、线程与工作目录
- 新增 DeerFlow 员工时，技能会自动安装或复用共享 runtime
- 需要跟官方 DeerFlow 更新时，可直接执行 `bash scripts/update_deerflow_runtime.sh`

常用命令：

```bash
bash scripts/add_worker.sh 小D deerflow complex
bash scripts/add_worker.sh 小D deerflow complex --deerflow-update-runtime
bash scripts/update_deerflow_runtime.sh
```

## 当前约束

- 没有默认员工，所有员工必须显式添加。
- `deerflow` 员工在办公室中仍然是“一个员工”，但底层已切换为技能内嵌 DeerFlow runtime 团队。
- 共享记忆通过 `MEMORY_CLI` 以可选方式启用，未配置时不影响主流程。

## 实际目录结构

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

技能预设目录：

~/.hermes/skills/agent-office/presets/
├── publishing-company.json
└── coding-company.json
```

说明：

- `SOUL.md`：员工身份说明，由 `templates/` 渲染生成
- `config.json`：员工配置快照
- `worker.log`：启动与运行日志

## office_state.json 结构

```json
{
  "workers": {
    "xiaolong": {
      "name": "小龙",
      "port": 5011,
      "role": "research",
      "engine": "openclaw",
      "workspace_dir": "~/.hermes/office/workers/xiaolong",
      "status": "idle",
      "config_path": "~/.hermes/office/workers/xiaolong/config.json",
      "soul_path": "~/.hermes/office/workers/xiaolong/SOUL.md",
      "added_at": "2026-04-13T00:00:00",
      "last_active": null
    }
  },
  "port_pool": {
    "used": [5011],
    "available": [5012, 5013, 5014, 5015, 5016, 5017, 5018, 5019, 5020]
  }
}
```

## 添加员工流程

当用户说“添加一个员工，叫 XXX，职责是 YYY”时，按以下顺序执行：

### Step 1：生成 worker_id 与端口

- 中文名字转拼音 / ASCII 工号
- 从 `port_pool.available` 里取最小可用端口

### Step 2：创建目录

```bash
mkdir -p ~/.hermes/office/workers/{worker_id}/logs
```

### Step 3：生成 SOUL.md

从 `templates/` 里按引擎选模板并渲染：

| 引擎 | 模板文件 |
|------|----------|
| `openclaw` | `templates/openclaw_prompt.md` |
| `hermes` | `templates/hermes_prompt.md` |
| `deerflow` | `templates/deerflow_prompt.md` |
| `cli` | `templates/cli_prompt.md` |
| `external` | `templates/external_prompt.md` |
| `stub` | `templates/stub_prompt.md` |

模板变量包括：

- `{{NAME}}`
- `{{ROLE}}`
- `{{WORKER_ID}}`
- `{{PORT}}`
- `{{ROLE_DESCRIPTION}}`
- `{{TIMEOUT}}`

### Step 4：注册 agent / 准备运行时

- `openclaw` / `hermes` 引擎会注册本地 agent
- `cli` 引擎写入 CLI profile / 命令配置
- `deerflow` 引擎会自动准备共享 DeerFlow runtime、员工独立 home 与 runtime config

```bash
openclaw agents add {worker_id} --workspace ~/.hermes/office/workers/{worker_id}
```

### Step 5：启动 worker_server.py

```bash
python3 worker_server.py \
  --port {port} \
  --worker-id {worker_id} \
  --name {name} \
  --role {role} \
  --engine {engine} \
  --workspace-dir {workspace_dir}
```

### Step 6：严格健康检查

必须满足：

- `/health` 返回 HTTP `200`
- 响应体里 `status == "ok"`

只要有一项不满足，员工状态就记为 `not_ready`，不会误记成 `idle`。

## worker_server 行为

### API

| 方法 | 路径 | 用途 |
|------|------|------|
| `GET` | `/health` | 存活检查 |
| `GET` | `/state` | 当前员工状态 |
| `POST` | `/tasks` | 创建任务 |
| `GET` | `/tasks/{task_id}` | 查任务状态或结果 |
| `GET` | `/tasks/{task_id}/result` | 只取结果 |

### 关键实现约束

- `openclaw` 员工执行任务时必须使用 `worker_id`，不能直接用中文显示名
- 任务标题不能通过全局共享变量透传，避免并发串单
- `hermes` 子进程在员工工作目录执行，方便读本地上下文与日志
- `deerflow` 任务通过技能内的 `deerflow_runtime_runner.py` 调共享 runtime，并读取员工独立 home/config

## 命令参考

以下命令都建议在技能目录中执行：

### 添加员工

```bash
bash scripts/add_worker.sh 小龙 openclaw research
bash scripts/add_worker.sh 小扣 cli code --cli-profile codex
```

### 应用团队预设

```bash
bash scripts/apply_preset.sh 出版公司
bash scripts/apply_preset.sh 编程公司 --dry-run
```

### 查看团队

```bash
bash scripts/list_workers.sh
```

### 健康检查

```bash
bash scripts/demo.sh
```

### 移除员工

```bash
bash scripts/remove_worker.sh 小龙
bash scripts/remove_worker.sh xiaolong
```

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `HERMES_OFFICE_DIR` | `~/.hermes/office` | 办公室目录 |
| `MEMORY_CLI` | 空 | MemPalace CLI 路径 |
| `AGENT_OFFICE_DEERFLOW_REPO_URL` | `https://github.com/bytedance/deer-flow.git` | DeerFlow runtime 来源仓库 |
| `AGENT_OFFICE_DEERFLOW_UPDATE_ON_ADD` | `0` | 设为 `1` 时，每次新增 DeerFlow 员工前都先更新共享 runtime |

## 发布前自检

至少验证下面几项：

1. `python3 -m py_compile worker_server.py scripts/add_worker.py scripts/remove_worker.py scripts/apply_preset.py scripts/run_flow.py`
2. `bash -n scripts/add_worker.sh scripts/list_workers.sh scripts/demo.sh scripts/remove_worker.sh scripts/apply_preset.sh scripts/run_flow.sh`
3. 添加一个 `stub` 员工，确认状态写入正常
4. 添加一个 `openclaw` 员工，确认 `/health` 正常
5. 添加一个 `cli` 员工，确认 `--list-cli-profiles` 与 worker 启动正常
6. 添加一个 `deerflow` 员工，确认共享 runtime 初始化、任务回传与离职清理正常
7. 提交一个任务，确认 `/tasks/{id}` 能返回 `done`

## 版本说明

### 1.4.2

- 修复 DeerFlow 沙箱默认挂载范围过宽的问题，不再把整个办公室目录暴露给 DeerFlow 子任务
- 当前 DeerFlow 员工默认只暴露 `/mnt/workspace` 与 `/mnt/worker`，避免误读其他员工目录
- 补充隔离挂载与模板边界约束测试，验证小D不会再串读小龙资料

### 1.4.1

- 移除 `1.4.0` 中误写到 DeerFlow 模板与文档里的旧网关 / 旧目录调试说明
- 将 `templates/deerflow_prompt.md` 恢复为与当前内嵌 runtime 架构一致的员工说明
- 校正文档版本说明，避免后续员工和经理被旧 DeerFlow 资产误导

### 1.3.0

- `deerflow` 引擎改为技能内嵌 DeerFlow runtime，不再依赖外部 `deerflow-worker` 网关
- 新增共享 runtime + 每员工独立 home/config 设计
- 新增 `scripts/update_deerflow_runtime.py` / `.sh`，可直接跟随官方 DeerFlow 更新
- 新增 DeerFlow runtime 相关测试与真实隔离烟测

### 1.2.0

- 新增 `cli` 引擎，可把主流本地 CLI 直接接成员工
- 内置 `codex`、`claude-code`、`aider`、`gemini-cli`、`opencode` 五个 profile
- 支持 `--cli-profile`、`--cli-cmd`、`--cli-args`、`--cli-timeout`、`--workspace`
- 新增 `templates/cli_prompt.md` 与对应测试

### 1.1.0

- 新增 `apply_preset.py` / `apply_preset.sh`
- 内置 `出版公司` 与 `编程公司` 两组团队预设
- 预设支持 `--list` 和 `--dry-run`

### 1.0.1

- 增强技能描述与标签，优化 `agent office` / `office worker` / `AI employee` 等搜索命中

### 1.0.0

- 修复 `worker_name` 被误当作 `worker_id` 的执行错误
- 启动后改为严格健康检查，不再用宽松返回码误判就绪
- `SOUL.md` 改为真实使用 `templates/` 渲染
- shell 入口收敛到 Python 主实现，减少逻辑漂移
- 文档与真实目录结构、命令路径、默认员工说明重新对齐
