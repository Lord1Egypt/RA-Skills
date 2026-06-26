# 🌅 AI前沿哨兵 - {{ date_str }}晨报

> **今日摘要**：{{ daily_summary }}

---

## ⭐ 编辑精选（Top 5）

{% for item in top_picks[:5] %}
### {{ loop.index }}. [{{ item.title }}]({{ item.url or item.hn_url or item.pdf_url or "#" }})

**一句话摘要**：{{ (item.summary or item.description or item.abstract or item.text or "暂无摘要")[:150] if (item.summary or item.description or item.abstract or item.text) else "暂无摘要" }}

**为什么重要**：
{% if item.stars %}- ⭐ 高热度开源项目（{{ item.stars }} stars）
{% elif item.score %}- 🔥 社区热议（{{ item.score }} 分）
{% else %}- 📚 重要学术贡献
{% endif %}

---

{% endfor %}

## 📚 学术前沿（arXiv）

{% if important_papers %}
{% for paper in important_papers[:2] %}
### [{{ paper.title }}]({{ paper.url }})

📝 **一句话描述**：{{ paper.title.split(":")[-1].strip() if ":" in paper.title else paper.abstract[:120] if paper.abstract else "重要AI研究论文" }}

| 信息 | 内容 |
|------|------|
| 👥 作者 | {{ paper.author_str or paper.authors[0] if paper.authors and paper.authors is iterable else "未知" }} |
| 🏷️ 分类 | {{ paper.primary_category or "Unknown" }} |
| 📅 发布 | {{ paper.published[:10] if paper.published else "未知" }} |

{% if paper.abstract %}
**摘要**：{{ paper.abstract[:250] }}...
{% endif %}

🔗 [阅读论文]({{ paper.url }})

---

{% endfor %}
{% else %}
暂无新论文
{% endif %}

## ⚡ 热门开源项目（GitHub）

{% if trending_projects %}
{% for project in trending_projects[:5] %}
### [{{ project.title }}]({{ project.url }})

{{ project.description[:150] if project.description and project.description != "无描述" else "热门AI开源项目" }}

| 指标 | 数值 |
|------|------|
| ⭐ Stars | {{ project.stars|default(0)|int|commalist }} |
| 🍴 Forks | {{ project.forks|default(0)|int|commalist }} |
| 🐙 语言 | {{ project.language or "Unknown" }} |
| 👤 作者 | [{{ project.author or "Unknown" }}]({{ project.author_url or "#" }}) |

---

{% endfor %}
{% else %}
暂无热门项目
{% endif %}

## 💬 社区热议（HackerNews）

{% if discussions %}
{% for item in discussions[:5] %}
### [{{ item.title }}]({{ item.hn_url or item.url or "#" }})

{{ item.text[:120] if item.text else (item.description[:120] if item.description else "社区热门讨论") }}...

| 信息 | 内容 |
|------|------|
| ⬆️ 得分 | {{ item.score|default(0) }} |
| 💬 评论 | {{ item.comments|default(0) }} |
| 👤 作者 | {{ item.author or "Unknown" }} |
| 🕐 时间 | {{ item.time or item.published or "未知" }} |

---

{% endfor %}
{% else %}
暂无社区讨论
{% endif %}

## 📰 行业动态（AI博客）

{% if news %}
{% for item in news[:5] %}
### [{{ item.title }}]({{ item.url or "#" }})

**来源**：{{ item.source or "AI博客" }} · {{ item.published or "未知" }}

{{ (item.summary or item.description or "行业动态")[:150] }}...

{% if item.categories %}
🏷️ 标签：{{ item.categories|join(', ') }}
{% endif %}

---

{% endfor %}
{% else %}
暂无新闻更新
{% endif %}

{% if tweets %}
## 🐦 大咖动态（Twitter）

{% for tweet in tweets[:3] %}
### [{{ tweet.author_name or tweet.author_username }}](https://twitter.com/{{ tweet.author_username }})

{{ tweet.text[:200] }}

| 指标 | 数值 |
|------|------|
| ❤️ 点赞 | {{ tweet.likes|default(0) }} |
| 🔁 转发 | {{ tweet.retweets|default(0) }} |
| 🔗 [查看原推]({{ tweet.url }}) |

---

{% endfor %}
{% endif %}

## 📊 今日数据

| 类型 | 数量 |
|------|------|
| 学术论文 | {{ summary.papers_count }} 篇 |
| 开源项目 | {{ summary.projects_count }} 个 |
| 社区讨论 | {{ summary.discussions_count }} 条 |
| 新闻动态 | {{ summary.news_count }} 条 |
| 社交动态 | {{ summary.tweets_count }} 条 |

### 🔥 今日热词

{% if hot_topics %}
{% for topic in hot_topics %}#{{ topic }} {% endfor %}
{% else %}
暂无热词分析
{% endif %}

---

## 💡 推荐阅读

- 🔍 持续关注 GitHub Trending 新上榜项目
- 📚 定期查看 arXiv 新提交的论文
- 💬 HackerNews 上的技术讨论往往预示趋势

---

{{ quality_card }}

---

**报告生成时间**：{{ date_str }} {{ time_str }}
**数据来源**：GitHub, arXiv, HackerNews, AI Blogs, Twitter
**由 AI前沿哨兵 自动生成**
