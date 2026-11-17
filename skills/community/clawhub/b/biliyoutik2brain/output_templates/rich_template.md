# {{ title }}

> UP主: {{ uploader }} | 时长: {{ duration_min }}分钟 | 平台: {{ platform }}
> 处理时间: {{ processed_at }}

---

## 📝 内容摘要

{{ summary }}

## 📖 转录文本（带关键帧）

{% for section in sections %}
### {{ section.title }}

{{ section.text }}

{% if section.screenshot %}
![关键帧 {{ section.timestamp }}]({{ section.screenshot }})
{% if section.ocr_text %}
**OCR 提取**: {{ section.ocr_text }}
{% endif %}
{% if section.cross_validation %}
> 📊 交叉验证: {{ section.cross_validation }}
{% endif %}
{% endif %}

{% endfor %}

## 🏷️ 关键词

{{ keywords }}

## 📊 章节

{% for chapter in chapters %}
- {{ chapter.title }}
{% endfor %}

## 📷 关键帧决策

{{ keyframe_report }}

## 💬 评论分析

{% if comments_report %}
{{ comments_report }}
{% else %}
无评论数据
{% endif %}

## 💡 知识点

{% for knowledge in knowledge_items %}
- **{{ knowledge.title }}**: {{ knowledge.description }}
{% endfor %}
