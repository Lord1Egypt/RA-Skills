# n8n Workflow Automation Skill

## Overview
This skill provides voice-controlled access to n8n workflow automation through the n8n MCP server.

## Capabilities
- List all workflows
- Get workflow details
- Create new workflows
- Activate/deactivate workflows
- Execute workflows manually
- Delete workflows
- Deploy workflow JSON

## Voice Commands

### List Workflows
**Trigger:** "List my n8n workflows" | "Show n8n workflows" | "What workflows do I have"
**Action:** Calls `list_workflows` tool
**Response:** Lists all workflows with their status (active/inactive)

### Get Workflow Details
**Trigger:** "Show me workflow [name]" | "Get details of [name]" | "Tell me about workflow [name]"
**Action:** Calls `get_workflow` tool with workflow ID
**Response:** Shows workflow details (nodes, status, last execution)

### Create Workflow
**Trigger:** "Create n8n workflow [name]" | "New workflow called [name]"
**Action:** Calls `create_workflow` tool
**Response:** Creates workflow and returns ID

### Activate/Deactivate
**Trigger:** "Activate workflow [name]" | "Turn on [name]" | "Deactivate [name]"
**Action:** Calls `activate_workflow` tool
**Response:** Confirms activation/deactivation

### Execute Workflow
**Trigger:** "Run workflow [name]" | "Execute [name]" | "Trigger [name]"
**Action:** Calls `execute_workflow` tool
**Response:** Executes workflow and returns result

### Delete Workflow
**Trigger:** "Delete workflow [name]" | "Remove [name]"
**Action:** Calls `delete_workflow` tool (with confirmation)
**Response:** Confirms deletion

## MCP Server Configuration

**Server Name:** `n8nbidirectional`
**Command:** `python -m n8n_mcp_server`
**Working Directory:** `mcp-servers/n8n-mcp-bidirectional`

**Environment Variables:**
- `N8N_API_KEY` - n8n API key
- `N8N_BASE_URL` - n8n instance URL

## Available Tools

1. **list_workflows** - List all workflows
2. **get_workflow** - Get workflow by ID
3. **create_workflow** - Create new workflow
4. **update_workflow** - Update existing workflow
5. **delete_workflow** - Delete workflow
6. **execute_workflow** - Execute workflow manually
7. **activate_workflow** - Activate/deactivate workflow
8. **deploy_workflow** - Deploy workflow JSON
9. **create_node** - Create individual node
10. **validate_workflow** - Validate workflow
11. **validate_node** - Validate node
12. **optimize_workflow** - Optimize workflow
13. **export_workflow** - Export workflow
14. **suggest_improvements** - Suggest improvements

## Example Interactions

### Example 1: List Workflows
**User:** "List my n8n workflows"
**Assistant:** 
```
Found 3 workflows:
1. Customer Onboarding (Active)
2. Daily Report Generator (Active)
3. Slack Notifications (Inactive)
```

### Example 2: Get Workflow Details
**User:** "Show me details of Customer Onboarding"
**Assistant:**
```
Workflow: Customer Onboarding
Status: Active
Nodes: 5
- Webhook Trigger
- Send Welcome Email
- Create CRM Entry
- Notify Team
- Set Follow-up Task
Last Execution: 2 hours ago (Success)
```

### Example 3: Create Workflow
**User:** "Create a new n8n workflow called Email Digest"
**Assistant:**
```
Created workflow: Email Digest
ID: abc123
Status: Inactive
Next: Add nodes to your workflow in the n8n UI
```

### Example 4: Execute Workflow
**User:** "Run the Daily Report Generator"
**Assistant:**
```
Executing workflow: Daily Report Generator
Status: Running...
Result: Success
Duration: 3.2 seconds
Output: Report generated and sent to team@company.com
```

## Integration with n8n Instance

**Production Instance:** https://automation.gervalla-steuern.de
**API Version:** v1
**Authentication:** API Key (JWT)

## Error Handling

### Common Errors:
1. **Workflow not found** - Check workflow name/ID
2. **API connection failed** - Verify n8n instance is running
3. **Authentication failed** - Check API key validity
4. **Execution failed** - Check workflow configuration

## Best Practices

1. **Always list workflows first** to get correct names/IDs
2. **Use exact workflow names** for better accuracy
3. **Confirm destructive actions** (delete, deactivate)
4. **Check execution results** after running workflows
5. **Keep workflows organized** with clear naming

## Related Skills
- **workflow-automation** - General workflow automation
- **api-integration** - API integration patterns
- **task-scheduling** - Scheduled task management

## Maintenance
- **API Key Expiry:** 2025-10-27
- **Server Location:** `mcp-servers/n8n-mcp-bidirectional`
- **Config File:** `.env` (not in Git)

## Troubleshooting

### Server Not Connected
1. Check MCP Tools in Settings
2. Verify `.env` file exists
3. Restart SpeakMCP
4. Run `fix-connection.ps1`

### Voice Commands Not Working
1. Verify server is connected (green in MCP Tools)
2. Check microphone permissions
3. Use exact trigger phrases
4. Speak clearly and wait for response

## Version History
- **v1.0** (2025-01-01) - Initial skill creation
- MCP Server: n8n-mcp-bidirectional
- Tools: 14 available

