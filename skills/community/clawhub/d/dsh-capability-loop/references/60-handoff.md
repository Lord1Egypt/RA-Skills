# 60 · DSH↔Trae 分工交接（feature-handoff 串联）

> 目标：**DSH 只出需求/设计/接口/验收，Trae 只写代码**；靠工程内文件交接，不靠口头。
> 实现：skill `feature-handoff`（已安装 `~/.dsh/skills/feature-handoff/`，源 `<ws>/tools/trae-handoff/`）。
> 本文件说明「在能力闭环里怎么用」，不复制其模板正文。

## 1. 角色契约（不可互换）

| 角色 | 写什么 | 禁止 |
|---|---|---|
| DSH | 需求、设计规格、接口/数据契约、任务拆解、验收用例、验收结论 | 不替 Trae 写实现代码（除非用户明确要求） |
| Trae | 按 `tasks.md` 改代码、补最小必要测试、交证据 | 不改需求/接口契约、不扩范围、**不给自己判 PASS** |
| 人工/Lead | 冲突裁决、范围变更确认 | — |

判定：**任何 PASS 必须由没写这段代码的一方给出**；Trae 自评只能是 `待验收`。

## 2. 七步流程

1. **定位工程**：确认目标仓库根 `$ws`（必须与 Trae 打开的目录一致）；先跑 `scripts/trae-status.ps1 -Workspace $ws -RequireMatch`——必须 `MATCH` 才能继续（防改错项目）；不匹配就先 `open-in-trae.ps1 -Workspace $ws` 切过去再确认。

1.5. **模块/路由预检（新增，必做）**：`python ~/.dsh/skills/dsh-capability-loop/scripts/module-preflight.py --project $ws --keyword "<中文模块名>" --alias <英文别名...> [--menu-dump <菜单导出.json>]`
   - `0 = NONE`：无同名模块 → **默认新建路由**，在 `brief.md` 写「新建 + 路由建议」；
   - `1 = EXISTS`：已存在同名模块 → **停下与开发者确认**「复用 / 改造 / 另建」，结论写入 `brief.md` 与 `tasks.md` 的「禁止变更」；未确认不得进入实现；
   - `3 = WEAK`：存在相似模块或路由线索 → 先确认能否复用，避免重复建设。
   - 实测反例：`--keyword 资源需求` 在 `rmp-frontend` 命中 `views/resourceDemand` → EXISTS，避免把已有月度页当新模块重写。

1.6. **材料随行（必做，防「实现者读不到设计稿」）**：设计稿/页面规格/接口文档若不在目标工程内（例如在文档工作区、另一个盘符），**先拷到** `docs/handoff/<slug>/materials/`，`brief.md`/`tasks.md`/`PROMPT.md` 一律用**工程内相对路径**引用。
   - 为什么：实现者（Trae）只能读打开的那个工程目录；工程外路径对它等于没给 → 只能按文字猜，复刻必然偏。
   - 最小集合：设计规范/token、真实系统样本页截图、接口契约、页面规格、交互细节。HTML 设计稿可只拷必要的几份。

1.7. **批次划分（必做，防上下文压缩后偏移）**：`tasks.md` 必须有「## 批次」段，**一批 ≤ 3 个任务、≤ 8 个文件、≤ 1 个页面/模块**；每批开工前生成 `PROMPT.md` 写明「本批次 = 哪几个 T-xx」，实现者只做本批，上一批「待验收」通过后再开下一批。
   - 为什么：十几条任务 + 几十 KB tasks.md 一起给，实现者上下文会被压缩，压缩后最容易丢的就是「禁止项」和「不要动清单外文件」。

1.8. **交接包体检（必做，门禁）**：

