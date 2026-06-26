---
slug: cn-batch-image-editor
name: 批量图片编辑器
version: "1.0.0"
author: 千策
---

# 批量图片处理工具

## 功能
- 批量压缩：减小图片体积，支持质量调节
- 批量调尺寸：固定宽高、比例缩放、智能裁剪
- 批量水印：文字水印、图片Logo水印
- 格式转换：PNG/JPG/WEBP/GIF互转
- 重命名：序号、日期、自定义前缀

## 使用方法

### 批量压缩
```bash
python scripts/batch_image.py compress /path/to/images --quality 85
```

### 批量调尺寸
```bash
# 固定宽度，高度等比缩放
python scripts/batch_image.py resize /path/to/images --width 800

# 固定高度
python scripts/batch_image.py resize /path/to/images --height 600

# 固定宽高（裁剪或填充）
python scripts/batch_image.py resize /path/to/images --width 800 --height 600 --mode crop
```

### 批量加水印
```bash
# 文字水印
python scripts/batch_image.py watermark /path/to/images --text "©养虾记" --position bottom-right --opacity 0.5

# 图片水印（Logo）
python scripts/batch_image.py watermark /path/to/images --logo /path/to/logo.png --position center --opacity 0.3
```

### 格式转换
```bash
# PNG转JPG
python scripts/batch_image.py convert /path/to/images --format jpg --quality 90

# 转WEBP（更小体积）
python scripts/batch_image.py convert /path/to/images --format webp
```

### 批量重命名
```bash
# 序号重命名
python scripts/batch_image.py rename /path/to/images --prefix "photo_" --start 1

# 日期重命名
python scripts/batch_image.py rename /path/to/images --date-format "%Y%m%d_%H%M%S"
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --quality | 压缩质量(1-100) | 85 |
| --width | 目标宽度 | - |
| --height | 目标高度 | - |
| --mode | 调整模式(scale/crop/fill) | scale |
| --text | 水印文字 | - |
| --logo | 水印图片路径 | - |
| --position | 水印位置 | bottom-right |
| --opacity | 水印透明度(0-1) | 0.5 |
| --format | 目标格式(png/jpg/webp/gif) | jpg |
| --output | 输出目录 | ./output |
| --prefix | 重命名前缀 | "" |
| --start | 重命名起始序号 | 1 |

## 水印位置选项
- `top-left`：左上角
- `top-right`：右上角
- `bottom-left`：左下角
- `bottom-right`：右下角
- `center`：居中
- `tile`：平铺

## 输出示例
```
处理完成！
输入目录：/Users/xxx/images
输出目录：/Users/xxx/images/output
处理图片：25张
总耗时：3.2秒
原始大小：125.6 MB → 处理后：32.4 MB（压缩74%）
```

## 典型场景
1. **电商图片**：批量调整为800x800，压缩到200KB以内
2. **社媒素材**：批量加水印，防止盗图
3. **证件照**：批量调尺寸（295x413），统一格式
4. **博客图片**：转WebP格式，减小体积

---

**出品：** AISoBrand｜爱索品牌 — AI搜索优化工具  
**官网：** https://aisobrand.com  
**免费检测你的品牌在AI搜索中有没有存在感 →** [30秒出结果](https://aisobrand.com/free-diagnosis.html)
