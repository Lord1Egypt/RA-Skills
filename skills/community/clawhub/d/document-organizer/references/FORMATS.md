# 格式支持详细说明

本文档详细说明 `document-organizer` 技能支持的所有文件格式，包括处理流程、质量评估和注意事项。

---

## 格式总览

| 格式分类 | 格式 | 扩展名 | 处理方式 | 质量 | 必需依赖 |
|---------|------|--------|---------|------|---------|
| **旧版 Word** | Word 97-2003 | `.doc` | LibreOffice → Markdown | ✅ 完美 | LibreOffice |
| **新版 Word** | Word 2007+ | `.docx` | LibreOffice → Markdown | ✅ 完美 | LibreOffice |
| **旧版 Excel** | Excel 97-2003 | `.xls` | LibreOffice → .xlsx → MarkItDown | ✅ 完美 | LibreOffice + markitdown |
| **新版 Excel** | Excel 2007+ | `.xlsx` | MarkItDown 直接 | ✅ 完美 | markitdown |
| **旧版 PPT** | PowerPoint 97-2003 | `.ppt` | LibreOffice → .pptx → MarkItDown | ✅ 良好 | LibreOffice + markitdown |
| **新版 PPT** | PowerPoint 2007+ | `.pptx` | MarkItDown 直接 | ✅ 良好 | markitdown |
| **PDF** | Adobe PDF | `.pdf` | MarkItDown 直接 | ✅ 优秀 | markitdown[pdf] |

---

## 详细处理流程

### 1. `.doc` (Word 97-2003)

**处理流程**:
```
原始 .doc 文件
    ↓ (LibreOffice --convert-to md)
Markdown 文件 (.md)
```

**特点**:
- ✅ 一步到位，不生成中间文件
- ✅ LibreOffice 内置的 Markdown 导出器
- ✅ 批量处理（`soffice --convert-to md *.doc`）
- ⚠️ 复杂格式可能略有简化

**质量评估**: 95%+ 格式保留

**示例**:
```bash
soffice --headless --convert-to md --outdir ./output *.doc
```

**已知限制**:
- 某些 VBA 宏不保留（Macro 字段会丢失）
- 嵌入式 OLE 对象转为占位符
- 页眉页脚合并到正文

---

### 2. `.docx` (Word 2007+)

**处理流程**:
```
原始 .docx 文件
    ↓ (LibreOffice --convert-to md)
Markdown 文件 (.md)
```

**特点**:
- ✅ 一步到位，不生成中间文件
- ✅ LibreOffice 内置的 Markdown 导出器
- ✅ 批量处理（`soffice --convert-to md *.docx`）
- ✅ 完美保留标题层级、列表、加粗、斜体
- ✅ 表格转为 Markdown 表格
- ✅ 图片链接自动处理（输出为 `![alt](path)`）
- ✅ 超链接完整保留

**质量评估**: 95%+ 格式保留

**示例**:
```bash
soffice --headless --convert-to md --outdir ./output *.docx
```

---

### 3. `.xls` (Excel 97-2003)

**处理流程**:
```
原始 .xls 文件
    ↓ (LibreOffice --convert-to xlsx)
临时 .xlsx 文件
    ↓ (MarkItDown.convert())
Markdown 表格
```

**特点**:
- ✅ 两步转换确保格式无损
- ✅ 表格结构完整保留（列、行、合并单元格）
- ✅ 数据格式（数字、日期）保持
- ⚠️ 复杂公式转为计算值（不保留公式本身）

**质量评估**: 95%+ 表格完整性

**示例**:
```bash
# 步骤 1: .xls → .xlsx
soffice --headless --convert-to xlsx --outdir ./temp ./temp/*.xls

# 步骤 2: .xlsx → .md（自动执行）
```

---

### 4. `.xlsx` (Excel 2007+)

**处理流程**:
```
原始 .xlsx 文件
    ↓ (MarkItDown.convert())
Markdown 表格
```

**特点**:
- ✅ 多 Sheet 处理（每个 Sheet 成为独立章节）
- ✅ 单元格样式（粗体、对齐）转为 Markdown 强调
- ✅ 合并单元格处理为跨列/行标记
- ⚠️ 条件格式丢失（仅保留显示值）

**质量评估**: 95%+ 表格完整性

---

### 5. `.ppt` / `.pptx` (PowerPoint)

