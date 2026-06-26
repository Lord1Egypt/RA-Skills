---
name: arxiv-daily-skill
description: 每日自动搜集 arXiv 论文（LLM/RAG/Agent 方向），带机构信息，飞书推送
version: "1.0.0"
author: OpenClaw User
license: MIT
---

# arXiv 每日论文精选 Skill

## 功能
每日自动搜集 arXiv 上 LLM/RAG/Agent/Context/Harness 等方向的最新高价值论文（2-5 篇），整理成易于阅读的简洁形式，通过飞书推送给用户。

## 触发方式
- **定时任务**：每个工作日上午 9:00 自动执行
- **手动触发**：用户发送"今日论文"、"arxiv 推荐"、"论文推送"、"看看今天的论文"等关键词
- **深度分析**：用户发送"详解第 X 篇"、"分析 [arXiv ID]"、"用 ljg-paper 分析这篇"

## 执行流程

### 1. 搜集论文
使用 arXiv API 搜索以下方向的最新论文（过去 3 天内）：
- Large Language Model (LLM)
- Retrieval Augmented Generation (RAG)
- AI Agent / Autonomous Agent
- Context Window / Context Management
- AI Harness / Agent Harness
- Transformer Architecture
- Language Model Reasoning
- Multimodal LLM

### 2. 筛选排序
- 过滤掉非 CS 领域（排除物理、生物、医学等）
- 优先选择 cs.CL, cs.AI, cs.LG, stat.ML 分类
- 根据标题关键词打分排序
- 去重后选择 Top 10（目录）+ Top 5（详解）

### 3. 机构信息提取
- 从机构数据库 `affiliations_db.json` 中查找（自动累积）
- 首次遇到的论文自动从 arXiv HTML 页面提取
- 支持知名机构识别：清华、北大、斯坦福、MIT、Google、Meta、华为等

### 4. 格式化输出
生成 Markdown 格式报告：

```markdown
# 📚 今日 ArXiv 论文推送 (2026-04-16)

## 📋 目录
1. 论文标题 1
2. 论文标题 2
...

---

## 📖 论文详解

### 1. 论文完整标题
**arXiv**: 2604.13016v1 | 2026-04-14 | Tsinghua University + THUNLP
**作者**: Yaxuan Li, Yuxin Zuo, Bingxiang He et al.
**链接**: https://arxiv.org/abs/2604.13016v1

**中文摘要**:
> ...

**解决的问题**:
- ...

**核心创新**:
- ...

**为什么重要**:
- ...

**局限性**:
- ...
```

### 5. 推送
- **飞书推送**：目录 + Top 5 详解（通过 Webhook）
- **文件保存**：完整报告保存到 `/tmp/arxiv_daily_YYYYMMDD.md`

## 输出要求
- **紧凑目录**：仅标题，快速浏览
- **详解格式**：包含机构、作者、链接、摘要、问题、创新、重要性、局限性
- **机构信息**：每篇论文必须显示机构（如"Tsinghua University + THUNLP"）
- **中文友好**：摘要保留英文原文，分析使用中文

## 配置
- 推送时间：工作日 09:00（Asia/Shanghai）
- 推送渠道：飞书（Webhook）
- 论文数量：目录 10 篇 + 详解 5 篇/天
- 时间范围：过去 3 天内的新论文

## 文件结构
```
arxiv-daily-skill/
├── SKILL.md                    # 本文件
├── fetch_arxiv.py              # 核心脚本
├── deep_analyze.py             # 深度分析工具
├── cron_run.sh                 # Cron 执行入口
├── run.sh                      # 手动测试
├── affiliations_db.json        # 机构数据库（自动累积）
├── feishu_config.json          # 飞书配置
└── README.md                   # 使用文档
```

## 依赖
- arXiv API（无需 API Key）
- Python 3.6+
- 飞书 Webhook（可选，用于推送）
- cron（定时任务）

## 高级功能

### 深度分析模式
对单篇论文进行详细解读：
```bash
python3 deep_analyze.py 2604.13016
```

或调用 `ljg-paper` skill：
- "用 ljg-paper 分析 2604.13016"
- "详解第 3 篇论文"

### 机构数据库
自动累积的机构信息保存在 `affiliations_db.json`：
```json
{
  "affiliations": {
    "2604.13016": ["Tsinghua University", "THUNLP"],
    "2604.13029": ["Huawei Technologies Co., Ltd."]
  }
}
```

### 自定义搜索方向
修改 `fetch_arxiv.py` 中的 `SEARCH_CONFIGS`：
```python
SEARCH_CONFIGS = [
    {"query": "cat:cs.AI AND all:large language model", "label": "LLM", "max": 3},
    # 添加新的搜索方向...
]
```

## 飞书配置

1. 在飞书群聊中添加自定义机器人
2. 复制 Webhook 地址
3. 编辑 `feishu_config.json`，填入 `webhook_url`
4. 测试推送：`./cron_run.sh`

## 示例对话

**用户**: "今天有什么新论文？"
**助理**: 推送今日 ArXiv 论文目录 + Top 5 详解

**用户**: "详解第 3 篇"
**助理**: 调用 `deep_analyze.py` 或 `ljg-paper` 进行深度分析

**用户**: "用 ljg-paper 分析 2604.13016"
**助理**: 生成完整的中文解读报告（费曼翻译 + 核心概念 + 博导审稿）

---

**版本**: v5  
**最后更新**: 2026-04-16  
**维护者**: OpenClaw Agent
