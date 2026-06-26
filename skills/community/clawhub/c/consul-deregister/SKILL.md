---
name: consul-deregister
description: Consul service deregistration tool. Triggered when users mention Consul deregister, remove service instance, service removal, or offline. Supports batch deregister by service ID across multiple Consul agents, parse and replay raw curl commands, dry-run preview, parallel execution, and ACL token auth.
---

# Consul Service Deregister

Deregister service instances from Consul via the HTTP API.

## Usage

### Mode 1: Service ID + Agent List (Most Common)

```
User: Deregister service my-service-id on consul-agent-1, consul-agent-2, and consul-agent-3
```

AI executes:
```bash
python3 /Users/shiheng/.qclaw/workspace/skills/consul-deregister/scripts/deregister.py \
  --service-id my-service-id \
  --agents http://<CONSUL_HOST_1>:8500 http://<CONSUL_HOST_2>:8500 http://<CONSUL_HOST_3>:8500
```

### Mode 2: Paste Raw curl Commands (Easiest)

User pastes existing curl commands, AI parses and replays them:

```
User: Execute these deregister commands:
      curl -XPUT http://<CONSUL_HOST_1>:8500/v1/agent/service/deregister/<SERVICE_ID>
      curl -XPUT http://<CONSUL_HOST_2>:8500/v1/agent/service/deregister/<SERVICE_ID>
```

AI executes:
```bash
python3 /Users/shiheng/.qclaw/workspace/skills/consul-deregister/scripts/deregister.py \
  --from-curl "curl -XPUT http://<CONSUL_HOST>:8500/v1/agent/service/deregister/<SERVICE_ID> ..."
```

### Mode 3: Read Agent List from File

```bash
python3 /Users/shiheng/.qclaw/workspace/skills/consul-deregister/scripts/deregister.py \
  --service-id my-service-id \
  --agents-file ./agents.txt
```

`agents.txt` format (supports `#` comments):
```
# Consul Agent node list
<CONSUL_HOST_1>:8500
<CONSUL_HOST_2>:8500
<CONSUL_HOST_3>:8500
```

### Dry-Run Preview

Add `--dry-run` to any mode to preview the requests without actually sending them:

```bash
python3 /Users/shiheng/.qclaw/workspace/skills/consul-deregister/scripts/deregister.py \
  --service-id my-service-id \
  --agents http://<CONSUL_HOST_1>:8500 http://<CONSUL_HOST_2>:8500 \
  --dry-run
```

### With ACL Token

```bash
python3 /Users/shiheng/.qclaw/workspace/skills/consul-deregister/scripts/deregister.py \
  --service-id my-service-id \
  --agents http://<CONSUL_HOST>:8500 \
  --token your-consul-acl-token
```

## Common Workflows

**Scenario 1: Batch Deregister Gray Nodes**
User provides a service ID and multiple IP:port pairs.

**Scenario 2: Release Rollback**
User triggers rollback; AI finds the old version's service ID from config/docs and deregisters.

**Scenario 3: Service Migration**
Moving a service from old cluster to new cluster — deregister from all old cluster nodes first.

## Notes

- `service-id` must exactly match the ID registered in Consul (no extra spaces)
- Agent addresses accept both `host:port` and full URL (`http://host:port`) — auto-completed
- Parallel requests by default (up to 10 concurrent), automatic speedup for many nodes
- Non-zero exit code on any failure; AI will surface failure details
- Use `--json` for JSON output suitable for scripting / pipeline integration