```powershell
python "$env:USERPROFILE\.dsh\skills\dsh-capability-loop\scripts\handoff-audit.py" --workspace "<工程根>" --slug <slug>
```
   - 查六组：A 包完整性、B 材料是否都在工程内可读、C `acceptance`/`record` 引用的证据是否真的存在于 `evidence/`、D 有没有批次段且 PROMPT 指明本批（每批 ≤3 任务）、E 有没有设计依据/`design-context`、F 契约里的 API 路径是否都带工程既有网关前缀（且无「不要写 /png 前缀」这类反向指令）。
   - 退出码：`0` 无 FAIL 且无 WARN → 可交；`3` 仅 WARN → 可交但要在 `record.md` 登记；`1` 有 FAIL → 先修再交；`2` 参数/路径错误。
   - 默认**只打印不写文件**（只读工具，不污染工程）；要留档就显式 `--out "<工作区>\.tmp\handoff-audit\<slug>.md"`，作为交接前证据。
1.9. **接口契约核对（必做，防「前缀漏写 → 404」）**：把 `tasks.md` 契约表里的 URL 与工程既有 API 常量对照——**网关前缀必须写全**（本项目既有常量形如 `/png/<服务>/<动作>`），host 不写、`/api` ≠ 网关前缀；同时核方法（GET/POST）、响应包装（`{code,msg,data}` 或裸 `data`）、错误码。
   - 真实事故（2026-11-13）：年度接口文档写 `Base /api/annualResourceDemand`、任务里还写「不要写 `/png` 前缀」→ 实现后联调 404；月度契约写了 `/png/monthlyResourceDemand/*` 才对。
   - 自动校验：`handoff-audit.py` **F 组**——从工程 `src/api/**`（含 `apps/*/src/api`）统计既有前缀集合，契约里出现的 API 路径首段必须命中；页面路由（`src/router/**` 的 path）自动排除；出现「不要/不写/不含/不需要写 … `/png` 前缀/硬编码」这类**反向指令**直接 FAIL（「不得漏写」属正向、豁免）。判定按**位置序**：去 `**`/反引号装饰、剥离不含 `/png` 的括号说明后，只按 `。；` 切句；**否定词必须出现在「`/png` … 前缀」之前**才算反向指令——因此「不写 host」「不含 `/api`」「网关前缀 `/png` 必写、host 不写」「不是同一前缀」都不会误报，而「不要写 `/api`、`/png` 前缀」「**不要**写 host，**也不要**写 `/api` 或 `/png` 前缀」都会 FAIL（「必写/必须/必含」的正向措辞不误报；`record.md` 里描述旧缺陷的历史行也不误报）。
   - `F-skip`：工程没有 `src/api`（纯文档/新项目）时本项不适用，按 OK 处理。

2. **建包**：`new-handoff.ps1 -Workspace $ws -Slug <kebab> -Title "<中文>"`（可加 `-WriteAgentsBlock` 把实现者契约写进工程 `AGENTS.md`，带幂等标记）。
3. **填四件套**：`brief.md`（背景/范围/引用）→ `tasks.md`（T-01 起任务、文件清单、**接口与数据契约**、禁止变更）→ `acceptance.md`（AC-001 起用例 + 证据列 + 置信度 A/B/C）→ 交接前门禁。
4. **过 prepare 门禁**：`check-handoff.ps1 -Stage prepare`（无 `{{占位符}}` 残留、无「待填」、任务行绑定 AC）。
5. **唤起 Trae**：`open-in-trae.ps1 -Workspace $ws -File docs/handoff/<slug>/tasks.md`；对话里显式引用一次实现者契约。
6. **回读取证**：`collect-evidence.ps1 -Workspace $ws -Slug <slug> -TestCommand "<命令>"` → `evidence/<时间戳>.md`（git 变更 + diff 摘要 + 测试输出；非 git 也会标注「diff 无法取证」）。
7. **填 record.md 结论 + deliver 门禁**：`check-handoff.ps1 -Stage deliver`（要求结论为 `PASS|FAIL|未实测`）。

## 3. 实现者契约（Trae 侧硬约束，已内置在 tasks.md 顶部）

- 只改任务清单列出的文件；要动清单外文件 → 停下提问；
- 接口/字段/错误码以「接口与数据契约」为准：不新增、不改名、不扩字段；
- 不改需求/验收标准；不删既有测试或断言来「变绿」；
- 完成后在「实现回报」填证据并标 `待验收`，**不得自判 PASS**；spec 缺口 → 停下提问，不自造。

