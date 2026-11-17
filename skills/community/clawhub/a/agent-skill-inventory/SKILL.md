---
name: skill-inventory
slug: skill-inventory
displayName: 技能盘点+健康体检 · Skill Inventory & Health Check
summary: Scan any skills directory and classify skills into used / protected / closeable / manual-review buckets with anti-accidental-close guardrails. 扫描技能目录，按「在用/受保护/可关闭/需人工确认」四档输出瘦身建议，防误关护栏齐全。
description: >-
  Office-agent skill inventory & health check. Scans any skills directory, measures size and context-token footprint, detects duplicates, and classifies skills into used / protected / closeable / manual-review buckets. Reverse-dependency scanning locks skills referenced by automations, hooks or plugins. Read-only by default: two disclosed, consent-gated writes — `--overrides --apply --yes` (programmatic close on platforms like WorkBuddy; dry-run without --yes) and `--set-lang` (saves language preference to ~/.workbuddy/skill-inventory.json) — plus one backup artifact (timestamped settings.json.bak.<ts>) created before the close write. No network, no subprocesses. English docs: SKILL.en.md.
  办公型 Agent 技能库盘点与效能体检。扫描任意技能目录，统计数量/体积/上下文 token 占用，识别重复技能，按「在用/受保护/可关闭/需人工确认」四档给出建议；反向依赖扫描锁定被自动化/Hook/插件引用的技能。默认只读，两处写路径均需授权：`--overrides --apply --yes`（缺 --yes 仅预览）与 `--set-lang`（写语言偏好）。无网络、无子进程。
tags: [skill-management, efficiency, token-optimization, inventory, devops]
author: Elisabeth15501
version: 1.5.3
allowed-tools: Bash(python scripts/skill_inventory.py:*), Read, Glob, Grep, Write(~/.workbuddy/settings.json), Edit(~/.workbuddy/settings.json), Write(~/.workbuddy/skill-inventory.json), Edit(~/.workbuddy/skill-inventory.json)
metadata:
  openclaw:
    requires:
      bins: [python3, python]
    permissions:
      network: none
      subprocess: none
      persistence: "no autonomous residency (no cron, startup script or daemon); two consent-gated config writes and one backup artifact DO survive the run — see filesystem.write"
      capabilities: ["file-read", "file-write"]
      filesystem:
        read: "skills directories, usage logs, automation/hook/routing/plugin configs"
        write: >-
          DECLARED STATE-CHANGING CAPABILITIES, all consent-gated and disclosed:
          (1) writes ONLY the "skillOverrides" key of ~/.workbuddy/settings.json via
          --overrides --apply --yes, reversible via the host /skills menu.
          This can persistently disable the listed skills and alter agent behavior — that is
          its disclosed purpose; it never runs without explicit user confirmation.
          (2) writes ONLY the report language preference file ~/.workbuddy/skill-inventory.json
          ({"language": "auto|zh|en"}) via the explicit --set-lang flag — a user-controlled
          display preference: not loaded automatically at startup, nothing scheduled or
          registered from it, reversible via --set-lang auto or by deleting the file;
          this is an authorized cross-session write, not autonomous residency.
          (3) creates ONE disclosed backup artifact during --apply --yes: a timestamped copy
          ~/.workbuddy/settings.json.bak.<YYYYMMDD-HHMMSS> written beside settings.json before
          it is modified (inert safety copy; its path is printed to the user; never read back).
---

# skill-inventory · 办公型 Agent 通用的技能库盘点与效能体检

> **English docs**：`SKILL.en.md`（本文件中文版）· `README.en.md`。报告与文档语言均可由用户选择，见下方「语言设置」。
> 中英双版内容对等：英文版字符数不少于中文版（v1.4.0 实测 SKILL 14,460 vs 10,722、README 14,505 vs 7,261），
> 章节数与 FAQ 条目一一对应。
> 维护者文档（发布清单 / 触发词归档）保留在 GitHub 仓库的 `references/`，不随平台分发包分发。

办公型 Agent（WorkBuddy、千问办公、百度搭子、天禧AI 等，均经 generic 模式支持；天禧等沙箱默认无关闭通道）装得多不等于能力强。
技能清单（name + description）每一轮对话都进模型上下文——装 54 个技能约等于每轮白烧 5,000+ tokens。

