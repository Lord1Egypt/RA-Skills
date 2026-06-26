# 文档整理技能参考资料

> 完整的 API、格式说明、配置指南和最佳实践

---

## 📚 目录

1. [API 参考](./API_REFERENCE.md)
2. [格式支持详细说明](./FORMATS.md)
3. [配置指南](./CONFIGURATION.md)
4. [故障排除](./TROUBLESHOOTING.md)
5. [性能优化](./PERFORMANCE.md)
6. [示例脚本](./EXAMPLES.md)

---

## 快速索引

### 核心 API

| 函数 | 用途 | 返回 |
|------|------|------|
| `scan_files(source_dir, file_types)` | 扫描并分类文件 | `by_dir: Dict[str, List[Path]]` |
| `convert_docs(...)` | Word 批量转换 | `(success, failed)` |
| `convert_excels(...)` | Excel 批量转换 | `(success, failed)` |
| `convert_presentations(...)` | PowerPoint 批量转换 | `(success, failed)` |
| `convert_pdfs(...)` | PDF 批量转换 | `(success, failed)` |
| `convert_modern(...)` | 现代格式转换 | `success` |

### 支持的格式

| 分类 | 格式 | 处理方式 | 质量 |
|------|------|---------|------|
| 旧版 Word | `.doc` | LibreOffice 直接 | ✅ 完美 |
| 新版 Word | `.docx` | MarkItDown | ✅ 完美 |
| 旧版 Excel | `.xls` | LibreOffice → .xlsx | ✅ 完美 |
| 新版 Excel | `.xlsx` | MarkItDown | ✅ 完美 |
| 旧版 PPT | `.ppt` | LibreOffice → .pptx | ✅ 良好 |
| 新版 PPT | `.pptx` | MarkItDown | ✅ 良好 |
| PDF | `.pdf` | MarkItDown | ✅ 优秀 |

---

## 依赖版本要求

| 工具/库 | 版本 | 必需性 |
|---------|------|--------|
| Python | >= 3.10 | 必需 |
| LibreOffice | 7.0+ | 仅旧版格式需要 |
| markitdown | >= 0.1.5 | 必需 |
| pywin32 | >= 311 | Windows 可选 |

---

## 典型使用场景

### 1. 历史文档数字化
- 来源：旧版 `.doc`/`.xls` 文件
- 目标：可搜索的 Markdown 知识库
- 推荐：`document-organizer` + 知识库索引

### 2. 项目归档
- 来源：混合格式项目文档
- 目标：统一 Markdown 格式
- 推荐：保持目录结构，使用 `--recursive`

### 3. PDF 提取
- 来源：扫描版/文字版 PDF
- 目标：结构化文本
- 推荐：纯 MarkItDown，OCR 可选

---

**最后更新**: 2026-03-11  
**对应版本**: document-organizer v1.0.0