三种落位：① `tasks.md` 顶部（主路径，100% 生效）；② 目标工程 `AGENTS.md` 标记区块（`-WriteAgentsBlock`）；③ `.github/instructions/*.instructions.md`（VS Code 系，未实测）。

## 4. 能力闭环中的接线

```
需求（30）产出可验收 AC/规则 R-ID
  → 交接包 acceptance.md 直接引用 AC/R-ID（不另写一套）
  → Trae 实现、交实现回报（待验收）
  → collect-evidence 取证
  → QA/测试（40）按 R-ID 跑追溯门
  → DSH 填 record.md 结论
  → check-handoff -Stage deliver + gate-check
  → Lead 终门 → 只有这时才允许说「完成」
```

## 5. 设计驱动开发（UI 类交接必须加这一层）

只给「功能任务清单」不够，Trae 会自己发明样式。UI 类交接包必须补充：
1. `design-context.md`（现有框架/组件库/token/状态，来自 `55-design-intake.md`）放进交接包或工程 `docs/design/`；
2. `tasks.md` 里每条 UI 任务绑定**设计依据**：页面/组件名 + token（间距/字号/色值）+ 复用组件 + 禁止自造项；
3. `acceptance.md` 增加**视觉 AC**：375/768/1440 三档截图、空/错误/加载态、暗色（如适用）、对比度与触控尺寸；证据列要求截图路径；
4. 禁止清单加一条：**不得引入新的 UI 框架/组件库/图标库/主题体系**；确需引入 → 停下提问；
5. DSH 验收时按 `design-review-rubric.md` 复核截图，`record.md` 写视觉结论（无截图 = 未实测）。
6. 现成模板：`templates/design-driven-acceptance.md`（视觉 AC 六条 + 判定口径，直接追加到 `acceptance.md`）。

> 能力闭环接线：`55-design-intake`（判断现状）→ `ui-design-production`（出稿）→ `feature-handoff`（设计驱动交接）→ `collect-evidence`（截图/测试）→ `record.md`（DSH 结论）。

**真实工程实测（明日清单）**：`templates/design-handoff-smoke.md` 给出「准备 → 交接前 → Trae 实现 → 回读验收 → 结论回写」全流程与判定标准；先跑 `scripts/handoff-smoke.ps1` 确认链路连通（临时工程，不碰真实项目），再按清单上真实工程。完成后把 `90-provenance.md §3` 的「未实测」改为「已实测（日期/工程/commit）」。

## 5.1 设计前置的可执行要求（系统已有 → 遵循；新项目 → 才做新设计）

判定顺序（**不许跳步**）：

1. **先判性质**：目标工程/模块是否已有可运行 UI 与设计体系（`product-context.ps1` + 真实系统截图）。
2. **已有系统**：必须产出 `design-context.md`（真实 token 值/组件库/状态/样本页），设计稿与 `tasks.md` 的「设计依据」指向它；**禁止自造色板/字号/间距/圆角/表格风格**；差异处必须写「为什么不用现有方案」。
3. **新项目/无既有体系**：可以做新设计，但先把选定的 token 固化成 `design-context.md`，后续任务以它为准。
4. **门禁**：`loop-gate.ps1 -Kind design`（缺 `design-context*.md` → FAIL）；交接侧由 `handoff-audit.py` 的 E 组检查（brief 有无设计依据、包内有无 `design-context*.md`、每个任务有无「设计依据」）。
5. **反例**（本项目实测）：设计稿 10:58 先出、设计规范 11:04 才反向补，且没有 `design-context.md` → 实现阶段只能按文字猜，风格一致性无法验收。

## 6. 本机事实与已知未实测

