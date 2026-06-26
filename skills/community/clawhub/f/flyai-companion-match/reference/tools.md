# ask_user_question 工具说明

本技能使用 `ask_user_question` 工具进行交互式信息收集。

## 核心特性

- **选项式问答**：给用户提供预设选项，降低输入成本
- **灵活输入**：用户始终可以选择"其他"来自由输入
- **分步收集**：将复杂信息拆分为多个简单问题
- **批量提问**：一次最多可提问 1-4 个问题


## 调用示例

```json
{
  "questions": [
    {
      "question": "这次旅行和谁一起？",
      "header": "同行人",
      "options": [
        {"label": "带小孩", "description": "有儿童/幼儿同行"},
        {"label": "带老人", "description": "有长辈同行"},
        {"label": "一家三代", "description": "老人+小孩都有"},
        {"label": "闺蜜/朋友同行", "description": "成年人组队"}
      ]
    },
    {
      "question": "计划玩几天？",
      "header": "天数",
      "options": [
        {"label": "2-3天", "description": "周末短途"},
        {"label": "4-5天", "description": "小长假"},
        {"label": "6天以上", "description": "深度游"}
      ]
    }
  ]
}
```
