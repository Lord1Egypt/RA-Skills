# 输出模板

本目录包含以下输出模板文件：

| 文件 | 说明 |
|------|------|
| `output-template.md`（本文件） | JSON结构模板 + Markdown试卷模板 |
| `html-template-audit.html` | 含LLM审核面板的完整HTML交互报告模板 |
| `llm-audit-prompt.md` | LLM审核检查Prompt模板 |
| `question-types.md` | 题型分类标准与正则规则 |
| `ocr-tools-comparison.md` | OCR工具对比与选择指南 |

---

## HTML报告功能特性

生成的HTML交互报告（`html-template-audit.html`）包含以下功能：

1. **试卷预览**：按原试卷结构展示所有题目
2. **题型筛选**：点击题型标签筛选显示
3. **答案切换**：显示/隐藏答案开关
4. **LLM审核报告面板**（新增）：右下角悬浮按钮 → 显示审核统计和逐题审核说明
5. **审核状态角标**：每题右上角显示审核状态（✅无需修改 / ✏️已校正 / ⚠️需复核 / ❌失败）
6. **统计面板**：题型分布、分值统计、题目数量
7. **导出功能**：一键导出为Markdown、导出JSON
8. **LaTeX公式渲染**：使用KaTeX CDN自动渲染

### 审核面板说明

LLM审核步骤会生成 `audit_log` 数组，包含每题的：
- `status`：ok / corrected / warning / error
- `confidence`：high / medium / low
- `issues`：修正说明数组

HTML报告读取 `audit_log`，在悬浮面板中展示统计和逐题说明，并在题目上标注状态角标。

---

## 1. JSON结构模板

OCR识别+结构化解析+LLM审核后的完整JSON格式：

```json
{
  "exam_info": {
    "title": "2024年高考数学模拟试卷",
    "subject": "数学",
    "total_score": 150,
    "duration": "120分钟",
    "source": "OCR识别重建",
    "ocr_date": "2025-06-29",
    "original_format": "PDF",
    "audit_enabled": true,
    "audit_model": "gpt-4o / claude-3.5 / hunyuan"
  },
  "sections": [
    {
      "section_id": 1,
      "section_title": "一、单项选择题",
      "section_type": "single_choice",
      "section_score": 40,
      "section_instruction": "本题共8小题，每小题5分，共40分。",
      "questions": [
        {
          "question_id": 1,
          "type": "single_choice",
          "score": 5,
          "stem": "设函数 $f(x) = x^2 + 2x + 1$，则 $f(0) = $",
          "options": {
            "A": "0",
            "B": "1",
            "C": "2",
            "D": "3"
          },
          "answer": "B",
          "explanation": "将 $x=0$ 代入得 $f(0) = 0^2 + 2 \\times 0 + 1 = 1$。",
          "image_refs": [],
          "latex_formulas": ["f(x) = x^2 + 2x + 1", "f(0)"],
          "audit": {
            "status": "corrected",
            "confidence": "high",
            "issues": [
              "题干'没函数'修正为'设函数'（同音字OCR错误）",
              "LaTeX公式 x2 修正为 x^2（上标丢失）"
            ],
            "original_ocr": "没函数 f(x) = x2 + 2x + 1，则 f(0) = "
          }
        }
      ]
    }
  ],
  "audit_log": [
    {
      "question_id": 1,
      "status": "corrected",
      "confidence": "high",
      "issues": ["题干'没函数'修正为'设函数'", "LaTeX公式修正"]
    }
  ],
  "stats": {
    "total_questions": 10,
    "total_sections": 3,
    "total_score": 150,
    "type_distribution": {
      "single_choice": 8,
      "fill_blank": 4,
      "calculation": 5
    },
    "audit_stats": {
      "ok": 6,
      "corrected": 3,
      "warning": 1,
      "error": 0
    },
    "has_answers": true,
    "has_explanations": true
  }
}
```

### audit 字段说明

每道题可包含 `audit` 对象（LLM审核后添加）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | ok / corrected / warning / error |
| `confidence` | string | high / medium / low |
| `issues` | string[] | 修正说明列表 |
| `original_ocr` | string | 原始OCR文本（用于对比） |

---

## 2. Markdown试卷模板

```markdown
# {exam_title}

**学科**：{subject}  **总分**：{total_score}分  **时间**：{duration}

---

## 一、单项选择题（共{N}题，每题{M}分）

**1.** {题干文本}

A. {选项A}
B. {选项B}
C. {选项C}
D. {选项D}

<details>
<summary>查看答案</summary>

**答案：** {答案}

{解析}

</details>

---

**2.** {题干文本}

...

---

## 二、填空题（共{N}题，每题{M}分）

**9.** {题干文本（含下划线___或括号）}

<details>
<summary>查看答案</summary>

**答案：** {答案}

</details>

---

## 三、解答题（共{N}题，共{total_score}分）

**17.**（{M}分）{题干文本}

<details>
<summary>查看答案</summary>

**解：**

{答案/解答过程}

</details>

---

*本试卷由 exam-ocr-rebuilder 自动识别重建*
*LLM审核：{audit_enabled} | 校正：{audit_corrected}题 | 需复核：{audit_warning}题*
*生成时间：{date}*
```

---

## 3. HTML报告生成要点

生成HTML时，将JSON数据嵌入为JS变量：

```html
<script>
    var EXAM_DATA = /* 此处填入完整JSON */;
    var AUDIT_LOG = EXAM_DATA.audit_log || [];
</script>
```

审核面板在HTML中的位置：
- 悬浮按钮：固定定位右下角（`position: fixed; bottom: 24px; right: 24px;`）
- 审核面板：按钮上方展开（`bottom: 80px;`）
- 题目状态角标：绝对定位在 `.question` 右上角

详见 `html-template-audit.html` 完整模板。
