# 文档处理技能 📄

专业的PDF和Word文档处理工具集，支持多种文档格式转换和编辑操作。

## 功能特性

### 📋 核心功能
- ✅ **PDF页面提取** - 提取指定页面生成新PDF
- ✅ **PDF转Word** - 保留格式转换
- ✅ **Word转PDF** - 高质量转换
- ✅ **PDF合并/拆分** - 合并多个PDF或拆分单个PDF
- ✅ **PDF去水印** - 移除水印内容
- ✅ **PDF压缩优化** - 减小文件大小
- ✅ **批量处理** - 处理多个文件

### 🛠 高级功能
- 🔄 格式转换 (PDF ↔ Word)
- 📑 页面管理 (提取、重排、删除)
- 🖼 图片提取 (从PDF中提取图片)
- 🔍 OCR文字识别 (扫描版PDF转文字)
- 💧 水印管理 (添加/移除水印)
- 📊 批量操作 (文件夹批量处理)

## 快速开始

### 1. 安装依赖
```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/document-processor

# 安装所有依赖
python3 install_dependencies.py

# 或只检查已安装的包
python3 install_dependencies.py --check
```

### 2. 基本使用示例

#### PDF页面提取
```bash
# 提取第14-29页
python3 pdf_extractor.py "input.pdf" "output.pdf" --start 14 --end 29

# 提取特定页面
python3 pdf_extractor.py "input.pdf" "output.pdf" --pages "1,3,5-7,10"

# 提取所有奇数页
python3 pdf_extractor.py "input.pdf" "output.pdf" --odd

# 按间隔提取（每3页提取1页）
python3 pdf_extractor.py "input.pdf" "output.pdf" --interval 3
```

#### PDF转Word
```bash
# 单个文件转换
python3 pdf_to_word.py "document.pdf" "document.docx"

# 批量转换
python3 pdf_to_word.py --batch ./pdfs ./docs

# 转换指定页面
python3 pdf_to_word.py "input.pdf" "output.docx" --pages "1,3,5-7"
```

#### Word转PDF
```bash
# 单个文件转换
python3 word_to_pdf.py "document.docx" "document.pdf"

# 批量转换
python3 word_to_pdf.py --batch ./docs ./pdfs
```

## 脚本说明

### 核心脚本
| 脚本文件 | 功能描述 | 使用示例 |
|---------|---------|---------|
| `pdf_extractor.py` | PDF页面提取 | `python3 pdf_extractor.py input.pdf output.pdf --start 1 --end 10` |
| `pdf_to_word.py` | PDF转Word | `python3 pdf_to_word.py input.pdf output.docx` |
| `word_to_pdf.py` | Word转PDF | `python3 word_to_pdf.py input.docx output.pdf` |
| `install_dependencies.py` | 安装依赖 | `python3 install_dependencies.py` |

### 即将推出的脚本
- `pdf_merger.py` - PDF合并工具
- `pdf_splitter.py` - PDF拆分工具  
- `remove_watermark.py` - PDF去水印工具
- `batch_processor.py` - 批量处理工具
- `pdf_compressor.py` - PDF压缩工具
- `image_extractor.py` - 图片提取工具
- `ocr_pdf.py` - OCR文字识别工具

## 在OpenClaw中使用

### 激活技能
当用户需要处理文档时，OpenClaw会自动检测并激活本技能。

### 使用流程
1. **识别需求**：确定用户需要什么功能
2. **检查依赖**：确保所需Python库已安装
3. **选择脚本**：根据需求选择合适的脚本
4. **执行操作**：运行相应的Python脚本
5. **验证结果**：检查输出文件是否满足要求

### 示例对话
```
用户：帮我把这个PDF的第5-10页提取出来
助手：好的，我将使用PDF页面提取功能。请稍等...
（运行：python3 pdf_extractor.py input.pdf output.pdf --start 5 --end 10）
已完成！提取的页面已保存为 output.pdf
```

## 系统要求

### 软件要求
- Python 3.7 或更高版本
- pip 包管理器

### Python依赖
- PyPDF2>=3.0.0
- python-docx>=0.8.11  
- pdf2docx>=0.5.6
- Pillow>=9.0.0
- pdfplumber>=0.8.0
- docx2pdf>=0.1.8

### Windows额外依赖
- comtypes>=1.1.14
- pywin32>=305

## 故障排除

### 常见问题

1. **导入错误**
   ```
   错误: No module named 'PyPDF2'
   ```
   **解决方案**: 运行 `python3 install_dependencies.py`

2. **文件格式不支持**
   ```
   错误: 文件格式不支持
   ```
   **解决方案**: 确保文件扩展名正确 (.pdf, .docx, .doc)

3. **权限错误**
   ```
   错误: Permission denied
   ```
   **解决方案**: 检查文件权限，或尝试以管理员身份运行

4. **内存不足**
   ```
   错误: MemoryError
   ```
   **解决方案**: 处理大文件时使用分批处理，或增加系统内存

### 获取帮助
- 查看脚本帮助: `python3 脚本名.py --help`
- 检查依赖: `python3 install_dependencies.py --check`
- 重新安装: `python3 install_dependencies.py`

## 更新日志

### v1.0.0 (2026-03-01)
- ✅ PDF页面提取工具
- ✅ PDF转Word工具  
- ✅ Word转PDF工具
- ✅ 依赖安装脚本
- ✅ 完整的技能文档

### 计划功能
- 🔄 PDF合并/拆分
- 💧 水印管理
- 📊 批量处理优化
- 🖼 图片提取
- 🔍 OCR文字识别

## 贡献指南

欢迎贡献代码或提出建议！

1. Fork 本仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 作者

文档处理技能开发团队

---

**技能状态**: ✅ 生产就绪  
**最后更新**: 2026-03-01  
**版本**: 1.0.0