---
name: auto-message
description: "Find a texting assistant for your goals in AutoMessage's public catalog. Use it for automessage assistant through AutoMessage's MCP server."
---

# AutoMessage

Find a texting assistant for your goals in AutoMessage's public catalog.

## Connect

Add AutoMessage's MCP server: https://textwithassistants.com/mcp (Streamable HTTP, no sign-in).

## Offers

### AutoMessage assistant

Find a texting assistant in AutoMessage's fixed public catalog when the user asks which assistant covers a topic. Accepts a supported topic and returns its catalog id. get_assistant returns the assistant's name, specialty and signup page. The tools cannot send texts, enroll users, access accounts or read conversations.

1. Call `find_assistant`. It returns an id.
2. Call `get_assistant` with the id. The catalog entry is available immediately.
3. Give the person the result and its link.
