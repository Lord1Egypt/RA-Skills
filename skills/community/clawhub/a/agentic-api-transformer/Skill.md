---
name: agentic-api-transformer
description: Transform existing API systems to follow the Agentic API Spec design with dynamic discovery and progressive disclosure
version: 0.1.0
metadata:
  openclaw:
    homepage: https://github.com/tomsun28/agent-api-spec
---

# Agentic API Transformer Skill

## Purpose

This skill helps you transform existing API systems to follow the Agentic API Spec design. It enables AI agents to discover APIs dynamically at runtime instead of loading massive static documentation upfront.

**Use this skill when:**
- Converting traditional REST APIs to agent-friendly formats
- Adding `relates` fields to API responses for progressive disclosure
- Generating `/api/llms.txt` entry points for API discovery
- Validating API compliance with the Agentic API specification

**Core concepts:**
- **Dynamic API Discovery**: APIs expose their capabilities through runtime responses
- **Relates Fields**: Each response includes next-step actions the agent can take
- **Progressive Disclosure**: Agents learn only what they need, when they need it
- **Error Code Standardization**: Stable error codes enable predictable agent behavior

## Workflow

When the user asks to transform their API to the Agentic API format:

### 1. Analyze Existing API
- Parse OpenAPI/Swagger specifications if available
- Identify CRUD operations and resource relationships
- Map resource hierarchies and dependencies
- Extract parameter schemas and response structures
- Generate TypeChat schemas for type definitions

**Tool**: Use API analysis utilities to scan existing endpoints
Available approaches:
- OpenAPI/Swagger parser libraries
- Manual endpoint documentation review
- Automated API discovery tools

### 2. Transform API Responses
- Add the three core fields: `data`, `error`, `relates`
- Standardize error codes (e.g., `TASK_LOCKED`, `INVALID_PARAM`)
- Generate `relates` arrays with next-step actions
- Create middleware for automatic transformation
- Preserve existing business logic without rewrites

**Tool**: Use response transformation utilities
Available approaches:
- Middleware wrappers for your framework
- Response interceptors and decorators
- Manual response formatting helpers

### 3. Generate API Entry Point
- Create `/api/llms.txt` endpoint for API discovery
- List top-level operations available to the current user
- Include TypeChat schemas for each entry API
- Add authentication requirements and usage guides
- Organize APIs by functionality or resource type

**Tool**: Use entry point generators
Available approaches:
- Template-based file generators
- Dynamic endpoint builders
- Static file generators with metadata

### 4. Generate Framework Code
- Detect the user's backend framework (Express, FastAPI, Spring Boot, Gin)
- Generate middleware for response transformation
- Create controller templates with proper structure
- Provide route handler examples
- Generate complete project structure if needed

**Tool**: Use code template systems
Available approaches:
- Framework-specific template engines
- Code generators with scaffolding
- Boilerplate plate generators

### 5. Validate Compliance
- Check all responses include `data`, `error`, `relates` fields
- Verify `relates` entries have `method`, `path`, `desc`, `schema`
- Ensure error codes are stable and documented
- Run automated test suites against transformed APIs
- Generate compliance reports with actionable recommendations

**Tool**: Use API validation utilities
Available approaches:
- Compliance testing frameworks
- Schema validation tools
- Automated API testing suites

## Output Format

After transformation, present:

### Analysis Summary
- Total endpoints analyzed
- Resource relationships discovered
- Required transformations identified

### Generated Code
- Middleware implementation for the detected framework
- Example transformed response structure
- `/api/llms.txt` content

### Validation Results
- Compliance status (passed/failed)
- Issues found with line references
- Recommendations for fixes

### Next Steps
- Installation commands for dependencies
- Integration instructions
- Testing commands to verify the transformation

## Rules

### Critical Requirements
- **Always preserve business logic**: Never rewrite existing API logic, only wrap responses
- **Validate before deploying**: Run compliance checks on all transformed endpoints
- **Use stable error codes**: Error codes must be consistent and documented (e.g., `TASK_LOCKED`, not generic messages)
- **Generate complete relates**: Every `relates` entry must include `method`, `path`, `desc`, and `schema`

### Best Practices
- **Start with analysis**: Always run API Analyzer before making changes
- **Incremental transformation**: Transform key endpoints first, then expand
- **Framework detection**: Auto-detect the user's framework from their codebase
- **Test thoroughly**: Run validation suite before marking transformation complete
- **Document changes**: Generate clear integration instructions for developers

