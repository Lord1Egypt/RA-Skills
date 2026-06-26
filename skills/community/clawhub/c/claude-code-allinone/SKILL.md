---
name: claude-code-allinone
description: ArkClaw / OpenClaw 沙箱里一键安装并配置 Anthropic Claude Code CLI 的 all-in-one skill。当用户提到 claude code、claude-code、想在 ArkClaw 里用 Anthropic 官方 Coding CLI、提到 ark-code-latest / 火山方舟 AgentPlan 接 claude code、想切换 claude code 的模型供应商、需要做代码 review / 代码改写、或者说"我没有 Anthropic 官方 API Key 但想用 claude code"时,使用本 skill。
license: MIT
---

# Claude Code All-in-One for ArkClaw

让 ArkClaw / OpenClaw 用户在**对话框里**完成 Claude Code CLI 的全部配置 — 不用打开终端、不用手写 `~/.claude/settings.json`、不用记 base_url。本 skill 还内置 **review / build 双模式智能路由**:

- **review 模式**(`--permission-mode plan`):只读分析,不改文件,适合代码审查 / 评估改造方案
- **build 模式**(`--allowedTools` 白名单):允许 Read / Edit / Write / Bash 等动手工具,适合实现代码

---

## 整体流程(决策树)

```
用户触发本 skill(说"用 claude code 帮我..." / "/claude-code-allinone ..." / 报错 等)
        │
        ▼
  ┌───────────────────────────┐
  │ 运行 scripts/doctor.sh    │  ← 每次触发都会运行,检测当前环境状态
  └─────────────┬─────────────┘
                │
       当前配置状态 = ?
                │
  ┌─────────────┼──────────────────────────────────┐
  │             │                                  │
"全新环境"    "本 skill 配过"                   "用户手动配过"
(从未配置)   (之前用本 skill 配置的)          (有 settings.json/config 但不是本 skill 写的)
  │             │                                  │
  ▼             ▼                                  ▼
路径 ①        路径 ②                             路径 ③
首次配置      正常使用(绝大多数情况)              兼容性检查
  │             │                                  │
  │             │                                  ├─ 检查通过 → 保留不动,转到路径 ②
  │             │                                  └─ 检查不通过 → 告知用户具体问题,
  │             │                                       询问是否用本 skill 重新配置
  │             │
问用户选择   智能判定 review/build 模式
A/B 菜单     然后执行: claude -p "用户的需求" --permission-mode plan
  │              或:    claude -p "用户的需求" --allowedTools <白名单>
  ▼
完成配置后
转到路径 ②
```

### 三条路径说明

| 路径 | 什么时候走 | 用户需要做什么 |
|---|---|---|
| ① 首次配置 | 环境里从未配过 claude code,或用户主动要求重新配置 | **默认直接走 AgentPlan**,优先尝试自动从 ArkClaw 沙箱环境变量(`ARK_AGENT_PLAN` / `ARK_CODING_PLAN` / `ARK_API_KEY`)零感知配好;失败再让用户粘贴一次 Key。**用户主动说"我有自己的 Anthropic 兼容网关 / 别的 base_url / 自定义模型"时才走 custom 分支** |
| ② 正常使用 | 已经配好了(本 skill 配的,或用户自配且体检通过) | **什么都不用做**,直接说编程需求即可 |
| ③ 兼容性检查 | 用户手动写过 settings.json,本 skill 首次遇到 | 如果检查通过:无需操作;如果不通过:选择重配或自己修 |

---

## 重要:正常使用时不要打扰用户

当配置已经就绪(路径 ②)时,**不允许**:

- 复述配置流程
- 解释 skill 在做什么
- 询问"是否需要切换 / 是否需要重新配置"
- 把 skill 的存在感暴露给用户

**只做**:
1. 运行 `bash scripts/ensure-onboarding.sh`(确保 `~/.claude.json` 标记 onboarding 完成)
2. 调用 `bash scripts/run.sh "用户的完整需求原文"`(自动判定 review / build 模式)
3. 把 claude code 的输出原样返回给用户

**用户体验**应该等同于"直接跟 claude code 对话",完全感觉不到 skill 的存在。

只有这三种情况允许打扰用户:
1. 首次配置(环境全新)
2. 兼容性检查不通过,且无法自动修复
3. 用户主动说"切换 / 换一家 / 切到 X"

---

## 触发方式

- **自然语言**:"用 claude code 帮我重构 utils.py" / "claude code review 一下这个 PR"
- **显式命令**:`/claude-code-allinone <你的编程需求>`(强制走本 skill)
- **报错触发**:用户贴出 `command not found: claude` / `Onboarding has not been completed` / `ANTHROPIC_AUTH_TOKEN is not set` 等

---

## 详细流程

### Step 0 — 运行 doctor.sh 检测环境

