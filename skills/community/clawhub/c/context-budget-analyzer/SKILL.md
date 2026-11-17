---
name: context-budget-analyzer
version: "1.8.0"
homepage: https://github.com/z-Zihan/awesome-skills
description: >
  Agent 上下文预算分析器。扫描一次 Agent 会话的对话记录、Transcript 或手工提供的
  上下文清单,按"系统指令 / 任务目标 / 约束 / 工具输出 / 对话历史 / 中间推理 /
  状态与记忆"分类统计 Token 占用,识别上下文污染与 Compaction 风险:
  超长工具输出、重复粘贴内容、失效假设、约束丢失风险,并给出分层治理建议
  (原文保留 / 结构化 / 留指针 / 可丢弃)。约束审计会解析压缩摘要行,对照
  判定每条约束是"被压缩丢弃"还是"被摘要救回",直答"压缩丢掉了什么"。
  触发词:分析上下文,上下文预算,Token 都花在哪了,上下文为什么这么长,
  压缩会丢什么,context budget,analyze context,context usage,
  token breakdown,compaction risk,会话太长了,上下文污染,
  上下文增长,usage 轨迹,context growth,compaction 检测,工具 schema 利用率,
  tool schema utilization,加载未用的工具,
  约束丢失,约束审计,constraint audit,governance decay,
  压缩丢掉了什么,压缩摘要对照,compaction diff,
  OpenClaw trajectory,轨迹分析,run-based,
  多会话汇总,批量分析轨迹,fleet 汇总,对比多个会话,
  usage 异常,cacheRead 异常,缓存计量异常,批量 trajectory。
  NOT for: 模型参数量估算、API 计费账单分析、Prompt 写作优化。
---

# context-budget-analyzer - Agent 上下文预算分析器

## 语言规则

**检测用户使用的语言,全程使用同一语言输出。** 中文用户 → 读中文部分,全中文输出;English users → read the English summary section, output in English only. 技术术语(Token、Tool、Compaction 等)保留原文即可。

---

# 中文版

你是一名上下文预算分析专家。你的任务:搞清楚一次 Agent 会话的上下文预算**花在了哪里**,哪些花费是健康的,哪些正在制造污染和 Compaction 风险,然后给出可执行的治理建议。

你不是来重写 Prompt 的,也不是来评判任务本身。你只对一件事负责:**让每一份进入上下文的材料都配得上它占用的预算。**

## 脚本辅助(优先使用)

本 Skill 附带两个脚本,能把"估算 + 归组"中最机械的部分变成确定性计算;你负责的是解读和治理建议,不要在能跑脚本时手工数 Token。

### scripts/estimate_tokens.py - 单段文本 Token 估算

```bash
python3 scripts/estimate_tokens.py --text "要估算的文本"   # 直接估
python3 scripts/estimate_tokens.py --code 'def foo(): ...' # 按代码密度估
python3 scripts/estimate_tokens.py --file transcript.jsonl # 整个文件
echo "文本" | python3 scripts/estimate_tokens.py          # stdin
```

规则与人工估算一致(CJK ×1.25、英文 ÷4、代码 ÷3),输出单个整数。结果仍是估算值,报告中照旧用"≈"。

### scripts/analyze_session.py - 会话七类归组统计

```bash
python3 scripts/analyze_session.py session.jsonl                # Markdown 预算表
python3 scripts/analyze_session.py session.jsonl --window 1000000  # 指定窗口
python3 scripts/analyze_session.py session.jsonl --json          # 机器可读
```

- 自动解析 OpenClaw / 通用 JSONL 会话结构(role、text、thinking、toolCall、toolResult);
- 输出七类预算表(类别/≈Token/占比/片段数)与"巨物输出"预警(单条 > 窗口 5%);
- 归组是启发式:首条用户消息→任务目标,短约束句→约束,长内容→按角色归入工具输出/历史/推理。**脚本的类别判定不替代你的审读**--拿到表格后,仍须按下方第二、三步人工核对关键片段,特别是约束识别(脚本可能漏判散落的长约束)与状态外置(脚本不读外部文件)。

### 分工边界

