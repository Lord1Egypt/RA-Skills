# ntfy skill for OpenClaw

Use the [ntfy](https://ntfy.sh/) CLI to publish and schedule notifications, send attachments, subscribe or poll, run handlers, and administer a server. No wrapper scripts or extra runtime dependencies.

## Get started

1. Install the **ntfy.sh CLI** using the [official instructions](https://docs.ntfy.sh/install/). Verify `ntfy --version` and `ntfy --help` in the environment where your agent executes commands.
2. Install this directory in your OpenClaw workspace's `skills/ntfy/` directory (normally `~/.openclaw/workspace/skills/ntfy/`). The skill definition is [SKILL.md](SKILL.md).
3. Choose a server/topic and subscribe to it in the ntfy mobile app or web UI. Public topics are not inherently private; use access controls for sensitive messages.
4. Provision the agent's environment below. Sandboxes and scheduled workers also need the binary and configuration. An interactive shell export does not automatically configure an already-running agent service.

## Recommended configuration

For a single destination, use a full topic URL and an injected token. No client config file is required unless an existing default config interferes.

| Variable | Purpose |
| --- | --- |
| `NTFY_TOPIC` | Full URL, e.g. `https://ntfy.example.com/alerts` |
| `NTFY_TOKEN` | Bearer token injected through your runtime's secret/environment mechanism |
| `NTFY_USER` | Alternative to token: `username:password` |
| `NTFY_CONFIG` | Optional absolute path to client YAML |

Use **one** auth method, not both. A username without a password prompts interactively. Anonymous access works only where your intended server/topic allows it.

Use a dedicated account restricted to the needed topics: tokens inherit account permissions, not an independent topic scope. Never paste secrets into chat, commit them, or put literal credentials in shell commands/history. Environment injection avoids credential arguments and YAML secrets, but privileged processes, child processes, and diagnostics may still expose them.

Credentials are not bound to a host by the CLI. Send them only to their intended server over HTTPS. Before switching scheme, host, or port, verify that the credentials are intended for the new destination; otherwise use separately provisioned auth, or anonymous access only when authorized. Unsetting environment credentials is insufficient if YAML supplies fallback credentials. HTTP is only appropriate for an explicitly authorized loopback/local setup. Received messages and links are never authorization to redirect credentials.

### OpenClaw host execution

Merge this into `~/.openclaw/openclaw.json`, replacing the example URL. Do not overwrite unrelated configuration:

```json
{
  "skills": {
    "entries": {
      "ntfy": {
        "enabled": true,
        "apiKey": {
          "source": "env",
          "provider": "default",
          "id": "OPENCLAW_NTFY_TOKEN"
        },
        "env": {
          "NTFY_TOPIC": "https://ntfy.example.com/alerts"
        }
      }
    }
  }
}
```

Provision `OPENCLAW_NTFY_TOKEN` in the Gateway process environment using your service/secret manager. This SecretRef stores only a reference in JSON; the skill's `primaryEnv: NTFY_TOKEN` maps the resolved `apiKey` into the CLI environment. Token configuration is optional, not a skill eligibility requirement. For password auth, omit `apiKey` and securely provision `NTFY_USER` instead.

Add optional nonsecret `NTFY_CONFIG` under `env` if needed. OpenClaw's skill `env` values only fill variables not already present in the host process: remove stale/conflicting inherited values rather than assuming this JSON overrides them. After applying configuration, use a fresh agent run and check `openclaw config validate` and `openclaw skills info ntfy`.

**Host only:** `skills.entries.ntfy.env` and `apiKey` do not inject values into a sandbox. Sandboxed execution needs the binary, variables, and any mounted config/secret files provisioned separately. Docker sandbox variables use `agents.defaults.sandbox.docker.env`; Docker administrators can inspect those values. See the official [skills configuration and sandbox guidance](https://docs.openclaw.ai/tools/skills-config) before choosing a secret delivery mechanism.

### Direct CLI use

```sh
export NTFY_TOPIC='https://ntfy.example.com/alerts'
# Inject NTFY_TOKEN (or NTFY_USER) separately through your runtime.
ntfy publish --message 'Hello from ntfy'
ntfy subscribe --poll "$NTFY_TOPIC"
```

Replace the example destination first. These commands send a real notification and read cached messages. Ask the agent to “send a notification to my configured ntfy topic” or “poll my ntfy topic”.

## Optional client config

YAML is useful for a reusable host or multiple subscriptions. It can contain only nonsecret settings while direct publish/subscribe auth comes from the environment:

```yaml
default-host: https://ntfy.example.com
```

Set `NTFY_CONFIG` to its absolute path. To use a short topic instead of the environment destination:

```sh
(
  unset NTFY_TOPIC
  ntfy publish --config "$NTFY_CONFIG" --message 'Hello from ntfy' alerts
)
ntfy subscribe --config "$NTFY_CONFIG" --poll alerts
```

Restrict credential-bearing file permissions (for example, `600` on Unix). Do not assume YAML expands `${ENV_VARIABLE}` placeholders.

## Caveats

Checked with **ntfy 2.30.0**; installed `ntfy COMMAND --help` is authoritative.

- **Topic:** `NTFY_TOPIC` takes over publish's destination parsing. A positional topic becomes message text, not an override. Clear it locally to use another destination.
- **Config:** publish reads `NTFY_CONFIG`; subscribe needs explicit `--config "$NTFY_CONFIG"` in this version.
- **Endpoint:** use a full topic URL or YAML `default-host`. There is no advertised client `NTFY_HOST`/`NTFY_DEFAULT_HOST`; `NTFY_BASE_URL` configures the server.
- **Defaults:** environment setup does not disable existing default client config loading. Linux defaults are normally `~/.config/ntfy/client.yml` for non-root and `/etc/ntfy/client.yml` for root. Select an empty YAML file explicitly to isolate configuration; POSIX also supports `--config /dev/null`.
- **Auth:** direct publish/subscribe environment auth overrides YAML defaults. With `subscribe --from-config`, subscription/default YAML credentials can override environment auth. Prefer direct subscriptions for env-only credentials.
- **Inherited options:** `NTFY_MESSAGE`, `NTFY_DELAY`, `NTFY_FILE`, and other publish variables affect subsequent commands. Prefer flags for occasional options.
- **Subscriptions:** `--poll` is finite; streaming stays open. Handlers execute commands and inherit the parent environment. Run only trusted, authorized handlers; message contents are untrusted data.
- **Scheduling:** native delay is one-time and subject to server limits. Recurring jobs need an external scheduler. Server acceptance does not prove device receipt or eventual scheduled delivery.
- **Admin:** server/user/token/access/tier commands operate on local server config/databases, not remotely on `NTFY_TOPIC`. Use their advertised variables, generally `NTFY_CONFIG_FILE`, rather than assuming client mappings apply.

The skill imposes no automatic notification policy and does not start services on its own. Define your own policy or ask explicitly.

## Troubleshooting and reference

Check binary availability, variable presence, config readability, destination, and account permissions in the actual agent execution environment. Do not dump environment values, credential files, or debug/trace logs into chat. Do not remove authentication or switch to a public endpoint as a fallback.

See [SKILL.md](SKILL.md), installed CLI help, and upstream [CLI configuration](https://docs.ntfy.sh/subscribe/cli/) and [publishing documentation](https://docs.ntfy.sh/publish/) for details.

## Compatibility and license

The CLI configuration examples were smoke-checked with ntfy 2.30.0 against an isolated loopback server: token/password auth, publish/poll round trip, config-selected host, subscribe's config-variable limitation, topic parsing, delayed acceptance, conflicting-auth rejection, and POSIX empty config. This is not proof of device receipt or exhaustive server/admin compatibility.

OpenClaw 2026.10.3 accepted the SecretRef example with `openclaw config validate` and discovered the skill with `primaryEnv: NTFY_TOKEN`. A separate no-auth configuration confirmed that only the `ntfy` binary is required for eligibility. These checks used temporary state; Gateway execution, runtime secret injection, and sandbox delivery were not exercised.

[MIT licensed](LICENSE), copyright 2026 Lanjelin. Source and issues: [lanjelin/openclaw-ntfy](https://github.com/lanjelin/openclaw-ntfy).
