---
name: fly-io
description: Deploy and manage applications on Fly.io using the flyctl CLI and Machines API. Use when asked to deploy an app, scale machines, check app status, view logs, manage secrets, create/destroy machines, set environment variables, run commands in a container, or manage Fly Postgres databases. Requires flyctl installed and authenticated via `fly auth login`.
---

# Fly.io Skill

Fly.io is managed via the `flyctl` CLI (alias: `fly`) and the Machines REST API.

## Auth
```bash
fly auth login          # opens browser
fly auth token          # print current token
export FLY_API_TOKEN=$(fly auth token)
```

## App Management
```bash
fly apps list                          # list all apps
fly status -a <app-name>               # app health + machine states
fly info -a <app-name>                 # app details, IPs, regions
fly open -a <app-name>                 # open in browser
```

## Deploy
```bash
fly deploy                             # deploy from current dir (uses fly.toml)
fly deploy --image registry/image:tag  # deploy a specific image
fly deploy --remote-only               # build remotely (no local Docker needed)
fly deploy -a <app-name>               # target specific app
```

## Logs
```bash
fly logs -a <app-name>                 # live log stream
fly logs -a <app-name> --no-tail       # recent logs, no follow
```

## Secrets
```bash
fly secrets set MY_KEY=value -a <app-name>
fly secrets list -a <app-name>
fly secrets unset MY_KEY -a <app-name>
```

## Scaling
```bash
fly scale count 3 -a <app-name>                    # set machine count
fly scale memory 512 -a <app-name>                 # set RAM (MB)
fly scale vm shared-cpu-2x -a <app-name>           # change VM size
fly scale show -a <app-name>                        # current scale
```

## Machines
```bash
fly machine list -a <app-name>
fly machine status <machine-id> -a <app-name>
fly machine restart <machine-id> -a <app-name>
fly machine stop <machine-id> -a <app-name>
fly machine destroy <machine-id> -a <app-name>
```

## Run a Command (one-off)
```bash
fly ssh console -a <app-name>                      # interactive shell
fly ssh console -a <app-name> -C "ls -la /app"    # run single command
```

## Postgres
```bash
fly postgres create --name myapp-db                # create Postgres cluster
fly postgres connect -a myapp-db                   # psql shell
fly postgres attach myapp-db -a <app-name>         # attach DB to app (sets DATABASE_URL)
```

## VM Sizes
`shared-cpu-1x` (256MB), `shared-cpu-2x` (512MB), `performance-1x` (2GB), `performance-2x` (4GB)

## Regions
`iad` (Virginia), `ord` (Chicago), `lax` (LA), `sea` (Seattle), `ams` (Amsterdam), `fra` (Frankfurt), `sin` (Singapore), `syd` (Sydney)

## Tips
- `fly.toml` is the app config — always check it before deploying
- `fly deploy --strategy rolling` for zero-downtime deploys
- Health checks in `fly.toml` under `[checks]` block
