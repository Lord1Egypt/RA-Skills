# 02 · 接管协议（Takeover）：让闭环自动生效，而不是等模型想起

> **解决什么**：装了 skill 但真实项目里不接管——不加载、不 INTAKE、不门禁、没证据。
> **不解决什么**：不做语义级拦截（DSH 没有「模型说完成时拦下」的钩子），不替模型写代码，不自动组队。
> 配套：`scripts/loop-state.ps1`（状态唯一写入）、`templates/loop-project.json`、`templates/agents-loop-fragment.md`、`docs/design/2026-11-18-capability-loop-panel.md`（面板设计稿）。

## 1. 为什么写了 description 还是不接管

| 层 | 事实 | 后果 |
|---|---|---|
| 触发层 | 会话里只有 catalog **摘要**；正文要么模型主动调 `skill`，要么用户打 `/name` | 加载是**概率**行为 |
| 描述层 | frontmatter 首块是「【重点】体检/修复 DSH 自身」，项目治理在【配套】 | 真实工程说「帮我做 XX」时语义不匹配 |
| 执行层 | `SKILL.md` 写「按需取段，不强行走完」，七阶段无状态载体 | 即使加载，也被当参考文档 |
| 证据层 | 门禁输出只在终端滚过去，没有落盘 | 用户看不到阶段与缺什么 |
| 反馈层 | 没记录「这次没接管」 | 无法自我修正 |

**结论**：需要把「触发 + 状态 + 可见性」三件事做成机制，而不是继续改文案。

## 2. 三层接管

| 层 | 做法 | 确定性 | 成本 | 何时用 |
|---|---|---|---|---|
| **P0 软接管**（本文件 + 模板） | `AGENTS.md` 12 行片段 + `.dsh/loop/state.json` | 中：`AGENTS.md` 链**一定注入**，但「读 state」靠模型照做 | 0 安装 | 今天就能用 |
| **P1 硬接管（已实现，夹具验证）** | 宿主插件 `plugins/capability-loop/`：在 `agent/pre-step` 把契约折进该步消息 | 高：首步必带，不依赖模型自觉 | 需装 bundle | 装了插件之后 |
| **P2 面板（v1 已实现）** | 同一个 bundle 的 client 半：`sidebar.panellist` + `main` 全局页 + **运行中心**（动作走会话命令 `/capability-loop`） | 高：状态可见、可动手 | 需 client 半 + host 命令 | 想让人看见/操作时 |

P1 的机制依据：`@deepseek-ai/dsh-agent-instructions` 就是用 `agent/pre-step` 在首个请求前注入 `AGENTS.md` 链（源码 `src/index.ts` L330–356）；插件照同样方式把契约插进 `decision.messages`，不用 `agent.inject()`（后者要等唤醒，且可能错过已认领批次的 pre-step）。

### 2.1 P1 插件（`plugins/capability-loop/`）

| 项 | 内容 |
|---|---|
| 入口 | `index.js`（host half，ESM）；`inject = ['fs', 'workingDirectory']`；`sandboxPolicy` 用 `ctx.get()` 可选取 |
| 钩子 | `agent/pre-step` 瀑布：先 `await next()`，再决定是否折入消息 |
| 档位 | `.dsh/loop/project.json` 的 `mode` → 被 `state.json` 的 `mode` 覆盖 → 缺省用插件 `defaultMode`（默认 `off`） |
| 注入 | `on`：完整契约 ≤1600 字符（实测约 810）；`shadow`：一行 ≤140 字符；`off`/未标记：0 |
| 位置 | 紧跟本步认领的用户消息之后（用户原话先出现，契约随后） |
| 去重 | 消息带 `source.kind='capability-loop'` + 内容指纹；同批、会话历史、resume/fork 都判重 |
| 影子计数 | 追加 `.dsh/loop/shadow-log.jsonl`（每会话一行）→ `loop-state.ps1 -Action sync-shadow` 计数并提示升级 |
| 纪律 | fail-open（任一失败只记日志、不注入）；只读 `state.json`；不新增 Session 事件类型 |

**安装**（本机目录，开发/内测）：

```
plugin_manager  action=install_bundle  target="<skill>\plugins\capability-loop"
```

装完在 **Plugins** 页打开该行，然后在**新会话**验证：`on` 档首条消息后应出现契约，`shadow` 档是一行提示。