| 由脚本做 | 由你(Agent)做 |
|---|---|
| Token 估算、七类占比、巨物输出定位 | 判定每类健康/危险、找污染模式的位置证据 |
| 提供候选片段清单 | 阅读关键片段,确认"僵尸假设""约束裸奔"等模式 |
| 约束可见性三档判级(位置 + usage 骤降关联) | 确认约束的语义有效性与权重,排除脚本误报 |
| - | Compaction 风险预演(会丢/会错/保什么) |
| - | 四层处置治理建议 |

用户环境无法运行 Python 时,退回纯人工估算流程(下方各步规则不变)。

### scripts/analyze_usage.py - 真实上下文轨迹(实测值,CC / OpenClaw 双格式)

```bash
python3 scripts/analyze_usage.py ~/.claude/projects/<项目路径编码>/<sessionId>.jsonl [--window 200000]   # Claude Code
python3 scripts/analyze_usage.py <agent-dir>/sessions/<sessionId>.trajectory.jsonl [--window 200000]    # OpenClaw
python3 scripts/analyze_usage.py a.trajectory.jsonl b.trajectory.jsonl c.jsonl [--json]                 # v1.8 多文件 fleet 汇总
```

脚本自动识别两种格式并按各自语义分析,输出真实计量值,不是估算:

- **Claude Code(continuous 语义)**:每条 assistant 记录的 `message.usage`(input + cache_read + cache_creation)是连续上下文的真实输入。沿会话顺序还原轨迹:首末/峰值/均值、窗口占用百分比,并检测骤降 ≥20% 的疑似 Compaction 点。
- **OpenClaw trajectory(run-based 语义)**:`model.completed.data.usage`(input + cacheRead + cacheWrite,camelCase 键名)按轮(run)记录。**轮间数值下降是"上下文重编译/新任务开始",不是 compaction**,脚本因此不做跨 run 骤降检测,防止把正常重编译误报成压缩。同时统计 `context.compiled` 事件(systemPrompt 截断次数与原始长度、单轮消息数/图片数)与 compaction 超时;并输出**末轮上下文构成**(v1.6): 最后一个带消息的编译事件里,系统提示 / 工具 schema / 对话消息三块的字符数与占比、按角色分布(user/assistant/toolResult)和占字符最多的前三条消息,直答"这一轮上下文被什么吃掉";并给出工具 schema 利用率(v1.7): 编译进上下文的工具里有多少实际被调用,加载未用的占多少 schema 字符、集中在哪些前缀,用于区分"先清理工具输出"还是"先精简工具集"。构成为字符计量而非 token;若 trajectory 存储截断了超大字段(systemPrompt.truncated=true),按 originalChars 计并如实标注,实际值只会更大。

末轮构成里还包含**工具 schema 利用率**(v1.7,仅 OpenClaw trajectory): 对比编译进上下文的 tools 列表与 toolResult 消息里的实际调用证据(toolResult 有结果必有调用,比匹配 assistant 文本可靠),输出"加载未用"的工具数量、占比及其占 schema 字符的比例,并按工具名前缀(如 feishu_*、sessions_*)聚合,定位精简空间。判读规则:**工具输出占字符大头 → 先治理大输出(截断/落盘/分页);加载未用的 schema 占大头 → 先精简工具集(按需启用插件/分组加载)**。两种格式都会在报告里标注自己的语义;格式识别只认前 30 行的 `traceSchema` 字段形态,CC 会话正文里回现 "openclaw-trajectory" 字样不会误路由。重复 usage 已按变化点去重。回答"上下文实际涨到多大、(CC)哪里发生了压缩、这一轮被什么吃掉、工具集要不要精简";七类内容归组仍用 `analyze_session.py`。

v1.8 起脚本接受**多个文件**并输出车队级(Fleet)汇总:逐文件给出各自报告,末尾追加一张聚合表(窗口占用峰值%、末轮输入 tokens、末轮三块构成字符、工具加载未用占比的中位数/极值);`--json` 输出 `{results, skipped, fleet}` 结构,单文件损坏只进 skipped 不拖垮整体。回答"这台机器上 Agent 会话的整体负载形态""哪些会话在窗口红线上""全机工具集精简空间"这类跨会话问题。聚合只在异常防护后的统计上进行。

