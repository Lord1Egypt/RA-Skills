# Install Receipt in OpenClaw (v1.0.7)

Receipt uses OpenClaw's native remote MCP support. No custom plugin is required.

The skill provides these instructions and remains eligible before setup. The `receipt` MCP server
is a separate OAuth connection created during setup.

For a connection created before the provider-compatible tool-name deployment,
remove and reconnect the `receipt` MCP connection so OpenClaw rediscovers the
eight `receipt_` names. Do not change OAuth scopes or create a new Receipt
account.

## Execute the clean-profile bootstrap

Do not begin by describing a URL that does not exist. Use the local execution tool to run:

```bash
bash "{baseDir}/scripts/bootstrap-receipt.sh"
```

The script executes this verified OpenClaw `2026.7.1-2` sequence:

1. Run `openclaw mcp show receipt --json`.
2. If absent, configure `https://receiptprotocol.com/mcp` as streamable HTTP with OAuth, the
   `receipt_*` tool filter, and parallel calls disabled.
3. Apply the `receipt_*` filter to both new and existing Receipt connections.
4. Run exactly one bare `openclaw mcp login receipt`.
5. Extract the complete Receipt authorization URL from that command's output.
6. Refuse to show callback-helper instructions if no authorization URL was produced.

When the script prints a URL between `RECEIPT_AUTHORIZATION_URL_BEGIN` and
`RECEIPT_AUTHORIZATION_URL_END`, copy the complete URL into the user-visible response. Do not
refer to an authorization URL indirectly. Display the URL itself and then tell the user:

1. Open that complete URL and approve Receipt.
2. The browser may land on a `127.0.0.1` callback error. This is expected.
3. Copy the entire callback URL from the browser address bar.
4. Do not start another login.
5. Do not paste the callback URL or authorization code into Agent chat.
6. Do not send a conversational acknowledgement after approval.

On macOS, complete that same attempt from the local shell without exposing the code:

```bash
bash ~/.openclaw/workspace/skills/get-with-receipt/scripts/complete-oauth-from-clipboard.sh
```

The helper reads the callback from `pbpaste`, extracts only the code, and runs the verified
`openclaw mcp login receipt --code <code>` form. It does not start a new login or write the callback
to disk.

On other systems, extract the `code` query parameter from the newest callback locally and run this
in the same shell:

```bash
openclaw mcp login receipt --code '<code-from-current-callback>'
```

Do not put the code in ordinary Agent chat. Codes are single-use and expire after 10 minutes.
Continue only after the CLI says `MCP OAuth credentials saved for "receipt".`

If exchange returns `invalid_grant`, say exactly:

> This authorization attempt is stale or mismatched. Start one new login, approve only its newest
> URL, copy its callback, and complete that same attempt. Do not run another bare login in between.

Do not automatically retry, loop, or treat browser approval alone as success.

## Verify after authorization

```bash
openclaw mcp status --verbose
openclaw mcp doctor receipt --probe
openclaw mcp probe receipt --json
```

Confirm `oauth: tokens=yes client=yes`, no diagnostics, and exactly the eight tools listed in
`SKILL.md`. OpenClaw may display provider-safe aliases, but they must map one-to-one to the eight
source `receipt_*` names. No seller-specific or `receipt_labs.*` tool may appear.

After verification, complete the bounded first-outcome sequence in `SKILL.md`: account, discovery,
one web-search quote at or below $0.10, disclosure, and—only when the owner selected the launch
credit option during OAuth—one purchase with `use_activation_credit: true`. If the owner opted out
or credit is unavailable, return the quote and stop before purchase.

Receipt setup completes when the agent has returned its first governed outcome and signed Receipt,
unless the owner opts out of the activation purchase.

Do not add a static `Authorization` header or copy provider keys into OpenClaw. Set Receipt to ask
every purchase, with a per-call limit of at most $1 and a daily limit of at most $5. The one
OAuth-authorized sponsor-funded activation is the only setup exception. Add no automatic seller
rules.

If any seller-specific tool appears, stop and remove that connection.
