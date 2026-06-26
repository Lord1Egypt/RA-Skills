---
name: docker-volume-backup-or-restore
version: 2.0.0
description: "Robust Docker volume migration and backup using per-volume encrypted archives and registry-based transport. Supports dry-runs, container exclusion, and safe restoration without executing untrusted code."
---

# Docker Volume Backup Or Restore (v2.0)

## Overview

This skill provides a secure, registry-backed workflow for migrating or backing up Docker volumes. Version 2.0 introduces a **per-volume encryption architecture**, creating separate encrypted archives for each volume. This improves reliability for large volume sets and eliminates path-parsing ambiguities during restoration.

Key features:
- **Zero-Trust Restore**: Files are copied out of the backup image using `docker cp`. The backup image's code is never executed.
- **Per-Volume Encryption**: Each volume is encrypted separately with AES-256-CBC (PBKDF2).
- **Container Safety**: Automatically stops containers to ensure data consistency, with an `--exclude-stop` flag for critical infrastructure (like proxies or AI providers).
- **Registry Transport**: Uses standard Docker registries as storage, making it easy to move data between any Docker-enabled hosts.
- **Dry-Run Support**: Preview actions before stopping containers or pushing data.

## Workflow

### 1. Prerequisites

1.  **Docker**: Must be installed and running.
2.  **Registry Login**: Ensure you are logged in to your target registry (e.g., `docker login`).
3.  **Helper Image**: The script uses a pinned `alpine` image for crypto operations. It must be pre-pulled for safety.

### 2. Backup Mode

Creates encrypted archives of all local volumes and pushes them as a single multi-layer image.

```bash
# Basic backup (auto-derives image name from hostname)
bash docker_volume_backup_or_restore.sh --backup --encrypt-password 'your-password'

# Backup with specific image and excluded containers
bash docker_volume_backup_or_restore.sh --backup-image user/repo:tag --encrypt-password 'pass' --exclude-stop proxy,db
```

**What happens:**
1.  Identifies all local volumes and running containers.
2.  Stops containers (except those in `--exclude-stop`).
3.  Mounts volumes into a trusted Alpine container.
4.  **New in v2.0**: Packages and encrypts each volume into its own `.tar.gz.enc` file.
5.  Builds a `scratch`-based image containing only these encrypted archives.
6.  Pushes the image to the registry.
7.  Restarts the stopped containers.

### 3. Restore Mode

Pulls a backup image and restores volumes to the local host.

```bash
bash docker_volume_backup_or_restore.sh --restore user/repo:tag --encrypt-password 'your-password'
```

**What happens:**
1.  Pulls the backup image.
2.  Creates a temporary container to `docker cp` the archives out (safely).
3.  Discovers volume names from the archive filenames.
4.  Creates missing local volumes.
5.  For each volume: decrypts the archive and copies data into the volume using a trusted helper.

## Arguments

- `--backup [IMAGE]`: Start backup mode. Optional IMAGE override.
- `--backup-image IMAGE`: Explicit backup image reference.
- `--restore IMAGE`: Start restore mode using the specified image.
- `--encrypt-password PASS`: **Required.** Password for AES-256 encryption/decryption.
- `--exclude-stop LIST`: Comma-separated list of containers to keep running during backup.
- `--dry-run`: Show planned actions without executing them.

## Safety and Tradeoffs

- **Encryption**: Uses `openssl` AES-256-CBC with PBKDF2. Passwords are never stored in the image.
- **Data Integrity**: Stopping containers is highly recommended to prevent partial writes.
- **Storage**: Large volumes will result in large images. Ensure your registry has sufficient quota and bandwidth.
- **Overwrites**: Restore mode will overwrite existing data if a volume with the same name already exists.
