# PDF 处理配置指南

MarkItDown 的 PDF 转换功能依赖多个组件，本指南说明如何正确配置。

## 安装依赖

### 基础安装（推荐）

```bash
pip install 'markitdown[all]'
```

这会安装所有 PDF 处理所需的依赖：
- `pdfminer.six` - 文本提取
- `pymupdf` (fitz) - 高级 PDF 处理
- `ocrmypdf` - OCR 功能（扫描 PDF）

### 按需安装

仅文本 PDF（无需 OCR）：
```bash
pip install 'markitdown[pdf]'
```

包含 OCR 的完整安装：
```bash
pip install 'markitdown[pdf] ocrmypdf[tesseract]'
```

## OCR 引擎配置

### Tesseract 安装

OCR 功能需要系统级 Tesseract 引擎。

#### Windows
1. 从 [GitHub UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki) 下载安装包
2. 安装时选择语言包（建议中文简体、英文）
3. 将 Tesseract 添加到 PATH 或设置环境变量 `TESSDATA_PREFIX`

验证安装：
```bash
tesseract --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-chi-sim  # 简体中文
```

#### macOS
```bash
brew install tesseract
brew install tesseract-lang  # 语言包
```

### 语言数据

确保所需语言的 `.traineddata` 文件存在，默认位置：
- Windows: `C:\Program Files\Tesseract-OCR\tessdata`
- Linux: `/usr/share/tesseract-ocr/4.00/tessdata/`
- macOS: `/usr/local/share/tessdata/`

下载额外语言包：
```bash
# 从官方仓库复制到 tessdata 目录
curl -O https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata
```

## 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `TESSDATA_PREFIX` | Tesseract 数据目录 | `C:\Tesseract\tessdata` |
| `OMP_THREAD_LIMIT` | 限制 OCR 线程数（避免内存问题） | `4` |
| `MARKITDOWN_OCR_ENGINE` | 指定 OCR 引擎（默认 ocrmypdf） | `ocrmypdf` |

## 测试配置

```python
from markitdown import MarkItDown
md = MarkItDown()

# 测试普通 PDF
result1 = md.convert("test_normal.pdf")
print(f"文本长度: {len(result1.text_content)}")

# 测试扫描 PDF（需要 OCR）
result2 = md.convert("test_scanned.pdf")
print(f"文本长度: {len(result2.text_content)}")
```

## 常见问题

### Q: OCR 很慢怎么办？
A: PDF 扫描页面越多越慢。可考虑：
- 仅对需要 OCR 的页面使用 `--force-ocr`
- 调整 `OMP_THREAD_LIMIT` 限制并发
- 使用 GPU 加速版 Tesseract

### Q: "Tesseract not found" 错误
A: 确保 Tesseract 在 PATH 中，或设置 `TESSDATA_PREFIX` 环境变量。

### Q: 中文识别效果差
A: 确保安装了 `chi_sim.traineddata`（简体）或 `chi_tra.traineddata`（繁体）。

### Q: 转换失败： "No text extractable"
A: 可能是完全扫描的图像 PDF，尝试：
```bash
# 强制 OCR
ocrmypdf --force-ocr input.pdf output.pdf
# 然后用 markitdown 处理 output.pdf
```

## 性能对比

| 文件类型 | 文本 PDF | 扫描 PDF（OCR） |
|---------|----------|----------------|
| 典型速度 | 秒级 | 分钟级（每页 ~10-30s） |
| 内存需求 | 低 | 中到高 |
| 依赖要求 | pdfminer.six | ocrmypdf + Tesseract |

---
参考: [ocrmypdf 文档](https://ocrmypdf.readthedocs.io/)