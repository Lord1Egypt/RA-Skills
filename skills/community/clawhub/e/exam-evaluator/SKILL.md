---
name: exam-evaluator
description: "从 .xlsx/.xls/.docx/.pdf 试卷/题库中提取试题，从五个维度（内容效度、结构效度、难度控制、区分度潜力、规范性）评估命题质量，生成交互式 HTML 可视化报告。Use when: (1) 用户要求评估试卷或题库质量，(2) 命题后需要质量检验，(3) 对比多份试卷的命题水平，(4) 生成试题分析报告，(5) 用户上传 Excel/Word/PDF 文件要求分析。触发词：评估试卷、评估题库、试题质量、试卷分析、题库分析、命题质量、命题检验、exam evaluation、question quality assessment、.xlsx、.docx、.pdf"
version: 1.3.0
---

# 试题质量评估

从试卷/题库中提取试题，结合客观量化指标（Python）和主观语义评价（Agent），从五个维度输出评估结果。

## ⛔ NEVER

- **NEVER** 跳过 Phase 4 确认模式直接评分
- **NEVER** 在没有解析质量标注的情况下生成报告
- **NEVER** 使用纯加权平均计算综合评分（必须用短板机制 `min(加权平均, 最低分+2)`）
- **NEVER** 将填空题答案唯一性交由 Python 判定（必须由 Agent 判断）
- **NEVER** 在低置信度题型未向用户确认的情况下继续
- **NEVER** 让判断题"正确"比例偏离 40%-60% 区间而不指出
- **NEVER** 忽略最长选项偏差 > 45% 的结构性问题
- **NEVER** 接受选择题答案分布标准差 > 7 而不指出失衡风险
- **NEVER** 在认知层级仅覆盖 ≤2 层时给出"良好"及以上评价

## 工作流程

### Phase 1: 解析

运行本地脚本提取原始文本：
- `.xlsx`/`.xls` → `scripts/parse_excel.py <file> temp/clean.json`（结构化可靠，直出 clean.json）
- `.docx` → `scripts/parse_docx.py <file> temp/raw.json`
- `.pdf` → `scripts/parse_pdf.py <file> temp/raw.json`

**注意**：Word/PDF 脚本仅提取文本，结构化由 Phase 2 Agent 完成。

### Phase 2: Agent 结构化

**多卷识别（MANDATORY）**：Agent 结构化前 MUST 先判断文档是否包含多套独立试卷。
识别信号：
- 出现多个独立标题（如不同学校/学期/科目名称）
- 题号重新从 1 开始
- 科目/班级/命题人信息发生变化
- 出现明显的分隔线或"第X页 共Y页"重置

**不应判为多卷的情况**（否定规则）：
- 题干内容中出现"第1题"字样（非题号标记）
- 同一试卷的附加页/续页（页码增加但科目、题型结构连续）
- 参考答案与试题正文被误判为独立试卷（检查是否只有答案无题干）
- 同一学校/学科不同题型分节（如"一、选择"→"二、填空"是单卷的正常分段）

**输出规则**：
- **多卷**：分别输出 `temp/clean_1.json`、`temp/clean_2.json`...，每个文件包含一套完整试卷的 `metadata` 和 `questions`
- **单卷**：输出 `temp/clean.json`

**Excel 路径**：跳过本 Phase，`parse_excel.py` 已输出 clean.json。

**Word/PDF 路径**：Agent 读取 `temp/raw.json` 中的 `paragraphs` 和 `tables`，转换为标准 clean JSON：
1. 识别题型（选择/判断/填空/简答/论述/案例分析/计算/应用等），附带 `confidence`（高/中/低）
2. 提取每题的 `id`、`question_type`、`stem`、`options`、`answer`、`explanation`、`score`、`rubric`、`knowledge_point`、`cognitive_level`、`difficulty`
3. 答案自动关联（可能在题干后，也可能在文末"答案与解析"部分）
4. 判断题答案标准化：A/正确/对/√/TRUE → "正确"，B/错误/错/×/FALSE → "错误"
5. 选择题选项提取为数组 `["A. 内容", "B. 内容", ...]`
6. **知识点自动识别**（MANDATORY）：即使原始试题无标注，MUST 根据题干+选项+解析自动识别 `knowledge_point`：
   - 选择题/判断题：从题干关键词 + 解析提取核心考点
   - 填空题：从答案反推考查知识点
   - 主观题：从评分标准提取能力要求对应的知识点
   - 无法归类时用"综合应用"