## 1. 适用场景

**触发短语示例**（匹配 `description` 自动挂载或显式调用）：

- 「盘点我装了哪些技能」「技能库太多了帮我看看哪些能关」
- 「哪些技能可以关闭/合并」「技能占了多少上下文」「帮我瘦身一下技能库」
- 「关闭 XX 前先看影响」（`--impact`）
- 「自测一下你的解析器」（`--selftest`）
- 「帮我找找技能装在哪」（`--probe`）
- 「把报告语言换成英文/中文」「语言设置改成 auto」
- 「百度的技能目录在哪」「通用平台怎么扫技能」（`--agent baidu` / `--agent generic --root <dir>`）

**不触发**：写周报、发邮件、代码生成等与技能库治理无关的任务——本技能只做技能库的
盘点、体检与关闭前评估。

## 2. 语言设置（auto / zh / en）

| 选项 | 说明 |
|------|------|
| `auto`（默认） | 自动——Agent 按用户当前对话语言传 `--lang` 决定；未传参时依次回落：环境变量 `SKILL_INV_LANG` → 系统区域语言 → 中文 |
| `zh` | 报告语言固定为中文（随时可用 `--set-lang` / `--lang` 改回） |
| `en` | 报告语言固定为英文（随时可用 `--set-lang` / `--lang` 改回） |

- **查看**：`--show-lang` 打印当前设置、三个选项及说明、切换方式。
- **保存**：`--set-lang auto|zh|en` 写入偏好文件 `~/.workbuddy/skill-inventory.json`（仅此一处，
  仅在你显式运行该命令时写入），切换后立即对后续运行生效；`--set-lang auto` 或删除该文件即恢复默认。
- **单次覆盖**：`--lang zh|en` 只影响本次运行，不改动已保存设置。
- **优先级**：`--lang`（本次）＞ 已保存设置（zh/en）＞ auto 回落链。
- **auto 不是锁定**：它是「用户尚未表达偏好时的回落」，不是强制——随时可用 `--set-lang` 固定为
  zh/en，或用 `--lang` 单次覆盖；不选语言的用户看到中文报告纯属默认，不是被强制。
- **恒定不变**：四档分类标识恒为英文（used / protected / closeable / manual-review），
  `--json` 输出恒为英文键——程序化消费不受语言设置影响。
- **零参数路径**：多数环境无需手写任何路径——直接跑 `python scripts/skill_inventory.py` 即自动
  探测已知平台；陌生宿主用 `--probe` 让工具自己找技能目录，仅在 `--probe` 也找不到时才退回
  `--root <目录>` 手填。

## 3. 输入材料

| 输入 | 必需 | 说明 |
|------|------|------|
| 技能目录 | ✅（已知平台可自动探测） | 每个子目录 = 一个技能（含 `SKILL.md` 即可）；其他平台用 `--root <目录>`，或直接 `--probe` 让它自己找 |
| 用量日志 | 可选 | `--usage-log <路径>`；WorkBuddy 自动探测 `usage-log.json` |
| 反向依赖根 | 可选 | `--refs <路径>`：自动化 / Hook / 路由配置等可能隐式引用技能的文件或目录 |
| 受保护清单 | 可选 | `--protect a,b,c` 或 `--protect-file`；另内置安全/审计类启发式 |

**权限边界**（与脚本头部的机器可读声明一致）：

- **读取**：技能目录、用量日志、自动化/Hook/路由/插件配置
- **写入**（两处目标 + 一份备份工件，均需显式授权）：
  1. `~/.workbuddy/settings.json` 的 `skillOverrides` 键——仅当你显式传 `--apply --yes`（写前自动备份）；
  2. `~/.workbuddy/skill-inventory.json` 的语言偏好——仅当你显式传 `--set-lang`；
  3. 备份工件——执行 `--apply --yes` 时，在 `settings.json` 旁生成 `settings.json.bak.<时间戳>` 安全副本（惰性副本、路径打印给你、不会被回读）。
- **网络**：无　**子进程**：无

