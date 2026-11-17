---
name: dsh-capability-loop
version: 2.9.5
description: DSH 能力升级与治理闭环：审计 skills/插件/运行时 → 修检索/桌面壳/Token 死重量 → 串接需求、测试、设计、团队与 Trae 分工 → 门禁验收 → 经验写回自身迭代。Use when 用户要升级/优化/体检 DSH、治理插件与技能、修会话检索或进程退出、降 Token、沉淀或迁移这套方法、迭代本 skill；单点需求/设计/测试任务走各自规范，不加载本 skill。
---

# DSH 能力升级与治理闭环（Capability Loop）

> **定位**：这是「meta 层」skill —— 把「DSH 自身的升级治理」与「在这台 DSH 上做项目/需求/设计/测试/交接的方法」串成一条**可重复执行、可度量、可回滚、可持续迭代**的闭环。
> **版本**：`version.json`（权威）+ `CHANGELOG.md`（每次写回必须 bump）+ `SKILL.md` frontmatter 的 `version`（必须与 `version.json` 一致；技能市场用它显示「已安装版本」）。**首次使用先读 `QUICKSTART.md`**（10 分钟上手）。
> **血缘**：session-0d908c48（DSH 审计与升级、团队/设计/需求/测试方法、迁移交付）+ session-3ef140c9（DSH↔Trae 分工交接）合并为单一 skill；证据与产物映射见 `references/90-provenance.md`。
> **结构**：本文件=路由与纪律；`README.md`=商店/人读概览；`references/`=深文档；`scripts/`=可执行检查；`templates/`=填空模板。
> **上架商店**：DSH 技能市场只负责安装，上架走 ClawHub 发布 → SkillHub 同步；命令与未实测项见 `references/95-store-publish.md`。

## 0. 触发与边界

**满足任一即加载本 skill：**

1. 升级/优化/体检 **DSH 本身**：skills、插件、profile patch、桌面壳、会话检索、Token/上下文成本。
2. 治理**死重量与触发混乱**：装了跑不起来的 skill、重复插件市场、超长 description、无触发限定的 skill。
3. 修 **P0 故障**：`session_search` 不可用、进程反复退出/「任务已停止」、3080 `EADDRINUSE`。
4. 把这套「需求→设计→测试→交接→验收」方法**沉淀成规范、迁移给同事、或迭代本 skill 自身**。
5. 需要判断「这套配置/流程是否还成立」——先体检再下结论。

**不加载（直接走对应规范）：** 单点需求评审（`standards/requirement-spec-standard.md`）、单页面 UI 设计（`ui-design-production`）、单次自动化测试（`upgrade/team/testing-workflow.md`）、单次交给 Trae 实现（`feature-handoff`）。本 skill 只在需要**串联、治理、沉淀、迁移**时加载。

## 1. 七阶段闭环（按需取段，不强行走完）

| 阶段 | 目标 | 动作入口 | 出口证据（无证据不算完成） |
|---|---|---|---|
| **INTAKE 接入** | 先弄清项目，再动工 | `references/05-intake.md` + `templates/project-profile.md` | `project-profile.md`（≤6 问的答案、真相源、目标与验收、专家编排） |
| **AUDIT 体检** | 先量化，再判断 | `scripts/capability-audit.ps1` + `references/10-audit.md` | 报告：九组指标 + 与上次的**漂移对比** + `文件:行号` |
| **FIX 修复** | 只动该动的，可回滚 | `references/20-runtime-fix.md` | DryRun → apply → verify 三步输出；备份路径 |
| **WIRE 串接** | 产品上下文、方法、角色、门禁接线 | `30-requirement.md`、`40-testing.md`、`50-design-team.md`、`55-design-intake.md` | 规范/剧本落盘 + 门禁可执行（正例/反例） |
| **HANDOFF 交接** | DSH 出规格与设计，Trae 只实现 | `references/60-handoff.md` + skill `feature-handoff` | `docs/handoff/<slug>/` 四件套 + `check-handoff` prepare/deliver |
| **GRILL 自对抗** | 交付前把「感觉没问题」逼成证据 | `references/75-grill.md` + `templates/grill-checklist.md` | `grill-YYYYMMDD.md`（≥1 个打回并修正；未解决项进 D-ID） |
| **GATE 验收** | 统一门禁 + 写回 | `scripts/loop-gate.ps1` + `references/80-evolution.md` | 门禁输出 + `CHANGELOG`/`version.json` 更新 + retro 条目 |

