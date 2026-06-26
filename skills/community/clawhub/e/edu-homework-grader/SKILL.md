---
name: edu-homework-grader
description: |
  EN: Automated K-12 homework grading for Chinese, Math, English, Physics and Chemistry. Handles objective items (multiple-choice, fill-in-the-blank, true/false) with deterministic scoring, and subjective items (essays, short answers, math derivations) with rubric-based partial-credit evaluation. Produces per-student score sheet, common-error analysis, and personalized improvement suggestions. Use when user provides homework text/photos and asks "批改作业 / 改卷 / 评分 / grade homework".
  中文：覆盖 K-12 语数英物化的自动作业批改。客观题（选择/填空/判断）按答案模板确定性评分；主观题（作文/简答/数学推导）按 rubric 给出部分分与文字反馈。输出每生成绩、共性错误分析、个性化提升建议。当用户提供作业内容并要求"批改/改卷/评分"时触发。
version: 1.0.0
metadata:
  openclaw:
    emoji: "📝"
    homepage: https://github.com/openclaw-skills/edu-homework-grader
    requires:
      bins:
        - python3
    envVars:
      - name: GRADER_CURRICULUM_REGION
        required: false
        description: Curriculum region hint, one of `RPEP|BNUEP|JSEP|HKDSE|US-CCSS`. Defaults to RPEP (人教版).
      - name: GRADER_OCR_ENGINE
        required: false
        description: Override OCR engine for handwritten input. Defaults to bundled tesseract+layout post-processor.
---

# Edu Homework Grader · K-12 作业智能批改

> Rubric-driven, evidence-backed grading that explains *why* each point was lost, not just the score. Designed for teachers, tutors, and self-study learners.
>
> 不只是给分，更告诉学生**为什么扣分**。按 rubric 评分、按知识点归因、按个体出建议，给老师、家教与自学者使用。

---

## 🎯 When to Use · 何时使用

**Trigger keywords (中文):** 批改作业、改卷、判作业、评分、给分、作文批改、数学批改、英语批改、错题分析、知识点诊断

**Trigger keywords (EN):** grade homework, mark assignment, essay scoring, rubric grading, error analysis, concept gap detection

**Supported subjects & item types:**

| 学科 / Subject | 题型 / Item Types |
|---|---|
| 语文 Chinese | 选择/填空/默写/阅读理解/作文 |
| 数学 Math | 选择/填空/计算/解答题/几何证明 |
| 英语 English | 选择/完形/阅读/翻译/作文 |
| 物理 Physics | 选择/填空/实验/计算/推导 |
| 化学 Chemistry | 选择/填空/方程式/实验/计算 |

**Do NOT use when:**
- Input has no answer key and no rubric (the grader needs ground truth or scoring criteria)
- User asks the grader to do the homework instead of grading it
- Subjective grading without rubric for high-stakes exams (always require human teacher final review for graded transcripts)

---

## 📋 Grading Pipeline · 批改流程

### Step 1: Input parsing · 输入解析

Accepted inputs:
- Text (questions + student answers + answer key)
- Image (photo of handwritten or printed homework) — auto-routed through OCR
- PDF (multi-page exam papers)
- Excel/CSV (batch grading roster)

```bash
python3 scripts/parse_input.py --input <file-or-stdin> --format auto
```

### Step 2: Question type detection · 题型识别

`scripts/detect_item_types.py` classifies each item into one of:
- `MC` multiple-choice (single/multi-correct)
- `FIB` fill-in-the-blank
- `TF` true/false
- `SA` short-answer
- `ESSAY` extended essay
- `MATH_DERIV` math derivation/proof
- `CHEM_EQ` chemistry equation
- `LANG_TRANSLATE` translation

### Step 3: Scoring · 评分

Two paths:

**Objective items** (`MC`, `FIB`, `TF`, `CHEM_EQ`):
- Strict match against answer key
- For `FIB`: normalize whitespace, full/half-width chars, accept synonym set from `knowledge/synonym_<subject>.json`
- For `CHEM_EQ`: balance and stoichiometry check via `scripts/chem_eq_check.py`

**Subjective items** (`SA`, `ESSAY`, `MATH_DERIV`, `LANG_TRANSLATE`):
- Apply rubric from `templates/rubric_<subject>_<grade>.json`
- For `MATH_DERIV`: step-by-step credit using `scripts/math_step_grader.py` (each correct step gets partial credit, even if final answer is wrong)
- For `ESSAY`: 6-dimension scoring (内容/结构/语言/书写/创意/规范) with LLM-assisted evaluation grounded in rubric
- For `LANG_TRANSLATE`: BLEU + grammatical correctness + key-term coverage

