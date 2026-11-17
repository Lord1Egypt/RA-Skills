# Going live

**Live mode contacts real people and charges the user's real card.** Each invitation goes from the user's account to a real person. When someone books a call or completes an answer, the card is charged that person's offer plus Instant Expert's fee, up to the total cap in the order preview, and sending places one authorization hold for the largest single offer, fee included. Before every live send, the agent must show the user the order preview and send only after the user explicitly approves it.

Test mode is a separate sandbox with fictional people and a Stripe test card. To ask real people, the user connects their own Instant Expert account through the MCP server at `https://instant.expert/mcp` (Streamable HTTP, OAuth 2.1 sign-in, no API key). Nothing from test mode carries over.

## 1. Connect the server

### Claude Code

```bash
claude mcp add --transport http --scope user instant-expert https://instant.expert/mcp
```

Then run `/mcp`, pick `instant-expert` and choose **Authenticate**. Claude Code opens the sign-in page in the browser. New tools appear after the sign-in; if they don't, restart Claude Code.

### OpenClaw

OpenClaw connects to remote MCP servers natively ([docs](https://docs.openclaw.ai/cli/mcp/transports)). Save the server with OAuth, then sign in:

```bash
openclaw mcp set instant-expert '{"url":"https://instant.expert/mcp","transport":"streamable-http","auth":"oauth","oauth":{"scope":"email profile"}}'
openclaw mcp login instant-expert
openclaw mcp doctor instant-expert --probe
```

`openclaw mcp login` prints a sign-in link; the user opens it, signs in to Instant Expert and approves. Keep the scope to `email profile`: Instant Expert refuses `openid`. With Gateway hot reload on, the tools appear on the next turn; otherwise restart the Gateway.

### Claude (claude.ai and Claude Desktop), Cursor, VS Code, Codex and others

Follow https://instant.expert/docs/mcp#connect. Codex needs `scopes = ["email", "profile"]` in its config, because Instant Expert refuses the `openid` scope.

## 2. Sign in and allow paid sending

The user signs in on instant.expert and approves the connection. A new connection can search, import, draft and read replies, but can't place paid orders. To let the agent place orders that charge their card, the user also:

1. ticks **Allow paid requests from this assistant** on the consent screen, or turns it on later at https://instant.expert/settings/connections, and
2. adds a card at https://instant.expert/settings/requesting?tab=account. Saving a card charges nothing. Card details never go through chat.

With paid sending on, the agent must still send only after the user approves the exact order preview. Without it, the agent prepares drafts and the user sends them from https://instant.expert/requests.

## 3. Use the live tools

Run the same flow as in test mode. Two differences:

- Real people take hours to days to answer. Check `list_requests` or `get_request` when the user asks, or on a schedule, instead of polling in a loop.
- `prepare_request_order` may return `status: "action_required"` with `blockers` and an `action_url`. Give the user `next_step` as written: one visit to that link fixes a missing card, the paid-sending permission and empty booking hours. Then call `prepare_request_order` again and show the new preview.

| Blocker | What it means |
| --- | --- |
| `send_permission_required` | Paid sending is off for this connection |
| `payment_method_required` | No saved card |
| `availability_required` | A call needs booking hours and the saved ones are empty |
| `select_saved_card` | Several cards and no default: ask which one, then pass its `payment_method_reference` |
| `spending_cap_required` | Pass `max_spend_cents` to `prepare_request_order` |

If the bank asks for verification, `send_requests` returns `payment_action_required` with a `review_url`; the user finishes there and nothing is sent until then.
