---
slug: cjg-skill-forge
name: cjg-skill-forge
displayName: 技能锻造炉——打造/重铸一个牛逼的技能，并且一直牛逼
version: 3.2.0
description: |
  技能锻造炉 / Skill Forge —— 元技能：**创建、升级、重铸、审计**一个「全球最牛」的 WorkBuddy / AI 技能，并让它越用越强。**锻造**模式：从零打造新技能（带版本反馈环、真实素材覆盖审计、外部标杆对比、自我迭代、生产签批、真机验证）；**审视**模式：10 维加权评分尺，给任何技能（含它自己）打分，判断够不够好；**重铸**模式：审计并整合本机重叠技能、合并同类、整理技能库，给出重铸计划与推荐基座；还能让技能更 AI 易读（清晰化）。当你想"做到最牛"、创建一个 XX 技能、升级我的技能、review this skill、整理技能、合并同类、skill 怎么改、SKILL.md 怎么写、怎么制作一个 AI 技能时，用它。

  Meta-skill to forge, upgrade, review, recast and refactor world-class WorkBuddy/AI skills — create a new skill from scratch, score any skill with a 10-dimension rubric, consolidate overlapping skills, and make skills more AI-readable. Use when building, improving, auditing, merging, or organizing agent skills.
agent_created: true
---

# Skill Forge · 技能锻造炉（元技能 · 锻造 + 审视 / Meta-skill）

> **一句话**：四模式（锻造 / 审视 / 重铸 / 清晰化）元技能，把任何技能从粗糙 v1 锻造到「全球最牛」，并活在使用反馈环里持续进化。
> **本文件是导航版（~150 行）**：路由 + 参数 + 红线 + 锚点索引；细节按需读 `references/*`（触发到才读取）。

---

## 零 a、首次使用：注册（强制 · 2026-09-28）

- **云交互命令（forge-publish / upload_signals / cjg-proposal-cli 等）启动时会校验创作者凭证**：未注册（技能目录缺 `.deploy/cloud_open.json` 的 signal_token）→ 命令拒绝执行并输出注册引导。
- 注册（约 1 分钟）：`python scripts/forge-register.py register`（按提示填邮箱 → 收验证码 → 回填）。
- **纯离线例外**：不注册 = 只能本地模式（信号仅本地蒸馏、不发布上线）。首次使用时向创作者说明两者取舍，显式选择，无静默绕过。

---

## 零 b、同步策略关卡（发布必选 · 2026-09-28）

发布时必须选**同步策略**（`forge-publish --sync-policy off|warn|block`，缺省交互询问）：

| 策略 | 含义 | 适用 |
|---|---|---|
| off | 不接入更新机制 | 纯内容/一次性/展示型（方法论、模板、showcase、原型） |
| warn | 提示有新版，不阻塞 | 大多数工具型技能（默认推荐档） |
| block | 版本落后即拒绝执行 | 外部 API/协议对齐、凭据/安全敏感（自身 sync/forge、gateway-ops、biblio-base） |

- **block 硬校验**：策略选 block 时，SKILL.md 必须含版本同步指引（提到 `sync_gate` 或 `skill_sync.py gate`），否则发布器拒绝。
- 策略随发布回写藏经阁索引（`skill_releases.sync_policy`），用户端 `cjg-skill-sync gate` 据此在调用时放行/提示/拦截。

---

## 零、进化燃料（本地即开 · 云端 opt-in）

- **本地记录默认开**（只记方法层标签，零原文零身份，留本机）；说「别记了」全关。
- **云端上传默认关**（零密钥）：说「开启云同步」才匿名回传藏经阁·易筋；「别传了」关云端（本地不受影响）。
- 透明：说「查看我的信号 / 我的技能成长 / 删除我的信号 / 同步我的信号 / 同类用法 / 本周改进」即触发。
- 定时回传为可选增强包（基础包零后台）；不装则本地记录，可手动 `scripts/upload_signals.py`。

---

## 命令执行约定（所有 scripts 命令先读这条）

所有 `scripts/*.py` 从技能根目录运行（先 `SKILL_DIR=$(find ~/.workbuddy/skills -maxdepth 2 -type d \( -name skill-forge -o -name cjg-skill-forge \) 2>/dev/null | head -1) && cd "$SKILL_DIR"`；说明：本地目录名可能是 `skill-forge`（WorkBuddy 安装）或 `cjg-skill-forge`（GitHub 克隆），且可能位于 `skills/` 下一级或命名空间子目录——用 find 兜底定位，勿用 `*/cjg-skill-forge` 这类假定发布 slug 即目录名的 glob。「线上发布 slug」始终是 `cjg-skill-forge`，与本地目录名是两回事）。`session_hook.py` 支持不带 `--dir` 自动推导。校验 / 打包脚本在 skill-creator 插件：`VALIDATOR=$(find ~/.workbuddy/plugins -name quick_validate.py|head -1) && python "$VALIDATOR" <技能目录>`。

---

## 快速上手（30 秒）