### Step 4: Error analysis · 错因归因

`scripts/diagnose_errors.py` classifies each wrong answer into:
- 知识点缺失 (Concept gap) — links to specific curriculum standard code
- 概念混淆 (Concept confusion)
- 计算失误 (Calculation slip)
- 审题错误 (Misreading question)
- 表达不规范 (Notation/format violation)
- 应试技巧 (Test-taking strategy)

### Step 5: Report generation · 报告生成

```bash
python3 scripts/render_report.py --grading-result graded.json --format student|teacher|class
```

Three report flavors:
- **Student report** — per-question feedback, encouragement, study suggestions
- **Teacher report** — class-level statistics, common errors, knowledge-point heatmap
- **Class report** — for class management systems, includes CSV/Excel export

---

## 📤 Output Format · 输出格式

```json
{
  "assignment": { "title": "...", "subject": "math", "grade": 8, "total_points": 100 },
  "students": [
    {
      "student_id": "S001",
      "name": "张三",
      "score": 87,
      "items": [
        {
          "item_id": "Q5",
          "type": "MATH_DERIV",
          "earned": 8,
          "max": 10,
          "feedback": "第二步因式分解正确，第三步符号错误导致后续计算偏差",
          "error_class": "计算失误",
          "knowledge_points": ["二次方程求根公式", "代数式化简"]
        }
      ],
      "improvement_plan": [
        "重点复习：一元二次方程求根公式（人教版数学九年级上 第21章）",
        "推荐练习：教材 P52 习题 21.2 第 3、5、7 题"
      ]
    }
  ],
  "class_stats": { "mean": 78.5, "median": 80, "stddev": 12.3, "knowledge_point_heatmap": {...} }
}
```

---

## ⚠️ Safety & Compliance · 安全合规

1. **Grader is an aid, not the final authority** — every report includes a "请教师终审" notice for graded transcripts.
2. **No student PII to external services** — all OCR and LLM processing happens through the assistant's configured providers per the user's setup; the skill itself never makes independent network calls.
3. **Bias mitigation** — essay rubrics are anchored to standard curriculum criteria; no personal-attribute features (gender, name, ethnicity) feed into scoring.
4. **Transparent rubrics** — all rubrics are stored as human-readable JSON in `templates/`, fully auditable and editable.
5. **Score appeal trail** — every score has a reasoning trace (`why_lost_points` field) supporting student appeals.

> 批改结果仅作教学辅助，正式成绩需教师终审；不向外部服务上传学生信息；评分依据公开 rubric；保留完整的扣分推理链以便申诉复核。

---

## 🚀 Usage Examples · 使用示例

### Example 1: Single student math homework

```bash
python3 scripts/run_pipeline.py \
  --input homework_zhangsan.txt \
  --answer-key key.json \
  --subject math --grade 8 \
  --output graded.json
python3 scripts/render_report.py --grading-result graded.json --format student
```

### Example 2: Batch grade an entire class

```bash
python3 scripts/batch_grade.py \
  --roster class_8a.csv \
  --homework-dir ./submissions/ \
  --answer-key key.json \
  --rubric rubric_math_g8.json \
  --output class_report.xlsx
```

### Example 3: Essay scoring with custom rubric

```bash
python3 scripts/grade_essay.py \
  --essay essay.txt \
  --rubric my_rubric.json \
  --output essay_feedback.md
```

### Example 4: Photo of handwritten homework

```bash
python3 scripts/run_pipeline.py \
  --input photo.jpg \
  --answer-key key.json \
  --ocr --subject chinese --grade 5
```

---

## 🧪 Testing · 测试

```bash
cd tests && python3 -m pytest -v
```

Coverage includes:
- 5 subjects × 3 grade levels = 15 reference assignments
- Edge cases: blank answers, partial OCR garbage, ambiguous Chinese characters, half/full-width digits
- Rubric stability tests (same input → same score within ±2%)

---

## 📚 References · 参考资料

- 教育部《义务教育课程标准（2022 年版）》
- 人教版/北师大版/苏教版各年级教材章节代码表（`knowledge/curriculum_<region>.csv`）
- BLEU score for translation: Papineni et al., 2002
- Educational rubric design: Andrade, 2005

## 🏷️ Tags · 标签

`education` `K12` `homework-grading` `rubric` `essay-scoring` `error-analysis` `教育` `K12` `作业批改` `自动评分`
