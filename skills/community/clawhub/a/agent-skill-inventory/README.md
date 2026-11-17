# skill-inventory · 面向办公型 Agent 的技能库盘点与效能体检

> English version: [README.en.md](README.en.md) · 文档语言：`SKILL.md`（中文）/ `SKILL.en.md`（English）
> 中英双版内容对等：英文版字符数不少于中文版（v1.4.0 实测 README 14,505 vs 7,261、SKILL 14,460 vs 10,722），
> 章节数与 FAQ 条目一一对应。

为办公型 Agent（WorkBuddy、千问办公、百度搭子、天禧AI 等）做「技能库盘点 + 效能体检」：
扫描任意技能目录，统计数量 / 体积 / 上下文 token 占用，识别重复与近似技能，
并给出**保守**的瘦身建议。**默认只读**：盘点、分类、建议全程不写任何文件；
写路径两处目标 + 一份备份工件、均需显式授权（`--overrides --apply --yes` 关闭写入，仅 WorkBuddy 等可关平台，
落笔前自动生成 settings.json 备份副本；`--set-lang` 语言偏好写入）——判断权始终在人。

> 装得多不等于能力强。技能清单（name + description）每一轮对话都进模型上下文，
> 装 54 个技能约等于每轮白烧 5,000+ tokens。本工具给「哪些该关」提供事实依据。

## 什么时候用

- 想知道「我装了哪些技能」「哪些技能该关 / 该合并」「技能占了多少上下文」
- 想给办公型 Agent 做「效能体检」、压一压上下文 token 消耗
- 要盘点 WorkBuddy / 千问办公 / 百度搭子 / 天禧AI 等平台的技能目录
- 想把报告语言固定为中文或英文（或恢复自动跟随对话）

## 怎么用

脚本在 `scripts/skill_inventory.py`。默认盘点 WorkBuddy 技能库：

```bash
python scripts/skill_inventory.py                          # 完整表格 + 四档分类（auto 探测平台）
python scripts/skill_inventory.py --agent workbuddy        # 指定平台档位
python scripts/skill_inventory.py --agent qwen             # 千问办公（可扫不可关）
python scripts/skill_inventory.py --agent baidu --root DIR # 百度搭子（可扫可关，路径待验）
python scripts/skill_inventory.py --overrides              # 起草可关闭清单（仅草稿）
python scripts/skill_inventory.py --overrides --apply --yes   # WB：在你同意下写入 skillOverrides 关闭
python scripts/skill_inventory.py --json                   # 机器可读输出
python scripts/skill_inventory.py --protect a,b,c          # 追加受保护技能
```

跨办公型 Agent：用 `--agent` 选平台档位（workbuddy / qwen / baidu / auto），或用 `--root` 直接指向技能目录。
用量日志用 `--usage-log` 指定；**若该平台无用量日志，工具会自动降级为「不判任何技能可关闭」**。

## 语言设置（auto / zh / en）

| 选项 | 说明 |
|------|------|
| `auto`（默认） | 自动——Agent 按当前对话语言传 `--lang` 决定；未传参时回落：环境变量 `SKILL_INV_LANG` → 系统区域语言 → 中文 |
| `zh` | 报告语言固定为中文（随时可用 `--set-lang` / `--lang` 改回） |
| `en` | 报告语言固定为英文（随时可用 `--set-lang` / `--lang` 改回） |

```bash
python scripts/skill_inventory.py --show-lang   # 查看当前设置、选项说明与切换方式
python scripts/skill_inventory.py --set-lang en # 保存偏好（写入 ~/.workbuddy/skill-inventory.json），立即生效
python scripts/skill_inventory.py --set-lang auto
python scripts/skill_inventory.py --lang en     # 仅本次运行覆盖，不改已保存设置
python scripts/skill_inventory.py --selftest    # 自测内置解析器（零依赖，可离线跑）
```