**第 0 步 · 云进化引导（进模式 A 必做）**：向创作者说人话说明「技能发布后终端用户匿名反馈回流→聚合提案→你审核发新版」闭环，并提示三件套（注册 `forge-register.py register` / 开启云同步 / 可选每日回传）。创作者说跳过即尊重。

1. **锻造 / 大升级** → 模式 A → S0–S8 流水线。  2. **发布前审计** → 模式 B → 10 维评分。  3. **技能库重叠** → 模式 C → `recast_scan.py`。  4. **AI 读不准** → 模式 D → S7 清晰化。

---

## 何时使用（触发词）

| 意图 | 模式 | 触发词 |
|---|---|---|
| 创建 / 大升级 | A 锻造 | "做到最牛"、"创建 XX 技能"、"升级我的技能"、forge、create skill |
| 审计技能 | B 审视 | "review this skill"、"够不够好"、skill audit |
| 整理合并库 | C 重铸 | "整理技能"、"合并同类"、skill cleanup |
| 更 AI 易读 | D 清晰化 | "改得更 AI 易读"、make skill clearer |
| 提案 / 信号 / 成长 | 闭环 | "看看提案"、"查看我的信号"、"我的技能成长" |

---

## 模式路由

| 模式 | 进入 | 核心 | 引用 |
|---|---|---|---|
| **A 锻造** | 新建 / 大升级 | 锻造循环 → **A.5 真机 S0–S8** | 深度锻造方法论已上云：注册藏经阁 + opt-in 由 `cjg-report` 免费增强提供；离线降级用本地 21 内核 |
| **B 审视** | 审计 | 评分尺 → 10 维 → 反模式 → 报告（`skill-report.py` 免费出雷达） | `skill-review-rubric.md`（D1–D10 留本地）｜ 反模式/深度方法论注册藏经阁免费解锁 |
| **C 重铸** | 重叠 | `recast_scan.py` 只读 → 确认合并 | `skill-consolidation.md` |
| **D 清晰化** | S7 / 显式 | D1–D4 + 保真闸 | `clarity-coverage.md` `clarity-fidelity-template.md` |

---

## 锻造循环 S0–S9（模式 A · 缺一不可）

| 阶段 | 必交付物 | 跳过后果 |
|---|---|---|
| S0 脚手架 | SKILL.md + 三件套 + **信号套件**(`forge-signal-kit.py`) | 无法回传信号 |
| S1 真实接线 | 真实调用语法 | 完成度 0 |
| S2 真机取证 | 跑通 1 条主链路 → `*_evidence.md` | 空话 |
| S3 外部标杆 | ≥3 全球竞品对标 | 不知排第几 |
| S4 覆盖审计 | 真实 ID 核对 | 隐性缺口 |
| S5 生产签批 | 评审文档 + 用户签批(纪律 5) | 越界 |
| S6 校验 + 安全 | quick_validate/package_skill + 纪律 13/17 | 不可发布 |
| S7 清晰化 | D1–D4 + 保真闸 | AI 读不准 |
| S8 可推广 | discovery/intro ≤1024(纪律 16) | 平台找不到 |
| S9 联合测试 | `joint_test.py` 三侧三方全绿(纪律 18) | 带病发布 |

> 端到端权威执行参考：`references/pipeline.md`（每步命令 / 产出 / 失败兜底 / 闸门）。

---

## A.0 明确不做清单（强制边界）

不替用户做：创意决策（选题 / 文案 / 设计方向）、选发布版本号、付费 / 对外发布（除非明确指令）。未触发 A.1 任一动作时，不假装执行、不编造结果——直接停并说明「我不做 X，因为…」。

## A.1 交互指令响应（强制 · 不可忽略）

| 指令 | 执行 | 未触发即停(unmet_action) |
|---|---|---|
| 开启云同步 | `.cloud_optin=on`(+建每日任务) | 说明权限原因 |
| 别传了 | `.cloud_optin=off` | 同上 |
| 别记了 / 再开 | `.optin=off / on` | 同上 |
| 查看我的信号 | `signal_control.py view` | 路径未找到 → 重跑 inject |
| 我的技能成长 | `growth_report.py report` | 同上 |
| 删除我的信号 | `signal_control.py delete`(需确认) | 先确认 |
| 同步我的信号 | `download_signals.py pull` | 未注册 / 未开 → 引导 |
| 同类用法 / 本周改进 | `growth_report.py report --with-cloud` | 引导注册 |
| 看看 / 应用 / 打回提案 | `cjg-proposal-cli.py list / get / approve / reject` | 缺 .deploy → 引导 register |

## A.2 会话钩子 + 收尾信号块（强制 · 本地记录默认开）

