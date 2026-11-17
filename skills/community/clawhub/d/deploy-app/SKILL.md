---
name: deploy-app
description: "Deploy a project from a git repository onto AgentsPodium: frontend and backend on one pod, behind one domain, with a persistent disk. Use when you are asked to ship an app somewhere, or to move a site off Netlify or Vercel without splitting the backend into functions."
version: 1.0.0
license: MIT
metadata:
  tags: [deployment, hosting, git, frontend, backend, static-site, ci]
---

# Deploying an app on AgentsPodium

One pod runs both halves of a web project: the frontend build is served as
static files, the backend runs as an ordinary process next to it, and one
proxy inside the pod puts them behind a single domain with TLS. The disk
survives rebuilds. There is no split into functions and no per-service bill.

**Status, 2026-09-13.** Verified on live pods: a private GitLab repository and
a public GitHub monorepo, both Expo web builds inside a `small` pod, served
over HTTPS on their own hostname. `node` and static output are the tested
paths; `python`, `go` and `docker` runtimes are written but not yet proven, so
check `GET /agents/:id/build` rather than assuming.

Base URL for everything below:

```
https://agentspodium.com/api
```

Errors are always `{"error":"CODE","message":"..."}`.

## 1. Get a key once

Ask your operator for an API key from https://agentspodium.com/account
("API keys for agents"). It looks like `ak_live_…` and goes on every call:

```
Authorization: Bearer ak_live_…
```

An e-mail code also works (`POST /auth/request`, then `POST /auth/verify`),
but it needs a mailbox. The key does not.

## 2. Describe the project

Everything the pod needs to build and run the project goes in one `app`
object. Only `repo` is required; the rest has defaults or is detected.

| field | meaning | default |
|---|---|---|
| `repo` | https git URL. SSH remotes are not supported | required |
| `branch` | branch to build | `main` |
| `rootDir` | directory the build runs in, for a monorepo | repository root |
| `runtime` | `node`, `python`, `go`, `static`, `docker` | detected from the repo |
| `buildCommand` | how to build | default for the detected runtime |
| `outputDir` | static output, **relative to `rootDir`** | none |
| `startCommand` | backend process | none |
| `appPort` | port the backend listens on inside the pod | `3000` |
| `apiPrefix` | paths routed to the backend; the rest is served static | `/api` |
| `env` | environment variables for the app | `{}` |
| `repoToken` | token for a private repository | none |
| `repoUser` | username paired with the token | what the host expects |

Set `outputDir`, `startCommand`, or both. A pod with neither serves nothing,
and the API says so rather than creating it.

## 3. Create it

`engine` is `app`, and the smallest plan is `small`: the build runs inside
the pod, so the plan is also the build machine, and `npm ci` on 1 GB does not
finish.

A real example — an Expo web app in a monorepo, static only, private repo on
a self-hosted Forgejo:

```bash
curl -s -X POST https://agentspodium.com/api/agents \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{
    "engine": "app",
    "tier": "small",
    "personaId": "personal-assistant",
    "name": "hq-app",
    "app": {
      "repo": "https://git.defispace.com/hq/app",
      "branch": "main",
      "rootDir": "app",
      "buildCommand": "npm ci && npx expo export -p web",
      "outputDir": "dist",
      "repoToken": "…"
    }
  }'
```

A fullstack example — React frontend and a Node API in the same repository:

```json
{
  "engine": "app", "tier": "small", "personaId": "personal-assistant",
  "app": {
    "repo": "https://github.com/owner/project",
    "buildCommand": "npm ci && npm run build",
    "outputDir": "dist",
    "startCommand": "node server/index.js",
    "appPort": 3000,
    "apiPrefix": "/api",
    "env": { "NODE_ENV": "production" }
  }
}
```

The reply is `{"agent":{…}}`. Keep `agent.id`. The pod answers at
`agent.endpointUrl`; `agent.app` shows the configuration as stored, and
`agent.appRepoTokenEnc` is `"set"` or `null` — the token itself never comes
back.

## 4. Watch the build, not the pod

```bash
curl -s https://agentspodium.com/api/agents/$ID/build -H "Authorization: Bearer $TOKEN"
# {"build":{"state":"building|ok|failed|unknown","commit":"abc1234",
#           "startedAt":"…","finishedAt":"…","logTail":"last lines"}}
```

A pod can be alive and still serving the previous version while a new build
fails, so pod health is not build health. `logTail` carries the reason.
Poll every five seconds; a first build with a cold cache takes minutes.

## 5. Your own domain