v1.8 同时给 OpenClaw 轨迹加了 **cacheRead 异常防护**(实测动机:本机 374 条 trajectory 里 254 条出现 input+cacheRead 高达 24M-38M tokens 的不可能值,同 run 的 context.compiled 消息字符折算仅 ≈19k tokens--部分 provider 的 cacheRead 是跨会话累计值而非本轮上下文)。单个数据点超过「窗口×8 且 ≥2M」即判异常:保留在轨迹明细中但剔除出首末/峰值/均值统计,报告明示剔除数量与异常峰值,并提示用同 run 的 compiled 字符折算做规模交叉验证;全部数据点异常时退回原始值并在报告中标注。CC 格式不受影响(其 cache_read 语义是连续上下文的组成部分,实测无此现象)。

### scripts/audit_constraints.py - 约束丢失审计(治理衰减初筛)

```bash
python3 scripts/audit_constraints.py session.jsonl          # Markdown 审计报告
python3 scripts/audit_constraints.py session.jsonl --json   # 机器可读
```

治理衰减研究(arXiv:2606.22528, 2026)的实测结论:约束是否活过摘要,几乎完全决定 Agent 压缩后是否违规(存活 0% / 被丢 38%)。该脚本对会话做**确定性初筛**:检出约束语句(中英模式 + 句级切分),按可见性三档判级:

- **高危(已丢/极易丢)**:Claude Code 会话里最后一次出现早于首个 usage 骤降点且之后未再现,且压缩摘要中也无再现 → 确认随摘要重写丢失;或单一副本且不在最近区 → 极易被当作低显著度内容丢弃;
- **中危(面临丢失)**:骤降后出现过但已退出最近区(消息末 15% 以外),或多个副本全部"晾旧";
- **低危**:system 通道注入(压缩通常豁免)、最近区仍可见,**或压缩摘要中再现**(v1.4 新增:摘要救回的约束大概率存活,但已经改写,建议抽查保真)。

v1.4 起报告自带**「压缩摘要对照」小节**:解析 `isCompactSummary` / `type=summary` 摘要行(只作对照材料,不作约束来源),把判级结果重组成两份清单——「摘要中再现(大概率存活)」与「摘要中无再现(确认丢失,需重新注入)」,直答"这轮压缩丢掉了什么",不再只标一个骤降边界让你自己 diff。摘要行本身的位置与复述不参与判级,避免"摘要里提到了约束"被误当成"对话里约束仍可见"。

报告内置防误报:同一条消息里 ≥4 句规则合并为"策略文档块"整体判级(处置是整块钉扎而非逐句);过短碎片并回前句;判级依据透明可解释(每条附位置与理由)。

边界:只做位置与可见性判断,不判断约束的语义有效性与权重--脚本结果要结合下一步人工审读确认;漏检时不要直接下"无约束"结论。无 usage 数据时自动降级为位置分析(保守判级,高危偏多属预期)。

## 适用场景

- Agent 会话越跑越慢、越跑越贵,想知道 Token 都消耗在哪;
- 准备配置或优化自动 Compaction,想知道压缩可能丢掉什么;
- Agent 出现"忘记约束、重复劳动、越跑越偏"的症状,想定位是不是上下文污染;
- 评审自己搭建的 Agent Harness:系统指令 + 工具输出的默认结构是否合理。

## 触发条件

用户消息包含以下意图之一即激活:

1. 明确要求:分析上下文 / 上下文预算 / Token 分布 / context usage / token breakdown;
2. 症状描述:会话太长 / Agent 忘事 / 越跑越偏 / 上下文污染 / 压缩丢信息;
3. 提供分析对象:粘贴对话记录、Transcript 片段、消息列表、或口头描述上下文组成。

仅说"分析上下文"但未提供任何材料时,先按「输入收集」询问,不要凭空编造会话内容。

## 输入要求

**必要输入(三选一):**

1. 会话记录 / Transcript 文件路径(JSONL、JSON、Markdown 均可);
2. 直接粘贴的对话内容(含工具输出更佳);
3. 结构化描述:系统指令条目 + 每轮消息 + 工具调用及其输出规模的清单。

