#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  cat <<'EOF2'
Usage:
  docker_volume_backup_or_restore.sh --backup [IMAGE] --encrypt-password PASSWORD [--dry-run] [--exclude-stop CONTAINER[,CONTAINER...]]
  docker_volume_backup_or_restore.sh --backup-image IMAGE --encrypt-password PASSWORD [--dry-run] [--exclude-stop CONTAINER[,CONTAINER...]]
  docker_volume_backup_or_restore.sh --restore IMAGE --encrypt-password PASSWORD [--dry-run]

Notes:
- Backup and restore modes are mutually exclusive.
- Requires Docker to be installed and authenticated to the target registry.
- Use fixed digest helper images; never rely on mutable latest tags.
- The encryption password must be passed with --encrypt-password and is never read from an environment variable.
- --dry-run will skip destructive actions (stop/rm/push/create) and show what would happen.
- --exclude-stop keeps named running containers alive during backup and skips restarting them afterward.
EOF2
}

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }

DRY_RUN=0
EXCLUDE_STOP_RAW=""
EXCLUDE_STOP_SET=""
ENCRYPT_PASSWORD=""

cleanup() {
  local exit_code=$?
  [[ "$DRY_RUN" -eq 1 ]] && exit "$exit_code"
  [[ -n "${BACKUP_CONTAINER_NAME:-}" ]] && docker rm -f "$BACKUP_CONTAINER_NAME" >/dev/null 2>&1 || true
  [[ -n "${RESTORE_CONTAINER_NAME:-}" ]] && docker rm -f "$RESTORE_CONTAINER_NAME" >/dev/null 2>&1 || true
  [[ -n "${WORKDIR:-}" && -d "$WORKDIR" ]] && rm -rf "$WORKDIR" || true
  if [[ "${MODE:-}" == "backup" && -n "${STOP_CONTAINERS[*]:-}" ]]; then
    log "Restarting containers that were stopped for backup..."
    docker start "${STOP_CONTAINERS[@]}" >/dev/null || true
  fi
  exit "$exit_code"
}
trap cleanup EXIT