- Trae CN `3.4.18`（VS Code `1.107.1` 内核），装在 `D:\Trae CN`；CLI `D:\Trae CN\bin\trae-cn.cmd` 支持 `-r/--reuse-window`、`-g/--goto <file:line>`、`-a/--add`。
- Trae 的 `~/.trae-cn/skills` 由 marketplace 管理（`skill-config.json` 的 `managedSkills`）；手工安装可选、带备份、可 `-Uninstall` 回滚；主路径仍是工程内交接包。
- **未实测（已在文档标注）**：① Trae SOLO 是否真读 `AGENTS.md`/instructions（兜底：把契约直接贴进对话）；② Trae 技能面板是否显示手工装 skill（不显示就删目录，不影响闭环）；③ 窗口是否精确跳到文件行（CLI 返回 0，未目视核对）。
- 回滚：删 `~/.dsh/skills/feature-handoff`、`install-trae-skill.ps1 -Uninstall`、删工程 `docs/handoff/<slug>/` 与 AGENTS.md 标记区块。

## 7. 分工的边界（常被问）

- 不做 MCP 桥（`dsh --profile headless` 需 API key，本机 `~/.dsh/.env` 缺失；成本高收益低）；不做 ACP 直连（Trae 不是 ACP 客户端）。
- 不把 Trae 加进 `open-in-app` 白名单（桌面壳升级会覆盖，收益不如文档契约）。
- **真正约束角色的不是「关联」，而是规则文件 + 评审门 + 可执行门禁。**

> 以下 v2.4.0–v2.7.0 条目对应的脚本都在 `feature-handoff/scripts/`（本 skill 只记接线，不复制脚本）。

- **自动填指令（v2.4.0）**：`feature-handoff/scripts/send-to-trae-prompt.ps1 -Workspace $ws -PromptFile docs/handoff/<slug>/PROMPT.md -ChatChord "^u"`：激活 Trae → 打开对话（本机实测 `Ctrl+U`）→ 粘贴 PROMPT → 不发送，开发者在 Trae 按 Enter 确认开工。与 `open-in-trae.ps1` 串联即「打开 + 填指令全自动，人只确认」。

- **Token 策略（v2.4.1）**：`send-to-trae-prompt.ps1` 默认**指针模式**（只发一行“按 PROMPT.md 执行 + 必读文件 + 禁止改契约 + 回填 record”），`-Inline` 才全文粘贴。理由：契约本就在文件里，粘贴全文会让对话历史重复计费；整份 tasks.md（50KB+）更不应贴进对话。

- **Click 模式（v2.5.0）**：`send-to-trae-prompt.ps1` 默认 `-Mode Click`：GetWindowRect + 相对坐标点击输入框（0.861/0.90）→ 粘贴 → 前后截图哈希校验 → 不发送。**禁止 `^A`/`^S` 盲发**（历史事故：Trae 的 Ctrl+U 不聚焦输入框，^A 落进编辑器覆盖了 tasks.md，已 Ctrl+Z 恢复）。

- **Click 模式限制（v2.5.1）**：坐标依赖「对话面板打开且布局固定」；实测面板关闭时点击落入终端（粘贴文本 + `^Z/^U` 字面写入）。必须先 `-VerifyOnly` 截图确认目标是对话面板；布局不明时禁用 Hotkey 模式。

- **面板检测 + 自动开启（v2.6.0）**：先检测发送按钮绿色像素判定对话面板是否打开；未打开则点编辑器并发送 `-ChatChord` 后复检；仍失败 `exit 3` 不盲发。实测本机 `Ctrl+U`/`Ctrl+Alt+B` 均未打开面板（检测 green=0→10，未达阈值 20），该分支待配置真实入口或用 CDP。

- **v2.6.1 校准**：发送键探针比例改为 `(0.964, 0.934)`（旧值偏差致误判）；实测打开时 green=132、关闭时 0；`Ctrl+U` 仅在编辑器聚焦时生效，脚本先点编辑器再发键；完整链路（检测→粘贴→哈希校验）已 PASS。

- **CDP 模式（v2.7.0，推荐）**：`-Mode Cdp [-Restart] [-Clear] [-AutoSend]`。`--remote-debugging-port=9333` → `/json/list` 找 workbench → 打分选 `DIV.chat-input-v2-input-box-editable` → 真实点击聚焦 → `Input.insertText` 写入 → 读回 `len/head` 校验；清空用 `Ctrl+A`+`Backspace`。实测 len=159 指针提示词写入成功、未发送；找不到输入框 exit 3，端口未开 exit 4。