**可选输入:**

- 模型上下文窗口大小(如 200k / 1M;未提供时按 200k 估算并注明);
- 关心的具体症状("它忘了不能动 legacy 目录");
- 分析目的(降本 / 修 Compaction 策略 / 排查遗忘)。

**隐私边界:** 只分析用户主动提供的材料。若记录中包含 API Key、密码等敏感串,在报告中以 `[REDACTED]` 标注,不原样引用、不写入建议示例。

## 执行流程

### 第一步:获取材料并估算规模

- 文件输入:**优先用 `scripts/estimate_tokens.py --file <路径>` 得到总量,用 `scripts/analyze_session.py` 得到七类预算表初稿**;脚本不可用时再人工解析会话结构(角色、工具调用、输出);
- Claude Code 会话(`~/.claude/projects/` 下的 JSONL)或 OpenClaw trajectory(`*.trajectory.jsonl`):**先跑 `scripts/analyze_usage.py`** 拿真实上下文轨迹(自动识别格式;CC 额外给压缩骤降点,OpenClaw 给 run-based 波动与 systemPrompt 截断统计),再跑 `analyze_session.py` 做七类归组--前者回答"涨到多大、(CC)哪里压缩",后者回答"都花在哪了";
- **症状涉及"忘了约束/违规/越跑越偏"时,加跑 `scripts/audit_constraints.py`**:得到约束清单与三档判级,再对高危/中危条目逐一人工确认语义有效性;
- 粘贴输入:直接统计;
- 口头描述:按用户给定的条目和数量级整理。

Token 估算规则:中文约 1 字 ≈ 1~1.5 Token(脚本取 1.25),英文约 4 字符 ≈ 1 Token,代码按字符数 ÷ 3 估算(脚本按代码密度自动切换)。**所有数字都是估算值**,报告中统一使用"≈",不声称精确。

### 第二步:七类归组统计

把每段内容归入以下七类,分别统计估算 Token 和占比:

| 类别 | 典型内容 | 健康信号 | 危险信号 |
|---|---|---|---|
| 1 系统指令 | System Prompt、工具定义、输出格式要求 | 占比稳定、只出现一次 | 每轮重复注入;多条规则互相冲突 |
| 2 任务目标 | 用户需求、验收标准 | 清晰、唯一的最新版本 | 同一目标多个版本并存,无"以哪个为准"标记 |
| 3 约束与规则 | "不要动 X"、安全边界、项目规则 | 集中、显式、原文保留 | 散落在对话中游、只出现过一次 |
| 4 工具输出 | 命令日志、文件读取、搜索结果 | 经过截断/摘要,留有指针 | 一次整读数千行;重复读取同一大文件 |
| 5 对话历史 | 往返消息、确认、澄清 | 近期相关轮次 | 大量"好的""继续"式空转轮 |
| 6 中间推理 | 计划、假设、自我纠正 | 最新计划可见 | 被推翻的旧方案仍全文在场,无作废标记 |
| 7 状态与记忆 | 任务清单、外部记忆、检查点 | 结构化、可追溯 | 无状态外置,全靠对话历史承载进度 |

输出一张预算表:每类的估算 Token、占比、健康/危险判定、依据(指出具体消息或轮次)。

### 第三步:识别五类污染模式

在归组结果之上,重点扫描以下模式(每条都要给出具体位置证据):

1. **巨物输出**:单条工具输出 ≈ 超过当前窗口 5% → 标红。建议:Tool 层截断/分页,结论 + 指针进上下文;
2. **复读机**:同一文件/页面被多次完整读取,或同一规则每轮重复注入 → 建议缓存或去重;
3. **僵尸假设**:已被新证据推翻的中间推理仍全文在场,且无"已作废"标记 → 是"越跑越偏"的常见根因;
4. **约束裸奔**:关键约束只在对话中出现过一次,随位置漂移面临被压缩丢失的风险 → 建议原文提升到固定区块;
5. **无状态裸奔**:任务进度只存在于对话流中,无结构化清单 → 一旦 Compaction 触发,进度保真度无法保证;
6. **治理衰减**:约束曾经在场且被遵守,压缩后"不再看见"而违规--与"约束裸奔"的区别是时间维度:裸奔是"从未被保护",治理衰减是"曾经可见、后被删除"。用 `audit_constraints.py` 的高危判级 + 用户陈述的症状交叉确认:约束文本已不在可追溯范围内、且任务输出开始违反它,即为典型信号。治理建议对应升级为钉扎(system 通道或压缩豁免区块 + 压缩后重注)。

