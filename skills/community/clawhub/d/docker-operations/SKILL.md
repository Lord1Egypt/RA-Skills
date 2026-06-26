---
name: docker-operations
description: Provides Docker container and image operations for creating, running, managing, and inspecting containers and images. Use for docker run, docker exec, docker ps, docker build, docker pull/push, docker images, docker start/stop/restart, docker logs, docker inspect, docker cp, docker commit, docker tag, docker save/load, docker buildx, docker compose, and any container or image management tasks.
---

# Docker Operations

This skill provides comprehensive Docker operations using the `docker` CLI. Ensure Docker is installed and configured on your system:

```bash
docker --version
```

## When to Use

- Creating, running, stopping, and managing containers
- Building and pulling/pushing Docker images
- Inspecting containers, images, and Docker objects
- Copying files between containers and host
- Managing Docker registries and image tags
- Viewing logs and real-time container stats
- Cleaning up unused Docker resources

## When NOT to Use

- Docker Swarm orchestration (use dedicated swarm tooling)
- Kubernetes container management
- Building Docker images with complex buildx bake files (see references/buildx.md)
- Docker Compose multi-container applications (see references/compose.md)

## Command Reference

### Container Lifecycle
Create, start, stop, pause, and remove containers.

| Command | Description | Reference |
|---------|-------------|-----------|
| `docker create` | Create container without starting | [references/container-lifecycle.md](references/container-lifecycle.md) |
| `docker start` | Start a container | [references/container-lifecycle.md](references/container-lifecycle.md) |
| `docker run` | Create and start a container | [references/container-lifecycle.md](references/container-lifecycle.md) |
| `docker stop` | Stop a running container | [references/container-lifecycle.md](references/container-lifecycle.md) |
| `docker restart` | Restart a container | [references/container-lifecycle.md](references/container-lifecycle.md) |
| `docker pause` | Pause container processes | [references/container-lifecycle.md](references/container-lifecycle.md) |
| `docker unpause` | Resume paused processes | [references/container-lifecycle.md](references/container-lifecycle.md) |
| `docker rm` | Remove a container | [references/container-lifecycle.md](references/container-lifecycle.md) |

### Container Interaction
Execute commands, view logs, copy files, and monitor containers.

| Command | Description | Reference |
|---------|-------------|-----------|
| `docker exec` | Execute command in container | [references/container-interaction.md](references/container-interaction.md) |
| `docker attach` | Attach to running container | [references/container-interaction.md](references/container-interaction.md) |
| `docker logs` | View container logs | [references/container-interaction.md](references/container-interaction.md) |
| `docker top` | Show running processes | [references/container-interaction.md](references/container-interaction.md) |
| `docker stats` | Display resource usage | [references/container-interaction.md](references/container-interaction.md) |
| `docker cp` | Copy files between host and container | [references/container-interaction.md](references/container-interaction.md) |
| `docker diff` | Show filesystem changes | [references/container-interaction.md](references/container-interaction.md) |

### Container Listing
List and filter Docker containers.

| Command | Description | Reference |
|---------|-------------|-----------|
| `docker ps` | List running containers | [references/container-listing.md](references/container-listing.md) |
| `docker ps -a` | List all containers | [references/container-listing.md](references/container-listing.md) |

### Image Operations
Pull, push, build, tag, save, load, and manage images.

| Command | Description | Reference |
|---------|-------------|-----------|
| `docker images` | List local images | [references/image-operations.md](references/image-operations.md) |
| `docker pull` | Pull image from registry | [references/image-operations.md](references/image-operations.md) |
| `docker push` | Push image to registry | [references/image-operations.md](references/image-operations.md) |
| `docker build` | Build image from Dockerfile | [references/image-operations.md](references/image-operations.md) |
| `docker tag` | Tag an image | [references/image-operations.md](references/image-operations.md) |
| `docker save` | Save image to tar | [references/image-operations.md](references/image-operations.md) |
| `docker load` | Load image from tar | [references/image-operations.md](references/image-operations.md) |
| `docker export` | Export container filesystem | [references/image-operations.md](references/image-operations.md) |
| `docker import` | Import tarball to image | [references/image-operations.md](references/image-operations.md) |
| `docker history` | Show image history | [references/image-operations.md](references/image-operations.md) |
| `docker rmi` | Remove an image | [references/image-operations.md](references/image-operations.md) |

### Image Inspection
Inspect Docker objects (containers, images, volumes, networks).

| Command | Description | Reference |
|---------|-------------|-----------|
| `docker inspect` | Return low-level info on containers, images, volumes, networks | [references/image-inspection.md](references/image-inspection.md) |

### Registry Operations
Login, logout, and search Docker registries.

| Command | Description | Reference |
|---------|-------------|-----------|
| `docker login` | Login to registry | [references/registry.md](references/registry.md) |
| `docker logout` | Logout from registry | [references/registry.md](references/registry.md) |
| `docker search` | Search Docker Hub | [references/registry.md](references/registry.md) |

### System Information
Get Docker version, system info, and real-time events.

| Command | Description | Reference |
|---------|-------------|-----------|
| `docker version` | Show Docker version | [references/system-info.md](references/system-info.md) |
| `docker info` | Display system info | [references/system-info.md](references/system-info.md) |
| `docker events` | Get real-time events | [references/system-info.md](references/system-info.md) |

### Cleanup Commands
Remove unused Docker resources.

| Command | Description | Reference |
|---------|-------------|-----------|
| `docker container prune` | Remove stopped containers | [references/cleanup.md](references/cleanup.md) |
| `docker image prune` | Remove unused images | [references/cleanup.md](references/cleanup.md) |
| `docker volume prune` | Remove unused volumes | [references/cleanup.md](references/cleanup.md) |
| `docker network prune` | Remove unused networks | [references/cleanup.md](references/cleanup.md) |
| `docker system prune` | Full system cleanup | [references/cleanup.md](references/cleanup.md) |

## Advanced Topics

For complex multi-platform builds and bake files, see [references/buildx.md](references/buildx.md).

For Docker Compose operations and multi-container orchestration, see [references/compose.md](references/compose.md).

### Advanced Image Operations
Extract image contents, analyze layers, and manipulate image filesystems.

| Operation | Description | Reference |
|-----------|-------------|-----------|
| Extract image to directory | Export image filesystem to local directory | [references/advanced-image-operations.md](references/advanced-image-operations.md) |
| Layer analysis | Inspect and extract specific image layers | [references/advanced-image-operations.md](references/advanced-image-operations.md) |
| Image filesystem comparison | Compare image contents between versions | [references/advanced-image-operations.md](references/advanced-image-operations.md) |
