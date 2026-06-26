---
name: 图片智能去重专业版
name-en: Image Deduplicator Pro
description: 递归扫描全目录图片，自定义相似度，安全软删除至回收站，保留高清原图
description-en: Recursively scan all images, custom similarity, safely move duplicates to trash, keep high-quality originals
version: 2.0.0
author: User
homepage: https://clawhub.ai/
user-invocable: true
disable-model-invocation: false
license: Commercial
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["python3"],
        "pips": ["pillow>=10.0.0"]
      },
      "os": ["darwin", "linux", "win32"],
      "emoji": "🖼️",
      "tags": ["image","deduplicate","photo","cleaner","recursive","tool","file management"]
    }
  }
---

# 🖼️ 图片智能去重专业版 | Image Deduplicator Pro

## 核心功能 | Core Features
✅ 递归深度扫描：根目录+所有子文件夹全量图片检索
✅ 自定义相似度：支持 0~100% 任意阈值设置
✅ 安全软删除：仅移动文件，不删除任何源文件
✅ 智能择优保留：优先留存高分辨率、大体积优质图片
✅ 全格式兼容：支持 JPG/PNG/WebP/BMP/TIFF
✅ 跨平台运行：macOS / Windows / Linux 全系统适配

✅ Recursive Deep Scan: Scan all images in root and subfolders
✅ Custom Similarity: 0~100% adjustable threshold
✅ Safe Soft-Delete: Only move files, never delete originals
✅ Smart Selection: Keep high-resolution & large-size images
✅ Full Format Support: JPG/PNG/WebP/BMP/TIFF
✅ Cross-Platform: Compatible with macOS/Windows/Linux

## 使用方法 | Usage
### AI 智能调用 | AI Agent
中文：帮我扫描 [文件夹路径] 下所有图片，使用 [相似度] 进行去重
English: Scan all images in [folder path] with [similarity] deduplication

### 命令行调用 | CLI
```bash
# 中文示例
python3 {baseDir}/main.py --path "你的图片目录" --similarity 99.5
# English Example
python3 {baseDir}/main.py --path "Your Image Folder" --similarity 99.5