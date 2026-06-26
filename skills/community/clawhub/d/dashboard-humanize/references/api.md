# Dashboard Console 去AI化接口（/ai-tools/humanize）

Base prefix（在 main.py 注册）：

- `POST /employee-console/dashboard/v2/api/ai-tools/humanize`

认证：

- 默认需要 `Authorization: Bearer <access_token>`
- token 获取接口：`POST /employee-console/dashboard/v2/api/auth/login`

## Request: HumanizerRequest

```json
{
  "title": "",                 // optional
  "content": "...",            // required
  "prompt": "",                // optional，自定义提示词
  "length": "standard",        // default: standard
  "tone": "normal",            // default: normal
  "purpose": "general_writing",// default: general_writing
  "language": "Simplified Chinese" // default
}
```

## Response: SuccessResponse[HumanizerResponse]

```json
{
  "success": true,
  "message": "内容人性化完成",
  "data": {
    "title": "...",
    "content": "...",
    "ai_score": 0.12,
    "detailed_result": {
      "ai_percentage": 12,
      "mixed_percentage": 23,
      "human_percentage": 65,
      "comprehensive_score": 88,
      "conclusion": "human_generated"
    }
  }
}
```

实现位置：

- `dashboard-console/api/ai_tools.py` → `@router.post("/ai-tools/humanize")`
- 内部会转调 core service：`/core-service/v1/humanize_content`
