---
name: dokploy
description: Use for Dokploy-specific API operations (apps, deployments, databases, domains, backups, settings) when tasks explicitly involve Dokploy. Route requests to domain modules, enforce inspect-first troubleshooting and controlled mutations via x-api-key authentication, and avoid use for generic Docker/Kubernetes work outside Dokploy.
---

# Dokploy API Skill

Use this skill to operate Dokploy through its API schema and generated domain modules.

## Scope guardrails

- Use this skill only when the task is explicitly about Dokploy.
- Do not use this skill for generic Docker/Kubernetes guidance unless Dokploy endpoints are involved.
- Authenticate with `x-api-key` header.
- Prefer minimal, reversible changes.

## Routing (module-first)

Start at `modules/_index.md`, then load only the smallest matching module.

Common routes:
- Applications/deployments: `modules/application.md`, `modules/deployment.md`, `modules/rollback.md`
- Databases: `modules/mysql.md`, `modules/postgres.md`, `modules/redis.md`, `modules/mongo.md`, `modules/mariadb.md`
- Networking/TLS: `modules/domain.md`, `modules/redirects.md`, `modules/certificates.md`, `modules/port.md`
- Platform settings/security/backups: `modules/settings.md`, `modules/security.md`, `modules/backup.md`
- Git providers: `modules/github.md`, `modules/gitlab.md`, `modules/bitbucket.md`, `modules/gitea.md`, `modules/gitprovider.md`

## Standard execution flow (required)

1. **Classify intent** and choose module by operation family.
2. **Resolve identifiers first** using read/list/search endpoints.
3. **Preflight checks**: required fields, scope, target existence, dependency impact.
4. **Mutate minimally** with the smallest payload required.
5. **Verify outcome** using read/status/search endpoints.
6. **Recover if needed** using rollback/redeploy/restart operations where available.

Do not run destructive actions unless user intent is explicit.

## Mutation safety policy

For create/update/delete/deploy/stop/restart actions, always enforce:

- inspect before mutate
- verify after mutate
- report exact operation IDs used
- include clear rollback/recovery next step on failure

If required fields are unknown, stop and fetch them from relevant read/list endpoints first.

## Secret handling

- Never echo raw API keys or tokens in user-visible output.
- Redact secrets in logs and summaries.
- Prefer environment/secure config storage over inline literals.

## References

- Domain index: `modules/_index.md`
- API snapshot: `openapi.json`
- Auth/profile source: Dokploy user profile token + `x-api-key`
