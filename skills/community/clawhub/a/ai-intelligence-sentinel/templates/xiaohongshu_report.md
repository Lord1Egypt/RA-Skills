# 🔥AI前沿情报站｜{{ date_str }}必看清单

姐妹们！今天的AI圈又炸了💥 一口气整理了{{ total_count }}条干货，建议先码再看⭐

---

## 💎 今日重磅（必看TOP5）

{% for item in top_picks[:5] %}
**{{ loop.index }}. {{ item.title }}**
{% if item.stars %}⭐{{ item.stars }}{% elif item.score %}🔥{{ item.score }}分{% endif %}

{{ (item.summary or item.description or "这个真的绝绝子！")[:80] }}

{% endfor %}

---

## 📚 论文党的福音（arXiv精选）

{% if important_papers %}
{% for paper in important_papers[:3] %}
📄 **{{ paper.title[:40] }}...**

{% if paper.abstract %}💡一句话：{{ paper.abstract[:60] }}...{% endif %}
🏷️ {{ paper.primary_category or "AI" }}｜{{ paper.published[:10] if paper.published else "最新" }}

{% endfor %}
{% else %}
今天论文区比较安静，明天蹲一波大的👀
{% endif %}

---

## 💻 开源真香现场（GitHub）

{% if trending_projects %}
{% for project in trending_projects[:3] %}
🔧 **{{ project.title }}**

{{ project.description[:50] if project.description else "宝藏项目！" }}...
⭐{{ project.stars|default(0) }} Stars｜{{ project.language or "多语言" }}

{% endfor %}
{% else %}
今天GitHub有点冷，但明天说不准就有爆款了✨
{% endif %}

---

## 📰 业内动态（不容错过）

{% for source, items in blog_sources.items() %}
### {{ source }}（{{ items|length }}条）
{% for item in items[:2] %}
• {{ item.title[:35] }}...
{% endfor %}

{% endfor %}

---

## 🔥 热门话题（MMChat精选）

{% for topic in mmchat_topics[:5] %}
{{ loop.index }}️⃣ {{ topic }}
{% endfor %}

---

## 📊 今日数据

| 类型 | 数量 |
|------|------|
| 📄 论文 | {{ arxiv_count }} 篇 |
| 💻 项目 | {{ github_count }} 个 |
| 📰 资讯 | {{ blog_count }} 条 |
| 🔥 热点 | {{ mmchat_count }} 个 |

---

💬 **今日份AI情报已送达！觉得有用就点个收藏吧～**
🔖 明天{{ report_time }}准时更新，记得蹲！

#AI #人工智能 #科技资讯 #每日打卡 #干货分享
