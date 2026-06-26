---
name: file-sorter
description: 通用文件智能分类工具，支持多种分类规则：类型、大小、日期、关键词等。适用于需要批量整理文件的场景，如下载文件夹整理、照片归档、文档分类等。
---

# File Sorter - 文件智能分类工具

## 功能特性
- ✅ 多种分类规则：文件类型、文件大小、文件日期、关键词
- ✅ 灵活操作：移动、复制、创建符号链接
- ✅ 预览功能：先预览效果，确认后再执行
- ✅ 撤销操作：支持撤销最近一次整理
- ✅ 自定义规则：支持自定义分类规则和文件夹结构
- ✅ 规则预设：保存和加载分类规则预设

## 快速开始

### 1. 按文件类型分类
```bash
file-sorter organize ~/Downloads --by-type --output ~/Sorted
```

### 2. 按文件大小分类
```bash
file-sorter organize ~/Downloads --by-size --output ~/Sorted
```

### 3. 按文件日期分类（修改日期）
```bash
file-sorter organize ~/Downloads --by-date modified --output ~/Sorted
```

### 4. 预览模式（不实际执行）
```bash
file-sorter organize ~/Downloads --by-type --preview
```

### 5. 撤销操作
```bash
file-sorter undo ~/Sorted
```

## 详细使用说明

### 分类规则说明

#### 按文件类型分类
- **默认类别**：
  - documents：文档类（.pdf, .doc, .docx, .txt, .xls, .xlsx, .ppt, .pptx）
  - images：图片类（.jpg, .jpeg, .png, .gif, .webp, .heic）
  - videos：视频类（.mp4, .avi, .mov, .mkv）
  - audio：音频类（.mp3, .wav, .flac, .aac）
  - installers：安装包类（.exe, .msi, .dmg, .pkg, .deb, .rpm）
  - archives：压缩包类（.zip, .rar, .7z, .tar, .gz）
  - code：代码类（.py, .js, .html, .css, .java, .cpp）
- **自定义类别**：使用 --categories 参数或配置文件

#### 按文件大小分类
- **默认规则**：
  - small：小于 1MB
  - medium：1MB - 100MB
  - large：大于 100MB
- **自定义规则**：使用 --size-rules 参数或配置文件

#### 按文件日期分类
- **选项**：
  - created：按创建日期
  - modified：按修改日期
  - accessed：按访问日期
- **文件夹结构**：按年/月/日组织（如 2026/03/07）

### 操作类型
- **move**：移动文件（默认）
- **copy**：复制文件
- **link**：创建符号链接

### 配置文件
可以在项目根目录创建 `.file-sorter.json` 配置默认选项：
```json
{
  "output_dir": "~/Sorted",
  "action": "move",
  "categories": {
    "documents": [".pdf", ".doc"],
    "images": [".jpg", ".png"]
  },
  "size_rules": {
    "small": [0, 1048576],
    "medium": [1048576, 104857600],
    "large": [104857600, null]
  },
  "backup_original": true
}
```

## 安全措施
1. **预览模式**：默认先显示预览，需要确认后才执行
2. **自动备份**：执行整理前自动保存操作日志
3. **撤销功能**：随时可以撤销最近一次操作
4. **dry-run 选项**：使用 --preview 查看效果

## 示例场景

### 场景 1：整理下载文件夹
```bash
# 按类型整理下载文件
file-sorter organize ~/Downloads --by-type --output ~/Downloads/Organized
```

### 场景 2：整理照片
```bash
# 按拍摄日期整理照片
file-sorter organize ~/Photos --by-date created --output ~/Photos/ByDate
```

### 场景 3：按大小分类大文件
```bash
# 找出所有大于 100MB 的文件
file-sorter organize ~/Videos --by-size --output ~/Videos/BySize
```

## 故障排除
- **撤销失败**：确保在同一目录下执行，且备份文件未被删除
- **规则冲突**：多个规则匹配时，按规则优先级处理（类型 > 大小 > 日期）
- **权限问题**：确保有文件读写权限

## 更新日志
### v1.0.0 (2026-03-07)
- 初始正式版本发布
- 支持按类型、大小、日期分类
- 支持预览和撤销功能
