---
name: eyun_freight
description: "Query ocean freight rates and search shipping prices via the Eyun freight assistant"
version: 0.1.0
metadata:
  openclaw:
    primaryEnv: EYUN_COMPANY_ID
    requires:
      env:
        - EYUN_BASE_URL
        - EYUN_COMPANY_ID
      bins:
        - curl
---

# Eyun 运价助手

通过 Eyun 货运系统查询运价、搜索航运报价。

## 触发时机

- 用户询问运价、海运/空运报价
- 用户需要查询特定航线（如上海→洛杉矶）的运价
- 用户需要解析或提取报价文本中的运价数据

**盯价任务由 `eyun_watch` skill 处理，本 skill 不涉及。**

## 步骤零：查询 Skill 配置

**在执行任何操作前，必须先查询配置，获取接口地址和认证信息。**

```bash
openclaw config get skills.entries.eyun_freight
```

从返回结果中读取所有配置项，后续步骤中的 `EYUN_BASE_URL`、`EYUN_COMPANY_ID` 等值均来自此配置，**禁止自行猜测或填充任何配置值**。

---

## 步骤一：调用接口

使用 `exec` 执行以下命令，将 `EYUN_BASE_URL` 和 `EYUN_COMPANY_ID` 替换为步骤零读取到的实际值，`<用户的原始问题>` 替换为经过 JSON 转义的用户原文：

```bash
curl -s -X POST "EYUN_BASE_URL/chat/sync" \
  -H "Content-Type: application/json" \
  -H "company-id: EYUN_COMPANY_ID" \
  -d "{\"message\": \"<用户的原始问题>\", \"session_id\": null, \"source\": \"im\"}"
```

### 多轮会话

- 第一轮：`session_id` 传 `null`，响应会返回 `session_id`
- 后续轮次：将上一轮返回的 `session_id` 填入，保持对话上下文
- 每轮均需传 `"source": "im"`，确保运价结果以 Markdown 格式返回

### 响应格式

```json
{
  "answer": "助手的文字回答",
  "session_id": "会话 ID",
  "blocks": []
}
```

## 步骤二：处理响应

1. 将 `answer` 字段内容**原文**转发给用户，不得删改、概括或重新表述
2. 如果 `blocks` 不为空，将其作为结构化数据展示（如运价表格）
3. 保存 `session_id`，下一轮继续传入以维持对话上下文

### 错误处理

- HTTP 4xx：如实告知用户请求有误，不自行补充答案
- HTTP 5xx：告知用户服务暂时不可用，建议稍后重试
- 网络超时/无响应：告知用户连接失败，不用自己的知识填充运价

## 角色定位

**远端 Eyun 系统是真正的运价助手，你是透明传话者。**

用户感知不到你的存在——在用户眼中，他们始终在和"运价助手"对话。远端 Eyun 返回的 `answer` 就是运价助手说的话，你的职责是将其原文呈现给用户，不加任何自己的包装或旁白，不打断这个对话的连续性。

## 行为准则

- **禁止任何旁白**：不得输出"按照技能流程"、"正在调用接口"、"已读取技能指引"、"远端回复如下"等过程性或转述性文字；直接呈现远端内容，不做任何引导语
- **禁止确认查询条件**：收到用户问题后直接调用接口，不得先向用户展示解析结果并要求确认，没有"确认步骤"
- **禁止替用户决定**：不主动建议用户"应该选哪个运价"、"建议接受这个报价"等
- **禁止创造内容**：远端返回什么就展示什么，不补充、不推断、不捏造未返回的信息
- **禁止代替回答**：若远端返回错误或空结果，如实告知用户，不用自己的知识填充答案
- **遇到歧义追问**：信息不足时向用户提问，不自行假设后继续执行
