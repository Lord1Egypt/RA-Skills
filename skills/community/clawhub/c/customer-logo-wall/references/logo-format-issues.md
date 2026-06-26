# Logo 格式常见问题与解决方案

## 问题背景

从搜索引擎（百度/Bing/Google）批量下载的 Logo 图片，扩展名虽然是 `.png`，但实际文件格式经常不一致。这会导致：

1. **Anthropic API 报错**：`Could not process image` (HTTP 400)
2. **PowerPoint 打开异常**：图片无法显示或格式错误
3. **python-pptx 嵌入失败**：某些格式不被支持

## 常见格式伪装

| 扩展名 | 实际格式 | 检测方法 | 频率 |
|--------|---------|---------|------|
| .png | JPEG | 文件头 `\xff\xd8` | 高（~40%） |
| .png | WEBP | 文件头 `RIFF....WEBP` | 中（~15%） |
| .png | SVG (XML) | 文件头 `<?xml` 或 `<svg` | 低（~5%） |
| .png | PNG（真正） | 文件头 `\x89PNG` | ~40% |

## 检测方法

```python
from PIL import Image

img = Image.open('logo.png')
print(img.format)  # 'JPEG', 'PNG', 'WEBP' 等

# 或检查文件头
with open('logo.png', 'rb') as f:
    header = f.read(4)
    if header == b'\x89PNG':
        print('真正的 PNG')
    elif header[:2] == b'\xff\xd8':
        print('实际是 JPEG')
```

## SVG 的特殊处理

SVG 是矢量格式，Pillow 无法直接打开。需要光栅化为 PNG：

| 工具 | 安装方式 | 质量 |
|------|---------|------|
| rsvg-convert | `brew install librsvg` | 最佳 |
| cairosvg | `pip install cairosvg` + 需系统 cairo 库 | 好 |
| qlmanage | macOS 自带 | 可用（偶尔渲染不完整） |

**qlmanage 注意事项**：
- SVG 中白色内容在白色背景上会"消失"（Scheer 案例）
- 某些复杂 SVG 会渲染为系统默认图标（Seidor 案例 → 地球图标）
- 建议转换后目视检查结果

## 解决方案

### 方案 1：使用 normalize_logos.py（推荐）

```bash
python3 scripts/normalize_logos.py --logos-dir ./logos --companies companies.json
```

自动检测并转换所有非 PNG 文件。

### 方案 2：build_ppt.py 内置修复

`build_ppt.py` 中的 `ensure_real_png()` 函数会在嵌入 PPT 前自动修复 JPEG/WEBP（但不处理 SVG）。

### 方案 3：手动批量转换

```python
from PIL import Image
import os

for f in os.listdir('./logos'):
    if not f.endswith('.png'):
        continue
    img = Image.open(f'./logos/{f}')
    if img.format != 'PNG':
        img.convert('RGBA').save(f'./logos/{f}', 'PNG')
```

## 实际案例（v1.2.0 修复记录）

咨询公司 Logo 项目中 30 个文件的实际格式分布：

- 真正 PNG：12 个（40%）
- JPEG 伪装 .png：12 个（40%）
- WEBP 伪装 .png：4 个（13%）
- SVG 伪装 .png：2 个（7%）

其中 4 个 Logo 内容也不正确（EY 截取不完整、BDO 空白、Seidor/Scheer SVG 渲染异常），需要重新下载。
