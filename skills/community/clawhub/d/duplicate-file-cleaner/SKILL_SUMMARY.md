# duplicate-file-cleaner 技能

一个智能的重复文件检测与整理工具，帮助你快速识别和清理计算机中的重复文件，释放宝贵的磁盘空间。

## ✨ 功能亮点

- **精准检测**：基于文件内容哈希比对，准确识别完全相同的重复文件
- **智能过滤**：支持按文件类型、大小进行筛选，聚焦高价值重复文件
- **安全删除**：提供智能删除建议，标注高风险文件，避免误删
- **详细报告**：生成结构化扫描报告，清晰展示重复文件分布和可释放空间
- **灵活执行**：支持自动删除、手动确认、备份后删除多种模式

## 🎯 使用场景

- 📁 **文件整理**：清理重复下载的文件，释放磁盘空间
- 🖼️ **照片库管理**：删除重复的图片和视频，特别是多设备同步后的照片
- 📄 **项目清理**：清理项目文件中的冗余备份
- 💾 **空间优化**：快速释放磁盘空间，提升系统运行效率
- 🔄 **数据同步后处理**：处理云同步、多设备备份产生的重复文件

## 📖 快速开始

### 扫描照片库
```bash
python duplicate-file-cleaner/scripts/duplicate_scanner.py \
  --directory ~/Pictures \
  --output report.json \
  --min-size 10240 \
  --extensions jpg,png,heic
```

### 扫描下载目录
```bash
python duplicate-file-cleaner/scripts/duplicate_scanner.py \
  --directory ~/Downloads \
  --output report.json \
  --min-size 102400
```

## 📋 系统要求

- Python 3.8 或更高版本
- 操作系统：Windows、macOS、Linux 均支持

## 📦 技能文件结构

```
duplicate-file-cleaner/
├── SKILL.md                          # 技能详细说明文档
├── README.md                         # 用户使用指南
├── manifest.md                       # 技能元数据清单
├── requirements.txt                  # 依赖说明（使用标准库，无外部依赖）
├── scripts/
│   ├── duplicate_scanner.py         # 核心扫描脚本
│   └── __pycache__/                  # Python 缓存目录
└── references/
    └── file-organization-guide.md    # 文件整理最佳实践指南
```

## ⚠️ 使用建议

### 安全优先
- 操作前先备份重要数据
- 建议优先从用户目录开始扫描（Documents、Pictures、Downloads）
- 避免直接扫描系统目录（如 Windows/Program Files）

### 效率优化
- 先设置较大的 `--min-size` 过滤小文件
- 使用 `--extensions` 限制扫描的文件类型
- 大目录扫描可能需要较长时间，请耐心等待

## 📚 详细文档

- [详细使用说明](SKILL.md) - 完整的功能介绍和操作步骤
- [用户指南](README.md) - 详细的使用教程和常见问题解答
- [整理最佳实践](references/file-organization-guide.md) - 文件管理专业建议

## 🏷️ 标签

文件管理、磁盘清理、照片整理、数据优化、系统工具

## 📅 版本信息

- 当前版本：v1.0.0
- 兼容性：Python 3.8-3.13，支持 Windows/macOS/Linux
