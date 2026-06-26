---
name: docker-encyclopedia
description: >-
  Docker documentation-first workflow for Docker-specific questions,
  troubleshooting, command planning, image/build work, container/runtime
  operations, Compose behavior, networking, volumes, registries, and
  diagnostics. Use when the request is clearly about Docker itself: the
  `docker` CLI, Docker Engine, Dockerfiles, BuildKit/buildx, Docker Compose,
  images, containers, registries, volumes, networks, contexts, rootless
  Docker, or Docker Desktop/Engine behavior where Docker-specific semantics
  matter. Do not use for generic Linux administration, generic OCI/container
  theory, generic shell work, or Kubernetes/orchestration questions unless the
  Docker layer is specifically what is being discussed or debugged.
metadata: {"openclaw":{"emoji":"🐳","homepage":"https://docs.docker.com/"}}
---

# Docker Encyclopedia

## Overview

Use a docs-first workflow for Docker work. Prefer the official Docker documentation at `https://docs.docker.com/`, consult cached local copies under `.Docker-Encyclopedia/` before re-fetching, and record useful official-doc excerpts plus environment-specific operational learnings so future work gets faster and safer.

This skill is for the **Docker product/runtime layer**. It should trigger for real Docker behavior, configuration, build/runtime, and operational questions — not for generic Linux admin work, generic container theory, or generic orchestration talk where Docker-specific semantics are not the real issue.

## Workflow

1. **Classify the task**
   - Decide whether the task is a Docker question, troubleshooting task, command-planning task, image/build task, Compose review, runtime review, or live operational task.
   - Use this skill when the request is specifically about Docker product behavior, Docker CLI semantics, Docker build/runtime behavior, Docker Compose behavior, image/container lifecycle, or Docker-specific networking/storage/registry details.
   - Do not use this skill for generic shell work, generic Linux admin, generic OCI/container theory, or Kubernetes questions unless the Docker layer is specifically in play.

2. **Check local cache first**
   - Use `.Docker-Encyclopedia/` as the local knowledge/cache root.
   - Check these locations first when relevant:
     - `.Docker-Encyclopedia/docs/docs.docker.com/...`
     - `.Docker-Encyclopedia/notes/components/...`
     - `.Docker-Encyclopedia/notes/patterns/...`
     - `.Docker-Encyclopedia/inventory/...`
   - If a cached page or note already answers the question well enough, use it.

3. **Consult official Docker docs before answering or touching the system**
   - Before answering direct or indirect Docker questions that depend on command syntax, feature boundaries, configuration semantics, builder/runtime behavior, storage/network semantics, or version-sensitive details, consult the official docs unless the answer is already well-supported by the local cache.
   - Before performing direct Docker CLI or configuration work, consult the relevant docs first when:
     - the exact command path matters
     - build/runtime semantics are easy to misremember
     - the action could affect running containers, images, volumes, networks, registries, credentials, or host reachability
   - Do not improvise high-impact Docker commands or config changes from memory when the docs are easy to check.

4. **Cache consulted docs locally**
   - When you consult a Docker docs page, save a normalized markdown/text cache copy under `.Docker-Encyclopedia/docs/docs.docker.com/...`.
   - Mirror the official docs path structure as much as practical.
   - Cache only pages actually consulted; do not try to mirror the whole docs site eagerly.
   - Use `scripts/cache_doc.py` when appropriate.

5. **Separate official documentation from local observations**
   - Store official-doc-derived material under `.Docker-Encyclopedia/docs/...`.
   - Store environment-specific operational knowledge under:
     - `.Docker-Encyclopedia/notes/components/`
     - `.Docker-Encyclopedia/notes/patterns/`
     - `.Docker-Encyclopedia/inventory/`
   - Distinguish clearly between:
     - official documented behavior
     - observed local configuration/state
     - inferred best-practice guidance

6. **Record useful local learnings**
   - After useful live work, save durable notes such as:
     - host-specific Docker layout and runtime conventions
     - recurring build/runtime/debugging patterns
     - image/registry/credential-helper gotchas
     - Compose/deployment conventions
     - safe/unsafe operational boundaries for the environment
   - Prefer concise durable notes over re-learning the same Docker details later.

## Live Work Rules

- Treat official Docker docs lookup as the default preflight for non-trivial Docker work.
- Prefer read/inspect first when entering a Docker area you have not recently reviewed.
- Treat image pruning, volume/network changes, Compose deployments, builder/registry config, daemon config, and credential-handling paths as high-sensitivity areas.
- When uncertainty remains after checking cache + docs, say so and avoid bluffing.
- When answering a question, mention when useful whether the answer comes from cached official docs, a fresh official docs lookup, or live observed environment state.

## Data Root

Use this workspace-local root for cache and notes:

- `.Docker-Encyclopedia/`

Expected structure:

- `.Docker-Encyclopedia/docs/docs.docker.com/...`
- `.Docker-Encyclopedia/notes/components/...`
- `.Docker-Encyclopedia/notes/patterns/...`
- `.Docker-Encyclopedia/inventory/...`

Use `scripts/init_workspace.py` to create or repair the expected directory structure.

## Note Destinations

- Component-specific observations → `.Docker-Encyclopedia/notes/components/<component-name>.md`
- Reusable Docker patterns/gotchas → `.Docker-Encyclopedia/notes/patterns/<topic>.md`
- Environment-wide deployment/access info → `.Docker-Encyclopedia/inventory/*.md`
- Cached official docs → `.Docker-Encyclopedia/docs/docs.docker.com/...`

## Secrets / Sensitive Data

- Do not store plaintext credentials, API keys, session tokens, private URLs, recovery codes, or other secrets in the encyclopedia notes/inventory tree.
- If a note needs to mention access details, keep it high-level and redact or omit secret material.
- Treat these workspace notes as operational memory, not as a secrets vault.

## Resources

- `scripts/init_workspace.py` — create or repair the `.Docker-Encyclopedia/` directory tree.
- `scripts/cache_doc.py` — fetch and cache a consulted official Docker docs page under `.Docker-Encyclopedia/docs/...`.
- `references/workflow.md` — detailed operating workflow and evidence-handling rules.
- `references/cache-layout.md` — canonical `.Docker-Encyclopedia/` directory structure.
- `references/topic-map.md` — useful Docker topic groupings for faster doc lookup.

## Good Outcomes

- Answer a Docker question using cached or freshly checked official docs instead of guesswork.
- Inspect a live Docker environment after checking the relevant docs and record any new local operational knowledge.
- Build a growing local Docker knowledge cache that makes later work faster, safer, and more grounded.
- Turn one-off Docker discoveries into durable notes so future work does not rediscover them from scratch.

## Avoid

- Answering Docker-specific questions purely from memory when docs are easy to consult.
- Treating local observed behavior as if it were guaranteed official documented behavior.
- Dumping large amounts of low-value docs into the workspace without a reason.
- Writing component-specific observations into the official-doc cache tree.
- Making high-impact live changes before checking the relevant docs when exact behavior matters.