7. 低置信度题型标记"待确认"，无法识别的题跳过（不要编造）

**内容质量验证（MANDATORY）**：

1. Agent MUST 逐题验证答案与题干逻辑一致性：
   - 检查答案是否实际回应题干提问内容
   - 多选题：确认正确选项存在且选项内容合理（非空/非占位符）
   - 记录结果至 clean.json `answer_verified` 字段：`"verified"` | `"suspicious"` | `"unverifiable"`

2. Agent MUST 检查题干语言文字质量：
   - 标记错别字、语法错误、歧义表述
   - 记录问题至 clean.json `linguistic_issues` 字段（字符串数组，无问题则为 `[]`）

3. Agent MUST 检查内容对齐性：
   - 确认答案内容确实属于本题（而非错位粘贴到其他题目）
   - 确认选项主题与题干相关
   - 记录问题至 clean.json `content_alignment` 字段（字符串数组，无问题则为 `[]`）

4. ⚠️ **GUARDRAIL**：Agent MUST NOT 自行判定答案为"错误"（`verified_wrong`），最高判定为 `"suspicious"`。最终验证由 Phase 7 完成。

**新增字段说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `answer_verified` | string | ✅ | `"verified"` \| `"suspicious"` \| `"unverifiable"` — Agent 对答案正确性的判断 |
| `linguistic_issues` | array | ✅ | 语言文字问题列表，如 `["第3题题干存在歧义表述", "第5题出现错别字"]`，无问题则为 `[]` |
| `content_alignment` | array | ✅ | 内容错位问题列表，如 `["第2题答案与题干主题不一致"]`，无问题则为 `[]` |

**输出格式**：标准 clean JSON，包含 `metadata`（title/total_score/source_type）、`parse_quality`（high/medium/low）、`questions` 数组（每题含 id、question_type、stem、options、answer、explanation、score、knowledge_point、cognitive_level、difficulty、confidence、answer_verified、linguistic_issues、content_alignment）。

### Phase 2+ 输出质量自动验证（Word/PDF 路径必须执行）

生成 clean.json 后，MUST 计算以下覆盖率指标：

| 指标 | 计算公式 | 合格阈值 |
|------|----------|----------|
| 答案覆盖率 | `有 answer 字段的题数 / 总题数` | ≥80% |
| 题型识别率 | `question_type ≠ "未知" 的题数 / 总题数` | ≥80% |
| 知识点覆盖率 | `knowledge_point ≠ "综合应用" 的题数 / 总题数` | ≥60% |

**验证结果分支**：

- **任一指标 < 80%（答案/题型）或 < 60%（知识点）** → ⚠️ 暂停后续流程，Do NOT 继续 Phase 3。
  向用户展示验证结果（三项指标的具体数值），并明确询问：
  > "当前 parse_quality 偏低（答案覆盖率 X%，题型识别率 Y%，知识点覆盖率 Z%）。是否启用 Agent 大模型深度识别进行二次解析？"
  >
  > - 选择"是"：Agent 重新逐题审阅 `raw.json` 中未识别/低置信度的段落，利用语义理解补充缺失字段
  > - 选择"否"：按当前质量继续，parse_quality 标记为 "low"，报告中显示警告

- **全部达标** → 继续 Phase 3

> ⚠️ **clean.json 字段名校验**（Phase 3 前 MUST 确认）：`compute_metrics.py` 按固定字段名读取。确认 clean.json 中每题的字段名使用下划线命名（`question_type`、`cognitive_level`、`knowledge_point`），不得使用驼峰（`questionType`、`cognitiveLevel`）。任一字段名不匹配将导致 metrics.json 所有统计为 0 或"未知"。

