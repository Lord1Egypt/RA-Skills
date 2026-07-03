---
name: api-push-product-platform
description: 推送后端 API 接口定义数据到产品部数据平台。
---

# API Push Product Platform

将后端 Java 接口定义（请求方法、路径、参数、响应结构）推送到产品部数据平台，实现接口文档的集中管理和同步。

## 触发场景

- 后端完成接口开发后推送到产品部数据平台
- 批量推送、增量更新、推送历史查询
- 产品需求（PRD）关联的接口文档同步

## 核心信息

- **推送地址**: `http://test-gateway.jinyi999.cn/rjhy-test-compliance-utils-api/api/v1/aitest/backend/message`
- **方法**: `POST`
- **Content-Type**: `application/json`
- **请求体参数**: 
  - `prdid` (必填): 产品需求 ID
  - `content` (必填): 接口文档 JSON 数据（主要是后端 Java 接口定义）

## 请求示例

```json
{
  "prdid": "PRD-2026-001",
  "content": {
    "apis": [
      {
        "method": "GET",
        "path": "/api/users/{id}",
        "description": "获取用户详情",
        "parameters": [...],
        "response": {...}
      }
    ]
  }
}
```

## 工作流程

1. 获取产品需求 ID（prdid）
2. 准备接口定义数据（Java 接口定义的 JSON 格式）
3. 执行推送脚本或 API 调用
4. 验证推送结果
5. 记录推送历史到 `references/push-history.md`

## 使用方式

**自然语言**（推荐）：直接告诉我需求，我引导你完成推送

**脚本方式**：
```bash
python3 scripts/push_api_to_product_platform.py --prdid "PRD-2026-001" --file ./api-definitions.json
```

**直接 API**：参考 `references/product-platform-api-docs.md`

## 接口定义格式

支持：
- 标准 JSON 格式
- Spring Boot Controller 注解提取
- Java 接口描述
- Swagger/OpenAPI 3.0 转换

详细格式规范见 `references/api-definition-standard.md`

## 错误处理

常见错误场景：
- 网络错误：重试机制（最多 3 次）
- 参数格式错误：检查 JSON 格式和必填字段（prdid, content）
- PRD ID 不存在：确认产品需求 ID 是否正确
- 服务器错误：记录详细错误日志并联系平台管理员

推送前验证接口定义完整性、参数清晰、响应结构明确。

## 最佳实践

- **推送前检查**：接口定义完整、参数清晰、响应结构明确
- **批量推送**：按模块分组，每次 < 50 个接口
- **版本管理**：标注新增/修改/废弃接口
- **通知相关人员**：推送完成后提供变更说明
- **记录历史**：每次推送记录到 `references/push-history.md`

详细实践见 `references/product-platform-api-docs.md`

## 相关文档

- [产品部数据平台 API 文档](references/product-platform-api-docs.md)
- [接口定义规范](references/api-definition-standard.md)
- [推送历史记录](references/push-history.md)

## 自动化集成

支持 CI/CD 集成和 Git Hook 集成，配置示例见 `references/product-platform-api-docs.md`
