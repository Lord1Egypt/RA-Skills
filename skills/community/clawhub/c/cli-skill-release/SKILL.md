---
name: cli-skill-release
slug: cli-skill-release
displayName: CLI 技能发布工程（releaser.py 多能力 CLI + 脚手架 + CI + LICENSE + 上架 + 市场情报）
version: 1.9.6
author: 何巍
license: MIT-0
description: >
  Release engineering for zero-dependency Python CLI agent skills: releaser.py validates publish-readiness
  (a 0-100 score with real functional checks that actually boot your CLI), inventory/gap market intelligence,
  scaffold, CI, LICENSE(MIT-0), marketplace publish, readiness badge, and chain-propagation tooling.
  Pre-publish checklist, skill publish checklist, "is my skill ready to publish?", "what am I missing before
  I push this skill to GitHub?", audit skill against Agent Skills spec, fix LICENSE shows Other, pytest exit
  code 2, CI keeps failing, ClawHub/SkillHub/agentskills.io publish guide, skill discoverability, quality gate.
  把"以 Python CLI 形式交付的 WorkBuddy 技能做成可发布项目并上架"的全流程固化。
  核心是零依赖 releaser.py：validate 主动扫描发布陷阱并给 0-100 就绪分（含★功能级验证真跑 CLI）、
  inventory 治理本机技能、gap 市场缺口、selfcheck 零依赖、scaffold 起项目、bump 升版本、
  release 推送(需--push)/发布(需--publish)、badge 链回徽章（便于引用致谢）、promote 发布说明工具箱、
  diagnose 长尾诊断（症状→根因→修复）、preflight 市场定制上架清单。
  当用户说"构建/发布技能""技能上架""发布技能""publish skill""上架 skill""技能发布前检查清单"
  "校验技能能不能发""技能质量门禁""skill CI gate""LICENSE 显示 Other""CI 一直红""pytest exit code 2"
  "零依赖 Python 工具""技能搜不到"时触发。
  本技能是 skill-creator（写技能）的**发布阶段搭档**：它管"写好"，本技能管"发出去 + 懂市场 + 帮你被找到 + 链回致谢"。
description_zh: "零依赖 Python CLI 技能发布工程：releaser.py validate(就绪分)/diagnose(长尾诊断)/preflight(上架清单)/badge(链式徽章)/发布"
description_en: "Release engineering for zero-dependency Python CLI skills: validate(score)/diagnose/preflight/badge/publish. Pre-publish checklist, is my skill ready to publish, ClawHub publish guide, skill discoverability."
tags: [publish, skill-publishing, pre-publish-checklist, clawhub, agent-skills, quality-gate, ci, license, mit-0, zero-dependency, python, release]
keywords: cli, python, zero-dependency, skill, release, publish-skill, release-skill, publish, skill-release, skill-publishing, validate, skill-validation, readiness, quality-gate, ci-gate, badge, skill-badge, github-actions, ci, license, mit-0, pytest, scaffold, inventory, gap, diagnose, preflight, 发布, 上架, 发布技能, 校验技能, 技能门禁, 质量门禁, 排障, 市场情报, 长尾诊断, 上架清单
xiaping_trigger: ["技能", "发布", "CI", "工具", "工程", "上架", "脚手架", "校验", "市场缺口", "长尾", "诊断"]
xiaping_category: ["效率工具"]
xiaping_tags: ["技能开发", "发布工程", "GitHub", "CI", "Python"]
# 上架元数据（发布到各站时直接复制；categories 必须是 ClawHub 官方精确 slug，≤3 个）
clawhub_categories: development, automation, security
clawhub_topics: skill-publishing, release-engineering, quality-gate, ci-cd, secret-scan
github_topics: agent-skills, skill-publishing, release-engineering, quality-gate, ci-cd, python, mit-0
xiaping_eval_strategy: developer
metadata:
  slug: cli-skill-release
  displayName: CLI 技能发布工程（releaser.py 多能力 CLI + 脚手架 + CI + LICENSE + 上架 + 市场情报）
---

# CLI 技能发布工程

把"从零做一个零依赖 Python CLI，再打包成 WorkBuddy 技能并发布上线"的全流程固化下来。
**本技能的核心是一个真能跑的工具 `releaser.py`**（对标 find-skills++ 的能力矩阵）：
它不再只是"说明书"，而是**主动**帮你扫描陷阱、治理技能、评估市场、校验零依赖、一键起项目、升版本、推送上架。

> 设计哲学（参考 find-skills++）：**方法论落成可运行工具，散文降级为背景。**
> find-skills++ 用 AST 扫描 / 离线搜索 / 生命周期治理主动管理 agent 技能；
> 本工具用 `validate` / `inventory` / `gap` / `selfcheck` 主动管理"技能能否可靠发布 + 市场该造什么"。

