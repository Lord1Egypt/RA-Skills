# cf-workers-logs

A [ClawHub](https://clawhub.ai) skill for querying Cloudflare Workers Observability logs from Claude Code.

Query logs from Workers, Durable Objects, Workflows, Queues, and Cron Triggers — all from your terminal.

## Install

```bash
clawhub install cf-workers-logs
```

## Setup

You need two environment variables:

| Variable | Description |
|----------|-------------|
| `CF_OBSERVABILITY_ACCOUNT_ID` | Your Cloudflare Account ID |
| `CF_OBSERVABILITY_API_TOKEN` | API token with Workers Observability permission |

### 1. Get your Account ID

1. Log in to the [Cloudflare dashboard](https://dash.cloudflare.com)
2. Go to **Workers & Pages** in the sidebar
3. Find **Account ID** in the right-side **Account details** section — click to copy

### 2. Create an API Token

1. Go to **My Profile > API Tokens** in the Cloudflare dashboard
2. Click **Create Token**
3. Choose **Create Custom Token**
4. Configure:
   - **Token name**: e.g. `workers-observability-read`
   - **Permissions**: `Account` / `Workers Observability` / `Edit`
   - **Account Resources**: select your account
5. Click **Continue to summary** → **Create Token**
6. Copy the token immediately (shown only once)

> **Note**: The permission level needs to be **Edit** (not Read) to run queries via the API.

### 3. Configure environment variables

**Option A: Project `.env` file** (recommended, per-project isolation)

```bash
# .env (make sure it's in .gitignore)
CF_OBSERVABILITY_ACCOUNT_ID=your-account-id
CF_OBSERVABILITY_API_TOKEN=your-api-token
```

**Option B: Shell profile** (`~/.zshrc` or `~/.bashrc`, shared across all projects)

```bash
export CF_OBSERVABILITY_ACCOUNT_ID=your-account-id
export CF_OBSERVABILITY_API_TOKEN=your-api-token
```

The skill searches for credentials in this order:
1. Shell environment variables
2. `.env` / `.env.*` files in the project directory

## Usage

```
/cf-workers-logs                                    # recent errors (last 1h)
/cf-workers-logs worker=my-api level=error          # errors from a specific worker
/cf-workers-logs entrypoint=MyDO last=30m           # Durable Object logs
/cf-workers-logs event=alarm                        # alarm-triggered logs
/cf-workers-logs search="timeout" last=24h          # free-text search
/cf-workers-logs userId=user_123                    # filter by custom field
```

Multiple arguments can be combined:

```
/cf-workers-logs worker=my-api level=error last=24h limit=50
```

### Available filters

| Argument | Description |
|----------|-------------|
| `worker=xxx` | Filter by Worker script name |
| `level=error` | Filter by log level (`log`, `info`, `warn`, `error`) |
| `entrypoint=MyDO` | Filter by entrypoint class (DO, Workflow) |
| `event=alarm` | Filter by event type (`fetch`, `rpc`, `queue`, `scheduled`, `alarm`) |
| `search=xxx` | Free-text search across all fields |
| `<key>=<value>` | Filter by any custom field |
| `last=1h` | Time range: `30m`, `1h`, `24h`, etc. (default: `1h`) |
| `limit=N` | Max results (default: `30`) |

## License

MIT