> **两个已验证的坑**（见 `70-playbook.md` `ERR-20261119-01/02`）：①本地目录安装是 pnpm link，**不能在模块顶层 import dsh 自带包**（会 `ERR_MODULE_NOT_FOUND` 导致整行不激活）——本插件改运行时动态解析 + 手工构造兜底；②插件写文件必须传**本会话**的 `sandboxPolicy.resolve({ session })`，否则按部署默认 `read-only` 被拒且容易静默失败。

> 装完必须确认 `plugin_manager action=set_plugin target=include:capability-loop enabled=true` 返回 **`application: applied`**；`install_bundle` 的 `exitCode=0` 不代表这一行活了。

**回归夹具**（10 条，`node --test`）：

```powershell
node --test "<skill>\plugins\capability-loop\test\takeover.test.mjs"
```

覆盖：未标记零注入 / off 不注入 / shadow 一行 + 影子日志 + 同会话只记一次 / on 契约含阶段·门禁·阻断·下一步且 ≤1600 / 注入紧跟用户消息 / resume 历史去重 / 同批去重 / fs 抛错 fail-open / state 坏 JSON 降级 / `defaultMode=on` 但未标记仍不注入 / **无 dsh-llm 可解析时的兜底路径**（11 条）。

**本机实测（2026-11-19）**：`install_bundle` → `application: applied`；`shadow` 真机会话收到一行提示并记账；`sync-shadow` 显示 2/3。**`on` 档已实测**：`loop-state.ps1 -Action set-mode -Mode on` 后，本工程真实会话的下一步即收到完整契约（阶段 / 硬约束 / 门禁 / 阻断 / 下一步全文，约 900 字符），脚本返回 `[PASS] set-mode … on`、exit 0。

### 2.2 运行中心（P2 动作，v2.13.0）

- 入口：面板「运行中心」卡片（门禁 kind + taskDir / 交接体检 slug / 模块预检 keyword + alias / 上架打包 handle / 只读动作）与头部三段档位（接管 / 影子 / 关闭）。
- 通道：面板 → `ctx.remote.commands.execute(sessionId, '/capability-loop …')` → Host `commands.register('capability-loop')` → `actions.js`（`dsh-doc/references/user-actions.md` 的「一个操作、两个调用方」）。
- 安全：`ACTIONS` 白名单（audit / gate / env / handoff-audit / preflight / pack / visual / skill-status / sync-shadow / mode）；参数逐个校验（kind 枚举、路径禁 `..` 与开头 `-`、中文/空格路径原样传、不拼 shell）；子进程 5s grace + 动作级超时 + `AbortSignal` 取消；输出只回尾部 40 行（≤6000 字）。
- 确认：每个动作先弹确认框（工程 + 完整命令 + 说明），确认后才执行；运行中可取消。
- 语法：`/capability-loop run gate kind=design taskDir=docs/design [grill=1]`、`/capability-loop run env`、`/capability-loop run audit`、`/capability-loop mode on`。**taskDir 必填**（没有任务目录时 loop-gate 只会报「没有可执行的门禁」，所以面板直接禁用运行键并提示）。
- **部署注意**：Host 半的命令注册在应用启动时完成，改 `index.js`/`actions.js` 后需**重启应用**；client 半（`client.js`）刷新页面（Ctrl+R）即可。夹具 46 条（actions 17 + client 15 + takeover 13 + fallback 1）。

## 3. 档位：off / shadow / on

| 维度 | `off` | `shadow`（影子） | `on`（接管） |
|---|---|---|---|
| 注入 | 无 | 一句话提示（≤120 字，只说明「只记录不阻断」） | 完整契约（≤400 token） |
| INTAKE | 不要求 | 不要求 | 治理场景必须 |
| 门禁结果 | 不记录 | **记录但不阻断**，FAIL 不影响对话 | 进阻断；FAIL 不得宣称完成 |
| 面板 | 空态「未接管」 | 虚线 banner + 观察计数 + 「升级为接管」 | 完整面板 |
| 切换 | — | 随时切 on/off | 随时切 shadow/off |

**首次启用（默认策略 A，2026-11-18 确认）**：新标记工程先走 `shadow`，累计 **3 个会话**后提示升级为 `on`；**不自动升级**。用户随时可强切。

## 4. 状态源 `.dsh/loop/state.json`

唯一写入方是**脚本**，插件/面板只读（`set-mode` 例外，写的是 `project.json`）。

