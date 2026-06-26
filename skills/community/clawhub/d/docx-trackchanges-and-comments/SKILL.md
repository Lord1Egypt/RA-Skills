---
name: docx-trackchanges-and-comments
description: Word文档 (.docx) 处理，支持修订模式(Track Changes)和批注操作。使用场景：(1) 修订模式 - 添加插入/删除修订、红字标注；(2) 批注操作 - 添加、删除、查看批注；(3) 文档内容修改。当用户要求"修订"、"track changes"、"批注"、"红字修订"、"添加评论"、"添加注释"时触发此技能。
---

# Word 文档处理 (修订模式 + 批注)

## 概述

Word 文档基于 OOXML 标准，内部结构为 ZIP 包，主要 XML 文件：
- `word/document.xml` - 文档正文内容
- `word/comments.xml` - 批注内容存储
- `word/settings.xml` - 文档设置（包含修订模式开关）

## 快速开始

### 使用脚本添加修订/批注

```bash python3 scripts/track_changes.py <input.docx> <output.docx> --add "原文本" "新文本" --author "修改人"
```

### 手动操作流程

1. 解压文档：`unzip -o document.docx -d docx_temp`
2. 编辑 XML 文件
3. 重新打包：`cd docx_temp && zip -r ../output.docx . && cd .. && rm -rf docx_temp`

---

## 功能一：修订模式 (Track Changes)

### 启用修订模式

在 `word/settings.xml` 中添加：
```xml
<w:trackChanges>true</w:trackChanges>
```

### 添加插入修订

```python
from scripts.track_changes import add_insertion
add_insertion(doc, "要插入的新内容", author="何大拿")
```

XML 原理：使用 `<w:ins>` 标签包裹插入内容（绿色下划线）

### 添加删除修订

```python
from scripts.track_changes import add_deletion
add_deletion(doc, "要删除的原文", author="何大拿")
```

XML 原理：使用 `<w:del>` 标签包裹删除内容（红色删除线）

---

## 功能二：批注操作

### 批注结构

批注涉及两个文件：
1. `word/comments.xml` - 存储批注内容
2. `word/document.xml` - 存储批注引用位置

### 快速查看批注

```bash
cd /path/to/inbound
unzip -o document.docx -d docx_temp
cat docx_temp/word/comments.xml
```

### 添加批注（XML 级别）

#### Step 1: 解压文档

```bash
cd /Users/hansel/.openclaw/media/inbound
unzip -o document.docx -d docx_temp
```

#### Step 2: 编辑 XML

需要修改两个文件：

**2.1 修改 comments.xml**

找到下一个可用的 comment ID：
```bash
grep -o 'w:id="[0-9]*"' docx_temp/word/comments.xml | sed 's/w:id="//;s/"//' | sort -n | tail -1
```

假设下一个 ID 是 `1`，添加新批注：
```xml
<w:comment w:id="1" w:author="你的名字" w:date="2026-03-17T14:00:00Z" w:initials="XX">
  <w:p w:rsidRDefault="00C227CD">
    <w:r><w:t>批注内容</w:t></w:r>
  </w:p>
</w:comment>
```

XML 实体转义：`&` → `&amp;`，`<` → `&lt;`，`>` → `&gt;`

**2.2 修改 document.xml**

在需要添加批注的文本位置添加标记：
```xml
<!-- 批注开始标记 -->
<w:commentRangeStart w:id="1"/>

<!-- 被批注的文本 -->
<w:r><w:t>这里是正文内容</w:t></w:r>

<!-- 批注结束标记 -->
<w:commentRangeEnd w:id="1"/>

<!-- 批注引用标记（显示为上标数字） -->
<w:r>
  <w:rPr>
    <w:rStyle w:val="CommentReference"/>
  </w:rPr>
  <w:commentReference w:id="1"/>
</w:r>
```

⚠️ **重要**：
- `<w:commentRangeStart>` 和 `<w:commentRangeEnd>` 是 `<w:p>` 的**同级兄弟元素**
- `<w:commentReference>` 需要包裹在 `<w:r>` 中

#### Step 3: 重新打包

```bash
cd docx_temp && zip -r ../output.docx . && cd ..
rm -rf docx_temp
```

### 删除批注

1. 从 `comments.xml` 中删除对应的 `<w:comment>` 元素
2. 从 `document.xml` 中删除三处标记：
   - `<w:commentRangeStart w:id="X"/>`
   - `<w:commentRangeEnd w:id="X"/>`
   - 包含 `<w:commentReference w:id="X"/>` 的整个 `<w:r>` 元素
3. 重新打包

### 接受批注（将批注内容合并到正文）

1. 从 `document.xml` 中删除三处批注标记
2. 保留 `comments.xml` 中的批注内容（可选）
3. 重新打包

---

## 批注 XML 详解

### comments.xml 结构

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:comments xmlns:w="...">
  <w:comment w:id="0" w:author="作者名" w:date="2026-01-01T12:00:00Z" w:initials="XX">
    <w:p w:rsidRDefault="00C227CD">
      <w:r><w:rPr><w:rStyle w:val="ae"/></w:rPr><w:annotationRef/></w:r>
      <w:r><w:t>批注内容</w:t></w:r>
    </w:p>
  </w:comment>
</w:comments>
```

### document.xml 中的批注引用

```xml
<w:p>
  <w:commentRangeStart w:id="0"/>
  <w:r><w:t>被批注的文本</w:t></w:r>
  <w:commentRangeEnd w:id="0"/>
  <w:r>
    <w:rPr>
      <w:rStyle w:val="CommentReference"/>
    </w:rPr>
    <w:commentReference w:id="0"/>
  </w:r>
</w:p>
```

---

## 注意事项

- **作者名称**：建议使用英文或拼音
- **日期格式**：ISO 8601 格式，如 `2026-03-17T14:00:00Z`
- **ID 唯一性**：每个批注的 ID 必须唯一，且在两个 XML 文件中保持一致
- **initials**：作者名缩写，2个字符为宜