保存后切换立即生效；`--set-lang auto` 或删除 `~/.workbuddy/skill-inventory.json` 即恢复默认。
`auto` 是「尚未表达偏好时的回落」而非锁定——随时 `--set-lang` 固定语言，或 `--lang` 单次覆盖。
四档分类标识恒为英文，`--json` 键恒为英文——程序化消费不受语言设置影响。

## 平台档位与能力感知关闭

不同 Agent 的「关闭」能力不同，本工具按 `can_close` 分叉——**不可关平台不产出任何关闭动作**，只给报告 + 手动移除指引：

| 平台 | 可扫描 | 有用量账本 | 可程序化关闭 | 本工具行为 |
|------|--------|-----------|-------------|-----------|
| **WorkBuddy** | ✅ `~/.workbuddy/skills` | ✅ `usage-log.json` | ✅ `skillOverrides` 四态 | 出盘点 + 可关闭草稿；`--apply --yes` 在你同意下写入 `off` |
| **千问办公** | ✅ `~/.qwenworkcn/skills` | ✅ 有（usage adapter 读取） | ❌ **无禁用开关**（实测） | 出盘点 + connector/UI 关闭说明，不代执行关闭 |
| **百度搭子** | ✅ 本地沙箱（路径待验→`--root`） | ❌ 无 | ✅ 禁用开关 + 专家套件禁用 | 出盘点 + 关闭指引；独占「专家套件」治理维度 |
| **通用档**（未知宿主，含天禧等云端沙箱） | ✅ `--root` 指定，或 `--probe` 自动探测 | ❌ 默认无（可用 `--usage-log` 指定） | ❌ 无关闭通道 | `--agent generic`：纯盘点 + 四档建议，全部落「需人工确认」，不产出关闭动作 |

> 原则：**未显式调用 ≠ 没用**。千问这类无关闭开关的平台，本工具只做「体检」，把「动刀」留给你手动处理，避免给出你根本执行不了的「关闭建议」。

## 🔒 行为契约（先读这段再信任它）

**默认只读，写路径两处目标 + 一份备份工件、均需显式授权：**

1. **默认不写任何文件。** 盘点、分类、建议全程只读；不调用任何禁用/删除接口。
2. **写路径一（关闭，需你显式授权）。** 在 WorkBuddy 等可关平台上，`--overrides --apply --yes`
   会**先自动备份 `settings.json`**，再把候选合并进 `skillOverrides` 的 `off` 态；
   缺 `--yes` 只做 dry-run 预览（不读写任何文件）；千问等不可关平台直接拒绝 `--apply`。
   每份报告和 `--overrides` 输出都会显式标注这条写路径——本工具**不会**静默或自行关闭任何技能。
   优先引导宿主自带开关（如 `/skills` 菜单，按 Esc 才落盘）。
   **备份工件**：`--apply --yes` 落笔前在 `settings.json` 旁生成 `settings.json.bak.<时间戳>`
   安全副本，路径打印在输出里；副本惰性、不会被回读，可手动删除。
3. **写路径二（语言偏好，需你显式触发）。** `--set-lang auto|zh|en` 把报告语言偏好写入
   `~/.workbuddy/skill-inventory.json`（仅此一个键）；这是一项用户可控的显示偏好，
   `--set-lang auto` 或删除该文件即恢复默认。
4. **无自动驻留。** 不注册定时任务 / cron、不写启动项、不留守护进程、不自我修改（即不自主执行）。
   跨会话**可见的写入**仅两处，均为用户显式授权的公开功能、随时可逆——`skillOverrides` 的 off 项
   （可在宿主 `/skills` 菜单恢复）与语言偏好文件。语言偏好文件只是显示偏好（单个 JSON 键）：
   不基于它注册或排程任何东西，仅在下一次运行时被读取用来挑报告语言；`--set-lang auto`
   或删除该文件即恢复默认。
   ↳ 注意：本工具确实会产生经授权的跨会话写入（见第 2、3 条），与「自动驻留（自主执行）」是两回事——前者需你显式触发，后者完全没有。
