---
version: "1.0.1"
name: dandan-file-organizer
description: 智能文件/桌面整理技能。当用户说"整理桌面"、"文件整理"、"整理文件夹"、"清理桌面"时触发。提供零删除、零篡改的安全文件归类，支持智能扫描、关键词匹配、按类型自动分类、多平台支持（macOS/Linux/Windows）。
metadata: {"openclaw": {"emoji": "📁"}}
---


# File Organizer 📁

智能文件归类整理，跨平台支持。

## 触发条件

- 用户说"整理桌面"、"文件整理"、"整理文件夹"、"清理桌面"
- 用户说"桌面太乱了"、"文件太多了"
- 用户要求按类型分类文件

## 文件分类规则

### 按扩展名分类

| 分类 | 扩展名 |
|------|--------|
| 图片 | png, jpg, jpeg, gif, bmp, tiff, webp, svg, ico, heic |
| 文档 | docx, pdf, txt, doc, ppt, pptx, odt, rtf, pages |
| 表格 | xlsx, csv, xls, numbers, ods, tsv |
| 视频 | mp4, avi, mov, mkv, flv, wmv, webm, m4v |
| 音频 | mp3, wav, flac, m4a, ogg, aac, wma, aiff |
| 代码 | py, js, tsx, java, c, cpp, h, go, rb, php, swift, kt, rs, sh, html, css, json, yaml |
| 压缩包 | zip, rar, 7z, tar, gz, bz2, xz |
| 电子书 | epub, mobi, azw3, djvu |
| 安装包 | exe, dmg, pkg, msi, apk, deb, rpm, appimage |
| 设计文件 | psd, ai, sketch, fig, xd, indd |
| 字体 | ttf, otf, woff, woff2 |
| 日志 | log |

## 整理策略

### 策略1：已有文件夹匹配
```
扫描目标目录 → 匹配文件名到已有文件夹 → 移动文件
关键词匹配：文件名包含文件夹名 → 移入
命名规律匹配：共享3字符以上前缀 → 移入
```

### 策略2：按类型分类（无匹配时）
```
不常用文件（60天未访问）→ 不常用文件/
其余按扩展名分类 → 图片/ | 文档/ | 表格/ | ...
```

### 策略3：按项目分类（phase2 AI 语义分析）
```
深度扫描未分类文件 → 提取关键词 → 生成项目文件夹 → 归类
```

## 跨平台命令

### macOS
```bash
# 列出桌面文件
ls -la ~/Desktop/

# 移动文件到分类文件夹
mv ~/Desktop/report.pdf ~/Documents/报告/

# 创建分类文件夹
mkdir -p ~/Desktop/{图片,文档,表格,代码,压缩包}

# 查看文件大小
du -sh ~/Desktop/*
```

### Linux
```bash
# 列出桌面文件
ls -la ~/桌面/   # 或 ~/Desktop/

# 移动文件
mv ~/桌面/report.pdf ~/文档/报告/

# 查看文件大小
du -sh ~/桌面/*

# 查找大文件
find ~/桌面 -type f -size +100M
```

### Windows (PowerShell)
```powershell
# 列出桌面文件
Get-ChildItem "$env:USERPROFILE\Desktop"

# 移动文件
Move-Item "$env:USERPROFILE\Desktop\report.pdf" "$env:USERPROFILE\Documents\报告\"

# 创建分类文件夹
New-Item -ItemType Directory -Path "$env:USERPROFILE\Desktop\图片"
New-Item -ItemType Directory -Path "$env:USERPROFILE\Desktop\文档"
New-Item -ItemType Directory -Path "$env:USERPROFILE\Desktop\表格"
```

## 零删除原则

- ❌ 不删除任何文件，只移动
- ❌ 不覆盖文件，自动重命名（filename_1.pdf）
- ❌ 不处理系统文件（.DS_Store、Thumbs.db 等）
- ⚠️ 快捷方式/别名不移动
- ⚠️ 被占用文件（lsof 检测）跳过
- ✅ 所有操作记录日志，可一键回撤

## 操作日志格式

```tsv
原路径    目标路径    分类    方法    状态
/home/user/Desktop/report.pdf    /home/user/Desktop/文档/report.pdf    文档    按类型分类    done
```

## 使用流程

```
1. 用户说"整理桌面"
   → 询问目标目录（默认 ~/Desktop）

2. 执行扫描（phase1）
   → 输出：文件列表、已有文件夹、建议分类方案

3. 用户确认
   → 执行整理（phase2）
   → 生成日志

4. 输出结果
   → 整理了多少文件
   → 创建了哪些文件夹
   → 日志文件位置（可回撤）
```

## 输出格式

```markdown
## 📁 文件整理结果

**目录**: ~/Desktop
**扫描时间**: 2026-03-19 19:54

### 📊 统计
- 扫描文件：42 个
- 整理完成：38 个
- 跳过：4 个（系统文件/被占用/白名单）
- 创建文件夹：7 个

### 📂 已创建文件夹
- 图片/（12个文件）
- 文档/（8个文件）
- 表格/（3个文件）
- ...

### 🔄 操作日志
[保存到 .file_organizer_logs/ organize_20260319_1954.log]

### ↩️ 回撤指令
如需回撤，执行：
[根据日志生成回撤命令]
```

## 注意事项

- 桌面文件通常较小，大文件建议移至对应分类文件夹
- 60天不常用规则可根据需要调整
- macOS 的 `.DS_Store`、Windows 的 `Thumbs.db` 自动跳过
- 整理前建议先做 phase1 扫描，用户确认后再执行
