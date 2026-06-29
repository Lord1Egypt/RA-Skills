# Mesh Operations

## Inter-Gateway Communication

All gateways expose chatCompletions API on :18789:
```bash
curl http://<IP>:18789/v1/chat/completions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"model":"default","messages":[{"role":"user","content":"ping"}]}'
```

## Mesh IP Map

| Node | IP | Region | Bot |
|------|-----|--------|-----|
| openclaw-gcp | 136.118.144.227 | us-west1-b | @EvezVearlBot |
| power-node | 136.113.102.152 | us-central1-a | @EVEZcloudBot |
| evez-primary | 34.53.51.34 | us-west1-b | @GCPwestbot |
| evez-gcp-openclaw | 35.222.248.151 | us-central1-a | @Evez4RealBot |
| Vultr | 64.176.221.16 | Newark NJ | — |

## Cross-Node Healing

Sibling watchdog v2 runs every 2 min on each node:
1. Check own gateway health → restart if down
2. Check each sibling's gateway → attempt SSH heal if unreachable
3. Heal actions: fix config bugs, kill zombie processes, reset-failed, restart
4. Auto-fix known config bugs: `api:"google"` → `api:"google-generative-ai"`, remove invalid keys

## Shared Brain

- GCS bucket: `evez666-shared-awareness/hive/`
- Each node writes a thought every 10 min
- Each node reads siblings' thoughts every 10 min
- Format: `{node, timestamp, status, thoughts, load}`

## Task Routing

```
quick task    → DeepSeek-V4-Flash (fast)
research task → Qwen3.5-397B (deep)
creative task → GLM-5.1-FP8 (balanced)
```

## Disk Hygiene

```
60% → proactive cleanup (logs, temp, cache)
75% → alert + aggressive cleanup
85% → panic: docker system prune, journal vacuum, old backups
```

## Revenue Pipeline

Distributed across nodes:
- Research on researcher (power-node)
- Outreach on scout (openclaw-gcp)
- Products: Mesh Infra $49/mo, Agent Network $99/mo, Custom $299/mo
