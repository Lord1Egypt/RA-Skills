---
name: Design_Daily
description: "Daily design industry brief for UI/UX designers and PMs. Covers AI × design, design engineering, top product experience breakdowns, and design decision logic. Triggers: 'design brief', '设计日报', '今日设计', '设计早报', 'design news today'"
version: "1.0.2"
author: ""
license: MIT
requires:
  env:
    - SERPER_API_KEY     # 必填：google.serper.dev 获取，免费额度 2500次/月
    - DEEPSEEK_API_KEY   # 必填：platform.deepseek.com 获取，极低费用
  python: ">=3.9"
  packages:
    - requests
    - pyyaml
---

# Design_Daily

每天自动抓取产品设计领域最新动态，提炼成**设计师之间的高质量谈资**。

每条内容只回答一个问题：

> **「这件事，对我这个岗位意味着什么？」**

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Keys

在 OpenClaw 环境变量中设置：

```bash
SERPER_API_KEY=你的Serper密钥      # 免费：google.serper.dev
DEEPSEEK_API_KEY=你的DeepSeek密钥  # 极低费用：platform.deepseek.com
```

### 3. 编辑 config.yaml

打开 `config.yaml`，取消注释你的岗位即可：

```yaml
roles:
  - UI设计师
  - UX设计师
  # - 交互设计师   ← 取消注释即可启用
```

> 💡 选 1~2 个岗位 → 内容更聚焦；选越多 → 信息面越广，但每条针对性会降低

### 4. 运行

```bash
# 一键配置向导（推荐首次使用）
python setup.py

# 或直接运行
python run.py

# 预览模式（不保存文件）
python run.py --preview
```

---

## 输出示例

```
  Design Daily  ·  2026/03/18
  UI设计师  ·  UX设计师
  ──────────────────────────────────────────
  今天有条挺有意思的：Figma 偷偷在学你怎么排版

  01  Figma 上线 AI 自动布局推断  [UI设计师]
      Figma 新功能可以根据内容自动推断间距和对齐规则，不用手动调了。

  ┃  说实话这个角度挺好玩——它不是在「帮你排版」，
     而是在观察你平时怎么排，然后复刻你的习惯。
     有点像带了个很会偷师的实习生。

  Figma Blog  →  https://figma.com/blog/...
  ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

  02  ...

  ──────────────────────────────────────────
  延伸阅读
  · Figma 上线 AI 自动布局推断
    https://figma.com/blog/...
  ──────────────────────────────────────────
```

---

## 定时运行（可选）

```bash
# 每天早 9 点自动运行
0 9 * * * cd /path/to/Design_Daily && python run.py >> logs/cron.log 2>&1
```

---

## 费用说明

| API | 免费额度 | 超出费用 |
|-----|---------|---------|
| Serper | 2500次/月 | $50/1000次 |
| DeepSeek | — | 约 ¥0.015/次 |

每天运行 1 次，**合计每月约 ¥20**。

---

## 文件结构

```
Design_Daily/
├── SKILL.md          # 本文件
├── config.yaml       # 用户配置（只改这里）
├── setup.py          # 一键配置向导
├── run.py            # 运行入口
├── fetch.py          # 搜索抓取模块
├── brief.py          # 日报生成模块
├── requirements.txt  # 依赖声明
└── logs/             # 运行日志 + 输出文件（自动创建）
```
