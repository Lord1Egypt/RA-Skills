# exam-ocr-rebuilder

试卷OCR重建助手 — WorkBuddy Skill

## 功能简介

将 PDF 或图片格式的试卷，通过 OCR 识别 + AI 结构化解析 + LLM 审核校正，重建为清晰、可编辑的新试卷。

## 核心流程

1. **PDF 转图片** — PyMuPDF 逐页转换
2. **OCR 识别** — 优先使用 tencent-docs OCR（高精度模式）
3. **AI 结构化解析** — 识别题型、提取题干/选项/答案/解析、转 LaTeX 公式
4. **LLM 审核校正** — 大模型逐题审核，修正 OCR 识别错误
5. **多格式输出** — HTML 交互报告 + JSON 结构数据 + Markdown 试卷

## 支持题型

单选题、多选题、判断题、填空题、简答题、计算题、论述题、阅读理解、完形填空、证明题、作图题

## 文件结构

```
exam-ocr-rebuilder/
├── SKILL.md                          # 核心指令文件
├── scripts/
│   └── pdf_to_images.py              # PDF 转图片辅助脚本
└── references/
    ├── question-types.md             # 题型识别标准与正则规则
    ├── output-template.md            # 输出模板说明
    ├── llm-audit-prompt.md           # LLM 审核 Prompt 模板
    ├── ocr-tools-comparison.md       # OCR 工具对比
    ├── html-template-audit.html      # 含审核面板 HTML 模板
    ├── sample_exam_data.json         # 示例 JSON 数据
    └── sample_exam_report.html       # 示例 HTML 报告
```

## 安装使用

将此技能放入 WorkBuddy 技能目录：

```bash
cp -r exam-ocr-rebuilder ~/.workbuddy/skills/
```

## 依赖

- Python 3.8+
- PyMuPDF (fitz)
- tencent-docs MCP 连接器（可选，用于 OCR）

## 作者

bettermen

## License

MIT
