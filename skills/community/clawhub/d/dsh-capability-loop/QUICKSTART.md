# QUICKSTART — 首次使用（10 分钟）

> 你刚装好这个 skill，想知道「它能替我做哪些事、第一次怎么开口、第一步跑什么」。本文件只讲上手；原理见 `SKILL.md`，方法细节见 `references/`。
> 全部命令在 Windows PowerShell 5.1 下执行；脚本只读或只写你的工作区，不会自动改 DSH 安装目录。

## 0. 先记住三件事

1. **这是一条闭环**：接入（问清项目）→ 体检（现状证据）→ 修复/升级（只动该动的）→ 串方法（需求/测试/设计/交接）→ 自对抗（grill）→ 门禁（验收 + 写回）。
2. **不猜业务**：它会把「项目是什么、真相源在哪、验收口径」一次问清（≤6 问），再安排对应专家/角色；不会直接开写。
3. **不谎报**：跑不了/测不了的写「未实测 + 补测方式」；不自动更新、不自动推送、不锁定你的修改。

## 1. 第一次运行（只读体检，2 分钟）

```powershell
$sk = "$env:USERPROFILE\.dsh\skills\dsh-capability-loop"
$ws = "C:\你的工作区"           # 有 AGENTS.md/memory/upgrade 的工作区；没有就填当前项目根

# 九组体检：运行时 / skills / 角色 / 插件·profile / 会话记忆 / 桌面壳 / 资产与门禁 / Trae·版本 / 漂移
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\capability-audit.ps1" -Workspace $ws
```

看输出最后一行 `汇总：PASS=… WARN=… FAIL=…`：
- 有 `FAIL`：按报告里的 `references/20-runtime-fix.md` 对应小节处理；
- 只有 `WARN`：先看 `references/70-playbook.md` 是否已有现成规避；
- 报告默认写到 `<ws>\.tmp\capability-audit-<时间>.md`，可直接转给同事或贴进复盘。

## 2. 接入你的项目（3 分钟，必做一次）

对 DSH 说一句类似：

> 「用 dsh-capability-loop 接入 <项目名>：这是 <行业> 的 <系统>，用户是 <角色>，现在要 <目标>。」

它会先问你 ≤6 个问题（项目/角色/阶段、行业与合规、真相源、目标与验收、技术栈与设计体系、交付形态），产出 `project-profile.md`，并安排专家：
- 能源（燃气/电网/碳/VPP/电价/标书）→ 叠加 `energy-pm-framework`；
- 需求评审 → 需求评审员；设计 → Designer + Reviewer；测试 → QA；实现 → Trae（只写代码）。

若你不想被问，也可以一次性给全：

```text
项目：<名>｜行业：<燃气/电网/…>｜用户：<角色>｜阶段：0-1 / 改版 / 维护
真相源：运行地址 <url>、仓库 <path>、接口 <path>、数据 <path/DB>
目标与验收：<一句话目标>；验收标准：<可量化>
技术栈/设计体系：<Vue+ant-design-vue / Figma / 无>
交付：需求 / 设计稿 / 原型 / 测试 / 交给 Trae 实现
```

## 3. 典型任务怎么开口

| 你要的 | 直接说 | 会发生什么 |
|---|---|---|
| 摸清现有系统与设计体系 | 「先做产品上下文：扫描 <仓库/前端地址>」 | 跑 `product-context.ps1`，产出技术栈/组件库/主题/页面接口规模 + 待人工确认项 |
| 出/改页面 | 「按生产级设计改 <页面>」 | 先出 `design-context.md`（现有主题/组件库/密度/状态），再出稿；非实现者评审 + 视觉 QA；缺证据标「未实测」 |
| 写需求/SRS | 「做 <模块> 需求评审」 | 四源证据（系统/代码/接口/数据）→ 标准 SRS → ≥80 质量门 → 三遍评审 |
| 自动化测试 | 「给 <模块> 做回归」 | 先建业务规则台账（A/B/C），用例绑 R-ID，双门禁通过才敢说 PASS |
| 交给 Trae 写 | 「交接给 Trae：<功能>」 | 生成 `docs/handoff/<slug>/` 四件套，唤起 Trae，回读 diff/测试，DSH 出验收结论 |
| 交付文档集 | 「出总览」 | 生成单文件 HTML（搜索/目录/明暗双主题/打印/设计稿预览） |

## 4. 任务完成前：一条命令验收

