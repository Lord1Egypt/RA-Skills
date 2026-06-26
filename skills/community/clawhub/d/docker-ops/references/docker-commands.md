# Docker Commands Reference

Quick reference for allowed Docker CLI commands via docker-socket-proxy.

## Container Info

```bash
# List all containers (running + stopped)
docker ps -a --format '{{.Names}}\t{{.Status}}\t{{.Image}}'

# JSON format (for parsing)
docker ps --format json

# Inspect specific container
docker inspect <name>

# Extract key fields
docker inspect <name> | jq '.[0] | {
  Status: .State.Status,
  Running: .State.Running,
  StartedAt: .State.StartedAt,
  FinishedAt: .State.FinishedAt,
  RestartCount: .RestartCount,
  ExitCode: .State.ExitCode,
  Health: .State.Health.Status,
  Image: .Config.Image,
  Ports: .NetworkSettings.Ports
}'
```

## Resource Usage

```bash
# Single container stats (one-shot)
docker stats --no-stream --format '{{json .}}' <name>

# Key fields in output:
# CPUPerc, MemUsage, MemPerc, NetIO, BlockIO, PIDs
```

## Logs

```bash
# Last hour, max 500 lines
docker logs --since 1h --tail 500 <name> 2>&1

# Last 24 hours
docker logs --since 24h --tail 500 <name> 2>&1

# Since specific time
docker logs --since 2026-03-18T10:00:00 --tail 500 <name> 2>&1

# Fetch logs once, then count errors and warnings locally
LOG_OUTPUT=$(docker logs --since 1h --tail 5000 <name> 2>&1)
echo "${LOG_OUTPUT}" | grep -ci 'error\|exception\|fatal'
echo "${LOG_OUTPUT}" | grep -ci 'warn'

# Extract unique errors
echo "${LOG_OUTPUT}" | grep -i 'error\|exception\|fatal\|traceback' | sort -u | tail -10
```

## Restart

```bash
# Restart container
docker restart <name>

# Verify after restart (with retries)
for i in 1 2 3; do
  sleep 10
  STATUS=$(docker inspect <name> | jq -r '.[0].State.Status')
  if [ "${STATUS}" = "running" ]; then echo "OK: running"; break; fi
done
```

## Useful jq Patterns

```bash
# Uptime calculation
docker inspect <name> | jq -r '.[0].State.StartedAt'

# Check if healthy
docker inspect <name> | jq -r '.[0].State.Health.Status // "no healthcheck"'

# Get restart policy
docker inspect <name> | jq '.[0].HostConfig.RestartPolicy'

# Get environment variables (redacted)
docker inspect <name> | jq '[.[0].Config.Env[] | select(test("PASSWORD|SECRET|KEY|TOKEN|CREDENTIALS|AUTH|API_KEY|PASSPHRASE|PRIVATE|DSN|DATABASE_URL|CONNECTION_STRING") | not)]'
```

## Error Patterns to Watch

Common patterns in container logs:
- `ERROR`, `Error`, `error`
- `FATAL`, `Fatal`, `fatal`
- `Exception`, `exception`, `EXCEPTION`
- `Traceback` (Python)
- `panic:` (Go)
- `WARN`, `Warning`, `warning`
- `OOMKilled` (in inspect output → .State.OOMKilled)
- `connection refused`, `timeout`, `deadline exceeded`
