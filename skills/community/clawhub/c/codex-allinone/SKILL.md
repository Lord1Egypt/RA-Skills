---
name: codex-allinone
description: ArkClaw / OpenClaw 沙箱里一键安装并配置 Codex CLI 的 all-in-one skill。当用户提到 codex、想在 ArkClaw 里用 OpenAI 官方 Coding CLI、提到 ark-code-latest / 火山方舟 AgentPlan / Kimi / DeepSeek / 自定义 OpenAI 兼容端点 接 codex、想切换 codex 的模型供应商、或者说"我没有 OpenAI 官方账号但想用 codex / claude code 这类工具"时,使用本 skill。
license: MIT
---

# Codex All-in-One for ArkClaw

让 ArkClaw / OpenClaw 用户在**对话框里**完成 Codex CLI 的全部配置 — 不用打开终端、不用写 config.toml、不用记 base_url。

---

## 整体流程(决策树)

```
用户触发本 skill(说"用 codex 帮我..." / "/codex-allinone ..." / 报错 等)
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
(从未配置)   (之前用本 skill 配置的)          (有 config.toml 但不是本 skill 写的)
  │             │                                  │
  ▼             ▼                                  ▼
路径 ①        路径 ②                             路径 ③
首次配置      正常使用(绝大多数情况)              兼容性检查
  │             │                                  │
  │             │                                  ├─ 检查通过 → 保留不动,转到路径 ②
  │             │                                  └─ 检查不通过 → 告知用户具体问题,
  │             │                                       询问是否用本 skill 重新配置
  │             │
问用户选择   自动确保服务就绪
A/B 菜单     然后执行: codex exec "用户的需求"
  │
  ▼
完成配置后
转到路径 ②
```

### 三条路径说明

| 路径 | 什么时候走 | 用户需要做什么 |
|---|---|---|
| ① 首次配置 | 环境里从未配过 codex,或用户主动要求重新配置 | **默认直接走 AgentPlan**,优先尝试自动从 ArkClaw 沙箱环境变量(`ARK_AGENT_PLAN` / `ARK_CODING_PLAN` / `ARK_API_KEY`)零感知配好;失败再让用户粘贴一次 Key。**用户主动说"切第三方/换 Kimi/换 DeepSeek/自定义"时才走第三方分支** |
| ② 正常使用 | 已经配好了(本 skill 配的,或用户自配且体检通过) | **什么都不用做**,直接说编程需求即可 |
| ③ 兼容性检查 | 用户手动写过 config.toml,本 skill 首次遇到 | 如果检查通过:无需操作;如果不通过:选择重配或自己修 |

---

## 重要:正常使用时不要打扰用户

当配置已经就绪(路径 ②)时,**不允许**:

- 复述配置流程
- 解释 skill 在做什么
- 询问"是否需要切换 / 是否需要重新配置"
- 把 skill 的存在感暴露给用户

**只做**:
1. 运行 `bash scripts/ensure-relay.sh`(自动按当前 profile 启对应端口的 relay,不需要时立即退出)
2. 执行 `cd ~ && codex exec --skip-git-repo-check "用户的完整需求原文"`
3. 把 codex 的输出原样返回给用户

**用户体验**应该等同于"直接跟 codex 对话",完全感觉不到 skill 的存在。

只有这三种情况允许打扰用户:
1. 首次配置(环境全新)
2. 兼容性检查不通过,且无法自动修复
3. 用户主动说"切换 / 换一家 / 切到 X"

---

## 触发方式

- **自然语言**:"用 codex 帮我重构 utils.py" / "codex 跑一下这个测试"
- **显式命令**:`/codex-allinone <你的编程需求>`(强制走本 skill)
- **报错触发**:用户贴出 `command not found: codex` / `connection refused 444X` 等

---

## 详细流程

### Step 0 — 运行 doctor.sh 检测环境

每次触发都先运行 `bash scripts/doctor.sh`,它会输出一个 JSON,包含:

```json
{
  "codex_installed": true,
  "codex_version": "0.130.x",
  "codex_outdated": false,
  "config_state": "clean | managed-by-skill | user-managed",
  "active_profile": "agentplan | kimi | deepseek | arkv3 | custom | null",
  "user_config_summary": {"model_provider": "...", "model": "..."} | null,
  "user_health": {"is_healthy": true/false, "checks": [...], "issues": [...]} | null,
  "expected_relay_port": 4446 | 4447 | 4448 | 4449 | null,
  "relay_running": true,
  "ark_api_key_set": true,
  "moonshot_api_key_set": false,
  "deepseek_api_key_set": false,
  "ark_v3_api_key_set": false,
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

### Step 1 — 安装 / 升级 Codex CLI(仅首次需要)

`scripts/install.sh` 的行为:

| 当前状态 | 行为 |
|---|---|
| 未安装 codex | 通过 npm 安装最新版 |
| 版本低于 0.130 | 升级到最新 |
| 已是最新版 | 跳过,不做任何事 |

### Step 2 — 配置模型服务(仅路径 ① 触发)

**默认行为:不问选项,直接走 AgentPlan**

减少用户感知是核心原则。**不要主动给用户列 A/B 菜单**。除非用户主动说"我要用 Kimi / 切第三方 / 用自定义网关 / 用我自购的方舟 v3 Key"等关键词,否则一律默认进入 AgentPlan 配置流程。

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
| true | `ark_coding_plan=true` 且 `ark_agent_plan!=true` | true | **零感知配置 (Coding Plan)**:直接 `bash scripts/setup-codingplan.sh --auto`。⚠️ 注意 **Coding Plan 与 AgentPlan 是两套不同套餐**,Key 互不通用,base_url 也不一样:AgentPlan → `/api/plan/v3` (relay 4446);Coding Plan → `/api/coding/v3` (relay 4450)。**绝不能套用 AgentPlan profile** |
| true | **两个都为 true(双开)** | true | **优先 AgentPlan**:直接 `bash scripts/setup-agentplan.sh --auto`。脚本内置预校验,若 AgentPlan Key 401 会**自动 fallback** 到 `setup-codingplan.sh --auto --from-fallback`,**全程零感知,不需要询问用户** |
| true | 两个都没标 | true | 默认 `bash scripts/setup-agentplan.sh --auto`(并打印一条 warning,401 时再切第三方分支) |
| false 或 `ark_api_key_set=false` | — | — | 走"传统首次配置":告知用户使用 AgentPlan,引导粘贴一次 Key |

> 实现细节:`setup-agentplan.sh --auto` 内部带**三层防护**:(1) 本地格式自检挡掉粘错的输入;(2) 调用上游 `/models` endpoint 做活性 ping(不消耗推理 token,3 次重试,仅 401/403 视为失败);(3) AgentPlan 401 且 `ARK_CODING_PLAN=true` 时自动 `exec` 转发到 `setup-codingplan.sh --auto --from-fallback`。所以即使 skill 选错或双开账号 AgentPlan Key 失效,都不会真的把错 Key 写进 profile。

#### 传统首次配置(仅在零感知不可用时触发)

向用户输出:

```
准备给你配置 Codex,使用火山方舟 AgentPlan(套餐内额度,ark-code-latest 智能路由)。