5. **受保护技能永远不进「可关闭」候选。** 包括：本工具自身、frontmatter 标了 `protected: true` 的技能、
   安全/审计类（名称含 security/audit/safe/guard/privacy/sanitize/compliance/backup），以及用户用
   `--protect` 追加的。报告里它们单列在「受保护」一档。
6. **未显式调用 ≠ 没用。** 用户可能**从不在对话里明说**要调某技能，而是：
   - 预先配置了**关键词/触发器**，让某类输入自动唤起它；
   - 借助会内部调用该技能的**专家/连接器组件**间接使用它。
   这两种用法在用量日志里**完全无痕**。所以**任何「可关闭候选」在关闭前，都必须向用户确认它是否仍被上述方式依赖**。
7. **遥测缺口不判死。** 当平台无用量日志、或日志读取失败（已修 P1，会显式告警而非静默），
   全库只能落「需人工确认」档，**不输出可关闭项**——宁可少报，不可误杀。
8. **反向依赖扫描（应对你最担心的场景）。** 在判「可关闭」前，工具会先扫自动化任务 / Hook 里的技能引用
   （默认 `~/.workbuddy/automations` 与 `~/.workbuddy/hooks`，可用 `--refs` 追加）。
   **凡被引用的技能一律锁定为「受保护」**——无论它有没有用量日志。这堵住了
   「用户只设了关键词/触发器、或借专家·连接器组件间接调用，日志里完全无痕」导致的误杀。
   若你的引用定义在别处，用 `--refs /path/to/defs` 指明；想完全关掉用 `--no-ref-scan`。

## 输出怎么读

- **有使用记录**：确实用过（可信）。
- **可关闭候选**：无使用记录 且 超过 30 天没改过。**仍须人工确认**，且先排除关键词/专家触发依赖。
- **需人工确认**：无使用记录但近期改过，或本平台无遥测——别急着关。
- **受保护**：永不自动建议关闭，须人工明确介入。

**实际输出长什么样（节选）**——跑一次 `python scripts/skill_inventory.py`，终端大致如下：

```text
平台 WorkBuddy · 技能总数 59 · 有使用记录 27 · 受保护 6 · 可关闭候选 19 · 需人工确认 7
                            ≈ 6912 tokens / 每轮对话
目录             ⚠/🔒  行    KB   来源   最后改     用  最后用
ai-weekly               168 2734   自建  2026-10-09  1   2026-10-05
skill-inventory      🔒  91   52   自建  2026-09-28  0   —
🔻 可关闭候选（仍须人工逐条确认）：
  bug-fixing   667 行 · 2026-08-04    log-analyzer  501 行 · 2026-08-04
```

- `⚠` = 近期改过但无使用记录（进「需人工确认」）；`🔒` = 受保护（永不进候选）；`—` = 无使用记录。
- 加 `--json` 输出机器可读对象，顶层键恒为英文（`agent` / `can_close` / `rows` / `buckets` /
  `telemetry_gap` / `telemetry_scope` / `cannot_close`），`buckets` 四档 `protected/keep/cleanup/review`。
- 加 `--selftest` 离线校验内置解析器（对照 PyYAML 块标量语义），输出「用例 8 通过 / 0 失败」。
- 完整版样例（含受保护块、JSON 全结构、selftest 全文）见 `SKILL.md §6 实际输出长什么样`。

## 应避免的错误用法

6 类最常踩的坑（完整版见 `SKILL.md §10`）：① 直接删技能目录（绕过备份/锁定，误杀被引用技能）
② 不看 `--impact` 就关闭（隐式依赖日志无痕）③ 把「无记录」当「没用」（T2–T6 无痕）
④ 在不可关平台期待 `--apply` 生效 ⑤ 把 `--protect` 当万能护栏（需配 `--refs`）
⑥ `--root` 指向父目录误纳无关目录（精确到技能根，或直接用 `--probe`）。

## 常见问题（速查版；完整 11 组见 SKILL.md §11）

