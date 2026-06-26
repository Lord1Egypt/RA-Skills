# 工具说明

## ask_user_question 工具

用于收集用户信息的交互式提问工具。当用户需求模糊时，使用此工具引导用户完善需求。

### 调用格式

```json
{
  "questions": [
    {
      "question": "问题内容？",
      "header": "短标签（最多12字符）",
      "options": [
        { "label": "选项1", "description": "选项说明" },
        { "label": "选项2", "description": "选项说明" }
      ],
      "multiSelect": false
    }
  ]
}
```

### 注意事项

- 每次最多问 4 个问题
- 系统自动添加"其他"选项供用户自由输入
- 用趣味化、生活化的语言提问，降低用户思考成本
- 善用 emoji 让选项更生动

### 示例：旅行风格追问

```json
{
  "questions": [
    {
      "question": "先帮你划定方向，你更想：",
      "header": "旅行风格",
      "options": [
        { "label": "🏖️ 海边吹风", "description": "沙滩、海浪、日落" },
        { "label": "🏔️ 山里避暑", "description": "清凉、徒步、自然" },
        { "label": "🏙️ 城市探索", "description": "美食、购物、文化" },
        { "label": "🎯 都可以", "description": "帮我推荐" }
      ]
    }
  ]
}
```

---

## fetch_content 工具

获取网页实时信息，用于补充 FlyAI 搜不到的内容。

### 调用格式

```
fetch_content(url, query)
```

### 参数说明

| 参数 | 说明 |
|------|------|
| url | 目标网页 URL |
| query | 要从网页提取的信息描述 |

### 使用场景

| 场景 | 示例 |
|------|------|
| 查询最新旅行政策 | `fetch_content("https://...", "入境政策")` |
| 获取小众目的地信息 | 补充 keyword-search 不够精准的结果 |
| 确认景点开放时间 | 官网实时信息 |
| 补充攻略信息 | 游记、攻略类内容 |

### 注意事项

- 优先使用 FlyAI 命令，fetch_content 作为补充
- 注意网页可能有反爬限制
- 提取信息后需二次整理，确保输出格式一致
