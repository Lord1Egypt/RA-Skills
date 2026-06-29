---
name: douyin-comment-manager
description: 抖音创作者中心评论管理助手。通过 Playwright 浏览器自动化抓取评论并批量回复，支持智能模板匹配和交互式可视化报告。
version: "1.0.0"
author: WorkBuddy
agent_created: true
tags: [douyin, comment-management, automation, playwright, creator-center]
triggers:
  - 抖音评论
  - 评论管理
  - 批量回复
  - 评论抓取
  - 抖音创作者
  - 评论自动回复
  - douyin comment
  - 粉丝互动管理
---

# 抖音评论管理助手 (Douyin Comment Manager)

> 基于 Playwright 浏览器自动化的抖音创作者中心评论管理 Skill。
> 抓取评论 → 智能批量回复 → 可视化报告，一站式管理。

## 适用场景

- 创作者日常管理粉丝评论，减少重复劳动
- MCN 机构统一管理多账号评论互动
- 电商带货号批量回复商品咨询
- 运营人员进行评论数据分析与舆情监控

## 核心能力

| 阶段 | 命令 | 功能 |
|------|------|------|
| 1. 登录 | `auth` | 扫码登录，持久化保存会话 |
| 2. 作品列表 | `works` | 拉取所有作品列表 |
| 3. 抓取评论 | `fetch` | 按作品抓取未回复评论，支持多维度过滤 |
| 4. 批量回复 | `reply` | 按模板策略批量回复评论 |
| 5. 可视化报告 | `report` | 生成交互式 HTML 分析报告 |

## 快速开始

### 环境要求

- Python 3.11+
- Node.js (Playwright 依赖)
- Chromium 浏览器

### 安装

```bash
# 确保在 WorkBuddy managed Python 环境中
pip install playwright
python -m playwright install chromium
```

### 初始化（用户本人扫码）

```bash
python scripts/auth.py
```

扫描弹出的二维码完成登录，会话将被持久化保存。

### 完整工作流

```bash
# 1. 获取作品列表
python scripts/fetch_comments.py --works

# 2. 抓取指定视频的未回复评论
python scripts/fetch_comments.py --video-title "我的视频标题"

# 3. 抓取所有视频的未回复评论
python scripts/fetch_comments.py --all

# 4. 预览回复计划（dry-run，不实际执行）
python scripts/batch_reply.py --input output/unreplied_comments.json --dry-run

# 5. 执行批量回复
python scripts/batch_reply.py --input output/unreplied_comments.json

# 6. 生成可视化报告
python scripts/report.py
```

## 详细用法

### `fetch_comments.py` — 评论抓取

```
参数：
  --works              获取作品列表
  --video-title TEXT   指定作品标题（模糊匹配）
  --video-id TEXT      指定作品 ID
  --all                拉取所有作品的未回复评论
  --max-per-video N    每个视频最多抓取评论数（默认 500）
  --output PATH        输出 JSON 路径（默认 output/unreplied_comments.json）
  --include-replied    同时输出已回复评论
  --filter-keyword KW  只抓取包含指定关键词的评论
  --sort-by {time,likes}  排序方式（默认时间倒序）

输出 JSON 结构：
[
  {
    "comment_id": "xxx",
    "video_id": "xxx",
    "video_title": "xxx",
    "author_name": "xxx",
    "author_id": "xxx",
    "content": "评论内容",
    "like_count": 10,
    "reply_count": 0,
    "create_time": "2026-06-21T12:00:00",
    "is_replied": false,
    "pinned": false,
    "images": []
  }
]
```

### `batch_reply.py` — 批量回复

```
参数：
  --input PATH         未回复评论 JSON（必填）
  --strategy {template,ai,random}  回复策略（默认 template）
  --template-file PATH 自定义回复模板 JSON
  --ai-system-prompt TEXT  AI 回复的系统提示词
  --delay N            每条回复间隔秒数（默认 3-5 随机）
  --max-replies N      最大回复条数
  --skip-keyword KW    跳过包含此关键词的评论
  --dry-run            预览模式，不实际执行回复
  --output PATH        回复结果 JSON 路径

回复模板 JSON 格式：
{
  "templates": [
    {
      "keywords": ["谢谢", "感谢", "支持"],
      "reply": "感谢支持！我会继续努力创作 💪"
    },
    {
      "keywords": ["问题", "怎么", "请问"],
      "reply": "可以私信我详细沟通哦～"
    },
    {
      "keywords": ["多少钱", "价格", "怎么卖"],
      "reply": "点击主页链接了解更多详情～"
    }
  ],
  "default_reply": "感谢你的评论！❤️"
}
```

### `report.py` — 可视化报告

```
参数：
  --input PATH         回复结果 JSON
  --output PATH        报告 HTML 路径（默认 output/report.html）
  --date-range START END  日期范围过滤

生成交互式 HTML 报告，包含：
- 评论总览仪表盘
- 回复率/互动率趋势图
- 评论情感分析（正面/中性/负面）
- 高频关键词词云
- 时段分析热力图
- TOP 评论/粉丝排行
```

## 硬约束与安全规则

1. **不绕过登录验证码** — 登录必须由用户本人扫码
2. **不复用他人登录态** — `.playwright/douyin-profile/` 目录为个人私有
3. **内容合规** — 不生成引流链接、联系方式、敏感词等违规内容
4. **频率控制** — 内置随机延迟，模拟真实操作节奏
5. **风控响应** — 遇到验证码/风控页面立即停止，通知用户人工处理
6. **页面容错** — DOM 选择器变化时报错退出，不尝试"暴力修复"

## 架构说明

```
douyin-comment-manager/
├── SKILL.md              # 本文件
├── scripts/
│   ├── auth.py           # 扫码登录与会话管理
│   ├── fetch_comments.py # 评论抓取引擎
│   ├── batch_reply.py    # 批量回复引擎
│   ├── report.py         # HTML 报告生成器
│   └── config.py         # 配置管理
├── references/
│   └── douyin-api.md     # 抖音开放平台 API 参考
├── output/               # 数据输出目录
│   ├── works.json
│   ├── unreplied_comments.json
│   ├── reply_results.json
│   └── report.html
└── .playwright/
    └── douyin-profile/   # 持久化登录态（gitignore）
```

## 常见问题

**Q: 遇到"需要重新登录"提示？**
A: 登录态过期，运行 `python scripts/auth.py` 重新扫码。

**Q: 回复失败/popup 提示异常？**
A: 抖音页面结构可能更新，先人工登录创作者中心确认页面正常，再重试。

**Q: 能不能自动识别负面评论优先回复？**
A: 支持！使用 `--sort-by likes` 优先回复高赞评论，结合 `--filter-keyword` 过滤负面关键词。

**Q: 支持多账号管理吗？**
A: 当前版本单账号。多账号可复制本 skill 到不同目录，各自维护独立的 `.playwright/` 登录态。

---

_Version: 1.0.0 | Last updated: 2026-06-21_
