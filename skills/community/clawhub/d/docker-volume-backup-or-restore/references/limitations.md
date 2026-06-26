# Limitations and Tradeoffs

## Fit
- Use this workflow when you want a registry-only migration path for Docker volumes.
- Use it when you accept the cost of packing all local volumes into one encrypted backup image.
- Use it when the source and destination machines can both access the same Docker registry account.

## Tradeoffs
- Large total volume size can make `docker commit`, `docker push`, and `docker pull` slow and fragile.
- Registry upload/download interruptions may force you to retry long transfers.
- Free Docker Hub plans typically have limited private-repository capacity, so sensitive backups may not fit your plan.
- The skill backs up Docker volumes only. It does not capture bind mounts, container definitions, Compose files, environment files, networks, secrets, or host-level configuration.
- Backup consistency depends on stopping currently running containers first. If data is also being changed outside Docker-managed containers, the archive may still miss in-flight writes.
- Restore overwrites the contents of same-named target volumes.

## Security
- Data is encrypted with `openssl enc -aes-256-cbc -pbkdf2` before being stored inside the backup image.
- Anyone without `BACKUP_PASS` should not be able to restore the payload.
- The encrypted archive still lives inside an image layer, so you must still treat the pushed image as sensitive material and keep the registry repository private.

## Operational Notes
- Backup mode requires an explicit image reference from the caller, such as `docker.io/yourname/backup-host:tag`.
- The repository name itself must already be valid for your logged-in registry context before pushing.
- This design is more portable for public skill users because it avoids hidden assumptions about namespace or hostname-derived tags.