- **开始**：`python scripts/session_hook.py start`（补传 + 拉回 + 缺失检测，一条命令，失败不阻塞）。
- **结束（必须 · 结束时记录方法层信号与客观使用）**：① 输出 `[信号] L<层>·<事件>`（off 时 `[信号] off`）② `python scripts/session_hook.py end --event L3:helpful`（脚本写标准 JSON 到 `signals-log.jsonl`，禁手写）③ 调过外部服务则说 `[使用] <服务>×N 成功M 失败K` 并跑 `session_hook.py usage --calls N --success M` ④ 已开云同步则 `upload_signals.py`。
- **动作链遥测（P1-4）**：用户完成白名单动作后 `python scripts/session_hook.py action <name> <outcome>`（name 见 `references/signals.md` §八；守体验铁律：匿名 / 方法层 / opt-in / 零 PII）。
- 仅方法层标签，零对话内容 / 零身份，只写本技能运行时文件。收尾信号块是用户可验证凭证。
- **前瞻红线（自动改进写回开放后）**：任何自动写回前先 `scripts/apply_guard.py --snapshot` 建快照 + 写 CHANGELOG，落地后 `--check` 对比采纳率，下降自动告警回滚。当前版本只度量不改。

**A.5 硬规则**（违即退回 S0）：S1/S2 不可跳过；先疑己再断外；够不到真环境标「非真机」；真实返回即证据禁编造；容错来自真机；不写参赛话术；S7 保真闸；S8 复用 S7 产物。

---

## 18 条纪律 · 红线速查

| # | 红线 |
|---|---|
| 1 覆盖审计 | 真实 ID，禁编造 |
| 2 外部标杆 | 标杆 = 全世界 |
| 3 自我迭代 | 主动 3–4 轮自审 |
| 4 不说谎说服 | 绝不断言虚假确定 |
| 5 生产签批 | 先评审 + 用户签批；停即停 + 回滚 |
| 6 真机测试 | 跑通才打包 |
| 7 触发精度 | description "Use when..."；SKILL.md <600 行；写作见 `skill-writing-guide.md` |
| 8 范围纪律 | 删掉 agent 照样干 → 不是技能 |
| 9 反馈环 | 默认观察，几乎不提问 |
| 10 宪法治理 | project/agent/workflow 必带宪法 |
| 11 技能注入 | 燃料 + footer + coverage.md；发布走 forge-publish |
| 12 融合连贯 | 冲突显式裁决；反缝合怪 |
| 13 发布包脱敏 | 密钥 / PII / 台账绝不进包 |
| 14 清晰化保真 | 只改怎么说不改做什么 |
| 15 版本同步 | version 单一真相源，先 bump |
| 16 可推广闸门 | find-skill 友好 + intro ≤1024 |
| 17 云鼎安全审计 | SkillHub 前置；Malicious 硬阻断 |
| 18 联合测试闸门 | `joint_test.py` 三侧三方全绿才下一步 |

---

## 结构与校验

- 导航式：SKILL.md 只留路由 + 红线，细节在 `references/`。
- `description` 单行双引号、无 `<>`、≤1024 字符。
- 校验：`quick_validate.py <dir>` → `package_skill.py <dir>`。

## 资源索引（按需加载 · 锚点）

- **方法论**：`references/skill-writing-guide.md` · `references/skill-review-rubric.md`（D1–D10 留本地）· `references/trigger-keywords.md` ｜ 深度锻造方法论（forge-modes / forge-disciplines / skill-types / anti-patterns 等 9 篇）已上云：注册藏经阁 + opt-in 由 `cjg-report` 免费增强提供，离线降级用本地内核。
- **质量纪律**：`references/coverage-audit.md` · `references/simulation-testing.md` · `references/project-governance.md` · `references/skill-consolidation.md` ｜ 反馈环 / 流失反思 / 人设设计（feedback-loop / churn-reflector / persona-design）已上云，注册藏经阁免费解锁增强。
- **清晰化 / 分发**：`references/clarity-coverage.md` · `references/clarity-fidelity-template.md` · `references/promotability-gate.md` · `references/yunding-security-audit.md` · `references/security-audit.md` · `references/discovery.md`/`references/intro.md` · `references/coverage-seeding.md`
- **执行参考**：`references/pipeline.md` · `scripts/forge_pipeline.py` · `scripts/forge_runbook.py`(→`scripts/run_verified.py`) · `scripts/joint_test.py` · `scripts/selfcheck.py` · `scripts/forge-describe.py`
- **模板**：`references/clarity-fidelity-template.md` · `references/cloud-config-schema.md` ｜ 硬核锻造模板（contest-hard-forge / quality-iteration-playbook 等）已上云，注册藏经阁免费解锁。
- **免费评测报告**：`scripts/skill-report.py <技能目录>` 离线出 D1–D10 雷达图；`--cloud --token <藏经阁令牌>` 免费解锁云端增强诊断（注册藏经阁即通过邮箱验证即解锁，**报告功能永远免费**）。
- **人设记忆**：`references/acquaintance.md`（persona 技能的跨会话用户画像卡；persona 方法论已上云，本卡常驻本地）

## 非职责边界

不是运行时工具：**不脚手架**（用 skill-creator）、**不自动发布**（产出待发目录）、**不替代领域专长**、**不保证通过**、**不在每次对话跑**。

---

> ⚙️ 本技能由「技能锻造炉」自我锻造 · 🔄 持续迭代，由藏经阁·易筋支持。想打造 / 重铸牛逼技能？SkillHub 搜 slug「cjg-skill-forge」。
