# 支持的格式详细说明

MarkItDown 支持广泛的文件格式，按依赖组分类。

## 核心格式（无需额外依赖）

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| 纯文本 | .txt | 基础文本文件 |
| CSV | .csv | 逗号分隔值 |
| JSON | .json | JavaScript 对象表示 |
| XML | .xml | 可扩展标记语言 |
| ZIP | .zip | 压缩包（遍历内容） |
| HTML | .html, .htm | 网页文档 |

## 文档格式（需 [docx] 依赖）

| 格式 | 扩展名 | 库依赖 | 特性 |
|------|--------|--------|------|
| Word | .docx | python-docx | 保留格式、列表、表格 |
| PowerPoint | .pptx | python-pptx | 幻灯片、备注、形状 |
| Excel | .xlsx | openpyxl | 工作表、单元格、公式 |

## PDF 格式（需 [pdf] 依赖）

| 特性 | 说明 |
|------|------|
| 文本提取 | 直接提取 PDF 文本层内容 |
| 表格识别 | 智能识别和转换表格结构 |
| 图片 OCR | 对扫描版 PDF 进行光学字符识别 |
| 超链接 | 保留文档内和外部链接 |
| 页眉页脚 | 提取页眉页脚内容 |

**注意**: OCR 功能需要系统安装 Tesseract 引擎。详细配置参考 [PDF_CONFIG.md](PDF_CONFIG.md)。

## 图片格式（需 [image] 依赖）

| 格式 | 扩展名 | 功能 |
|------|--------|------|
| 图片 | .png, .jpg, .jpeg, .gif, .bmp, .tiff | EXIF 元数据 + OCR 文字提取 |

支持从图片中提取嵌入的文字和元数据（拍摄时间、设备信息、GPS 坐标等）。

## 音频格式（需 [audio] 依赖）

| 格式 | 扩展名 | 功能 |
|------|--------|------|
| 音频 | .mp3, .wav, .m4a, .flac, .ogg | EXIF 元数据 + 语音转录 |

支持提取音频元数据并生成文字转录稿（需要 OpenAI Whisper 或类似引擎）。

## 电子书（需额外依赖）

| 格式 | 扩展名 | 依赖 |
|------|--------|------|
| EPUB | .epub | epub 库 |

提取书籍正文、章节标题、元数据。

## 在线资源

| 资源 | 支持 | 依赖 |
|------|------|------|
| YouTube 视频 | URL 如 `https://youtu.be/xxx` | yt-dlp + ffmpeg |

下载视频并提取字幕/音频转录。

## 格式检测机制

MarkItDown 自动根据文件扩展名和内容检测格式，无需手动指定。对于无扩展名或可疑文件，可使用 `FileConverter` 的 `convert()` 方法，库会自动尝试合适的转换器。

### 转换优先级

1. 根据扩展名匹配内置转换器
2. 若无匹配，尝试 `magic` 库检测文件类型
3. 若仍无法确定，尝试所有可用转换器直至成功
4. 全部失败则抛出 `UnsupportedFormatError`

## 自定义转换器

可通过实现 `DocumentConverter` 接口添加新格式支持：

```python
from markitdown import DocumentConverter

class MyCustomConverter(DocumentConverter):
    @property
    def supported_extensions(self) -> List[str]:
        return ['.myformat']

    def convert(self, file_stream, **kwargs):
        # 实现转换逻辑
        pass
```

参考 [API_REFERENCE.md](API_REFERENCE.md) 了解完整接口。