---
name: CDK最佳实践服务
description: AWS CDK MCP Server是一个提供AWS Cloud Development Kit (CDK)最佳实践、基础设施即代码模式和CDK Nag安全合规性的工具，适用于开发者在构建AWS应用程序时获取指导和建议。
version: 1.0.0
---

# CDK最佳实践服务

AWS CDK MCP Server是一个提供AWS Cloud Development Kit (CDK)最佳实践、基础设施即代码模式和CDK Nag安全合规性的工具，适用于开发者在构建AWS应用程序时获取指导和建议。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| Use this tool to get prescriptive CDK advice for building applications on AWS.

Args:
    ctx: MCP context
 | `scripts.tools.CDKGeneralGuidance` |
| Explain a specific CDK Nag rule with AWS Well-Architected guidance.

CDK Nag is a crucial tool for ensuring your CDK applications follow AWS security best practices.

Basic implementation:
```typescript
import { App } from 'aws-cdk-lib';
import { AwsSolutionsChecks } from 'cdk-nag';

const app = new App();
// Create your stack
const stack = new MyStack(app, 'MyStack');
// Apply CDK Nag
AwsSolutionsChecks.check(app);
```

Optional integration patterns:

1. Using environment variables:
```typescript
if (process.env.ENABLE_CDK_NAG === 'true') {
  AwsSolutionsChecks.check(app);
}
```

2. Using CDK context parameters:
```typescript
3. Environment-specific application:
```typescript
const environment = app.node.tryGetContext('environment') || 'development';
if (['production', 'staging'].includes(environment)) {
  AwsSolutionsChecks.check(stack);
}
```

For more information on specific rule packs:
- Use resource `cdk-nag://rules/{rule_pack}` to get all rules for a specific pack
- Use resource `cdk-nag://warnings/{rule_pack}` to get warnings for a specific pack
- Use resource `cdk-nag://errors/{rule_pack}` to get errors for a specific pack

Args:
    ctx: MCP context
    rule_id: The CDK Nag rule ID (e.g., 'AwsSolutions-IAM4')

Returns:
    Dictionary with detailed explanation and remediation steps
 | `scripts.tools.ExplainCDKNagRule` |
| DEPRECATED: This tool is deprecated. Please use the AWS IaC MCP Server instead.

Check if CDK code contains Nag suppressions that require human review.

Scans TypeScript/JavaScript code for NagSuppressions usage to ensure security
suppressions receive proper human oversight and justification.

Args:
    ctx: MCP context
    code: CDK code to analyze (TypeScript/JavaScript)
    file_path: Path to a file containing CDK code to analyze

Returns:
    Analysis results with suppression details and security guidance
 | `scripts.tools.CheckCDKNagSuppressions` |
| DEPRECATED: This tool is deprecated. Please use the AWS IaC MCP Server instead.

Generate OpenAPI schema for Bedrock Agent Action Groups from a file.

This tool converts a Lambda file with BedrockAgentResolver into a Bedrock-compatible
OpenAPI schema. It uses a progressive approach to handle common issues:
1. Direct import of the Lambda file
2. Simplified version with problematic imports commented out
3. Fallback script generation if needed

Args:
    ctx: MCP context
    lambda_code_path: Path to Python file containing BedrockAgentResolver app
    output_path: Where to save the generated schema

Returns:
    Dictionary with schema generation results, including status, path to generated schema,
    and diagnostic information if errors occurred
 | `scripts.tools.GenerateBedrockAgentSchema` |
| Search and discover AWS Solutions Constructs patterns.

AWS Solutions Constructs are vetted architecture patterns that combine multiple
AWS services to solve common use cases following AWS Well-Architected best practices.

Key benefits:
- Accelerated Development: Implement common patterns without boilerplate code
- Best Practices Built-in: Security, reliability, and performance best practices
- Reduced Complexity: Simplified interfaces for multi-service architectures
- Well-Architected: Patterns follow AWS Well-Architected Framework principles