> 顺序纪律：**INTAKE 未清不动工；AUDIT 未出证据不做 FIX；FIX 未验证不 WIRE；GRILL 未做不宣称完成（记录缺失默认 WARN，需硬门时给 `loop-gate.ps1 -RequireGrill`）；GATE 未过不宣称完成。**

## 2. 不变式（违反即回滚 / 判失败）

1. **证据先于结论**：任何「已修复/已生效/已通过」必须带命令、退出码、关键输出或截图；不能实测的写「未实测 + 原因 + 补测方式」。
2. **PASS 必须来自非实现者**：写代码/写设计的人不得给自己的产物 PASS；Lead 终门基于他人的评审记录。
3. **写回本 skill 必须版本化**：改 `references/`/`scripts/`/`SKILL.md` 任意一处，同一提交内更新 `version.json` + `CHANGELOG.md`，并至少跑 1 正例 + 1 反例回归。
4. **批量改，不碎改**：工具集/skill 清单/catalog 变化会击穿 prompt 前缀缓存；同类改动一次做完。
5. **本机脚本 = Windows PowerShell 5.1**：禁 `??`/三元 `? :`/`&&`/`-AsArray`/`#requires -Version 7.0`；含中文的 `.ps1` 必须 **UTF-8 带 BOM**；**任何编辑后都要重新补 BOM**（编辑工具会剥掉）；运行用 `powershell -NoProfile -ExecutionPolicy Bypass -File`。
6. **不谎报浏览器/视觉**：视觉验收前先跑 `scripts/visual-qa-check.ps1`——exit 0 走 **A 路径（Chrome headless 批量截图，已实测可渲染）**；exit 2 属**权限受限**，必须**显式提示用户**选 A（切 danger-full-access）/ B（用户截图 + `read_image`）/ C（标「未实测 + 原因 + 补测方式」，不得判 PASS）；agent-browser 在部分环境会挂起，不作主路径。不许用「应该没问题」代替截图。
7. **长会话不切模型**：切模型只在任务边界/新会话；贵模型只用于短上下文规划/评审。
8. **尊重既有修改权**：迁移给同事的包是**基线**，不锁定、不遥感、不自动更新；可随意 fork/改名/改阈值。
9. **先问项目再动手**：新项目/新模块/新合作，先按 `05-intake.md` 问清（≤6 问、一次问完），产出 `project-profile.md`；不懂业务不装懂。
10. **先读现有设计体系再出稿**：任何设计稿/原型前必须有 `design-context*.md`（框架/组件库/主题 token/状态/样本页），否则 `loop-gate` 的 design 类别直接 FAIL；差异必须写清「为什么不用现有方案」。
11. **文档集交付必须出 HTML 总览**：面向人的 `.md` 文档集 → 生成单文件 HTML（搜索/目录/明暗双主题/打印/设计稿预览位），交给用户前自测可打开。可用源工作区 `tools/build-docs-html.py` 做模板，但它是**项目专用**的（改 PROJ/DOCS/标题 3 处常量），换项目必须改配置或写等价脚本，不得直接套用旧项目标题。
12. **交付前必须 grill**：原型/设计/需求/对外文档交付前，按 `75-grill.md` 做自对抗评审，记录 `grill-*.md`；没有「会被打回」的问题 = 问得不够。默认缺失记 WARN，交付前硬门用 `loop-gate.ps1 -RequireGrill`（缺失即 FAIL）。三域分别用 `grill-design-*.md` / `grill-req-*.md` / `grill-test-*.md`。
13. **更新只提示不代做**：安装版与源/商店记录不一致时只提示；上架后**更新由商店负责**（安装/更新/回滚都在商店 UI），不得手工覆盖商店安装版。见 `scripts/skill-status.ps1`、`scripts/package-skill.ps1`。
14. **记住用户偏好**：用户偏好写工作区 `memory/user-profile.md`（不是 skill 正文），任务前读取并按偏好交付；偏好变化记变更记录。
15. **交接前必须确认工程匹配**：Trae 当前打开的工程必须等于目标工程（`trae-status.ps1 -Workspace <ws> -RequireMatch` → MATCH），否则不得让 Trae 改代码（防改错项目）。
16. **发布物可校验**：上架包必须由 `package-skill.ps1` 生成（frontmatter/version/CHANGELOG 校验 + `manifest.json` + `SHA256SUMS.txt`），发布前不得手工拼包。

