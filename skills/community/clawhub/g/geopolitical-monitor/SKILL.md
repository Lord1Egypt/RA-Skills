
---
name: geopolitical-monitor
description: 地缘政治事件监控与分析工具 - 监控地缘政治相关新闻，分析对股票板块的影响，生成投资建议报告
metadata: {"clawdbot":{"emoji":"🌍","requires":{"bins":["python3","requests"]}}}
---

# 地缘政治监控与分析工具

监控地缘政治相关新闻，分析对股票板块的影响，生成投资建议报告。

## 核心特性

- 🌍 **地缘政治新闻监控**: 关注中东、伊朗、以色列、石油、制裁等关键词
- 📊 **板块影响分析**: 自动分析能源、黄金、军工、航运等板块的受影响程度
- 📈 **投资建议**: 生成板块排名和趋势预测
- 💾 **数据持久化**: 自动保存监控报告到 JSON 文件
- 🔧 **易扩展**: 支持接入真实 RSS 或新闻 API 源

## 快速开始

### 安装依赖

```bash
pip3 install requests
```

### 运行监控

```bash
cd /path/to/skill
python3 geopolitical_rss_monitor.py
```

## 配置说明

### 监控关键词

在脚本中编辑 `KEYWORDS` 列表：

```python
KEYWORDS = [
    "中东", "伊朗", "以色列", "巴勒斯坦", "石油", "制裁",
    "地缘政治", "冲突", "原油", "黄金", "避险",
    "霍尔木兹海峡", "红海", "波斯湾"
]
```

### 板块配置

在 `SECTORS` 字典中配置各板块的关键词、敏感度、方向和相关股票：

```python
SECTORS = {
    "能源": {
        "keywords": ["石油", "天然气", "原油", "能源", "油气", "OPEC", "霍尔木兹海峡"],
        "sensitivity": 0.9,
        "direction": "positive",
        "stocks": ["中国石油", "中国石化", "中海油", "潜能恒信", "海油工程"]
    },
    "黄金": {
        "keywords": ["黄金", "贵金属", "避险"],
        "sensitivity": 0.95,
        "direction": "positive",
        "stocks": ["紫金矿业", "山东黄金", "赤峰黄金", "湖南黄金"]
    },
    "军工": {
        "keywords": ["军工", "国防", "武器", "军事", "导弹", "伊朗", "以色列", "冲突"],
        "sensitivity": 0.85,
        "direction": "positive",
        "stocks": ["中航沈飞", "中航西飞", "中航光电", "航天电器", "海格通信"]
    },
    # ... 更多板块
}
```

## 数据目录

默认数据保存位置：

```
~/shared_memory/geopolitical/
```

可以在脚本中修改 `DATA_DIR` 变量来更改位置。

## 输出示例

监控运行后会生成：

1. **JSON 报告文件**: 包含新闻事件、板块分析、排名等完整信息
2. **控制台输出**: 实时显示监控进度和板块排名

```
🌍 地缘政治监控开始 - 2026-03-23 15:30:00
📊 获取到 10 条相关新闻（模拟数据）
🔍 分析板块影响...
📝 生成报告...
✅ 报告已保存: ~/shared_memory/geopolitical/2026-03-23_15.json

📈 板块排名:
   能源     - 9.5分 (3条新闻) [⬆️]
   黄金     - 9.0分 (2条新闻) [⬆️]
   军工     - 8.5分 (4条新闻) [⬆️]
   航运     - 7.0分 (2条新闻) [➖]
   消费     - 3.0分 (1条新闻) [⬇️]
   科技     - 2.0分 (1条新闻) [⬇️]
   金融     - 4.0分 (1条新闻) [➖]

📰 最新事件:
   • 伊朗最高领袖更换引发中东局势紧张... (新华社)
   • 美以继续打击伊朗石油设施... (路透社)
   • 霍尔木兹海峡航运风险上升... (彭博社)
   • 国际油价突破关键点位... (财联社)
   • 黄金价格创新高避险需求旺盛... (华尔街见闻)

🎉 监控完成！
```

## 扩展开发

### 接入真实数据源

替换 `MOCK_NEWS` 为真实的新闻数据获取逻辑：

```python
# 示例：从新浪财经 RSS 获取新闻
import feedparser

def fetch_real_news():
    url = "https://finance.sina.com.cn/roll/finance.d.xml"
    feed = feedparser.parse(url)
    news_items = []
    for entry in feed.entries[:20]:
        news_items.append({
            "title": entry.title,
            "source": "新浪财经",
            "timestamp": entry.published
        })
    return news_items
```

### 自定义分析逻辑

重写 `analyze_news()` 函数来实现自定义的板块影响分析：

```python
def analyze_news(news_items: List[Dict[str, Any]]) -&gt; Dict[str, Any]:
    """自定义分析逻辑"""
    # 实现你的分析算法
    pass
```

## 常见问题

### Q: 如何添加新的板块？
A: 在 `SECTORS` 字典中添加新的键值对即可。

### Q: 数据源返回错误怎么办？
A: 检查 RSS/API URL 是否正确，是否需要 headers 或认证，尝试在浏览器中访问确认。

### Q: 如何调整监控频率？
A: 使用 cron 或其他调度工具定期运行脚本。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

---

*由 Zbot 自动生成* 💥
