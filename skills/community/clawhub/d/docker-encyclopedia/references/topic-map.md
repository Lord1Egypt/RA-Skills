# Docker Topic Map

Use this as a quick orientation aid when deciding what docs to look up.

## Core areas

- Docker Engine / daemon / runtime behavior
- CLI commands and operational workflows
- Dockerfiles / image builds / BuildKit / buildx
- Containers / images / layers / lifecycle
- Volumes / bind mounts / storage behavior
- Networks / ports / name resolution
- Compose / multi-container application definitions
- Registries / authentication / image distribution
- Rootless Docker / contexts / remote engines

## Typical lookup prompts

When the task is about...

### Engine / CLI
Look for docs covering:
- docker CLI commands
- daemon behavior
- contexts
- rootless mode
- engine configuration

### Builds / Dockerfiles
Look for docs covering:
- Dockerfile reference
- build context semantics
- BuildKit/buildx
- caching behavior
- multi-stage builds

### Compose
Look for docs covering:
- compose file reference
- service/network/volume semantics
- environment/config handling
- lifecycle commands

### Storage / networking
Look for docs covering:
- volumes
- bind mounts
- overlay/network drivers
- publishing ports
- DNS/name resolution

### Registries / auth
Look for docs covering:
- registries
- image push/pull
- auth/login
- credential stores/helpers

### Security / operations
Look for docs covering:
- rootless mode
- daemon socket exposure
- capabilities/seccomp when relevant
- cleanup/pruning behavior
