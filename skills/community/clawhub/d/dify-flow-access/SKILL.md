# Dify Workflow - OpenClaw CLI for Dify API

Use OpenClaw to query company knowledge base or execute workflows via Dify API. Supports multi-turn conversation and streaming responses.

## Trigger Conditions

When users need to access internal knowledge bases, documentation queries, Q&A systems, or execute specific workflows, this skill handles those requests such as "help me check the knowledge base" or "query Dify workflow".

## Features

- ✅ Call Dify Workflow API (workflow mode)
- ✅ Call Dify ChatApp API (chat mode)  
- ✅ Multi-turn conversation context management
- ✅ Streaming response support (show results incrementally)
- ✅ Automatic timeout and error handling
- ✅ Configurable request parameters

## Quick Start

```bash
# Basic ChatApp mode query (recommended, no workflow ID needed)
/dify-workflow "如何部署项目？" --chat

# Workflow mode query (requires specifying workflow ID)
/dify-workflow "查询 AI 助手信息" --wf wf_123456abcdef

# Multi-turn conversation (use conversation_id from previous response)
/dify-workflow "那退款流程呢？" --conv conv_xyz789

# Streaming response (show results incrementally)
/dify-workflow "解释一下这个概念" --stream

# Combined usage
/dify-workflow "查询中电港 AI 助手相关信息" --chat
```

## Configuration

**Base URL**: `http://10.10.10.159/v1`  
**API Key**: `app-jUhDcPj3lcnEG04JW4gRsfyy`

### Environment Variables (Optional Overrides)

You can override defaults via environment variables:

```bash
export DIFY_BASE_URL="http://your-dify-server/v1"
export DIFY_API_KEY="your-api-key-here"
export DEFAULT_TIMEOUT=120
```

## Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--chat` | Use ChatApp mode (default for most apps) | `--chat` |
| `--wf ID` | Specify workflow ID for Workflow mode | `--wf wf_xxx` |
| `--conv ID` | Specify conversation ID for multi-turn | `--conv conv_xxx` |
| `--stream` | Enable streaming response mode | `--stream` |

## API Endpoints

- **Workflow**: `POST /v1/workflows/run` - Execute predefined workflows
- **ChatApp**: `POST /v1/chat-messages` - Chat interface with knowledge base

### Request Format Examples

#### ChatApp Mode
```json
{
  "inputs": {},
  "query": "user query",
  "conversation_id": "conv_xxx",  // Optional for multi-turn
  "response_mode": "blocking",     // or "streaming"
  "user": "openclaw-user",
  "files": []
}
```

#### Workflow Mode
```json
{
  "workflow_id": "wf_xxx",
  "inputs": {
    "query": "user query"
  },
  "response_mode": "blocking",
  "user": "openclaw-user"
}
```

## Response Extraction

The script automatically extracts answers from different Dify response formats:

- **ChatApp**: `.data.answer`
- **Workflow**: `.data.outputs.answer` or `.data.outputs.*`
- **Advanced Chat**: `.answer` (top-level)

## Common Use Cases

### 1. Knowledge Base Query
```bash
/dify-workflow "员工手册中的报销政策是什么？" --chat
```

### 2. Multi-turn Conversation
```bash
# First query returns conversation_id: conv_abc123
/dify-workflow "那加班制度呢？" --conv conv_abc123
```

### 3. Execute Specific Workflow
```bash
/dify-workflow "生成月度报告" --wf wf_report_gen_xyz
```

### 4. Streaming Large Outputs
```bash
/dify-workflow "分析这个数据集" --stream
```

## Troubleshooting

### Common Errors and Solutions

1. **"not_workflow_app"**
   - **Cause**: Using Workflow mode for a ChatApp
   - **Solution**: Use `--chat` flag: `/dify-workflow "query" --chat`

2. **"conversation_id_invalid"**
   - **Cause**: Expired or incorrect conversation ID
   - **Solution**: Start fresh without `--conv` option

3. **"workflow_not_found"**
   - **Cause**: Invalid workflow ID
   - **Solution**: Verify the workflow ID exists in your Dify app (should start with `wf_`)

4. **"query missing parameter"**
   - **Cause**: Query parameter not included in payload
   - **Solution**: Ensure query is properly specified

### Getting IDs from Dify Dashboard

**ChatApp Mode:**
- No additional setup needed
- Conversation IDs are automatically returned in responses

**Workflow Mode:**
1. Open your Workflow app in Dify dashboard
2. Go to "API Access" or check the URL
3. Look for IDs starting with `wf_`

## Technical Details

### Unicode Support
- Automatic decoding of Unicode escape sequences (e.g., `\u4f60\u597d` → `你好`)
- Supports Chinese and other multi-language responses

### Error Handling
- Clear error messages with actionable suggestions
- Timeout protection (default 120 seconds)
- Graceful fallback for missing dependencies

### Dependencies
- Python 3.x (for JSON parsing and Unicode decoding)
- curl (for HTTP requests)
- jq (optional, for advanced output formatting)

## Version Information

- **Version**: 1.0.0
- **Last Updated**: 2026-05-20
- **Author**: OpenClaw Team
- **License**: Internal use only

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your Dify API credentials and configuration
3. Ensure network connectivity to Dify server at `http://10.10.10.159/v1`

---

**Note**: Default timeout is 120 seconds to accommodate complex workflow executions. Adjust via `DEFAULT_TIMEOUT` environment variable if needed.