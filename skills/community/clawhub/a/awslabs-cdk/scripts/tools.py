from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def CDKGeneralGuidance(
) -> Dict[str, Any]:
    """
    Use this tool to get prescriptive CDK advice for building applications on AWS.

Args:
    ctx: MCP context

    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419060465667", "CDKGeneralGuidance", arguments)

def ExplainCDKNagRule(
    rule_id: str
) -> Dict[str, Any]:
    """
    Explain a specific CDK Nag rule with AWS Well-Architected guidance.

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

    
    Args:
        rule_id: null
    
    Returns:
        null
    """
    arguments = {
        "rule_id": rule_id
    }
    
    return call_api("1777419060465667", "ExplainCDKNagRule", arguments)

def CheckCDKNagSuppressions(
    code: Optional[null] = None,
    file_path: Optional[null] = None
) -> Dict[str, Any]:
    """
    DEPRECATED: This tool is deprecated. Please use the AWS IaC MCP Server instead.

Check if CDK code contains Nag suppressions that require human review.

Scans TypeScript/JavaScript code for NagSuppressions usage to ensure security
suppressions receive proper human oversight and justification.

Args:
    ctx: MCP context
    code: CDK code to analyze (TypeScript/JavaScript)
    file_path: Path to a file containing CDK code to analyze

Returns:
    Analysis results with suppression details and security guidance

    
    Args:
        code: null
        file_path: null
    
    Returns:
        null
    """
    arguments = {
        "code": code,
        "file_path": file_path
    }
    
    return call_api("1777419060465667", "CheckCDKNagSuppressions", arguments)

def GenerateBedrockAgentSchema(
    lambda_code_path: str,
    output_path: str
) -> Dict[str, Any]:
    """
    DEPRECATED: This tool is deprecated. Please use the AWS IaC MCP Server instead.

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

    
    Args:
        lambda_code_path: null
        output_path: null
    
    Returns:
        null
    """
    arguments = {
        "lambda_code_path": lambda_code_path,
        "output_path": output_path
    }
    
    return call_api("1777419060465667", "GenerateBedrockAgentSchema", arguments)

def GetAwsSolutionsConstructPattern(
    pattern_name: Optional[null] = None,
    services: Optional[null] = None
) -> Dict[str, Any]:
    """
    Search and discover AWS Solutions Constructs patterns.

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

    
    Args:
        pattern_name: null
        services: null
    
    Returns:
        null
    """
    arguments = {
        "pattern_name": pattern_name,
        "services": services
    }
    
    return call_api("1777419060465667", "GetAwsSolutionsConstructPattern", arguments)

def SearchGenAICDKConstructs(
    query: Optional[null] = None,
    construct_type: Optional[null] = None
) -> Dict[str, Any]:
    """
    Search for GenAI CDK constructs by name or type.

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

    
    Args:
        query: null
        construct_type: null
    
    Returns:
        null
    """
    arguments = {
        "query": query,
        "construct_type": construct_type
    }
    
    return call_api("1777419060465667", "SearchGenAICDKConstructs", arguments)

def LambdaLayerDocumentationProvider(
    layer_type: str
) -> Dict[str, Any]:
    """
    Provide documentation sources for Lambda layers.

This tool returns information about where to find documentation for Lambda layers
and instructs the MCP Client to fetch and process this documentation.

Args:
    ctx: MCP context
    layer_type: Type of layer ("generic" or "python")

Returns:
    Dictionary with documentation source information

    
    Args:
        layer_type: null
    
    Returns:
        null
    """
    arguments = {
        "layer_type": layer_type
    }
    
    return call_api("1777419060465667", "LambdaLayerDocumentationProvider", arguments)

