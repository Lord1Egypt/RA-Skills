---
name: custom-api-summary
version: 2.0.0
description: "调用自定义摘要 API，对用户提供的文本进行处理并返回结果"
tags: ["API", "总结", "摘要", "文本处理"]
tools: ["Bash"]
---

# Custom API Summary Skill

## 功能
当用户明确要求对一段文本进行总结、提炼、归纳或处理时，调用 HTTP 接口，将用户输入作为 `content` 参数传入，并返回接口处理结果。

## 适用场景
- 总结一段较长文本
- 提炼文章重点
- 对输入内容做统一的摘要处理

## 触发条件
当用户表达以下意图时触发：
- "帮我总结这段内容"
- "提炼一下这段文字"
- "把这段话做个摘要"

不应在普通闲聊、无明确文本处理需求时自动触发。

## 输入
用户提供的原始文本内容。

## 执行脚本

```bash
# API 接口地址
API_URL="https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call"

# 用户输入的内容（自动获取）
USER_TEXT="$1"

# 检查输入是否为空
if [ -z "$USER_TEXT" ]; then
  echo "❌ 错误：请输入需要总结的文本内容"
  echo "用法：帮我总结这段内容：[你的文本]"
  exit 1
fi

# 显示请求信息
echo "📝 正在处理你的请求..."
echo "🔌 调用接口：$API_URL"
echo ""

# 核心：POST JSON 请求
curl -s -X POST "$API_URL" \
  -H "Content-Type: application/json; charset=UTF-8" \
  -d "{\"content\":\"$USER_TEXT\"}"

echo ""
```

## 返回格式
```json
{
  "success": true,
  "result": { "目标 API 返回的数据" }
}
```

失败时返回：
```json
{
  "success": false,
  "message": "错误信息"
}
```

## 使用约束
- 必须传入非空 `content`
- `content` 应为待处理的完整文本
- 如果后端接口不可用，应明确返回失败原因，而不是伪造处理结果

## 说明
本 Skill 通过 Bash 脚本直接调用目标 API，无需中间服务。