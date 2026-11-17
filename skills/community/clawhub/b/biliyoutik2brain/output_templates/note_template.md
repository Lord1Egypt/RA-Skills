# {{ title }}

> UP主: {{ uploader }} | 时长: {{ duration_min }}分钟 | 领域: {{ domain }}
> 处理时间: {{ processed_at }}

---

## 📝 内容摘要

{{ summary }}

## 📖 转录文本

{{ transcript }}

## 🏷️ 关键词

{{ keywords }}

## 📊 章节

{% for chapter in chapters %}
- {{ chapter.title }}
{% endfor %}

## 💡 知识点

{% for knowledge in knowledge_items %}
- **{{ knowledge.title }}**: {{ knowledge.description }}
{% endfor %}
