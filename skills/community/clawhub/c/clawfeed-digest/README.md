# ClawFeed Digest Fetcher

> 抓取 ClawFeed AI 新闻简报，写入 Obsidian 知识库

## 功能

- 抓取 ClawFeed 简报（4h/日报/周报）
- 自动写入 Obsidian 指定目录
- 支持命令行参数灵活配置

---

## 文档

- [快速开始](./docs/README.md) — 导航和快速开始
- [Fast Note Sync Service](./docs/fast-note-sync-service.md) — Obsidian 与 OpenClaw 同步配置
- [Obsidian Sync](./docs/obsidian-sync.md) — ClawHub Skill 使用
- [定时任务](./docs/cron-jobs.md) — 定时任务配置

---

## 安装

```bash
# 克隆仓库
git clone https://github.com/adminlove520/clawfeed-digest.git
cd clawfeed-digest

# 安装依赖
pip install requests
```

---

## 使用方法

```bash
# 获取今日日报
python scripts/fetch_clawfeed.py

# 获取 4h 简报
python scripts/fetch_clawfeed.py -t 4h

# 获取周报
python scripts/fetch_clawfeed.py -t weekly
```

---

## 数据来源

- [ClawFeed](https://clawfeed.kevinhe.io/) - AI 新闻简报聚合

---

## 相关链接

- **Fast Note Sync Service**: https://github.com/haierkeys/fast-note-sync-service
- **Obsidian Sync (ClawHub)**: https://clawhub.ai/AndyBold/obsidian-sync

---

**Author**: 小溪 (adminlove520)  
**Version**: 1.0.1
