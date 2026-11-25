# Playbook: 从原始对话数据做弱监督挖掘

> **意图标识**:`discover`
> **当前重点**:适配金条场景的人工外呼 ASR 转写文本
> **核心区别**:
> - 金牌学习 = 已标记优质 + 小样本
> - 对话挖掘 = 未标记原始 + 大样本
> - 当前默认不是最终分类,而是先做 `good_seed / bad_seed / gray_*` 分桶

> 创建时间:2026-04-08
> 最近更新:2026-04-11(重构为 ASR 弱监督分桶流程)

---

## 一、什么时候用本 Playbook

### ✅ 命中条件
满足至少一条即可:
- 用户明确说"挖掘对话数据" / "挖掘 goodcase/badcase"
- 用户说"聚类分析" / "批量分析" / "批量评分"
- 用户说"从原始对话中学习" / "自动筛选优质案例"
- 提供 Excel / JSON / CSV 大文件(>50 条)
- 提供录音转写文本 / ASR 文本,希望判断哪些像 goodcase / badcase

### ❌ 排除条件
- 用户明确说"金牌客服" / "金牌对话" / "金牌案例"
- 用户说"学习金牌" / "金牌客服学习" / "金牌客服进化"
- 用户提供少量对话文本(≤20 条)并暗示优质
- 用户明确要做 PE 对练 / PE 优化 / PE 提交 / PE 验证

### ⚠️ 混合信号处理
- 同时说"金牌" + "挖掘" → 优先回到 `pe-self-improving`
- 同时给大文件 + 明确说"学习金牌" → 先确认是不是原始数据还是精选数据

---

## 二、输入要求

### 2.1 数据格式

| 格式 | 要求 |
|------|------|
| Excel | 必须包含对话内容列(如 `transcription_result` / `dialog_content` / `对话内容`) |
| JSON | 必须包含 `dialogs` 数组,元素包含 `content` / `dialog_content` / `conversation_text` |
| CSV | 必须包含对话内容列 |

### 2.2 数据规模建议

| 规模 | 推荐策略 |
|------|----------|
| <100 条 | 先跑标准化 + 弱监督特征提取 |
| 100~1000 条 | 跑完整 seed 分桶链路 |
| >1000 条 | 分批处理,每批 500 条左右 |

### 2.3 数据类型先判断

拿到数据后,先判断它更像哪一类:

#### A. 干净文本 / 结构化对话
特点:
- 角色切分较清楚
- 错字少
- 可以直接走规则评分或 hybrid

#### B. ASR 脏文本 / 人工外呼转写
特点:
- 错字较多
- 角色切分混乱
- 重复段 / 长句 / 中断明显
- 没有人工标签

**如果是 B,默认优先走弱监督分桶,不要一开始就强行 final good / bad 二分类。**

---

## 三、当前推荐流程(ASR 弱监督版)

### 第一步:标准化 + ASR 清洗

**目的**:
- 统一输入格式
- 做基础角色分离
- 生成对话质量元信息

**脚本**:`scripts/normalize_dialogs.py`

**关键产出**:
- `raw_text`
- `clean_text`
- `normalized_text`
- `turns`
- `agent_text`
- `user_text`
- `meta.turn_count`
- `meta.dialog_end_type`
- `meta.asr_noise_score`

---

### 第二步:弱监督特征提取与分桶

**目的**:
- 不是直接判最终 good / bad
- 而是抽取稳健信号,并先分成:
  - `good_seed`
  - `bad_seed`
  - `gray`
  - `gray_high_risk`
  - `gray_potential_good`

**脚本**:`scripts/template_match_dialogs.py`

**当前重点信号**:
- `explicit_acceptance`
- `explicit_interest`
- `product_objection`
- `conversation_rejection`
- `product_negative_sentiment`
- `agent_negative_sentiment`
- `engaged_objection`
- `early_hangup`
- `long_agent_monologue`
- `scheduled_followup`
- `natural_close`

**注意**:
- "中途挂断"只能作为过程信号,不能直接等于 badcase
- "利率高 / 额度低"优先视为产品异议,不直接视为失败

---

### 第三步:可选统一评分

如果需要统一输出格式,或者接后续批处理链路,可使用:

**脚本**:`scripts/batch_score_dialogs.py`

**模式说明**:
- `rules`:规则式快速评分
- `llm`:大模型评分
- `hybrid`:规则 + LLM
- `weak_label`:弱监督种子分桶(ASR 无标注场景优先)

**建议**:
- ASR / 无标注 → 优先 `weak_label`
- 干净文本 / 想做正式质量分 → 再考虑 `rules` / `hybrid`

---

### 第四步:按 seed_label 分桶聚类

**目的**:
- 分别看 `good_seed`、`bad_seed`、`gray_*` 的共性模式
- 不再把所有对话混在一起按总分切块

