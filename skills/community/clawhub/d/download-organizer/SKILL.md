---
name: download-organizer
description: 下载文件自动分类工具，自动识别文件类型并按类别整理到不同文件夹。适用于整理下载文件夹，自动分类文档、图片、视频、音频、安装包、压缩包等文件！
---

# Download Organizer - 下载文件自动分类工具

## 功能特性
- ✅ 自动识别文件类型（文档、图片、视频、音频、安装包、压缩包、代码等）
- ✅ 按文件类型自动分类到不同文件夹
- ✅ 支持自定义分类规则
- ✅ 预览模式（先看效果再执行）
- ✅ 撤销操作（安全可靠）

## 安装
```bash
# 方法一：通过 clawhub 安装
clawhub install download-organizer

# 方法二：作为 Python 脚本运行
git clone <repo-url>
cd download-organizer
```

## 快速开始

### 1. 整理下载文件夹
```bash
download-organizer organize ~/Downloads --output ~/Downloads/Organized
```

这会自动创建以下文件夹结构，并把文件移动进去：
```
Organized/
├── documents/
│   ├── report.pdf
│   └── notes.docx
├── images/
│   ├── photo.jpg
│   └── screenshot.png
├── videos/
│   └── movie.mp4
├── audio/
│   └── song.mp3
├── installers/
│   └── app.exe
├── archives/
│   └── files.zip
└── code/
    └── script.py
```

### 2. 预览模式（不实际执行）
```bash
download-organizer organize ~/Downloads --preview
```

### 3. 撤销操作
```bash
download-organizer undo ~/Downloads/Organized
```

## 详细使用说明

### organize 命令参数
- `directory`：（必需）要整理的目录，通常是下载文件夹
- `--output`：输出目录，默认在输入目录下创建 `Organized` 文件夹
- `--preview`：预览模式，只显示方案不实际执行

### 默认文件分类
| 文件夹 | 文件类型 |
|-------|---------|
| documents | .pdf, .doc, .docx, .txt, .xls, .xlsx, .ppt, .pptx |
| images | .jpg, .jpeg, .png, .gif, .webp, .heic |
| videos | .mp4, .avi, .mov, .mkv |
| audio | .mp3, .wav, .flac, .aac |
| installers | .exe, .msi, .dmg, .pkg, .deb, .rpm |
| archives | .zip, .rar, .7z, .tar, .gz |
| code | .py, .js, .html, .css, .java, .cpp |

### 配置文件（计划中）
可以在项目根目录创建 `.download-organizer.json` 来自定义分类规则：
```json
{
  "output_dir": "~/Downloads/Organized",
  "categories": {
    "documents": [".pdf", ".doc"],
    "images": [".jpg", ".png"]
  },
  "backup_original": true
}
```

## 示例场景

### 场景 1：整理下载文件夹
```bash
# 整理你的下载文件夹
download-organizer organize ~/Downloads
```

### 场景 2：先预览，再执行
```bash
# 第一步：预览
download-organizer organize ~/Downloads --preview

# 第二步：确认没问题后执行
download-organizer organize ~/Downloads --output ~/Downloads/Organized
```

## 注意事项
- 确保有文件的读写权限
- 建议先用 --preview 预览效果
- 大量文件整理可能需要一些时间
- 整理前建议先备份原文件

## 更新日志
### v1.0.0 (2026-03-06)
- 初始版本发布
- 支持按文件类型自动分类
- 支持预览模式
- 支持撤销操作