### Phase 3: 量化指标计算

**单卷**：
- `scripts/compute_metrics.py temp/clean.json temp/metrics.json`
- `scripts/detect_duplicates.py temp/clean.json --output temp/duplicates.json`

**多卷**：对每个 `temp/clean_N.json` 分别运行，输出 `temp/metrics_N.json`、`temp/duplicates_N.json`。

### Phase 4: 确认模式（强制明确）

**必须向用户确认（使用以下精确交互格式）：**

> **AskUserQuestion（一次询问三个问题）：**
>
> **问题1 - 评价模式**：请选择评价模式
> - "整体评价"（推荐，token 最少）：全卷综合评分，速度最快
> - "抽样评价"：分层抽取 5-10 题逐题评价后推导全卷
> - "逐题评价"（token 最多）：每题独立评分，输出最详细
>
> **问题2 - 权重预设**：请选择评估权重标准
> - "默认权重"（推荐）：内容25%, 结构20%, 难度20%, 区分度15%, 规范20%
> - "升学考试"：侧重难度(30%)和区分度(25%)
> - "日常测验"：侧重内容(30%)和规范性(25%)
> - "竞赛选拔"：侧重区分度(30%)和难度(25%)
>
> **问题3 - 低置信度题型**（如有 confidence=低的题）：以下题目识别置信度较低，是否确认？
> [列出低置信度题目摘要]

用户未回复前 Do NOT 继续 Phase 5。

### Phase 5: Agent 评价

**评估前自问框架**（评分前 MUST 思考）：
- **内容效度**：这份试卷真的考查了它声称要考的内容吗？知识点与题型匹配是否恰当？
- **结构效度**：如果我是学生，能否从选项长度/格式猜出答案？干扰项是否"似是而非"？
- **难度控制**：真正理解的学生 vs 死记硬背的学生，得分差异会明显吗？
- **区分度潜力**：每道题都有明确的区分意图吗？还是只是"送分题"？
- **规范性**：题干表述有歧义吗？解析质量能帮助学生理解错误原因吗？
- **答案一致性**：每道题的答案真的回答了那个问题吗？是否有答非所问？
- **语言文字质量**：题干表述是否存在错别字、语病或标点问题？
- **内容错位**：是否有答案不属于本题、选项内容与题干无关的情况？

**MANDATORY - READ ENTIRE FILE**: 评分前 MUST 完整读取
[`references/evaluation_criteria.md`](references/evaluation_criteria.md)（51 行），严格按 10 分制细则评分。

**条件加载**：
- 用户要求分析认知层级分布 → 读取 [`references/bloom_taxonomy.md`](references/bloom_taxonomy.md)（18 行）
- 题型含简答/论述/案例分析等主观题 → 读取 [`references/question_types.md`](references/question_types.md)（19 行）
- 明确是职教/对口升学考试 → 读取 [`references/vocational_standards.md`](references/vocational_standards.md)（17 行）
- 用户明确指定权重场景（如"按升学考试标准评估"）→ 读取 `references/weights/` 下对应预设

**Do NOT load**：
- `bloom_taxonomy.md` — 只需整体评分或全是客观题（选择/判断/填空）
- `question_types.md` — 全是选择/判断/填空
- `vocational_standards.md` — 非职教考试
- **weights 预设文件** — 用户未指定权重场景时使用默认权重

**五维度：**
| 维度 | 默认权重 | 评分要点 |
|------|----------|----------|
| 内容效度 | 25% | 考点覆盖、考纲匹配、认知层级分布、答案与题干一致性、内容错位检测 |
| 结构效度 | 20% | 答案分布、选项设计、干扰项质量 |
| 难度控制 | 20% | 低中高比例、难度梯度 |
| 区分度潜力 | 15% | 区分不同水平学生、干扰项有效性 |
| 规范性 | 20% | 格式统一、题干清晰、解析质量、无重复、语言文字质量（错别字、语病、标点规范） |

