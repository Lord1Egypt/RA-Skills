---
title: "{{ title }}"
uploader: "{{ uploader }}"
platform: "{{ platform }}"
video_id: "{{ video_id }}"
duration: {{ duration_min }}
domain: "{{ domain }}"
tags: [biliyoutik2brain, {{ domain | lower }}, {{ tags | join(', ') }}]
created: "{{ processed_at }}"
url: "{{ url }}"
---

# {{ title }}

> [!info] 视频信息
> - **UP主**: {{ uploader }}
> - **时长**: {{ duration_min }}分钟
> - **平台**: {{ platform }}
> - **领域**: {{ domain }}
> - **处理时间**: {{ processed_at }}

## 📝 摘要

{{ summary }}

## 📖 转录笔记

{{ transcript }}

## 🏷️ 关键词

#{{ keywords }}

## 📊 章节

{% for chapter in chapters %}
### {{ chapter.title }}
{{ chapter.summary }}
{% endfor %}

## 🔗 相关知识

{% for knowledge in knowledge_items %}
- [[{{ knowledge.title }}]]: {{ knowledge.description }}
{% endfor %}

## 💬 评论洞察

{% if comments_report %}
{{ comments_report }}
{% endif %}