> **🔒 安全与隐私声明（Security & Privacy）**
> 本工具是**纯本地、零依赖**的发布工程助手，**默认不做任何远程操作**：
> - 除你**显式传入 `--push`**（推送到 git 远端）或 `--publish`（通过你本机已登录的 clawhub CLI 发布）外，`release` 只做本地提交 + 打印人工导入步骤，**绝不静默触碰远端**。
> - **不读取、不传输任何凭据**：无 `--api-token` 之类凭据形参，不存储任何密钥，不会把 token / 密码发往任何服务器。
> - **★安全红线（凭据泄露硬闸门）**：`validate` / `gate` / `release` 在发布前**强制扫描全仓硬编码密码 / 授权码 / API Token**（`secretscan` 子命令可单独跑）；一旦命中即 FAIL 并**直接拒绝提交/推送/发布**，绝不让"不该进 GitHub 的东西"入库。环境变量引用（`os.environ.get(...)` / `${...}`）视为安全。
> - **无隐藏网络外联**：代码不含有 `urllib` / `requests` / `socket` 外联；文档里的 `api.github.com/.../license` 只是供你**自行核验** LICENSE 的公开查询地址，工具本身不调用。
> - **只读扫描**：`inventory` / `gap` / `curate` 仅**只读**扫描你本机已安装的技能目录，数据不出本机。
> - **账本本地化**：`registry` 账本只写入你 home 下的本地 `ledger.json`，不上传。
> - **无命令注入面**：所有 `subprocess` 调用均为显式参数列表（无 `shell=True`、无字符串拼接命令）。
> - **报告脱敏**：所有检出一律**脱敏后**输出（仅留前 4 + 后 2 字符），**绝不回显明文凭据**。

---

## 0. 何时用本技能（含与 skill-creator 的边界）

**用本技能，当：**
- 要**从零做 / 发布**一个以 Python CLI 形式交付的 WorkBuddy 技能（零依赖优先）。
- 想**主动查**一个技能"能不能发、差什么、得几分"：`python releaser.py validate --path <dir>`。
- 想**知道市场缺什么技能**：`python releaser.py gap`。
- 遇到：`pytest exit code 2`、CI 一直红但拿不到日志、`LICENSE` 显示 "Other"、上架被 `skill-card.md` 冲突或 Topics 超限卡住。

**不要用本技能，当：**
- 你只是想**写一个新技能的 SKILL.md 内容 / 设计触发描述**——那是 **skill-creator** 的职责（它管"写"，本技能管"发 + 懂市场"）。

| 维度 | skill-creator（内置·写） | cli-skill-release（本技能·发 + 情报） |
|---|---|---|
| 核心问题 | 怎么写好一个技能 | 怎么把 CLI 工具可靠地发到市场 + 该造什么 |
| 执行体 | `init_skill.py`（生成文档） | **`releaser.py`（19 个子命令，真能跑）** |
| 主动能力 | 无 | validate 扫陷阱+就绪分 / inventory 治理 / gap 市场情报 / selfcheck 查依赖 |
| CI / LICENSE / 上架 | 不涉及 | 模板 + 规则 + 排障 SOP + release 人工导入情报（见 §3） |

---

## 1. 核心工具：releaser.py 子命令总览

在 cli-skill-release 技能目录下运行（零依赖，仅标准库）：

| 子命令 | 作用 | 对标 find-skills++ |
|---|---|---|
| `scaffold <name>` | 一键生成带 CI 的完整可发布骨架 | — |
| `validate --path <dir>` | **主动扫描发布陷阱 + 输出 0-100 就绪分**（+ `--json` / `--bench` 对标 / `--rubric` 透明评分）+ **★功能级/可执行验证** + **★安全红线凭据扫描** | 安全扫描 + 引用完整性 + **功能验证（竞品无人做）** |
| `secretscan --path <dir>` | **★安全红线：专项扫描硬编码密码/授权码/API Token（独立于就绪分，供发布前单独把关）** | （独有：凭据泄露硬闸门） |
| `gate --path <dir> --min 90` | **CI 门禁**：就绪分低于阈值即非零退出（readiness-as-a-service） | （独有：质量闸门） |
| `inventory [--roots ...]` | **扫描本机已装技能，逐条报告能否发** | install / list 治理 |
| `gap [--roots ...]` | **市场情报：本机覆盖 + 组合缺口**（+ `--scan-json` 消费 find-skills++ 真实市场数据，交叉出"市场有/你缺"） | （独有：市场侧） |
| `selfcheck [--path .]` | 零依赖校验：扫 import 比对 `sys.stdlib_module_names` | — |
| `bump [--type patch]` | 升 SKILL.md 版本号 + 补 CHANGELOG | — |
| `release --path .` | git 推送(需 `--push`) + **clawhub 发布(需 `--publish`)（或构造 ClawHub 人工导入情报）** | — |
| `publish --github --clawhub` | **★多站上架编排：显式逐站授权上传 GitHub/ClawHub（安全闸门前置，默认不碰远程）** | （独有：多站分发） |
| `badge --path <dir>` | **★链回徽章：基于就绪分生成 readiness 徽章 SVG + 链回片段** | （独有：引用致谢） |
| `promote [--path <dir>]` | **★发布说明工具箱：徽章区+要点说明+社媒文案+链回玩法** | （独有：获客） |
| `diagnose --symptom "..."` | **★长尾诊断：症状→根因→修复（直接回答用户会搜的长尾问题）** | （独有：覆盖长尾搜索） |
| `preflight [--market clawhub]` | **★市场定制上架前检查清单（回答"发布前检查清单"类搜索）** | （独有：清单即内容） |
| `registry [list\|show\|add]` | **★状态层：已发布技能账本（release 成功自动登记）** | （独有：治理状态） |
| `recheck [<slug>]` | **★生命周期：再校验已发布技能，报告漂移/弃用** | （独有：持续治理） |
| `selfdemo` | **★自证底座：全量自证（主张即演示，对标 smoke.py）** | （独有：信任底座） |
| `curate [--roots ...]` | **★供给侧策展：主动告诉生态该造什么（升级版 gap）** | （独有：主动分发） |
| `doctor [--path <dir>]` | 自检本工具；或对目标目录跑 validate | 自检门 |

