# Inbound tokens

Issue or rotate tokens only when the user asks. All access changes require user approval. One label/token per peer; never share one token among several peers. The label is who sent a task. Prefer pairing (`connect`, then your human approves) over issuing a token by hand. Get the card URL with `npx -y a2a-exposed@latest url` plus `/.well-known/agent-card.json`. Share a token with the card URL only on a channel the user approves.

| Command | Effect |
| --- | --- |
| `npx -y a2a-exposed@latest token issue <label>` | Prints a new token (`a2aow_...`) once on stdout. Only its SHA-256 hash is stored. Fails when the label is already active |
| `npx -y a2a-exposed@latest token list` | Labels, creation time, active or revoked, and `via pairing: code ...` for tokens created by pairing |
| `npx -y a2a-exposed@latest token revoke <label>` | Takes effect immediately: the peer gets 401, including a push reply to a task already sent. An unknown or already revoked label exits 1 |
| `npx -y a2a-exposed@latest token rotate <label>` | Issues a new token and invalidates the old one |

Someone with only the official `a2a` CLI cannot pair. When the user approves a token for them, point them to [Use with the official A2A CLI](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/official-a2a-cli.md#with-only-the-official-cli): a dedicated mode-600 file with the card URL and `A2ACLI_AUTH=Bearer <token>`, passed with `--config`. Never the global `~/.config/a2a-cli/.env`, which sends the token to every agent.
