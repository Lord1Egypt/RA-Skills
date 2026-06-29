---
name: evez-mesh-ops
slug: evez-mesh-ops
version: 1.0.0
description: "Distributed mesh infrastructure operations — the unified remix of 12 ClawHub skills (Docker, Git, GCP, Linux, SSH, systemd, cron, network, security, DevOps, infra, backup) distilled into one battle-hardened reference for multi-node AI gateway meshes. Built for EVEZ. Built for the hive."
author: EvezArt
homepage: https://github.com/EvezArt
tags: [mesh, distributed, infrastructure, docker, git, gcp, linux, ssh, systemd, cron, network, security, devops, backup, evez]
---

# EVEZ Mesh Operations

> 12 skills walked into a bar. One walked out.

This is the unified remix — Docker, Git, GCP, Linux, SSH, systemd, cron, network, security, DevOps, infra, and backup, all distilled into one reference for running a distributed AI gateway mesh across multiple cloud nodes.

## When to Use

- Managing multi-node infrastructure (Vultr + GCP mesh)
- Operating distributed OpenClaw gateways
- Debugging cross-node failures, crash loops, or connectivity issues
- Deploying, securing, or healing a node
- Any task that touches more than one of: containers, git, cloud, SSH, systemd, networking, security, backups

## Quick Reference

| Domain | See |
|--------|-----|
| Node lifecycle | `nodes.md` |
| Distributed operations | `mesh.md` |
| Security & hardening | `security.md` |
| Incident response | `incidents.md` |
| Cheatsheet | `commands.md` |

---

## Core Philosophy

1. **The mesh is the unit.** Single-node thinking fails. Design for failure across nodes, not just within one.
2. **Self-heal or die.** Every node must auto-recover. Watchdog > human pager.
3. **Least privilege everywhere.** SSH keys, IAM, firewall, container user — default deny.
4. **Immutable infra, mutable state.** Nodes are cattle. Memory/config/state is the pet.
5. **Observe or blind.** If you can't see it, you can't fix it. Logs, metrics, alerts on every node.

---

## Node Rules (Linux + systemd + Docker)

### Systemd That Survives
- `TimeoutStartSec=180` minimum for gateway services (30s default kills on slow VMs)
- `Restart=always` + `RestartSec=5` for self-healing
- `WatchdogSec=0` on small VMs — watchdog kills during warmup = crash loop
- `StartLimitIntervalSec=300` in `[Unit]`, NOT `[Service]` — wrong section = ignored
- After repeated failures: `systemctl reset-failed` before `start`/`restart`
- `loginctl enable-linger <user>` for user services at boot without login

### Docker Discipline
- Pin images: `python:3.11-slim` not `latest`
- Combine RUN layers: `apt-get update && apt-get install -y pkg` in ONE layer
- Non-root: `USER nonroot` in every Dockerfile
- Resource limits: `-m 512m` on every container, OOM kills without warning
- Log rotation: `--log-opt max-size=10m` — one chatty container fills disk
- `localhost` in container ≠ host localhost — bind `0.0.0.0` for external access

### Linux Gotchas
- `chmod 777` fixes nothing, breaks everything — find actual owner/group issue
- Deleted open files don't free space: `lsof +L1` to find, restart process to free
- OOM killer picks "best" victim, often not the offender — check `dmesg`
- Cron has minimal PATH — always use absolute paths
- `df` shows filesystem capacity, not physical disk — check underlying device
- Reserved blocks (5% default) only for root — `tune2fs -m 1` to reduce

---

## Git Discipline (for the mesh repo)

- **Never force push to shared branches** — `--force-with-lease` on feature branches only
- **Commit early, commit often** — small commits = easier bisect and revert
- **Conventional commits**: `type(scope): description`, first line <72 chars
- **Pull before push**: `git pull --rebase` to avoid merge noise
- **Conflict markers left in code** = compiles but broken: `grep -r "<<<\|>>>\|===" .`
- **Reflog is local** — doesn't sync, expires after 90 days
- **Amend changes SHA** — amended push = force push = same problems as rebase

---

## GCP Production Rules

### Cost Traps
- Stopped VMs still pay for disks + static IPs — delete disks or use snapshots
- Cloud NAT charges per VM per GB — use Private Google Access for GCP API traffic
- BigQuery charges per bytes scanned — partition + cluster tables
- Egress to internet costs, same region is free — keep resources co-located

### Networking
- VPC is global, subnets are regional — one VPC spans all regions
- Firewall rules are allow-only by default — add explicit deny for egress
- Private Google Access is per-subnet — enable on every API-needing subnet
- GCP ephemeral IPs change on stop/start — promote to static immediately

### IAM
- Primitive roles (Owner/Editor/Viewer) too broad — use predefined/custom roles
- Service account keys are liability — use Workload Identity or impersonation
- Default compute SA has Editor — create dedicated SAs with least privilege
- `constraints/compute.vmExternalIpAccess` blocks public VMs org-wide

