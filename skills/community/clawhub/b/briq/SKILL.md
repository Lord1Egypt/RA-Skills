---
name: briq
description: Run real services and sandboxes on briq (briq.cloud) for the work at hand. A sandbox is a microVM with Python, Node, git and a shell, for scripts, tests and builds that should not run on the user's machine. A service is Postgres, MySQL, Redis, MongoDB, Qdrant, a headless Chrome, DuckDB dashboards, an app from a GitHub repo or any Docker image, with connection strings and HTTPS preview URLs. Use when the user wants a real database for a project, tests against real services instead of mocks, code run somewhere other than their computer, a preview link for an app, a copy of a database before a risky change, or mentions briq. Also covers connecting briq: adding its MCP server, signing the user in from a laptop, a server or a chat app, and the CLI for scripts and CI.
license: MIT
compatibility: Needs network access to api.briq.cloud and a briq account (the user signs in once). Works in any agent with MCP; the CLI needs Node 22.6 or later.
metadata:
  homepage: https://briq.cloud
  docs: https://briq.cloud/docs
---

# briq

briq runs services and sandboxes for agents, each on its own microVM, through one MCP server:
`https://api.briq.cloud/mcp` (Streamable HTTP, OAuth). Every answer about a briq shows its cost so
far and when it goes to sleep.

## Connect, if the briq tools are missing

You have the tools when `briq_run`, `briq_exec` and `briq_quota` are available. If not:

1. Add the MCP server for all projects (user scope): name `briq`, URL
   `https://api.briq.cloud/mcp`. Your client's exact steps: https://briq.cloud/docs/setup/clients.md
2. Get the user signed in. They pick the team you work for and your budget; you never handle a
   password or a token.
   - On their computer: start your client's sign-in (`claude mcp login briq`,
     `codex mcp login briq`, `/mcp` then Authenticate), or call any briq tool.
   - On a server, in a container or a chat app: use your client's device-code login
     (Hermes: `hermes mcp login briq --flow device`), then send the user the link it prints:
     "Open this link to connect briq to your account: https://app.briq.cloud/connect?user_code=…".
3. Most clients load a new server only after a restart or a reconnect: tell the user.
4. Call `briq_quota`: it answers with the team, the credits and the limits.

All the details and troubleshooting: https://briq.cloud/docs/setup/agents.md

## Run code in a sandbox

```text
briq_run({ recipe: "sandbox" })
→ bq_7kq2m9x1p4ab sandbox running · WORKDIR=/work
briq_exec({ briq: "bq_7kq2m9x1p4ab", cmd: ["sh", "-c", "cd /work && git clone --depth 1 https://github.com/acme/shop . && npm ci && npm test"], async: true })
→ ex_9p2kd7mq1x4r running
briq_exec_result({ briq: "bq_7kq2m9x1p4ab", exec: "ex_9p2kd7mq1x4r" })
→ exited 1 after 2m · stdout: … 2 failed, 36 passed …
```

- A command that can take over a minute runs with `async: true`, then `briq_exec_result`.
- Files: `briq_files_put` and `briq_files_get`, 1 MB each way. Bigger: `git clone` or `curl` from
  inside.
- A credential goes in as a secret, never as plain text:
  `env: { TOKEN: { secret: "TOKEN", value: "…", scope: "boot" } }` for setup steps only, or with
  `hosts: ["api.example.com"]` so only requests to those hosts carry it.
  See https://briq.cloud/docs/guides/run-code-in-a-sandbox.md

## Run a service

```text
briq_run({ recipe: "postgres", stack: "shop" })
→ bq_… db running · DATABASE_URL=postgres://postgres:…@…internal:5432/app
briq_run({ recipe: "node", stack: "shop", checkout: { repo: "github.com/acme/shop" }, steps: [{ run: "npm ci" }], cmd: "npm start", expose: "private" })
→ bq_… web running · url: https://web-x2kd.briq.run/?briq_token=…
```

- `briq_catalog` lists every recipe and its fields: postgres, mysql, redis, mongo, qdrant,
  chrome, duckdb, sandbox, node, python, go, bun, ruby, rust, php, static, nginx, and more.
  Prefer a recipe to a bare image: it returns ready connection strings.
- Briqs in the same `stack` reach each other on a private network and sleep and wake together.
- `briq_expose` gives a port an HTTPS URL (`mode: "private"` carries a token, `"public"` opens
  it to anyone), or a TLS endpoint for a database client outside briq (`protocol: "postgres"`).
- `briq_fork` copies a briq or a whole stack with its disk: try a migration on the copy, keep
  the one that works.

## Spend with care

- A briq sleeps after its `sleep` window without use (`briq_set_sleep`: `"30m"`, `"3h"`, `"7d"`,
  `"never"`) and wakes on the next call or visit. Asleep, it keeps its disk and costs nothing.
- Destroy what you are finished with: `briq_destroy`.
- `payment_required`: the team has no credits. Tell the user (they confirm their email address
  or top up on the dashboard) and stop; retrying does not help.
- `quota_exceeded` or `plan_limit`: call `briq_quota`, then pick a smaller size or fewer briqs,
  or tell the user.

## Without MCP: the CLI

For a git hook, a CI job or a script, use the CLI. It has one command per tool, with the same
options:

```bash
npm install -g @briq-cloud/cli
briq login                      # prints a link for the user, like the device-code login
briq run sandbox
briq exec bq_7kq2m9x1p4ab npm test
```

In CI, set `BRIQ_API_KEY` (a key from the dashboard's Agents page) instead of `briq login`.
Every command: https://briq.cloud/docs/cli.md

## More

- Every tool, with an example: https://briq.cloud/docs/mcp/tools.md
- Every recipe: https://briq.cloud/cookbook.md
- `briq_docs` reads any docs page from inside your session.
- Something does not work as documented: `briq_feedback` reaches the people who build briq.
