# Feishu Integration Problem Solver

This skill automatically solves Feishu integration problems by researching official documentation, finding community solutions, and implementing the most reliable automation approach.

## Capabilities

- **Authentication & Authorization**: Handles app_id/app_secret setup, tenant access tokens, user access tokens, and bot access tokens
- **Message Handling**: Supports text, rich text, cards, and file messages with proper formatting
- **Event Processing**: Webhook event handling with signature verification and proper response format
- **API Integration**: Comprehensive support for Feishu's service APIs including docs, drive, wiki, calendar, etc.
- **Error Handling**: Intelligent error diagnosis and recovery for common issues like token expiration, permission errors, and rate limiting
- **Fallback Strategies**: When complete automation isn't possible, provides alternative approaches and manual workarounds

## Usage

### Basic Integration Setup
When users mention Feishu integration issues, this skill will:
1. Analyze the specific problem (authentication, messaging, API calls, etc.)
2. Check if they have proper app credentials configured
3. Implement the appropriate solution based on the use case
4. Provide fallback options if automation isn't possible

### Supported Scenarios
- **Bot Development**: Creating interactive bots that respond to messages and events
- **Document Automation**: Reading/writing Feishu documents and cloud files
- **Workflow Integration**: Connecting Feishu with external systems and services
- **Permission Management**: Handling sharing and collaboration permissions
- **Knowledge Base Access**: Reading and managing Feishu wiki/knowledge base content

## Implementation Details

### Authentication Flow
The skill implements the standard Feishu authentication flow:
1. **App Credentials**: Uses `FEISHU_APP_ID` and `FEISHU_APP_SECRET` from environment or configuration
2. **Tenant Token**: Automatically obtains and caches tenant access tokens with proper refresh logic
3. **User Tokens**: Handles OAuth flows when user-specific actions are required
4. **Bot Tokens**: Manages bot access tokens for messaging capabilities

### Error Recovery
Common error scenarios and their solutions:
- **Token Invalid (99991663)**: Automatically refreshes expired tokens
- **Permission Denied (99991672)**: Guides users through permission setup in Feishu admin console
- **Rate Limiting**: Implements exponential backoff with jitter
- **Network Issues**: Provides retry logic with circuit breaker patterns

### Fallback Strategies
When automation isn't possible:
1. **Manual Configuration Guide**: Step-by-step instructions for manual setup
2. **Alternative APIs**: Suggests different API endpoints or approaches
3. **Web Interface Workaround**: Provides guidance for using Feishu web interface as alternative
4. **Community Solutions**: References relevant GitHub repositories and community examples

## Dependencies

This skill leverages existing Feishu skills when available:
- `feishu-doc`: For document operations
- `feishu-drive`: For cloud storage management  
- `feishu-perm`: For permission handling
- `feishu-wiki`: For knowledge base operations

If these skills aren't available, it implements basic functionality directly using Feishu's REST APIs.

## Security Considerations

- **Credential Management**: Never logs or exposes app secrets
- **Token Storage**: Caches tokens securely with automatic expiration
- **Input Validation**: Validates all inputs to prevent injection attacks
- **Rate Limiting**: Respects Feishu's API rate limits to avoid account restrictions

## Testing & Validation

The skill includes built-in validation:
- **Connection Test**: Verifies app credentials and basic connectivity
- **Permission Check**: Validates required permissions before attempting operations
- **Mock Mode**: Allows testing without making actual API calls (for development)
- **Diagnostic Output**: Provides detailed logs for troubleshooting

## Examples

### Example 1: Bot Message Handling
```
User: "My Feishu bot isn't receiving messages"
Skill: Checks webhook configuration, verifies signature validation, tests message routing
```

### Example 2: Document Access
```
User: "I can't read Feishu documents programmatically"  
Skill: Implements document reading with proper authentication, handles permission errors, suggests alternative approaches
```

### Example 3: Permission Issues
```
User: "Getting permission denied when trying to share files"
Skill: Guides through permission setup, implements proper sharing workflow, provides manual workaround
```