# Bilibili Video Analyzer

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🎓 分析B站学术视频，自动生成**清洁版学习笔记**

一个智能的 B站视频分析工具，能够自动下载视频、转录字幕、使用 AI 提取知识点，并生成专业的 Markdown 学习报告。

## ✨ 核心功能

- 🎬 **视频下载** - 支持B站扫码登录，下载高清视频
- 🎤 **智能转录** - 使用 Whisper AI 生成高质量中文字幕
- 🤖 **AI 分析** - Claude 自动提取核心知识点和关键概念
- 📸 **关键截图** - 自动捕获10张关键画面
- 📝 **精美报告** - 生成结构化 Markdown 学习笔记
- 🎯 **质量保证** - 28项质量检查清单，确保输出标准

## 🚀 快速开始

### 安装

```bash
# 安装依赖工具
pip install railgun-bili-tools

# 验证安装
bili-dl --version
```

### 系统要求

- Python 3.7+
- FFmpeg（用于视频处理）
- 足够的磁盘空间（视频+报告约 1-2GB）

### 使用示例

```bash
# 分析一个B站视频
python scripts/analyze_video.py BV1ms4y1Y76i

# 或使用完整URL
python scripts/analyze_video.py https://www.bilibili.com/video/BV1ms4y1Y76i

# 指定输出目录
python scripts/analyze_video.py BV1ms4y1Y76i --output ./my_reports
```

## 📖 文档导航

| 文档 | 说明 |
|------|------|
| [📘 SKILL.md](SKILL.md) | 完整的使用指南和工作流程 |
| [📖 BEST_PRACTICES.md](references/BEST_PRACTICES.md) | 最佳实践和质量标准（535行） |
| [✅ QUICK_QUALITY_CHECKLIST.md](references/QUICK_QUALITY_CHECKLIST.md) | 28项质量检查清单 |
| [📁 references/](references/) | 参考文档目录 |

## 🎯 输出示例

生成的学习笔记包含：

```
reports/2026-02-28/BV1ms4y1Y76i_细胞聚团原因剖析/
├── 细胞聚团原因剖析.mp4              # 原视频
├── 细胞聚团原因剖析.srt              # SRT字幕
├── 细胞聚团原因剖析_transcript.txt   # 转录文本
├── 细胞聚团原因剖析_analysis.json    # AI分析结果
├── 细胞聚团原因剖析_学习笔记.md       # 学习报告
└── screenshots/                      # 关键截图
    ├── screenshot_001_120.5s.jpg
    ├── screenshot_002_280.0s.jpg
    └── ...
```

**学习笔记结构**：
- 📌 **核心知识点卡片**（6-10个）
  - 标题（10-15字）
  - 核心概念（20-30字）
  - 详细说明（200-400字）
  - 关键要点（3-5个）
  - 配图截图
- 🎯 **知识框架总结**
- 💡 **实践价值说明**
- 📚 **学习建议**（6条）

## 🔧 工作流程

```
1. 🔐 登录检查        → bili-dl login
2. 📹 视频下载        → bili-dl download
3. 🎤 转录字幕        → bili-dl transcribe
4. 🤖 AI 分析         → Claude 提取知识点
5. 📸 截取画面        → FFmpeg 批量截图
6. 📝 生成报告        → Markdown 学习笔记
```

**预计耗时**：
- 短视频（5-10分钟）：约 15-20分钟
- 中等视频（20-30分钟）：约 30-45分钟
- 长视频（60分钟+）：约 1-2小时

## 📊 质量标准

基于成功案例 [BV1ms4y1Y76i](reports/2026-02-28/) 的质量标准：

| 指标 | 标准 | 说明 |
|------|------|------|
| 知识点数量 | 6-10个 | 平衡深度和广度 |
| 单点字数 | 200-400字 | 信息密度适中 |
| 核心概念 | 20-30字 | 一句话精髓 |
| 关键要点 | 3-5个/点 | 便于记忆 |
| 截图数量 | 10张 | 均匀分布 |
| 质量评分 | ≥25/28 | 优秀标准 |

使用 [快速质量检查清单](references/QUICK_QUALITY_CHECKLIST.md) 进行自评。

## 🛠️ 技术栈

- **视频处理**: bilibili-dl, FFmpeg
- **语音识别**: OpenAI Whisper
- **AI 分析**: Claude API
- **报告生成**: Python + Markdown

## 📝 版本历史

**当前版本**: v1.1.0 (2026-02-28)

- ✅ 增强内容生成指南
- ✅ 完善最佳实践文档
- ✅ 28项质量检查清单
- ✅ 真实案例参考

查看 [CHANGELOG.md](CHANGELOG.md) 了解完整历史。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 [LICENSE](../../LICENSE) 文件

## ⭐ 相关项目

- [bilibili-dl](https://github.com/railgun9983/bilibili-download) - B站视频下载工具

---

**💡 提示**: 首次使用建议先阅读 [SKILL.md](SKILL.md) 了解完整工作流程，然后参考 [BEST_PRACTICES.md](references/BEST_PRACTICES.md) 提升输出质量。
