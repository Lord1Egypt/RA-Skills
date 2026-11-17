# dsh-capability-loop — DSH 能力升级与治理闭环

> 把「DSH 自身升级治理」与「在这台 DSH 上做项目（接入 / 需求 / 设计 / 测试 / 交接 / 验收）」串成一条**可重复、可度量、可回滚**的闭环。
> 它不是一个「帮你写代码」的 skill，而是一个**先取证、再动手、最后过门禁**的治理型 skill。

## 这个 skill 解决什么问题

| 你遇到的 | 它会做 |
|---|---|
| DSH 越装越慢、skill 互相抢触发、Token 变贵 | 九组只读体检 + 与上次快照的漂移对比，指出该删/该修的具体项（带 `文件:行号`） |
| 会话检索失效、进程反复退出、3080 端口冲突 | 按 `references/20-runtime-fix.md` 走可回滚修复（先 DryRun，再 apply，再 verify） |
| 新项目上来就开写，最后返工 | 先问清 ≤6 个问题（项目/角色/真相源/目标/技术栈/交付），产出 `project-profile.md` |
| 需求/设计/测试/交接各做各的，互相不认账 | 统一到同一条证据链：需求四源对账 → 设计先读现有体系 → 测试建业务规则台账 → 交接走四件套 |
| 「感觉没问题」就交付 | 交付前 grill 自对抗（设计/需求/测试三域），门禁 `loop-gate.ps1` 不过不算完成 |
| 想把它交给同事 / 上架技能商店 | 生成可校验发布包（manifest + SHA256 + ZIP），并给出真实上架路径（见 `references/95-store-publish.md`） |

**不适用**：单点需求评审、单页面 UI 设计、单次自动化测试、单次交给 Trae 实现——这些直接走各自 skill/规范，不需要本 skill。

## 安装

### 方式 A：从 DSH 技能市场安装（上架后）

1. 打开左侧 **Skill Market** 面板，搜索 `dsh-capability-loop`；
2. 点安装 → **重启 DeepSeek Harness**（技能目录在会话开始时确定，新装 skill 在新会话里才能调用）；
3. 安装目录为 `~/.dsh/skills/<handle>--dsh-capability-loop/`，之后**更新/回滚都在市场 UI 完成**。

### 方式 B：手工安装（本机/内网）

```powershell
# 把整个目录拷到 DSH 技能根目录，目录名建议保持 dsh-capability-loop
Copy-Item -Recurse -Force .\dsh-capability-loop "$env:USERPROFILE\.dsh\skills\dsh-capability-loop"
# 重启 DeepSeek Harness
```

> 技能目录里必须有 `SKILL.md`（带 `name` / `description` frontmatter），否则不会出现在技能列表。
> 上架/发布流程见 [`references/95-store-publish.md`](references/95-store-publish.md)。

## 快速开始（10 分钟）

首次使用先读 [`QUICKSTART.md`](QUICKSTART.md)。最小三步：

```powershell
$sk = "$env:USERPROFILE\.dsh\skills\dsh-capability-loop"
$ws = "C:\你的工作区"     # 有 AGENTS.md / memory / upgrade 的工作区；没有就填项目根

# 1) 只读体检（2 分钟）：九组指标 + 与上次的漂移
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\capability-audit.ps1" -Workspace $ws

# 2) 任务完成前的聚合门禁（design / requirement / test 自动识别）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\loop-gate.ps1" -TaskDir "<任务目录>"

# 3) 本 skill 有没有新版本（商店优先；只提示，不自动更新）
powershell -NoProfile -ExecutionPolicy Bypass -File "$sk\scripts\skill-status.ps1" -Workspace $ws
```

怎么开口：`「用 dsh-capability-loop 接入 <项目>：这是 <行业> 的 <系统>，目标 <目标>」`。

## 七阶段闭环

`INTAKE 接入 → AUDIT 体检 → FIX 修复 → WIRE 串接（需求/测试/设计/交接） → HANDOFF 交 Trae → GRILL 自对抗 → GATE 门禁验收`

顺序纪律：**INTAKE 未清不动工；AUDIT 未出证据不做 FIX；FIX 未验证不 WIRE；GRILL 未做不宣称完成；GATE 未过不宣称完成。**

## 目录结构

```text
dsh-capability-loop/
├─ SKILL.md            # 路由与纪律（Agent 加载入口）
├─ QUICKSTART.md       # 首次使用手册（10 分钟）
├─ README.md           # 本文件：商店详情页/人读概览
├─ CHANGELOG.md        # 版本变更、验证方式、回滚方法
├─ version.json        # 版本、商店元数据、脚本/引用清单
├─ references/         # 深文档：体检/修复/需求/测试/设计/交接/grill/进化/来源
├─ scripts/            # 可执行检查（只读为主，输出到 .tmp）
└─ templates/          # 填空模板（项目画像/设计上下文/grill/复盘）
```