```jsonc
{
  "schema": 1,
  "skillVersion": "2.10.0",
  "mode": "on",                    // off | shadow | on
  "shadowSessions": 0,             // shadow 下累计的会话数（P1 由插件递增）
  "project": { "name": "…", "root": "…", "profile": "docs/loop/project-profile.md", "intakeAt": "…" },
  "stage": "WIRE",                 // INTAKE|AUDIT|FIX|WIRE|HANDOFF|GRILL|GATE
  "stageSince": "…",
  "next": { "label": "…", "command": "…" },
  "checks": {
    "design":   { "status": "FAIL", "at": "…", "exit": 1, "cmd": "…", "evidence": ["docs/design/…"] },
    "grill":    { "status": "MISSING", "at": null, "exit": null, "cmd": "…", "evidence": [] },
    "environment-audit": { "status": "WARN", "at": "…", "exit": 3, "cmd": "capability-audit.ps1", "evidence": [] }
  },
  "blockers": [ { "id": "D-01", "text": "…", "owner": "lead", "due": "2026-11-19" } ],
  "metrics": { "gatePassRate7d": 0.67, "rework7d": 2, "catalogChars": 3673, "driftAlerts": 2 },
  "digest": "sha1:…",              // mode+stage+checks+blockers 的指纹，P1 用它判断要不要追增量
  "updatedAt": "…"
}
```

**容错（面板与注入都必须处理）**：文件缺失、JSON 坏、`schema` 不认、`skillVersion` 不匹配、`updatedAt` 超过 24h。一律**降级显示**并给修复动作，不显示空白、不把缺失当 0。

## 5. 注入契约（P1 逐字稿；P0 用 AGENTS 片段近似）

**on（≈1,450 字符 ≈ 350–400 token）**

```text
<system-reminder>
[capability-loop v2.10.0] 本工程已启用治理闭环；当前阶段 WIRE（第 4/7 阶段）。
适用：需求/方案、设计/改版、实现与交接、测试与验收、复盘。豁免：只读问答、单文件小改（≤30 分钟）、纯闲聊——直接做，不套流程。

硬约束：
1. 未完成 INTAKE（.dsh/loop/project-profile.md）不得进入实现；新项目/新模块/跨模块改动才做完整六问，小改只问目标/验收/影响面。
2. 说“完成/已修复/已通过”必须附证据：命令 + 退出码 + 关键输出或截图；拿不到实测就写“未实测 + 原因 + 补测方式”。
3. PASS 不得由写的人自己给；终门要有他人的评审记录。
4. 交付/交接前必须 grill（记录 grill-*.md）；硬门用 loop-gate.ps1 -RequireGrill。
5. 改本 skill 必须在同一提交 bump version.json + CHANGELOG.md。
6. 门禁 FAIL 时只能说“未通过 + 缺什么”，不得改写结论。

本阶段出口：design-context.md 已取证；loop-gate -Kind design 退出码 0；grill 至少 1 条打回并修正。
下一步：补 design-context 后运行 loop-gate.ps1 -TaskDir docs/design/<slug>。
需要细节再读：<skill-dir>/references/55-design-intake.md（只读这一篇，不整包加载）。
状态源：.dsh/loop/state.json（用户可在“能力闭环”面板查看）。
</system-reminder>
```

**shadow（≈90 字符）**

```text
<system-reminder>
[capability-loop · 影子] 本工程已记录治理状态（.dsh/loop/state.json）。只记录、不阻断；需要时按 state.next 执行，门禁失败不会拦住对话。
</system-reminder>
```

**注入纪律**：首步只注入一次；`digest` 变化时只追加 ≤3 行增量（阶段/阻断/下一步）→ 追加式，KV 前缀不受影响；失败 fail-open（不注入、只记日志）；不新增 Session event 类型；`<skill-dir>` 运行时解析（商店安装目录可能是 `<handle>--dsh-capability-loop`）；**不写进 system prompt**（那是 profile 级，会对所有项目生效）。

## 6. 命令（P0 全部可用）