纯本地静态分析，零网络依赖、零子进程（沙箱红线天然合规）。

## 4. 输出结果

1. **盘点报告**（默认）：技能总数 / 市场与自建占比 / 清单 token 占用估算 / 逐技能表格，四档分类：
   - **used 有使用记录**：确实用过（可信）。
   - **closeable 可关闭候选**：无使用记录 且 超过 30 天没改过。**仍须人工逐条确认**。
   - **manual-review 需人工确认**：无使用记录但近期改过，或本平台无遥测——别急着关。
   - **protected 受保护**：不会自动建议关闭（本工具自身 / `protected: true` / 安全审计类 / 被引用锁定 / 用户追加）。
2. **影响预览**：每个被引用锁定的技能，列出「关闭将断掉 N 处引用」——`[来源类型] 完整路径` + 命中的技能名；单技能深查 `--impact <名称>`。
3. **重复/跨区提示**：真·多份激活、激活+禁用副本、同名技能。
4. **机器可读 JSON**（`--json`）：四档清单、结构化 `referenced_by`、`telemetry_scope`（`t1-only`/`none`），英文键。

## 5. 执行步骤

规范写法：`python scripts/skill_inventory.py [flags]`。常用 flags 组合：

| flags | 说明 |
|---|---|
| （无参数） | auto 探测平台，完整报告 |
| `--agent workbuddy\|qwen\|baidu` | 指定宿主平台（workbuddy 有用量账本可起草关闭；qwen 有调用记录；baidu 无遥测 → 全库需人工确认） |
| `--agent generic --root <dir>` | 通用档：任意平台/自定义目录 |
| `--agent generic --probe [dirs]` | 陌生宿主让工具**自己找**技能目录（可跟逗号分隔候选路径；也认 `SKILL_INVENTORY_ROOT` 环境变量） |
| `--impact <名称>` | 单技能影响深查（关闭前审阅） |
| `--json` | 机器可读 JSON（顶层键恒英文） |
| `--show-lang` / `--set-lang auto\|zh\|en` | 查看 / 保存语言设置 |
| `--lang zh\|en` | 本次运行语言覆盖（不改已保存设置） |
| `--selftest` | 自测内置 frontmatter 解析器（零依赖，可离线跑） |

流程：`auto 探测平台 → 失败回落 generic 通用档`。通用档优先用 `--probe` 自动找技能目录（找不到再退回
`--root <目录>` 手填）；无用量日志自动降级为「不判任何技能可关闭」；`--refs` 可补充反向依赖扫描根。

## 6. 实际输出长什么样

跑一次 `python scripts/skill_inventory.py` 后，终端会按以下结构打印（节选，WorkBuddy 档、中文）：

```text
ℹ  遥测口径：用量日志只覆盖「显式调用」（T1）。自动挂载 / 定时任务 / Hook / 专家内部
   调用（T2–T6）不计入——「有使用记录」≠「只被显式用过」，「无使用记录」也不等于
   「没在用」（反向依赖扫描只兜住可发现的配置根）。

平台                          WorkBuddy
技能总数                        59    （市场安装 29 / 自建或自改 30）
有使用记录                       27
受保护（不关）                     6
可关闭候选                       19    （仍须人工逐条确认）
需人工确认                        7
                            19665 字符  ≈ 6912 tokens / 每轮对话

目录                                      行      KB      来源        最后改    用        最后用
----------------------------------------------------------------------------------------
agnes-ai                            ⚠   537    23.9      自建 2026-10-09   0          —
ai-weekly                               168  2734.0      自建 2026-10-09  1 2026-10-05
skill-publish-gate                      211   324.7      自建 2026-10-09  2 2026-10-09
skill-inventory                     🔒    91    52.1      自建 2026-09-28   0          —
office-token-booster                    375   653.2      自建 2026-09-25  4 2026-08-21
skill-creator                           356   52.6      市场 2026-06-30  17 2026-08-27

🔻 可关闭候选：无使用记录 且 超过 30 天没改过（19 个）
   ⚠ 仅建议，未经你显式确认不得关闭；先确认无关键词/专家触发依赖。
  bug-fixing                                667 行   2026-08-04
  log-analyzer                              501 行   2026-08-04
  code-fix                                  262 行   2026-08-04

🔒 受保护（不关）：6 个
  skill-inventory                     （本工具自身，永不进候选）
  skill-clean-audit                   （安全/审计类启发式命中）
  security-audit                      （名称含 security）
  ⋯
```