When to use Solutions Constructs:
- Implementing common architecture patterns (e.g., API + Lambda + DynamoDB)
- You want secure defaults and best practices applied automatically
- You need to quickly prototype or build production-ready infrastructure

This tool provides metadata about patterns. For complete documentation,
use the resource URI returned in the 'documentation_uri' field.

Args:
    ctx: MCP context
    pattern_name: Optional name of the specific pattern (e.g., 'aws-lambda-dynamodb')
    services: Optional list of AWS services to search for patterns that use them
             (e.g., ['lambda', 'dynamodb'])

Returns:
    Dictionary with pattern metadata including description, services, and documentation URI
 | `scripts.tools.GetAwsSolutionsConstructPattern` |
| Search for GenAI CDK constructs by name or type.

The search is flexible and will match any of your search terms (OR logic).
It handles common variations like singular/plural forms and terms with/without spaces.
Content is fetched dynamically from GitHub to ensure the most up-to-date documentation.

Examples:
- "bedrock agent" - Returns all agent-related constructs
- "knowledgebase vector" - Returns knowledge base constructs related to vector stores
- "agent actiongroups" - Returns action groups for agents
- "opensearch vector" - Returns OpenSearch vector constructs

The search supports subdirectory content (like knowledge bases and their sections)
and will find matches across all available content.

Args:
    ctx: MCP context
    query: Search term(s) to find constructs by name or description
    construct_type: Optional filter by construct type ('bedrock', 'opensearchserverless', etc.)

Returns:
    Dictionary with matching constructs and resource URIs
 | `scripts.tools.SearchGenAICDKConstructs` |
| Provide documentation sources for Lambda layers.

This tool returns information about where to find documentation for Lambda layers
and instructs the MCP Client to fetch and process this documentation.

Args:
    ctx: MCP context
    layer_type: Type of layer ("generic" or "python")

Returns:
    Dictionary with documentation source information
 | `scripts.tools.LambdaLayerDocumentationProvider` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.CDKGeneralGuidance
工具描述：Use this tool to get prescriptive CDK advice for building applications on AWS.

Args:
    ctx: MCP context

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|

---

## scripts.tools.ExplainCDKNagRule
工具描述：Explain a specific CDK Nag rule with AWS Well-Architected guidance.

CDK Nag is a crucial tool for ensuring your CDK applications follow AWS security best practices.

Basic implementation:
```typescript
import { App } from 'aws-cdk-lib';
import { AwsSolutionsChecks } from 'cdk-nag';

const app = new App();
// Create your stack
const stack = new MyStack(app, 'MyStack');
// Apply CDK Nag
AwsSolutionsChecks.check(app);
```

Optional integration patterns:

1. Using environment variables:
```typescript
if (process.env.ENABLE_CDK_NAG === 'true') {
  AwsSolutionsChecks.check(app);
}
```

2. Using CDK context parameters:
```typescript
3. Environment-specific application:
```typescript
const environment = app.node.tryGetContext('environment') || 'development';
if (['production', 'staging'].includes(environment)) {
  AwsSolutionsChecks.check(stack);
}
```

For more information on specific rule packs:
- Use resource `cdk-nag://rules/{rule_pack}` to get all rules for a specific pack
- Use resource `cdk-nag://warnings/{rule_pack}` to get warnings for a specific pack
- Use resource `cdk-nag://errors/{rule_pack}` to get errors for a specific pack

Args:
    ctx: MCP context
    rule_id: The CDK Nag rule ID (e.g., 'AwsSolutions-IAM4')

Returns:
    Dictionary with detailed explanation and remediation steps

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|rule_id|string|true| |null|

---

## scripts.tools.CheckCDKNagSuppressions
工具描述：DEPRECATED: This tool is deprecated. Please use the AWS IaC MCP Server instead.

Check if CDK code contains Nag suppressions that require human review.