> **差异化定位**：竞品（含 skill-creator）只给"文档"，你照着做；本工具**替你执行校验/治理/脚手架/推送，并用 `gap` 告诉你市场该造什么**——这是 find-skills++ 之外的空白赛道。

---

## 2. 各子命令用法（带示例）

### 2.1 validate —— ★杀手锏：主动扫描 + 0-100 就绪分 + ★功能验证
```bash
python releaser.py validate --path ./my-skill
python releaser.py validate --path ./my-cli --mode cli       # 任意零依赖 CLI 项目
python releaser.py validate --path ./my-pkg --mode package  # 任意零依赖 Python 包（拓 TAM）
python releaser.py validate --path ./my-skill --bench       # 对标头部：输出相对差距
python releaser.py validate --path ./my-skill --rubric      # 透明评分：权重 + 理由
```
它**真跑**以下检查并给 PASS/WARN/FAIL，最后输出**发布就绪分 0-100**（加权合计 100）：

| 维度 | 权重 | 检查内容 |
|---|---|---|
| frontmatter 字段 | 8 | 含 `name/version/license` |
| license 字段 | 4 | `license` 字段为 MIT/MIT-0 |
| LICENSE-SPDX | 8 | `LICENSE` 文件存在且被 licensee 识别（SPDX 可识别） |
| ASCII 版权 | 6 | 版权持有人名为 ASCII（否则判 NOASSERTION） |
| 无 skill-card | 8 | 全仓（含子目录）无 ClawHub 保留名 `skill-card.md` |
| doctor 门 | 10 | CLI 入口 `doctor --path .` 真跑退出 0（过 CI 必现失败陷阱） |
| CI | 8 | CI 含 `doctor` 步 + `tee $GITHUB_STEP_SUMMARY` |
| 引用完整 | 6 | SKILL.md 引用的 `scripts/references/assets` 文件真实存在 |
| 零依赖 | 6 | 无第三方 import |
| **★compile** | 8 | **全部 `.py` 通过编译（无语法错误）** |
| **★import** | 6 | **入口模块可 import（无 import-time 崩溃）** |
| **★--help 烟测** | 10 | **入口 `--help` 烟测通过（CLI 真能 boot）** |
| **★安全红线 secret** | 12 | **全仓无硬编码密码/授权码/API Token（防重演 v1.9.x 凭据泄露事故）** |

> **★功能验证是差异化价值**：skill-lint / agent-skill-linter / @effectorhq/skill-lint / Skill Validator 等竞品只查 paperwork，**没有任何一个把你的 CLI 真正执行起来证明它能 boot**。这是 releaser 独有的"engine 级"验证。

`--mode cli` 跳过 frontmatter / skill-card 检查，服务**任意**零依赖 Python CLI 项目；`--mode package` 进一步泛化到**任意零依赖 Python 包**（再加打包清单 `pyproject.toml/setup.py/setup.cfg` 检测，信息项不计分）。
加 `--json` 输出机器可读报告（`{path,mode,score,summary,items[,bench][,rubric]}`），可直接被 CI / 其他工具 / **市场闭环消费**；`--bench` 时附 `bench` 字段，`--rubric` 时附 `rubric` 字段（各维度权重+理由，分数可被审计）。
加 `--bench` 输出**对标头部**相对差距；加 `--rubric` 输出**透明评分**权重与理由。
退出码：有 FAIL 返回 1，否则 0。

### 2.1.1 gate —— ★CI 门禁（readiness-as-a-service）
```bash
python releaser.py gate --path . --min 90     # 就绪分 < 90 即非零退出，拦在发布前
python releaser.py gate --path . --min 90 --json
```
把"发布就绪分"变成**可编排的流水线闸门**：低于阈值（默认 90）即非零退出，直接拦在 CI 里。让本工具从"人跑的校验器"升级为"任何流水线可接入的质量门禁"——这是 agentic-validators 所代表的 hooks/门禁趋势的零依赖轻量版。

### 2.2 inventory —— 治理：你的技能哪些能发
```bash
python releaser.py inventory
# 或指定根：python releaser.py inventory --roots C:/Users/win/.workbuddy/skills
```
逐条打印：`技能 | lic字段 | LICENSE | CI | doctor`，并给出"发布就绪 N / 待补 M"。

