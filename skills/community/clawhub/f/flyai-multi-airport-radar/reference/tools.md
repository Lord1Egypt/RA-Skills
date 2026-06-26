# 工具说明

## ask_user_question 工具

用于向用户提出选择题，快速收集信息。

**格式要求**：
- question: 清晰的问题文案
- header: 简短标签（≤12字符）
- options: 2-4个选项，每个包含 label 和 description

**示例**：
```json
{
  "questions": [{
    "question": "你从哪个城市出发？",
    "header": "出发城市",
    "options": [
      { "label": "上海", "description": "长三角出发" },
      { "label": "北京", "description": "华北出发" }
    ]
  }]
}
```

## FlyAI 核心能力

使用 `npx @anthropic-ai/flyai-cli@latest` 调用飞猪数据。

**常用命令**：
- `search flights`: 搜索航班
- `search hotels`: 搜索酒店
- `search attractions`: 搜索景点
- `search restaurants`: 搜索餐厅