**内容验证评分要点（Agent MUST 参考 clean.json 中的验证字段）：**
- `answer_verified: "suspicious"` 的题目：内容效度自动扣 1 分/题
- `linguistic_issues` 非空：规范性扣分 0.5 分/题（最多扣 3 分）
- `content_alignment` 非空：内容效度扣分 1 分/题
- 跨题答案矛盾：发现后每题在内容效度中扣 1-2 分

**评分规则：**
- 每题/全卷 五个维度各评 1-10 分
- **综合评分** = min(加权平均, 最低维度得分 + 2) — 短板机制
- 列出优秀项、需改进项、具体建议（P0/P1/P2 优先级）
**评价模式差异：**
- **整体模式**：全卷综合评分
- **抽样模式**：分层抽取 5-10 题逐题评价，推导全卷
- **逐题模式**：每题独立评分，输出详细明细

### Phase 5 Output: evaluation.json Schema

**MUST 严格按以下 Schema 输出，字段名必须完全匹配**（`generate_report.py` 按固定字段名读取，命名不一致将导致报告全部显示默认值/空白）：

```json
{
  "evaluation_mode": "overall",
  "overall_scores": {
    "内容效度": 7,
    "结构效度": 6,
    "难度控制": 8,
    "区分度潜力": 5,
    "规范性": 7
  },
  "dimension_details": {
    "内容效度": { "evidence": "考点覆盖了教材核心章节，但缺少xxx知识点..." },
    "结构效度": { "evidence": "选项分布基本均衡，但第5题最长选项偏差达40%..." },
    "难度控制": { "evidence": "低:中:高≈3:5:2，难度梯度合理..." },
    "区分度潜力": { "evidence": "多数题为记忆型，缺乏应用分析类题目..." },
    "规范性": { "evidence": "格式统一，但第3题题干存在歧义..." }
  },
  "weights": {
    "内容效度": 0.25,
    "结构效度": 0.20,
    "难度控制": 0.20,
    "区分度潜力": 0.15,
    "规范性": 0.20
  },
  "strengths": [
    "难度梯度设计合理，低中高比例为3:5:2",
    "选择题干扰项设计有效"
  ],
  "weaknesses": [
    "判断题答案严重偏向'正确'（占比75%），不符合命题规范",
    "缺少答案解析，规范性不足"
  ],
  "suggestions": [
    {
      "priority": "P0",
      "title": "调整判断题答案分布",
      "description": "将判断题正确/错误比例调整至接近1:1，避免答案一边倒"
    },
    {
      "priority": "P1",
      "title": "补充题目解析",
      "description": "为每道题添加详细解析，解释正确选项的原因和干扰项的排除理由"
    }
  ],
  "questions": [
    {
      "id": "1",
      "question_type": "选择题",
      "stem_summary": "下列关于xxx的说法正确的是",
      "scores": {
        "内容效度": 8,
        "结构效度": 7,
        "难度控制": 6,
        "区分度潜力": 5,
        "规范性": 8
      },
      "total_score": 6.7
    }
  ],
  "knowledge_points_summary": {
    "细胞结构": 3,
    "光合作用": 2,
    "遗传定律": 1
  }
}
```

**字段说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `evaluation_mode` | string | ✅ | `"overall"` / `"per_question"` / `"sampling"` |
| `overall_scores` | object | ✅ | 五个维度各评 1-10 分，键名必须用中文全称 |
| `dimension_details` | object | ✅ | 每维度含 `evidence` 字段，说明评分理由 |
| `weights` | object | ✅ | 五维度权重，值之和为 1.0 |
| `strengths` | array | ✅ | 优秀项列表，每项为字符串 |
| `weaknesses` | array | ✅ | 需改进项列表，每项为字符串 |
| `suggestions` | array | ✅ | 含 `priority`（P0/P1/P2）、`title`、`description` |
| `questions` | array | 逐题/抽样模式 | 含 `id`, `question_type`, `stem_summary`（≤30字）, `scores`（五维度）, `total_score` |
| `knowledge_points_summary` | object | ✅ | `{"知识点名称": 出现次数}`，用于词云图 |

