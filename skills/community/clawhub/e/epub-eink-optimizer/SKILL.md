---
name: epub-eink-optimizer
description: >
  This skill should be used when the user wants to optimize an epub file for e-ink readers
  (墨水屏电子书). It handles image deduplication, removal of tiny decorative images, resizing
  oversized images, and JPEG recompression — all targeting reduced file size while preserving
  readability on e-ink devices. Trigger phrases include: epub优化、墨水屏、电子书瘦身、epub压缩、
  epub图片处理、epub减小体积、epub图片优化、epub图片去重、清理epub图片、缩小epub、
  optimize epub, epub for kindle/kobo/boox.
---

# epub 墨水屏优化技能

## 目标

将 epub 文件中的图片进行四步优化，大幅减小文件体积，同时保留在墨水屏设备上的可读性。

## 核心脚本

`scripts/optimize_epub.py` — 一键运行全部优化步骤，支持单独开关每个步骤。

```bash
# 全量优化（推荐默认用法）
python skills/epub-eink-optimizer/scripts/optimize_epub.py <epub路径>

# 先分析，不修改文件
python skills/epub-eink-optimizer/scripts/optimize_epub.py <epub路径> --dry-run

# 自定义参数示例
python skills/epub-eink-optimizer/scripts/optimize_epub.py <epub路径> \
    --max-width 600 \
    --quality 65 \
    --min-size 20480

# 只做某几步
python skills/epub-eink-optimizer/scripts/optimize_epub.py <epub路径> \
    --no-dedup --no-clean-small
```

**参数说明：**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--max-width` | 800 | 图片最大宽度（像素），超过则等比缩小 |
| `--quality` | 70 | JPEG 压缩质量（1-95），70 为画质与体积的平衡点 |
| `--min-size` | 10240 | 清除低于此字节数的图片（默认 10KB） |
| `--no-dedup` | — | 跳过重复图片合并 |
| `--no-resize` | — | 跳过宽度缩放 |
| `--no-recompress` | — | 跳过 JPEG 重压缩 |
| `--no-clean-small` | — | 跳过清小图 |
| `--dry-run` | — | 仅分析，不修改文件 |

## 四步优化流程

### 步骤 1：去重复图片

同一张图片以不同文件名出现在多篇文章中（常见于转载同款配图、作者反复使用的插图）。

- 用 MD5 哈希识别完全相同的图片
- 保留文件名排序靠前的一份，其余删除
- 自动更新所有 XHTML 中的引用和 OPF manifest

### 步骤 2：清除小图

微信公众号文章末尾通常插有固定的二维码、点赞、广告等装饰性小图（通常 < 5KB），对阅读毫无价值。

- 删除低于 `--min-size` 字节的图片文件
- 从 XHTML 中移除对应的 `<img>` 标签
- 清理残留的空 `<p>` / `<div>` 标签

### 步骤 3：缩放大图

墨水屏设备分辨率通常为 1024-1448px 宽，超出无意义。

- 将宽度超过 `--max-width` 的图片等比缩小
- JPEG 保存为 JPEG，PNG 保存为 PNG
- 中间使用 LANCZOS 高质量缩放算法

### 步骤 4：JPEG 重压缩

epub 中的 JPEG 原始质量往往是 85-95，对墨水屏来说过于精细。

- 以 `--quality`（默认 70）重新压缩所有 JPEG
- 使用 `optimize=True` 开启哈夫曼表优化
- 通常可节省 15-25%

## 典型效果参考

| 场景 | 优化前 | 优化后 | 压缩率 |
|------|--------|--------|--------|
| 微信公众号合集（100篇+） | 70MB | 13MB | ~82% |
| 图文并茂博客（50篇） | 30MB | 8MB | ~73% |
| 纯文字为主（少量配图） | 5MB | 3MB | ~40% |

## 手动处理补充指南

脚本覆盖大多数场景，以下情况需要手动干预（参考 `references/manual-fixes.md`）：

- 图片为 base64 内嵌（非独立文件）
- epub 内部目录结构非标准（如多层嵌套）
- 需要将彩色图片转为灰度以进一步减体积

## 依赖

```bash
pip install Pillow
```

Python 标准库：`zipfile`, `hashlib`, `re`, `io`, `os`
