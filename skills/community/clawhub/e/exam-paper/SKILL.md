---
name: exam-paper
description: >
  【考试试卷生成器 | 题库管理 | 错题本】输入学科和题目数量，自动从题库随机抽题，生成考卷PDF和答案PDF两份文件。支持单选题、判断题、编程填空题。内置题库增删查、错题记录与复习标记功能。当前内置信息学奥赛22题，支持扩展其它学科。
  触发词：出卷、组卷、考试卷、试卷、生成试卷、生成考试、题库、错题本、错题库、错题记录、信息学奥赛、信息学竞赛、考试卷生成、考试题库、exam paper、generate exam、question bank、error tracking、错题复习、考前练习、自动组卷、考试PDF。
  当用户需要生成/导出考试试卷PDF、管理题目库、查看/记录错题时使用此技能。
---

# Exam Paper Generator - 考试试卷生成器

## 功能概览

| 功能 | 触发场景 |
|------|---------|
| 自动组卷生成PDF | "出一套信息学奥赛试卷" / "生成考试卷" |
| 题库管理 | "添加题目" / "查看题库" / "加题" |
| 错题追踪 | "记一下错题" / "查看错题" / "复习错题" |
| 扩展学科 | 新学科题库JSON，支持数学、英语等 |

## 数据目录
所有题库和错题数据存储在 `~/.qclaw/workspace/exam-data/`：
- `questions/` — 题库JSON文件（按学科命名，如 `informatics.json`）
- `errors/` — 错题记录JSON文件（如 `informatics_errors.json`）

## 工作流程

### 1. 生成试卷PDF
用户说"出一套信息学奥赛试卷"或"组卷"时：

1. 确认参数：学科（默认informatics）、题目数量、难度、知识点范围
2. 运行导出命令生成exam JSON：
   ```
   python -X utf8 <skill_dir>/scripts/manage_bank.py export --subject informatics --count 15 --outdir ~/.qclaw/workspace/exam-data
   ```
3. 运行PDF生成：
   ```
   python -X utf8 <skill_dir>/scripts/gen_pdf.py <exam.json> --outdir ~/Desktop
   ```
4. 确认输出两个PDF：试卷 + 答案

### 2. 管理题库
- **初始化**：`python -X utf8 <skill_dir>/scripts/manage_bank.py init`
- **查看题库**：`python -X utf8 <skill_dir>/scripts/manage_bank.py list --subject informatics`
- **添加题目**：准备符合格式的JSON文件，然后：
  `python -X utf8 <skill_dir>/scripts/manage_bank.py add <questions.json>`
- **随机选题**：`python -X utf8 <skill_dir>/scripts/manage_bank.py random --subject informatics --count 10`

### 3. 错题管理
- **记录错题**：`python -X utf8 <skill_dir>/scripts/manage_bank.py error-add <qid> <student_answer>`
- **查看错题**：`python -X utf8 <skill_dir>/scripts/manage_bank.py error-list --subject informatics`
- **标记已复习**：`python -X utf8 <skill_dir>/scripts/manage_bank.py error-mark <qid>`

## 添加新题目

题目JSON格式（添加到题库）：
```json
{
  "subject": "informatics",
  "questions": [
    {
      "id": "info_016",
      "type": "choice",
      "topic": "python",
      "difficulty": 1,
      "text": "题目内容（ ）。",
      "options": ["A. 选项1", "B. 选项2", "C. 选项3", "D. 选项4"],
      "answer": "B",
      "answer_desc": "简短答案",
      "explanation": "解析说明"
    }
  ]
}
```

题目类型(type)：
- `choice` — 选择题（需有options字段）
- `judgment` — 判断题（answer为"✓ 正确"或"✗ 错误"）
- `programming_fill` — 编程填空题（需有code和fills字段）

知识点(topic)参考：`references/informatics.md`

## 扩展新学科

1. 在 `exam-data/questions/` 创建新学科JSON（如 `math.json`）
2. 按相同格式添加题目（id前缀改为学科缩写，如 `math_001`）
3. 运行 `manage_bank.py add math_questions.json` 导入
4. 组卷时指定 `--subject math`

考试格式配置参考：`references/exam-formats.md`

## 注意事项

- 所有Python脚本必须用 `python -X utf8` 运行（Windows编码兼容）
- 生成PDF需要reportlab库（pip install reportlab）
- 题目id不能重复，添加时脚本会自动跳过已存在的id
- 编程填空题的code字段中，`<` 和 `>` 会在PDF渲染时自动转义

## ClawHub 发布信息
- 版本：1.0.0
- 技能ID：k97dw1dg2h2zae5arhpdnt7281864we0
- 安装：`clawhub install exam-paper`