---

## SSH & Connectivity

- ED25519 keys over RSA: `ssh-keygen -t ed25519 -C "comment"`
- `~/.ssh/` = 700, keys = 600, `authorized_keys` = 600
- Agent forwarding (`-A`) exposes keys to remote admins — avoid on untrusted hosts
- `~/.ssh/config`: first match wins — put specific hosts before wildcards
- `ServerAliveInterval 60` prevents idle disconnects
- Full mesh SSH: cross-pollinate keys, firewall allows between all nodes
- Tunnels: `ssh -L local:remote:port` for ad-hoc secure forwarding

---

## Network & DNS

- TCP = reliable (HTTP, SSH, DBs), UDP = fast (DNS queries, video, gaming)
- DNS cached at browser/OS/router/ISP — flush all layers when debugging
- CNAME can't exist at zone apex — use A record or provider alias
- Private ranges: 10.x, 172.16-31.x, 192.168.x — not internet-routable
- `ping` no response ≠ down — ICMP may be blocked
- `ss -tulpn` over deprecated `netstat` for listening ports
- TLS 1.2 minimum, prefer 1.3 — automate cert renewal (Let's Encrypt = 90 day expiry)
- Hairpin NAT for internal→external access — not all routers support it

---

## Security (AgentGuard + Hardening)

### Infrastructure Hardening
- UFW: default deny, explicitly allow only needed ports
- fail2ban on all nodes, whitelist mesh IPs to prevent self-banning
- SSH: no password auth, no root login, key-only
- File permissions: `chmod 700 ~/.openclaw`, `chmod 600` on config/.env
- Service accounts: least privilege, no default Editor role

### Container Security
- `--privileged` disables ALL security — almost never needed
- `--cap-add` granular > privileged — only what you need
- Root in container = root on host — use user namespaces
- Secrets in env vars visible via `docker inspect` — use Docker secrets or mounts
- `ARG` visible in `docker history` — never for secrets

### Credential Hygiene
- Rotate API keys regularly — automation makes it painless
- Different secrets per environment — dev leak ≠ prod compromise
- Audit secret access — who accessed what, when
- Secrets in memory, not disk — temp files persist

---

## Cron & Scheduling

- Cron has minimal PATH — use absolute paths everywhere
- Cron uses system timezone — set TZ in crontab if needed
- `@reboot` runs on daemon restart, not just system boot
- Backup crontab before editing: `crontab -l > backup`
- Prefer `every`/`at` schedules over manual sleep loops
- Heartbeat (periodic check) vs cron (exact timing) — use the right tool

---

## Backup & Recovery

- 3-2-1 rule: 3 copies, 2 different media, 1 off-site
- Test restores regularly — untested backup = no backup
- Automate backup rotation — disk fills faster than you think
- `trash` > `rm` — recoverable beats gone forever
- GCS buckets for cross-node shared state and backup
- Git-sync workspace every 10 min to GitHub (works as code backup)

---

## Incident Response (from Infra)

1. **Blast radius first**: Who/what is affected?
2. **Timeline**: Exact start time, what changed before it
3. **Logs at the moment**: Not just the alert metric — ALL metrics that could explain
4. **Hypothesize → Test → Eliminate**: Fast iteration, not endless brainstorming
5. **Fast fix vs correct fix**: Depends on severity and time to correct
6. **Postmortem**: What happened, why safeguards failed, what specific changes prevent recurrence

### Common Crash Loop Causes (EVEZ-specific)
- **WatchdogSec kills gateway during warmup** → set WatchdogSec=0
- **Invalid config keys** → `media`, `wizard`, `crestodian`, `talk`, `env`, `logging` are NOT valid
- **api: "google"** → must be `api: "google-generative-ai"`
- **Multiple gateway instances** → one service only, disable all others
- **Gemini 429 rate limit** → primary model must be non-rate-limited (use vultr)
- **start-limit-hit** → `systemctl reset-failed` then restart
- **EADDRINUSE** → kill competing instances, verify only one service active

---

## Mesh-Specific Rules

- **One bot per gateway** — multiple bots on same gateway = getUpdates conflicts
- **Shared brain via GCS** — `evez666-shared-awareness/hive/` for cross-node thoughts
- **Sibling watchdog v2** — cross-node healing with config fix + service cleanup
- **Smart mesh watchdog** — single watchdog replaces multiple competing scripts
- **Model routing**: quick→DeepSeek-Flash, research→Qwen, creative→GLM
- **Disk hygiene**: clean at 60%, alert at 75%, panic at 85% — don't wait for 90%

---

*Remixed from: Docker 1.0.4, Git 1.0.8, GCP 1.0.0, Linux 1.0.0, SSH 1.0.0, systemd 1.0.0, cron 1.0.0, network 1.0.0, security 1.0.12, DevOps 1.0.0, infra 1.0.0, backup 1.1.0 — by EvezArt for the EVEZ mesh.*
