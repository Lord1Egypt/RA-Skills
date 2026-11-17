# Setup — OAuth vs publisher key

Wire the hosted MCP once. This skill is markdown + judgement only; it does not
ship binaries or scripts.

**Endpoint:** `https://app.artifactpublisher.com/mcp` (streamable HTTP)

## 1. OAuth (preferred)

When the client supports browser consent (Cursor, Claude Connect, ChatGPT Apps,
etc.):

1. Register `https://app.artifactpublisher.com/mcp` as the remote MCP URL.
2. Complete consent in the browser (PKCE).
3. Never ask the user to paste an access token into chat.
4. Tokens stay in the client secret store.

Cursor example (`mcp.json` — URL only, no headers):

```json
{
  "mcpServers": {
    "artifact-publisher": {
      "url": "https://app.artifactpublisher.com/mcp"
    }
  }
}
```

Then Settings → MCP → Connect / Login.

## 2. Publisher key (advanced / headless)

Practical for Hermes, OpenClaw operators, and always-on agents that cannot do
browser OAuth:

1. Open https://artifactpublisher.com/account/ and mint a publisher key (shown
   once). Store in the client secret store or env — **never echo in chat**.
2. Set `ARTIFACT_PUBLISHER_KEY`.
3. Send `Authorization: Bearer ${ARTIFACT_PUBLISHER_KEY}` (or the client’s env
   interpolation form).

### Hermes

```bash
hermes mcp add artifact-publisher --url https://app.artifactpublisher.com/mcp
```

Hand-edited `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  artifact-publisher:
    url: "https://app.artifactpublisher.com/mcp"
    headers:
      Authorization: "Bearer ${ARTIFACT_PUBLISHER_KEY}"
```

Reload with `/reload-mcp`. Keep the key out of chat and out of `SKILL.md`.

### OpenClaw

```bash
openclaw mcp set artifact-publisher '{"url":"https://app.artifactpublisher.com/mcp","transport":"streamable-http","headers":{"Authorization":"Bearer ${ARTIFACT_PUBLISHER_KEY}"}}'
```

Or in OpenClaw config (typical `~/.openclaw/config.json`):

```json
{
  "mcp": {
    "servers": {
      "artifact-publisher": {
        "url": "https://app.artifactpublisher.com/mcp",
        "transport": "streamable-http",
        "headers": {
          "Authorization": "Bearer ${ARTIFACT_PUBLISHER_KEY}"
        }
      }
    }
  }
}
```

### Claude Code

```sh
claude mcp add --transport http artifact-publisher https://app.artifactpublisher.com/mcp \
  --header "Authorization: Bearer ${ARTIFACT_PUBLISHER_KEY}"
```

## 3. Discovery without credentials

Keyless `initialize` / `tools/list` / `ping` work for discovery only. Publish
and workspace tools require OAuth or a key.

## 4. Desk

Mint and manage keys at https://artifactpublisher.com/account/. Keys are shown
once; only a hash is stored server-side.

## Explicit non-actions

- Do **not** run `clawhub skill publish` until Bobby/Simon greenlight
  (`docs/internal/skill-clawhub-checklist.md`).
- Do **not** claim `npx skills add ni3do/artifact-publisher` while the product
  repo is private (ADR 0025).
- Do **not** add a `scripts/` directory that downloads or runs binaries.