请粘贴 AgentPlan 控制台分配的专属 Key:
```

拿到 Key 后立即跑:
```bash
bash scripts/setup-agentplan.sh "$KEY"
```

#### 何时走第三方分支?

只有以下情况才询问/触发第三方流程,**不要主动给用户列菜单**:

- 用户**主动**说:"我要用 Kimi / Moonshot" / "切到 DeepSeek" / "用自定义网关" / "用我的方舟 v3 Key"
- 用户**主动**给出 base_url + Key + model 三件套
- 用户**主动**说"我没有 AgentPlan Key,但我有 Kimi / DeepSeek / 自建网关 Key"

触发后引导用户给出对应 Key,然后跑:
```bash
bash scripts/setup-thirdparty.sh <provider> "$KEY"
# 或 custom:
bash scripts/setup-thirdparty.sh custom "$KEY" "<model>" "<base_url>"
```

> ⛔ **不允许**在用户没主动提"切/换/第三方/Kimi/DeepSeek/自定义"等关键词时,主动展示 A/B 菜单或让用户做选择。这会增加感知,违背"默认 AgentPlan + 零感知优先"原则。

配置脚本会自动完成:写 Key → 写 profile → 按需启动 codex-relay → 写自动恢复命令到 .bashrc。如果用户已有 config.toml,会**先备份**再覆盖。

### Step 3 — 兼容性检查(仅路径 ③ 触发)

当 doctor.sh 返回 `config_state == "user-managed"` 时,说明用户之前手动写过 config.toml。此时读取 `user_health` 字段:

**检查通过**(`is_healthy == true`):
- 不打扰用户,直接当作"已配好",进入正常使用

**检查不通过**(`is_healthy == false`):
向用户展示具体问题,并询问:

```
检测到你已有的 codex 配置存在以下问题:
  1. <具体问题描述>
  2. <具体问题描述>

你希望:
  A. 让本 skill 帮你重新配置(推荐,会先备份你现有的文件)
  B. 我自己去修改

