# runbook-generator — Status

**Price:** $59
**Status:** Ready
**Created:** 2026-04-01

## Description
Generate operational runbooks by scanning project infrastructure files. Produces structured Markdown runbooks with start/stop/restart/deploy/rollback/troubleshoot/monitoring procedures.

## Features
- Scans 7 file types: Dockerfile, docker-compose.yml, systemd units, Makefile, package.json, .env, nginx.conf
- Dockerfile: base image, exposed ports, multi-stage builds, healthchecks, env vars
- Docker Compose: services, ports, volumes, dependencies, restart policies
- systemd: ExecStart/Stop/Reload, dependencies, restart policy, env files
- Makefile: target extraction (build, test, deploy, clean)
- package.json: scripts, engines, metadata
- .env: variable detection with value masking
- nginx: listen ports, server names, upstreams, locations
- 11 runbook sections generated automatically
- 2 output formats (markdown, JSON)
- File output with -o flag
- Pure Python stdlib (no dependencies)

## Tested Against
- OpenClaw npm package (package.json detected, scripts extracted)
- Docker multi-service project (Dockerfile + compose + .env + Makefile)
- JSON output verified