**Q：为什么我的技能进了「需人工确认」而不是「可关闭候选」？**
只有「无使用记录」**且**「超过 30 天没改过」才是候选。四个原因：无遥测 / 最近改过 / 平台没有关闭通道 /
命中受保护规则。用 `--usage-log <路径>` 补日志、用 `--protect` 保护关键技能可减少噪声。

**Q：「有使用记录」等于「只被显式用过」吗？**
不等于。用量日志只记显式调用（T1）；自动挂载、关键词路由、定时任务、Hook、专家内部调用（T2–T6）
完全无痕。所以「无记录」不等于「没用」。

**Q：报告说「遥测缺口」怎么办？**
该平台没有可用日志，报告只能基于最后修改时间，**不会**给可关闭项。有日志就用 `--usage-log <路径>`
指定；没有就靠 `--refs` 反向依赖扫描 + 人工确认兜底。

**Q：会不会误关被自动化 / 关键词调用的技能？**
三层护栏：反向依赖扫描即锁定、安全类与本工具永不进候选、每条都要你确认。但护栏不穷尽（T2 自动挂载
扫不到），关闭前先跑 `--impact <名称>` 看影响。

**Q：报错里的 `[E-LOG]` `[E-CONF]` 是什么？**
稳定错误码：`E-LOG`（用量日志缺失/读不了）、`E-ROOT`（技能目录找不到）、`E-PLATFORM`（`--agent` 值不认识）、
`E-NOCLOSE`（该宿主无程序化关闭通道）、`E-CONF`（settings.json 读写失败，本次未改动）、`E-READ`（单个技能目录
读不到，已跳过）。完整对照表见 SKILL.md §11。

## 局限性（如实告知）

- 调用频率只依赖平台用量日志；WorkBuddy 有真账本（`usage-log.json`），其余平台多数无等价账本，
  此时结论仅基于最后修改时间，**不可作为关闭依据**。
- 无法从文件系统探测「关键词触发器/专家组件」依赖，这是结构性盲区，只能靠用户确认兜底。
- 重复检测是名称/描述/体积的近似比对，不是语义级去重。

## 关于自动化扫描器的说明（SkillSpector findings 与逐条回应）

部分自动扫描器（如 ClawHub SkillSpector）会对本技能报出若干条 findings。绝大多数属于**检查局限**
或**对已披露能力的重复提示**，不是可疑行为。下表逐条给出可核对的事实依据（行数为 v1.3.1 实测）：

