---
name: "文本问数"
description: "将自然语言问题转化为 SQL 查询并执行，支持多轮对话、意图识别、SQL 审计、可视化推荐等全流程。"
---

# chat_ai（文本问数）

## 功能
将自然语言问题转化为 SQL 查询并执行，支持多轮对话、意图识别、SQL 审计、可视化推荐等全流程。

## 触发方式
- “查一下上个月销售额最高的5个产品”
- “对比华东和华北的GMV”
- “用 text2sql 帮我分析用户留存”

## 输入参数
- `query`: 用户自然语言问题（必填）

## 输出格式
```json
{
  "status": "success|error",
  "sql": "SELECT ...",
  "result": [{...}],  // 表格数据
  "summary": "简要结论",
  "regions": ["recognize_intent", "sql_generator", ...]
}