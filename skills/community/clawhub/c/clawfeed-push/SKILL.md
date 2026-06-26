---
name: clawfeed-push
description: |
  ClawFeed 新闻摘要飞书推送。定时抓取全球新闻（BBC · CNBC · Reuters · Al Jazeera）→ AI 生成中文摘要 → 推送至飞书。
  触发条件：(1) 用户要求推送新闻 (2) 测试推送 (3) 配置定时任务
---

# ClawFeed Push - 新闻摘要飞书推送

定时抓取全球新闻 → AI 生成中文摘要 → 推送至飞书对话。

## 功能

- 自动抓取 BBC World、Al Jazeera、CNBC、Reuters 等主流媒体 RSS
- 基于 MiniMax AI 生成中文新闻摘要
- 每日定时推送 50 条新闻到飞书
- 支持手动触发推送测试

## 配置

### 1. 飞书用户 ID

默认推送到当前飞书对话（`user:ou_30597b1b45c505faac65f11983d1276d`），如需修改目标，编辑 `scripts/push-feishu.py` 中的 `TARGET` 变量。

### 2. Crontab 定时推送

脚本已在 crontab 中注册：
```
30 8 * * 1-5  /home/goofy/.openclaw/workspace/scripts/clawfeed-daily.sh
```
每周一至周五 8:30 自动执行。

## 手动命令

```bash
# 生成当日摘要（不推送）
python3 ~/.openclaw/workspace/scripts/clawfeed-digest.py daily zh

# 仅推送最新摘要到飞书
python3 ~/.openclaw/workspace/scripts/clawfeed-push-feishu.py

# 生成 + 推送（完整流程）
bash ~/.openclaw/workspace/scripts/clawfeed-daily.sh
```

## 依赖

- Python 3
- `openclaw` CLI（已安装）
- ClawFeed 服务运行于 `localhost:8767`
- MiniMax API Key

## 新闻源

- BBC World News · Al Jazeera English · CNBC Top News · Reuters Business

共约 50-80 条原始新闻，AI 摘要后保留 50 条。