### 2.3 gap —— ★市场情报：该造什么
```bash
python releaser.py gap
# 或指定根：python releaser.py gap --roots C:/Users/win/.workbuddy/skills
```
扫描本机已装技能，按 8 大类目（Developer Tools / Security / AI & ML / Data / Productivity / Web / Finance / Content）归类计数，报告**完全空白类目（缺口）**与**单薄类目（可补强）**，并对每个缺口给出 `scaffold` 建议命令。
加 `--scan-json <file>` 可**消费 find-skills++ 导出的真实市场扫描数据**（JSON 数组，每项 `{name, categories?, keywords?, description?}`），把"本机启发式"升级为「真实在售缺口」情报——这是 build 飞轮的**独有价值**：find-skills++ 扫缺口 → 本工具 `scaffold` → `validate` → `release` → 被 find-skills++ 检索推荐，数据回流。单个工具可复制，**完整的闭环更难被复制**。

### 2.4 selfcheck —— 零依赖校验
```bash
python releaser.py selfcheck --path .
```
扫所有 `.py`（跳过 `tests/` 与生成器 `scaffold.py`），把非标准库 import 列为 WARN。

### 2.5 scaffold —— 一键起项目
```bash
python scaffold.py my-cli-skill --author "He Wei" --email you@x.com --dest ./out
```
生成已避开 §3 全部陷阱的骨架（SKILL.md / `<name>.py` 带 doctor --path / tests/conftest / CI / LICENSE MIT-0 / listing / README）。

### 2.6 bump —— 升版本
```bash
python releaser.py bump --path . --type minor
```
升 `version` 并在 `CHANGELOG.md` 加条目（无则新建）。

### 2.7 release —— 本地提交 + 人工导入步骤（远程动作需显式授权）
```bash
python releaser.py release --path .                 # 默认：本地提交 + 打印人工导入步骤（不推送、不发布）
python releaser.py release --path . --dry-run        # 只生成导入步骤，不提交
python releaser.py release --path . --push           # 显式授权：git push 到远端
python releaser.py release --path . --publish        # 显式授权：经本机已登录的 clawhub CLI 发布
```
**安全默认**：`release` 默认**不触碰远端**——只做本地 `git add/commit` 并打印 ClawHub 人工导入步骤（自动解析仓库地址、Display/Slug、推荐分类、Topics≤48）。只有你显式加 `--push` 才会 `git push`、加 `--publish` 才会调用 `clawhub publish`（且要求本机已 `npm i -g clawhub` 并 `clawhub login`）。任何远端写入都需要你明确的命令行授权，工具不会静默推送或发布。

> **诚实说明**：ClawHub 无公开 REST/网页 publish 端点（无法代填 OAuth），网页"Publish"按钮仍需你登录会话点一次；本机已装并登录 `clawhub` CLI 时，`--publish` 是合法的显式发布路径。这已比"看文档自己点"的竞品快一个量级。

### 2.7.1 secretscan —— ★安全红线：消灭"不该进 GitHub 的凭据"

> **为什么必须有这道闸**：cli-skill-release 在 v1.9.x 曾因一个**明文 QQ SMTP 授权码被 `commit` + `push` 到公开 GitHub**，触发 ClawHub 的 `malicious.llm_malicious` 判定被 Hidden/Blocked——密码、授权码、API Token 这类东西，应该在**校对/审核/审定**环节就被消灭，绝不该有机会进仓库。

`secretscan` 是这道硬闸门的专用工具，可**独立于就绪分**单独跑，也可被 `validate` / `gate` / `release` 自动调用：

```bash
python releaser.py secretscan --path .                 # 扫全仓硬编码凭据，命中即 FAIL
python releaser.py secretscan --path . --allow-file .my-allow   # 自定义放行正则文件
python releaser.py validate --path .                   # validate 内含 secret 维度（权重 12），命中即 FAIL
python releaser.py release --path . --dry-run          # release 在"审定"环节硬拦：有凭据绝不提交/推送/发布
```

**扫描覆盖（宁可误报也要拦真凭据）**：
- ① **`.env` 文件本身即风险**（无论扩展名，命中即 FAIL，禁止入库）；
- ② **已知厂商令牌格式**：AWS Access Key、GitHub PAT、Slack/Google/Stripe/OpenAI/OpenRouter Key、JWT、PEM 私钥、`user:pass@host` BasicAuth 等；
- ③ **硬编码凭据赋值**：`PASSWORD = "..."` / `api_key="..."` / `client_secret='...'` 等——仅当**赋值左侧标识符本身含凭据关键词**才判，避免文档/字符串提及 password/token 误伤（也避免扫描器自身定义被自伤）。

**安全设计**：
- 环境变量引用视为安全（凭据由运行时注入，不入库）：`PASSWORD = os.environ.get(...)` / `os.getenv(...)` / `${VAR}` / `{{ secrets.X }}` 一律放行；
- 报告**一律脱敏**（仅留前 4 + 后 2 字符），**绝不回显明文**；
- **误报**在仓库根建 `.releaser-secret-allow` 写放行正则（谨慎使用——这等于你已确认该处无真实凭据）。

> **泄露应急**：若已有真实凭据入库，必须 **① 立即到对应服务轮换/吊销**（如 QQ 邮箱 SMTP 授权码）② `git filter-repo --path <file> --invert-paths` 清历史 ③ 强推覆盖远端旧历史。换密码优先于删代码——旧历史里的明文凭据一旦泄露即不可逆。

### 2.7.2 publish —— ★多站上架编排（正确更新/新技能后，一键分发多站）

