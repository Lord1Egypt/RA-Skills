# docker-ops

Manage Docker containers: status reports, log analysis, and restarts via docker-socket-proxy.

## Prerequisites

- `docker` CLI available in PATH
- `jq` available in PATH
- `DOCKER_HOST` environment variable is pre-configured (do NOT override it manually)
- `whitelist.yml` in the agent workspace root

## Whitelist

Before **any** Docker command, check the `SYSCTL_WHITELIST_PATH` environment variable.

**If `SYSCTL_WHITELIST_PATH` is NOT set or empty:**
- Do NOT run any Docker commands
- Reply: "⚠️ `SYSCTL_WHITELIST_PATH` is not configured. Set this environment variable in the container to point to the whitelist YAML file."
- This applies to ALL requests without exception

**If set**, read the whitelist file from that path. There is no fallback file.

Structure:

```yaml
containers:
  - name: container_name
    description: "Human description"
    can_restart: true|false
```

**Rules:**
- NEVER run Docker commands against containers not in the whitelist
- NEVER restart containers where `can_restart: false`
- If a requested container is not in the whitelist, respond: "Container `<name>` is not in the whitelist. Available: <list>"

## Allowed Commands

You may ONLY use these Docker commands:

| Command | When |
|---------|------|
| `docker ps --format json` | List running containers |
| `docker ps -a --format json` | List all containers (including stopped) |
| `docker inspect <name>` | Get container details (status, uptime, restart count) |
| `docker stats --no-stream --format json <name>` | Get resource usage (CPU, RAM, NET, BLOCK) |
| `docker logs --since <period> --tail 500 <name>` | Read container logs |
| `docker restart <name>` | Restart a container (explicit request only!) |

### Forbidden Commands

NEVER execute: `docker rm`, `docker stop`, `docker kill`, `docker exec`, `docker run`, `docker pull`, `docker build`, `docker push`, `docker network`, `docker volume`, `docker image`, `docker system`, `docker compose`.

## Report Procedure

When asked for a status report:

### Step 1: Parse the period

Convert user text to `--since` parameter:
- "за последний час" / "last hour" → `1h`
- "за сегодня" / "today" → `24h`
- "за 30 минут" / "30 minutes" → `30m`
- "за неделю" / "last week" → `168h`
- No period specified → default `1h`
- **Maximum:** `168h` (7 days). If user requests more — cap at 168h and inform them.

### Step 2: Collect data

All `docker` commands must be wrapped with `timeout 30` to prevent hanging.

```bash
# Status + uptime + restart count
timeout 30 docker inspect <name> | jq '.[0] | {Status: .State.Status, StartedAt: .State.StartedAt, RestartCount: .RestartCount, Health: .State.Health.Status}'

# Resource usage
timeout 30 docker stats --no-stream --format '{{json .}}' <name>

# Fetch logs once, then count errors and warnings locally
LOG_OUTPUT=$(timeout 30 docker logs --since <period> --tail 5000 <name> 2>&1)

# Error/warning count (quick stats)
echo "${LOG_OUTPUT}" | grep -ci 'error\|exception\|fatal\|traceback'
echo "${LOG_OUTPUT}" | grep -ci 'warn'

# Last errors (up to 10 unique)
echo "${LOG_OUTPUT}" | grep -i 'error\|exception\|fatal\|traceback' | sort -u | tail -10
```

### Step 3: Sanitize output

Before displaying log fragments to users, mask sensitive patterns:
- Tokens, API keys, Bearer headers
- Database connection strings with credentials
- Passwords, secrets in environment variable dumps

Replace with `[REDACTED]` where detected.

### Step 4: Format response

Use this template (adapt to language of request):

```
<status_emoji> **<container_name>**

**Status:** `running` (uptime: 2d 5h 13m)
**Restarts:** 0
**CPU:** 2.3% | **RAM:** 145MiB / 512MiB (28%)
**NET I/O:** 1.2MB / 340KB | **BLOCK I/O:** 12MB / 5MB

**Logs at last hour:**
- 🔴 Errors: 3
- ⚠️ Warnings: 12

**Last errors:**
• `ConnectionRefusedError: connect to postgres:5432`
• `TimeoutError: request took >30s`

**Recommendation:** Check access to PostgreSQL
```

Status emoji rules:
- ✅ — running, 0 errors, low resource usage
- ⚠️ — running but has warnings/errors, or high resource usage (>80% CPU/RAM)
- 🔴 — stopped/restarting/exited, or critical errors

## Restart Procedure

When asked to restart a container:

1. Verify container is in whitelist AND `can_restart: true`
2. Confirm the request is **explicit** (user said "restart", "перезапусти", "рестартни")
3. **Cooldown check:** do not restart the same container more than once per 5 minutes. If repeated — warn and ask to confirm.
4. **Audit log:** before executing, output:
   ```
   [AUDIT] <ISO-timestamp> restart <container_name> requested_by=<user_id_if_available>
   ```
5. Execute: `timeout 30 docker restart <name>`
6. Wait and verify with retries:
   ```bash
   for i in 1 2 3; do
     sleep 10
     STATUS=$(timeout 30 docker inspect <name> | jq -r '.[0].State.Status')
     if [ "${STATUS}" = "running" ]; then break; fi
   done
   ```
7. If running → report success with new status
8. If not running after 30s → report failure with last 20 log lines:
   `timeout 30 docker logs --tail 20 <name> 2>&1`

## Log Viewing

When asked to show logs:

1. Verify container is in whitelist
2. Apply `--tail 500` limit always
3. If user asks for filtered logs (errors only, etc.) — use `grep`
4. For large output — summarize, don't dump raw
5. Sanitize sensitive data before displaying (see Step 3 in Report Procedure)

## Safety Notes

- NEVER pass user input directly into shell commands as container names — only use exact matches from whitelist
- Always use `2>&1` when piping docker logs (stderr contains the actual logs)
- If `DOCKER_HOST` is not set, do NOT guess the address — report to user: "DOCKER_HOST is not configured. Set this environment variable to point to the docker-socket-proxy endpoint."
- If docker command fails with connection error — report to user that docker-socket-proxy may be down
