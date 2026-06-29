# Security & Hardening

## Layer 1: OS

- SSH: key-only, no password, no root login, ED25519 keys
- UFW: default deny, allow 22/80/443/18789/+app-specific
- fail2ban: active, mesh IPs whitelisted
- `chmod 700 ~/.openclaw`, `chmod 600 ~/.openclaw/config.yaml ~/.openclaw/.env`

## Layer 2: Network

- GCP VPC: custom (evez-vpc), peered with default
- Firewall: allow-only + explicit deny-all egress on sensitive subnets
- Private Google Access on all API-needing subnets
- Cloud NAT for outbound-only nodes
- No public IPs on internal-only services

## Layer 3: Cloud IAM

- Dedicated SAs per function (evez-os, evez-compute, evez-cloudrun)
- No Editor/Owner on default compute SA
- Service account keys in Secret Manager, not on disk
- Workload Identity where possible, keys where not

## Layer 4: Container

- Non-root USER in every Dockerfile
- `--cap-add` only specific capabilities
- No `--privileged` ever
- Docker secrets or mounted files for credentials
- Resource limits on every container

## Layer 5: Application

- Gateway auth token on all API endpoints
- Telegram bot tokens isolated per node
- dmScope: per-account-channel-peer for session isolation
- Audit logging via BigQuery sink (severity ≥ WARNING)

## AgentGuard Scan Rules

24 detection categories covering:
- Shell exec (child_process, subprocess, os.system)
- Auto-update / self-modification
- Remote code loading (dynamic import, eval(fetch))
- Credential reading (env, SSH keys, keychain)
- Web3 exploits (wallet draining, unlimited approvals)
- Obfuscation, prompt injection, social engineering

## Common Exposures to Check

- [ ] `.env` files in git
- [ ] API keys in code
- [ ] Public storage buckets
- [ ] Open management ports (6969, 18789 without auth)
- [ ] Default credentials
- [ ] Unrotated service account keys