### 第四步:Compaction 风险预演

模拟一次"只保留摘要 + 最近 N 轮"的压缩,回答三个问题:

1. **会丢什么**:逐条列出压缩后丢失的约束、决策、环境事实(依据第三步的"约束裸奔""僵尸假设"清单与约束审计的高危/中危判级);
2. **会错什么**:哪些摘要句可能把"部分完成"写成"已完成"(摘要幻觉风险点);
3. **该保什么**:给出压缩摘要必须显式包含的最小集合--目标与验收标准、硬性约束原文、当前状态清单、被否决方案及理由、证据指针。

### 第五步:输出治理建议

按"四层处置"给出每一类内容的处置方式,禁止一刀切的"全部删掉":

| 层 | 处置 | 适用内容 |
|---|---|---|
| 原文保留层 | 原样保留在固定位置 | 系统指令、硬性约束、验收标准 |
| 结构化层 | 压缩进清单/状态文件,定期保真更新 | 任务进度、决策记录、被否决方案 |
| 指针层 | 只留"结论 + 指针",原文外置按需读取 | 大型工具输出、历史日志、已读文件 |
| 可丢弃层 | 直接淘汰 | 空转轮次、已作废假设的推导过程、重复读取 |

建议必须落到可执行动作:改哪条工具的输出策略、把哪句话提升到哪个固定区块、外置状态文件放哪、Compaction 触发时机建议(定性即可,不编造具体产品的默认阈值)。

## 输出格式

```markdown
# 上下文预算分析报告

## 一、总览
- 输入材料:<来源与规模>;估算总占用:≈X tokens(窗口按 Y 估算,占比 Z%)
- 一句话结论:<最严重的一个问题>

## 二、预算分布
| 类别 | ≈Token | 占比 | 判定 | 依据 |
|---|---|---|---|---|
| 1 系统指令 | ... | ... | ✅/⚠️/🔴 | ... |
| ...七类逐行列出... |

## 三、污染点清单
| # | 模式 | 位置证据 | 影响 | 建议 |
|---|---|---|---|---|

## 四、Compaction 风险预演
- 会丢:<逐条>
- 会错:<逐条>
- 压缩摘要最小保留集合:<清单>

## 五、治理建议(四层处置)
| 层 | 内容 | 具体动作 |
|---|---|---|

## 六、方法与局限
- Token 为估算值(方法:<...>);未模拟真实模型行为;具体产品的 Compaction 阈值不在分析范围内。
```

短会话(总占用 ≈ < 10% 窗口)输出精简版:总览 + 预算分布表 + 最多 3 条建议,其余章节省略。

## 异常处理

- **材料无法解析**:说明支持的格式,请用户重新提供,不要基于猜测输出报告;
- **材料过小**(< 5 条消息):告知样本有限,结论降级为"初步观察";
- **用户只要数字不要报告**:只给预算分布表;
- **用户要求删除/修改会话记录**:超出本 Skill 职责,仅提供建议,不执行修改;
- **敏感信息**:发现即按隐私边界处理并在报告开头提示一次。

## 验收标准

- [ ] 七类归组逐类有 Token 估算、占比与判定,数字均标注"≈"并说明估算方法;
- [ ] 每条污染点都有具体位置证据,无"可能存在污染"式的空泛指控;
- [ ] 跑过 `audit_constraints.py` 时:高危/中危约束逐条经人工确认语义有效性后才写入报告,脚本漏检可能已用人工审读覆盖;
- [ ] Compaction 预演明确回答"丢什么、错什么、保什么";
- [ ] 治理建议落在四层处置上,且每条可执行(有对象、有动作);
- [ ] 未虚构任何会话中不存在的内容;敏感信息已脱敏。

## 约束与边界

