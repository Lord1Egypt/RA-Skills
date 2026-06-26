---
name: bidding-document-parser
description: 招标文件解析助手。自动解析招标文档（PDF/DOCX/TXT），提取资格审查项、废标项、评分标准、技术要求、装订要求、格式要求等6类关键信息，默认输出为结构化Word（DOCX）报告，带PDF原始页码标注。
---

# 招标文件解析 SKILL

## 概述
本SKILL用于解析招标文件，自动识别并提取6类关键信息，生成结构化的Word（DOCX）分析报告（带PDF原始页码标注）。

## 触发条件
当用户输入以下任一内容时，应加载本SKILL：
- 关键词："解析招标文件"、"分析招标文档"、"提取招标要点"、"招标文件解析"
- 上传招标相关文件（PDF、DOCX、TXT）
- 提供招标文件文本内容

---

## 工作流程

### 步骤1：获取招标文件内容

根据输入类型选择解析方式：

**输入为PDF文件** ⚠️ 必须使用带页码的PDF转换工具
- **使用Python脚本** `scripts/extract_pdf_with_pages.py`（基于pdfplumber库，保留页码信息）
- 执行命令：
  ```bash
  cd "[workspace]"
  py scripts/extract_pdf_with_pages.py "PDF文件路径"
  # 或指定输出路径
  py scripts/extract_pdf_with_pages.py "PDF文件路径" "输出TXT路径"
  ```
- 输出文件：`<PDF文件名>_带页码.txt`（默认与PDF同目录）
- ⚠️ 禁止使用 `@pdf` skill（无法保留页码信息）

**输入为DOCX文件**
- 使用 `@docx` skill 读取内容
- 或使用 `Markdown Converter` skill 转换

**输入为文本内容**
- 直接使用提供的文本

**输入为文件路径**
- 根据扩展名选择上述对应方式

---

### 步骤2：提取6类关键信息

**使用方法**：读取 `references/extraction_prompt.md` 文件，获取完整的提取提示词模板。

**执行步骤**：
1. 读取 `references/extraction_prompt.md` 文件内容
2. 将招标文件内容插入到模板的 `[在此插入招标文件文本内容]` 位置
3. 使用填充后的提示词模板进行信息提取
4. 按照模板中的表格格式输出6类关键信息

**提取的6类信息**：
1. 资格审查项
2. 废标项/取消资格项
3. 评分标准得分项/加分项
4. 技术要求
5. 装订要求
6. 格式要求

**⚠️ 重要**：
- 凡涉及"废标"、"取消资格"、"投标作废"、"投标文件作废"、"无效标"等描述的条款，均应列入废标项
- 必须添加PDF原始页码标注（格式：`P5`、`P9-10`）

---

### 步骤3：生成Markdown报告（中间格式）

将提取的6类信息整合为一个完整的Markdown文档，包含：
- 报告标题：`# 招标文件解析报告`
- 项目基本信息（项目名称、编号、解析日期、招标人、集采机构）
- 6个章节，每章为一个表格
- **⚠️ 必须添加PDF原始页码标注**（如：`P5`、`P9-10`）
- 总结和建议（可选）

保存为Markdown文件：
- 文件名：`招标文件解析报告_[项目名称]_[YYYYMMDD].md`
- 保存路径：`[workspace]/`（工作空间根目录）
- 如无法获取项目名称，使用 `招标文件解析报告_未知项目_[YYYYMMDD].md`

---

### 步骤4：生成DOCX报告（⚠️ 必须执行）

**执行方式**：使用Python脚本 `scripts/md_to_docx.py` 将Markdown报告转换为DOCX格式。

**⚠️ 重要**：此步骤为必须执行步骤，DOCX格式为默认输出格式。

**执行命令**：
```bash
cd "[workspace]"
py scripts/md_to_docx.py "招标文件解析报告_XXX_YYYYMMDD.md" "招标文件解析报告_XXX_YYYYMMDD.docx"
```

**输入输出**：
- 输入：`[workspace]/招标文件解析报告_[项目名称]_[YYYYMMDD].md`
- 输出：`[workspace]/招标文件解析报告_[项目名称]_[YYYYMMDD].docx`

**格式规范**：
- 详细格式规范参见 `references/report_format.md`
- 全文微软雅黑字体
- 表格：深蓝色表头（#2E5496）、黑色边框、无首行缩进
- 自动清理LaTeX公式
- 页码标注格式：`P4`、`P9-15`

**注意**：
- `[workspace]` 为当前会话的工作空间路径（如 `e:/000 Skills/招标文件解析`）
- 如Markdown报告中无页码标注，DOCX表格中"页码"列留空

---

## 工具和依赖

### PDF文件解析 ⚠️ 必须使用带页码的工具

| 工具 | 路径 | 说明 |
|------|------|------|
| ✅ **extract_pdf_with_pages.py** | `scripts/extract_pdf_with_pages.py` | 基于pdfplumber，保留页码，**优先使用** |
| ❌ `@pdf` skill | — | 禁止使用（无法保留页码） |

### DOCX报告生成

| 工具 | 路径 | 说明 |
|------|------|------|
| ✅ **md_to_docx.py** | `scripts/md_to_docx.py` | 核心转换脚本，已修复字体/表格问题 |
| ✅ **validate_and_fix_md.py** | `scripts/validate_and_fix_md.py` | MD格式检查与自动修复 |
| ✅ **auto_convert.py** | `scripts/auto_convert.py` | 一键格式检查+转换 |

### DOCX文件解析
- `@docx` skill 或 `Markdown Converter` skill

### Python依赖
```
pdfplumber   # PDF解析
python-docx  # DOCX生成
```

### 参考文档
- `references/extraction_prompt.md`：提取提示词模板
- `references/report_format.md`：报告格式规范

---

## 注意事项

1. **大文件处理**：如招标文件超过字数限制，可分段解析后整合
2. **表格合并**：如同一类信息分散在文件多个位置，应合并到同一表格
3. **歧义处理**：如条款理解有歧义，应在备注中说明
4. **更新记录**：如用户后续补充信息，可更新报告并注明更新日期

---

## 文件路径说明

- `[workspace]`：当前会话工作空间根目录
  - 当前项目：`e:/000 Skills/招标文件解析`
- `scripts/`：可执行脚本目录（位于 `.workbuddy/skills/bidding-document-parser/scripts/`）
- `references/`：模板和格式规范文档
- 所有输出文件默认保存到 `[workspace]/` 目录
