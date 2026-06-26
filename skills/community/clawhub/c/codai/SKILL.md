---
name: Codai
slug: codai
version: 1.0.0
description: "Orchestration skill for the codai-dev local environment. Routes user commands to the right plugin (proxy-manager, mysql-manager, postgres-manager, redis-manager, worktree-manager). Use when the user asks to manage any part of the dev environment without specifying which plugin."
changelog: Initial release.
triggers:
  - "subir mysql"
  - "subir postgres"
  - "subir redis"
  - "subir proxy"
  - "subir ambiente"
  - "start mysql"
  - "start postgres"
  - "start redis"
  - "start environment"
  - "criar worktree"
  - "create worktree"
  - "remover worktree"
  - "remove worktree"
  - "dump main para"
  - "dump main to"
  - "subir worktree"
  - "parar instância"
  - "listar instâncias"
  - "status do ambiente"
  - "environment status"
  - "codai"
metadata: {"clawdbot":{"emoji":"⚙️","requires":{"bins":["docker","git"]},"os":["linux","darwin"]}}
---

# Codai

Orchestration skill for the codai-dev local development environment. Routes user requests to the correct plugin without requiring the user to remember which script handles what.

## Plugin Map

| What user asks | Plugin | Command |
|----------------|--------|---------|
| subir/start MySQL | `mysql-manager` | `./mysql/run.sh start` |
| parar/stop MySQL | `mysql-manager` | `./mysql/run.sh stop` |
| status MySQL | `mysql-manager` | `./mysql/run.sh status` |
| dump de main para `<x>` | `mysql-manager` | `./mysql/run.sh dump codai_main codai_<x>` |
| subir/start PostgreSQL | `postgres-manager` | `./postgres/run.sh start` |
| parar/stop PostgreSQL | `postgres-manager` | `./postgres/run.sh stop` |
| dump postgres para `<x>` | `postgres-manager` | `./postgres/run.sh dump codai_main codai_<x>` |
| subir/start Redis | `redis-manager` | `./redis/run.sh start` |
| parar/stop Redis | `redis-manager` | `./redis/run.sh stop` |
| flush Redis | `redis-manager` | `./redis/run.sh flush` |
| subir/start proxy | `proxy-manager` | `./nginx-proxy/run.sh start` |
| conectar proxy `<x>` | `proxy-manager` | `./nginx-proxy/run.sh connect <x>` |
| criar worktree `<x>` | `worktree-manager` | `./run.sh create-worktree <x>` |
| subir worktree `<x>` | `worktree-manager` | `./run.sh start <x>` |
| parar worktree `<x>` | `worktree-manager` | `./run.sh stop <x>` |
| remover worktree `<x>` | `worktree-manager` | `./run.sh remove-worktree <x>` |
| listar instâncias | `worktree-manager` | `./run.sh list` |
| status geral | todos | run each `status` in order |

## Plugin Locations in codai-dev-base

```
codai-dev-base/
├── run.sh                  # worktree-manager entry point
├── mysql/run.sh            # mysql-manager
├── nginx-proxy/run.sh      # proxy-manager
└── .claude/skills/         # all plugin SKILL.md files
```

Redis and PostgreSQL are optional extras — install their directories when needed.

## Startup Order

Always follow this sequence:

```bash
./nginx-proxy/run.sh start      # 1. creates nginx-proxy_net network
./mysql/run.sh start            # 2. MySQL joins the network
./run.sh start main             # 3. main app instance (seeds db, starts containers, connects proxy)
```

For Redis or Postgres (if in use):
```bash
./redis/run.sh start
./postgres/run.sh start
```

## Multi-Step Workflows

### Create and start a new worktree from scratch
```bash
./run.sh create-worktree <name>   # creates branch worktree/<name>, .worktrees/<name>, .env.worktree-<name>
./run.sh start <name>             # creates db, dumps codai_main→codai_<name>, starts containers, connects proxy
```
Result: `http://<name>.frontend.localhost` and `http://<name>.backend.localhost`

### Dump main database to a feature branch
```bash
./mysql/run.sh dump codai_main codai_<name>
# For PostgreSQL:
./postgres/run.sh dump codai_main codai_<name>
```

### Remove a worktree completely (confirm first)
Confirm: "Remover worktree '<name>'? Isso apaga os containers, banco de dados, git worktree (branch `worktree/<name>`) e o env file."
```bash
./run.sh remove-worktree <name>
```

### Full environment status
```bash
./run.sh list                   # worktrees + infra status
./mysql/run.sh status           # MySQL databases
./nginx-proxy/run.sh status     # proxy routes
```

## Rules

- **Always confirm** before `remove-worktree` — it is irreversible.
- **Always report URLs** after starting a worktree: frontend and backend.
- **Check infra first**: if MySQL or proxy is not running, start them before trying to start an instance.
- **Startup order matters**: proxy → databases → app instances.
- If the user says "sobe tudo" or "start everything", start in order: proxy → mysql → run.sh start main.
- Never run `./mysql/run.sh drop-db codai_main` — it is the source of truth.

## Environment Variables (shared across plugins)

| Variable          | Default             | Used by                            |
|-------------------|---------------------|------------------------------------|
| `MYSQL_CONTAINER` | `codai_db`          | mysql-manager, worktree-manager    |
| `MYSQL_ROOT_PASS` | `secret`            | mysql-manager, worktree-manager    |
| `MYSQL_MAIN_DB`   | `codai_main`        | mysql-manager, worktree-manager    |
| `PROXY_CONTAINER` | `codai_nginx_proxy` | proxy-manager, worktree-manager    |
| `CODAI_NETWORK`   | `nginx-proxy_net`   | all plugins                        |
| `PROJECT_PREFIX`  | `codai-dev`         | proxy-manager, worktree-manager    |
