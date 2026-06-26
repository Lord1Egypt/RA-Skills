# 🔥 cn-hot-trends

> 中文全平台热搜聚合。知乎·微博·百度·B站·抖音·头条，一键获取。

## 功能

- **6大平台热搜** — 知乎/微博/百度/B站/抖音/头条实时热搜
- **全平台总榜** — 跨平台热度综合排名
- **AI选题推荐** — 基于热搜自动生成内容选题 + 目标平台 + 切入角度 + 建议标题
- **JSON输出** — 方便接入其他工具

## 快速开始

```bash
# 全平台热搜
python3 scripts/fetch_trends.py

# 单平台
python3 scripts/fetch_trends.py --platform zhihu

# AI选题推荐
python3 scripts/fetch_trends.py --platform zhihu --limit 5 --recommend

# JSON格式
python3 scripts/fetch_trends.py --json
```

## AI选题推荐示例

```
🎯 AI选题推荐
1. 李想朋友圈发飙...
   📍 平台: 知乎 | 专业分析文 | 给背景、分析、结论
   🎯 可写角度: 行业分析 / 竞争格局 / 创始人故事
   📝 建议标题:「关于「李想朋友圈发飙」，我从3个角度拆解」
```

## 数据来源

所有数据来自平台公开 API，无需登录无需 Key。

## 安装

```bash
# OpenClaw 用户直接安装
clawhub install freedompixels/cn-hot-trends

# 或手动复制到 skills 目录
cp -r cn-hot-trends ~/.qclaw/skills/
```
