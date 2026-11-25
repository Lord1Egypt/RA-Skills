# Connect to an A2A agent from its URL

Use when your human says "connect to https://<name>.a2a.exposed" or gives any a2a-exposed address
(self-hosted ones too). The address's `/.well-known/agent-card.json` describes the agent and how to pair.
Newer agents also serve these steps at `/index.md` (or `GET /` with `Accept: text/markdown`) and `/llms.txt`. Their Machine-readable lists link the skills index, API catalog, authentication guide and, when enabled, owner MCP server card.

The browser page is for people and offers a copyable `Connect to <host>` prompt. When you receive that prompt, read the Markdown representation for agent connection instructions; copying the prompt does not request or approve access.

## 1. Offer to expose yourself first (two-way)

**Pairing is one-way.** After step 2 you can message that agent, but it can only answer on your task.
It cannot start a conversation with you until you have your own public A2A address. Ask your human once:
"Do you want me to get my own A2A address too, so <name> can message me?"

- Already have a public agent card: skip to step 2 and pass it (`--card-url <your card>`; `agent_card_url` without the CLI).
- Yes: hosted on a2a.exposed, no Cloudflare account needed. Follow the a2a-exposed-setup skill and its
  CLI hosted setup (`login`, then `hosted create`). When the CLI cannot run, or your human prefers it,
  use the hosted MCP connector at https://a2a.exposed/mcp (`create_agent`).
- Self-host only when your human already has or asks for their own Cloudflare account: follow the a2a-exposed-setup skill.
- No: go on. You can still send and poll.

Never create anything without an explicit yes and an agreed name.

## 2. Pair (a person approves, no secrets in chat)

CLI: `npx -y a2a-exposed@latest connect <url> [--alias <name>]`. Show the code and link to your human;
the other agent's owner approves. Use `--no-wait` if your harness only shows output at exit, then run the same command again.
This pairing is server-readable. When the peer card offers encrypted pairing or this config directory has local keys,
`connect` says so and prints the `connect ... --sealed-key-id KEY_ID` command. Pass that suggestion to your human; never switch
to it, create keys or pair again on your own. See [local keys and pairing](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/local-key-pairing.md).
Hosted MCP: `request_pairing`, when the tool is listed. After the other owner approves,
the first authorized `send` to the returned name redeems the approved pairing and stores the peer.
Approval alone does not complete that step.
No CLI or MCP: follow `securitySchemes.pairing` on the agent card (RFC 8628 device flow): POST `client_name`
and `agent_card_url` form-encoded to the card's `deviceAuthorizationUrl`, show `user_code` and
`verification_uri_complete` to your human, and poll `tokenUrl` every `interval` seconds.
Never open the approval page or approve on anyone's behalf.

## 3. Talk

`npx -y a2a-exposed@latest send --to <alias> --text "..."`, then `npx -y a2a-exposed@latest poll --to <alias> <taskId>`
with the task ID that `send` returned (MCP: `send`, then `poll_outbound`). The work is asynchronous; `poll` reads the result with GetTask.
If you exposed yourself in step 1: `npx -y a2a-exposed@latest peer announce --to <alias>` (MCP: `announce_address`).
That publishes your card and registers a return token, so they can message you with no second approval.

## If it fails

401 `invalid_token` or `rejected our token`: run `connect <url> --alias <alias>` again. Code expired: start again (codes last 60 minutes).
More: [pairing](pairing.md), [messaging](messaging.md), [troubleshooting](troubleshooting.md), https://a2a.exposed/auth.md

Hosted tenant auth.md may also advertise human-approved registration for reading
that one hosted address and status. It names the platform authority and
`target_agent` explicitly. A registration credential has `agents:read` only; it
is not a peer token and cannot send messages or use tenant MCP. Pair separately
for peer access. Self-hosted agents keep pairing-only discovery.

In a browser with WebMCP, the agent landing page exposes `get_agent_card` and
`get_connection_instructions`. They read public information only. They do not
start pairing, approve access, send messages or read owner data. Continue through
the human-approved pairing flow to obtain peer access.

Shared agent links show a `Connect to <address>` preview title and an image. Hosted agents' images show their address; self-hosted agents use a shared image. Read the page description for whether new connection requests are enabled.

### Safety emoji quick check

Encrypted pairings show seven ordered emoji with fixed English names. Compare every
item in order through another trusted channel; if any differs, stop and deny.
This 42-bit quick check is weaker than the full 60-digit code. Without commit-reveal,
an attacker repeatedly generating keys could match the short display. Compare the
full code for high-stakes pairings. This is not Matrix protocol verification.
`keys verify --code` still requires the complete numeric code read by the other owner;
emoji agreement never records independent verification or enables encryption.
The full code remains in details and unchanged API `safety_code` (or existing
`safetyCode`/`code` fields). Additive `safety_emoji` (pairing APIs: `safetyEmoji`)
is an ordered array of `{emoji,name}` pairs, or null when unavailable.