每次触发都先运行 `bash scripts/doctor.sh`,它会输出一个 JSON,包含:

```json
{
  "claude_installed": true,
  "claude_version": "2.1.143",
  "claude_outdated": false,
  "config_state": "clean | managed-by-skill | user-managed",
  "active_profile": "agentplan | custom | null",
  "user_settings_summary": {"base_url": "...", "model": "..."} | null,
  "user_health": {"is_healthy": true/false, "checks": [...], "issues": [...]} | null,
  "onboarding_complete": true,
  "ark_api_key_set": true,
  "custom_api_key_set": false,
  "ark_managed_env": true,
  "ark_agent_plan": true,
  "ark_coding_plan": false,
  "ark_api_key_managed": true,
  "ark_model_id": "ark-code-latest",
  "issues": []
}
```

根据 `config_state` 决定走哪条路径。

### Step 1 — 安装 / 升级 Claude Code CLI(仅首次需要)

`scripts/install.sh` 的行为:

| 当前状态 | 行为 |
|---|---|
| 未安装 claude | 通过 npm 安装 `@anthropic-ai/claude-code@latest` |
| 版本低于 2.1.0 | 升级到最新 |
| 已是最新版 | 跳过,不做任何事 |

### Step 2 — 配置模型服务(仅路径 ① 触发)

**默认行为:不问选项,直接走 AgentPlan**

减少用户感知是核心原则。**不要主动给用户列 A/B 菜单**。除非用户主动说"我有自己的 Anthropic 兼容网关 / 自定义 base_url / 别的模型 Key",否则一律默认进入 AgentPlan 配置流程。

#### 零感知首选:扫环境变量自动配好

ArkClaw / OpenClaw 沙箱会**自动注入**当前账号的套餐和 Key 信息,本 skill 应**优先利用这些变量做零感知配置**,避免让用户再粘贴一次 Key。

doctor.sh 输出会包含:

```json
{
  "ark_managed_env": true,
  "ark_agent_plan": true,
  "ark_coding_plan": false,
  "ark_api_key_set": true,
  "ark_api_key_managed": true,
  "ark_model_id": "ark-code-latest"
}
```

| `ark_managed_env` | 套餐标识 | `ark_api_key_set` | 应执行的动作 |
|---|---|---|---|
| true | `ark_agent_plan=true` 且 `ark_coding_plan!=true` | true | **零感知配置 (AgentPlan)**:直接 `bash scripts/setup-agentplan.sh --auto`,**完全不要询问用户** |
| true | `ark_coding_plan=true` 且 `ark_agent_plan!=true` | true | **零感知配置 (Coding Plan)**:直接 `bash scripts/setup-codingplan.sh --auto`。⚠️ 注意 **Coding Plan 与 AgentPlan 是两套不同套餐**,Key 互不通用,base_url 也不一样(coding vs plan),**绝不能套用 AgentPlan profile** |
| true | **两个都为 true(双开)** | true | **优先 AgentPlan**:直接 `bash scripts/setup-agentplan.sh --auto`。脚本内置预校验,若 AgentPlan Key 401 会**自动 fallback** 到 `setup-codingplan.sh --auto --from-fallback`,**全程零感知,不需要询问用户** |
| true | 两个都没标 | true | 默认 `bash scripts/setup-agentplan.sh --auto`(并打印一条 warning,401 时再切 codingplan) |
| false 或 `ark_api_key_set=false` | — | — | 走"传统首次配置":告知用户使用 AgentPlan,引导粘贴一次 Key |

> 实现细节:`setup-agentplan.sh --auto` 内部带**三层防护**:(1) 本地格式自检挡掉粘错的输入;(2) 调用 `/models` endpoint 做活性 ping(不消耗推理 token,3 次重试,仅 401/403 视为失败);(3) AgentPlan 401 且 `ARK_CODING_PLAN=true` 时自动 `exec` 转发到 `setup-codingplan.sh --auto --from-fallback`。所以即使 skill 选错或双开账号 AgentPlan Key 失效,都不会真的把错 Key 写进 profile。

#### 传统首次配置(仅在零感知不可用时触发)

向用户输出:

```
准备给你配置 Claude Code,使用火山方舟 AgentPlan(套餐内额度,ark-code-latest 智能路由)。

请粘贴 AgentPlan 控制台分配的专属 Key:
```

拿到 Key 后立即跑:
```bash
bash scripts/setup-agentplan.sh "$KEY"
```

#### 何时走自定义网关分支?

只有以下情况才询问/触发 custom 流程,**不要主动给用户列菜单**:

- 用户**主动**说:"我有自己的 Anthropic 网关" / "用我们公司的 base_url" / "我有 claude-code-router" / "用 Bedrock / Vertex 转出来的端点"
- 用户**主动**给出 base_url + Key + model 三件套
- 用户**主动**说"我没有 AgentPlan Key,但我有别的 Anthropic 兼容端点"

