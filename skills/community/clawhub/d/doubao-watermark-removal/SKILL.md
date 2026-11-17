---
name: doubao-watermark-removal
description: Batch remove Doubao (豆包 AI) watermarks from images using OpenCV inpainting. Use when the user asks to remove watermarks, batch remove watermarks, 去水印, 批量去水印, or 去豆包水印. Also use for general batch watermark removal when the user provides a directory of images and knows the watermark area.
---

# 去豆包水印

批量去除豆包 AI 生成图片右下角水印，基于 OpenCV 图像修复（inpainting）。同样适用于其他固定位置水印的批量去除。

## 前置条件

首次使用需安装依赖：

```bash
python3 -m pip install -r <skill-dir>/requirements.txt
```

如果系统默认 Python 太旧（pip 版本 <9.0.3），使用项目 Python：

```bash
"/Users/liuyue/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3" -m pip install -r <skill-dir>/requirements.txt
```

## 水印位置参考

豆包生成的角色资源图通常有两种尺寸，水印均位于右下角。已验证的水印区域：

| 图片尺寸 | 用途 | 参数 | 说明 |
|----------|------|------|------|
| 1254×1254 | 精确去除 | `1015,1170,220,70` | 标准水印区域 |
| 1254×1254 | 去残留 | `1000,1160,240,85` | 放大区域，覆盖更多边缘 |
| 2048×2048 | 精确去除 | `1650,1890,398,158` | 右下角水印较大、更靠边 |

2048×2048 图片四角通常还有小标记，需同时清理：

```text
--rect 1650,1890,398,158 --rect 0,0,24,24 --rect 2024,0,24,24 --rect 0,2024,24,24 --rect 2024,2024,24,24
```

**如果图片尺寸不同**，先取一张图用 `python3 -c "import cv2; img=cv2.imread('<path>'); print(img.shape)"` 查看尺寸，再按比例估算水印位置，或让用户截图标注。

## 批量去水印

```bash
python3 <skill-dir>/scripts/batch_remove_watermark.py <input_dir> <output_dir> --rect 1015,1170,220,70 --clear-alpha
```

- `<input_dir>` — 含源图的目录
- `<output_dir>` — 输出目录，自动创建
- `--rect X,Y,W,H` — 水印矩形区域（左上角坐标 + 宽高），可重复使用
- `--clear-alpha` — 对透明 PNG，将水印区域设为完全透明（否则 inpainting 会在透明通道留下痕迹）
- `--recursive` — 递归处理子文件夹
- `--force` — 覆盖已有输出
- `--radius N` — inpainting 半径，默认 3，大块水印可调至 5-7
- `--only FILENAME` — 只处理匹配的文件名，可重复使用（如 `--only 女孩_走路.png --only 女孩_正面.png`）

### 1254×1254 图片

```bash
python3 <skill-dir>/scripts/batch_remove_watermark.py \
  "/Users/liuyue/Desktop/some-folder" \
  "/Users/liuyue/Desktop/some-folder-clean" \
  --rect 1015,1170,220,70 \
  --clear-alpha \
  --force
```

### 2048×2048 图片

```bash
python3 <skill-dir>/scripts/batch_remove_watermark.py \
  <input_dir> <output_dir> \
  --rect 1650,1890,398,158 \
  --rect 0,0,24,24 \
  --rect 2024,0,24,24 \
  --rect 0,2024,24,24 \
  --rect 2024,2024,24,24 \
  --clear-alpha --force
```

### 只处理指定文件

```bash
python3 <skill-dir>/scripts/batch_remove_watermark.py \
  <input_dir> <output_dir> \
  --rect 1650,1890,398,158 \
  --rect 0,0,24,24 --rect 2024,0,24,24 --rect 0,2024,24,24 --rect 2024,2024,24,24 \
  --clear-alpha --force \
  --only 女孩_走路.png --only 女孩_正面.png
```

### 边缘残留处理

如果处理后有残留水印边缘，放大区域重新处理：

```bash
python3 <skill-dir>/scripts/batch_remove_watermark.py \
  <input_dir> <output_dir> \
  --rect 1000,1160,240,85 \
  --clear-alpha --force
```

## 自定义水印位置

如果水印不在右下角或图片尺寸不同：

1. 让用户截一张图，标注水印位置
2. 用图像工具获取水印的像素坐标 `(X, Y, W, H)`
3. 代入 `--rect X,Y,W,H` 运行

### 多个水印区域

```bash
python3 <skill-dir>/scripts/batch_remove_watermark.py \
  <input_dir> <output_dir> \
  --rect 1015,1170,220,70 \
  --rect 20,30,180,48 \
  --clear-alpha
```

## 工作流程

1. 确认用户要处理的图片目录
2. 抽一张图查看尺寸，确认水印位置
3. 如果尺寸与预设（1254×1254 / 2048×2048）匹配，直接用预设参数
4. 如果尺寸不同，按比例调整或请用户提供水印区域
5. 运行批量去水印命令
6. 核对输出结果（`Processed: N, skipped: 0, failed: 0`）

## 常见问题

- **`Missing dependency: cv2`** — 重新执行前置条件中的 pip install
- **`Input folder does not exist`** — 检查输入路径，注意空格和中文
- **pip 版本过旧** — 使用 Codex 自带 Python
- **处理后有残留** — 放大 `--rect` 区域或增大 `--radius`
