---
name: custom-api-summary
description: 调用自定义摘要 API，对用户提供的文本进行处理并返回结果
version: 1.0.0
---

# Custom API Summary Skill

## 功能
当用户明确要求对一段文本进行总结、提炼、归纳或处理时，调用本项目提供的 HTTP 接口，将用户输入作为 `content` 参数传入，并返回接口处理结果。

## 适用场景
- 总结一段较长文本
- 提炼文章重点
- 对输入内容做统一的摘要处理

## 触发条件
当用户表达以下意图时触发：
- “帮我总结这段内容”
- “提炼一下这段文字”
- “把这段话做个摘要”

不应在普通闲聊、无明确文本处理需求时自动触发。

## 输入
用户提供的原始文本内容。

## 调用方式

### Skill 服务入口
- **URL**: `/api/skill/call`
- **Method**: `POST`
- **Headers**:
```json
{
  "Content-Type": "application/json"
}
```
- **Body**:
```json
{
  "content": "用户输入的内容"
}
```

### 服务内部转发目标
- **URL**: `https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call`
- **Method**: `POST`
- **Headers**:
```json
{
  "Content-Type": "application/json"
}
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
本文件作为当前项目的正式 skill 说明文件使用。
如果需要命令行调试，可参考 `heqq-skill.md` 中的调试版脚本。