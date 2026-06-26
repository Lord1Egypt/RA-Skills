---
name: extract-pic-text
description: 从图片文件名中提取指定位置的文本内容。支持自定义分隔符和提取位置，可批量处理目录中的图片文件。适用于需要从规范化命名的图片中提取ID、编号、日期等信息的场景。Use when: (1) 需要从图片文件名中提取特定位置的文本, (2) 批量处理命名规范的图片文件, (3) 提取文件名中的ID、编号、日期等信息。
metadata:
  openclaw:
    emoji: 🖼️
    requires:
      bins: [python3]
---

# extract-pic-text

从图片文件名中提取指定位置的文本内容。支持自定义分隔符、提取位置，可批量处理目录中的图片文件。

## 功能特点

- 支持自定义分隔符（默认为 `_`）
- 支持指定提取位置（默认为第2部分，即第一个和第二个分隔符之间的内容）
- 支持多种图片格式（jpg, jpeg, png, gif, bmp, webp, tiff, tif）
- 可自定义图片扩展名列表
- 支持结果排序和去重
- 可输出到文件或 stdout

## 用法

### 基本用法

```bash
# 提取默认位置（第一个和第二个下划线之间的文本）
python3 scripts/extract_pic_text.py /path/to/images

# 示例：BIN245_515194318_0128N.jpg -> 515194318
```

### 高级选项

```bash
# 使用不同的分隔符和位置
python3 scripts/extract_pic_text.py /path/to/images -d '-' -p 0
# 示例：img-12345-test.jpg -> img (位置0)

# 指定图片扩展名
python3 scripts/extract_pic_text.py /path/to/images -e .jpg .png

# 结果排序并去重
python3 scripts/extract_pic_text.py /path/to/images --sort --unique

# 保存到文件
python3 scripts/extract_pic_text.py /path/to/images -o result.txt
```

### 完整参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `directory` | - | 图片所在目录路径（必填） | - |
| `--delimiter` | `-d` | 文件名分隔符 | `_` |
| `--position` | `-p` | 提取位置（0开始） | `1` |
| `--extensions` | `-e` | 图片扩展名列表 | `.jpg .jpeg .png .gif .bmp .webp .tiff .tif` |
| `--output` | `-o` | 输出文件路径 | stdout |
| `--sort` | - | 对结果排序 | False |
| `--unique` | - | 去重 | False |

## 提取规则示例

假设分隔符为 `_`，位置为 `1`：

| 文件名 | 提取结果 |
|--------|----------|
| `BIN245_515194318_0128N.jpg` | `515194318` |
| `abc_def_ghi.png` | `def` |
| `2024_0307_event.jpg` | `0307` |
| `product_SKU123_detail.jpg` | `SKU123` |

## 输出格式

```
515194318,515196709,515270355

注意：2个文件格式不符：invalid_file.jpg, no_underscore.png
```

## 使用场景

1. **图片处理**：从 `SKU_12345_variant.jpg` 中提取 SKU 编号
2. **照片管理**：从 `2024_0307_event.jpg` 中提取日期
3. **批量重命名辅助**：提取现有文件名中的关键信息
4. **数据整理**：从规范化命名的图片中提取ID进行数据库比对

## 脚本路径

```
scripts/extract_pic_text.py
```

在 skill 目录下可直接执行：
```bash
python3 ~/.openclaw/workspace/skills/extract-pic-text/scripts/extract_pic_text.py /path/to/images
```