> ⚠️ 字段名拼写错误（如 `overall_scores` 写成 `overallScores`、`scores` 或 `dimension_scores`）将导致 `generate_report.py` 的 `.get()` 全部返回默认值，报告显示综合评分 0.0、图表空白。

### Phase 5+ evaluation.json Schema 校验（MUST 执行）

写入 `temp/evaluation.json` 后，MUST 运行自动化校验脚本：

```bash
python scripts/validate_evaluation.py temp/evaluation.json [--mode overall|per_question|sampling]
```

**校验内容**（脚本内置）：
- `evaluation_mode` 有效性、"区分度"简写检测
- `overall_scores` 五维度完整 + 值域 [1,10]
- `weights` 键名与 `overall_scores` 一致 + 值之和 = 1.0
- `dimension_details` 五维度含 `evidence`
- `knowledge_points_summary` 非空
- `suggestions` 子字段 (`priority`/`title`/`description`)
- 逐题模式：`questions` 数组每项含 `id`/`scores`/`total_score`

**校验结果**：
- 输出 `✅ 全部校验通过` → 继续 Phase 6
- 输出 `❌ 校验失败 — N 个错误` → Do NOT 继续 Phase 6。根据输出的具体失败项修正 evaluation.json 后重新运行脚本，直到通过。

### Phase 6: 报告生成

**单卷**：
- `scripts/generate_report.py --metrics temp/metrics.json --evaluation temp/evaluation.json --duplicates temp/duplicates.json --output output/report.html`

**多卷**：
- 对每套试卷分别运行 `generate_report.py`，输出 `output/report_1.html`、`output/report_2.html`...
- 生成 `output/index.html` 汇总导航页，列出各卷名称、科目、题量和综合评分，提供链接跳转各卷详细报告。

**输出要求**（脚本不可用时 Agent 直接生成 HTML）：
1. Chart.js CDN（`https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js`）
2. 五维雷达图 + 题型分布饼图 + 难度分布图 + 认知层级环形图
3. 选择题答案分布柱状图（如有选择题）
4. 知识点分布词云图（从 `knowledge_points_summary` 生成，字体大小映射频次）
5. 五维度评分表（短板机制说明，"说明"列填充 `evidence` 字段）
6. 优秀项/需改进项/改进建议（P0/P1/P2 标签）
7. 每个图表下方解读文本（数据异常、合理之处、改进建议）

### Phase 7: 质量验证

交付前 MUST 执行以下自动化 + 手动验证：

**1. 自动化验证**：
```bash
# Schema 校验（如跳过 Phase 5+，此处补执行）
python scripts/validate_evaluation.py temp/evaluation.json [--mode overall|per_question|sampling]

# 报告文件存在性
test -f output/report.html && echo "✅ report.html 存在" || echo "❌ 缺失"
```

**2.5. 内容验证检查**：

读取 `temp/metrics.json` 的 `format_validation` 字段和 `temp/clean.json` 的验证字段，执行以下检查：

1. **格式问题联动检查**：
   - 遍历 `format_validation` 中的每个 issue
   - 检查该 issue 是否在 `evaluation.json` 的 `weaknesses` 或 `suggestions` 中得到回应
   - 未被回应的格式问题 MUST 生成新增建议项：
     ```
     suggestion: { "priority": "P1", "title": "修复格式问题", "description": "..." }
     ```

2. **可疑答案审查**：
   - 读取 `temp/clean.json`，检查 `questions` 数组中 `answer_verified` 为 `"suspicious"` 的题目
   - 如有 suspicious 条目，在 Phase 7 输出中列出：
     ```
     ⚠️ 发现 N 题答案标记为 suspicious，建议人工复核：
       - 第X题：题干摘要...
       - 第Y题：题干摘要...
     ```
   - 确认这些题目已在 evaluation 的 `weaknesses` 中得到回应（如"第X题答案存疑"）

