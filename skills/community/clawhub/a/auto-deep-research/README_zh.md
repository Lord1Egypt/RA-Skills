# Deep Research Skill for Claude Code

[English](README.md) | [中文](README_zh.md)

> If you find this project helpful, please give it a star! :star:

![架构图](architecture.png)

自动深度研究技能。给 Claude Code 等 AI Agent 用的研究助手，通过多轮搜索和多源验证，输出结构化报告。

## 使用场景

- **概念调研**: 了解技术原理、学习新概念
- **工具对比**: 选型评估、竞品分析
- **趋势追踪**: 行业动态、事件分析
- **深度调查**: 主题研究、信息收集

## 安装

```bash
git clone https://github.com/Pancat009/auto-deep-research-skill
cd auto-deep-research-skill
cp env.example .env
```

配置 API Key（至少一个）：
- Tavily: https://tavily.com
- Jina Reader: https://jina.ai/reader

## 使用

```bash
# 赋予脚本执行权限
chmod +x scripts/*.sh
```

触发命令：
```
/auto-deep-research 你的研究问题
```

## 输出文件

每次研究在 `output/{topic-slug}/` 目录下生成：
- `state.json` - 执行状态（轮数、子问题进度）
- `memo.json` - 结构化研究笔记
- `sources.json` - 来源列表
- `report.md` - 最终报告

## 文件结构

```
auto-deep-research-skill/
├── SKILL.md              # 技能定义
├── README.md             # 中文说明
├── README_en.md          # English
├── env.example           # 环境变量示例
├── scripts/
│   ├── search.sh         # 搜索脚本
│   └── read_page.sh      # 页面读取脚本
├── references/
│   ├── conflict-detection.md
│   └── source-trust.md
└── evals/
    └── evals.json
```

## 版本

v0.0.1 - 初始版本