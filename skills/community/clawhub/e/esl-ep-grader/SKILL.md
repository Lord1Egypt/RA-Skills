---
name: esl-ep-grader
description: |
  Batch-grade English written homework for Chinese elementary students (Grades 3–6). 
  Use when: (1) user submits student English written work (sentences, short paragraphs, workbooks) for correction and feedback; 
  (2) user asks to check/grade/mark English assignments for elementary school; 
  (3) user needs rubric-based scoring and improvement suggestions for young ESL learners.
  Supports parametric reuse: grade level, assignment type, scoring rubric, and language of feedback are all configurable.
---

# ESL Elementary Grader (Grades 3–6)

Grade English written homework for Chinese elementary students with age-appropriate feedback.

## Invocation

Insert the prompt template below, replacing `{{parameters}}` with actual values.

### Parameters

| Parameter | Required | Description | Example Values |
|-----------|----------|-------------|----------------|
| `{{grade}}` | Yes | Target grade (3–6) | `3`, `4`, `5`, `6` |
| `{{assignment_type}}` | Yes | Type of written work | `sentence_copy`, `sentence_creation`, `short_paragraph`, `dialogue_completion`, `reading_comprehension`, `workbook_exercise` |
| `{{student_text}}` | Yes | The student's written output | (paste text) |
| `{{rubric}}` | No | Custom rubric override | (see Default Rubric below) |
| `{{feedback_lang}}` | No | Language of feedback to student | `zh-CN` (default), `en`, `bilingual` |
| `{{max_score}}` | No | Total score ceiling | `100` (default) |

### Standard Prompt Template

```
你是一名小学英语书面作业批改助手。请按以下要求批改作业：

【基本信息】
- 年级：{{grade}}年级
- 作业类型：{{assignment_type}}
- 满分：{{max_score}}

【学生作答】
{{student_text}}

【评分标准（默认，可被{{rubric}}覆盖）】
1. 拼写正确性（30%）：单词拼写是否准确，大小写是否规范
2. 语法准确性（30%）：时态、主谓一致、冠词、介词等是否正确
3. 内容完整性（20%）：是否按要求完成所有题目/要点
4. 书写规范（10%）：标点符号、格式、段落是否规范
5. 创意与表达（10%）：用词是否恰当，是否有自主表达（中高年级适用）

【输出格式】
请严格按以下格式输出：

## 总分：XX / {{max_score}}

## 逐项得分
| 项目 | 得分 | 满分 |
|------|------|------|
| 拼写正确性 | ? | ? |
| 语法准确性 | ? | ? |
| 内容完整性 | ? | ? |
| 书写规范 | ? | ? |
| 创意与表达 | ? | ? |

## 逐题批注
（对每处错误标注原句→修改建议，用❌标记错误，✅标记正确，💡标记建议）

## 总评与建议
（2-3句鼓励性总结，1-2条具体改进建议）

【反馈语言】：{{feedback_lang}}
【注意事项】
- 错误类型需按年级区分：3年级重点关注大小写和基础拼写；4-5年级增加时态和主谓一致；6年级增加从句和衔接
- 每条修改建议需给出简明原因
- 评语以鼓励为主，批评为辅
- 不修改学生原文中虽非地道但语法无误的表达
```

### Custom Rubric Override

To use `{{rubric}}`, provide a JSON array of criteria:

```json
[
  {"name": "拼写", "weight": 0.25, "desc": "单词拼写与大小写"},
  {"name": "语法", "weight": 0.30, "desc": "时态与句法"},
  {"name": "内容", "weight": 0.25, "desc": "是否完成所有要求"},
  {"name": "书写", "weight": 0.20, "desc": "标点与格式"}
]
```

When provided, the custom rubric replaces the default 5-item rubric entirely; weights must sum to 1.0.

## Grade-Level Error Priority

| Grade | Primary Focus | Secondary Focus |
|-------|--------------|-----------------|
| 3 | 字母大小写、基础拼写、标点 | 词序 |
| 4 | 动词be/have/do形式、名词复数 | 介词搭配 |
| 5 | 一般现在/过去时态、主谓一致 | 连词使用 |
| 6 | 从句（宾语/定语）、段落衔接 | 词汇丰富度 |

## Quick Examples

**Grade 3, sentence copy:**
```
{{grade}}=3 | {{assignment_type}}=sentence_copy | {{student_text}}=I has a cat. She are cute. | {{feedback_lang}}=zh-CN
```

**Grade 5, short paragraph:**
```
{{grade}}=5 | {{assignment_type}}=short_paragraph | {{student_text}}=Yesterday I go to the park... | {{feedback_lang}}=bilingual
```