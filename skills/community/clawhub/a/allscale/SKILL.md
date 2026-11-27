---
name: allscale
description: Work in the business dollar account that AllScale provides, through the hosted AllScale MCP server. Check balances and transactions, send invoices, create checkout links and prepare payouts that the merchant approves with a passkey.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://www.allscale.io/mcp
---

# AllScale

AllScale provides businesses with a global dollar account, with balances held and settled in USDC and USDT. This skill tells you how to connect to the AllScale MCP server and how to use its tools safely.

## Connect

The tools come from AllScale's hosted MCP server at `https://mcp.allscale.io/mcp` (Streamable HTTP, OAuth). No API key is needed. If the AllScale tools are not available, ask the user to run:

```bash
openclaw mcp set allscale '{"url":"https://mcp.allscale.io/mcp","transport":"streamable-http","auth":"oauth"}'
openclaw mcp login allscale
```

The second command prints a sign-in link. The user signs in to AllScale in the browser, then chooses one merchant account, an optional checkout store and the permissions to grant. Check the connection with `openclaw mcp doctor allscale --probe`.

The user needs an AllScale account, which businesses open at https://www.allscale.io. Connections can be removed in AllScale under Settings → Connected AI apps.

## Tools

Read:

- `whoami`: merchant, store and permission status. Call this first when a tool reports a permission problem.
- `wallet_list`: balances by asset and network.
- `transaction_list`, `transaction_get`: transactions, newest first, and one in detail.
- `invoice_list`, `invoice_get`: issued or received invoices.
- `claim_link_list`, `claim_link_get`: Claim Links and their status.

Write (needs write permission):

- `invoice_create_and_send`: creates a USDT or USDC invoice and emails it to the customer.
- `invoice_update`: updates an invoice's memo or extends an overdue invoice's due date.
- `checkout_link_create`: creates a one-time checkout link. Needs a checkout store selected at sign-in.

Payment preparation (passkey approval):

- `payment_prepare`: prepares a USDT or USDC transfer to a wallet address.
- `invoice_pay_prepare`: prepares payment of an invoice another business sent.
- `claim_link_prepare`: prepares a funded Claim Link.
- `pending_action_status`: checks the result of a prepared action.

## Rules

- Before any write or payment tool, show the user the details (recipient, amount, asset, network, due date) and get a clear yes.
- Payment tools only create a pending action. Funds move only after the merchant approves it in AllScale with a passkey. Never tell the user a payment was sent until `pending_action_status` confirms it.
- Never ask for or handle private keys, seed phrases, passwords or one-time codes. AllScale does not need them.
- If a tool reports missing permission, call `whoami`, tell the user which permission is missing, and ask them to reconnect with `openclaw mcp login allscale`.