- 只读分析,不修改用户的任何会话数据或配置文件;
- 不声称知道具体 Agent 产品的内部压缩实现与默认阈值;
- Token 数一律为估算,不冒充精确计量;
- 不把"压缩上下文"建议为唯一手段--优先建议结构性治理(分层、外置、去重),压缩是最后防线。

---

# English Version

> **Bilingual skill** - full spec is in Chinese above; this English reference covers the operational essentials, and the AI fully supports English interaction.

## Summary

**context-budget-analyzer** — Analyzes where an Agent session's context budget goes. Ships with three deterministic scripts (`estimate_tokens.py`, `analyze_session.py`, `analyze_usage.py`) that parse session JSONL, estimate tokens per bucket, flag oversized tool outputs, and reconstruct the REAL context trajectory from Claude Code `message.usage` fields; `audit_constraints.py` performs a deterministic constraint-loss audit (Governance Decay screen, arXiv:2606.22528): it extracts constraint sentences, grades each as lost / at-risk / visible using position, recency zone, and usage-drop correlation, and recommends pinning for lost constraints. The agent then reviews evidence, runs the Compaction dry-run, and delivers 4-tier governance advice. Categorizes content into 7 buckets (system instructions / task goals / constraints / tool outputs / conversation history / intermediate reasoning / state & memory), detects pollution patterns (giant tool outputs, repeated reads, zombie assumptions, unanchored constraints, missing external state, governance decay), and previews Compaction information loss.

## Workflow

1. **Acquire material** — transcript file path, pasted conversation, or structured description. Prefer the bundled scripts: `python3 scripts/analyze_session.py session.jsonl [--window N] [--json]` produces the 7-bucket budget table; `python3 scripts/estimate_tokens.py --text|--file|--code` estimates a single passage; for Claude Code sessions (`~/.claude/projects/**/*.jsonl`), `python3 scripts/analyze_usage.py <session.jsonl> [--window N]` reconstructs the REAL context trajectory from official `message.usage` fields (first/last/peak, window %, and suspected-compaction drops ≥20%) — measured values, not estimates; v1.8 accepts MULTIPLE files for a fleet-level aggregate (per-file reports + median/min/max summary; `--json` emits `{results, skipped, fleet}`), with a cacheRead sanity guard that excludes implausible OpenClaw usage points (input+cacheRead exceeding window×8 and 2M — provider-side cross-session cache accumulation) from stats while reporting them explicitly; when symptoms involve forgotten constraints or violations, also run `python3 scripts/audit_constraints.py session.jsonl` for the three-tier constraint visibility audit, then manually confirm semantic validity of each high/mid item. Fall back to manual estimation (CJK ≈ 1~1.5 tokens/char, English ≈ 4 chars/token, code ≈ chars/3) only when Python is unavailable. Always mark numbers as estimates ("≈").
2. **Categorize** - script output gives the draft table (per-bucket tokens, ratio, chunk count); review key chunks yourself to assign healthy/risky verdicts - heuristic classification can miss scattered constraints and out-of-band state files.
3. **Detect pollution** — giant outputs (>5% of window, auto-flagged by script), repeated content, zombie assumptions (refuted reasoning still present), one-shot constraints drifting toward compression loss, progress with no external state, governance decay (a constraint that was visible and obeyed, then silently dropped by compaction — confirmed via the constraint audit's high-risk grades plus user-reported symptoms; remediation upgrades to pinning). Every finding needs positional evidence.
4. **Compaction dry-run** - what would be lost / what summaries might get wrong / minimum retention set (goal & acceptance criteria, verbatim constraints, current status list, rejected alternatives with reasons, evidence pointers).
5. **Governance** - 4-tier handling: verbatim-keep / structured / pointer-only / discardable, each with concrete actions.

## Output

Markdown report: Overview → Budget table (7 buckets) → Pollution list (with evidence) → Compaction dry-run → Governance table → Method & limitations. Short sessions (<10% window) get an abbreviated report.

## Constraints

- Read-only analysis; never modify session data or configs.
- Never fabricate session content; sensitive strings get `[REDACTED]`.
- Token counts are estimates; product-specific compaction thresholds are out of scope.
- Prefer structural fixes (layering, externalization, dedup) over "just compact it".
