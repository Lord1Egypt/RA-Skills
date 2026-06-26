# 对话框模型出题指南

Agent 执行 `generate-question-bank` 时必须遵循本指南，**禁止**调用 `app/services/ai_generator.py` 的本地模板出题。

## 出题流程

1. **提取资料**：运行 `extract_material.py` 或 Read 工具读取用户资料
2. **模型出题**：在当前对话中阅读资料全文，按下方规范生成题目 JSON
3. **写入 JSON**：保存到 `data/generated-bank.json`（或用户指定路径）
4. **导出 Excel**：运行 `export_question_bank.py` 生成 xlsx
5. **询问导入**：导出成功后询问用户是否导入刷题系统；若同意，运行 `import_bank_to_db.py`

## 生成参数（用户未指定时）

| 参数 | 默认 |
|------|------|
| 题量 | 20 |
| 题型 | 单选 + 判断 + 多选 |
| 题型顺序 | 先全部单选，再全部判断，最后全部多选 |
| 难度 | 中等（3/5） |

题量分配：总数按 3 种题型均分（余数依次给单选、判断、多选）。

## 强规则

1. **严格基于资料**，不得编造资料中不存在的事实
2. **题干仅含题目正文**，禁止「第 1 题」「第 2 题」等序号
3. **解析**紧扣资料，格式：`答案：X（选项摘要）。依据：……。错项：……。` 条理清晰，不冗余
4. 单选/多选提供 4 个选项；**判断题选项固定**：A=正确，B=错误（不打乱顺序）
5. **多选题**正确答案数量为 **2～4 个**（每题随机，不必固定 3 个），须保证至少 1 个错项
6. **判断题答案**：A 表示题干表述正确，B 表示题干表述错误；解析格式 `答案：A（正确）。依据：……。` 或 `答案：B（错误）。依据：……。`，**必须与 answer 字段一致**
7. 单选/多选生成时可将正确答案放在前几项，导出脚本会随机打乱选项并同步解析
8. 题目顺序在 JSON 中即按：单选 → 判断 → 多选

## JSON 格式

```json
{
  "title": "题库名称（取自资料或文件名）",
  "category": "未分类",
  "description": "基于资料自动生成 · 20 道题",
  "questions": [
    {
      "q_type": "single",
      "content": "根据资料，Python 中用于定义函数的关键字是？",
      "options": ["def", "function", "func", "define"],
      "answer": "A",
      "explanation": "答案：A。依据：资料明确指出使用 def 定义函数。错项：function/func/define 均非 Python 关键字。"
    },
    {
      "q_type": "judge",
      "content": "Python 中列表使用方括号定义。",
      "options": ["正确", "错误"],
      "answer": "A",
      "explanation": "答案：A（正确）。依据：资料说明列表用 [] 定义。"
    },
    {
      "q_type": "judge",
      "content": "Python 变量使用前必须先声明数据类型。",
      "options": ["正确", "错误"],
      "answer": "B",
      "explanation": "答案：B（错误）。依据：资料写明变量无需声明类型，直接赋值即可。"
    },
    {
      "q_type": "multiple",
      "content": "关于 Python 变量，以下哪些说法正确？（多选）",
      "options": ["变量无需声明类型", "变量名区分大小写", "变量必须先分配类型", "Python 没有变量"],
      "answer": "A,B",
      "explanation": "答案：A,B。依据：资料说明 Python 为动态类型且标识符区分大小写。C、D 与资料不符。"
    },
    {
      "q_type": "multiple",
      "content": "资料列出的算术运算符包括哪些？（多选）",
      "options": ["加(+)", "减(-)", "乘(*)", "按位与(&)"],
      "answer": "A,B,C",
      "explanation": "答案：A,B,C。依据：资料列举 +、-、*、/、//、%、**。按位与未提及。"
    }
  ]
}
```

## 导出命令

```bash
python skills/ai-question/scripts/export_question_bank.py data/generated-bank.json -o "输出题库.xlsx"
```

## 导入刷题系统（用户确认后）

```bash
python skills/ai-question/scripts/import_bank_to_db.py data/generated-bank.json
```

写入 `data/quizai.db`，可在 Web「我的题库」中刷题。

## 质量自检

导出前确认：

- [ ] 每题内容均能在资料中找到依据
- [ ] 题干无「第 N 题」前缀
- [ ] JSON 中题型顺序为单选 → 判断 → 多选
- [ ] 多选题正确答案数为 2～4 个（各题数量应有变化）
- [ ] 每题均有解析，且点明对错原因
- [ ] 题量与用户需求一致
- [ ] 导出后已询问用户是否导入刷题系统
