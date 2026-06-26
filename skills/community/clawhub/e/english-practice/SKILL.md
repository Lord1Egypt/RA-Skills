# English Practice - 英语练习册生成技能 v2.1

> 基于题库化 + 组卷化的英语练习生成系统  
> 更新日期：2026-03-14  
> 版本：v2.1

---

## 📚 功能说明

基于 AI 的英语练习册生成工具，支持：

- ✅ **题库化存储** - 单题入库，按题型统一 schema
- ✅ **组卷算法** - 按 blueprint 抽题，难度 + 标签分散
- ✅ **指纹去重** - 每题唯一 hash，防止重复
- ✅ **历史去重** - 7 天使用记录，避免每天同一套题
- ✅ **PDF 导出** - 学生版/教师版（含答案）
- ✅ **多版本** - 人教版（3-6 年级）、外研版（7-9 年级）
- ✅ **8 种题型** - 情景单选、完形填空、阅读理解、句型转换、词形转换、改错、语法填空、写作

---

## 🎯 核心架构

```
题库层 → 生成层 → 校验层 → 组卷层 → 导出层
```

### 架构说明

| 层级 | 职责 | 关键文件 |
|------|------|----------|
| **题库层** | 存储题目，按题型分表 | `question_bank_v2.json` |
| **生成层** | LLM/API 生成新题，人工补题 | `question_gen.py` |
| **校验层** | 结构校验、内容校验、去重校验 | `paper_assembler.py` |
| **组卷层** | 按 blueprint 抽题，难度控制 | `paper_assembler.py` |
| **导出层** | 编号、排版、PDF 生成 | `pdf_gen.py` |

---

## 📋 题库结构（v2.1 标准）

### 公共字段（每题都有）

```json
{
  "id": "cloze_001",
  "type": "cloze_test",
  "grade": 7,
  "version": "外研版",
  "difficulty": "medium",
  "tags": ["daily_life", "weather"],
  "source": "manual",
  "status": "approved",
  "fingerprint": "cloze_test:A Rainy Morning:This morning...",
  "created_at": "2026-03-14T22:00:00Z",
  "updated_at": "2026-03-14T22:00:00Z",
  "content": {}
}
```

| 字段 | 含义 | 示例 |
|------|------|------|
| id | 题目唯一 ID | `cloze_001` |
| type | 题型 | `cloze_test`, `reading_comprehension` |
| grade | 年级 | `7`, `8`, `9` |
| version | 教材版本 | `人教版`, `外研版` |
| difficulty | 难度 | `easy`, `medium`, `hard` |
| tags | 主题标签 | `["daily_life", "weather"]` |
| source | 来源 | `manual`, `api`, `llm` |
| status | 状态 | `draft`, `approved`, `rejected` |
| fingerprint | 去重指纹 | `type:title:passage_hash` |
| content | 题型具体内容 | 见下方各题型 schema |

---

## 📝 题型 Schema

### 1. 情景单选 (multiple_choice)

```json
{
  "type": "multiple_choice",
  "content": {
    "title": "Daily Conversation",
    "scenario": "thanking",
    "dialogue": "— Thank you for your help.\n— ______",
    "question": "Choose the best response:",
    "options": ["You're welcome", "Never mind", "That's right", "Good idea"],
    "answer": "You're welcome",
    "explanation": "对感谢的回答用 You're welcome"
  }
}
```

**必填字段**：title, dialogue, question, options(4 个), answer

### 2. 完形填空 (cloze_test)

```json
{
  "type": "cloze_test",
  "content": {
    "title": "A Rainy Morning",
    "passage": "This morning, I woke up... ___1___ ... ___2___ ...",
    "blanks": [
      {"id": 1, "answer": "umbrella", "options": ["umbrella", "ticket", "basket", "cap"]},
      {"id": 2, "answer": "earlier", "options": ["earlier", "later", "faster", "again"]}
    ],
    "word_count": 270,
    "explanation": "完形填空测试综合语言理解能力"
  }
}
```

**强校验**：
- passage 中的 `___1___` ... `___N___` 数量必须等于 blanks.length
- blanks[].id 必须连续
- 每个 options 必须 4 个
- answer 必须存在于 options

### 3. 阅读理解 (reading_comprehension)

```json
{
  "type": "reading_comprehension",
  "content": {
    "title": "The Power of Reading",
    "passage": "Reading is one of the most important skills...",
    "word_count": 180,
    "questions": [
      {
        "id": 1,
        "question": "What is the main benefit of reading?",
        "options": ["It helps us gain knowledge", "It makes us rich", "...", "..."],
        "answer": "It helps us gain knowledge",
        "explanation": "文章第一段明确提到"
      }
    ]
  }
}
```

**强校验**：
- 每篇阅读至少 3~5 小题
- 每小题 4 个选项
- answer 必须在 options 中

### 4. 句型转换 (sentence_transformation)

