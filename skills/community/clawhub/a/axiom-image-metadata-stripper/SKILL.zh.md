---
name: axiom-image-metadata-stripper
description: 图像元数据去除器 — 从 JPEG/PNG/GIF 图像中删除 EXIF、GPS、相机信息和其他元数据。在发布照片并希望删除 PII 时使用。纯标准库 (不需要 Pillow),无需 LLM。
version: 0.1.2
license: Apache-2.0
---

# axiom-image-metadata-stripper

**Version:** 0.1.2
**Axioma Tools**

去除图像元数据,同时保留实际图像数据。

## What this skill does

- JPEG:去除 EXIF、ICC profile、XMP、IPTC
- PNG:去除 tEXt、zTXt、iTXt、eXIf 数据块
- GIF:去除注释扩展
- 保留图像像素 (不重新编码)
- 字节入,字节出

## When to use this skill

- ✅ 分享照片前去除 GPS 坐标
- ✅ 删除相机序列号
- ✅ 发布到网络前清理
- ❌ 重新编码/调整大小 (使用 Pillow)
- ❌ 查看 EXIF (使用 exiftool)

## Usage

```bash
python3 axiom_image_metadata_stripper.py photo.jpg -o photo-clean.jpg
python3 axiom_image_metadata_stripper.py ./photos/ --output-dir ./clean/
```

```python
from axiom_image_metadata_stripper import strip_metadata
clean_bytes = strip_metadata(open('photo.jpg', 'rb').read())
```

## Validation

| Check | Status |
|-------|--------|
| Unit tests | 20+ cases |
| Performance | <100ms |
| Security | Pure stdlib, no injection |
| Determinism | Byte-to-byte stable |
| License | Apache-2.0 |

_Last updated: 2026-06-14_