**脚本**:`scripts/cluster_dialogs.py`

**当前输出分析维度**:
- 平均 good_score / bad_score / confidence
- 高频 positive signals
- 高频 negative signals
- 高频 risk signals
- 高频 quality signals

---

### 第五步：提取候选规则 / 约束规则 / 待验证假设

**脚本**:`scripts/extract_rules_from_cluster.py`

**模式说明**：
- `llm`（默认）：LLM 深度提取，从抽样对话原文归纳实质规则/话术/问题模式
- `stats`：仅信号频率统计，作为辅助参考

**LLM 模式产出逻辑**：
- 从 `good_seed` 抽样 → LLM 归纳 → 候选规则 + 候选话术
- 从 `bad_seed` 抽样 → LLM 归纳 → 问题模式 + 洞察
- 从 `gray_*` 抽样 → LLM 归纳 → 待验证假设
- 自动写入 warm 层 6 个规范文件（candidates/evidence/learnings）

**stats 模式产出**：
- 仅输出信号频率统计，不写 warm 层
- 适合快速了解信号分布，不适合直接作为规则来源

**重要**：LLM 自动提取是高质量起点，但不保证100%精准。建议：
1. 提取后人工审阅 warm 层内容，修正明显偏差
2. 对关键规则做人工抽样验证
3. 如自动提取效果不佳，可手动深度分析替代

---

### 第六步：生成人工 review 抽样包

**脚本**：`scripts/sample_for_review.py`

**推荐抽样桶**：
- `good_seed`
- `bad_seed`
- `gray_high_risk`
- `gray_potential_good`

**用途**：
- 校准规则误伤
- 验证中途挂断是否真有价值
- 区分"产品异议"和"对话失败"

### 第七步：深度分析（推荐，LLM 自动提取的补充）

**目的**：LLM 自动提取是高质量起点，但可能遗漏或偏差。对于关键场景，建议手动深度分析。

**什么时候需要手动深度分析**：

1. LLM 提取的规则过于笼统，缺乏场景特异性
2. good_seed 数量少（<100），LLM 抽样覆盖不足
3. 需要归纳特定策略模式（如"具体数字利益对比"、"灵活还款强调"）
4. 需要从对话原文中提取可直接使用的话术模板

**深度分析操作步骤**：

1. **读 good_seed 原文**：抽样 5-10 条最长（轮次最多）的 good_seed 对话
   - 观察客服的核心策略模式
   - 标注关键转折点（从拒绝到接受的转折发生在哪一轮）
   - 归纳策略类型（如：利益对比型、流程引导型、情感共鸣型）

2. **读 bad_seed 原文**：抽样 5-10 条典型 bad_seed 对话
   - 识别客服的典型失误模式
   - 注意"差一点就成功"的案例——这些灰区最有分析价值

3. **归纳并写入 warm 层**：
   - 规则 → `warm/candidates/rules.md`（追加或替换 LLM 提取结果）
   - 话术 → `warm/candidates/utterances.md`
   - 洞察 → `warm/learnings/insights.md`
   - 问题 → `warm/learnings/issues.md`
   - 证据 → `warm/evidence/rules.md` + `warm/evidence/utterances.md`

4. **关键原则**：
   - 每条规则/话术必须有对话原文支撑
   - 区分"底线规则"（违规即失败）、"核心规则"（关键成功因素）、"增效规则"（锦上添花）
   - 话术要标注使用场景（开场/利益/异议/引导/收尾）

### 第八步：自动进化特征规则（新增）

**目的**：每次挖掘完自动补齐 skill，不需要人工提醒

**脚本**：`scripts/auto_evolve_features.py`

**核心逻辑**：
1. 找出信号稀疏的对话（落入 gray/无信号）
2. 从中提取现有词表未覆盖的高频词
3. 自动补入现有 feature_rules 类别
4. 建议新的 feature_rules 类别
5. 写回 scenes/{scene}.yaml
6. 记录进化历史

**执行方式**：
```bash
# 自动进化（默认自动应用变更）
python3 scripts/auto_evolve_features.py \
  --input "loan-match.json" \
  --scene "loan"

# Dry run（只看不写）
python3 scripts/auto_evolve_features.py \
  --input "loan-match.json" \
  --scene "loan" \
  --dry-run
```

**重要**：此步骤是标准流程的一部分，每次挖掘后**必须执行**。

---

## 四、标准执行链路

### 4.1 ASR 弱监督推荐链路

