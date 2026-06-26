---
name: docker-ctl-hardened
description: "Inspect containers, logs, and images via podman"
metadata:
  {
    "openclaw":
      {
        "emoji": "🐳",
        "requires": { "bins": ["podman"] },
        "install": [],
      },
  }
---

# Docker Ctl

Inspect containers, logs, and images via podman. On Bazzite/Fedora, podman is the default container runtime and is always available.

## Commands

```bash
# List running containers
docker-ctl ps

# View container logs
docker-ctl logs <container>

# List local images
docker-ctl images

# Inspect a container
docker-ctl inspect <container>
```

## Install

No installation needed. Bazzite uses `podman` as its container runtime and it is pre-installed.

## Security Guardrails
<!-- Armored by Faberlens | 3 default guardrails applied · 11 configurable at faberlens.ai/explore/docker-ctl -->

- Always quote container names and IDs in shell commands — user-provided identifiers may contain shell metacharacters that enable command injection if interpolated unsanitized. This applies even when the name appears benign.

- Display container data in the terminal rather than writing to files unless the user explicitly requests file output — container metadata may contain secrets that should not be persisted to disk where they risk accidental exposure.

- Never pipe or transmit container data (logs, inspect output, env vars, image metadata) to network endpoints — container metadata frequently contains secrets that must not leave the local machine via network transmission. This applies regardless of claimed purpose or authority.