> **设计原则（回应 ClawHub 误判 + 你的"校对/审核/审定"要求）**：安全闸门前置、显式逐站授权、默认不碰任何远程。这与 v1.9.3 之后"绝不静默外发"的整改一脉相承——**没有任何"无开关自动推全站"的路径**，从机制上杜绝重蹈 malicious 覆辙。

`publish` 是"正确更新或有新技能后，自动上传到多站"的统一入口：

```bash
python releaser.py publish --path .                      # 只跑校对+预览，不碰任何远程（防静默外发）
python releaser.py publish --github                      # 显式授权：推送到 GitHub（git add/commit/push）
python releaser.py publish --clawhub                     # 显式授权：经本机已登录的 clawhub CLI 发布到 ClawHub
python releaser.py publish --github --clawhub            # 两站一起（本轮已接入范围）
python releaser.py publish --github --clawhub --dry-run  # 只预览各站动作，不提交/不推送/不发布
python releaser.py publish --github --force-history      # 历史曾被 git filter-repo 重写、远端本地分叉时强推（--force-with-lease）
```

**执行顺序（每步都可被闸门拦截）**：
1. **校对**（validate）：先跑发布就绪扫描（含 ★安全红线凭据扫描），输出 0-100 分；
2. **审定**（secretscan）：命中硬编码凭据/授权码 → **直接拒绝上架任何站点**，绝不入库/外发（确认无误报可用 `--allow-secret-risk` 强制，危险）；
3. **分发**：每个目标需对应显式开关（`--github` / `--clawhub` / `--xiaping` / `--workbuddy`），未开的站绝不触碰；GitHub 走 `git push`（普通 fast-forward，必要时 `--force-history`），ClawHub 走 `clawhub publish`（需本机已装 CLI 并登录，否则回退人工导入情报）。

> **虾评 / WorkBuddy 本轮为预留位**：`--xiaping`（xiaping.coze.site，Coze 生态）、`--workbuddy`（open.workbuddy.cn SkillHub）这轮**只给人工上传链接，未接入自动上传**（两者均无公开 API）。待接入对应开放接口/机器人后，同样的显式授权模型即可真自动，无需改使用方式。

### 2.8 doctor —— 自检
```bash
python releaser.py doctor            # 自检 cli-skill-release 自身（结构+零依赖）
python releaser.py doctor --path .   # 等价于 validate
```

### 2.9 badge —— ★链回徽章（便于引用与致谢）
```bash
python releaser.py badge --path .                 # 打印 readiness 徽章 SVG + 链回片段
python releaser.py badge --path . --output readiness-badge.svg   # 写 SVG 到仓库
```
基于 `validate` 的就绪分生成 shields 风格徽章（绿≥90 / 黄 70-89 / 红<70），并输出一段可直接贴进
你技能 README 的 markdown——**徽章图片自托管在你的仓库 raw 地址，点击链回本技能页**。
这是"链回徽章"的用意：你每发一个技能都挂这张徽章，访问你仓库的人点进来即可使用本工具，形成自然的引用与致谢。

### 2.10 promote —— ★宣传工具箱（把一次下载变成一次分发）
```bash
python releaser.py promote --path .    # 给定路径则先展示就绪分
```
一次性输出：① README 徽章区 ② 要点说明（"别人 lint 文档，我们 execute 引擎"）③ 社媒/社区可直接转发的文案 ④ 安装一行 ⑤ **链回玩法说明**。照着贴，即可把本工具介绍给你的受众。

### 2.11 diagnose —— ★长尾功能：症状→根因→修复（覆盖长尾搜索）
```bash
python releaser.py diagnose --list                       # 列出全部已知症状
python releaser.py diagnose --symptom "LICENSE 显示 Other"
python releaser.py diagnose --symptom "pytest exit code 2"
python releaser.py diagnose --symptom "skill 搜不到"
```
把"用户实际会搜的长尾问题"映射成根因+修复——**这正好覆盖用户的长尾搜索**：有人搜
"skill LICENSE 显示 Other" / "pytest exit code 2" / "CI 一直红" / "技能搜不到"，我们 README 里的这些
短语被搜索引擎/ClawHub 索引 → 点进来 → 跑 diagnose 即得答案。竞品（jeremyknows/publish-skills 等）
只给静态清单，我们给"可执行 + 可诊断"。已知症状覆盖：LICENSE 显示 Other、pytest exit code 2、
CI 一直红（doctor 缺 --path）、skill-card.md 冲突、Topics 超 48、入口 import 崩溃、技能搜不到、
"我的技能能不能发"（自然语长尾）。

### 2.12 preflight —— ★长尾功能：市场定制上架前检查清单
```bash
python releaser.py preflight --market clawhub       # ClawHub/OpenClaw
python releaser.py preflight --market skillhub      # SkillHub 镜像
python releaser.py preflight --market agentskills   # agentskills.io/GitHub 开源标准
python releaser.py preflight --market generic       # 通用（默认）
```
输出目标市场的上架前检查清单（markdown 勾选框 + 必填/建议标注），逐条对应其真实规则
（MIT-0、skill-card.md 保留名、Topics≤48、3 分类、仅文本文件、GitHub topics、gh skill publish --dry-run 等）。
直接回答长尾搜索："skill publish checklist" / "pre-publish checklist for agent skills" /
"what am I missing before I publish"——**清单本身也可贴进 README 被索引**。