Scans TypeScript/JavaScript code for NagSuppressions usage to ensure security
suppressions receive proper human oversight and justification.

Args:
    ctx: MCP context
    code: CDK code to analyze (TypeScript/JavaScript)
    file_path: Path to a file containing CDK code to analyze

Returns:
    Analysis results with suppression details and security guidance

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|code|null|false| |null|
|file_path|null|false| |null|

---

## scripts.tools.GenerateBedrockAgentSchema
工具描述：DEPRECATED: This tool is deprecated. Please use the AWS IaC MCP Server instead.

Generate OpenAPI schema for Bedrock Agent Action Groups from a file.

This tool converts a Lambda file with BedrockAgentResolver into a Bedrock-compatible
OpenAPI schema. It uses a progressive approach to handle common issues:
1. Direct import of the Lambda file
2. Simplified version with problematic imports commented out
3. Fallback script generation if needed

Args:
    ctx: MCP context
    lambda_code_path: Path to Python file containing BedrockAgentResolver app
    output_path: Where to save the generated schema

Returns:
    Dictionary with schema generation results, including status, path to generated schema,
    and diagnostic information if errors occurred

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|lambda_code_path|string|true| |null|
|output_path|string|true| |null|

---

## scripts.tools.GetAwsSolutionsConstructPattern
工具描述：Search and discover AWS Solutions Constructs patterns.

AWS Solutions Constructs are vetted architecture patterns that combine multiple
AWS services to solve common use cases following AWS Well-Architected best practices.

Key benefits:
- Accelerated Development: Implement common patterns without boilerplate code
- Best Practices Built-in: Security, reliability, and performance best practices
- Reduced Complexity: Simplified interfaces for multi-service architectures
- Well-Architected: Patterns follow AWS Well-Architected Framework principles

When to use Solutions Constructs:
- Implementing common architecture patterns (e.g., API + Lambda + DynamoDB)
- You want secure defaults and best practices applied automatically
- You need to quickly prototype or build production-ready infrastructure

This tool provides metadata about patterns. For complete documentation,
use the resource URI returned in the 'documentation_uri' field.

Args:
    ctx: MCP context
    pattern_name: Optional name of the specific pattern (e.g., 'aws-lambda-dynamodb')
    services: Optional list of AWS services to search for patterns that use them
             (e.g., ['lambda', 'dynamodb'])

Returns:
    Dictionary with pattern metadata including description, services, and documentation URI

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|pattern_name|null|false| |null|
|services|null|false| |null|

---

## scripts.tools.SearchGenAICDKConstructs
工具描述：Search for GenAI CDK constructs by name or type.

The search is flexible and will match any of your search terms (OR logic).
It handles common variations like singular/plural forms and terms with/without spaces.
Content is fetched dynamically from GitHub to ensure the most up-to-date documentation.

Examples:
- "bedrock agent" - Returns all agent-related constructs
- "knowledgebase vector" - Returns knowledge base constructs related to vector stores
- "agent actiongroups" - Returns action groups for agents
- "opensearch vector" - Returns OpenSearch vector constructs

The search supports subdirectory content (like knowledge bases and their sections)
and will find matches across all available content.

Args:
    ctx: MCP context
    query: Search term(s) to find constructs by name or description
    construct_type: Optional filter by construct type ('bedrock', 'opensearchserverless', etc.)

Returns:
    Dictionary with matching constructs and resource URIs

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|query|null|false| |null|
|construct_type|null|false| |null|

---

## scripts.tools.LambdaLayerDocumentationProvider
工具描述：Provide documentation sources for Lambda layers.

This tool returns information about where to find documentation for Lambda layers
and instructs the MCP Client to fetch and process this documentation.

Args:
    ctx: MCP context
    layer_type: Type of layer ("generic" or "python")

Returns:
    Dictionary with documentation source information

### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|layer_type|string|true| |null|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据