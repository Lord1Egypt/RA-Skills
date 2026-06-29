---
name: smart-file-organizer
version: 1.0.0
description: Smart file organizer: auto-classify files by type, date and naming patterns
---

# Smart File Organizer

一键整理混乱的文件夹。三种模式：按类型、按日期、按命名规则自动归类。

## 功能

- **按类型归类**：图片/文档/视频/音频/压缩包/代码 自动分入对应文件夹
- **按日期归类**：按年/年月/年月日创建子目录
- **按命名规律归类**：自定义匹配规则
- **预览模式**：`--dry-run` 先看再执行
- **一键撤销**：`--undo` 恢复到整理前

## 触发词

- 整理文件夹
- 文件归类
- 按类型整理文件
- organize files
- classify files

## 使用

```bash
# 按类型整理
python scripts/main.py --dir D:\Downloads

# 按月份整理照片
python scripts/main.py --dir D:\Photos --method date --date-mode month

# 按规则整理
python scripts/main.py --dir D:\Docs --method pattern --patterns "发票:Invoices,报表:Reports"

# 预览
python scripts/main.py --dir D:\Downloads --dry-run

# 撤销
python scripts/main.py --dir D:\Downloads --undo
```

## 依赖

Python >= 3.10，无第三方依赖。
