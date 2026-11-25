# 能力闭环：自动接管 + Harness 控制台 · 设计稿 v0.3（收敛版）

> 状态：**设计呈现（未实现）**，供评审。所有「已实测」都带证据位置；没有证据的写「未实测」。
> 日期：2026-11-18 · 作者：lead · 关联：`dsh-capability-loop` v2.9.6
> 配套：[design-context.md](design-context.md)（现有系统取证）· [grill-design-20261118.md](grill-design-20261118.md)（自对抗评审）· [review-20261118-self.md](review-20261118-self.md)（设计自审：P0 已修 / P1 已收敛）· [panel-mockup.html](panel-mockup.html)（可交互稿）
> **v0.2 变更**：覆盖 skill 全量能力（7 Tab / 32 项），补齐影子模式，动作可跑门禁。
> **v0.3 收敛**（按自审）：总览缩为 6 张能力卡 + 32 项抽屉；门禁合成一个列表（当前阶段置顶/筛选）；只保留一个主「运行门禁」；补确认模态；A–I 改 5+4；描述 12px；L3 动作标「仅复制」；异常态禁用档位；页头/侧栏去噪。**Q1 已确认 A（首启 3 会话影子观察）。**

---

## 0. 结论与面板作用

**「不接管」不是 description 写得不够好，而是缺三件事：确定性触发、会话内状态、用户可见的证据。**
架构拆成 **Arm（接管判定）→ Contract（≤400 token 契约注入）→ State（唯一状态源）→ Panel（全量控制台）**。

### 0.1 面板解决什么（v0.2 的答案：全量能力，不是只看进度）

| 它解决 | 它不解决 |
|---|---|
| **全量能力入口**：12 项能力地图 + 7 个 Tab，覆盖接入/阶段/门禁、DSH 九组体检、运行时修复、技能与插件治理、交接交付、记忆迭代、运行记录 | 不替模型写代码、不替评审打分 |
| **接管的可见性**：当前阶段、缺哪条证据、下一步 | 不拦截模型口头的「完成了」（DSH 无该语义钩子） |
| **「完成」的可证性**：命令、退出码、时间、证据路径、输出尾部 | 不自动组队、不自动跑完七阶段 |
| **治理的可控性**：接管/影子/关闭 + 首次观察期 + 阻断项 | 不做项目管理系统（不排期、不派活） |
| **动作一步到位**：白名单动作可直接运行（体检/门禁/交接体检/预检/打包/视觉探测），带确认、输出、取消、写回 | 不允许任意命令，不执行工程源码改动 |
| **成本与迭代**：注入字符、catalog 字符、漂移、返工、门禁通过率、版本/商店状态 | 不替代 skill 正文（知识仍在 `references/`） |

**预览（1440×900，真实 token；打开 [panel-mockup.html](panel-mockup.html) 可切 7 个 Tab / 4 态 / 明暗）**

![总览 · 暗色](panel-overview-dark.png)
![项目闭环 · 暗色](panel-project-dark.png)

其余：[能力体检](panel-health-dark.png) · [技能治理](panel-skills-dark.png) · [交接交付](panel-handoff-dark.png) · [记忆迭代](panel-memory-dark.png) · [运行记录](panel-runs-dark.png) · [确认弹窗](panel-run-modal-dark.png) · [影子模式](panel-shadow-dark.png) · [总览 · 亮色](panel-overview-light.png) · [未接管](panel-empty-dark.png) · [状态异常](panel-error-dark.png)

---

## 1. 现场问题：为什么实际项目里没接管

### 1.1 现象（用户报告，本会话输入）

在真实工程会话里提出实现/设计类需求，`dsh-capability-loop` 没有被加载，更没有被执行：没有 INTAKE、没有门禁、没有证据收口。用户必须手动 `/dsh-capability-loop` 或点名「按闭环做」。

### 1.2 机制层根因（按 DSH 0.2.2-rc.3 的实际机制）

| # | 层 | 事实（证据） | 后果 |
|---|---|---|---|
| R1 | **触发层** | skill 进入会话的是「catalog 摘要」；正文只有模型调用 `skill` 或用户输入 `/name` 才注入（`@deepseek-ai/dsh-tool-skill`、`dsh-client-ui-skill` README §User-explicit skill invocation） | 是否加载由模型**概率判断**；description 再准也不是确定性触发 |
| R2 | **描述层** | frontmatter 第一语义块是「【重点】体检/修复 DSH 自身：九组审计→…」，项目治理被标成「【配套】」（`SKILL.md` frontmatter，v2.9.6） | 真实工程的「帮我做 XX」与描述的首要语义不匹配，模型不加载 |
| R3 | **执行层** | 正文 §1 明写「按需取段，不强行走完」；七阶段没有状态载体，跨会话不保留（`SKILL.md` §1） | 即使加载，模型把它当参考文档，而不是「本会话的角色与流程」 |
| R4 | **证据层** | `loop-gate.ps1` 只有模型主动想起才会跑；输出只在终端滚过去（`scripts/loop-gate.ps1` L156–159） | 用户看不到「现在哪一阶段、缺什么证据」，也无法在下一轮追责 |
| R5 | **反馈层** | 没有记录「这次没接管」；`memory`/retro 只在任务后手动写 | skill 无法从「漏触发」中自我修正 |

### 1.3 对旧结论的更正

