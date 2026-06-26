# AI File Organizer - 快速开始指南

🚀 5 分钟上手 AI 智能文件整理

---

## 📦 安装（1 分钟）

```bash
# 1. 进入技能目录
cd ~/.openclaw/workspace/skills/ai-file-organizer

# 2. 安装依赖
pip install aiofiles aiomultiprocess tqdm pyyaml

# 3. 验证安装
python scripts/organizer.py --demo
```

看到演示成功输出即安装完成 ✅

---

## 🎯 基础使用（2 分钟）

### 场景 1: 整理下载文件夹

```bash
# 最简单的方式
python scripts/organizer.py --organize ~/Downloads
```

**效果:**
- 自动创建 `Organized` 文件夹
- 文件按类型分类（文档、图片、视频、代码等）
- 智能重命名（日期_类型_原名格式）

### 场景 2: 清理重复文件

```bash
# 检测并移动重复文件
python scripts/organizer.py --duplicates ~/Files
```

**效果:**
- 自动检测内容完全相同的文件
- 保留一份，其余移动到 `_duplicates` 文件夹
- 显示释放的磁盘空间

### 场景 3: 自定义整理规则

```bash
# 创建配置文件
cat > my_config.yaml << EOF
naming:
  format: "{date}_{original}"
  date_format: "%Y%m%d"

classification:
  categories:
    - name: "工作"
      keywords: ["报告", "方案", "合同"]
      folder: "Work"
    - name: "学习"
      keywords: ["教程", "课程"]
      folder: "Learning"
EOF

# 使用配置
python scripts/organizer.py --organize ~/Downloads --config my_config.yaml
```

---

## ⚡ 进阶技巧（2 分钟）

### 技巧 1: 提升处理速度

```bash
# 增加并发数（默认 10）
python scripts/organizer.py --organize ~/Downloads --concurrent 20

# 禁用缓存（首次整理时）
python scripts/organizer.py --organize ~/Downloads --no-cache
```

### 技巧 2: 预览整理方案

```bash
# 先预览，确认后再执行
python scripts/organizer.py --organize ~/Downloads --dry-run
```

### 技巧 3: 导出整理报告

```bash
# 生成 JSON 报告
python scripts/organizer.py --organize ~/Downloads --report report.json

# 查看详细统计
cat report.json | python -m json.tool
```

### 技巧 4: 定时自动整理

```bash
# 编辑 crontab
crontab -e

# 添加：每周日凌晨 2 点自动整理
0 2 * * 0 python /path/to/organizer.py --organize ~/Downloads
```

---

## 🎨 配置示例

### 最简配置（推荐新手）

```yaml
# minimal_config.yaml
naming:
  format: "{date}_{type}_{original}"
  max_length: 100

classification:
  categories:
    - name: "文档"
      keywords: ["pdf", "doc", "txt"]
      folder: "Documents"
    - name: "图片"
      extensions: ["jpg", "png", "gif"]
      folder: "Images"
```

### 完整配置（高级用户）

```yaml
# full_config.yaml
naming:
  format: "{date}_{type}_{original}"
  date_format: "%Y%m%d"
  max_length: 100
  replace_spaces: true

classification:
  enabled: true
  categories:
    - name: "工作文档"
      keywords: ["报告", "方案", "合同", "发票"]
      folder: "Work/Documents"
    - name: "财务报表"
      keywords: ["预算", "决算", "账单"]
      folder: "Work/Finance"
    - name: "代码项目"
      extensions: ["py", "js", "java", "go"]
      folder: "Code"
    - name: "图片视频"
      extensions: ["jpg", "png", "mp4", "mov"]
      folder: "Media"

duplicates:
  enabled: true
  move_to_folder: "_duplicates"

cache:
  enabled: true
  max_size: 10000

logging:
  level: "INFO"
  file: "logs/organizer.log"
```

---

## ❓ 常见问题

### Q: 处理速度慢？
```bash
# 增加并发数
python scripts/organizer.py --organize ~/Downloads --concurrent 20
```

### Q: 分类不准确？
完善配置文件中的关键词：
```yaml
classification:
  categories:
    - name: "工作"
      keywords: ["报告", "方案", "合同", "发票", "会议纪要"]  # 添加更多关键词
      folder: "Work"
```

### Q: 如何撤销操作？
整理是复制文件（非移动），原文件保留。如需清理：
```bash
# 删除整理后的文件夹
rm -rf ~/Organized
```

### Q: 支持哪些文件类型？
支持所有常见文件类型：
- 📄 文档：PDF, DOC, DOCX, TXT, MD
- 📊 表格：XLS, XLSX, CSV
- 🖼️ 图片：JPG, PNG, GIF, BMP, SVG, WEBP
- 🎥 视频：MP4, AVI, MOV, MKV
- 🎵 音频：MP3, WAV, FLAC
- 💻 代码：PY, JS, JAVA, CPP, GO, RS
- 📦 压缩：ZIP, RAR, 7Z, TAR, GZ

---

## 📊 性能参考

| 文件数量 | 耗时 | 速度 |
|---------|------|------|
| 100 个 | 5 秒 | 20 个/秒 |
| 1000 个 | 45 秒 | 22 个/秒 |
| 10000 个 | 7 分钟 | 24 个/秒 |

*测试环境：8 核 CPU, SSD, 默认配置*

---

## 🆘 获取帮助

```bash
# 查看完整帮助
python scripts/organizer.py --help

# 查看版本
python scripts/organizer.py --version

# 查看详细日志
python scripts/organizer.py --organize ~/Downloads --verbose
```

---

## 📚 下一步

- 📖 阅读完整文档：[README.md](README.md)
- 🔧 学习性能调优：[docs/PERFORMANCE.md](docs/PERFORMANCE.md)
- 💡 查看更多示例：[examples/](examples/)
- 🐛 遇到问题？[故障排查指南](README.md#故障排查)

---

<div align="center">

**开始整理你的文件吧！** 🎉

遇到问题？查看 [README.md](../README.md) 或提 Issue

</div>