```powershell
# 自动识别 design / requirement / test 并聚合；有 FAIL 返回 1
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\loop-gate.ps1" -TaskDir "<任务目录>"

# 升级 DSH 后：环境验收
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\loop-gate.ps1" -Environment

# 交接状态（Trae 装没装、当前打开工程是否=目标、包到哪一步）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\trae-status.ps1" -Workspace "<工程根>"
# 交接前硬门：工程不匹配 → exit 1（防改错项目）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\trae-status.ps1" -Workspace "<工程根>" -RequireMatch

# 视觉验收能力探测（0=A 路径可用；2=权限受限 → 必须让你选 A/B/C，不得静默跳过）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\visual-qa-check.ps1" -OutDir "<工作区>\.tmp\visual-qa"

# 交接链路冒烟（临时工程，不碰真实项目）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\handoff-smoke.ps1" -Workspace "<工作区>"

# 交接前模块/路由预检（0=可新建；1=已存在，必须先与开发者确认复用/改造/另建；3=有相似线索）
python "$sk\scripts\module-preflight.py" --project "<工程根>" --keyword "<中文模块名>" --alias resourceDemand

# 自动填指令（可选；脚本在 feature-handoff skill，不在本目录）：见 references/60-handoff.md 步骤 5
#   send-to-trae-prompt.ps1（Click/CDP 模式，默认只填不发）、trae-cdp.mjs（--remote-debugging-port=9333）

# 上架技能商店前打包（校验 + manifest + SHA256 + zip）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\package-skill.ps1" -Handle "<store-handle>" -Slug "dsh-capability-loop"

# 本 skill 有没有新版本（商店优先；只提示，不自动更新）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\skill-status.ps1" -Workspace "<工作区>"
```

## 4.1 上架技能商店后怎么更新

- 安装/更新/回滚都在**技能市场 UI** 完成；本 skill 不自动更新、不手工覆盖商店安装版。
- `skill-status.ps1` 会读市场记录（`panel.json` 的 `latestVersion`）：`origin=market` 且商店版本更新 → 提示去商店点更新；`origin=manual` → 说明「上架后由商店接管」。
- 发布前跑 `package-skill.ps1`：校验 frontmatter/version/CHANGELOG，输出 `manifest.json` + `SHA256SUMS.txt` + ZIP + `PUBLISH-NOTES.md`；上架目录名由商店决定（通常是 `<handle>--<slug>`），`SKILL.md` 的 `name` 不变。

## 4.2 怎么上架（开发者）

DSH 技能市场只负责安装，**不是发布端**。上架路径：**ClawHub 发布 → SkillHub 同步 → DSH 市场可装**。

```powershell
npm.cmd i -g clawhub          # Node 22.13+/24
clawhub login
cd "<工作区>"
clawhub skill publish "tools\capability-loop\skill\dsh-capability-loop" --slug "dsh-capability-loop" --name "dsh-capability-loop" --changelog "vX.Y.Z: 变更摘要"
```

首次授权、同步时延、未实测项、回滚方式见 `references/95-store-publish.md`。人读概览见 `README.md`。

## 5. 它会主动做、也会主动拒绝的事

**主动做**：问清项目再动手；检查现有设计体系再出稿；交付前自对抗（grill，可按域记录）；出 HTML 总览；把经验写回 `references/`/`CHANGELOG`/`memory`；检测版本漂移并提示；交接前校验工程匹配；上架前生成可校验发布包。

**主动拒绝**：替 Trae 写实现代码；把「没跑」写成「通过」；在普通沙箱谎报浏览器实测（全权限/用户截图可做，实测见 `50-design-team.md`）；强制覆盖 DSH 升级后的桌面壳补丁；自动更新/推送/锁定你的修改；在工程不匹配时让 Trae 动手。

## 6. 出问题先看哪里

| 现象 | 先看 |
|---|---|
| 体检 FAIL / 检索不可用 / 任务已停止 | `references/20-runtime-fix.md` |
| 脚本报语法/编码/BOM/中文乱码 | `references/70-playbook.md` A 节 |
| 需求文档被打低分 | `references/30-requirement.md` §3、§7 |
| 测试门一直 FAIL | `references/40-testing.md` §6（刻意拦截，不是 bug） |
| 设计没法定稿/评审不过 | `references/55-design-intake.md`、`50-design-team.md` |
| 浏览器截图不可用/权限不足 | 先跑 `scripts\visual-qa-check.ps1`：exit 2 会**明确提示**你选 A（切全权限）/ B（你截图）/ C（标未实测）；见 `50-design-team.md §3` |
| Trae 没反应/包卡住 | `references/60-handoff.md`、`trae-status.ps1` |
| 想让它更懂你的偏好 | `references/85-ux-memory.md` |
| 想升级 skill 自身 | `references/80-evolution.md` + `skill-status.ps1` |