触发后引导用户依次给出 3 个信息,然后跑:
```bash
bash scripts/setup-custom.sh "$BASE_URL" "$KEY" "$MODEL"
```

> ⛔ **不允许**在用户没提"自定义/别的网关/我的 Key"等关键词时,主动展示 A/B 菜单或让用户做选择。这会增加感知,违背"默认 AgentPlan + 零感知优先"原则。

配置脚本会自动完成:写 Key → 写 settings.json → 写 `~/.claude.json` 的 `hasCompletedOnboarding: true` → `.token` 文件落盘。如果用户已有 `settings.json`,会**先备份**再覆盖。

### Step 3 — 兼容性检查(仅路径 ③ 触发)

当 doctor.sh 返回 `config_state == "user-managed"` 时,说明用户之前手动写过 settings.json。此时读取 `user_health` 字段:

**检查通过**(`is_healthy == true`):
- 不打扰用户,直接当作"已配好",进入正常使用

**检查不通过**(`is_healthy == false`):
向用户展示具体问题,并询问:

```
检测到你已有的 claude code 配置存在以下问题:
  1. <具体问题描述>
  2. <具体问题描述>

你希望:
  A. 让本 skill 帮你重新配置(推荐,会先备份你现有的文件)
  B. 我自己去修改

请回复 A 或 B。
```

### Step 4 — 正常使用(智能路由 review / build 模式)

```bash
bash scripts/run.sh "用户的完整需求原文"
```

`run.sh` 内部会:
1. 关键词扫描决定 mode:
   - 命中 "review / 评审 / 审查 / 看一下 / 分析 / 评估 / 检查 / lint / 评 / read-only" → **review 模式**(`--permission-mode plan`)
   - 否则默认 **build 模式**(`--allowedTools "Read,Glob,Grep,LS,Bash,Edit,Write"`)
2. 用 `nohup setsid + </dev/null + log file + 110s PID polling` 跑 claude(避免 PTY 挂起)
3. 把日志末尾原样返回

也可以由 Agent 显式指定:
```bash
bash scripts/run.sh --mode review "用户需求"
bash scripts/run.sh --mode build  "用户需求"
```

### Step 5 — 切换模型服务(用户主动要求时)

**仅当用户明确说**"切换 / 换一家 / 切到 X / 换成自定义 / 用回 AgentPlan"等关键词时触发,**不要主动建议切换**。

```bash
bash scripts/switch-profile.sh             # 列出已配置的服务
bash scripts/switch-profile.sh agentplan   # 切换到 AgentPlan
bash scripts/switch-profile.sh custom      # 切换到自定义网关
```

切换实际上是把 `~/.claude/settings.json` 替换为目标 profile 的内容(同时同步 `.token` 文件),并把 `~/.claude/active-profile` 写成目标名。

---

## 关键配置点(踩坑后的硬约束)

> 这是 v3.1 现网走通后总结出的**必须遵守**的规则,违反就报错。

| 规则 | 说明 |
|---|---|
| 用 `ANTHROPIC_AUTH_TOKEN`,**不要** `ANTHROPIC_API_KEY` | 后者会被 CLI 强制走 anthropic.com 鉴权链路,在境内 IDC 必然失败 |
| `~/.claude.json` 必须有 `hasCompletedOnboarding: true` | 否则 CLI 拒绝在非交互模式启动,报 `Onboarding has not been completed` |
| `~/.claude/settings.json` 的 `env` 块 + `~/.claude/.token` 文件 **二者并存** | env 块负责 base_url / model / 各类开关,.token 文件负责 Key(更安全) |
| build 模式必须显式 `--allowedTools` 白名单 | 否则默认 ask 模式会等用户交互,在沙箱里直接挂死 |
| review 模式必须用 `--permission-mode plan` | 这样不会出现写文件的副作用,review 才是真正只读 |
| ⛔ Skill 调用方**禁止**叠加 `pty: true` | run.sh 的 `</dev/null` 会被 PTY 重新打开 stdin,导致 claude 等待输入 |
| 110s 超时是硬约束 | 走 `nohup setsid + log file + while-poll PID` 路径;一旦 PID 还活着且超过 110s,主动 `kill -9`,从日志里取已生成的内容 |

---

## 健康检查都检查什么?

