---
name: daily-report
description: "Daily report generation with timeliness verification for news and content freshness checking."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl", "python3"] },
        "install": [],
      },
  }
---

# Daily Report Skill

Daily report generation with timeliness verification for news and content freshness checking.

## Features

- **Timeliness Verification**: Verify news and content freshness
- **Date Standardization**: Use explicit dates, not relative time
- **Quality Scoring**: Freshness, accuracy, relevance scoring
- **Multi-source Validation**: Cross-reference multiple sources
- **Report Templates**: Structured report formats

## Usage

This skill provides daily report generation with built-in timeliness verification. Perfect for:

- AI科技晨报/晚报
- 高校AIGC日报
- 科技日报
- 任何需要时效性验证的日报内容

## Timeliness Rules

### 1. Date Standardization
```markdown
## Standard Format
- Use explicit dates: "2026-05-30" not "1 hour ago"
- Categorize by freshness:
  - 📅 Today's News (发布日期 = 当天)
  - 📅 Yesterday's News (发布日期 = 前一天)
  - 📅 Recent News (发布日期在3天内)
```

### 2. Verification Process
```python
def verify_timeliness(news_item):
    """
    Verify news timeliness
    """
    # 1. Check publication date
    pub_date = news_item.get('publication_date')
    
    # 2. Cross-reference multiple sources
    sources = news_item.get('sources', [])
    if len(sources) < 2:
        return "Insufficient sources"
    
    # 3. Check for relative time expressions
    content = news_item.get('content', '')
    if any(phrase in content for phrase in ['1小时前', '2小时前', '刚刚']):
        return "Contains relative time expressions"
    
    # 4. Verify date accuracy
    today = datetime.now().strftime('%Y-%m-%d')
    if pub_date == today:
        return "Today's news"
    elif pub_date == (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'):
        return "Yesterday's news"
    else:
        return f"News from {pub_date}"
```

### 3. Quality Metrics
- **Freshness Score**: How recent is the news? (0-10)
- **Accuracy Score**: Multiple sources confirmed? (0-10)
- **Relevance Score**: Is it relevant to the audience? (0-10)
- **Overall Score**: Average of above scores

## Report Structure

### 1. Header
```markdown
# 🌙 AI科技晚报 (2026-05-30)

**时效性验证**: ✅ 所有新闻均为当日或昨日发布
**质量评分**: 8.5/10 (新鲜度: 9, 准确性: 8, 相关性: 8)
```

### 2. News Sections
```markdown
## 📅 今日新闻（5月30日）
1. **苹果AI图像压缩技术** 
   - 发布时间: 2026-05-30 10:30
   - 来源: 新浪财经、虎嗅网、36氪
   - 链接: https://finance.sina.com.cn/roll/2026-05-30/doc-inhzrvnr8889579.shtml

## 📅 昨日新闻（5月29日）
2. **Claude Opus 4.8发布**
   - 发布时间: 2026-05-29 09:00
   - 来源: Anthropic官方、腾讯新闻、知乎
   - 链接: https://www.anthropic.com/news/claude-opus-4-8

## 📅 近期重要新闻（5月26-28日）
3. **DeepSeek V4多模态模型预告**
   - 发布时间: 2026-05-26 15:00
   - 来源: 腾讯新闻
   - 链接: https://news.qq.com/rain/a/20260526A05JEB00
```

### 3. Verification Summary
```markdown
## 🔍 时效性验证报告
- ✅ 今日新闻: 1条
- ✅ 昨日新闻: 1条  
- ✅ 近期新闻: 1条
- ❌ 过期新闻: 0条
- ⚠️ 需验证: 0条

**验证方法**: 
1. 检查新闻发布日期
2. 交叉验证多个来源
3. 避免相对时间表述
4. 使用可靠新闻源
```

## Best Practices

1. **Always verify publication dates** - Check multiple sources
2. **Use explicit dates** - Avoid "1 hour ago" etc.
3. **Cross-reference sources** - Minimum 2 reliable sources
4. **Categorize by freshness** - Today, Yesterday, Recent
5. **Include verification report** - Show timeliness verification results
6. **Use reliable sources** - Official announcements, reputable media

## News Sources

### Reliable Sources
- **官方发布**: 公司官网、官方博客
- **权威媒体**: 新浪财经、腾讯新闻、知乎专栏
- **科技媒体**: 36氪、虎嗅网、机器之心
- **国际媒体**: Anthropic官方、OpenAI官方

### Verification Checklist
- [ ] 发布日期是否明确？
- [ ] 是否有多个来源确认？
- [ ] 是否包含相对时间表述？
- [ ] 来源是否可靠？
- [ ] 内容是否过时？

## Integration

### Cron Job Example
```json
{
  "name": "AI科技晚报",
  "schedule": {"kind": "cron", "expr": "0 20 * * *", "tz": "Asia/Shanghai"},
  "payload": {
    "kind": "agentTurn",
    "message": "生成今日AI科技晚报，要求：1. 所有新闻必须有明确发布日期 2. 避免相对时间表述 3. 交叉验证多个来源 4. 包含时效性验证报告"
  }
}
```

## License

MIT License - Feel free to modify and distribute.