## 脚本一览

| 脚本 | 用途 | 退出码 |
|---|---|---|
| `capability-audit.ps1` | 九组只读体检 + 漂移对比；`-Strict` 作 CI 门禁 | 0 / 1（有 FAIL） |
| `loop-gate.ps1` | 聚合门禁：design（含 design-context 硬门）/ requirement / test / `-Environment` | 0 / 1 |
| `product-context.ps1` | 扫描工程，输出框架/组件库/主题/规模线索 | 0 |
| `trae-status.ps1` | Trae 安装/进程/当前工程匹配/交接包进度；`-RequireMatch` 硬门 | 0 / 1 |
| `visual-qa-check.ps1` | 视觉验收能力探测；权限受限时显式提示 A/B/C | 0 / 2 / 1 |
| `handoff-smoke.ps1` | 交接链路冒烟（临时工程，不碰真实项目） | 0 / 1 |
| `module-preflight.py` | 交接前模块/路由预检：已存在同名模块必须先确认（Python3） | 0 / 1 / 3（参数错误 2） |
| `handoff-audit.py` | 交接包体检：材料可达性 / 证据对账 / 批次 / 设计依据 / **API 网关前缀一致性**（Python3） | 0 / 1 / 3（参数错误 2） |
| `skill-status.ps1` | 商店优先的版本检查（只提示，不自动更新） | 0 / 1（`-Strict`） |
| `package-skill.ps1` | 生成可校验发布包（manifest + SHA256 + ZIP + 上架说明） | 0 / 1 / 2 |

> 通用约定：**参数/路径错误统一 `exit 2`**（上表只列业务退出码；以各脚本头注释为准）。
> `skill-status.ps1` 请**从安装版目录运行**（`~/.dsh/skills/dsh-capability-loop/scripts/`）；从源目录运行会变成「源 vs 源」自比自，脚本会打印提示。
> 交接自动化脚本（`send-to-trae-prompt.ps1`、`trae-cdp.mjs`）在 `feature-handoff` skill 内（**不在本目录**），接线见 `references/60-handoff.md`。

## 版本与更新

- **当前版本**：见 [`version.json`](version.json) 与 [`CHANGELOG.md`](CHANGELOG.md)。
- **更新由商店负责**：安装/更新/回滚在技能市场 UI 完成；本 skill **不后台下载、不自动覆盖、不推送**。
- **手工安装**：用 `skill-status.ps1` 看「源目录 vs 安装版」差异，只提示、不自动合并。
- **版本号三处一致**：`version.json`（权威）/ `CHANGELOG.md` 条目 / `SKILL.md` frontmatter `version`；frontmatter 缺失时市场「已安装版本」会显示为空（`package-skill.ps1` 会 WARN，不一致则 FAIL）。
- 版本语义：`PATCH` 修错/补证据/在既有脚本内收紧校验（不改门禁脚本退出码语义）；`MINOR` 新增章节/脚本/模板；`MAJOR` 改 name/触发边界/门禁退出码语义。

## 环境要求

- **Windows PowerShell 5.1**（脚本按 5.1 语法编写，含中文的 `.ps1` 为 UTF-8 带 BOM）；
- **Node.js 22.13+ 或 24+**（可选：上架发布用的 `clawhub` CLI，其 `engines` 为 `^22.13.0 || >=24`；仓库内 `.mjs` 工具只需 22+；本 skill 的检查脚本以 PowerShell 为主）；
- **Python ≥ 3.11**（`scripts/module-preflight.py` 交接预检、`scripts/handoff-audit.py` 交接包体检必需；`tools/build-docs-html.py` 类文档工具另需 `markdown`）；
- **网络**：skill 运行本身不联网；上架/发布需要访问 ClawHub/SkillHub（见 `95-store-publish.md`）。

## 安全边界（它会主动拒绝的事）

- 不把「没跑」写成「通过」；不能实测的写「未实测 + 原因 + 补测方式」，**不得判 PASS**；
- 不在普通沙箱谎报浏览器实测（走 A/B/C 三路径，见 `references/50-design-team.md §3`）；
- 不自动更新、不后台推送、不覆盖商店安装版、不锁定使用者的修改权；
- 交接给 Trae 前必须工程匹配（`trae-status.ps1 -RequireMatch`），防止改错项目；
- 发布包由 `package-skill.ps1` 生成并校验，不手工拼包；上架前扫描本机路径/凭证。

## 许可证与来源

- 许可证：以发布时 `SKILL.md` frontmatter 的 `license` 字段为准（当前仓库未声明前，请勿假定可再分发）。
- 血缘：合并自两个 DSH 会话的能力沉淀，证据映射见 `references/90-provenance.md`。
- 本 skill 与 DeepSeek / Tencent SkillHub / OpenClaw ClawHub 均无隶属关系；商店只负责分发。