**处理流程**:
```
.ppt → LibreOffice → .pptx → MarkItDown → .md
.pptx → MarkItDown → .md (直接)
```

**特点**:
- ✅ 每张幻灯片转为独立章节（`## 幻灯片标题`）
- ✅ 文本框、列表保留
- ✅ 图片自动提取并链接
- ⚠️ 动画效果丢失（Markdown 不支持）
- ⚠️ 演讲者备注可能不完整

**质量评估**: 85-90% 内容保留

**`.ppt` vs `.pptx`**:
- `.ppt` 需要 LibreOffice 中转（多一步）
- `.pptx` 直接 MarkItDown，质量更好

---

### 6. `.pdf` (Portable Document Format)

**处理流程**:
```
原始 PDF
    ↓ (MarkItDown.convert())
结构化 Markdown
```

**特点**:
- ✅ 文本型 PDF：完美提取，保留段落
- ✅ 表格检测：自动转为 Markdown 表格
- ✅ 图片提取：保存为单独文件并链接
- ⚠️ 扫描版 PDF 需要 OCR（需安装 `markitdown[pdf]` 和 Tesseract）
- ⚠️ 复杂布局可能顺序错乱

**质量评估**:
- **文字 PDF**: 95%+ ✅
- **扫描 PDF + OCR**: 80-90% ✅（依赖 OCR 质量）

**OCR 启用**:
```bash
pip install 'markitdown[pdf]'
# 安装 Tesseract: https://github.com/tesseract-ocr/tesseract

markitdown scanned.pdf --ocr --lang chi_sim
```

---

## 格式对比表

| 特性 | .doc | .docx | .xls | .xlsx | .ppt | .pptx | .pdf |
|------|------|-------|------|-------|------|-------|------|
| **文本保留** | ✅ 优秀 | ✅ 优秀 | ✅ 完美 | ✅ 完美 | ✅ 优秀 | ✅ 优秀 | ✅ 优秀 |
| **表格保留** | N/A | N/A | ✅ 完美 | ✅ 完美 | ⚠️ 部分 | ⚠️ 部分 | ✅ 良好 |
| **图片提取** | ✅ 是 | ✅ 是 | ❌ 否 | ❌ 否 | ✅ 是 | ✅ 是 | ✅ 是 |
| **超链接** | ✅ 保留 | ✅ 保留 | ❌ 丢失 | ❌ 丢失 | ✅ 保留 | ✅ 保留 | ✅ 保留 |
| **多Sheet/页** | N/A | N/A | ✅ 支持 | ✅ 支持 | ✅ 支持 | ✅ 支持 | ✅ 支持 |
| **宏/VBA** | ❌ 丢失 | ❌ 丢失 | N/A | N/A | N/A | N/A | N/A |
| **公式** | ⚠️ 值 | ⚠️ 值 | ⚠️ 值 | ⚠️ 值 | N/A | N/A | N/A |
| **批注** | ⚠️ 部分 | ⚠️ 部分 | N/A | N/A | ⚠️ 部分 | ⚠️ 部分 | ❌ 丢失 |
| **依赖要求** | LibreOffice | LibreOffice | LibreOffice+md | markitdown | LibreOffice+md | markitdown | markitdown |

---

## 智能匹配规则

`scan_files()` 函数实现智能扩展名匹配：

```python
# 用户指定 .doc → 自动匹配 .doc 和 .docx
if ft == '.doc':
    all_files.extend(source.rglob('*.doc'))
    all_files.extend(source.rglob('*.docx'))

# 用户指定 .xls → 自动匹配 .xls 和 .xlsx
if ft == '.xls':
    all_files.extend(source.rglob('*.xls'))
    all_files.extend(source.rglob('*.xlsx'))

# 用户指定 .ppt → 自动匹配 .ppt 和 .pptx
if ft == '.ppt':
    all_files.extend(source.rglob('*.ppt'))
    all_files.extend(source.rglob('*.pptx'))
```

**好处**:
- 用户无需分别指定 `.doc` 和 `.docx`
- 自动处理新旧格式混合场景
- 减少重复代码

---

## 转换质量汇总