17. **交接前必须做模块/路由预检**：目标工程里若已存在同名/相似模块，**未与开发者确认前不得默认新建**。跑 `scripts/module-preflight.py --project <工程根> --keyword '<模块名>' --alias <英文别名...>`：0=NONE（默认新建路由）、1=EXISTS（必须先确认复用/改造/另建）、3=WEAK（相似线索，先确认复用）。EXISTS 时必须在交接包 brief.md 写明复用/改造决定与路由归属。
18. **交接包必须先体检再交**：`handoff-audit.py --workspace <工程根> --slug <slug>` 退出码 `1`（有 FAIL）不得交。它查六组（A–F）：材料是否都在**工程内**可读（跨工作区的设计稿/规格必须先拷到 `docs/handoff/<slug>/materials/`）、`acceptance`/`record` 引用的证据是否真存在于 `evidence/`、`tasks.md` 有无批次段且 `PROMPT.md` 指明本批（**一批 ≤3 任务**）、有无设计依据/`design-context`。上下文压缩导致的开发偏移，多半就是没分批 + 材料读不到。

19. **接口契约必须写全网关前缀**：交接包契约里的 URL 要含工程既有前缀（如 `/png/<服务>/<动作>`），host 不写、`/api` 不是网关前缀；出现「不要写 `/png`」这类反向指令一律视为缺陷。`handoff-audit.py` 的 F 组会自动校验：前缀集合只统计 `src/api/**`（不扫 `public/`/`router/`，页面路由自动排除），「不要/不写/不含/不需要写 … `/png` 前缀/硬编码」视为反向指令直接 FAIL；**「不得漏写」是正向要求，豁免**。判定按**位置序**：去 `**`/反引号装饰、剥离不含 `/png` 的括号说明、按 `。；` 切句后，**否定词必须位于「`/png` … 前缀」之前**才算反向指令；「不写 host」「不含 `/api`」「…必写、host 不写」「A 与 B 不是同一前缀」不误报。前缀集合只取 `src/api/**`（排除 test/mock，排除 `api` 段），出现 1 次的段降级为 WARN 需人工确认。工程无 `src/api` 时 F-skip 不适用。

## 3. 开工基线（先核，不背旧结论）

每次任务开始先核这 8 项（脚本已覆盖）：`DSH_HOME` 路径与读写权限 · 活动/停用 skill 数量 · `profiles/web/cordis.patch.yml` 的检索三件套（`path/openAt/journalMode`）与超时 · `session-index.sqlite*` 是否存在及大小 · 桌面壳 `main.js` 的健康检查锚点（`HEALTH_PROBE_TIMEOUT/HEALTH_FAILURE_LIMIT/HEALTH_DOWN_WINDOW_MS/isTcpAccepting`） · `~/.dsh/agents` 角色数 · 工作区资产（`AGENTS.md`/`memory`/`standards`/`tools`/`upgrade/team` 门禁） · PowerShell/Node/Python 版本。
> 源环境 2026-11-12 的快照值见 `references/00-baseline.md`；**只作对照，不当事实**。
> 项目级基线：先有 `project-profile.md`（接入）；设计任务先有 `design-context.md`（现有系统设计体系）。两者缺失时先补，不进入下一阶段。

## 4. 快速命令