`references/50-design-team.md` §5 写「DSH 没有配置级路由/hook，只能靠 AGENTS.md + description + memory 三道软约束」。**这句话在 0.2.2-rc.3 已不成立**：

- `@deepseek-ai/dsh-agent-instructions` 用 `agent/pre-step` 瀑布，在会话首个请求前注入 `AGENTS.md` 链（源码 `src/index.ts` L330–356；README §Main flow，预算 65,536 B/链）；
- 插件可用 `ctx.systemPrompt.section()` 与 `agent.inject()`（`dsh-doc/references/practices.md` §Stability）；
- 客户端插件可用 `sidebar.panellist` + `main` 注册全局页（`dsh-client-ui-sidebar` / `dsh-client-ui-plugin-manager` README）。

所以「确定性接管」在机制上**做得到**，缺的是把它做出来。

### 1.4 为什么「把规则再写进 AGENTS.md」不够

`AGENTS.md` 是**静态文档**：不区分小改与重构、不知道当前阶段、不能记录证据、用户也看不见它有没有生效；每个新项目还要手工拷一遍。它适合放 10 行以内的「路由契约」，不适合承载状态机。

---

## 2. 目标 / 非目标 / 成功判据

### 2.1 目标

| ID | 目标 | 可判定判据 |
|---|---|---|
| G1 | 标记为受治理的工程，**每个新会话自动进入接管**，无需用户点名 | 首个请求的会话事件里存在 `capability-loop` 注入消息（`agent/inbox/spliced` 或等价事件），采样 10 个新会话 ≥10/10 |
| G2 | 接管**只在治理场景**生效，不劫持闲聊与只读问答 | 反例会话（纯问答）无注入、无 intake 追问；由注入契约的「适用/豁免」段约束 |
| G3 | 治理成本可控 | 首步注入 ≤ 1,600 字符（≈400 token）；状态变化追加 ≤ 400 字符；不重复整包加载 24 KB `SKILL.md` |
| G4 | 「完成」可证 | `loop-gate.ps1` 结果落盘到状态文件；面板可列出门禁、退出码、时间、证据路径、输出尾部 |
| G5 | 用户可控可回滚 | 面板可切 `接管 / 影子 / 关闭`；关闭后不注入、不改行为；动作白名单可关 |
| G6 | **能力全量可见** | 面板 Tab/能力地图覆盖 skill 的 12 项一级能力（见 §4.2 的 32 行映射）；无一项能力「没有入口」 |

### 2.2 非目标（本期明确不做）

- ❌ 不做语义级「拦截模型说完成」的强制钩子（DSH 没有该语义边界；只能做到脚本门禁 + 面板证据）。
- ❌ 不把 24 KB `SKILL.md` 常驻进上下文。
- ❌ 不自动 spawn 团队/子代理（治理 ≠ 组队；小改明确不组队）。
- ❌ 不改 DSH 核心、不改用户其它项目、不写用户 profile 之外的文件。
- ❌ 不做 iframe 面板、不复制一套视觉体系。
- ❌ 面板不提供「任意 shell」；只跑白名单脚本，参数白名单校验。

---

## 3. 总体架构：Arm → Contract → State → Panel

```
┌──────────────────────────── 工程工作区 ────────────────────────────┐
│ .dsh/loop/project.json   接管声明（名称/档位/profile 相对路径）      │
│ .dsh/loop/state.json     唯一状态源（阶段/门禁/证据/阻断/下一步）     │
│ docs/loop/…              INTAKE 产物、gate 输出、grill 记录（可选）   │
└───────────────┬────────────────────────────────┬───────────────────┘
                │ 读                              │ 读/写（脚本）
        ┌───────▼────────┐              ┌────────▼─────────┐
        │ Host 插件       │              │ skill 脚本        │
        │ capability-loop │              │ loop-gate.ps1     │
        │ · Arm 判定      │              │ loop-state.ps1    │
        │ · Contract 注入 │              │ capability-audit  │
        │ · 运行中心(P2)  │              │ handoff-audit.py  │
        └───────┬────────┘              └────────┬─────────┘
                │ pre-step 注入                    │ 写 state.json
        ┌───────▼────────────────────────────────▼─────────┐
        │ Agent 会话：契约（≤400 token）+ 按需 read 参考文档  │
        └───────┬──────────────────────────────────────────┘
                │ workspaceFiles.read(sessionId, statePath)
        ┌───────▼────────┐
        │ Client 控制台   │  sidebar.panellist + main，7 Tab
        │ 「能力闭环」     │  总览/项目/体检/技能/交接/记忆/运行
        └───────┬────────┘
                │ 动作：commands.execute → Host 运行中心（同一实现）
                └──────────────────────────────────────────→
```

### 3.1 档位：off / shadow / on（影子模式的定义）

| 维度 | `off` | `shadow`（影子） | `on`（接管） |
|---|---|---|---|
| 何时用 | 未标记工程；明确不想治理 | **首次接入观察期**（建议 3 个会话）、团队试点、状态源不可靠时降级 | 标记工程正式治理 |
| 注入 | 无 | 一条 ≤120 字符提示（见 §3.2） | 完整契约（≤400 token） |
| 行为约束 | 无 | **只记录，不阻断**：不要求 INTAKE、不要求门禁、FAIL 不影响对话 | 治理场景必须 INTAKE/证据/门禁/grill |
| 面板 | 空态「未接管」 | 顶部虚线 banner + 档位控件选中「影子」+ 「已观察 N/3」+ 「未阻断 M 次」+ 「升级为接管」 | 完整面板 |
| 门禁结果 | 不显示 | 显示，但标「参考，不阻断」 | 显示；FAIL 进阻断 |
| 退出/切换 | 面板切 on/shadow | 观察期满提示升级；随时可切 on/off | 随时可切 shadow/off |