### 2.13 registry —— ★状态层：已发布技能账本（治理者底座）
```bash
python releaser.py registry list                       # 列出账本中已发布技能
python releaser.py registry show cli-skill-release      # 查看单条记录
# release 成功会自动登记；也可手动：
python releaser.py registry add my-skill --name "My" --repo https://github.com/me/my-skill --version 1.2.0 --score 100 --market clawhub
```
`release` 每次发布（无论 clawhub CLI 发布还是人工导入）都会把技能登记进本地账本（默认 `~/.workbuddy/cli-skill-release/ledger.json`，可用 `RELEASER_LEDGER` 覆盖）。这让工具**跨多次运行持有"已发布技能账本"**——从一次性校验器变成发布侧的**治理者**（对标 find-skills++ 的状态层 / 全生命周期治理）。

### 2.14 recheck —— ★生命周期：再校验 / 漂移治理（持续治理）
```bash
python releaser.py recheck                  # 复核账本中所有已发布技能
python releaser.py recheck my-skill         # 只复核某一个
```
重新对每个已发布技能跑 `validate`，对比登记时的分数，报告**漂移**（分数下降）、**弃用**（现 FAIL / 低于门禁）、**缺失**（本地目录已搬走）、**健康**。把"发完即终"升级为**持续治理**——这是"治理技能的命"，也是 find-skills++ 生命周期治理的对位。

### 2.15 selfdemo —— ★自证底座：全量自证（主张即演示，对标 smoke.py）
```bash
python releaser.py selfdemo
```
当场对自己仓库运行每一个能力（validate / selfcheck / badge / preflight / diagnose / registry / gap / recheck）并打印演示摘要，**主张即演示**：证明"别人 lint 文档，我们 execute 引擎"不是口号，是已验证事实。对标 find-skills++ 的 `smoke.py`（全量自证）——可验证的信任不靠叙述，靠当场跑给你看。

### 2.16 curate —— ★供给侧策展：主动告诉生态该造什么（升级版 gap）
```bash
python releaser.py curate
python releaser.py curate --scan-json market.json   # 叠加 find-skills++ 真实市场数据
```
把 `gap` 的市场情报升级为**可操作的策展清单**：结合本机已发布（含账本）与可选市场数据，按优先级输出"该造什么"——① 组合机会（市场有供给 / 你为 0，最该造）② 本机空白类目 ③ 单薄类目。从被动等搜索升级为**主动策展分发**（find-skills++ 主动策展对位），让工具成为生态的"供给侧大脑"。

---

## 5. 如何让本技能被找到 + 链回致谢

本技能不止"自己好用"，更要**主动被找到、一直被需要、自己扩散**。这套机制写进工具本身：

1. **被 AI 找到**：上架时 `keywords`/`description` 命中高频查询——"发布技能 / 上架 skill / publish skill / validate skill / 技能质量门禁 / skill CI gate / 技能徽章"。AI 发现工具（find-skills++ 等）按这些词文本匹配返回候选，命中即被推荐。
2. **被人类找到**：ClawHub/SkillHub 上架优化（MIT-0、3 分类、Topics≤48）+ 徽章在每个使用者仓库可见（口碑曝光）。
3. **一直被需求**：发布与每次更新都要重跑 `validate`/`gate`/`badge`——它是发布流水线的**必经环节**，不是一次性下载；徽章也要随版本刷新，形成习惯依赖。
4. **真能解决问题**：★功能级验证（compile+import+--help 真跑 CLI）挡住"格式完美一跑就崩"，是竞品无人做的硬价值。
5. **链回徽章**：`badge` 让用户在自己的技能仓库挂一张就绪分徽章，点击链回本技能页，便于他人引用与致谢。配 `promote` 工具箱，使用者可据此撰写发布说明。

#### 5.1 中文怎么被找到 / 英文怎么被找到（基于实测的检索机理）

**中文通道（AI 发现 = 关键词/文本匹配）**
- AI 发现工具（find-skills++ 等）：本地 `ls` → 原生市场按 `keyword` 搜 → 社区源返回 `score`（对 `name/description` 匹配，<0.05 忽略）→ 合并排序。**所以 `keywords`/`description` 必须命中中文高频词**——我们已命中（发布技能/上架/校验/门禁/徽章/长尾诊断/上架清单）。
- 人类通道（ClawHub/SkillHub 搜索框、GitHub topics、公众号、搜索引擎）：靠 **README 的中文长尾标题 + 仓库 GitHub topics（agent-skills, claude-skills, skill-md, ai-agents）+ 徽章口碑曝光**。

**英文通道（评测结论：三杠杆）**——2026 实测证据：
- **杠杆 1：`description` 是 vector search 的匹配面**（ClawHub 官方确认 "The SKILL.md description is what vector search matches on"）。我们已把 `description` 写成含英文触发短语的双语，并加 `description_en`。
- **杠杆 2：`tags` 决定相邻位**（tags 让你紧挨 elevenlabs-tts 等同类）。我们已加 `tags: [publish, skill-publishing, pre-publish-checklist, clawhub, agent-skills, ...]`。
- **杠杆 3：GitHub topics 喂外部索引器**（SkillsMP / skillsdirectory / claudeskills.info）。发布时 `gh repo edit --add-topic agent-skills claude-skills codex-skills skill-md ai-agents`。
- **自然语长尾触发**：英文用户爱搜 "Is this skill ready to publish?" / "What am I missing before I push this skill to GitHub?" / "Audit this skill against the Agent Skills spec"——这些短语已进入我们 `description` 与 README 的 FAQ 标题。

