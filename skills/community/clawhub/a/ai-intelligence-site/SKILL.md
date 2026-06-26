---
name: ai-intelligence-site
version: 1.0.0
description: >
  AI 情报中心网站自动化管理。创建、更新、部署 AI 竞品分析网站到 GitHub Pages。
  支持 5 个子站：全球站、中文站、Skills站、资讯站、模型站。
  每日自动更新：删除旧数据 → Serper 搜索发现网站 → 获取真实流量 → 推送 GitHub。
  触发词：AI情报中心、竞品分析网站、AI聚合网站、更新情报站、intelligence site。
---

# AI 情报中心网站管理

自动化管理 AI 竞品分析网站，部署到 GitHub Pages。

## 网站结构

```
competitor-site/
├── index.html          # 全球站（AI 聚合网站）
├── data.json           # 全球站数据
├── cn/                 # 中文站
├── skills/             # Skills & MCP 站
├── news/               # AI 资讯站
├── models/             # AI 模型站
└── daily_update.py     # 每日更新脚本
```

## 核心功能

### 1. 每日全量更新

执行脚本：
```bash
python3 scripts/daily_update.py
```

更新流程：
1. 删除旧数据，从零开始
2. 通过 Serper 搜索发现新网站
3. 获取每个网站的真实流量数据
4. 无数据则跳过（不使用模拟）
5. 重新计算层级（T1/T2/T3）和趋势
6. 推送到 GitHub

### 2. 数据源配置

每个站点有独立的搜索关键词和已知网站列表：

| 站点 | 搜索关键词示例 |
|------|---------------|
| 全球 | AI tools directory, AI aggregator |
| 中文 | 中国AI工具导航, AI工具集 |
| Skills | MCP server marketplace, Claude skills |
| 资讯 | AI news website, AI newsletter |
| 模型 | LLM API provider, AI model platform |

### 3. 数据结构

```json
{
  "lastUpdated": "ISO时间戳",
  "competitors": [
    {
      "id": "唯一标识",
      "name": "网站名称",
      "domain": "域名",
      "monthlyVisits": 1000000,
      "tier": "T1/T2/T3",
      "trafficTrend": [历史流量数组]
    }
  ],
  "insights": [{"title": "", "content": "", "color": ""}]
}
```

### 4. 层级划分

- **T1**: 月访问 ≥ 100万
- **T2**: 月访问 10万-100万
- **T3**: 月访问 < 10万

## 环境变量

- `SERPER_API_KEY`: Serper 搜索 API Key（必需）

## 部署

1. 创建 GitHub 仓库并启用 Pages
2. 配置 Git remote
3. 运行 `daily_update.py` 初始化数据
4. 设置定时任务每日更新
