---
name: api-push-frontend
description: "推送后端 API 接口定义到前端数据接口平台。"
---

# API Push Frontend

将后端 API 接口定义（请求方法、路径、参数、响应结构）推送到前端数据接口平台，实现前后端接口文档同步。

## 触发场景

- 后端完成接口开发后推送到前端平台
- 批量推送、增量更新、推送历史查询

## 核心信息

- **推送地址**: `https://jffe.techgp.cn/md/api/uploadV4`
- **方法**: `POST`
- **Content-Type**: `application/json`
- **必填参数**: `prdId` (产品需求 ID), `apis` (接口定义数组)

## 工作流程

1. 获取产品需求 ID（prdId）
2. 准备接口定义（JSON/Swagger/自然语言）
3. 执行推送脚本或 API 调用
4. 验证推送结果
5. 记录推送历史到 `references/push-history.md`

## 使用方式

**自然语言**（推荐）：直接告诉我需求，我引导你完成推送

**脚本方式**：
```bash
python3 scripts/push_api_to_frontend.py --prdId "PRD-2026-001" --file ./api-definitions.json
```

**直接 API**：参考 `references/frontend-api-docs.md`

## 接口定义格式

支持：
- 标准 JSON 格式
- Swagger/OpenAPI 3.0
- Spring Boot Controller 注解
- Java 接口描述

详细格式规范见 `references/api-definition-standard.md`

## 错误处理

常见错误码：
- `400`: 参数格式错误 → 检查 JSON 格式和必填字段
- `401`: 认证失败 → 检查认证 token
- `404`: prdId 不存在 → 确认产品需求 ID
- `500`: 服务器错误 → 联系平台管理员

推送前验证、网络错误重试（最多 3 次）、记录详细错误日志。

## 最佳实践

- 推送前检查：接口定义完整、参数清晰、响应结构明确
- 批量推送：按模块分组，每次 < 50 个接口
- 版本管理：标注新增/修改/废弃接口
- 通知前端：推送完成后提供变更说明

详细实践见 `references/frontend-api-docs.md`

## 相关文档

- [前端数据接口平台 API 文档](references/frontend-api-docs.md)
- [接口定义规范](references/api-definition-standard.md)
- [推送历史记录](references/push-history.md)

## 自动化集成

支持 CI/CD 集成和 Git Hook 集成，配置示例见 `references/frontend-api-docs.md`
