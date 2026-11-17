# Citation Discipline / 引用纪律

本文件详解本 skill 的引用规范，融合 Firecrawl 多源交叉、Deepdive 四层验引、LitRAG 两阶段检查、Cited-but-Not-Verified 三维评估。

## 硬规矩

### 1. 每条事实必须可点开核验

- **URL 必须是本次实际抓取到的地址**
- **绝不凭记忆构造 URL**
- 抓不到就写「未取得」，并写清为什么取得失败

### 2. 引号内一个字都不能动

要消除引语里的破折号，就把引语在破折号处断成两段，破折号落到引号之外换成叙述性连接。

### 3. 搜索结果摘要一律不是证据

搜索结果的 snippet 只能用于**决定要不要去抓取原文**，不能作为档案里的引用来源。必须去抓原文页面。

### 4. 二手条目转引必须回到被引出处核对措辞

如果档案里的一句话来自二手转引（如维基条目转引某媒体），必须回到原始媒体核对措辞是否一致。转引过程中经常被"编辑性改写"。

## 引用质量三维评估（Cited but Not Verified 吸收）

对每条引用，检查三个维度：

| 维度 | 检查 | 失败类型 |
|---|---|---|
| **Link Works** | URL 是否可打开 | F1: 链接失效 |
| **Relevant Content** | 页面内容是否相关 | F2: 相关度低 |
| **Fact Check** | 引用是否真正支持该 claim | **F6: 引用存在但不支持 claim** |

**F6 比 F1 更危险**：读者点进去看到 URL 存在就信了，但页面根本没支持这个 claim。

**处理**：每条 claim 至少跑 2-3 独立来源检索交叉验证。

## 多源交叉验证（Firecrawl 吸收）

**规则**：每个 claim 跑 2-3 独立来源检索。

**Verdict 三种**：
- **supported**：多来源支持
- **contradicted**：至少一来源反驳
- **unverified**：搜索后仍无法确认

**处理**：
- supported → 可信度升到 ① 可靠事实
- contradicted → 两说并列写进档案
- unverified → 标 ⑤ 未知，写进待核实清单

## 四层验引（Deepdive 吸收）

**四层**：
1. **Link layer**：URL 是否可打开
2. **Quote layer**：引号内文字是否原文出现
3. **Passage layer**：被引段落是否支持 claim
4. **Source-authority layer**：来源本身是否可靠

**每层失败对应处理**：
- L1 失败 → 尝试找其他镜像，或用 Wayback Machine
- L2 失败 → 检查是否为翻译/改写，若是则不加引号
- L3 失败 → 该 claim 需要回炉，或标 inferred
- L4 失败 → 降低 claim state，或标 unknown

## Dissent Protection（Deepdive 吸收）

**规则**：反方声音不被吞并。

**具体做法**：
- 搜索时**主动加反向关键词**（如 `"X" criticism`, `"X" scammer`, `"X" refuted`）
- 找到的反方证据**必须写进"争议与风险点"章节**，不做"作者认为 X"的独裁判断
- 如果反方是低质量 SEO 内容（67 views / 2K 订阅），**仅作为"争议存在性"记录**，不采纳其结论

## Two-stage Quote Verification（LitRAG 吸收）

**阶段 1：确定性字符串匹配**
- 用脚本检查档案里所有直引语（`"..."` 内）是否真的出现在被引源的原文里
- 不匹配的直接标为「引语待核实」

**阶段 2：LLM Judge 判 passage 是否支持 claim**
- 对每条事实 claim，判断被引源的相关段落是否**真正支持**该 claim
- 只支持"引语是否原文"和"段落是否支持 claim"两件事，不做事实判断

**落点**：本 skill v1.2 实现 `scripts/verify_quotes.py`

## Atomic Fact 分解（FActScore 吸收）

**规则**：**一条时间线只写一件事**。

**为什么**：
- 合并的事件无法单独验证，FActScore 无法评估
- 一条时间线里塞 3 件事，读者不知道要信哪一件

**范例**：

❌ **合并**：
> 2014 年他出版了《XX》，同时开始做 XX 项目，并获得 XX 奖项。

✅ **拆分**：
> 2014-03 出版《XX》。
> 2014-05 开始 XX 项目。
> 2014-11 获得 XX 奖。

## Retraction Check（Moonweave 吸收）

**规则**：引用被撤回/更新的来源应显式标记。

**做法**：
- 引用学术论文时检查 retraction 数据库
- 引用被后续更新的数据（如 star 数变化）标注"数据截至 YYYY-MM-DD"
- 关键：不是"引用错了"，而是"引用时是对的，现在过时了"

## 结构化 Verdict 输出

对每条 claim 的判定，用统一格式：

```
claim: [原文]
verdict: supported | contradicted | unverified
sources: [URL1, URL2, ...]
notes: [简短说明]
```

## Pitfalls

1. **构造 URL** → 严禁，抓不到就写「未取得」
2. **只验链接不验内容** → F6 比 F1 更危险
3. **只找正面不找反方** → 违反 dissent protection
4. **合并多件事到一条时间线** → 违反 atomic fact 约束
5. **机构自述当可靠事实** → 混淆立场与事实
6. **二手条目转引不核对措辞** → 引语变形
7. **不写引用时状态** → 应标注数据截至日期，避免引用过时