```powershell
$sk = "$env:USERPROFILE\.dsh\skills\dsh-capability-loop"

# 体检（只读；九组指标 + 与上次的漂移对比；报告默认写到 <工作区>\.tmp\）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\capability-audit.ps1" -Workspace "<工作区>"

# 产品/设计上下文线索（扫描工程：框架/组件库/主题/页面接口规模）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\product-context.ps1" -Project "<工程根>"

# 任务级门禁（自动识别 design/requirement/test；design 缺 design-context 会 FAIL；交付前硬门 grill 加 -RequireGrill）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\loop-gate.ps1" -TaskDir "<任务目录>" [-RequireGrill]

# 环境级验收（等价于跑 upgrade/post-restart-check.ps1）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\loop-gate.ps1" -Environment

# Trae 关联状态（安装/进程/当前打开工程是否=目标工程/交接包进度）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\trae-status.ps1" -Workspace "<工程根>"
# 交接前硬门：工程不匹配就 exit 1
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\trae-status.ps1" -Workspace "<工程根>" -RequireMatch

# 视觉验收能力探测（0=A 可用；2=权限受限→必须显式让用户选 A/B/C）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\visual-qa-check.ps1" -OutDir "<工作区>\.tmp\visual-qa"


# 模块/路由预检（交接前必跑；0=NONE 新建 / 1=EXISTS 需确认 / 3=WEAK 需确认）
python "$sk\scripts\module-preflight.py" --project "<工程根>" --keyword "资源需求" --alias resource-demand resourceDemand
# 交接包体检（材料可达性/证据对账/批次/设计依据；1=有 FAIL 不得交、3=仅 WARN、0=可交）
python "$sk\scripts\handoff-audit.py" --workspace "<工程根>" --slug "<slug>"
# 交接链路冒烟（临时工程，不碰真实项目；首次上真实工程前先跑）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\handoff-smoke.ps1" -Workspace "<工作区>"

# 上架商店前打包（校验 frontmatter/version/CHANGELOG + manifest + SHA256 + zip）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\package-skill.ps1" -Handle "<store-handle>" -Slug "dsh-capability-loop"

# 发布到 ClawHub（上架 = ClawHub publish → SkillHub 同步 → DSH 市场可装；详见 references/95-store-publish.md）
# npm.cmd i -g clawhub
# clawhub login
# clawhub skill publish "<工作区>\tools\capability-loop\skill\dsh-capability-loop" --slug "dsh-capability-loop" --name "dsh-capability-loop" --changelog "vX.Y.Z: 变更摘要"

# 版本与更新提示（商店优先：读技能市场记录；源目录仅开发对照；不自动更新）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\skill-status.ps1" -Workspace "<工作区>"

# 体检收紧模式：有 FAIL 时 exit 1（适合放进 CI/定时任务）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\capability-audit.ps1" -Strict
```

## 5. 自迭代协议（本 skill 如何持续升级）

**三层写入，不要混层：**

| 你发现了什么 | 写到哪里 | 形式 |
|---|---|---|
| 环境事实变化（版本/路径/阈值/新插件） | `references/00-baseline.md` | 事实表 + 复核命令 + 日期 |
| 新坑/新错误/新规避 | `references/70-playbook.md` | `ERR-YYYYMMDD-NN`：现象 / 根因 / 修法 / 是否已复现 |
| 新流程/新门禁/方法改进 | 对应 `references/` 下的 05/30/40/50/55/60/75/85 及 `scripts/`、`templates/` | 步骤 + 可执行命令 + 正反例 |
| 单次任务的经验/决策 | 工作区 `memory/*.md`（**不是**本 skill） | `LRN/ERR/ADR` 条目 |
| 用户偏好/交付习惯 | 工作区 `memory/user-profile.md` | 维度 + 来源 + 生效/过期 |
| 同类问题 ≥3 次 | 提升为 `memory/rules.md` 规则（≤120 字） | 规则编号 |

**更新检测与发布**：
- 用户侧：`scripts/skill-status.ps1` **商店优先**——读技能市场记录（`panel.json`/`installed.json`）的 `latestVersion` 与安装版本对比；`origin=manual` 时说明「上架后由商店接管」；源目录对比仅作开发对照。**不自动更新、不推送、不手工覆盖商店安装版**。
- 发布侧：`scripts/package-skill.ps1` 校验 frontmatter/version/CHANGELOG/敏感路径，生成 `manifest.json` + `SHA256SUMS.txt` + ZIP 与上架说明；发布前跑「正例 PASS / 反例 FAIL / 空跑不崩溃」+ `capability-audit.ps1 -Strict`，再 bump 版本。
- 上架侧：DSH 技能市场**不是发布端**（只做浏览/安装）。上架 = 用 `clawhub` CLI 发布到 ClawHub（`clawhub login` → `clawhub skill publish <技能目录> --slug ... --changelog ...`），SkillHub 同步后 DSH 市场即可搜索安装；完整命令、证据与未实测项见 `references/95-store-publish.md`。
- 健康漂移：`capability-audit.ps1` 每次把指标快照写到 `<工作区>\.tmp\capability-loop\audit-state.json`，下次自动对比（skills 增减、catalog 字符、索引大小、桌面壳补丁、检索开关、Trae 可用性、会话数）。

