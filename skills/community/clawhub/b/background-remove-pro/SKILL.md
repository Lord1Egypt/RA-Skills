# bg-remove

图片智能去背景工具，使用 RMBG-1.4 或 rembg 库实现高精度背景移除。

## 功能

- **智能去背景**: 使用 AI 模型自动识别并移除图片背景
- **支持多种格式**: PNG、JPG、WebP、BMP 等常见图片格式
- **批量处理**: 支持批量处理多张图片
- **透明背景**: 输出带透明通道的 PNG 图片
- **支持本地模型**: 可选择使用本地模型或默认模型

## 触发词

- 去背景、移除背景、图片去背景
- 抠图、去除图片背景、透明背景
- bg-remove、remove background

## 使用方法

### 基本用法

```bash
# 去除单张图片背景
/bg-remove --input photo.jpg

# 指定输出路径
/bg-remove --input photo.jpg --output result.png

# 批量处理整个文件夹
/bg-remove --input ./photos --output ./output

# 使用特定模型
/bg-remove --input photo.jpg --model RMBG-1.4
```

### 高级选项

```bash
# 调整处理阈值 (0-1)
/bg-remove --input photo.jpg --threshold 0.5

# 保持原始文件名
/bg-remove --input ./photos --output ./output --keep-name

# 覆盖已存在的文件
/bg-remove --input photo.jpg --force
```

## 命令参数

| 参数 | 简写 | 说明 | 默认值 |
|-----|------|------|-------|
| `--input` | `-i` | 输入图片或文件夹路径 | 必填 |
| `--output` | `-o` | 输出路径（文件或文件夹） | 同输入目录 |
| `--model` | `-m` | 使用的模型 (u2net/RMBG-1.4) | u2net |
| `--threshold` | `-t` | 分割阈值 (0-1) | 0.5 |
| `--keep-name` | `-k` | 保持原始文件名 | false |
| `--force` | `-f` | 覆盖已存在的文件 | false |
| `--alpha-matting` | - | 启用 Alpha Matting 增强边缘 | false |
| `--alpha-matting-foreground` | - | Alpha Matting 前景阈值 | 240 |
| `--alpha-matting-background` | - | Alpha Matting 背景阈值 | 10 |

## 输出说明

- 输出格式为 PNG，支持透明通道
- 文件名默认添加 `_nobg` 后缀
- 处理后的图片可直接用于设计、电商、产品展示等场景

## 示例

```bash
# 电商产品图去背景
/bg-remove --input ./product.jpg --output ./product_nobg.png

# 批量处理证件照背景
/bg-remove --input ./photos/ --output ./results/

# 人像照片去背景
/bg-remove --input portrait.jpg --model RMBG-1.4 --alpha-matting
```

## 依赖

- Python 3.8+
- rembg
- pillow
- onnxruntime

首次使用会自动下载模型文件。