各图例含义：`⚠` = 近期改过但无使用记录（进「需人工确认」）；`🔒` = 受保护（永不进候选）；
`—` = 无使用记录；行/KB = 该技能目录的 `SKILL.md` 行数与体积。

**机器可读（`--json`）**：加 `--json` 时输出一个 JSON 对象，顶层键恒为英文（不受语言设置影响）：

```json
{
  "agent": "workbuddy",
  "can_close": true,
  "rows": [
    { "name": "office-token-booster", "lines": 375, "kb": 653.2,
      "from_market": false, "last_modified": "2026-09-25", "last_used": "2026-08-21",
      "uses": 4, "protected": false, "locked": false, "referenced_by": [] }
  ],
  "buckets": { "protected": [ "skill-inventory" ], "keep": [ "⋯" ],
               "cleanup": [ "bug-fixing" ], "review": [ "⋯" ] },
  "telemetry_gap": false,
  "telemetry_scope": "t1-only",
  "cannot_close": false
}
```

`buckets` 四档：`protected`（受保护，不关）/ `keep`（有使用记录，保留）/
`cleanup`（可关闭候选，仍须人工确认）/ `review`（需人工确认）。`telemetry_gap=true` 时表示
无遥测、报告不含可关闭项。

**自测（`--selftest`）**：校验内置回退解析器与 PyYAML 的块标量语义是否一致，离线可跑：

```text
[selftest] frontmatter block-scalar semantics 块标量语义
  用例 8 通过 / 0 失败（对照源：PyYAML）
  [OK] SKILL.md 回退解析：version=1.5.1、description 1390 字符
```

## 7. 数据源优先级

1. **平台用量日志**（最高置信）：只覆盖「显式调用」（T1）；自动挂载 / 定时任务 / Hook / 专家内部调用（T2–T6）在日志里不可见——报告会常显这一口径。
2. **反向依赖扫描**（兜底盲区）：扫描自动化 / Hook / 路由状态 / 插件清单等配置里的技能引用，凡被引用即锁定为受保护。
3. **最后修改时间**（最低置信）：仅当无遥测时作参考，**不可单独作为关闭依据**。
4. **用户确认**（最终裁决）：任何「可关闭候选」动刀前必须经用户逐条确认。

## 8. 用户确认点

行为契约全文见 `README.md §🔒 行为契约`（8 条，先读再信任）。此处只列**关闭前必须确认**的
三点（SKILL 侧技术要点，不与 README 重复）：

- **本工具不会自行关闭任何技能。** 关闭写路径需你显式授权——在可关平台上 `--overrides
  --apply --yes` 会先自动备份 `settings.json` 再合并进 `skillOverrides`；缺 `--yes` 仅 dry-run；
  不可关平台直接拒绝 `--apply`。
- **优先引导宿主自带开关**（`/skills` 菜单、客户端启用开关）；通用档无关闭通道，只给候选清单。
- **可关闭候选动刀前先看影响预览**（`--impact <名称>`），确认无关键词触发器 / 专家组件 /
  自动化依赖（`referenced_by` 为空）。

## 9. 风险边界

完整行为契约（默认只读、两处受控写 + 一份备份工件、无自动驻留、受保护永不进候选、遥测缺口
不判死、反向依赖扫描）见 `README.md §🔒 行为契约`。此处只列**技术边界**（SKILL 侧，不与
README 重复全文）：

- **写路径**（均需显式授权并在输出中标注）：① `--overrides --apply --yes` 写
  `~/.workbuddy/settings.json` 的 `skillOverrides`（先备份）；② `--set-lang` 写语言偏好文件
  `~/.workbuddy/skill-inventory.json`（单键）；③ `--apply --yes` 生成 `settings.json.bak.<时间戳>`
  惰性备份副本（路径打印、不回读、可手动删除）。
