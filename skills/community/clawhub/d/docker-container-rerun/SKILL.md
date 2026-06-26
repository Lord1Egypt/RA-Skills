---
name: docker-container-rerun
description: Safely check whether a Docker container's image has changed and, only when needed, recreate that docker run container with a user-provided original docker run command. Use when updating an existing Docker container managed by docker run, especially when the user provides a fixed recreate_command and wants image Id (sha256) comparison before pull/recreate. Do not use for docker compose, automatic command reconstruction, volume pruning, or speculative container changes.
---

# Docker Container Rerun

Update a `docker run` container with a conservative workflow.

## Required Inputs

Require both of these from the user:

- `container_name`
- `recreate_command`

Treat `recreate_command` as the source of truth. Do not try to reconstruct missing flags from `docker inspect`.

## Scope

Support only containers originally managed by `docker run`.

Do not use this skill for:

- `docker compose`
- guessing or synthesizing missing run flags
- deleting volumes
- `docker system prune`
- changing environment variables, mounts, ports, labels, or networks unless the user explicitly changed the recreate command

## Update Rule

Always compare image **Id** values, not repo digests.

Use this exact logic:

1. Read current image Id from the running container:
   ```bash
   docker inspect -f '{{.Image}}' <container_name>
   ```
2. Extract the image reference from `recreate_command`.
3. Pull the latest version of that image:
   ```bash
   docker pull <image>
   ```
4. Read the latest local image Id:
   ```bash
   docker image inspect <image> --format '{{.Id}}'
   ```
5. Recreate the container only if the two Id values differ.

## Safety Rules

Before any destructive action, restate the exact recreate command that will be used.

If `recreate_command` is missing, ambiguous, or not clearly a `docker run` command, stop and ask the user to provide a valid full command.

If the image cannot be extracted from `recreate_command`, stop and ask the user to provide the image explicitly inside the command.

Never silently modify the recreate command.

Prefer this sequence when update is needed:

```bash
docker stop <container_name>
docker rm <container_name>
<recreate_command>
```

## Validation of recreate_command

Before using it, verify all of the following:

- starts with `docker run`
- includes an image name as the final image argument before any container command
- clearly targets the same logical container the user wants updated

If the command includes an inline container command after the image, preserve it exactly.

If the command is multiline, preserve it exactly.

## Recommended Execution Workflow

1. Confirm the target container name.
2. Echo back the exact recreate command.
3. Extract the image from the recreate command.
4. Compare current image Id and latest pulled image Id.
5. If Ids match, report that the container is already up to date and do nothing else.
6. If Ids differ:
   - run `docker stop <container_name>`
   - run `docker rm <container_name>`
   - run the exact `recreate_command`
7. Verify startup with:
   ```bash
   docker ps --filter name=<container_name>
   docker inspect <container_name>
   docker logs --tail 100 <container_name>
   ```
8. Report status clearly, including whether healthcheck is `healthy`, `starting`, or absent.

## Bundled Script

Use the bundled script when you want a deterministic check/apply flow:

```bash
python3 scripts/update_docker_run_container.py \
  --container-name <container_name> \
  --recreate-command '<full docker run command>'
```

Add `--apply` only when the user has approved the exact recreate command and actual recreation should happen.

The script will:

- validate `recreate_command`
- extract the image
- pull the latest image
- compare current vs latest image Id
- optionally stop/remove/recreate
- emit JSON summary with container state, health status, and recent logs

## Output Expectations

When reporting results, include:

- target container name
- extracted image name
- current image Id
- latest image Id
- whether recreation was needed
- post-recreate container state
- health status if present
- any obvious log errors seen in recent logs

## Example Pattern

Input:

- `container_name`: `my-container`
- `recreate_command`:
  ```bash
  docker run -d --network host --name my-container --restart unless-stopped -v example_data:/data -v example_certs:/etc/ssl/certs -e DB_HOST=<db_host> -e DB_PORT=<db_port> -e DB_NAME=<db_name> -e DB_USER=<db_user> -e DB_PASSWORD=<db_password> --health-cmd="/bin/check-health" --health-interval=600s --health-retries=5 --health-timeout=3s example/image:latest
  ```

Expected behavior:

- extract image `example/image:latest`
- compare current container image Id vs pulled latest image Id
- recreate only if the Ids differ
- preserve the recreate command exactly

## Notes

When users ask to "update container X", prefer asking for the original `docker run` command unless it is already documented in memory or provided in the current request.

If the user has a known fixed recreate command for a specific container, prefer using that exact command unchanged.