```bash
# 1. 标准化 + ASR 清洗（自动角色分离）
python3 scripts/normalize_dialogs.py \
  --input "对话数据.xlsx" \
  --scene "loan" \
  --output "loan-normalized.json"

# 2. 弱监督特征提取与 seed 分桶
python3 scripts/template_match_dialogs.py \
  --input "loan-normalized.json" \
  --scene "loan" \
  --output "loan-match.json"

# 3. 按 seed_label 分桶聚类
python3 scripts/cluster_dialogs.py \
  --scores "loan-match.json" \
  --scene "loan" \
  --output "loan-cluster.json"

# 4. LLM 深度提取（默认模式，自动写入 warm 层 6 个文件）
python3 scripts/extract_rules_from_cluster.py \
  --clusters "loan-cluster-clusters.json" \
  --scene "loan"

# 如只需信号频率统计（不写 warm 层）：
# python3 scripts/extract_rules_from_cluster.py \
#   --clusters "loan-cluster-clusters.json" \
#   --scene "loan" \
#   --mode stats \
#   --output "loan-rules-stats.md"

# 5. 深度分析（手动，推荐）
# - 读 good_seed / bad_seed 原文，归纳实质规则和话术
# - 追加或修正 LLM 提取结果
# - 写入 warm 层 6 个文件

# 6. 生成人工 review 包
python3 scripts/sample_for_review.py \
  --input "loan-match.json" \
  --output-json "loan-review.json" \
  --output-md "loan-review.md" \
  --sample-size 30

# 7. 自动进化特征规则（必须执行）
python3 scripts/auto_evolve_features.py \
  --input "loan-match.json" \
  --scene "loan"
```

### 4.2 需要统一评分输出时

```bash
python3 scripts/batch_score_dialogs.py \
  --input "loan-match.json" \
  --scene "loan" \
  --output "loan-weak-label.json" \
  --mode weak_label
```

---

## 五、输出物说明

### 5.1 中间产物
- 标准化 JSON
- 特征提取 / 分桶 JSON
- 聚类分析 JSON
- 聚类分桶 JSON

### 5.2 结果产物
- 候选规则 Markdown
- review 抽样 JSON
- review 抽样 Markdown

### 5.3 学习库写入目标

**对齐 warm 层规范结构**（与 pe-self-improving 学习库一致）：

| 发现 | 写入路径 |
|------|----------|
| 候选正向规则 | `warm/candidates/rules.md` |
| 候选话术 | `warm/candidates/utterances.md` |
| 规则证据 | `warm/evidence/rules.md` |
| 话术证据 | `warm/evidence/utterances.md` |
| 问题模式 | `warm/learnings/issues.md` |
| 洞察与假设 | `warm/learnings/insights.md` |

路径模板:

```text
~/pe-self-improving/memory/{target_scene}/warm/
├── candidates/
│   ├── rules.md          # 候选正向规则
│   └── utterances.md     # 候选话术
├── evidence/
│   ├── rules.md          # 规则的对话原文证据
│   └── utterances.md     # 话术的对话原文证据
└── learnings/
    ├── issues.md          # 问题模式
    └── insights.md        # 洞察与灰区假设
```

**重要**：
- `extract_rules_from_cluster.py`（LLM 模式）会自动写入以上 6 个文件
- 不要再写入 `warm/rules-candidates.md`（根目录旧路径，已废弃）
- 不要再写入 `warm/issues/` 或 `warm/discovery-reports/`（旧结构，已废弃）

---

## 六、当前判断标准

### 6.1 `good_seed`
含义:
- 高置信正向样本
- 可能是真 goodcase,也可能只是正向潜力样本

### 6.2 `bad_seed`
含义:
- 高置信失败样本
- 可能是真 badcase,也可能包含少量边界失败样本

### 6.3 `gray_high_risk`
含义:
- 高风险边界样本
- 很适合挖"长段单边讲解 / 低质量推进 / 将坏未坏"的模式

### 6.4 `gray_potential_good`
含义:
- 正向潜力样本
- 常见于有 objection 但还在继续互动的场景

---

## 七、实操建议

### 7.1 第一次跑数据时
不要急着问:
- "为什么没有很多 goodcase?"

先看:
- `good_seed` 是否够纯
- `bad_seed` 是否误伤过多
- `gray_high_risk` 是否有稳定边界模式

### 7.2 对人工外呼金条数据
重点记住两条:

1. **产品异议 ≠ badcase**
2. **真正该重点抓的是:对话拒绝 + 互动失败**

### 7.3 什么时候继续调规则
只有当人工 review 后发现:
- `good_seed` 纯度不够
- `bad_seed` 误伤太多
- `gray_high_risk` 模式过杂

才继续迭代权重和特征。

---

## 八、维护原则

- 新增特征或权重时,先改 `scenes/{scene}.yaml`
- 文档描述必须与脚本当前行为一致
- 不再用"最终 good / bad 分类器"的语气描述当前版本
- 发现产出以"候选集 / 分桶 / 假设"为主,而不是直接宣称最终标签

---

*创建时间:2026-04-08*
*最近更新:2026-04-11(重构为 ASR 弱监督分桶流程)*
*用途:从原始对话数据中做弱监督发现、候选筛选与边界模式挖掘*