- **读边界**：技能目录、用量日志、自动化/Hook/路由/插件配置；**网络无、子进程无**。
- **遥测口径**：用量日志只覆盖 T1 显式调用；T2–T6（自动挂载/定时任务/Hook/专家内部）无痕，
  靠反向依赖扫描 + 用户确认双层兜底。
- **重复检测是近似比对**（名称/描述/体积），非语义级去重；仅覆盖可发现配置根。

---

## 10. 应避免的错误用法

以下 6 类是真实使用中最常踩的坑，本工具**设计上不鼓励**这些做法：

| # | 错误做法 | 为什么错 | 正确做法 |
|---|---|---|---|
| 1 | **直接删技能目录** 来「关闭」一个技能 | 绕过备份工件与受保护锁定检测，可能删掉被自动化/Hook/触发器引用的技能且无回滚 | 让工具输出 `--overrides` 草稿，按报告里打印的备份副本路径走宿主 `/skills` 菜单或手动移除，保留可回滚 |
| 2 | **不看影响预览就关闭** | 该技能可能仍被关键词触发器 / 专家 / 自动化隐式调用，日志无痕 → 误杀 | 关闭前先跑 `--impact <名称>`，确认 `referenced_by` 为空再动手 |
| 3 | **把「无使用记录」当「没用」** | 无记录只代表 T1 显式调用没命中，T2 自动挂载 / T3 关键词路由 / T4 定时任务 / T5 Hook / T6 专家内部调用在日志里完全无痕 | 看「可关闭候选」+「需人工确认」两档，任何候选都经用户逐条确认后才关闭 |
| 4 | **在不可关平台期待 `--apply` 生效** | `can_close=False` 的平台（千问 / 百度 / 通用档）没有程序化关闭通道，`--apply` 直接被拒绝 | 用宿主自带的启用/禁用开关或客户端手动移除；工具只给盘点与候选清单 |
| 5 | **把 `--protect` 当万能护栏** | `--protect` 只是把指定技能追加进受保护桶，不改变「反向依赖扫描只兜可发现配置根」的事实 | 配合 `--refs` 指明额外的引用定义目录（自动化/Hook/路由），双重兜底 |
| 6 | **`--root` 指向父目录** 导致误纳无关目录 | 通用档 `--root` 会把该目录下的**所有**子目录当技能扫，混进不相关的文件夹 | 把 `--root` 精确到「技能根目录」（每个子目录 = 一个技能）；陌生宿主优先用 `--probe` 让工具自己找 |

> 设计取向：**宁可少报，不可误杀。** 工具永远不会替你决定「可以关闭」——它只输出候选与影响，
> 每一笔写操作都需要你显式授权并打印备份路径。

---

## 11. 常见问题（FAQ）

**Q1：为什么我的技能被标成「需人工确认」，而不是「可关闭候选」？**
只有「无使用记录」**且**「超过 30 天没改过」的技能才会进可关闭候选。出现「需人工确认」有四种原因：
① 无遥测（用量日志缺失或读不了）——本工具宁可少报也不误杀；② 最近 30 天内被改过；③ 所属平台没有
程序化关闭通道（如千问、通用档）；④ 命中受保护规则。用 `--usage-log <路径>` 补上日志、把确认过的
技能用 `--protect` 追加保护，能把噪声压下去。

**Q2：「有使用记录」就等于「只被显式用过」吗？**
不等于。用量日志只记录**显式调用**（T1）。自动挂载（T2）、关键词路由（T3）、定时任务（T4）、
钩子（T5）、专家/连接器内部调用（T6）在日志里完全无痕。所以「有记录」不代表只被显式用过，
「无记录」也不等于没用——后者才是需要人工确认的原因。

**Q3：报告说「遥测缺口」，我该怎么补？**
这表示用量日志读不到，报告只能基于「最后修改时间」，**不会**给出可关闭项。两种补法：① 该平台有日志
时用 `--usage-log <路径>` 指定（如 `~/.qwenworkcn/skill-usage.json`）；② 没有日志就靠反向依赖扫描
（`--refs` 指定自动化 / Hook / 配置根）+ 人工确认兜底，此时工具会一直保持保守输出。