请回复 A 或 B。
```

### Step 4 — 正常使用

```bash
bash scripts/ensure-relay.sh
cd ~ && codex exec --skip-git-repo-check "用户的完整需求原文"
```

> `ensure-relay.sh` 做什么?
> - 读取 `~/.codex/active-profile`,根据当前 profile 自动启对应端口的 codex-relay
> - 端口分配:agentplan=4446 / kimi=4447 / deepseek=4448 / custom=4449
> - arkv3(直连)和 custom 直连模式立即退出,不耗时

### Step 5 — 切换模型服务(用户主动要求时)

```bash
bash scripts/switch-profile.sh        # 列出已配置的服务
bash scripts/switch-profile.sh kimi   # 切换到 Kimi
```

---

## codex-relay 是什么?

Codex CLI 0.130+ 默认发 OpenAI **Responses 协议**,而多数模型服务只支持 **Chat 协议**。codex-relay 是一个轻量的本地服务,负责做协议翻译:

```
Codex CLI ──(Responses)──→ codex-relay (本机端口) ──(Chat)──→ 上游模型服务
```

每个 profile 占一个独立端口:

| Profile | 端口 | 是否需要 relay |
|---------|------|---------------|
| agentplan | 4446 | ✅ |
| codingplan | 4450 | ✅ |
| kimi | 4447 | ✅ |
| deepseek | 4448 | ✅ |
| arkv3 | — | ❌ 直连(原生支持 Responses) |
| custom | 4449 / — | 🔍 自动探测(setup 时 curl `/responses` 决定) |

custom 路径的探测:`POST {base_url}/responses` 返回 404 → 不支持 → 走 relay;返回 200/400/401/403/422 → 支持 → 直连。

安装方式:
```bash
pip install --user --break-system-packages codex-relay
```

安装后可通过 `codex-relay --help` 验证。

---

## 健康检查都检查什么?

| 检查项 | 不通过时的具体表现 |
|---|---|
| model_provider 字段是否设置 | Codex 不知道连接哪个服务 |
| base_url 地址是否填写 | Codex 不知道请求发往哪里 |
| wire_api 协议是否有效 | 老版本的 `chat_completions` 在 0.130 以后已废弃;`chat` 也已 deprecated,推荐 `responses` |
| API Key 环境变量是否存在 | 连接时会被拒绝(401 错误) |
| 当前 profile 对应端口的 relay 是否在运行 | 会报 connection refused |
| 是否硬编码了 temperature/top_p | 部分模型不支持,会返回 400 错误 |

---

## Profile 设计

每个模型服务在 `~/.codex/profiles/` 下有一个 .toml 配置文件:

```
~/.codex/profiles/
├── agentplan.toml    — 火山方舟 AgentPlan(经 relay 端口 4446 → /api/plan/v3)
├── codingplan.toml   — 火山方舟 Coding Plan(经 relay 端口 4450 → /api/coding/v3)
├── kimi.toml         — Kimi (月之暗面 Moonshot,经 relay 端口 4447)
├── deepseek.toml     — DeepSeek(经 relay 端口 4448)
├── arkv3.toml        — 火山方舟普通 v3 Key(直连)
└── custom.toml       — 自定义 OpenAI 兼容端点(自动探测,直连或经 relay 端口 4449)
```

`~/.codex/config.toml` 是一个快捷方式(软链接),指向当前使用的配置文件。切换模型服务 = 把快捷方式指向另一个文件。

---

## 必读参考文档

| 场景 | 需要读的文件 |
|---|---|
| 引导用户选择第三方 Key | `references/thirdparty-providers.md` |
| 用户报错 / 检查不通过 | `references/troubleshooting.md` |
| 不确定整体流程 | `references/routing-flow.md` |

---

## 安全规则

- 用户的 Key 只保存在 `~/.bashrc` 和 `~/.codex/profiles/*.toml` 中(用户家目录内)
- 覆盖配置前**自动备份**到 `~/.codex/config.toml.bak.<时间戳>`
- 不上传任何外部服务,不在日志中记录 Key 明文

## 不做什么

- ❌ **不**尝试连接 OpenAI 官方服务(沙箱网络在境内 IDC,连不上 openai.com)
- ❌ **不**自动猜测 Key,所有 Key 必须由用户主动粘贴
- ❌ **不**做 Claude Code 的配置(那是另一个 skill)
- ❌ **不**在用户没确认前覆盖已有的 config.toml

## 常用对话示例

| 用户说 | Skill 做什么 |
|---|---|
| "帮我装 codex" / "在 ArkClaw 里用 codex" | 安装 + 引导配置 |
| "/codex-allinone 帮我写个 Python 脚本" | 直接执行(如果已配好) |
| "切换到 Kimi" / "换成 DeepSeek" | 运行 switch-profile.sh |
| "切换模型服务" / "换一家" | 列出已配置的选项 |
| "codex 报 connection refused 444X" | 用人话告知:"本地协议中转服务没起来,我重启一下",然后跑 ensure-relay.sh |
| "codex 报 401" | 用人话告知:Key 失效或贴错套餐,引导去控制台刷新 / 切套餐 / 换 Kimi 等 |
| "我现在用的哪家?" | 读取 ~/.codex/active-profile |

---

## 给用户的"人话提示"模板(必须遵守)

skill 与用户沟通时,**禁止出现** profile / config.toml / relay / Responses API / wire_api 等内部术语。下表是对应的人话翻译,凡需告知用户错误时一律按此输出:

| 内部状态 | 给用户的人话提示 |
|---|---|
| 401 / 403 鉴权失败 | "连接火山方舟时被拒绝(可能是 Key 过期或贴错套餐)。可以这样修:\n  1. 去火山方舟控制台 → AgentPlan 页面,复制最新的专属 Key 发给我,我帮你重新写入(原配置会自动备份)\n  2. 如果你有别的可用 Key(Coding Plan 的、Kimi 的、DeepSeek 的、自建网关的),告诉我用哪个,我切过去\n请直接回复 1 或 2,或者直接把新 Key / "用 Kimi" 这类话发给我。" |
| connection refused 444X | "本地的协议中转服务没起来,我重启一下(2 秒)" |
| model_provider / base_url 缺失 | "配置文件里少了一项必要信息,我帮你重新配一下" |
| ARK_API_KEY 环境变量缺失 | "Key 还没注入到当前 shell,我重新加载一下" |
| Key 格式自检失败 | "你给的这串看起来不像一把有效的 Key — 应该是一串 20 位以上的字母+数字。请去控制台完整复制后再发我" |
| 网络抖动跳过预校验 | "网络有点抖,在线校验跳过,先把配置写下来。如果运行时报错我再告诉你怎么修" |
| codex-relay 安装失败 | "本地中转服务装不上,可能是 pip 网络问题。我重试一次,如果还不行你可以手动执行: `pip install --user --break-system-packages codex-relay`" |
| relay 端口活着但调用 401 | "本地中转服务在运行,但没拿到 Key(可能是早期版本残留进程),我重启一下让它重新读取(3 秒)" |
