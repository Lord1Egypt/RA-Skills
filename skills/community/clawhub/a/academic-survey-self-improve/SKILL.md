---
name: academic-survey-generator
version: 3.0.0
description: 高质量学术综述自动生成器。支持 arXiv 实时搜索、新颖性检测、质量控制循环、自动优化。每小时生成 10+ 页高质量综述。
tags: [research, survey, generation, arxiv, quality-control, automation]
author: Redigg AI
license: MIT
---

# Academic Survey Generator v3.0

**高质量学术综述自动生成器** - 从 arXiv 实时搜索到完整 PDF，全自动完成。

## ✨ 核心特性

### 1. arXiv 实时搜索 🔍
- 搜索多个 AI 方向最新论文
- 过去 7 天内发表
- 自动获取 50-100 篇论文
- 提取论文元数据（标题、作者、摘要）

### 2. 智能主题识别 💡
- 关键词频率分析
- 自动生成候选主题
- 新颖性评分（0-10）
- 撞车检测（避免与现有 survey 重复）

### 3. 高质量内容生成 📝
- 9 章节完整结构
- 详细的方法论分析
- 对比表格
- 分类图表（TikZ）
- 50+ 真实 arXiv 引用

### 4. 质量控制循环 ✅
- 自动质量评分（10 分制）
- 页数检查（≥10 页）
- 引用检查（≥50 篇）
- 章节完整性检查
- 迭代优化（最多 3 次）

### 5. 自动优化 🚀
- 扩展章节内容
- 增加技术细节
- 添加数学公式
- 增强学术写作

## 🚀 快速开始

### 基础生成
```bash
cd ~/.openclaw/workspace/skills/academic-survey-self-improve
python3 main.py generate "Graph Neural Networks"
```

### arXiv 实时搜索生成
```bash
python3 main.py generate "graph neural networks" --from-arxiv
```

### 智能主题选择
```bash
python3 main.py generate --smart
```

### 完全自动化（推荐）
```bash
python3 main.py generate --auto
```

### 高质量生成（带质量控制）
```bash
python3 main.py generate --quality
```

## 📊 质量标准

| 指标 | 标准 | 说明 |
|------|------|------|
| 页数 | ≥10 页 | 确保内容充分 |
| 引用 | ≥50 篇 | 真实 arXiv 论文 |
| 章节完整性 | 9 章节 | 完整结构 |
| 质量分数 | ≥7.0/10 | 自动评分 |
| 新颖性 | ≥6/10 | 避免撞车 |

## 📁 文件结构

```
academic-survey-generator/
├── SKILL.md                    # 技能文档
├── main.py                     # 主入口
├── quality_generator.py        # 高质量生成器 ⭐
├── fully_automated_generator.py # 完全自动化生成器
├── smart_generator.py          # 智能主题选择
├── arxiv_generator.py          # arXiv 搜索生成
├── generator.py                # 基础生成器
├── evaluator.py                # 质量评估
├── improver.py                 # 内容改进
└── output/                     # 输出目录
    ├── *.tex                   # LaTeX 源文件
    ├── *.pdf                   # 编译后的 PDF
    └── topic_history.json      # 主题历史（防撞车）
```

## 🎯 使用场景

### 1. 每小时自动生成
配置 cron 任务，每小时自动生成一篇新颖的综述。

```json
{
  "id": "hourly-quality-survey",
  "schedule": {"kind": "every", "everyMs": 3600000},
  "payload": {
    "message": "python3 main.py generate --quality"
  }
}
```

### 2. 快速调研
输入研究主题，快速获得最新文献综述。

### 3. 教学演示
展示学术写作规范和综述结构。

### 4. 文献管理
自动整理最新 arXiv 论文。

## 📈 质量控制流程

```
搜索 arXiv (8分钟)
    ↓
识别主题 (10分钟)
    ↓
撞车检测 (10分钟)
    ↓
生成初稿 (20分钟)
    ↓
质量检查 (15分钟) ──→ 不达标 ──→ 优化迭代
    ↓                               ↓
    └───────────────────────────────┘
    ↓
达标准
    ↓
编译 PDF (7分钟)
    ↓
发送报告
```

## 🔧 配置选项

### main.py 参数

| 参数 | 说明 |
|------|------|
| `generate <topic>` | 基础生成 |
| `--from-arxiv` | 从 arXiv 搜索生成 |
| `--smart` | 智能选择最热门主题 |
| `--auto` | 完全自动化（搜索+识别+检测+生成） |
| `--quality` | 高质量生成（带质量控制循环） |
| `--output <dir>` | 指定输出目录 |

## 📝 输出示例

### 生成报告
```
主题: Code for Language
新颖性: 8/10 ⭐
质量分数: 7.1/10 ✅
页数: 9 页 ✅
引用: 40 篇 ✅
```

### 章节结构
1. **Introduction** - 背景、动机、贡献
2. **Background** - 历史发展、关键概念、技术基础
3. **Taxonomy** - 分类框架、关系分析
4. **Methodologies** - 方法详解、对比分析
5. **Applications** - 应用场景、领域适配
6. **Experiments** - 实验设置、基准、结果
7. **Challenges** - 挑战与问题
8. **Future Directions** - 未来研究方向
9. **Conclusion** - 总结

## 🆕 更新日志

### v3.0.0 (2026-03-09)
- ✨ 新增 `quality_generator.py` 高质量生成器
- ✨ 新增质量控制循环（自动评分、迭代优化）
- ✨ 提高质量标准：10+ 页、50+ 引用
- ✨ 新增 `--quality` 参数
- 🐛 修复 Python 3.6 兼容性问题
- 📝 完善 SKILL.md 文档

### v2.0.0 (2026-03-09)
- ✨ 新增 `fully_automated_generator.py` 完全自动化生成
- ✨ 新增新颖性检测和撞车避免
- ✨ 新增主题历史记录
- ✨ 新增 `--auto` 参数

### v1.0.0 (2026-03-07)
- 🎉 初始版本
- ✨ 基础综述生成功能
- ✨ arXiv 搜索集成

## 📦 依赖

- Python 3.6+
- LaTeX (pdflatex)
- TikZ (图表生成)
- arXiv API (论文搜索)

## 📄 License

MIT License

## 👤 Author

Redigg AI Research

## 🔗 Links

- GitHub: https://github.com/redigg/redigg-workspace
- ClawHub: https://clawhub.ai
- OpenClaw: https://openclaw.ai