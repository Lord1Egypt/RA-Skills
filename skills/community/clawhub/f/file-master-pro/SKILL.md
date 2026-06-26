---
name: 文件管理大师
slug: file-master-pro
description: 强大的文件批量处理工具，支持重命名、整理、搜索、转换等操作，让文件管理变得简单高效。
version: 1.0.0
author: 阿策自动化工作室
tags: [file, management, automation, batch, rename, organize]
price: $9.99
category: productivity
os: [windows, macos, linux]
---

# 文件管理大师 📁✨

一键解决文件管理烦恼！支持批量重命名、智能整理、快速搜索、格式转换等强大功能。

## 核心功能

### 1. 批量重命名
```
# 智能重命名模式
file-master rename "D:\photos\" --pattern "vacation_{num:03d}.jpg"

# 正则表达式重命名  
file-master rename "D:\docs\" --regex "^(.*)_old\.txt$" --replace "$1_new.txt"

# 添加前缀后缀
file-master rename "D:\music\" --prefix "2026_" --suffix "_final"
```

### 2. 智能文件整理
```
# 按类型整理
file-master organize "D:\downloads\" --by type

# 按日期整理
file-master organize "D:\photos\" --by date --format "YYYY-MM"

# 按大小整理  
file-master organize "D:\files\" --by size --groups "small,medium,large"
```

### 3. 高级搜索
```
# 内容搜索
file-master search "D:\projects\" --content "TODO:" --recursive

# 元数据搜索
file-master search "D:\photos\" --metadata "camera=Canon" --date "2026-01-01..2026-03-31"

# 重复文件查找
file-master find-duplicates "D:\backup\" --algorithm md5
```

### 4. 格式转换
```
# 图片格式转换
file-master convert "D:\images\*.jpg" --to png --quality 90

# 文档格式转换
file-master convert "D:\docs\*.docx" --to pdf

# 批量压缩
file-master compress "D:\files\" --format zip --level 9
```

### 5. 文件操作
```
# 批量复制
file-master copy "D:\source\*.txt" "D:\backup\"

# 批量移动
file-master move "D:\temp\*.log" "D:\logs\"

# 批量删除
file-master delete "D:\cache\*.tmp" --confirm
```

## 使用场景

### 场景1：整理照片库
```
# 将杂乱的照片按日期整理
file-master organize "D:\Camera\" --by date --format "YYYY-MM-DD"
file-master rename "D:\Camera\2026-03\*" --pattern "IMG_{date:YYYYMMDD}_{num:03d}.jpg"
```

### 场景2：清理下载文件夹
```
# 自动分类下载文件
file-master organize "D:\Downloads\" --by type --auto-clean
file-master find-duplicates "D:\Downloads\" --delete
```

### 场景3：项目文件管理
```
# 批量重命名项目文件
file-master rename "D:\Project\*.js" --prefix "module_"
file-master search "D:\Project\" --content "deprecated" --report
```

### 场景4：备份和归档
```
# 创建智能备份
file-master backup "D:\Work\" --to "E:\Backup\" --incremental
file-master compress "D:\Archives\2026-Q1\" --format 7z --password "secure123"
```

## 安装和使用

### 快速开始
```bash
# 安装技能
openclaw skills install file-master-pro

# 基本使用
file-master --help
file-master rename --help
```

### 配置选项
```yaml
# ~/.file-master/config.yaml
defaults:
  confirm_deletion: true
  backup_before_rename: true
  log_level: info
  
paths:
  downloads: "D:\Downloads"
  photos: "D:\Pictures"
  documents: "D:\Documents"
  
rules:
  auto_organize_downloads: true
  clean_temp_files_daily: true
  backup_important_folders: weekly
```

## 高级功能

### 1. 自动化工作流
```yaml
# 定义自动化工作流
workflows:
  daily_cleanup:
    trigger: daily 02:00
    steps:
      - organize_downloads
      - clean_temp_files
      - backup_changes
      
  photo_import:
    trigger: file_added "D:\Camera\"
    steps:
      - rename_by_date
      - convert_to_jpg
      - backup_to_cloud
```

### 2. 自定义脚本
```python
# 使用Python API扩展功能
from file_master import FileMaster

fm = FileMaster()
fm.rename_files("D:\docs\", pattern="doc_{num:04d}.txt")
fm.organize_by_type("D:\downloads\")
fm.find_duplicates("D:\photos\", delete=True)
```

### 3. 集成OpenClaw
```javascript
// 在OpenClaw中直接使用
const result = await exec({
  command: 'file-master organize "D:\\Downloads\\" --by type --auto-clean'
});

// 或使用技能接口
const files = await fileMaster.search({
  path: "D:\\Projects\\",
  content: "TODO",
  recursive: true
});
```

## 安全特性

### 数据保护
- **操作确认**：重要操作前要求确认
- **自动备份**：重命名和删除前自动备份
- **操作日志**：记录所有文件操作
- **撤销功能**：支持操作撤销

### 权限控制
- **只读模式**：测试模式不实际修改文件
- **沙箱模式**：在隔离环境中测试
- **权限检查**：检查文件访问权限
- **用户确认**：敏感操作需要用户确认

## 系统要求

### 最低要求
- **操作系统**：Windows 10+ / macOS 10.15+ / Linux
- **内存**：512MB RAM
- **磁盘空间**：50MB
- **Python**：3.8+（可选，用于高级功能）

### 推荐配置
- **操作系统**：Windows 11 / macOS 12+ / Ubuntu 20.04+
- **内存**：2GB RAM
- **磁盘空间**：100MB
- **Python**：3.11+（推荐）

## 更新计划

### v1.1.0（计划中）
- 云存储集成（Google Drive, Dropbox）
- AI智能分类功能
- 更多文件格式支持
- 性能优化

### v1.2.0（规划中）
- 移动端应用
- 团队协作功能
- 高级分析报告
- 插件系统

## 技术支持

### 获取帮助
- **文档**：https://docs.file-master.pro
- **社区**：https://community.file-master.pro
- **支持**：support@file-master.pro
- **问题反馈**：https://github.com/file-master-pro/issues

### 常见问题
**Q: 是否支持网络路径？**
A: 是的，支持UNC路径和映射网络驱动器。

**Q: 处理大量文件时性能如何？**
A: 采用多线程和增量处理，支持百万级文件。

**Q: 是否支持撤销操作？**
A: 是的，所有修改操作都支持撤销。

**Q: 是否有试用版？**
A: 提供7天免费试用，功能无限制。

## 购买和授权

### 定价
- **个人版**：$9.99（永久授权，1台设备）
- **家庭版**：$19.99（永久授权，5台设备）
- **商业版**：$49.99（永久授权，无限设备）

### 购买方式
1. **ClawHub商店**：直接购买并自动安装
2. **官网购买**：获取授权码手动激活
3. **批量采购**：联系销售获取报价

### 退款政策
30天内无条件退款，如果产品不符合您的需求。

---

**让文件管理变得简单高效！** 🚀

*文件管理大师 - 您的智能文件管家*