### Error Handling
- If OpenAPI spec is missing, ask user to provide API documentation or endpoint list
- If framework cannot be detected, ask user which framework they're using
- If validation fails, provide specific fixes with code examples
- If dependencies are missing, provide installation commands

### Security
- Never expose API keys or credentials in generated code
- Warn if relates expose sensitive operations without auth checks
- Flag any hardcoded secrets in validation reports

## Examples

### Example 1: Quick API Transformation
```bash
# Analyze existing API (using OpenAPI parser)
# Example: Use swagger-parser or similar library

# Transform responses (using middleware)
# Example: Create response wrapper in your framework

# Output format:
# {
#   "data": {"id": "task_123", "title": "Fix bug"},
#   "error": null,
#   "relates": [
#     {
#       "method": "PUT",
#       "path": "/tasks/{id}",
#       "desc": "Update task info",
#       "schema": "interface UpdateTask { title?: string; completed?: boolean; }"
#     }
#   ]
# }
```

### Example 2: Generate Entry Point
```markdown
# Task Manager API

Manage tasks and projects with AI-friendly endpoints.

## Entry APIs

### POST /tasks
desc: Create a new task with specified priority  
schema: interface CreateTask { title: string; priority: 'low' | 'medium' | 'high'; }

### GET /tasks
desc: List all tasks with pagination  
schema: interface ListTasks { page?: number; limit?: number; }
```

Generate this file using:
- Template engines (Handlebars, Mustache)
- Static site generators
- Framework-specific routing
- Manual file creation

### Example 3: Framework-Specific Middleware
```javascript
// Express.js middleware example
app.use((req, res, next) => {
  const originalSend = res.send;
  res.send = function(data) {
    const transformed = {
      data: data,
      error: null,
      relates: generateRelates(req.path, req.method)
    };
    originalSend.call(this, transformed);
  };
  next();
});
```

```python
# FastAPI middleware example
from fastapi import Request, Response
import json

async def agentic_middleware(request: Request, call_next):
    response = await call_next(request)
    
    if response.headers.get("content-type", "").startswith("application/json"):
        data = json.loads(response.body)
        transformed = {
            "data": data,
            "error": None,
            "relates": generate_relates(request.url.path, request.method)
        }
        response.body = json.dumps(transformed).encode()
    
    return response
```

Similar patterns apply to Spring Boot, Go/Gin, and other frameworks.

## Reference: Agentic API Response Structure

All transformed APIs must return this structure:

```json
{
  "data": {},    // Business data (current state)
  "error": {     // Error control
    "code": "STABLE_ERROR_CODE",
    "message": "Human-readable message"
  },
  "relates": [   // Related actions (future options)
    {
      "method": "GET|POST|PUT|DELETE",
      "path": "/path/to/resource",
      "desc": "Brief description of the API's intent and parameters",
      "schema": "type Schema = { param: string; }"
    }
  ]
}
```

## Reference: /api/llms.txt Format

```markdown
# Project Name

Project description, usage guide, and authentication info.

## Entry APIs

### POST /tasks
desc: Create a new task with specified priority  
schema: interface CreateTask { title: string; priority: 'low' | 'medium' | 'high'; }

### GET /tasks
desc: List all tasks with pagination  
schema: interface ListTasks { page?: number; limit?: number; }
```

## Troubleshooting

### Missing Relates
**Problem**: Responses don't include next-step actions  
**Fix**: Ensure resource relationship mapping in analyzer, check relates generation logic

### Invalid TypeChat Schemas
**Problem**: Schema validation fails  
**Fix**: Use TypeScript interface syntax, validate with TypeChat parser

### Validation Errors
**Problem**: Compliance checks fail  
**Fix**: Review validation report, fix missing fields, ensure stable error codes

## Advanced: Custom Relates Logic

For complex workflows with conditional next steps:

```bash
# For complex workflows with conditional next steps:
# Use business logic to determine relates based on:
# - Current resource state
# - User permissions/roles
# - Workflow stage
# - Contextual factors

# Example logic (pseudocode):
if current_state == 'pending' and user.can_approve:
    relates.append({
        'method': 'POST',
        'path': '/approvals',
        'desc': 'Approve pending request',
        'schema': 'type Approve = { request_id: string; }'
    })
```

---

**Transform your APIs for the AI agent era!** 