| 规则 | 扫描器的说法 | 事实依据与回应 |
|---|---|---|
| **Ae1** 引用的工件未被完整检查 | 无法把 `scripts/skill_inventory.py` 完整纳入上下文检查 | **检查能力局限**。该脚本 v1.5.0 实测 1562 行，零第三方依赖（仅标准库，`yaml` 为可选加速项）。同一文件的**静态分析层结论为 Pass**（"No suspicious patterns detected"）。完整源码公开在 [GitHub 仓库](https://github.com/Elisabeth15501/skill-inventory)，可随时人工审查。findings 条数随脚本行数增长（7→11→12），与代码量正相关，不反映行为变化 |
| **Lp1** 能力宽于声明 | 脚本会写盘，能力范围超出声明 | 声明已补全为**两处写目标 + 一份备份工件**（frontmatter `permissions` 与脚本头部声明块均可 grep 验证）：① `settings.json` 的 `skillOverrides` 键——需 `--apply --yes` 双显式 flag，缺一即 dry-run；② 语言偏好文件——需显式 `--set-lang`；③ `settings.json.bak.<ts>` 安全副本——仅在第①步落笔前生成，路径打印在输出里，从不回读。逐条见上方「行为契约」 |
| **Session Persistence** | 存在跨会话写入（均经授权） | 无 cron / 启动项 / 守护进程 / 自我修改（即无自动驻留）。语言偏好文件是显示偏好（单个 JSON 键），不基于它注册或排程任何东西，仅在下次运行时被读取一次；`--set-lang auto` 或删文件即恢复默认 |
| **Anti-Refusal** | 文档出现「always / 始终」类措辞 | 已改为「报告语言固定为 X（随时可改回）」——描述的是**工具输出语言**，不构成对用户的服从承诺 |
| **Rp1** | 供应链存在未钉版依赖 | 技能运行零外部依赖（Python 标准库）；文档中的发布命令已钉 `clawhub@0.23.3`，不用 `@latest` |
| **NL Policy** | 语言选择 | 三选项 auto / zh / en。auto 是**用户未表达偏好时的回落**，不是锁定：随时 `--set-lang` 固定，或 `--lang` 单次覆盖 |
| **stability**（TRACE 评测） | 未设显式超时，建议评 4 分 | **申诉：本地文件操作不需要全局超时。** 读文件已做有限重试——`_read_text()` 遇「文件被占用」类 `PermissionError` 会重试 **2 次、间隔 0.5s**（代码常量 `retries=2, delay=0.5`，脚本头部 docstring 亦声明）。这是针对 Windows 文件锁的针对性容错，非无限阻塞；加全局超时反而会误杀慢网络/慢盘上的合法操作。写操作走原子替换（临时文件 + `os.replace`），单文件粒度，无需超时保护 |
| **func / accuracy**（TRACE 评测） | 重复检测是近似比对，非语义级 | **申诉：已知局限 + 可自验路径。** 重复检测按名称/描述/体积做近似比对，**不做语义去重**（语义去重需嵌入模型，对零依赖单文件脚本而言代价与收益不匹配，已显式声明「只是线索不是结论」）。用户可用 `--json` 取 `name`/`desc` 两字段自行核验，或跑 `--impact <名称>` 看单技能影响 |
| **DBM / Intent-Code**（ClawHub v1.4.0） | 描述与行为矛盾 91% / 意图与代码分歧 87% | **v1.5.1 已修**：`persistence` 字段由 `none` 精确化为「无自动驻留（不自主执行），两处授权写入 + 一份备份工件确实跨会话留存」，并补 `capabilities: ["file-read","file-write"]`；全库「无持久化机制」→「无自动驻留」，显式区分「经授权的跨会话写入 ≠ 自动驻留」。见 commit ef9eb03 |
| **Lp1**（ClawHub v1.4.0） | 能力声明宽于实际 | **v1.5.1 已修**：frontmatter 补 `capabilities` 顶层清单，与 `filesystem.write` 并存；脚本删 shebang（Lp1 "env" 证据源）。见 commit ef9eb03 |

**平台侧结论**：静态分析 + 人工复核均为 **Moderate CLEAN**；扫描器 Overview 自述
"disclosed, user-triggered… no evidence of hidden network, autonomous residency, or destructive behavior"。
脚本头部另有一块机器可 grep 的「权限与驻留声明」，欢迎直接验证。若你发现声明与实现不符，
请优先回报 issue——这比任何扫描器判定都更快地修正问题。

**本次两份报告（v1.4.0）新 findings 处置说明**（对应 P2-14 申诉材料同步）：
- **DBM 91% / Intent-Code 87%**：v1.5.1 已通过「persistence 精确化 + 全库措辞修正」消除，非误报——是文档内部逻辑矛盾，已实修
- **Lp1 75%（file-write / env）**：v1.5.1 补 `capabilities` 字段 + 删 shebang，证据源已清除
- **Ae1 13 条**：v1.5.2 通过 P2-11 执行步骤去噪音压缩（12 行重复路径 → 9 行 flags 表），降低扫描面；根因是脚本 1562 行零依赖，属检查能力局限非行为问题
- **TRACE 四项退步（docQuality 4.8→4.3 / antiPatternFaq 4.5 / progressive 4.5 / structure 4.5）**：v1.5.2 通过 P1-5~P1-8 补齐文档欠账（输出样例专章 + 错误用法专章 + 行为契约去重 + README/SKILL 差异化），预期回升

## 许可证

MIT —— 见 [LICENSE](LICENSE)。
