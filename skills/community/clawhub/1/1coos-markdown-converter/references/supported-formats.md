# 支持格式详细说明

## markitdown[all] 支持的文件格式

### 文档类

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| PDF | .pdf | 文本提取，支持 Azure Document Intelligence 增强 |
| Word | .docx | 保留标题、列表、表格、链接结构 |
| PowerPoint | .pptx | 提取幻灯片文本、备注、表格 |
| Excel | .xlsx, .xls | 转换为 Markdown 表格 |
| EPub | .epub | 电子书文本提取 |

### Web 和数据格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| HTML | .html, .htm | 转换 HTML 标签为 Markdown 语法 |
| CSV | .csv | 转换为 Markdown 表格 |
| JSON | .json | 格式化输出为代码块 |
| XML | .xml | 结构化文本提取 |

### 媒体文件

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| 图片 | .jpg, .png, .gif, .bmp, .tiff | EXIF 信息提取 + OCR 文字识别 |
| 音频 | .mp3, .wav, .m4a | EXIF 信息 + 语音转文字 |

### 其他

| 格式 | 说明 |
|------|------|
| ZIP 归档 | 遍历归档内容，逐个转换 |
| YouTube URL | 提取视频标题、描述、字幕 |

## 依赖说明

使用 `markitdown[all]` 安装完整依赖包，包括：

- **PDF 处理**: pdfminer 等 PDF 解析库
- **OCR 支持**: 图片文字识别相关依赖
- **音频转录**: 语音转文字相关依赖
- **Office 文档**: python-docx, python-pptx, openpyxl 等

## markitdown CLI 选项

```
-o OUTPUT       指定输出文件路径
-x EXTENSION    文件扩展名提示（用于 stdin 输入）
-m MIME_TYPE    MIME 类型提示
-c CHARSET      字符集提示（如 UTF-8）
-d              使用 Azure Document Intelligence（需配置端点）
-e ENDPOINT     Azure Document Intelligence 端点 URL
--use-plugins   启用第三方插件
--list-plugins  显示已安装的插件
```

## 注意事项

- 首次运行 `uvx markitdown[all]` 会下载并缓存依赖，后续运行速度更快
- 复杂 PDF（扫描件等）建议使用 `-d` 参数配合 Azure Document Intelligence
- 图片 OCR 和音频转录需要 `markitdown[all]` 的完整依赖
- 大文件转换可能耗时较长，默认超时 60 秒，可通过 config.json 调整