**版本规则（semver）：**
- `PATCH`：修错别字、补证据、在既有脚本内修正或收紧校验（`package-skill` 可对不合格包 FAIL；`loop-gate`/`capability-audit`/`skill-status`/`visual-qa-check` 退出码语义不变）。
- `MINOR`：新增 references 章节、新增脚本、新增模板（向后兼容）。
- `MAJOR`：改 `name`、改触发边界、改门禁口径/退出码语义、删除已有 references 章节（会导致触发或流程不兼容）。
- 每次 bump 在 `CHANGELOG.md` 写：日期、版本、改了什么、为什么、验证方式、回滚方式。

**回归要求（脚本改动 Before→After 都要跑）：**
1. 正例：一个真实/夹具任务目录，`loop-gate.ps1` 应 PASS；
2. 反例：故意缺产物/缺证据的目录，应 FAIL 并列出缺口；
3. 无工作区资产时：应 SKIP 而不是崩溃（幂等、可空跑）。

**健康度指标（每次体检报告尾部输出，用于判断闭环是否真在起作用）：**
catalog 描述总字符数（源环境：磁盘 description 合计 6,419 → 3,673，−43%；按 catalog 注入估算 14,950 字符/21 条 → 约 6k 字符/12 条）· 死重量 skill 数（目标 0）· `session_search` 可用（索引存在且 >100MB）· 门禁通过率 · 本 skill 的 retro 条目数 / 月 · 误触发次数 · **漂移告警数**（与上次体检对比）· **用户返工/纠正次数**（`85-ux-memory.md`，趋势向下）。

**拆分规则**：`SKILL.md` 正文 **< 300 行**；任一 reference **≤ 200 行**；超了就拆文件并在 §7 地图登记；拆完后 `name` 不变。

**周期维护**：每次任务后 10 分钟 retro（`templates/retro.md`）→ 每月一次全量体检 + 版本盘点 → 淘汰连续 3 次未被引用的规则/章节。

## 6. 交付与迁移

- 迁移给同事：交付**基线包**（文档 01–07 + `upgrade/` + `standards/` + `tools/` + 示例项目 + `AGENTS.md`/`memory` 模板），按「先读权限声明 → 再读执行手册」；脚本自动备份，出问题 `rollback.ps1`。
- 本 skill 自身的分发：**上架商店**优先（`clawhub skill publish` → SkillHub 同步 → 用户在技能市场一键安装/更新/回滚，见 `references/95-store-publish.md`）；对方也可把本目录原样拷到 `~/.dsh/skills/dsh-capability-loop/`，之后可自由改，**不回报、不锁定**。
- 版本对照：对方 `version.json` 与你不同不是问题；用 `CHANGELOG.md` 做差异说明，不做自动合并。

## 7. 参考文件地图

