---
name: a4-to-a3-pdf
version: 1.0.0
description: 将文件夹中的图片按顺序两两合并为A3横向PDF（两张A4左右并排）。触发词：合并PDF、合成A3、两张A4合成一页、图片转PDF。
---

# A4 to A3 PDF Merger

将多张图片合并为 A3 横向 PDF，每页放置两张图片（左右并排）。

## Usage

### 方法1：使用脚本（推荐）

```bash
python scripts/merge_a4_to_a3.py <图片文件夹> <输出PDF路径> [dpi]
```

示例：
```bash
python scripts/merge_a4_to_a3.py "C:\Users\ZERO\Desktop\质保书" "C:\Users\ZERO\Desktop\输出.pdf"
```

### 方法2：手动生成

如需自定义（如添加白边、调整尺寸），参考脚本逻辑自行修改。

## Output Format

- 页面尺寸：A3 横向（420mm × 297mm）
- 每页：左右两张 A4 图片，无白边
- 分辨率：默认 300 DPI
- 图片按数字顺序排列（1.jpg, 2.jpg, ...）

## Dependencies

- Python 3.x
- Pillow: `python -c "from PIL import Image"` 或 `python -m pip install Pillow`
