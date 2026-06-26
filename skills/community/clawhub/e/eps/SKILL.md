---
name: eps
description: Inspect EPS/PS/EPSF metadata and convert to PNG/JPG/SVG/PDF via API / 解析 EPS 元数据并通过 API 转换为 PNG/JPG/SVG/PDF
user-invocable: true
---

# EPS Tool

Inspect EPS / PS / EPSF file metadata and convert to PNG/JPG/SVG/PDF via API.
通过 API 解析 EPS / PS / EPSF 文件元数据，并转换为 PNG/JPG/SVG/PDF。

Server: https://eps.futrixdev.com

## API Reference

### Convert EPS to PNG/JPG/SVG/PDF / 格式转换

```bash
curl -X POST https://eps.futrixdev.com/api/convert \
  -F "file=@<file.eps>" \
  -F "format=png" \
  -F "dpi=300" \
  -o output.png
```

- `file` (required): EPS/PS/EPSF file (max 20MB) / 要转换的文件（最大 20MB）
- `format` (optional): png (default), jpg, svg, pdf / 输出格式
- `dpi` (optional): 36–1200, default 300 (for png/jpg) / 分辨率
- Response: converted file binary / 返回转换后的文件

### Inspect EPS metadata / 查看元数据

```bash
curl -X POST https://eps.futrixdev.com/api/info \
  -F "file=@<file.eps>"
```

- `file` (required): EPS/PS/EPSF file (max 20MB) / 要解析的文件（最大 20MB）
- Response: JSON with title, creator, BoundingBox, dimensions (pt/mm), PS version, fonts
- 返回 JSON，包含标题、创建者、BoundingBox、尺寸、PS 版本、字体等

### Health check / 健康检查

```bash
curl https://eps.futrixdev.com/api/health
```

## Web Viewer / 在线工具

https://eps.futrixdev.com — upload, preview, and export to PNG/JPG/SVG/PDF
打开网页工具上传文件，可预览并导出

## Examples

Convert EPS to PNG:
```bash
curl -X POST https://eps.futrixdev.com/api/convert -F "file=@logo.eps" -F "format=png" -o logo.png
```

Convert EPS to PDF:
```bash
curl -X POST https://eps.futrixdev.com/api/convert -F "file=@logo.eps" -F "format=pdf" -o logo.pdf
```

Get metadata:
```bash
curl -X POST https://eps.futrixdev.com/api/info -F "file=@logo.eps"
```

Example response:
```json
{
  "signature": "%!PS-Adobe-3.0 EPSF-3.0",
  "psVersion": "3.0",
  "epsfVersion": "EPSF-3.0",
  "title": "Logo Design",
  "creator": "Adobe Illustrator",
  "boundingBox": { "llx": 0, "lly": 0, "urx": 400, "ury": 300 },
  "widthPt": 400, "heightPt": 300,
  "widthMm": 141.12, "heightMm": 105.84
}
```

## Usage Guidelines / 使用建议

- Use `/api/convert` for format conversion (PNG/JPG/SVG/PDF) / 使用 API 进行格式转换
- Use `/api/info` to inspect file metadata / 使用 `/api/info` 查看文件元数据
- Supported input: `.eps`, `.ps`, `.epsf` files / 支持的输入格式