| 检查项 | 不通过时的具体表现 |
|---|---|
| `~/.claude/settings.json` 是否存在且 JSON 合法 | claude 启动会直接 abort |
| `env.ANTHROPIC_BASE_URL` 是否设置 | claude 不知道请求发往哪里 |
| 用了 `ANTHROPIC_AUTH_TOKEN` 而非 `ANTHROPIC_API_KEY` | 后者必然走 anthropic.com,境内 IDC 连不上 |
| `~/.claude.json` 是否存在且 `hasCompletedOnboarding == true` | 否则 CLI 在非交互模式下 abort |
| `~/.claude/.token` 是否存在且非空 | 否则连接时被拒 401 |
| `env.ANTHROPIC_MODEL` 是否设置 | 否则 CLI 会回退默认 sonnet,在自定义网关上找不到模型 |

---

## Profile 设计

每个模型服务在 `~/.claude/profiles/` 下有一个 settings.json 模板:

```
~/.claude/profiles/
├── agentplan.json    — 火山方舟 AgentPlan(ark-code-latest,base_url /api/plan)
├── codingplan.json   — 火山方舟 Coding Plan(ark-code-latest,base_url /api/coding)
└── custom.json       — 自定义 Anthropic 兼容网关(占位符 __BASE_URL__ / __MODEL__)
```

`~/.claude/settings.json` 是当前激活配置的实际内容(由 setup / switch 脚本写入),`~/.claude/active-profile` 文件记录当前是哪一个。

---

## 必读参考文档

| 场景 | 需要读的文件 |
|---|---|
| 引导用户选择模型供应商 | `references/providers.md` |
| 用户报错 / 检查不通过 | `references/troubleshooting.md` |
| 不确定整体流程 / review vs build | `references/routing-flow.md` |

---

## 安全规则

- 用户的 Key 只保存在 `~/.bashrc`、`~/.claude/.token` 和 `~/.claude/profiles/*.json` 中(用户家目录内)
- 覆盖配置前**自动备份**到 `~/.claude/settings.json.bak.<时间戳>`
- 不上传任何外部服务,不在日志中记录 Key 明文
- ⛔ 不会出现在日志或 stdout 的任何地方打印完整 Key

## 不做什么

- ❌ **不**尝试连接 Anthropic 官方服务(沙箱网络在境内 IDC,连不上 anthropic.com)
- ❌ **不**自动猜测 Key,所有 Key 必须由用户主动粘贴
- ❌ **不**做 Codex 的配置(那是另一个 skill,叫 codex-allinone)
- ❌ **不**在用户没确认前覆盖已有的 settings.json
- ❌ **不**接管 review/build 之外的复杂权限模式(如 `bypassPermissions`、`dontAsk`),那是用户自己的事

## 常用对话示例

| 用户说 | Skill 做什么 |
|---|---|
| "帮我装 claude code" / "在 ArkClaw 里用 claude code" | 安装 + 引导配置 |
| "/claude-code-allinone 帮我写个 Python 脚本" | 直接执行(已配好则走 build 模式) |
| "claude code review 一下 utils.py" | 直接执行(走 review 模式,只读) |
| "切换到自定义网关" / "换一家" | 运行 switch-profile.sh |
| "claude 报 Onboarding has not been completed" | 跑 ensure-onboarding.sh |
| "claude 报 401" | 用「人话提示」告知用户:Key 失效或贴错套餐,引导去 ArkClaw 控制台刷新 / 切套餐 / 换 Kimi 等 |
| "我现在用的哪家?" | 读取 ~/.claude/active-profile |

---

## 给用户的"人话提示"模板(必须遵守)

skill 与用户沟通时,**禁止出现** profile / token / settings.json / apiKeyHelper / onboarding 这类内部术语。下表是对应的人话翻译,凡需告知用户错误时一律按此输出:

| 内部状态 | 给用户的人话提示 |
|---|---|
| 401 / 403 鉴权失败 | "连接火山方舟时被拒绝(可能是 Key 过期或贴错套餐)。可以这样修:\n  1. 去火山方舟控制台 → AgentPlan 页面,复制最新的专属 Key 发给我,我帮你重新写入(原配置会自动备份)\n  2. 如果你有别的可用 Key(Coding Plan 的、Kimi 的、DeepSeek 的、自建网关的),告诉我用哪个,我切过去\n请直接回复 1 或 2,或者直接把新 Key / "用 Kimi" 这类话发给我。" |
| Onboarding 未完成 | "Claude Code 还没完成首次启动检查,我帮你跳过(2 秒)" |
| relay 端口 connection refused | "本地的协议中转服务没起来,我重新启动一下(2 秒)" |
| settings.json 字段缺失 | "配置文件里少了一项必要信息,我帮你重新配一下" |
| apiKeyHelper 路径不存在 | "Key 文件丢失了(可能清理过家目录),我重写一下" |
| Key 格式自检失败 | "你给的这串看起来不像一把有效的 Key — 应该是一串 20 位以上的字母+数字。请去控制台完整复制后再发我" |
| 网络抖动跳过预校验 | "网络有点抖,在线校验跳过,先把配置写下来。如果运行时报错我再告诉你怎么修" |
