# Deep Research to PPT Pro v2.0

> 一键将深度研究报告转化为高质量 PPT 演示文稿

## 功能特性

| 特性 | 说明 |
|------|------|
| 深度研究 | 通过 ZeeLin DeSearch API 自动生成万字研究报告 |
| 数据验证 | 所有数据声明仅从 .gov 域名验证，标注来源网址 |
| 原创概念 | 每份报告提出 3-5 个团队首创概念 |
| 图片生成 | 使用 Gemini API 批量生成手绘风格幻灯片图片 |
| OCR 核验 | 自动检测错字/漏字/乱码，不合格页面自动重生成 |
| 弹性页数 | 根据报告实际内容调整，不强制凑页数 |
| 内容溯源 | PPT 文字 100% 来自报告原文 |

## 快速开始

1. 将 `.env` 文件中的 API Key 替换为你自己的
2. 按照 `SKILL.md` 中的 6 个阶段依次执行
3. 最终产出：PPTX + PDF + Markdown 研究报告

## 目录结构

```
desearch-ppt/
├── SKILL.md                          # 主文件（Agent 执行指南）
├── README.md                         # 本文件
├── .env                              # 环境变量配置
├── references/
│   ├── zeelin_api.md                 # ZeeLin API 调用指南
│   ├── slide_structure.md            # PPT 结构与布局规范
│   └── prompt_design.md              # 图片提示词设计规范
└── scripts/
    ├── data_validator.py             # 数据声明提取与验证
    ├── concept_generator.py          # 原创概念生成器
    ├── report_to_ppt_outline.py      # 报告到PPT大纲转换
    ├── outline_to_prompts.py         # 大纲到提示词转换
    ├── generate_and_assemble.py      # 图片生成与组装（Linux/Mac）
    ├── generate_and_assemble_win.py  # 图片生成与组装（Windows）
    └── ocr_validator.py              # OCR 文字核验器
```

## 依赖安装

```bash
# Python 依赖
pip install google-genai pillow fpdf2 python-pptx pytesseract python-Levenshtein requests

# Tesseract OCR（Linux）
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim

# Tesseract OCR（Windows）
# 下载安装：https://github.com/UB-Mannheim/tesseract/wiki
```

## 版本历史

- **v2.0** (2026-03): 新增数据验证、原创概念、OCR核验、弹性页数、内容溯源
- **v1.0** (2025-12): 初始版本，基础研究报告到PPT转换
