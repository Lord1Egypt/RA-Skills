functions/src/mcp/openclaw-skill/SKILL.md

# Capital Equipment Platform

Find, book, and manage scientific research equipment through your AI assistant. Search 10,000+ instruments across 500+ core facilities at 200+ institutions.

## What This Skill Does

- **Search Equipment**: Find microscopes, spectrometers, sequencers near any location
- **Check Availability**: Real-time booking windows for shared instruments
- **Book Equipment**: Reserve time slots directly through your assistant
- **Submit Service Requests**: Describe needs and get quotes from providers
- **Find Collaborators**: Discover researchers by expertise in specific techniques
- **Track Papers**: Find published research linked to specific instruments
- **Compatibility Check**: Verify equipment combinations for workflows
- **Price Intelligence**: Fair market values, institutional rates, depreciation
- **Compliance**: IP agreement and safety requirements for cross-institutional use

## Authentication

This skill uses OAuth 2.1 for secure access via the standard MCP OAuth flow:

1. On first use, you will be redirected to the Capital Equipment sign-in page
2. Sign in with your institutional credentials (Google, Microsoft, or email)
3. Authorize the AI assistant to act on your behalf
4. The OAuth token is managed automatically - no API keys needed

**Required Scopes**: `equipment:read`, `equipment:book`, `service-requests:write`, `profile:read`

**Token Lifetime**: 1 hour (refresh tokens issued automatically)

**No credentials need to be stored in your OpenClaw configuration.**

## Setup

Add the MCP server to your OpenClaw configuration:

```json
{
  "mcp": {
    "servers": [
      {
        "name": "capneteq-cesco345",
        "type": "sse",
        "url": "[https://capneteq.com/mcpServer/mcp](https://capneteq.com/mcpServer/mcp)"
      }
    ]
  }
}
```