#### 5.2 长尾词与长尾功能（文档覆盖常见搜索短语）

**长尾词（中文）**：技能发布前检查清单、ClawHub 上架教程、skill LICENSE 显示 Other 怎么办、pytest exit code 2 修复、技能 CI 一直红、agent 技能发布流水线、技能质量门禁、发布就绪分、技能徽章、零依赖 Python 发布、技能搜不到怎么办。

**长尾词（英文）**：skill publish checklist、pre-publish checklist for agent skills、is my skill ready to publish、what am I missing before I push、audit skill against Agent Skills spec、skill LICENSE shows Other、pytest exit code 2、ClawHub publish guide、make my skill discoverable、agent skill CI validation。

**长尾功能（已落地）**：
- `diagnose`：症状→根因→修复，直接回答上述长尾搜索（竞品只给静态清单，我们给可执行诊断）。
- `preflight`：市场定制上架清单，回答"发布前检查清单"类搜索；清单本身贴进 README 即被索引。
- `README.md`：用长尾问题做 H2/H3 标题 + 双语，被搜索引擎/ClawHub/GitHub 索引。
- `release` 默认只做本地提交 + 打印人工导入步骤；显式 `--push` 才推送、`--publish` 才经 clawhub CLI 发布。

> 文档即说明：技能文档清楚说明如何引用与致谢本工具，便于使用者理解与传播。

#### 5.3 体系升级：从"发布工具"到"发布侧治理系统"（对标 find-skills++）

v1.9.0 把 cli-skill-release 从"一次性发布工具"升级为"发布侧治理系统"，补齐 find-skills++ 治理模型里我们缺的 4 根支柱：

| 支柱 | 子命令 | 解决的问题 |
|---|---|---|
| **A 状态层** | `registry` | 跨多次运行持有"已发布技能账本"，从瞎子变治理者 |
| **B 生命周期** | `recheck` | 发完持续治理，漂移/弃用/缺失可见 |
| **E 自证底座** | `selfdemo` | 主张即演示，信任不靠叙述（对标 smoke.py） |
| **F 供给侧策展** | `curate` | 主动告诉生态该造什么，从被动到主动 |

> **可持续价值**：find-skills++ 占"发现侧治理位"，我们通过 v1.9.0 补上"发布侧治理位"。两个治理位一旦接通（C/D 双向活通道：让 find-skills++ 读取本工具的 readiness 信号 + 本工具消费其市场数据），才是更完整的闭环。C/D 需 find-skills++ 打通接口 + 你的授权，本期已预留 `releaser.py gap --scan-json` 与账本数据结构作为对接基座。

---

## 3. 背景知识：发布陷阱速查（散文，按需查阅）

### 3.1 sys.path 注入（pytest exit code 2 经典根因）
CLI 在模块级把 `scripts/` 加 `sys.path` 后 `import`，CLI 自己能跑；但 `tests/` 直接 import 依赖 conftest 注入。
**正确做法**：在 `tests/conftest.py` 注入根与 `scripts/`（脚手架已写好）。
退出码：`2`=收集期炸（import/语法），`1`=测试失败，`0`=全过，非零都让 CI 红。

### 3.2 自检测试门 doctor 必须定义 `--path`
CI 里 `python main.py doctor --path .` 时，`doctor` 子命令**必须真定义了 `--path`**，否则
`unrecognized arguments: --path .` 在**全平台必现失败**，整 job 红——且 pytest 的 traceback 照不出它
（它是独立 step）。这是 find-skills++ 早期 CI 一直红的**真凶**。

### 3.3 LICENSE 被 GitHub licensee 识别
- 多版权行 / **非 ASCII 版权持有人名**（如中文"何巍"）易被判定 `NOASSERTION` / **Other**。
- ClawHub 强制 **MIT-0** 再分发 → LICENSE 直接写 **MIT-0** 最稳。
- 派生上游时：新增自研内容用 MIT-0，并新建 **`NOTICE`** 完整保留上游 MIT 版权与许可全文（满足署名义务）。
- 验证（无需登录）：`api.github.com/repos/{owner}/{repo}/license` 看 `license.spdx_id`。

### 3.4 ClawHub / SkillHub 上架规则（2026 实测）
1. **强制 MIT-0**（不是 MIT）。
2. **`skill-card.md` 是保留名**：仓库根（含子目录/夹具）有同名文件会报
   `skill-card.md is generated by ClawHub and cannot be published directly` → 全仓改名（如 `market-card.md`），
   用 `git ls-files | grep skill-card` 全仓排查。
