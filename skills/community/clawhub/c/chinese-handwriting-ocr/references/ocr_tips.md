# OCR 参数与技巧 (v2.0 双引擎版)

## 引擎选择策略

- **印刷体/扫描文档**: 用 Tesseract (`--engine tesseract`)，快且够用
- **手写体/签名/日期**: 用 RapidOCR (`--engine rapid`)，准确率 60-85%
- **混合内容**: 用 Dual 双引擎 (`--engine dual`)，Tesseract 识别印刷体 + RapidOCR 补充手写区

## DPI（分辨率）

- **Tesseract**: 300 DPI 足够中文印刷体，低于 200 需先提升
- **RapidOCR**: 400 DPI 对手写体更佳，可在 `--dpi 400` 指定

## RapidOCR 加速

- 首次使用会自动下载模型并缓存到 `~/.EasyOCR/model` 或 RapidOCR 内置缓存
- CPU 模式单页约 2-3s，GPU(CUDA) 模式可快 3-5x
- 如需 GPU 加速：`pip install onnxruntime-gpu`

## 语言模型

- **Tesseract**: `-l chi_sim` (简体) / `-l chi_tra` (繁体) / `-l chi_sim+eng` (中英混合)
- **RapidOCR**: 自动检测中英文，无需指定语言代码

## 日期提取

RapidOCR 在 `--date-mode` 下自动从手写区域解析日期（支持模糊匹配）：
- 完整日期: `2022年6月15日`
- 部分日期: `2022年6月` 或 `6月15日`
- 仅月份: `6月`

## 常见问题

### RapidOCR 报 "ModuleNotFoundError"
```bash
pip install rapidocr-onnxruntime
```

### 双引擎模式输出较大
双引擎模式会同时保存 Tesseract 文字层和 RapidOCR 注释，文件体积略有增加。

### 手写体仍不理想
- 提高 `--dpi` 到 500-600
- 裁剪更精确的区域（缩小 `--region` 范围）
- 图像预处理：先用 `--clean --deskew` 去噪纠偏

## 并行处理

批量处理大量文件时可使用 PowerShell 并行：
```powershell
Get-ChildItem *.pdf | ForEach-Object -Parallel {
    python scripts/ocr_batch.py $_ "$($_.BaseName)_rapid.pdf" --engine rapid
} -ThrottleLimit 4
```
