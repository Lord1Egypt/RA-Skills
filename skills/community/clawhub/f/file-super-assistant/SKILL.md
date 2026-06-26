---
name: file-super-assistant
description: 文件创建与 AI 降味助手。支持 docx/xlsx/pptx/pdf 文件创建和编辑，提供 AI 内容改写为人类风格功能。
---

# File Super Assistant - 文件超级助手

## 核心功能

### 1. 文件创建与编写

| 文件类型 | 支持操作 | 工具/库 |
|----------|----------|---------|
| **Word 文档** (.docx) | 创建、编辑、格式化、插入表格/图片 | python-docx |
| **Excel 表格** (.xlsx) | 创建、数据填充、公式、图表 | openpyxl / pandas |
| **PPT 演示** (.pptx) | 创建幻灯片、模板应用、动画 | python-pptx |
| **PDF 文件** (.pdf) | 生成、合并、拆分、水印 | reportlab / PyPDF2 |

### 2. AI 内容"降味"

将 AI 生成的内容改写为更自然、更像人类写作的风格。

**AI 味特征（需要避免）：**
- 过度使用"首先、其次、最后"等连接词
- 句式过于工整、缺乏变化
- 语气过于正式、缺乏情感
- 堆砌形容词、副词
- 缺乏个人体验和具体细节

**降味技巧：**
- 加入口语化表达、语气词
- 变化句式长短、结构
- 加入个人经历、具体案例
- 适当使用反问、设问
- 加入情绪表达、主观评价

---

## 使用流程

### 创建文档

```bash
# 调用脚本创建文档
python scripts/create_doc.py --type docx --output "报告.docx" --content "内容..."
```

### 降 AI 味

```bash
# 调用脚本处理 AI 内容
python scripts/remove_ai_flavor.py --input "ai_text.txt" --output "human_text.txt"
```

---

## 脚本说明

### scripts/create_doc.py

**功能：** 创建各类文档文件

**参数：**
- `--type`: 文件类型 (docx/xlsx/pptx/pdf)
- `--output`: 输出文件名
- `--content`: 内容（或从 stdin 读取）
- `--template`: 可选模板文件

**示例：**
```bash
python scripts/create_doc.py --type docx --output "周报.docx" --content "本周工作内容..."
python scripts/create_doc.py --type xlsx --output "数据表.xlsx" --data data.csv
python scripts/create_doc.py --type pptx --output "汇报.pptx" --template assets/template.pptx
```

### scripts/remove_ai_flavor.py

**功能：** 将 AI 生成内容改写为人类风格

**参数：**
- `--input`: 输入文件（AI 生成的内容）
- `--output`: 输出文件（处理后的人类风格）
- `--style`: 风格选项 (casual/professional/story)
- `--intensity`: 降味强度 (1-5，默认 3)

**示例：**
```bash
python scripts/remove_ai_flavor.py --input "article.txt" --output "article_human.txt"
python scripts/remove_ai_flavor.py --input "post.txt" --output "post_human.txt" --style casual --intensity 4
```

---

## 降味规则参考

详见 `references/ai-flavor-rules.md`

---

## 文件模板

### assets/templates/

- `docx_report_template.docx` - 报告模板
- `pptx_business_template.pptx` - 商务 PPT 模板
- `xlsx_data_template.xlsx` - 数据表格模板

---

## 使用场景

### 场景 1：创建周报

```
用户：帮我写一份周报
→ 使用 create_doc.py 创建 docx 文件
→ 调用 remove_ai_flavor.py 降味
→ 输出自然的人类风格周报
```

### 场景 2：制作 PPT

```
用户：做个产品汇报 PPT
→ 使用 assets 中的商务模板
→ 用 create_doc.py 生成 pptx
→ 人工微调
```

### 场景 3：文章去 AI 味

```
用户：这篇文章 AI 味太重了，帮我改改
→ 调用 remove_ai_flavor.py
→ 选择 casual 风格，强度 4
→ 输出更自然的文章
```

---

## 注意事项

1. **文件路径**：所有文件路径使用绝对路径或相对于 workspace 的路径
2. **编码问题**：中文文件使用 UTF-8 编码
3. **字体问题**：Windows 使用中文字体（宋体、微软雅黑）
4. **降味适度**：不要过度降味导致内容失真

---

## 相关资源

- `scripts/create_doc.py` - 文档创建脚本
- `scripts/remove_ai_flavor.py` - AI 降味脚本
- `references/ai-flavor-rules.md` - AI 味特征与降味规则
- `assets/templates/` - 文件模板
