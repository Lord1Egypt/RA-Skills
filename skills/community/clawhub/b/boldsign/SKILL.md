---
name: boldsign
description: BoldSign e-signature platform API integration with managed OAuth. Send documents for signature, manage documents, create embedded signing links, and track document status. Use this skill when users want to send contracts for e-signature, list signed documents, create custom fields, or manage document workflows in BoldSign.
---

# BoldSign

![BoldSign](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/boldsign.png)

BoldSign is an e-signature platform for sending, signing, and managing electronic documents. This integration lets you send documents for signature, track document status, manage brands and custom fields, and create embedded signing experiences through ClawLink's hosted OAuth flow.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect BoldSign |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect BoldSign |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────>│   ClawLink   │────>│  BoldSign API    │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
```

## Install

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

## Quick Start

1. **List your documents** -- `boldsign_document_list`
2. **Send a document for signature** -- `boldsign_document_send`
3. **Check API credits** -- `boldsign_plan_get_api_credits_count`

## Authentication

ClawLink handles OAuth automatically. When you connect BoldSign through the dashboard, ClawLink obtains and refreshes tokens on your behalf. No API keys needed.

Connect at: https://claw-link.dev/dashboard?add=boldsign

## Connection Management

- **List connections**: `clawlink_list_integrations`
- **Verify connection**: `clawlink_list_tools --integration boldsign`
- **Reconnect**: Visit https://claw-link.dev/dashboard?add=boldsign

## Security & Permissions

Read operations (listing documents, brands, credits) are safe. Write operations (sending documents, creating custom fields) require confirmation. Destructive operations (removing document authentication) are marked high-impact and require explicit approval.

## Tool Reference

### Document Operations

| Tool | Description | Mode |
|------|-------------|------|
| `boldsign_document_list` | List documents in My Documents with filters | Read |
| `boldsign_document_behalf_list` | List documents sent on behalf of users | Read |
| `boldsign_document_team_list` | List team documents with optional filters | Read |
| `boldsign_document_send` | Send a document for eSignature | Write |
| `boldsign_document_edit_beta` | Edit a draft or sent document (beta) | Write |
| `boldsign_document_extend_expiry` | Extend a document's expiry date | Write |
| `boldsign_document_remove_authentication` | Remove signer authentication from a document | Write |

### Brand Operations

| Tool | Description | Mode |
|------|-------------|------|
| `boldsign_brand_get` | Get brand details by brand ID | Read |
| `boldsign_brand_list` | List all brands in the account | Read |

### Custom Field Operations

| Tool | Description | Mode |
|------|-------------|------|
| `boldsign_custom_field_create` | Create a brand-scoped custom field | Write |
| `boldsign_custom_field_edit` | Edit an existing custom field | Write |

### Embedded Signing Operations

| Tool | Description | Mode |
|------|-------------|------|
| `boldsign_embedded_request_create_link` | Create an embedded request link for in-app signing | Write |

### File Operations

| Tool | Description | Mode |
|------|-------------|------|
| `boldsign_file_upload` | Upload a file for use in other BoldSign actions | Write |

### Plan & Billing Operations

| Tool | Description | Mode |
|------|-------------|------|
| `boldsign_plan_get_api_credits_count` | Get remaining API credits count | Read |

## Code Examples

**List documents**
```json
{
  "tool": "boldsign_document_list",
  "args": { "page": 1, "pageSize": 20 }
}
```

**Send a document for signature**
```json
{
  "tool": "boldsign_document_send",
  "args": {
    "title": "Service Agreement",
    "signers": [{ "name": "John Doe", "emailAddress": "john@example.com" }],
    "files": [{ "fileUrl": "https://example.com/contract.pdf" }]
  }
}
```

**Create embedded signing link**
```json
{
  "tool": "boldsign_embedded_request_create_link",
  "args": {
    "title": "NDA",
    "signers": [{ "name": "Jane Smith", "emailAddress": "jane@example.com" }]
  }
}
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm `boldsign` is connected.
2. Call `clawlink_list_tools --integration boldsign` to see the live catalog.
3. Use `boldsign_document_list` to find existing documents.
4. Use `boldsign_brand_list` to see available brand configurations.

## Execution Workflow

```
Read path:  User asks "Show my documents"         -> boldsign_document_list
Write path: User asks "Send contract for signing"  -> Confirm -> boldsign_document_send
```

## Notes

- Documents can only be edited while in draft status or before finalization.
- The `boldsign_file_upload` tool is a helper that returns a key used by other tools (like brand logo upload).
- Embedded request links are useful for integrating signing directly into your application.
- API credit consumption depends on your BoldSign plan.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | BoldSign integration not connected |
| Missing connection | Authenticate via https://claw-link.dev/dashboard?add=boldsign |
| 403 Forbidden | Insufficient permissions or expired credits |
| Document not found | Invalid document ID or document does not belong to your account |

## Troubleshooting

### Tools Not Visible
Run `clawlink_list_tools --integration boldsign` to confirm the connection is active.

### Document Send Fails
Ensure the file URL is publicly accessible. Check that signer email addresses are valid.

## Resources

- BoldSign API Docs: https://developers.boldsign.com/
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=boldsign
- ClawLink Docs: https://docs.claw-link.dev/openclaw

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=boldsign)** -- an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)