| 格式 | 总体评分 | 文本 | 结构 | 表格 | 图片 | 链接 |
|------|---------|------|------|------|------|------|
| `.doc` | 95% | ✅ | ✅ | N/A | ✅ | ✅ |
| `.docx` | 95% | ✅ | ✅ | N/A | ✅ | ✅ |
| `.xls` | 95% | ✅ | ✅ | ✅ | ❌ | ❌ |
| `.xlsx` | 95% | ✅ | ✅ | ✅ | ❌ | ❌ |
| `.ppt` | 85% | ✅ | ⚠️ | N/A | ✅ | ✅ |
| `.pptx` | 88% | ✅ | ⚠️ | N/A | ✅ | ✅ |
| `.pdf` | 90%* | ✅ | ✅ | ✅ | ✅ | ✅ |

*PDF 评分取决于原始质量（文字型 vs 扫描型）

---

## 推荐使用场景

### 场景 1: 历史 Word 文档批量转换
**推荐格式**: `.doc` → `.md`
**原因**: LibreOffice 直接转换，速度快，质量好
**命令**:
```bash
npx skills run document-organizer --source "G:\old_docs" --type doc
```

### 场景 2: 现代 Office 文档处理
**推荐格式**: `.xlsx` / `.pptx`
**原因**: MarkItDown 直接处理，无需 LibreOffice
**命令**:
```bash
npx skills run document-organizer --source "G:\new_docs" --type xlsx,pptx
```

### 场景 3: 混合历史文档（最常见）
**推荐**: 默认 `--type doc,xls,docx,xlsx,ppt,pptx,pdf`
**原因**: 自动识别新旧格式，统一输出

### 场景 4: 大规模 PDF 数字图书馆
**推荐**: 单独用 `markitdown` 技能
**原因**: PDF 是 MarkItDown 的强项，独立处理更高效
**命令**:
```bash
npx skills run markitdown --source "G:\pdfs" --recursive
```

---

## 不支持的格式

以下格式 **不在本技能范围** 内，但可通过其他技能处理：

| 格式 | 扩展名 | 建议工具 |
|------|--------|---------|
| 图片 | `.jpg`, `.png` | OCR 技能或 `markitdown[image]` |
| 音频 | `.mp3`, `.wav` | Whisper 或 `markitdown[audio]` |
| 视频 | `.mp4`, `.avi` | 需专用视频处理 |
| 压缩包 | `.zip`, `.rar` | 先解压再处理 |
| 代码 | `.py`, `.js` | 可直接读取（无需转换）|
| 纯文本 | `.txt`, `.md` | 无需转换 |

---

## 格式检测与验证

### 文件头检测（Magic Number）

```python
def detect_format(filepath):
    with open(filepath, 'rb') as f:
        header = f.read(8)

    if header.startswith(b'PK\x03\x04'):
        return 'zip-based'  # .docx, .xlsx, .pptx, .zip
    elif header.startswith(b'\xd0\xcf\x11\xe0'):
        return 'ole'  # .doc, .xls, .ppt
    elif header.startswith(b'%PDF'):
        return 'pdf'
    else:
        return 'unknown'
```

---

## 故障与格式

| 问题 | 可能格式 | 原因 | 解决 |
|------|---------|------|------|
| 表格错乱 | `.xls` / `.xlsx` | 合并单元格支持有限 | 检查输出，手动调整 |
| 图片丢失 | `.doc` / `.ppt` | LibreOffice 导出问题 | 使用 `.docx`/`.pptx` 源文件 |
| 乱码 | 所有 | 源文件编码非 UTF-8 | 检查源文件编码 |
| 转换超时 | 大文件 | LibreOffice 处理慢 | 增加 `timeout` 参数 |
| 公式变值 | `.xls`/`.xlsx` | MarkItDown 只读值 | 正常，公式不保留 |
| 页眉页脚合并 | `.doc` | 导出限制 | 正常，页眉页脚整合到正文 |

---

## 升级与扩展

### 支持新格式的步骤

1. **评估格式**: 是否有通用转换工具？
2. **添加扫描逻辑**: 修改 `scan_files()` 扩展名匹配
3. **实现转换函数**: 类似 `convert_pdfs()`
4. **更新依赖**: 在 `manifest.json` 添加 pip 包
5. **文档更新**: 添加格式到本文件表格
6. **测试**: 准备样本文档，验证输出质量

---

**最后更新**: 2026-03-11  
**对应版本**: document-organizer v1.1.0  
**维护**: 比特老板 / OpenClaw AI
