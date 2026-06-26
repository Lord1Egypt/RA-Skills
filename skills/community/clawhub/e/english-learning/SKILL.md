---
name: 英语听力训练
description: 提供小学、专四、专八英语听力材料，支持获取材料列表和详细段落。
version: 1.0.0
author: 你的名字
env:
  - SUPABASE_URL
  - SUPABASE_ANON_KEY
---

# 英语听力训练助手

当用户需要听力训练时，按以下步骤操作。

## 1. 获取训练类别
目前支持三种类别：
- 小学 → 代码 `primary`
- 专四 → 代码 `tem4`
- 专八 → 代码 `tem8`

用户可以说：“小学英语听力”、“专四材料”、“给我专八练习”等。

## 2. 根据类别获取材料列表

调用 API（将 `{category}` 替换为对应代码）：

```http
GET ${SUPABASE_URL}/rest/v1/listening_materials?is_active=eq.true&training_category=eq.{category}&select=id,title,description,difficulty,audio_url,duration,listening_text_segments(id,text_content,start_time,end_time,sequence_order,audio_url)

请求头：
apikey: ${SUPABASE_ANON_KEY}
Authorization: Bearer ${SUPABASE_ANON_KEY}

展示材料列表
将返回的结果格式化为清晰列表，例如：
📚 【小学英语听力材料】
1. 我的学校 (难度：初级)
2. 春天的故事 (难度：中级)
...
请回复序号选择材料，或直接说出材料名称。

展示具体材料内容
当用户选择材料后，从之前获取的数据中提取 listening_text_segments，按 sequence_order 顺序展示每个段落。如果材料有总音频链接，也可以提供播放链接。

安装说明
在 OpenClaw 中设置以下环境变量（必须）：

SUPABASE_URL：你的项目 API 地址
示例：https://fhpyglovinmpqsnhqqay.supabase.co

SUPABASE_ANON_KEY：你的 anon key
示例：eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZocHlnbG92aW5tcHFzbmhxcWF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjczODE1OTIsImV4cCI6MjA4Mjk1NzU5Mn0.q7go9R7Kcc-J4xobxmvQ_OQe6PfZ5VtKOzEdqQpPnYU