require_cmd() { command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" >&2; exit 1; }; }
require_value() { [[ -n "$2" ]] || { echo "Missing required value: $1" >&2; exit 1; }; }
validate_image_ref() { [[ -n "$1" ]] || { echo "Image reference must not be empty" >&2; exit 1; }; [[ ! "$1" =~ [[:space:]] ]] || { echo "Image reference must not contain whitespace: $1" >&2; exit 1; }; }
is_digest_ref() { [[ "$1" == *@sha256:* ]]; }

MODE=""
BACKUP_IMAGE=""
RESTORE_IMAGE=""
BACKUP_IMAGE_WAS_EXPLICIT=0

[[ $# -gt 0 ]] || { usage; exit 1; }
while [[ $# -gt 0 ]]; do
  case "$1" in
    --backup)
      [[ -z "$MODE" ]] || { echo "Backup and restore modes are mutually exclusive" >&2; exit 1; }
      MODE="backup"; shift
      if [[ $# -gt 0 && "$1" != --* ]]; then BACKUP_IMAGE="$1"; BACKUP_IMAGE_WAS_EXPLICIT=1; shift; fi
      ;;
    --backup-image)
      [[ -z "$MODE" || "$MODE" == "backup" ]] || { echo "Backup and restore modes are mutually exclusive" >&2; exit 1; }
      MODE="backup"; shift; [[ $# -gt 0 ]] || { echo "--backup-image requires an image value" >&2; exit 1; }
      BACKUP_IMAGE="$1"; BACKUP_IMAGE_WAS_EXPLICIT=1; shift
      ;;
    --restore)
      [[ -z "$MODE" ]] || { echo "Backup and restore modes are mutually exclusive" >&2; exit 1; }
      MODE="restore"; shift; [[ $# -gt 0 ]] || { echo "--restore requires an image value" >&2; exit 1; }
      RESTORE_IMAGE="$1"; shift
      ;;
    --encrypt-password)
      shift; [[ $# -gt 0 ]] || { echo "--encrypt-password requires a value" >&2; exit 1; }
      ENCRYPT_PASSWORD="$1"; shift
      ;;
    --dry-run) DRY_RUN=1; shift ;;
    --exclude-stop)
      shift; [[ $# -gt 0 ]] || { echo "--exclude-stop requires a comma-separated container list" >&2; exit 1; }
      EXCLUDE_STOP_RAW="$1"; shift
      ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

[[ -n "$MODE" ]] || { echo "Either --backup or --restore is required" >&2; exit 1; }
require_value "--encrypt-password" "$ENCRYPT_PASSWORD"
export ENCRYPT_PASSWORD

require_cmd docker
require_cmd hostname
require_cmd openssl
require_cmd tar

docker info >/dev/null 2>&1 || { echo "Docker daemon is not reachable. Start Docker and try again." >&2; exit 1; }

RUNNING_CONTAINERS=(); STOP_CONTAINERS=(); BACKUP_CONTAINER_NAME=""; RESTORE_CONTAINER_NAME=""; WORKDIR="$(mktemp -d)"
BACKUP_ARTIFACT_DIR="$WORKDIR/backup-artifact"; RESTORE_WORK_DIR="$WORKDIR/restore-src"
mkdir -p "$BACKUP_ARTIFACT_DIR" "$RESTORE_WORK_DIR"
[[ -n "$EXCLUDE_STOP_RAW" ]] && EXCLUDE_STOP_SET=",$(printf '%s' "$EXCLUDE_STOP_RAW" | tr ',' '\n' | sed '/^$/d' | paste -sd, -),"

HELPER_IMAGE="alpine@sha256:48b0309ca019d89d40f670aa1bc06e426dc0931948452e8491e3d65087abc07d"
if [[ "$MODE" == "backup" ]]; then
  [[ -n "$BACKUP_IMAGE" ]] || {
    DOCKER_USER="$(docker info 2>/dev/null | awk -F': ' 'tolower($1) ~ /username/ {print $2; exit}')"
    HOST_TAG="$(hostname | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9._-]/-/g' | sed 's/-\{2,\}/-/g' | sed 's/^-//;s/-$//')"
    [[ -n "$HOST_TAG" ]] || { echo "Failed to derive hostname-based image tag" >&2; exit 1; }
    BACKUP_IMAGE="${DOCKER_USER:+$DOCKER_USER/backup:}$HOST_TAG"
  }
  validate_image_ref "$BACKUP_IMAGE"

  mapfile -t RUNNING_CONTAINERS < <(docker ps --format '{{.Names}}')
  mapfile -t VOLUMES < <(docker volume ls -q | sort)
  for container in "${RUNNING_CONTAINERS[@]}"; do [[ -n "$EXCLUDE_STOP_SET" && "$EXCLUDE_STOP_SET" == *",$container,"* ]] && continue; STOP_CONTAINERS+=("$container"); done
  printf '%s\n' "${RUNNING_CONTAINERS[@]}" > container_running_list
  printf '%s\n' "${VOLUMES[@]}" > volume_list
  [[ ${#VOLUMES[@]} -gt 0 ]] || { echo "No Docker volumes found to back up." >&2; exit 1; }

  if [[ "$DRY_RUN" -eq 1 ]]; then
    log "[DRY-RUN] Backup mode summary:"; log "[DRY-RUN] Target image: $BACKUP_IMAGE"; log "[DRY-RUN] Containers to stop: ${STOP_CONTAINERS[*]}"; [[ -n "$EXCLUDE_STOP_RAW" ]] && log "[DRY-RUN] Containers excluded from stop: $EXCLUDE_STOP_RAW"; log "[DRY-RUN] Volumes to back up: ${VOLUMES[*]}"; exit 0
  fi

  [[ ${#STOP_CONTAINERS[@]} -gt 0 ]] && { log "Stopping running containers to freeze volume writes..."; docker stop "${STOP_CONTAINERS[@]}" >/dev/null; } || log "No stoppable running containers detected."
  BACKUP_CONTAINER_NAME="backup-$(date +%s)"
  log "Using fixed-digest helper image: $HELPER_IMAGE"
  docker image inspect "$HELPER_IMAGE" >/dev/null 2>&1 || { echo "Helper image $HELPER_IMAGE is not available locally. Pin and pre-pull a trusted digest before using this skill." >&2; exit 1; }

  MOUNTS=(); for volume in "${VOLUMES[@]}"; do MOUNTS+=( -v "$volume:/docker_volume/$volume:ro" ); done
  log "Creating encrypted backup payload inside temporary helper container..."
  docker run --rm --name "$BACKUP_CONTAINER_NAME" -v "$BACKUP_ARTIFACT_DIR:/artifact" -e ENCRYPT_PASSWORD="$ENCRYPT_PASSWORD" "${MOUNTS[@]}" "$HELPER_IMAGE" sh -lc '
    apk add --no-cache openssl tar >/dev/null
    mkdir -p /artifact/volumes
    for vol_path in /docker_volume/*; do
      [ -d "$vol_path" ] || continue
      vol_name=$(basename "$vol_path")
      tar czf - -C "$vol_path" . | openssl enc -aes-256-cbc -pbkdf2 -salt -pass env:ENCRYPT_PASSWORD -out "/artifact/volumes/${vol_name}.tar.gz.enc"
    done
  '

  cat > "$WORKDIR/backup-manifest.json" <<MANIFEST
{"image":"$BACKUP_IMAGE","created_at":"$(date -u '+%Y-%m-%dT%H:%M:%SZ')"}
MANIFEST
  cp -a "$BACKUP_ARTIFACT_DIR/volumes" "$WORKDIR/volumes"
  cat > "$WORKDIR/Dockerfile" <<'DOCKERFILE'
FROM scratch
COPY volumes/ /backup/volumes/
COPY backup-manifest.json /backup/backup-manifest.json
DOCKERFILE
  docker build -t "$BACKUP_IMAGE" "$WORKDIR" >/dev/null
  log "Pushing backup image to registry: $BACKUP_IMAGE"
  docker push "$BACKUP_IMAGE"
  log "Backup complete. Image pushed as: $BACKUP_IMAGE"
  [[ "$BACKUP_IMAGE_WAS_EXPLICIT" -eq 0 ]] && log "Image name was auto-derived from hostname because no explicit backup image was provided."
  log "Saved lists: ./container_running_list and ./volume_list"
fi

if [[ "$MODE" == "restore" ]]; then
  validate_image_ref "$RESTORE_IMAGE"
  [[ "$DRY_RUN" -eq 1 ]] && { log "[DRY-RUN] Restore mode summary:"; log "[DRY-RUN] Source image: $RESTORE_IMAGE"; log "[DRY-RUN] (Skipping data inspection in dry-run)"; exit 0; }

  log "Pulling backup image: $RESTORE_IMAGE"
  docker pull "$RESTORE_IMAGE"
  ! is_digest_ref "$RESTORE_IMAGE" && log "Warning: restore image is not digest-pinned; proceed only if the source is trusted."
  docker image inspect "$HELPER_IMAGE" >/dev/null 2>&1 || { echo "Helper image $HELPER_IMAGE is not available locally. Pin and pre-pull a trusted digest before using this skill." >&2; exit 1; }

  log "Copying encrypted archives out of image without running its command path..."
  RESTORE_CONTAINER_NAME="restore-$(date +%s)"
  # Provide a dummy command (even if it doesn't exist) to satisfy Docker create for images with no CMD
  docker create --name "$RESTORE_CONTAINER_NAME" "$RESTORE_IMAGE" /bin/sh >/dev/null
  docker cp "$RESTORE_CONTAINER_NAME:/backup/volumes" "$WORKDIR/volumes"
  docker rm -f "$RESTORE_CONTAINER_NAME" >/dev/null
  RESTORE_CONTAINER_NAME=""

  log "Discovering volumes from image structure..."
  ls "$WORKDIR/volumes" | sed 's/\.tar\.gz\.enc$//' > "$WORKDIR/volume_list.discovered"
  mapfile -t VOLUMES < "$WORKDIR/volume_list.discovered"
  printf '%s\n' "${VOLUMES[@]}" > volume_list
  [[ ${#VOLUMES[@]} -gt 0 ]] || { echo "No volumes discovered inside backup image." >&2; exit 1; }

  for volume in "${VOLUMES[@]}"; do
    log "Restoring volume: $volume"
    docker volume create "$volume" >/dev/null
    RESTORE_STAGING="$WORKDIR/restore-staging/$volume"
    mkdir -p "$RESTORE_STAGING"
    openssl enc -d -aes-256-cbc -pbkdf2 -pass env:ENCRYPT_PASSWORD -in "$WORKDIR/volumes/${volume}.tar.gz.enc" | tar xzf - -C "$RESTORE_STAGING"
    docker run --rm -v "$volume:/target" -v "$RESTORE_STAGING:/source:ro" "$HELPER_IMAGE" sh -lc 'cp -a /source/. /target/'
  done
  log "Restore complete. Restored volumes listed in ./volume_list"
fi
