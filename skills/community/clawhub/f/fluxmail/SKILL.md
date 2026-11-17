---
name: fluxmail
description: Connect OpenClaw to self-hosted Fluxmail and work with Gmail, Outlook, and IMAP mailboxes through its MCP tools.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - fluxmail
    install:
      - kind: node
        package: fluxmail
        bins:
          - fluxmail
    homepage: https://fluxmail.ai/docs/quickstart
---

# Fluxmail

Use Fluxmail when the user wants an OpenClaw agent to read, search, draft, send, schedule, or organize mail in an existing Gmail, Outlook, or IMAP/SMTP mailbox.

## Set up

Fluxmail runs on the user's computer or server. If it is not installed, follow the [Fluxmail quickstart](https://fluxmail.ai/docs/quickstart). A local installation uses `npm install -g fluxmail`, then `fluxmail setup` and a provider-specific mailbox connection. Let the user complete password and provider consent steps.

For a local OpenClaw installation, configure Fluxmail as a stdio MCP server with read-only access first:

```bash
openclaw mcp add fluxmail --command fluxmail --arg stdio --arg --profile --arg read-only
openclaw mcp probe fluxmail
```

If the user wants drafting, sending, or mailbox changes, review the [Fluxmail permission profiles](https://fluxmail.ai/docs/permissions) with them before changing access. For a remote Fluxmail server, use its Streamable HTTP `/mcp` endpoint and a scoped Fluxmail API key. Follow the [MCP connection guide](https://fluxmail.ai/docs/connect-an-mcp-client); keep the key out of chat, logs, and the skill files.

## Work with mail

- Use Fluxmail MCP tools available in the current session. Check which account and permission scope they use before acting across multiple mailboxes.
- Search or list messages before fetching full threads. Summarize only the messages needed for the user's request.
- Create drafts for review when the user asks for help writing mail. Confirm recipients and content before sending, forwarding, scheduling, deleting, or making bulk mailbox changes.
- If a tool is missing, check the MCP connection and its permission profile. Do not work around a denied permission.

Fluxmail's Personal plan supports one member and three mailboxes. Paid plans raise those limits and add team access. Fluxmail software is source available under the Elastic License 2.0. See [plans and licensing](https://fluxmail.ai/docs/teams-and-plans) for details.