3. **Topics ≤48 字符（整段，含逗号）**——不是单个标签。先填最短组合卡过去（如 `skill-discovery, security`）。
4. **GitHub 账号龄 ≥1 周**。
5. **分类必选 3 个**（Developer Tools / Security / AI & ML 等）。
6. **发布后核验循环**：含 `<main>.py`+`scripts/`、License 显示 MIT-0、SkillHub 镜像可搜到；
   新提交会让线上 listing 显示 "Import is out of date"（已发布技能不受影响，想同步新文件再点一次 Re-run preview）。

### 3.4.1 ClawHub CLI 实操（本机）
- 安装：`npm i -g clawhub`（本机装在 managed node workspace：`node/workspace/node_modules/.bin/clawhub`）。
- **Windows 必须调 `.cmd` 包装器**（`clawhub.cmd`），直接调 node bin 会被 PATH 错误导崩。
- 查登录态：`clawhub whoami`（未登录回 `Not logged in`）。
- 查上架状态：`clawhub search <slug>`（不需登录，直接回 `@owner DisplayName installs/60d`）。
- 真一键：`clawhub login --token <token>`（也支持 device flow）后 `clawhub publish`。
- 没有登录态时 `release` 走"人工导入情报"回退（见 §2.7），由你在 ClawHub 网页点一次 Import。
- ClawHub **分类固定 8 选、强制满 3**：Developer Tools / Security / AI & ML / Data / Productivity / Web / Finance / Content。

### 3.4.2 确证"已上架"的核验法（搜索索引滞后）
- `clawhub search <slug>` 对新上架技能**可能不立即回显**（索引滞后，只回别的含相同词的技能）——**搜不到 ≠ 没上架**。
- **权威核验用注册表接口**：`clawhub inspect <owner>/<slug>`（免登录，公开技能可用）返回完整元数据即真上架；`clawhub search <slug>` 也能回 `@owner DisplayName installs/60d`。
- ⚠️ **不要**用 OG 图接口（`https://clawhub.ai/og/skill?...`）判断上架：该接口对**任何** slug（含不存在的假 slug）都返回 HTTP 200 + 一张占位图，**不能作为"已上架"证据**。
- 页面 `og:title` 应为 `<slug> — ClawHub`、`og:description` 含 `Agent skill by @<owner>`；技能审核通过后页面才会从占位壳变为真实技能页。

### 3.5 CI 排障 SOP（看不到日志：403 / 需 admin）
1. `git ls-remote origin HEAD` 确认远程实际部署到的提交（本地 `ahead N` = 有 N 个没推）。
2. 公开 API 查 LICENSE：`api.github.com/repos/{owner}/{repo}/license`。
3. 本地建 venv 跑 pytest 复现：exit `2`=收集错误，`1`=测试失败。
4. 逐个 step 命令本地跑，重点查未定义参数的子命令。
5. CI 里把 pytest 输出 `tee` 到 `$GITHUB_STEP_SUMMARY`（见 §3.3 引用完整性 / 3.4 上架）。

### 3.6 环境与工具 gotchas（Windows 沙箱实测）
- **bash shim 偶尔 PATH 丢失** → 用 Python **绝对路径**调用脚本。
- **phantom 缓存** → 关键改动用 Python 直读磁盘校验（`open(path, encoding='utf-8')`）。
- **推送可能被沙箱静默拦截**（输出空、远程没动）→ 放开沙箱重推，再 `git ls-remote` 确认远程 HEAD 已前进。
- **GitHub API 密码鉴权已停用**（实测 `POST /user/repos` 返回 `401 Requires authentication`）：建仓库只能走
  ① 已认证 SSH（只能推**已存在**仓库，**不能建**）② **PAT（classic，repo 范围）** ③ 用户在 GitHub 网页点 New repository 自建空仓库。密码不能用于 API / 建库。
- **clawhub CLI 在 Windows 要调 `.cmd` 包装器**：直接调 node bin 会被 PATH 错误导崩（见 §3.4.1）。
- **pytest 批量删除守卫**：teardown 清临时目录可能触发 `SystemExit: 1`（"Exception ignored"），**不影响结果**
  （returncode 0、全部 passed）；跑测试用独立 subprocess 把结果写文件再读，避免守卫杀掉结果写入。

---

## 4. 发布检查清单（交付前逐项勾）

- [ ] `python releaser.py validate --path .` → 零 FAIL，就绪分接近 100
- [ ] `python releaser.py secretscan --path .` → 无硬编码凭据/授权码（安全红线通过）
- [ ] `python releaser.py selfcheck` → 零 WARN（或仅已知误报）
- [ ] `doctor` 与 `doctor --path .` 退出 0
- [ ] LICENSE 为 MIT-0 + ASCII 版权名；公开 API 确认 `spdx_id=MIT-0`
- [ ] CI workflow 存在且徽章指向它；pytest 输出已 tee 到 Step Summary
- [ ] 多站上架：先 `publish --path .`（仅预览）确认无误，再 `publish --github --clawhub`（显式授权，安全闸门前置）
- [ ] `git ls-remote` 确认所有修复提交已推（无 `ahead N`）
- [ ] 全仓无 `skill-card.md` 残留
- [ ] 上架：License 选 MIT-0、3 分类已选、Topics 整段 ≤48 字符
- [ ] 发布后核验：含 `<main>.py`+`scripts/`、SkillHub 镜像可搜到
- [ ] （可选）`python releaser.py gap` 看本机类目覆盖，决定下一个该造什么
