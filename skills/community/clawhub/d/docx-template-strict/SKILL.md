---
name: docx-template-strict
description: "Strictly fill a DOCX template (preserving cover/headers/sections/styles) using placeholder tokens, with optional figures and references. For any task like: ‘use this Word template to format/fill papers and keep the template layout identical’."
license: MIT
---

# docx-template-strict

目的：把 `.docx` 当作“模板”来用，**完整保留**模板的封面、分节（sectPr）、页眉页脚、样式、下划线 run 结构、字体与布局；只在模板中指定的占位符位置填充文本/图片/参考文献。

> 关键原则：**不要用 python-docx 重新生成段落结构**（这会破坏模板 run/sectPr）。
> 本 skill 采用：`docx(zip) → XML 精确替换 → 写回 docx`。

## 适用场景
- “按某个 Word 模板格式提交作业/论文/报告，封面与排版必须和模板一致”。
- 需要插图、图题、参考文献，同时保持模板视觉 1:1。

## 输入要求（模板必须包含占位符）

### 占位符格式
- 统一：`{{TOKEN_NAME}}`
- 必须是**连续字符串**，避免被 Word 拆成多个 run。

### 常用占位符（建议）
- `{{TITLE_CN}}` / `{{TITLE_EN}}`
- `{{NAME_CN}}` / `{{NAME_EN}}`
- `{{MAJOR}}` `{{CLASS}}` `{{STUDENT_ID}}`
- `{{COURSE}}` `{{TEACHER}}` `{{DATE_CN}}`
- `{{ABSTRACT_CN}}` `{{KEYWORDS_CN}}`
- `{{ABSTRACT_EN}}` `{{KEYWORDS_EN}}`

### 图占位符（段落级）
每张图推荐 3 段占位符（各占一整段，且仅包含该 token）：
- `{{FIG1}}`
- `{{FIG1_CAPTION_CN}}`
- `{{FIG1_CAPTION_EN}}`

第二张图：`FIG2` 同理。

### 参考文献占位符
- 推荐整块替换：`{{REFERENCES}}`（多行文本，包含 `[1]...`）

## 用法

### 1) 填充模板生成 docx
运行脚本：

```bash
python3 ~/.openclaw/skills/docx-template-strict/scripts/fill_template.py \
  --template "/path/to/template.docx" \
  --out "/path/to/output.docx" \
  --data "/path/to/data.json"
```

`data.json` 示例：
```json
{
  "TITLE_CN": "...",
  "TITLE_EN": "...",
  "NAME_CN": "林佩权",
  "NAME_EN": "Lin Peiquan",
  "ABSTRACT_CN": "...",
  "ABSTRACT_EN": "...",
  "KEYWORDS_CN": "...",
  "KEYWORDS_EN": "...",
  "REFERENCES": "[1] ...\n[2] ...\n"
}
```

### 2) 插图（可选）
在 `data.json` 中提供：
```json
{
  "FIG1": {"path": "/path/to/fig1.png"},
  "FIG2": {"path": "/path/to/fig2.jpg"}
}
```
脚本会：
- 把 `{{FIG1}}` 所在段落替换为图片 drawing
- 保留模板段落样式（对齐/缩进）

## 输出 QA（脚本自动做）
- 扫描是否仍存在 `{{...}}` 未替换 token
- 检查模板分节数量（sectPr）是否被破坏（必须一致）
- 检查 media 资源是否写入且 rels 指向有效

## 注意事项 / 已知限制
- 强依赖占位符：如果模板里没有 token，无法保证 1:1。
- 若 Word/WPS 将 token 拆成多个 run：脚本可能无法识别（建议复制 token 时使用“仅保留文本”）。
- PDF 导出不在本 skill 保真范围内：建议用本机 Word/WPS 导出 PDF，避免 LibreOffice 渲染漂移。