Point an A record at `138.199.136.33`, then send `domain` on create or set it
later on the agent page. `GET /api/domains/check?domain=<name>&https=1` says
whether DNS points here and whether HTTPS already answers. The certificate is
issued automatically once the record resolves. Names under `agentspodium.com`
are refused: every pod already gets one.

## 6. Ship a new version of an app that already exists

This is the common case: the project is already deployed, you pushed a commit,
now make the pod serve it. Two things are needed and nothing else — the API
key, and the id of the instance.

If you do not have the id, list what the key can see:

```bash
curl -s https://agentspodium.com/api/agents -H "Authorization: Bearer $TOKEN"
# {"agents":[{"id":"agt_…","name":"hq-app","engine":"app","status":"running",
#             "endpointUrl":"https://…","app":{"repo":"…","branch":"main",…}}]}
```

Match on `engine: "app"` and the `app.repo` you just pushed to. Then:

```bash
curl -s -X POST https://agentspodium.com/api/agents/$ID/rebuild -H "Authorization: Bearer $TOKEN"
curl -s https://agentspodium.com/api/agents/$ID/build -H "Authorization: Bearer $TOKEN"
```

`rebuild` fetches the latest commit on the configured branch, runs the build
again and reloads the pod's routing. The disk is kept, so `node_modules` and
framework caches survive and the second build is much faster than the first.
Poll `/build` until `state` is `ok` or `failed`; on `failed`, `logTail` says
why, and the site keeps serving the previous version in the meantime.

Nothing else is required. The token, the branch and the build command are
already stored on the instance.

## 7. Change the configuration, then rebuild

```bash
# point at another branch, fix the build command, replace the token
curl -s -X PATCH https://agentspodium.com/api/agents/$ID/app \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"branch":"release","buildCommand":"npm ci && npm run build:prod"}'

# apply it: rebuild from the latest commit, keeping the disk
curl -s -X POST https://agentspodium.com/api/agents/$ID/rebuild -H "Authorization: Bearer $TOKEN"
```

The PATCH answers `"applied":"on the next rebuild"` because the pod reads the
configuration when it starts. Nothing changes until you rebuild.

## 8. Private repositories

Send `repoToken` with a token that can read the repository. It is encrypted
at rest, handed to the pod at deploy time, and never returned.

`repoUser` you can leave out. Forges disagree about what goes next to a token
— GitHub takes `x-access-token`, GitLab `oauth2`, Bitbucket `x-token-auth`,
Gitea and Forgejo the token alone — and a self-hosted GitLab is
indistinguishable from a self-hosted Gitea by its URL. The pod tries the forms
in turn and keeps the one the server accepts; the build log names it. Send
`repoUser` only to skip that.

Know what you are agreeing to: the token lives in the pod's environment, and
the code you deploy runs in that pod. It is your own repository token, but
anything you deploy can read it. Use a token scoped to that one repository.

## 9. Instead of polling

Send `webhookUrl` on create and the platform POSTs signed events instead:
`agent.running`, `agent.stopped`, `agent.failed`, `agent.deleted`,
`payment.confirmed`, `deletion.warning`. The signing secret comes back once
as `webhookSecret`. See https://hosting.defispace.com/docs/webhooks.md

## 10. What goes wrong

- **`Engine "app" needs app.repo`** — `engine: "app"` without the `app`
  object. The two travel together.
- **`App requires at least the small plan`** — `tier: "tiny"`. The build runs
  in the pod; 1 GB is not enough to install a frontend's dependencies.
- **`outputDir must be a path inside the repository`** — a leading `/` or a
  `..` segment. Paths are relative to `rootDir`.
- **`Set outputDir, startCommand, or both`** — nothing to serve and nothing
  to run. One of them has to be there.
- **`Repository URL must use https`** — `git@host:owner/repo.git` is not
  accepted. Use the https URL and a token for private repositories.
- **Build `failed` with an empty `logTail`** — the build produced no output
  before dying, usually out of memory. Move to a bigger plan and rebuild.
- **`Could not fetch the repository`** — for a private one, the token cannot
  read it, or it has expired. The log shows the attempt with the token
  replaced by `***`; git prints the URL it tried on an auth failure, so it is
  masked on the way out rather than trusted not to appear.
- **Pod answers, site is blank** — `outputDir` points at a directory the
  build did not produce. Check the build log for where the output went.

## 11. Everything else

An app instance is an instance like any other: `GET /agents/:id` for status,
`/liveness`, `/usage`, `/term` for when it expires, pause, resume, delete,
export, and the payment endpoints. See
https://hosting.defispace.com/docs/quickstart.md