```json
{
  "type": "sentence_transformation",
  "content": {
    "title": "Sentence Transformation",
    "original": "Tom is interested in playing football.",
    "prompt": "Rewrite the sentence using the word in brackets",
    "target": "Tom is interested in ___ (play) football.",
    "answer": "playing",
    "grammar_point": "动名词"
  }
}
```

**必填字段**：original, prompt, target, answer

### 5. 词形转换 (word_formation)

```json
{
  "type": "word_formation",
  "content": {
    "title": "Word Formation",
    "root_word": "care",
    "sentence": "Be ___ when you cross the road.",
    "answer": "careful",
    "explanation": "care → careful (形容词)"
  }
}
```

**必填字段**：root_word, sentence, answer

### 6. 改错题 (error_correction)

```json
{
  "type": "error_correction",
  "content": {
    "title": "Error Correction",
    "sentence": "They was very happy yesterday.",
    "answer": "They were very happy yesterday.",
    "explanation": "主语是 They，be 动词应使用 were"
  }
}
```

**必填字段**：sentence, answer

### 7. 语法填空 (fill_blank)

```json
{
  "type": "fill_blank",
  "content": {
    "title": "Grammar Fill-in-the-Blank",
    "question": "She ___ (go) to school every day.",
    "blanks": [
      {"id": 1, "answer": "goes", "hint": "一般现在时"}
    ],
    "explanation": "一般现在时，第三人称单数动词加 -es"
  }
}
```

**必填字段**：question, blanks, blanks[].answer

### 8. 写作题 (writing)

```json
{
  "type": "writing",
  "content": {
    "title": "My Favorite Season",
    "prompt": "Write a short passage (60-80 words) about your favorite season.",
    "word_limit": "60-80 words",
    "requirements": ["Clear structure", "Correct grammar", "Relevant vocabulary"]
  }
}
```

**必填字段**：prompt, word_limit

---

## 🔧 组卷算法

### Blueprint（试卷模板）

```python
BLUEPRINT = {
    "multiple_choice": 2,
    "cloze_test": 4,
    "reading_comprehension": 5,
    "sentence_transformation": 2,
    "word_formation": 2,
    "error_correction": 2,
    "fill_blank": 2,
    "writing": 1
}
# 总计：20 道题
```

### 组卷流程

```python
# 1. 加载题库
question_bank = load_question_bank('question_bank_v2.json')

# 2. 筛选候选（过滤已使用、非 approved）
candidates = filter_candidates(
    question_bank=question_bank,
    qtype='cloze_test',
    grade=7,
    version='外研版',
    history_used_ids=used_last_7_days,
    used_ids_in_this_paper=current_paper_ids
)

# 3. 选题（难度 + 标签分散）
selected = select_questions(
    candidates=candidates,
    qtype='cloze_test',
    count=4
)

# 4. 校验 + 去重
validated = validate_and_dedup(
    new_questions=selected,
    question_bank=question_bank,
    current_paper_questions=paper_questions
)

# 5. 整卷校验
validate_full_paper(paper_questions)

# 6. 输出试卷
paper = build_paper_json(
    grade=7,
    version='外研版',
    questions=paper_questions
)
```

### 指纹生成规则

```python
def build_fingerprint(q):
    t = q['type']
    c = q['content']
    
    if t in ['cloze_test', 'reading_comprehension']:
        raw = f"{t}|{c.get('title')}|{c.get('passage')}"
    elif t == 'sentence_transformation':
        raw = f"{t}|{c.get('original')}|{c.get('target')}"
    elif t == 'word_formation':
        raw = f"{t}|{c.get('root_word')}|{c.get('sentence')}"
    elif t == 'error_correction':
        raw = f"{t}|{c.get('sentence')}"
    elif t == 'fill_blank':
        raw = f"{t}|{c.get('question')}"
    elif t == 'multiple_choice':
        raw = f"{t}|{c.get('dialogue')}|{json.dumps(c.get('options'))}"
    elif t == 'writing':
        raw = f"{t}|{c.get('prompt')}"
    
    return hashlib.md5(raw.encode('utf-8')).hexdigest()
```

---

## 💻 使用方法

### CLI 方式

```bash
# 生成练习册
english-practice generate --grade 7 --version 外研版 --count 20

# 指定题型
english-practice generate \
  --grade 7 \
  --version 外研版 \
  --types multiple_choice,cloze_test,reading \
  --output practice.pdf

# 生成 PDF
english-practice pdf \
  --input paper_demo.json \
  --output student.pdf \
  --with-answers teacher.pdf
```

### Python API

```python
from paper_assembler import generate_paper, load_question_bank

# 加载题库
question_bank = load_question_bank('question_bank_v2.json')

# 生成试卷
paper = generate_paper(
    question_bank=question_bank,
    grade=7,
    version='外研版',
    history_used_ids=set()  # 最近 7 天用过的题 ID
)

# 保存试卷
with open('paper.json', 'w', encoding='utf-8') as f:
    json.dump(paper, f, ensure_ascii=False, indent=2)

# 生成 PDF
from pdf_gen import PDFGenerator
pdf_gen = PDFGenerator()
pdf_gen.generate(
    practice_id=paper['paper_id'],
    questions=paper['questions'],
    version=paper['version'],
    grade=paper['grade'],
    with_answers=False  # 学生版
)
```

