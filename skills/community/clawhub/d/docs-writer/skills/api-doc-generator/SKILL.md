---
name: api-doc-generator
description: API 文档生成：OpenAPI/Swagger 规范、端点说明、请求示例、鉴权文档、错误处理
source:
  type: derived
  repo: skills-repo/docs-writer
  path: skills/api-doc-generator/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/sickn33/antigravity-awesome-skills/api-documentation-generator
metadata:
  category: 文档
  platform: Web
  difficulty: 进阶
---

# API 文档生成器

> 从代码自动生成专业 API 文档：端点描述、请求/响应示例、鉴权说明、错误处理、使用指南。

## 能力

- **OpenAPI 规范**：生成符合 OpenAPI 3.0/Swagger 规范的 API 描述文件
- **端点文档**：路径、方法、参数、请求体、响应体的完整文档
- **鉴权文档**：API Key、Bearer Token、OAuth2 等方式的说明
- **示例生成**：curl 命令、SDK 调用示例、响应 JSON 示例
- **多格式支持**：REST、GraphQL、WebSocket API 文档化
- **错误处理**：状态码说明、错误响应格式、常见错误排查

## 使用方式

```text
/api-doc-generator 为这个 Express 路由生成 API 文档
/api-doc-generator 从代码注释生成 OpenAPI 规范
/api-doc-generator 更新这个 API 的请求示例
```

## 工作流

1. 扫描代码中的 API 路由和处理器
2. 提取端点、参数、请求/响应类型
3. 识别鉴权方式和错误处理
4. 生成 OpenAPI/Swagger 规范文件
5. 可选：输出 Swagger UI / Redoc 可交互文档

## 适用场景

- REST API 文档初始化
- OpenAPI 规范补全
- API 文档从代码自动生成
- 第三方 API 对接文档
- 新开发者 API 入门文档

## 限制

- 主要覆盖 REST API，GraphQL schema 文档需额外配置
- 不涉及 SDK 文档生成
- 复杂鉴权流程需手动补充

## 相关参考（Playbook）

- [references/api-doc-authoring-playbook.md](../../references/api-doc-authoring-playbook.md) — 核心 playbook：REST/GraphQL 文档策略、质量矩阵、版本演进不破坏调用方、示例质量
- [references/doc-lifecycle-and-pipeline.md](../../references/doc-lifecycle-and-pipeline.md) — API 文档在生成顺序第 3 步、与实现一致性（CI 重生成防漂移）
- 产出后核查：[scripts/check_md_links.py](../../scripts/check_md_links.py)、[scripts/check_code_blocks.py](../../scripts/check_code_blocks.py)（第 6/10 节 CI 门禁）
- 规则源：[assets/markdown-lint-rules.json](../../assets/markdown-lint-rules.json)