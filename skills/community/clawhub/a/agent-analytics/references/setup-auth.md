# Setup and auth reference

Use this file only when the compact skill needs more detail for setup, authentication, paid-tier handoff, or managed-runtime storage.

## Official CLI path

Use live Agent Analytics through:

```bash
npx --yes @agent-analytics/cli@0.5.37 <command>
```

Do not replace it with raw HTTP, local binaries, repo-local scripts, or MCP unless the user explicitly asks.

## Browser approval first

For Claude Code, Codex, Cursor, and local CLI runtimes:

```bash
npx --yes @agent-analytics/cli@0.5.37 login
npx --yes @agent-analytics/cli@0.5.37 create my-site --domain https://mysite.com
npx --yes @agent-analytics/cli@0.5.37 events my-site --event <first_useful_event> --days 7 --limit 20
```

The CLI opens browser approval and waits for the callback. Do not choose detached login only because an agent is running the shell.

## Detached approval

Use detached approval for Paperclip, OpenClaw, issue-based or headless runtimes, or failed callback environments:

1. Run `npx --yes @agent-analytics/cli@0.5.37 login --detached`.
2. Send the approval URL to the user.
3. Wait for the finish code.
4. Run the printed exchange command.
5. Continue with project setup and verification.

Do not ask for raw API keys.

## Managed-runtime storage

For OpenClaw and similar runtimes, store auth in a persistent workspace path:

```bash
export AGENT_ANALYTICS_CONFIG_DIR="$PWD/.openclaw/agent-analytics"
npx --yes @agent-analytics/cli@0.5.37 auth status
```

If environment persistence is uncertain, prefix every command:

```bash
AGENT_ANALYTICS_CONFIG_DIR="$PWD/.openclaw/agent-analytics" npx --yes @agent-analytics/cli@0.5.37 projects
```

`--config-dir "$PWD/.openclaw/agent-analytics"` is also valid. Ensure `.openclaw/` is gitignored. Never commit `.openclaw/agent-analytics/config.json`.

## Paid-tier handoff

Run the requested command first. If it returns `PRO_REQUIRED` or a free-tier cap:

```bash
npx --yes @agent-analytics/cli@0.5.37 upgrade-link --detached
```

Send the dashboard handoff. It confirms the same account as the CLI and opens payment. The browser link uses a fixed reason and excludes full commands and private query data; keep the original command in the agent session. After the user confirms upgrade:

```bash
npx --yes @agent-analytics/cli@0.5.37 whoami
```

Then rerun the blocked command. Use `upgrade-link --wait` only when keeping the shell polling is intentional.