```powershell
$sk = "$env:USERPROFILE\.dsh\skills\dsh-capability-loop"
$st = "$sk\scripts\loop-state.ps1"

# 接入（默认 shadow；自动生成 .dsh/loop/project.json + state.json + .gitignore）
powershell -NoProfile -ExecutionPolicy Bypass -File $st -Action init -Root "<工程根>" -ProjectName "<工程名>"

# 看状态（只读；未接入 exit 3）
powershell -NoProfile -ExecutionPolicy Bypass -File $st -Action status -Root "<工程根>" [-Json]

# 档位 / 阶段 / 下一步
powershell -NoProfile -ExecutionPolicy Bypass -File $st -Action set-mode  -Root "<工程根>" -Mode shadow|on|off
powershell -NoProfile -ExecutionPolicy Bypass -File $st -Action set-stage -Root "<工程根>" -Stage WIRE -NextLabel "补 design-context" -NextCommand "loop-gate -TaskDir docs/design -Kind design"
powershell -NoProfile -ExecutionPolicy Bypass -File $st -Action set-next  -Root "<工程根>" -NextLabel "…" -NextCommand "…"

# 阻断
powershell -NoProfile -ExecutionPolicy Bypass -File $st -Action add-blocker     -Root "<工程根>" -BlockerText "缺 1440 截图" -Owner lead -Due 2026-11-19
powershell -NoProfile -ExecutionPolicy Bypass -File $st -Action resolve-blocker -Root "<工程根>" -BlockerId D-01

# 门禁自动写回（工程有 .dsh/loop/project.json 时 loop-gate 自动调用；也可显式）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\loop-gate.ps1" -Workspace "<工程根>" -TaskDir docs/design -Kind design [-StateFile "<state.json>"]
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\capability-audit.ps1" -Workspace "<工程根>"

# 影子观察计数（装 P1 插件后：读 shadow-log.jsonl → shadowSessions + 升级提示）
powershell -NoProfile -ExecutionPolicy Bypass -File $st -Action sync-shadow -Root "<工程根>" [-ShadowTarget 3]
```

**写回规则**：`loop-gate.ps1` 只在「单一类别（design/requirement/test）或 `-Environment`」且「给了 `-StateFile` 或工程有 `.dsh/loop/project.json`」时写 `checks.<类别>`；`capability-audit.ps1` 先写 `.tmp/capability-loop/audit-state.json`，再同步 `metrics` 并记 `checks.environment-audit`。**未标记工程零变化**。

## 7. 正反例（回归基线）

| 场景 | 期望 |
|---|---|
| 未标记工程跑门禁 | 不创建 `.dsh/`；exit 0/1 与旧行为一致 |
| 标记工程跑 `-Kind design`（有 design-context + grill） | PASS；`checks.design.status=PASS`；`updatedAt` 变化 |
| 标记工程跑 `-Kind design`（缺 design-context） | FAIL（exit 1）；`checks.design.status=FAIL`；不改写已有 `next.label` |
| `-Kind all` | **不写回**（避免把整体结果误记到某一类） |
| `set-mode` | `project.json.mode` 与 `state.mode` 同步 |
| `sync-shadow`（无日志） | exit 1 + 提示「未装插件则无此文件」 |
| `sync-shadow`（3 会话） | `shadowSessions=3`；`shadow.canUpgrade=true`；`status` 打印「可升级：-Action set-mode -Mode on」 |
| JSON 坏 | `status` 报错但其它命令可修复（`init -Force`） |
| 未接入跑 `status` | exit 3 + 提示，不创建文件 |

## 8. 已知限制

- P0 的「读 state」是**软**的：模型可能跳过那次 `read`；P1 插件才是确定性的。
- `shadowSessions` 计数只有 P1 插件能可靠递增；P0 阶段可手工 `set-mode` 升级。
- 面板读状态需要**当前会话**授权（`workspaceFiles.read(sessionId, …)`）；第三方 bundle 不能给 `dsh-api-remotes` 加命名空间。
- **P1 已实现并夹具验证**；`on`/`shadow` 注入已在本机真实会话实测（`on`：2026-11-19 本工程，契约全文出现在该步用户消息后）。未实测：自定义 `source.kind` 在 Web UI 的渲染表现、真实 token 计费差异、多工作区切换时的读取时序。
- **P2 已实现（client 半 v1）**：只读面板 + 运行中心（门禁/体检/交接体检/预检/打包/视觉探测/版本检查/影子计数/切档位）。动作不直连脚本：面板发 `/capability-loop <动作>` → Host 命令 handler → `actions.js` 白名单 + 参数校验 + 子进程超时/取消。**Host 命令注册要重启应用才生效**（client 半刷新页面即可）；真机按钮点击验收待补，见 `docs/design/grill-p2-actions-20261119.md`。
