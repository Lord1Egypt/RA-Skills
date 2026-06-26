# Download Organizer - 下载文件自动分类工具

一个简单但强大的下载文件自动分类工具，帮助你快速整理混乱的下载文件夹！

## 功能特性
- ✅ 自动识别文件类型（文档、图片、视频、音频、安装包、压缩包、代码等）
- ✅ 按文件类型自动分类到不同文件夹
- ✅ 支持自定义分类规则（计划中）
- ✅ 预览模式（先看效果再执行）
- ✅ 撤销操作（安全可靠）

## 安装

### 方法一：通过 clawhub 安装
```bash
clawhub install download-organizer
```

### 方法二：作为 Python 脚本运行
```bash
# 克隆或下载项目
git clone <repo-url>
cd download-organizer
```

## 快速开始

### 1. 整理下载文件夹
```bash
python3 download_organizer.py organize ~/Downloads --output ~/Downloads/Organized
```

这会自动创建以下文件夹结构，并把文件复制进去：
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
├── code/
│   └── script.py
└── others/
    └── other.file
```

### 2. 预览模式（不实际执行，先看效果）
```bash
python3 download_organizer.py organize ~/Downloads --preview
```

这会显示整理方案，但不会实际移动文件。确认没问题后再去掉 --preview 参数执行。

### 3. 撤销操作
如果你整理错了，可以随时撤销：
```bash
python3 download_organizer.py undo ~/Downloads/Organized
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
| code | .py, .js, .html, .css, .java, .cpp, .c, .h, .go, .rs |
| others | 其他未分类的文件 |

### 配置文件（计划中）
未来版本将支持配置文件 `~/.download-organizer.json`：
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
python3 download_organizer.py organize ~/Downloads
```

### 场景 2：先预览，再执行
```bash
# 第一步：预览
python3 download_organizer.py organize ~/Downloads --preview

# 第二步：确认没问题后执行
python3 download_organizer.py organize ~/Downloads --output ~/Downloads/Organized
```

## 安全性
- 工具默认使用复制而非移动，原文件不会被删除
- 执行前会自动保存备份
- 支持一键撤销操作
- 建议先用 --preview 预览效果

## 故障排除

### 问题：权限不足
**解决方法**：确保你有文件的读写权限

### 问题：撤销失败
**原因**：备份文件可能被删除或修改
**解决方法**：确保在同一目录下执行，且备份文件未被删除

## 开发计划
- [ ] 自定义分类规则
- [ ] 配置文件支持
- [ ] 更智能的文件识别（内容识别）
- [ ] GUI 界面（可选）
- [ ] 自动监控下载文件夹，新文件自动整理

## 贡献
欢迎提交 Issue 和 Pull Request！

## 许可证
MIT License

---

**Download Organizer** - 让下载文件夹整理变得简单！📥