3. **内容错位检查**（如有 `content_alignment` 非空题目）：
   - 确认对应题目在 evaluation 的 `weaknesses` 中有对应项
   - 未被回应的错位问题 MUST 生成建议项

**2. 手动验证**：
- [ ] 五个维度均有评分（1-10），综合评分计算正确（短板机制）
- [ ] HTML 文件可打开，图表（雷达图/饼图/柱状图/词云）正常渲染
- [ ] 逐题表数据完整（逐题/抽样模式下 questions 列数与总题数一致）
- [ ] 中文显示正常，无乱码
- [ ] 无"0.0"综合评分、无空白图表区域

**3. 验证失败处理**：
- 自动化验证失败 → 回 Phase 5+ 修正后重新运行
- 手动验证失败 → 回 Phase 6 修正报告生成

## 错误处理（按优先级排序）

**处理原则**：先处理 P0 → 再处理 P1 → 最后处理 P2。P0 无法解决则停止后续流程。

**P0 - 阻断级**（必须解决才能继续）：
- clean.json 为空 → 检查原始文件是否加密/损坏/格式不匹配，告知用户
- questions 数组为空 → 题型格式无法识别，告知用户

**P1 - 警告级**（继续但标注）：
- 解析质量=低 → 报告标题区标注 "⚠️ 解析质量低，部分数据可能不准确"
- 某题型题量 < 3 → 该题型指标仅供参考，不纳入综合评分

**P2 - 降级级**（跳过并注明）：
- compute_metrics.py 报错 → 检查 clean.json 格式后重试，仍失败则跳过量化指标
- detect_duplicates.py 报错 → 跳过重复检测，报告中注明 "未执行重复检测"
- generate_report.py 报错 → Agent 直接生成 HTML（见 Phase 6 fallback）

**多卷场景**：
- 无法明确分卷 → 按单卷处理，报告中注明"文档可能包含多套试卷但未明确分隔"
- 某卷题量 < 5 → 该卷单独标注"题量过少，评估结果仅供参考"

## 常见问题

| 问题 | 排查步骤 |
|------|----------|
| Excel 读取失败 | 确认文件未加密，检查是否为 .xls 旧格式（需 openpyxl 或 xlrd） |
| Excel 含多个工作表 | `parse_excel.py` 自动合并所有 sheet，若混入无关数据可在 Phase 2 过滤 |
| Word 文档含图片题 | 图片中的题干/选项无法被 `parse_docx.py` 提取，Agent 结构化时标记"图片题-需人工确认" |
| 认知层级仅 1-2 层 | 在建议中明确指出，降低内容效度评分 |
| 判断题答案一边倒 | P0 级问题，必须在 weaknesses 中突出显示 |
| 无解析字段 | 规范性评分降至 3-4 分，建议补充解析 |

## 输出

- 主文件：`output/report.html`（交互式可视化报告）
- 可选：`output/逐题明细.csv`（从 HTML 导出按钮下载）

| 评价模式/权重不一致 | evaluation_mode 与 questions 数组内容不匹配（如 mode="overall" 但有 questions 数据） |
| 权重键名不一致 | weights 的键与 overall_scores 的键不完全匹配 → 某维度权重被静默置0 |

## 权重预设文件

> ⚠️ **键名一致性约束**：所有权重预设文件的键名 MUST 与 `overall_scores` 完全一致，使用五维度的中文全称：`内容效度`、`结构效度`、`难度控制`、`区分度潜力`、`规范性`。不得使用简写（如"区分度"）。键名不匹配将导致对应维度权重被静默置0。

- `references/weights/升学考试.json` — 难度30%, 区分度潜力25%, 内容20%, 结构15%, 规范10%
- `references/weights/日常测验.json` — 内容30%, 规范25%, 难度20%, 结构15%, 区分度潜力10%
- `references/weights/竞赛选拔.json` — 区分度潜力30%, 难度25%, 内容20%, 结构15%, 规范10%
