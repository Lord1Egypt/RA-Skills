---
name: docker-container-rerun-all
description: Sequentially check and optionally update all docker run containers that already have fixed recreate commands recorded in long-term memory. Use when the user wants a batch refresh of remembered docker-run-managed containers, wants dynamic discovery from MEMORY.md instead of a hardcoded list, and wants the results grouped into updated, already up-to-date, and failed containers with image tag and image Id change details.
---

# Docker Container Rerun All

Batch-check remembered `docker run` containers conservatively.

Use this skill to discover every container that already has a fixed recreate command recorded in long-term memory, then process them one by one with the same image-Id comparison workflow used by `docker-container-rerun`.

## Preconditions

Use this skill only when all of the following are true:

1. The target containers were originally created with `docker run`, not `docker compose`.
2. Each target container already has a full fixed recreate command recorded in `MEMORY.md`.
3. The sibling skill `docker-container-rerun` is installed and available locally.
4. The current machine can run Docker commands against the target Docker daemon.
5. The user understands that `--apply` may stop, remove, and recreate containers when image Ids changed.

Do not use this skill when recreate commands are missing, incomplete, reconstructed from memory, or only partially known.

## Dependencies

This skill has two explicit dependencies:

- sibling skill: `docker-container-rerun`
- long-term memory file: `MEMORY.md`

### Required sibling skill

This skill calls the bundled script from the sibling skill directory:

- `../docker-container-rerun/scripts/update_docker_run_container.py`

If `docker-container-rerun` is missing or broken, fix that first before using this skill.

### Required MEMORY.md structure

This skill parses container recreate commands from the section header below inside `MEMORY.md`:

```md
## 已记住的 Docker 容器固定重建命令
```

Under that section, each remembered container entry should include:

1. a list item whose bold label contains the container name in backticks
2. descriptive text mentioning `docker run`
3. a fenced `bash` code block containing the exact recreate command

Example entry using `autoheal`:

```md
## 已记住的 Docker 容器固定重建命令

- **`autoheal`**：固定 docker run 重建命令
```bash
docker run -d \
  --name autoheal \
  --restart unless-stopped \
  -e AUTOHEAL_CONTAINER_LABEL=all \
  -e AUTOHEAL_INTERVAL=30 \
  -e AUTOHEAL_START_PERIOD=300 \
  -e CURL_TIMEOUT=30 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  willfarrell/autoheal:latest
```
```

Keep the recreate command exact. Do not rewrite it from `docker inspect`, and do not omit flags that matter.

## Apply Modes

This skill supports two modes:

### Non-apply mode (default)

Command:

```bash
python3 scripts/run_all_docker_reruns.py
```

Behavior:

- reads `MEMORY.md`
- discovers remembered containers dynamically
- pulls the latest image for each remembered container
- compares current image Id vs latest image Id
- reports which containers need recreation
- does **not** stop, remove, or recreate any container

Use this mode when the user wants a safe inspection pass first.

### Apply mode

Command:

```bash
python3 scripts/run_all_docker_reruns.py --apply
```

Behavior:

- performs the same checks as non-apply mode
- for containers whose image Id changed, runs the sibling `docker-container-rerun` apply workflow
- may stop, remove, and recreate matching containers sequentially
- leaves already up-to-date containers unchanged

Use this mode only when the user explicitly wants real container recreation.

## Workflow

1. Read `MEMORY.md` and locate the section that stores fixed recreate commands for remembered `docker run` containers.
2. Build the working container list dynamically from memory.
   - Do not hardcode container names in the skill logic.
   - If the user adds more remembered recreate commands later, include them automatically.
3. For each discovered container, preserve the exact remembered `docker run` command.
4. Process containers sequentially, never in parallel.
5. Use the bundled script to run the same check/apply workflow as `docker-container-rerun` for each container.
6. Report results in three groups with polished Chinese wording:
   - 已更新
   - 已是最新
   - 执行失败
7. For every updated container, include:
   - container name
   - image reference
   - image tag
   - previous image Id
   - latest image Id
   - version hint when the image tag contains a meaningful version string
8. Prefer a Telegram-friendly Chinese summary instead of dumping raw JSON directly to the user.

## Safety Rules

- Treat `MEMORY.md` as the source of truth for the container list and fixed recreate commands.
- Do not reconstruct missing flags from `docker inspect`.
- Do not silently edit remembered `docker run` commands.
- Run containers one by one in sequence.
- If memory parsing fails for a container, put it in the failed group and continue with the next one.
- If the user asked only to create the skill, do not execute updates.
- When actual recreation is requested later, use `--apply` explicitly.

## Bundled Script

Use the bundled script for deterministic batch execution from the skill directory:

```bash
python3 scripts/run_all_docker_reruns.py
```

Add `--apply` only when the user explicitly wants to recreate containers that need updates:

```bash
python3 scripts/run_all_docker_reruns.py --apply
```

The script will:

- parse remembered containers from `MEMORY.md`
- discover the current container set dynamically
- call the bundled `docker-container-rerun` script once per container
- keep execution sequential
- emit JSON with discovered containers, raw per-container results, and grouped summary

## Output Format

Prefer a compact Chinese grouped report for chat surfaces.

### Recommended Chinese Template

Use a detailed Chinese report by default.
Append a final `重点异常提示` section that highlights failed containers, non-running containers, and health states like `starting` or `unhealthy`.

```text
Docker 容器批量检查结果

本次共处理：<total> 个容器
- 已更新：<updated_count> 个
- 已是最新：<up_to_date_count> 个
- 执行失败：<failed_count> 个

【本次发现的容器】
1. <container_name> - <image>
2. <container_name> - <image>
...

【已更新】
1. <container_name>
   - 镜像：<image>
   - Tag：<tag>
   - Image Id：<old_id> → <new_id>
   - 版本提示：<version_hint_or_无>
   - 当前状态：<status>
   - 健康检查：<health_or_无>
   - 最近日志：<logs_tail_or_无>

【已是最新】
1. <container_name>
   - 镜像：<image>
   - Tag：<tag>
   - Image Id：<same_id>
   - 当前状态：<status>
   - 健康检查：<health_or_无>

【执行失败】
1. <container_name>
   - 原因：<error>

【重点异常提示】
1. <container_name>
   - 异常类型：<health_or_status_or_failure>
   - 说明：<short_reason>
```

### Updated

For each updated container, report:

- `container_name`
- `image`
- `tag`
- `current_image_id -> latest_image_id`
- `version_hint` when available
- post-update container status and health if available

### Already Up To Date

For each unchanged container, report:

- `container_name`
- `image`
- `tag`
- unchanged image Id

### Failed

For each failure, report:

- `container_name`
- failure reason

## Notes

- This skill intentionally depends on `MEMORY.md` instead of a hardcoded container list.
- This skill intentionally depends on the sibling `docker-container-rerun` skill for the single-container check/apply workflow.
- Relative paths are used so the skill remains portable after installation, as long as both skill directories keep their normal sibling layout.
