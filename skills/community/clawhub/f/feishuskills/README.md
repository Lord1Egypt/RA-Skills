# Feishu Integration Solver Skill

A comprehensive skill that automatically solves Feishu integration problems by analyzing official documentation, community best practices, and implementing reliable automation approaches.

## Overview

This skill addresses the common challenges developers face when integrating with Feishu's Open Platform API:

- **Authentication Complexity**: Handles various token types (tenant_access_token, app_access_token, user_access_token)
- **API Versioning**: Manages different API versions and endpoints
- **Error Handling**: Provides intelligent error diagnosis and recovery
- **Rate Limiting**: Implements proper rate limiting and retry strategies
- **Community Best Practices**: Incorporates lessons learned from successful community implementations

## Features

### 1. Multi-Language Support
- **Python**: Uses `lark-oapi` SDK with async support
- **TypeScript/JavaScript**: Uses `@larksuiteoapi/node-sdk`
- **Go**: Uses official Go SDK
- **Ruby**: Community-maintained Ruby gem support

### 2. Problem Diagnosis
The skill can identify and solve common integration issues:
- Invalid access tokens (99991663 errors)
- Missing permissions (99991672 errors)
- Rate limiting issues
- Webhook signature verification failures
- Event subscription configuration problems

### 3. Automation Approaches
- **Full Automation**: When complete automation is possible with available credentials
- **Semi-Automation**: When manual steps are required (e.g., admin approval)
- **Best Alternative**: When automation isn't feasible, provides the optimal manual workflow

### 4. Integration Types Supported
- **Bot Integration**: Message sending, receiving, and interactive cards
- **Document Operations**: Read/write cloud documents, spreadsheets, wikis
- **User Management**: Directory operations, user information retrieval
- **File Operations**: Cloud storage file management
- **Permission Management**: Sharing and collaboration settings
- **Event Subscriptions**: Real-time webhook event handling

## Usage

### Basic Configuration
```json
{
  "app_id": "cli_xxx",
  "app_secret": "xxx",
  "problem_type": "auth_error",
  "error_code": "99991663"
}
```

### Advanced Configuration
```json
{
  "app_id": "cli_xxx",
  "app_secret": "xxx",
  "problem_type": "integration_setup",
  "integration_type": "bot",
  "features": ["message", "card", "file_upload"],
  "language": "python",
  "deployment_type": "server"
}
```

## Implementation Strategy

Based on extensive research of:
1. **Official Feishu Documentation**: Service API structure, authentication flows, rate limits
2. **Community Solutions**: GitHub repositories like FlashClaw, AIFeedTracker, alertmanager-webhook-feishu
3. **Best Practices**: Modular architecture, proper error handling, security considerations

### Key Insights from Research

**Authentication Flow**:
- Use `tenant_access_token` for most server-side operations
- Refresh tokens before expiration (2-hour TTL)
- Handle different token scopes based on required permissions

**Error Handling**:
- Error code 99991663: Invalid tenant token → refresh and retry
- Error code 99991672: Insufficient permissions → guide user through permission setup
- Implement exponential backoff for rate limiting

**Community Patterns**:
- **FlashClaw**: Plugin-based architecture with hot-reloading
- **AIFeedTracker**: Robust error handling with automatic cookie refresh
- **AlertManager Integration**: Simple webhook pattern for notifications

## Testing

The skill includes comprehensive tests covering:
- Authentication scenarios
- Common error conditions
- Different integration types
- Multi-language code generation
- Fallback strategies

Run tests with:
```bash
python scripts/test_feishu_integration_solver.py
```

## Dependencies

- Python 3.8+
- `lark-oapi>=1.4.8`
- `requests>=2.31.0`
- `pydantic>=2.0.0`

## Security Considerations

- Never log sensitive credentials
- Use environment variables for app secrets
- Validate webhook signatures for incoming events
- Implement proper input validation
- Follow principle of least privilege for permissions

## Limitations and Alternatives

### When Complete Automation Isn't Possible

1. **Admin Approval Required**: Some permissions require enterprise admin approval
   - **Alternative**: Provide step-by-step manual approval instructions
   
2. **Custom Domain Restrictions**: Enterprise-specific domain policies
   - **Alternative**: Guide through domain whitelist configuration
   
3. **Legacy API Versions**: Older Feishu deployments
   - **Alternative**: Detect version and provide compatible implementation

4. **Network Restrictions**: Corporate firewall/proxy limitations
   - **Alternative**: Provide proxy configuration guidance

## Examples

### Solving Authentication Errors
```python
from feishu_integration_solver import solve_integration_problem

config = {
    "app_id": "cli_xxx",
    "app_secret": "xxx", 
    "problem_type": "auth_error",
    "error_code": "99991663"
}

solution = solve_integration_problem(config)
print(solution.implementation_code)
print(solution.setup_instructions)
```

### Setting Up a New Bot Integration
```python
config = {
    "app_id": "cli_xxx",
    "app_secret": "xxx",
    "problem_type": "integration_setup", 
    "integration_type": "bot",
    "language": "python"
}

solution = solve_integration_problem(config)
# solution contains complete working implementation
```

## Contributing

This skill follows the OpenClaw skill structure:
- `SKILL.md`: Main skill definition and usage instructions
- `scripts/`: Implementation scripts
- `examples/`: Configuration examples  
- `tests/`: Test cases (if applicable)
- `assets/`: Additional resources (if needed)

To extend functionality:
1. Add new problem types to the solver logic
2. Implement additional language support
3. Enhance error diagnosis capabilities
4. Add more integration type templates

## License

MIT License - see LICENSE file for details.