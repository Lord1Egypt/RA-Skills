# Edu Homework Grader · K-12 作业智能批改

[English](#english) | [中文](#chinese)

---

## English

Automated K-12 homework grading for Chinese, Math, English, Physics and Chemistry with rubric-based subjective evaluation.

### Quick Start

```bash
python3 scripts/run_pipeline.py \
  --input homework.txt --answer-key key.json \
  --subject math --grade 8 --output graded.json
python3 scripts/render_report.py --grading-result graded.json --format student
```

### Features

- 📝 5 subjects × all standard item types (MC, FIB, essay, math derivation, chem equations)
- 🎯 Rubric-driven subjective scoring with partial credit
- 🔍 Error classification (concept gap, calc slip, misread, etc.)
- 📊 Student / teacher / class report flavors
- 🇨🇳 Aligned with 人教版 / 北师大版 / 苏教版 curriculum codes

### License

MIT-0

---

## Chinese

覆盖 K-12 语数英物化的自动作业批改，主观题按 rubric 给部分分与文字反馈。

### 快速开始

```bash
python3 scripts/run_pipeline.py \
  --input 作业.txt --answer-key 答案.json \
  --subject math --grade 8 --output graded.json
python3 scripts/render_report.py --grading-result graded.json --format student
```

### 功能

- 📝 5 学科 × 全部常规题型（选择/填空/作文/推导/方程式）
- 🎯 Rubric 驱动的主观题部分分评分
- 🔍 错因分类（知识点缺失/计算失误/审题错误等）
- 📊 学生 / 教师 / 班级三种报告
- 🇨🇳 对接人教版/北师大版/苏教版课程标准代码

### 协议

MIT-0