**Q4：会不会误关被自动任务或关键词触发器调用的技能？**
护栏有三层：① 反向依赖扫描发现被自动化 / Hook / 路由 / 插件引用即锁定进受保护桶；② 安全审计类关键词
与本工具自身永不进候选；③ 任何候选都要你逐条确认。**但护栏不能穷尽**——T2 自动挂载与描述性关键词
引用扫不到，所以关闭前请先看影响预览：`--impact <名称>`。

**Q5：关闭到底写入了什么？能不能撤销？**
只写一处：`~/.workbuddy/settings.json` 的 `skillOverrides` 键（把候选标成 `off`）。落笔前自动生成
`settings.json.bak.<时间戳>` 备份副本，路径打印在输出里，可用 `os.replace` 原子替换，不会留下半截配置。
撤销有三条路：把备份文件改回去、在宿主 `/skills` 菜单改回、或直接删掉 `skillOverrides` 里对应条目。

**Q6：为什么千问 / 百度 / 通用档不给我「关闭」动作？**
不同宿主的关闭能力不同：`can_close=False` 的平台没有「关闭单个技能」的程序化通道，本工具按能力感知
分叉——只给盘点与候选清单，把动刀留给宿主开关或手动移除，避免给出你根本执行不了的建议。

**Q7：报告里的「疑似重复」准吗？**
是**近似**比对（名称 / 描述 / 体积），不是语义级去重：会把同名的市场版与自建版标成疑似重复，也会漏掉
描述完全不同但功能重叠的。拿它当线索，别当结论。

**Q8：报错里的 `[E-LOG]` / `[E-CONF]` 是什么意思？**
稳定的错误码，便于检索与反馈：
| 码 | 含义 | 通常怎么办 |
|----|------|-----------|
| `E-LOG` | 用量日志缺失或读不了 | `--usage-log <路径>` 指定日志；或先用 `--protect` 保护关键技能 |
| `E-ROOT` | 找不到技能目录 | 检查路径，或用 `--root <目录>` 显式指定 |
| `E-PLATFORM` | `--agent` 值不认识 | 用 workbuddy / qwen / baidu / generic / auto 之一 |
| `E-NOCLOSE` | 该宿主没有程序化关闭通道 | 改用宿主自带开关或手动移除 |
| `E-CONF` | settings.json 读写失败 | 本次未做任何修改，检查文件是否被其他进程占用（读会重试 2 次） |
| `E-READ` | 某个技能目录读不到 | 已跳过该目录，其余结果照常；检查该目录权限 |

**Q9：报告没列出「可关闭候选」，是我的技能没问题吗？**
不一定——很可能没有遥测（Q1/Q3）。工具的设计取向是「宁可少报，不可误杀」：看不到使用记录时它不会
替你做关闭决定，但会明确告诉你缺口在哪。

---

## 附：平台档位一览

| 平台 | 探测 | 用量账本 | 程序化关闭 | 本工具行为 |
|------|---------|---------|-----------|-----------|
| WorkBuddy | `~/.workbuddy/skills` 自动 | ✅ `usage-log.json` | ✅ `skillOverrides`（需 `--apply --yes`，先备份） | 盘点 + 可关闭草稿 |
| 千问办公 QwenWork | `~/.qwenworkcn/skills` 自动 | ✅ `skill-usage.json` | 经连接器/UI（不代执行） | 盘点 + 调用记录 + 客户端确认清单 |
| 百度搭子 Baidu DuMate | 多根自动探测 | ❌ | 经 UI/连接器（不代执行） | 盘点 + 关闭指引；无遥测全库需人工确认 |
| 通用档 Generic（含天禧等沙箱） | `--probe` 自动找 / `--root` 手填 | 默认无 | ❌ 无关闭通道 | 盘点 + 建议；全库需人工确认 |

> 原则：**能力感知**——平台能不能「程序化关闭」决定工具产出什么。不可关平台不产出关闭动作，
> 只做体检与候选清单，把「动刀」留给宿主与用户。
>
> **零参数路径**：通用档优先 `--probe` 让工具自己找技能目录，多数环境无需手写路径；
> 仅在探测失败时才退回 `--root <目录>` 手填。