### 交互模式

```bash
english-practice interactive

# 交互式问答：
# 1. 选择年级：7
# 2. 选择版本：外研版
# 3. 选择题型：全选
# 4. 生成 PDF：是
```

---

## 🌐 API 端点

**基础 URL**: `http://101.34.62.112:8083`

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/practice/generate` | POST | 生成练习册 |
| `/api/practice/{paper_id}` | GET | 获取试卷详情 |
| `/api/pdf/generate/{paper_id}` | GET | 生成 PDF |
| `/api/answer-key/{paper_id}` | GET | 获取答案 |
| `/api/question/add` | POST | 添加新题到题库 |
| `/api/question/list` | GET | 查询题库 |

### 生成练习册请求示例

```bash
curl -X POST http://101.34.62.112:8083/api/practice/generate \
  -H "Content-Type: application/json" \
  -d '{
    "version": "外研版",
    "grade": 7,
    "question_types": ["multiple_choice", "cloze_test", "reading"],
    "question_count": 20
  }'
```

---

## 📁 文件结构

```
english-practice/
├── backend/
│   ├── question_bank_v2.json       # 标准化题库
│   ├── paper_assembler.py          # 组卷算法
│   ├── question_gen.py             # 题目生成
│   ├── pdf_gen.py                  # PDF 生成
│   └── main.py                     # API 服务
├── pdfs/
│   ├── paper_*_student.pdf         # 学生版
│   └── paper_*_teacher.pdf         # 教师版（含答案）
├── data/
│   └── questions_v2.db             # SQLite 题库
└── README.md
```

---

## 🎯 核心改进（v2.1）

| 问题 | v2.0 | v2.1 |
|------|------|------|
| 出题方式 | 单次生成整卷 | 题库 + 组卷 |
| 题目存储 | 整卷 JSON | 单题入库 |
| 去重方式 | 临时去重 | 指纹 hash |
| 质量管控 | 无审核 | draft/approved/rejected |
| 每天重复 | 无记录 | 7 天使用记录 |
| 难度控制 | 无 | easy/medium/hard |
| 主题分散 | 无 | 标签系统 |

---

## 📊 验证清单

生成试卷后，运行以下验证：

```bash
# 1. 验证题量
python3 -c "
import json
with open('paper.json') as f:
    paper = json.load(f)
print('题目总数:', len(paper['questions']))
"

# 2. 验证无重复
python3 -c "
from paper_assembler import validate_full_paper, load_question_bank
paper = load_question_bank('paper.json')
assert validate_full_paper(paper), '整卷校验失败'
print('✅ 整卷校验通过')
"

# 3. 验证题型分布
python3 -c "
from collections import Counter
types = Counter([q['type'] for q in paper['questions']])
for t, c in sorted(types.items()):
    print(f'  {t}: {c}道')
"
```

**预期输出**：
```
题目总数：20
✅ 整卷校验通过
  cloze_test: 4 道
  error_correction: 2 道
  fill_blank: 2 道
  multiple_choice: 2 道
  reading_comprehension: 5 道
  sentence_transformation: 2 道
  word_formation: 2 道
  writing: 1 道
```

---

## 🔧 依赖

```txt
Python 3.8+
FastAPI
uvicorn
reportlab (PDF 生成)
sqlite3
hashlib (指纹生成)
```

安装：
```bash
pip install fastapi uvicorn reportlab
```

---

## 📝 更新日志

### v2.1 (2026-03-14) - 题库化 + 组卷化
- ✅ 题库 JSON 标准结构（16 个公共字段）
- ✅ 8 种题型 content schema
- ✅ 组卷算法实现（6 个核心函数）
- ✅ 指纹去重（按题型生成唯一 hash）
- ✅ 标签分散（避免同主题堆积）
- ✅ 难度控制（easy/medium/hard）
- ✅ 整卷校验（题量、重复、状态）

### v2.0 (2026-03-14) - 去重机制
- ✅ key_for_question() 唯一键生成
- ✅ deduplicate_questions() 去重
- ✅ generate_with_dedup() 生成 + 去重 + 补题

### v1.0 (2026-03-10) - 初始版本
- 基础出题功能
- PDF 导出

---

## 📚 相关文档

- [ARCHITECTURE_V2.1.md](../../projects/english-practice/ARCHITECTURE_V2.1.md) - 架构设计
- [DELIVERY_REPORT.md](../../projects/english-practice/DELIVERY_REPORT.md) - 交付报告
- [成果汇报.md](../../projects/english-practice/成果汇报.md) - 实际成果展示

---

*技能版本：v2.1*  
*最后更新：2026-03-14*  
*维护者：老六 🥷*