**为什么需要影子**：接管会改变模型行为，直接全量开启风险高；影子让用户先看到「它会记录什么、门禁会判什么」而不改变当前工作习惯。**它不是「弱一点的接管」，而是「只观测、不执行」**。

**首次启用策略（已确认 A，2026-11-18）**：

1. 新标记工程：前 **3 个会话** 自动 `shadow`，面板计数并显示「再观察 1 次可升级」；
2. 3/3 后**提示**升级为 `on`（不自动升级，避免悄悄变硬）；
3. 用户随时可强制 `on`、回到 `shadow` 或 `off`。

### 3.2 Contract：注入什么（逐字稿）

**on（完整契约，约 1,450 字符 ≈ 350–400 token）**

```text
<system-reminder>
[capability-loop v2.9.6] 本工程已启用治理闭环；当前阶段 WIRE（第 4/7 阶段）。
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

**shadow（影子提示，约 90 字符）**

```text
<system-reminder>
[capability-loop · 影子] 本工程已记录治理状态（.dsh/loop/state.json）。只记录、不阻断；需要时按 state.next 执行，门禁失败不会拦住对话。
</system-reminder>
```

**注入纪律**：

- 只在首步注入一次；`state.json` 的 `digest` 变化时追加一条**增量**（≤3 行：阶段/阻断/下一步），不重发全文 → 追加式，KV 前缀缓存不受影响（对齐 `dsh-agent-instructions` 的 KV 策略）。
- **折叠进 pre-step 批次**，不用 `agent.inject()` 等待唤醒：按 `dsh-agent-instructions` 的做法，在 `agent/pre-step` 的 `decision.messages` 里插到用户消息之后（源码 `src/index.ts` L330–356），保证首个请求就带上。
- 失败**fail-open**：读文件失败/JSON 坏/版本不匹配 → 不注入，只记日志；面板显示异常。治理不能把聊天弄挂。
- 注入消息带来源标识（`capability-loop`），resume/fork 时按会话历史去重；**不新增 Session event 类型**（避免 Session 拒绝打开）。
- **路径不硬编码**：契约里的 skill 目录从 `ctx.skills` 目录/插件配置解析；商店安装目录可能是 `<handle>--dsh-capability-loop`。
- 不在 system prompt 里写「本工程已接管」——system prompt 是 profile 级、跨会话静态的，写进去会对所有项目生效。

### 3.3 State：唯一状态源 `.dsh/loop/state.json`

```jsonc
{
  "schema": 1,
  "skillVersion": "2.9.6",
  "mode": "on",
  "shadowSessions": 0,
  "project": {
    "name": "气量平衡月表",
    "root": "E:/work/gas-balance",
    "profile": "docs/loop/project-profile.md",
    "intakeAt": "2026-11-18T10:20:00+08:00"
  },
  "stage": "WIRE",
  "stageSince": "2026-11-18T14:05:00+08:00",
  "next": {
    "label": "补 design-context 后重跑设计门",
    "command": "powershell -NoProfile -ExecutionPolicy Bypass -File \"<skill-dir>\\loop-gate.ps1\" -TaskDir docs/design/gas-balance"
  },
  "checks": {
    "requirement": { "status": "PASS", "at": "2026-11-17T16:40:00+08:00", "exit": 0, "cmd": "loop-gate -Kind requirement", "evidence": ["docs/loop/requirement-review.md"] },
    "design":      { "status": "FAIL", "at": "2026-11-18T14:02:00+08:00", "exit": 1, "cmd": "loop-gate -Kind design", "evidence": [] },
    "test":        { "status": "PASS", "at": "2026-11-18T13:10:00+08:00", "exit": 0, "cmd": "loop-gate -Kind test", "evidence": ["docs/loop/test-report.md"] },
    "handoff":     { "status": "WARN", "at": "2026-11-18T14:10:00+08:00", "exit": 3, "cmd": "handoff-audit.py --slug gas-balance", "evidence": [] },
    "grill":       { "status": "MISSING", "at": null, "exit": null, "cmd": "loop-gate -RequireGrill", "evidence": [] },
    "environment": { "status": "PASS", "at": "2026-11-16T09:00:00+08:00", "exit": 0, "cmd": "loop-gate -Environment", "evidence": [] }
  },
  "blockers": [
    { "id": "D-01", "text": "design-context 缺现有系统截图", "owner": "lead", "due": "2026-11-19" },
    { "id": "D-02", "text": "交接包材料在工程外，Trae 读不到", "owner": "dev", "due": "2026-11-20" }
  ],
  "metrics": {
    "gatePassRate7d": 0.67,
    "rework7d": 2,
    "catalogChars": 3673,
    "driftAlerts": 2
  },
  "digest": "sha1:9f2c…",
  "updatedAt": "2026-11-18T14:12:00+08:00"
}
```

**写入方**：脚本（唯一写入者）——`loop-gate.ps1`、`capability-audit.ps1`、新增 `loop-state.ps1`（`set-stage` / `set-next` / `add-blocker` / `resolve-blocker` / `set-mode`）。插件只读，**除** P2 的 `set-mode`（经同一 Host 方法，写 `project.json.mode`）。

**容错**：文件缺失、JSON 坏、`schema` 不认、`skillVersion` 不匹配、`updatedAt` > 24 h（stale）——面板/注入都要有降级文案与修复动作，不显示空白、不伪造 0。

### 3.4 Panel 为什么是架构的一部分

1. **省 token**：面板承载详细状态，模型只拿 400 token 契约；否则要么漏治理，要么每会话 7k token。
2. **全量入口**：32 项能力有统一归口，用户不用记 15 个脚本名才知道能做什么。
3. **可证**：命令、退出码、时间、证据路径、输出尾部从终端滚动条变成可复查列表。
4. **可控**：档位、观察期、阻断、动作白名单都在一个地方。
5. **可迭代**：漂移、返工、通过率、版本/商店状态驱动月度体检与 skill 写回。

### 3.5 不走插件的降级路径（P0）

```markdown
<!-- dsh-capability-loop:on -->
## 能力闭环（本工程）
动手/交付前先读 `.dsh/loop/state.json`：按 `stage` 与 `next` 执行；没有该文件就按普通流程。
宣称完成必须有证据（命令 + 退出码/截图）；门禁用 `loop-gate.ps1`；交付前做 grill。
只读问答与单文件小改不套流程。
```

`AGENTS.md` 链由 DSH 自动注入，所以这段文字**一定进上下文**；状态由模型主动 `read` 一次。模型可能跳过那次 read——P0 是验证 `state.json` 与面板数据的过渡，P1 的宿主注入才是确定性升级。

---

## 4. 面板设计：覆盖全量能力的控制台

### 4.1 位置与导航（你已确认：全局主面板）

- **形态**：全局主面板，与 Plugins 同级；**不绑定单个会话**（工程级、跨会话）。
- **注册**：`sidebar.panellist` 列表项（id `capability-loop`，图标环形箭头，标签「能力闭环」/ "Capability loop"），`main` keyed slot 注册页面；`ctx.layout.selectPanel('capability-loop')` 可切换。
- **顺序**：插件之后、自动化任务之前；可用「更多」收起。
- **7 个 Tab**：总览 / 项目闭环 / 能力体检 / 技能治理 / 交接交付 / 记忆迭代 / 运行记录。1000px 内容宽下 7 个 4 字标签可容纳；更窄时 Tab 横向滚动（沿用管理页 Tab 规格 34px）。
- **为什么不做右侧栏**：右侧栏是会话级 45% 宽，闭环状态跨会话；右上状态点留 P3。

### 4.2 能力覆盖矩阵（全量，32 行）

**接入与阶段（9）**

| 能力 | 面板位置 | 数据源 | 状态口径 |
|---|---|---|---|
| 项目接入六问 / profile / 真相源 | 总览 · 项目接入卡；项目闭环 · INTAKE | `project-profile.md`、`state.project` | 已答 N/6；缺失即 INTAKE 未完成 |
| 七阶段与出口 | 项目闭环 · 阶段轨道 | `state.stage/checks` | done/current/blocked/todo |
| 门禁聚合（design/requirement/test） | 项目闭环 · 门禁列表；运行记录 | `loop-gate` 输出 + `state.checks` | PASS/WARN/FAIL/MISSING + exit + 时间 |
| 环境验收 | 项目闭环 · 门禁列表 | `loop-gate -Environment` | 同上 |
| 设计前置 `design-context` + `product-context` 扫描 | 项目闭环 · 设计门展开 | 文件存在 + 门禁判定 + 扫描线索 | 缺文件 FAIL（小改需显式豁免） |
| 需求规范（SRS ≥80、三遍评审） | 项目闭环 · 需求门 | `30-requirement` 产物 + 门禁 | PASS + 文档路径 |
| 测试（台账 A/B/C、追溯） | 项目闭环 · 测试门 | `40-testing` 产物 + 门禁 | PASS + 用例数 |
| grill 三域 | 项目闭环 · 门禁列表 | `grill-*.md` | 未运行 / 已记录（打回数） |
| 角色与评审门（G1/G2/G3） | 项目闭环 · 团队与评审门 | `agents` 角色 + 评审记录 | 角色数；G1/G2/G3 PASS/未做 |

**DSH 体检与运行时（4）**

| 能力 | 面板位置 | 数据源 | 状态口径 |
|---|---|---|---|
| 九组体检 A–I（含开工基线 8 项） | 能力体检 · 九组指标 | `capability-audit.ps1` | 每组 PASS/WARN/FAIL/SKIP |
| 漂移对比 | 能力体检 · 漂移卡 | `.tmp/capability-loop/audit-state.json` | 指标增减 + 告警数 |
| 运行时修复（检索/桌面壳/Token/死重量） | 能力体检 · 可修复项 | `20-runtime-fix` 判定 + audit | 可修复 N 项 + 将写文件 |
| Token / catalog 成本 | 技能治理 · 成本卡；能力体检 | audit B + metrics | 字符、占比、趋势 |

**技能与插件（5）**

| 能力 | 面板位置 | 数据源 | 状态口径 |
|---|---|---|---|
| 本 skill 版本/安装来源/商店最新 | 技能治理 · 本 skill 卡 | `version.json` + `skill-status.ps1` | 版本差、origin、更新只提示 |
| 死重量/超长描述/触发冲突/无触发词 | 技能治理 · 治理卡 | audit B | 名称清单 + 建议动作 |
| 插件与市场重复/失效行 | 技能治理 · 插件卡 | `plugin_manager` 清单 | 数量 + 重复数 |
| 上架打包（manifest/SHA256/ZIP） | 技能治理 · 上架包行；运行记录 | `package-skill.ps1` | 最近包、校验结果、动作 |
| 更新提示（不自动覆盖） | 技能治理 · 本 skill 卡 | 市场 `panel.json/installed.json` | 落后版本提示 |

**交接与交付（8）**

| 能力 | 面板位置 | 数据源 | 状态口径 |
|---|---|---|---|
| 交接四件套 + 批次（≤3 任务/批） | 交接交付 · 交接包卡 | `docs/handoff/<slug>/` | 4/4、批次数、PROMPT 指向本批 |
| Trae 安装/进程/工程匹配 | 交接交付 · Trae 卡 | `trae-status.ps1` | MATCH / MISMATCH（不匹配禁发） |
| 模块/路由预检 | 交接交付 · 前置校验 | `module-preflight.py` | NONE/EXISTS/WEAK |
| 交接包体检 A–F | 交接交付 · A–F 卡 | `handoff-audit.py` | 六组状态 + exit |
| 网关前缀一致性 | 交接交付 · 前置校验；A–F 的 F 组 | `handoff-audit.py` F 组 | 前缀集合 + 反向指令 |
| 视觉 QA（A/B/C 路径） | 交接交付 · 前置校验 | `visual-qa-check.ps1` | exit 0/2 + 补测方式 |
| 交接冒烟与回滚 | 交接交付 · 冒烟卡 | `handoff-smoke.ps1`、`rollback.ps1` | 最近一次结果 + 备份路径 |
| 迁移/交付基线包（文档 01–07 + rollback） | 交接交付 · 迁移卡 | 迁移包目录 + `rollback.ps1` | 包是否存在、最近交付时间 |

**记忆/迭代/运行（6）**

| 能力 | 面板位置 | 数据源 | 状态口径 |
|---|---|---|---|
| 用户偏好（维度/来源/过期） | 记忆迭代 · 偏好卡 | `memory/user-profile.md` | N 条 + 过期告警 |
| rules（同类 ≥3 次） | 记忆迭代 · 规则卡 | `memory/rules.md` | N 条 + 触发次数 |
| retro / 返工趋势 | 记忆迭代 · Retro 卡 | `memory/retro` + metrics | 最近 3 条 + 7/30 天 |
| 版本与 CHANGELOG | 记忆迭代 · 版本卡 | `version.json`、`CHANGELOG.md` | 最近 3 版 |
| 运行任务/日志/取消 | 运行记录 | Host 运行中心 | 进行中/历史/输出/退出码 |
| 状态源/回滚 | 总览 · 状态源卡；运行记录 | `state.json` + 备份 | 路径、schema、最近写入 |

### 4.3 各 Tab 规格（v0.3 收敛后）

| Tab | 首屏区块 | 交互 | 空/异常 |
|---|---|---|---|
| **总览** | 4 KPI；**6 张能力卡**（项目/体检/技能/交接/记忆/运行，各带 2–3 子项计数）；下一步 + 最近活动 + 状态源；「查看全部 32 项」 | 点卡进入对应 Tab；下一步可运行/复制；32 项明细进抽屉 | 无状态 → 空态；状态坏 → 异常态 |
| **项目闭环** | 阶段轨道；**单一门禁列表**（「本阶段/全部」筛选、当前阶段标签、展开证据）；阻断与待办；本阶段出口作为纯证据清单 | 一个主按钮「运行门禁 ▾」；行点击展开证据/命令；阶段点开看出口 | 无门禁记录 → 「未运行」；无阻断 → 「无阻断」 |
| **能力体检** | A–I 九组 chip（**5+4 两行**）；九组指标表；漂移卡；可修复项 | 运行体检（-Strict 可选）；查看报告；修复项展开「将写文件」 | 无历史 → 首次基线；审计失败 → 错误态 |
| **技能治理** | 本 skill 版本/商店；catalog 成本；插件与市场；死重量/触发冲突；Token | 运行打包；停用/发 Trae 等 L3 动作标「仅复制」；更新提示「去商店」 | 无商店记录 → 「仅本地」；无死重量 → 「无」 |
| **交接交付** | Trae 状态；交接包卡；前置校验；A–F 体检；冒烟/回滚/迁移 | 交接体检（L1）可直接跑；发送/生成（L3）标「仅复制」；Trae 不匹配禁发 | 无交接包 → 空态；Trae 不匹配 → 禁用 |
| **记忆迭代** | 偏好卡；规则与返工；Retro；版本/CHANGELOG | 查看条目；打开源文件；返工趋势 | 无 memory → 引导创建；偏好过期 → 告警 |
| **运行记录** | 运行中；历史；白名单；**动作分级（L1/L2/L3）**；确认弹窗 | 主「运行」→ **模态确认**（命令/工作目录/将写/超时/取消）；取消 kill 进程树 | 无运行 → 空态；失败 → 输出尾部 |

> 「首屏 ≤5 块」按**区块**计：总览 = KPI / 6 卡 / 底部三卡（3 个区块）；32 项明细不是首屏内容，进「查看全部」抽屉。工作台 Tab 每屏 ≤5 个卡片区块。

### 4.4 四态 + 影子态

| 状态 | 触发 | 页面表现 |
|---|---|---|
| A 已接管 `on` | `project.json` 且 `mode=on` | 完整 7 Tab；档位选中「接管」；KPI「开启 on」 |
| B 影子 `shadow` | `mode=shadow` 或首启观察期 | 顶部虚线 banner「只记录、不阻断 · 已观察 2/3」+ KPI「影子 shadow · 未阻断 1 次」+ 档位选中「影子」+ 「升级为接管」；门禁标「参考」 |
| C 未接管 `off` | 无标记/关闭 | 隐藏 Tab；空态：「这个工程还没有接入能力闭环」+ 说明覆盖 32 项能力 + 「复制接入命令」「查看接入示例」；档位选中「关闭」且**禁用**；**不提供「打开状态文件」**（无文件，死动作） |
| D 异常 | JSON 坏 / schema 不认 / 版本不匹配 / stale >24h | 顶部错误条 + 只读降级；已隐藏阶段/门禁（避免显示过期结论）；保留「最近体检」；给「定位文件」「重新体检」 |

加载：骨架块（KPI 4 + 列表 3 行），`prefers-reduced-motion` 静止；首屏失败不弹 toast，刷新失败才 toast。

### 4.5 运行中心：一步到位跑门禁（你已确认）

**白名单（唯一可执行集合；参数白名单校验，不拼接字符串）**

| 动作 | 脚本 | 参数 | 写什么 | 超时/取消 |
|---|---|---|---|---|
| 体检 | `capability-audit.ps1` | `-Workspace <当前>`、可选 `-Strict` | `.tmp/capability-loop/audit-state.json` | 180s；kill 进程树 |
| 门禁 | `loop-gate.ps1` | `-TaskDir <校验路径>`、`-Kind`、可选 `-RequireGrill` | `.dsh/loop/state.json`（通过 `-StateFile`） | 120s |
| 交接体检 | `handoff-audit.py` | `--workspace`、`--slug`（白名单字符） | 无（只读） | 60s |
| 模块预检 | `module-preflight.py` | `--project`、`--keyword`、`--alias` | 无（只读） | 60s |
| 上架打包 | `package-skill.ps1` | `-Handle`、`-Slug` | `out/` ZIP + manifest + SHA256 | 180s |
| 视觉探测 | `visual-qa-check.ps1` | `-OutDir` | `.tmp/visual-qa` 截图 | 120s |
| 版本检查 | `skill-status.ps1` | `-Workspace` | 无（只读） | 60s |

**动作分级（避免「全量面板 = 全量执行」的误解）**

| 级 | 动作 | P2 行为 |
|---|---|---|
| L1 可运行 | 上表 7 个脚本 | 面板确认后直接跑，显示输出/退出码，写回 state |
| L2 一键切换 | 接管/影子/关闭（`set-mode`） | 确认后写 `project.json.mode`，重启注入生效 |
| L3 只给命令/链接 | 停用 skill、发送 Trae、生成交接包、生成迁移包、商店更新、grill 访谈 | 复制命令或打开文档/商店；**面板不代执行** |
| L4 后续 | L3 中低风险项（如停用 skill） | 纳入白名单后再开放，复用同一确认/超时/取消 |

> 这样「全量容纳」指**状态与入口全量**；「可运行」仍限定在白名单，避免面板变成任意 shell。

**确认模态（所有 L1/L2 动作；见 [确认弹窗预览](panel-run-modal-dark.png)）**

- 内容：标题、完整命令、工作目录、**将写文件**、不会写什么、超时、取消方式。
- 按钮：取消 / 确认运行；默认焦点「取消」，Esc 关闭并还焦。
- 运行中：模态不关，显示进度与「取消」；取消后显示退出码与输出尾部。
- 失败/被拒绝：显示原因 + 复制命令；**不改写结论**。

**交互规范**

- 每次运行先弹**确认**：完整命令、工作目录、将写的文件、超时、取消方式；「确认运行」「复制命令」「取消」。
- 运行中：进度/已运行时长/输出流（尾部 50 行）；「取消」发 kill 到进程树并等待退出；同一工作区同时只允许 1 个动作（其余排队或拒绝）。
- 结束：显示 exit code、时长、结果徽标；写入 `state.json`（若适用）；刷新对应 Tab；失败时保留输出尾部与日志路径。
- 历史：最近 20 条，含动作/参数/exit/时长/时间；可展开输出；可复制命令复跑。
- 安全：只从白名单构造 argv；用户可输入的只有 TaskDir/Slug/Keyword/Handle 等**受校验字符串**；禁止 shell、管道、重定向、`..` 越界；`allowRun: false` 时只复制命令。
- 权限：动作是用户主动触发（不是模型），仍需确认；执行走与 bash 工具相同的沙箱策略；面板显示「将写」清单。

> 依赖：P1 的 Host 插件注册会话命令（`ctx.commands.register()`），P2 的面板用 `ctx.remote.commands.execute()` 调用，Host 方法复用同一实现（`dsh-doc/references/user-actions.md` 的「一个操作、两个调用方」）。

### 4.6 组件与 token（沿用，不自造）

| 元素 | 规格 |
|---|---|
| 页面 | `max-width: 1000px`（含 7 Tab 的稍宽布局）；左右 40px；顶部 22px；块间距 12–20px |
| 页头标题 | 20px/600（不新增字号档） |
| 字号阶梯 | 标题 20/600 · 区块 14/600 · 正文 13 · 卡描述 12 · meta/标签 11 · 运行输出 11 等宽；不新增字号档 |
| Tab | 34px 高、选中 2px 底边、`aria-selected`；横向可滚 |
| 指标块 | `--dsw-alias-card-fill`、`--dsw-radius-md`、内距 10–12px；数值 18px/600；标签 11px |
| 阶段轨道 | 连接线 1px `border-l2`；当前 `state-business-primary`；完成 `state-success-primary`；未开始 `state-idle-primary` |
| 结果徽标 | **文字 `label-primary`**；语义色只在 5px 圆点 + 10% 底色（PASS/WARN/FAIL/未运行）；颜色不是唯一载体 |
| 行 | 36px；hover 仅 `@media (hover:hover)`；分隔线 `border-l1` |
| 运行输出 | 等宽字体（`--ds-font-family-code`）、11px、`bg-base` 内嵌、尾 50 行 |
| 焦点 | `--dsw-focus-ring-color` 2px、`outline-offset: 2px` |
| 图标 | 16px 线性、`currentColor`、8px 状态点 |

> 不新增颜色值：影子用 `state-warn-secondary` 虚线；只读用 `label-tertiary` + 锁；运行中 `state-business-primary`。

### 4.7 响应式

| 宽度 | 行为 |
|---|---|
| ≥1280 | 能力地图 4 列；双栏（主区 + 320 侧栏）用于总览/项目 |
| 1024–1279 | 能力地图 3 列；单栏；侧栏块移到下方 |
| 768–1023 | 2 列卡片；Tab 横向滚动；指标块 2×2 |
| <768 | 1 列；Tab 横向滚动；阶段轨道改纵向列表；页宽 inset 20px；动作行 44px |

### 4.8 无障碍

- Tab：`role="tablist"` / `role="tab"` / `aria-selected`；左右方向键切换。
- 档位：`role="radiogroup"` + 方向键；确认弹窗焦点进入并 Esc 关闭还焦。
- 门禁/运行行：`<button aria-expanded>` 展开输出；结果徽标带文字，不靠颜色。
- 对比度：正文约 16–19:1、次级约 6–10:1（按 token 值估算，未用工具实测）；运行输出用次级色，≥4.5:1 待实测。
- 动效：0.2s `--ds-ease-in-out`；`prefers-reduced-motion` 关闭。

### 4.9 数据与刷新

- **读通道**：`ctx.remote.workspaceFiles.read(sessionId, '.dsh/loop/state.json')`（现有 Remote）；第三方 bundle 不能给 `dsh-api-remotes` 新增命名空间（其 README §Known Limitations：capability set 构建期固定），所以不自造 `capabilityLoop.status`。全局页按**当前会话**授权读；无会话 → 空态「先打开一个会话」。
- **刷新**：打开读一次；`workspaceFiles.changes` 推变更（P2）；运行结束主动重读；不做前端轮询。
- **版本**：`skillVersion` 与 Host 从 skill 目录读到的 `version.json` 比对；不一致只读 + 提示（不自动更新）。
- **动作**：`commands.execute()` → Host 运行中心；面板只展示与触发，不直接 exec。
- **数据边界**：只读 `.dsh/loop/`、`.tmp/`、`docs/loop/`、`docs/handoff/`、`memory/` 与 skill 自身；不读工程源码内容（除门禁脚本需要的路径）。

---

## 5. 分阶段落地（含你的决定）

| 阶段 | 交付 | 依赖 | 验收 | 回滚 |
|---|---|---|---|---|
| **P0 无插件**（1–2 天） | `loop-state.ps1`；`loop-gate`/`capability-audit` 增 `-StateFile`；`SKILL.md` 增接管协议 + 两段注入稿；`05-intake` 生成 `project.json`；AGENTS.md 12 行片段 | 无 | 真实工程：`project.json` 生成；gate 后 state 字段齐全；`/dsh-capability-loop` 按契约执行；未标记工程零变化 | 删 `project.json` + 回退版本；新参数不影响旧调用 |
| **P1 自动接管**（3–4 天） | 宿主插件：Arm 判定 + Contract 注入 + 会话命令注册；启动观察期计数；不做 UI/Remote | 0.2.2-rc.3；`agent/pre-step` | 标记工程 10/10 注入；未标记 10/10 不注入；shadow 只注入提示；坏 JSON 不崩不注入；resume 不重复 | 关闭插件行；删除 bundle |
| **P2 控制台**（5–6 天） | 客户端半：`sidebar.panellist` + `main`；7 Tab；四态+影子；**运行中心（白名单 + 确认 + 输出 + 取消 + 写回）**；`workspaceFiles` 读 + `commands.execute` | P1 | 7 Tab 全部可达；375/768/1024/1440 截图；暗/亮各一；运行 = 命令行同结果；取消可停；状态写回；失败不改写结论 | 关客户端行；关 `allowRun` |
| **P3 增强**（2–3 天） | watch 推送、右上会话状态点、历史 20 条导出、告警（stale/版本/阻断） | P2 | 不轮询；告警不误报；导出可打开 | 关增强开关 |

> 每个阶段都按本 skill 自己的纪律：P0 产物过 `loop-gate`，P2 界面过 `-Kind design` + grill。

---

## 6. 风险与反模式

| 风险 | 表现 | 对策 |
|---|---|---|
| 过度治理 | 问一句「这函数干嘛的」也被追问六问 | 契约写死豁免；INTAKE 只在「动手/交付」；小改三问 |
| 影子被误解 | 以为影子=弱接管，结果门禁 FAIL 仍不阻断 | 面板 banner/KPI 明写「只记录不阻断」；观察期倒计时；升级需确认 |
| 信息过载 | 32 项能力 + 7 Tab 一屏塞满 | 总览只放 12 卡 + 下钻；每 Tab 首屏 ≤5 块；能力地图可点进 |
| 运行动作误伤 | 面板跑脚本改了不该改的文件 | 白名单 + 参数校验 + 「将写」清单 + 确认 + 超时/取消 + 同一工作区串行 |
| 假接管 | 注入成功但模型不照做 | 面板显示门禁证据；「完成但无 gate」在收口时由 skill 自查（软）；不承诺语义拦截 |
| 状态腐烂 | state 一周没更新仍显示 PASS | stale >24h 降级「未核实」；不隐藏 |
| 版本漂移 | 面板 2.9.6、装 2.9.5 | 版本不匹配 → 只读 + 「按商店更新」 |
| 插件崩溃 | 注入抛错导致对话失败 | fail-open；面板显示「guard 未运行」 |
| 权限 | 面板动作越权 | 走 Host 同一策略；默认只读；`allowRun` 可关 |
| 数据外泄 | state 提交到公开仓库 | `state.json` 默认 `.gitignore`；`project.json` 只放名称/档位/相对路径 |

**反模式**：把整套规则塞进 system prompt；为每个项目改 AGENTS.md 全量；用颜色当唯一状态；面板里放「一键跑完七阶段」；面板直接 exec 任意命令。

---

## 7. 你的决定（已记录）

| # | 决策 | 结论 | 落点 |
|---|---|---|---|
| Q1 | 标记工程默认档位 | **A（已确认）**：首启 3 会话影子观察 → 提示升级 `on`；不自动升级 | §3.1 策略；`project.json.mode` + `shadowSessions` |
| Q2 | 面板位置 | **全局主面板**（已确认） | §4.1 |
| Q3 | 面板动作深度 | **一步到位可跑门禁**（已确认） | §4.5 白名单 + 确认 + 输出 + 取消 |
| Q4 | 状态目录 | **`.dsh/loop/`**（已确认） | §3.3；`state.json` 默认 gitignore |

Q1 已确认走 **A**：首启 3 会话影子观察 → 再提示升级。影子本身在任何方案下都保留，供随时切；用户也可在观察期内直接切 `on`。

---

## 8. 未实测与证据清单

| 项 | 状态 | 说明 |
|---|---|---|
| 侧栏 `sidebar.panellist` 注册（第三方 bundle） | 未实测 | 依据 `dsh-client-ui-sidebar` / `dsh-client-ui-plugin-manager` README；P2 用真实 bundle 验证 |
| 第三方 bundle 新增 Remote | **文档核实不可行** | `dsh-api-remotes` README §Known Limitations；改用 `workspaceFiles` |
| 面板读状态通道（`workspaceFiles` + 当前会话） | 未实测 | 需要 sessionId 授权；无会话降级空态；P2 验证 |
| `agent/pre-step` 注入与 resume 去重 | 未实测 | 依据 `dsh-agent-instructions` 源码 L245–356；P1 夹具验证 |
| 注入消息 `source.kind` | 未核实 | 是否允许第三方自定义 kind 未查；不允许则用固定前缀 + 内容判定去重 |
| 运行中心子进程/取消/超时 | 未实测 | P2 用真实脚本验证；Windows 进程树 kill 需专门验证 |
| 7 Tab 在 960/768/375 的真实渲染 | 未实测 | 仅出 1440 稿；P2 补三档截图 |
| 注入 token 数 | 估算 | 按字符 ≤1,600 ≈400 token；P1 实测 |
| 对比度 | 估算 | 按 token 值；未用 axe/Lighthouse |
| 独立 Reviewer | 未指派 | grill 为设计者自问；判定「有条件交付」 |

> **门禁实测（2026-11-18）**：`loop-gate.ps1 -TaskDir docs/design -Kind design` → `RESULT: PASS（PASS=2 WARN=0 FAIL=0 SKIP=1）`，exit 0；SKIP 为 `upgrade/team/gate-check.ps1` 缺失（本仓库是 skill 源，不含交付基线包）。
>
> 自检：`design-context.md` 已出（PARTIAL）；差异清单见其 §6；四态+影子全覆盖；token 全部来自 `design-platform.css`/`base.css`；grill 记录见 [grill-design-20261118.md](grill-design-20261118.md)；设计自审见 [review-20261118-self.md](review-20261118-self.md)（P0 已修，P1 未收敛，P2 面板暂缓）。



