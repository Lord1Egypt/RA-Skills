# Tool Patterns

## Git

- Prefer `git push --force-with-lease` over `git push --force`
- Before force-push or reset, create a backup branch from `HEAD`
- Use `git clean -ndx` before `git clean -fdx`
- Use `git reflog` as the primary rollback path after destructive history edits

## Docker

- Review containers, images, and volumes before `docker system prune`
- Treat `docker system prune -a --volumes` as near-irreversible
- Prefer targeted `docker rm`, `docker image rm`, or `docker volume rm` over global prune

## kubectl

- Run `kubectl diff` or server-side dry run before `apply`
- Export current manifests before `delete`
- Capture workload names so `kubectl rollout undo` is available if deployment fails

## Terraform

- Run `terraform plan -out=tfplan` before `terraform apply`
- Back up state before high-impact changes
- Treat `terraform destroy` and broad `-target` usage as high-risk operations

## curl and wget

- Treat `curl | sh`, `wget | bash`, or remote PowerShell execution as `critical`
- Prefer download, inspect, verify checksum or signature, then execute

## Package Managers

- Before `npm install`, `pip install`, or `cargo add`, note manifest and lockfile changes
- Prefer commit or backup of lockfiles before bulk dependency updates

## File Operations

- Quote exact paths instead of relying on broad wildcards
- Resolve relative targets before delete, move, or overwrite
- Prefer move-to-quarantine or rename-first workflows over direct deletion
