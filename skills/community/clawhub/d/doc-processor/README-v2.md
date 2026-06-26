# doc-processor v2.0 新功能

> **⚠️ v2.7.11 重要变更**: AI 功能已移除，由 OpenClaw 主程序统一处理。
> 本文档中的 AI 相关功能（AI 摘要、AI 匹配）在 v2.7.11+ 中已不再包含。

## 🎉 重大升级

v2.0 从"文档填充工具"升级为"智能文档生成引擎"

---

## ✨ 新增功能

### 1. 样式感知

**自动识别模板样式，填充后保持格式美观**

```python
from doc_processor import DocumentProcessor

processor = DocumentProcessor()

# 提取模板样式
style_def = processor.style_extractor.extract("template.docx")
print(f"章节数：{len(style_def.sections)}")
print(f"样式：{style_def.styles}")
```

### 2. 内容适配

**根据样式要求自动适配内容**

```python
# 摘要自动总结（过长时）
adapter = ContentAdapter()
summary = adapter._adapt_summary(长文本)

# 列表格式统一
tasks = adapter._adapt_list("任务 1\n任务 2\n任务 3")
# 输出：['• 任务 1', '• 任务 2', '• 任务 3']
```

### 3. 三层模板策略

**智能选择最佳模板**

- **Level 1**: 用户提供模板 → 保存 + 学习
- **Level 2**: 历史模板匹配 → AI 多维度匹配
- **Level 3**: Style Guide 引导 → 通用规范生成

```python
# 智能文档生成
result = processor.generate(
    user_request="生成周报",
    content={"week": 12, "author": "张三"}
)
print(f"输出：{result.output_path}")
print(f"使用模板：{result.template_used}")
```

### 4. 模板填充

**支持 {{placeholder}} 语法**

```python
# 模板内容：第{{week}}周工作报告
# 数据：{"week": 12}
# 结果：第 12 周工作报告

processor.fill_template(
    template_path="template.docx",
    data={"week": 12, "author": "张三"},
    output_path="report.docx"
)
```

### 5. 用户模板管理

**自动保存和匹配历史模板**

```
~/.openclaw/workspace/user-templates/
├── registry.json          # 注册表
├── templates/             # 模板文件
│   ├── tpl_20260325_001.docx
│   └── ...
└── categories/            # 分类索引
```

---

## 📊 Style Guide

v2.0 提供通用文档样式规范：

- `style-guide.md` - 总纲
- `word-style-guide.md` - Word 规范
- `excel-style-guide.md` - Excel 规范
- `elements/` - 文档元素样式

---

## 🚀 快速开始

### 安装 v2.0

```bash
clawhub install doc-processor --version 2.0.0
```

### 使用模板填充

```python
from doc_processor import DocumentProcessor

processor = DocumentProcessor()

# 填充模板
result = processor.fill_template(
    template_path="weekly-report.docx",
    data={
        "week": 12,
        "author": "张三",
        "main_work": "完成 v2.0 开发"
    },
    output_path="week12-report.docx"
)
```

### 智能文档生成

```python
# 自动匹配历史模板或使用 Style Guide
result = processor.generate(
    user_request="生成一份周报",
    content="这周完成了 v2.0 开发，修复了 3 个 bug"
)
```

---

## 📋 兼容性

### 保留的 v1.x 功能

- ✅ `read()` - 读取文档
- ✅ `write()` - 写入文档
- ✅ `convert()` - 格式转换
- ✅ `merge()` - 文档合并
- ✅ `extract()` - 数据提取

### 新增的 v2.0 功能

- ➕ `fill_template()` - 模板填充
- ➕ `generate()` - 智能生成
- ➕ `StyleExtractor` - 样式提取器
- ➕ `ContentAdapter` - 内容适配器

---

## 🎯 使用场景

### 场景 1: 周报生成

```python
# 第一次：上传模板
processor._save_user_template("my-weekly.docx", "生成周报")

# 后续：自动生成
result = processor.generate("生成周报", {"week": 12})
```

### 场景 2: 批量合同

```python
# 使用模板批量生成
for client in clients:
    processor.fill_template(
        "contract-template.docx",
        {"client": client, "amount": 10000}
    )
```

---

## 📚 文档

- [Style Guide](templates/style-guide.md)
- [Word 规范](templates/word-style-guide.md)
- [Excel 规范](templates/excel-style-guide.md)

---

*版本：v2.0.0 | 发布日期：2026-03-25*