| 文件 | 解决什么 |
|---|---|
| `QUICKSTART.md` | 首次使用手册：3 条命令、怎么开口、出问题看哪里 |
| `README.md` | 商店/人读概览：能力边界、安装方式、脚本表、版本与更新、安全边界 |
| `references/05-intake.md` | 项目接入：≤6 问、真相源、目标与验收、专家/角色编排 |
| `references/00-baseline.md` | 环境事实基线（路径/阈值/资产/版本）+ 复核命令 |
| `references/10-audit.md` | 审计口径：九组指标、阈值、漂移、报告结构、只读纪律 |
| `references/20-runtime-fix.md` | P0 修复：检索重建、桌面壳稳定性、插件/技能清理、Token 收敛、回滚 |
| `references/30-requirement.md` | 需求：系统证据驱动、L0 权威入口、SRS 结构、≥80 质量门、三遍评审 |
| `references/40-testing.md` | 测试：oracle 问题、业务规则台账 A/B/C、三类 oracle、追溯门禁、事故闭环 |
| `references/50-design-team.md` | 设计：`ui-design-production` 八步、rubric V1–V12、视觉 QA、团队角色/评审门 |
| `references/55-design-intake.md` | 设计前置：动态判断现有主题/组件库/状态/样本页，产出 `design-context.md` 后才出稿 |
| `references/60-handoff.md` | DSH↔Trae：四件套、四脚本、prepare/deliver 门禁、**设计驱动开发**、实现者契约 |
| `references/70-playbook.md` | 失败手册：PS5.1/BOM/反引号/crashpad/索引/端口/编码/多帧 zstd/MCP 等 |
| `references/75-grill.md` | 自对抗评审：`grill-me` 接线 + 设计/需求/测试**三域**攻击清单、退出条件、反形式化 |
| `references/80-evolution.md` | 自迭代协议：分层、版本、回归、商店更新与发布、漂移、月度维护 |
| `references/85-ux-memory.md` | 用户偏好记忆与体验进化：记什么/怎么采集/怎么应用/度量 |
| `references/90-provenance.md` | 来源追溯：两个源会话的产出、验证证据、已知限制、能力对照 |
| `references/95-store-publish.md` | 上架商店实操：ClawHub 发布 → SkillHub 同步 → DSH 市场安装；命令、证据、未实测项 |
| `scripts/capability-audit.ps1` | 九组只读体检 + 与上次的漂移对比 + 版本/更新检查（`-Strict` 可作门禁） |
| `scripts/loop-gate.ps1` | 聚合门禁：design（含 design-context 硬门）/requirement/test + 环境验收 + `-RequireGrill` |
| `scripts/product-context.ps1` | 扫描工程产出「产品/设计上下文线索」（框架/组件库/主题/规模），供设计前置 |
| `scripts/trae-status.ps1` | Trae 安装/进程/**当前打开工程是否=目标**/交接包进度（只读；`-RequireMatch` 硬门） |
| `scripts/skill-status.ps1` | 商店优先的版本检查（读市场记录 + 源目录回退；不自动更新） |
| `scripts/visual-qa-check.ps1` | 浏览器视觉验收探测：A 路径可用性 + 权限受限时显式提示 A/B/C（exit 0/2） |
| `scripts/handoff-smoke.ps1` | 交接链路冒烟（临时工程：建包/门禁/取证/唤起解析/工程匹配） |
| `scripts/module-preflight.py` | 交接前置：模块/路由预检（已存在则必须先确认，防重复开发/路由冲突） |
| `scripts/handoff-audit.py` | 交接包体检：包完整性 / 材料可达性 / 证据对账 / 批次划分 / 设计依据 / **API 网关前缀一致性**（0/1/3/2） |
| `scripts/package-skill.ps1` | 上架包生成（校验 + manifest + SHA256 + ZIP + 上架说明） |
| `templates/project-profile.md` | 项目画像模板（接入产出） |
| `templates/intake-questions.md` | 接入六问可直接粘贴版 + 追问规则 + 默认/降级 |
| `templates/design-context.md` | 设计上下文模板（出稿前必填） |
| `templates/design-driven-acceptance.md` | UI 类交接的视觉验收追加段 |
| `templates/design-handoff-smoke.md` | 真实工程设计驱动交接实测清单（明日用） |
| `templates/grill-design.md` / `grill-requirement.md` / `grill-testing.md` | 三域 grill 记录模板 |
| `templates/grill-checklist.md` | 通用 grill 记录模板（兼容旧用法） |
| `templates/retro.md` | 任务后复盘模板（结论/证据/写回/用户反馈/待办） |

## 8. 与其它 skill 的关系

- `ui-design-production`：设计任务**必须**加载；本 skill 只负责路由、设计前置（`55`）与评审门（`50`）。
- `feature-handoff`：交接任务**必须**加载；本 skill 只负责串起「需求/测试证据 → 设计驱动交接 → 验收」的闭环（`60`）。
- `grill-me`：三域（设计界面+交互 / 需求分析 / 自动化测试）自对抗评审**优先加载**；用 `75-grill.md` 的域清单组织问题，记录用对应模板；不在 catalog 时用清单自问并标注「未使用访谈式工具」。
- `energy-pm-framework`：能源行业需求先加载；本 skill 不复制其内容。
- `self-improvement` / `proactive-agent`：写 memory 的格式参考；本 skill 的写回目标是**自身版本化文件** + 工作区 `memory`，两者不混用。