---
name: buffer-mcp
description: Safely draft, review, inspect, and explicitly approved schedule/publish workflows through Buffer's official MCP server. Use when an operator has already configured Buffer MCP in their MCP client or OpenClaw runtime and wants approval-first social media workflow guidance for Buffer accounts, organizations, channels/profiles, drafts, queues, scheduled posts, or publishing.
metadata:
  openclaw:
    emoji: "🗓️"
    homepage: https://forge.rayhollister.com/rayhollister/buffer-mcp
    envVars:
      - name: BUFFER_MCP_AUTHORIZATION
        required: false
        description: Optional local name for a Buffer MCP bearer credential if your MCP client maps credentials from environment variables. Prefer your MCP client's secret store or OpenClaw SecretRef.
---

# Buffer MCP

Use Buffer's official Streamable HTTP MCP server with an approval-first social publishing workflow.

This skill contains instructions only. It does not include executable helper scripts, install-time code, network clients, credential writers, or background automation.

## Configure Buffer MCP

Buffer's MCP settings are:

```text
URL: https://mcp.buffer.com/mcp
Header name: Authorization
Header value: Bearer <credential>
```

Get the credential from Buffer's MCP integrations page:

```text
https://publish.buffer.com/settings/integrations/mcp
```

Store the credential in your MCP client's secret store or in OpenClaw SecretRef. Do not paste it into chat, commit it to a repository, or save it as plaintext config.

If your client supports MCP server configuration, add Buffer as a Streamable HTTP MCP server using the official URL above. Keep that endpoint unless you intentionally trust another server.

## Safe workflow

1. Draft or review copy in chat first.
2. Use Buffer MCP read/list tools to identify the correct account, organization, and channel/profile.
3. Before any write, confirm all of the following in the current conversation:
   - Buffer account or organization,
   - target channel/profile,
   - action: draft, queue, schedule, publish, update, or delete,
   - final post text and media,
   - schedule time and timezone when relevant,
   - whether the action will become public immediately.
4. Do not create, schedule, publish, update, or delete anything unless the user explicitly approves that exact write in the current conversation.
5. Prefer drafts for tests. If the Buffer tool schema supports draft creation, use the draft option instead of publishing or scheduling.
6. After any approved write, summarize the result with the Buffer post/idea ID, status, target channel, and whether anything was published or scheduled.

## Approval language

Approval must be specific. Acceptable approval looks like:

```text
Approved: schedule this exact post for WJCT on LinkedIn at 2026-05-15 09:00 America/New_York.
```

Do not treat broad statements like "looks good" or "go ahead with Buffer" as approval unless the account, channel, action, content, and timing are already unambiguous in the current conversation.

## Security model

- This skill is no-code documentation for using Buffer's official MCP endpoint; it does not execute local commands or make network requests by itself.
- Buffer credentials grant delegated access according to Buffer's permissions. Store them in a secret manager or SecretRef and rotate them if exposed.
- Buffer write tools can affect public or scheduled social content. Use explicit current-conversation approval for each write.
- Only send post text, media references, channel IDs, and scheduling details to Buffer when that is expected for the requested workflow.

## Content guidance

- Match the organization's voice and platform norms.
- Keep captions clear, specific, and human.
- Avoid invented facts, fake urgency, and generic hype.
- Include alt text suggestions when media is attached or requested.
- Respect platform-specific requirements shown by the MCP tool schema, especially media requirements for visual/video platforms.
