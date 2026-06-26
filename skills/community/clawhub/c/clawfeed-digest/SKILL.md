# ClawFeed Digest Fetcher

> 抓取 ClawFeed AI 新闻简报，写入 Obsidian 知识库

## 功能

- 抓取 ClawFeed 简报（4h/日报/周报）
- 自动写入 Obsidian 指定目录

## 使用方法

```bash
# 安装依赖
pip install requests

# 获取今日日报
python scripts/fetch_clawfeed.py

# 获取 4h 简报
python scripts/fetch_clawfeed.py -t 4h
```

## 参数

- `--type`, `-t`: 简报类型 (4h, daily, weekly)
- `--limit`, `-l`: 获取数量
- `--output`, `-out`: 输出目录

## 数据来源

- [ClawFeed](https://clawfeed.kevinhe.io/)

## OpenClaw 定时任务

```json
{
  "name": "每日 AI 新闻简报",
  "schedule": "0 17 * * *",
  "payload": {
    "message": "运行 python ~/.openclaw/skills/clawfeed-digest/scripts/fetch_clawfeed.py"
  }
}
```
