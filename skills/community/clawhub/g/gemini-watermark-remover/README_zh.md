# Gemini 去水印工具

[English](./README.md) | 中文

---

使用反向 Alpha 混合算法去除 Gemini AI 生成图片的水印。

## ⚠️ 免责声明

**本工具仅限个人学习研究使用，不得用于商业用途。**

根据您所在的司法管辖区及图像的实际用途，移除水印的行为可能具有潜在的法律影响。用户需自行确保其使用行为符合适用法律、相关服务条款以及知识产权规定，并对此承担全部责任。

**本软件按"原样"提供，不提供任何形式（明示或暗示）的保证。**

## 功能

- ✅ 纯本地处理（图片不上传）
- ✅ 反向 Alpha 混合算法，无损去水印
- ✅ 自动检测水印尺寸（48×48 或 96×96）
- ✅ 独立脚本，无外部依赖

## 安装

```bash
# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 命令行

```bash
# 基本用法
python3 scripts/remove_watermark.py 图片.jpg

# 指定输出
python3 scripts/remove_watermark.py 图片.jpg -o 去水印.jpg
```

### Python API

```python
from scripts.remove_watermark import remove_watermark

# 去水印
remove_watermark('输入.jpg', '输出.jpg')
```

## 算法原理

### 水印原理

Gemini 使用 Alpha 混合将水印叠加到原图：

```
带水印 = α × Logo + (1-α) × 原图
```

### 去除原理

反向求解：

```
原图 = (带水印 - α × 255) / (1-α)
```

### 关键点

- 使用嵌入代码的水印模板（Base64 编码，无外部依赖）
- Alpha map = RGB 通道最大值
- 包含噪声过滤（ALPHA_NOISE_FLOOR）
- 图片 ≤ 1024×1024 用 48×48 模板，反之用 96×96

## 检测规则

| 图片尺寸 | 水印尺寸 | 右边距 | 下边距 |
|---------|---------|--------|--------|
| 宽 > 1024 且 高 > 1024 | 96×96 | 64px | 64px |
| 其他情况 | 48×48 | 32px | 32px |

## 局限性

- ❌ 仅去除 Gemini 可见水印（右下角半透明 Logo）
- ❌ 无法去除隐形水印（如 SynthID）
- ❌ 针对当前 Gemini 水印模式设计

## 许可证

[MIT License](./LICENSE)
