# Daily Game News - 使用说明

## 📋 功能

每日自动抓取游戏资讯并生成报告，包含以下 **9 个网站**：

### 国内媒体（优先级 1）
1. **机核 GCORES** - 2 篇/天
2. **游民星空** - 2 篇/天
3. **游戏陀螺** - 2 篇/天
4. **触乐** - 2 篇/天
5. **游研社** - 2 篇/天
6. **GameLook** - 2 篇/天

### 国际媒体（优先级 1）
7. **IGN** - 4 篇/天
8. **GameSpot** - 4 篇/天
9. **GameDeveloper** - 2 篇/天

**预计每日抓取总量**: 22 篇文章

---

## 🏷️ 自动分类（7 大类）

每篇文章自动分类到以下大类：

| 分类 | Emoji | 关键词示例 |
|------|-------|-----------|
| 🔥 头条要闻 | 🔥 | breaking, major, 重磅，独家，现象级 |
| 🎮 新品动态 | 🎮 | 发售，上线，更新，DLC, release, launch |
| 🏢 厂商动态 | 🏢 | 公司，战略，裁员，人事，layoff, strategy |
| 📊 行业数据 | 📊 | 财报，数据，销量，report, sales, revenue |
| ⭐ 值得关注 | ⭐ | 独立，小众，创意，indie, creative |
| 💰 投融资 | 💰 | 融资，投资，收购，上市，acquisition, IPO |
| 📁 其他 | 📁 | 无法归类的内容 |

---

## ⏰ 定时任务

**执行时间**: 每天北京时间 **10:00**  
**推送方式**: 飞书私信  
**存档方式**: Word 文档本地存储

---

## 📁 报告存储位置

Word 文档存储在：
```
/home/admin/.openclaw/workspace/reports/daily-game-news/daily-game-news-YYYY-MM-DD.docx
```

---

## 🔍 获取 Word 报告的指令

### 方式 1：直接读取文件（推荐）
```bash
# 获取今日报告
read /home/admin/.openclaw/workspace/reports/daily-game-news/daily-game-news-2026-03-07.docx

# 获取指定日期报告
read /home/admin/.openclaw/workspace/reports/daily-game-news/daily-game-news-2026-03-06.docx
```

### 方式 2：列出所有历史报告
```bash
# 查看所有报告
ls -la /home/admin/.openclaw/workspace/reports/daily-game-news/

# 查看最近 5 个报告
ls -lt /home/admin/.openclaw/workspace/reports/daily-game-news/ | head -6
```

### 方式 3：通过对话获取
直接对我说以下任意指令：
- "获取今日游戏资讯报告"
- "获取 2026-03-07 游戏资讯报告"
- "查看昨天的游戏资讯报告"
- "列出所有历史游戏资讯报告"

---

## 🛠️ 手动触发

```bash
# 手动执行抓取
uv run /home/admin/.openclaw/workspace/skills/daily-game-news/scripts/crawler.py
```

---

## 📊 报告格式

### 飞书消息格式
```markdown
# 📰 每日游戏资讯报告

**报告日期**: 2026-03-07
**数据来源**: 机核 GCORES、游民星空、游戏陀螺、触乐、游研社、GameLook、IGN、GameSpot、GameDeveloper

## 🔥 头条要闻
| 发布源 | 时间 | 文章标题 | 链接 |
|--------|------|----------|------|
| IGN | Mar 6, 2026 | Xbox Confirms... | [查看详情](url) |
| 游民星空 | Mar 6, 2026 | ... | [查看详情](url) |

## 🎮 新品动态
...
```

### Word 文档格式
- **标题**: 每日游戏资讯报告
- **元信息**: 日期、时间、数据来源
- **分类内容**: 按 7 大分类列出所有文章
- **每篇文章包含**:
  - 序号
  - 标题（加粗）
  - 发布源
  - 时间
  - 链接（可点击）
  - 摘要（可选）

---

## ⚙️ 配置文件

配置文件位置：
```
/home/admin/.openclaw/workspace/configs/news-crawler-config.json
```

### 可配置项

```json
{
  "网站配置": [
    {
      "id": "网站 ID",
      "name": "网站名称",
      "base_url": "https://...",
      "抓取优先级": 1,  // 1=抓取，2=跳过
      "分区": [
        {
          "筛选数量": 2,  // 每站抓取文章数
          "时间范围": "24h"
        }
      ]
    }
  ],
  "定时任务": {
    "时间": ["10:00"]  // 执行时间
  }
}
```

---

## 📝 日志

日志文件位置：
```
/home/admin/.openclaw/workspace/logs/daily-game-news.log
```

查看日志：
```bash
# 查看最新日志
tail -f /home/admin/.openclaw/workspace/logs/daily-game-news.log

# 查看今日日志
cat /home/admin/.openclaw/workspace/logs/daily-game-news.log | grep "2026-03-07"
```

---

## 🆘 常见问题

### Q: 如何修改抓取时间？
A: 编辑配置文件中的定时任务部分，然后重新配置 cron：
```bash
crontab /home/admin/.openclaw/workspace/skills/daily-game-news/crontab.txt
```

### Q: 如何添加/删除网站？
A: 编辑 `news-crawler-config.json`，在"网站配置"数组中添加或删除网站配置。

### Q: 如何修改每个网站的抓取数量？
A: 在配置文件中找到对应网站的"分区"配置，修改"筛选数量"字段。

### Q: 报告没有按时发送？
A: 检查以下步骤：
1. cron 任务是否正常运行：`crontab -l`
2. 日志文件是否有错误：`tail logs/daily-game-news.log`
3. Python 环境是否正常：`uv run --version`
4. 网络连接是否正常

### Q: 如何获取昨天的报告？
A: 
```bash
# 方法 1：直接读取
read /home/admin/.openclaw/workspace/reports/daily-game-news/daily-game-news-2026-03-06.docx

# 方法 2：列出所有报告
ls /home/admin/.openclaw/workspace/reports/daily-game-news/

# 方法 3：对我说
"获取昨天的游戏资讯报告"
```

### Q: Word 文档打不开？
A: 检查文件是否存在：
```bash
ls -lh /home/admin/.openclaw/workspace/reports/daily-game-news/
```

---

## 📈 统计信息

查看抓取统计：
```bash
# 查看本月报告数量
ls /home/admin/.openclaw/workspace/reports/daily-game-news/ | wc -l

# 查看最新报告大小
ls -lh /home/admin/.openclaw/workspace/reports/daily-game-news/ | tail -1
```

---

## 🔧 依赖

本 Skill 依赖以下工具和库：
- Python 3.8+
- uv (Python 包管理器)
- python-docx (Word 文档生成)
- SearXNG (搜索 API)

安装依赖：
```bash
cd /home/admin/.openclaw/workspace/skills/daily-game-news
pip install python-docx
```
