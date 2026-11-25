# Troubleshooting: when a deployment or a command fails

What `error.category` calls for, and the limits on automatic repair, are in SKILL.md (section 6). This file says where the evidence is and what the usual causes are. What each error code means is in section 7 of the [appcli reference](appcli-reference.md).

Contents: where the evidence is · the result is not known · the project is not there · errors about the plan · what is seen, and the usual cause

## Where the evidence is

- A failed build (it runs on the platform's server): `error.details.buildLogTail` is the last 200 lines of the build log. `appcli deployment <id> --wait` prints all of the task's events, the whole build log among them, to standard error.
- A failed run: `result.logTail`, `result.container` and `result.health`.
- A failure before a task exists (the manifest, packing, parameters, uploading) has no `result`; the evidence is in `error.details`.

## The result is not known

- `AGENT_LOST` (status `lost`): the result is not known for now. Tell the user, and ask again later with `appcli deployment <id>`; it may be corrected to the real result. Do not deploy the same thing again meanwhile.
- `RESULT_UNKNOWN`: there was still no result after 24 hours. See with `appcli status` which version the project is really running.
- `PREVIOUS_TASK_UNRESOLVED`: tell the user that a deployment's result is not known yet, and try again later.

## The project is not there

`APPLICATION_NOT_FOUND` or `APPLICATION_DEACTIVATED`: ask the user whether to empty the applicationId in the manifest and deploy as a new project.

- A new project gets a new address and none of the old data. An earlier agreement to migrate data no longer holds, so ask again if there is local data.
- A deactivated project can also be brought back by the administrator within 30 days, with its address unchanged.
- `APPLICATION_NOT_FOUND` with `details.reason` `purged`: the project was deleted for good (`details.purgedAt` says when). It cannot be brought back; say so, rather than that it "does not exist".
- A new project needs a free place in the plan. When the places are taken (`PROJECT_QUOTA_EXCEEDED`), see below.

## Errors about the plan

None of them is a problem of the project: do not change the project to get around them and do not retry over and over.

- `message` says which limit it is and what can be done. Pass it on in the user's language, with the address in `error.details.plansUrl` (the page where the plan is changed).
- `error.details.reason` names the limit for a program: `project_quota`, `projects`, `database`, `database_dedicated`, `builds`, `versions_kept`, `data`.

| Error code | What to do |
|---|---|
| `PROJECT_QUOTA_EXCEEDED` | The plan's places are all taken, so no new project can be created. `details.projects` lists the projects that take them (ID, state, address): tell the user which they are, since the one in the way may be a project this directory knows nothing about. The user deactivates one they no longer need (on the console's projects page, or `appcli delete` run where a manifest names it) or upgrades on the Plans page (`/plans`). When one of them is in fact the project the user wants to update, put its ID into the manifest's applicationId instead of creating a new one |
| `PLAN_LIMIT_EXCEEDED` | The plan has no room: too many projects, or a database service the plan does not include. The user upgrades, or deactivates projects they no longer need |
| `APPLICATION_ASLEEP` | The project is asleep. Run `appcli wake --wait --json`, and when it succeeds retry the original command (`appcli deploy` wakes the project itself and does not meet this error) |
| `BUILD_QUOTA_EXCEEDED` | The builds of the last 24 hours are used up. Tell the user they can deploy again after `details.retryAt`, or upgrade the plan; do not retry before then |
| `DATA_QUOTA_EXCEEDED` | The project stores more (files plus database, `details.usedMb`) than the plan gives one project (`details.limitMb`). Deploying again does not help: the user deletes data the application no longer needs, or upgrades |
| `TERMS_NOT_ACCEPTED` | The platform's user agreement was updated. Run `appcli console`, ask the user to open the link and agree, and retry after they have |

**Running at the plan's ceiling.** `notices` in the output of a deployment (the same sentence is a `[plan]` line among its events) means the deployment runs at the plan's memory / CPU ceiling, below what the manifest asks for. It is there on a failed deployment as well as on a successful one. If the application then fails to start and it looks like too little memory (container exit code 137, OOM in the logs, `JavaScript heap out of memory`), raising memory in the manifest has no effect: tell the user the plan's memory ceiling per project and let them decide between upgrading the plan and making the application use less.

## What is seen, and the usual cause

| What is seen | Usual cause | Repair |
|---|---|---|
| BUILD_FAILED, npm download fails or times out | npmmirror is not in use (for example `.npmrc` is not copied into the build stage, or `.dockerignore` excludes it) | Check that `.npmrc` exists, is not excluded and is copied before `npm ci`, and that the addresses in yarn.lock are replaced. The platform's server itself can reach npmmirror |
| BUILD_FAILED, an install script times out reaching github.com | A package downloads a binary and has no mirror configured | Configure the npmmirror binary mirror for that package in `.npmrc` or as ENV in the build stage |
| BUILD_FAILED, compiling a native module or downloading its prebuilt binary times out | The build stage lacks the build tools, or is trying to download the prebuilt binary from GitHub | Use a version that has prebuilt binaries, or install the build tools in the build stage and compile from source (see [base images](base-images.md)) |
| REGISTRY_UNREACHABLE | The base image cannot be pulled for the build | Check that the image name and version tag exist. Registries other than Docker Hub may be unreachable: change to an equivalent image on Docker Hub, or to `node-base`. When `node-base` cannot be pulled either, it is the server's problem: tell the user to contact the administrator |
| SOURCE_INVALID | The source contains something that is not allowed (a link pointing outside the project and the like), is over 500 MB, or the Dockerfile is not in the package | Adjust `.dockerignore` or the dockerfile path in the manifest as the message says; exclude large files with `.dockerignore` |
| BUILD_TIMEOUT | The build took more than 30 minutes | Look for a large download or a network request that hangs during the build; reduce the build steps |
| PLATFORM_MISMATCH | The image that was built is not linux/amd64 (a `FROM --platform=...`, or a base image that exists only for another architecture) | Remove the platform override, or choose a base image that has a linux/amd64 build |
| PORT_IN_USE | The port was taken before the first deployment | Deploy once more, unchanged. When it fails again, report the error code and suggest contacting the administrator; the address will not change |
| CONTAINER_START_FAILED, Cannot find module | The standalone output lacks files, or a native module was not copied | Correct the copy steps in the Dockerfile |
| CONTAINER_START_FAILED, EACCES / EROFS | Something is written to a directory that is not declared, or the directory's permissions are wrong | Move the write to declared storage or /tmp and add the storage declaration |
| HEALTHCHECK_FAILED, connection refused | Listening on 127.0.0.1, or on another port | Listen on 0.0.0.0, read PORT, check containerPort |
| HEALTHCHECK_FAILED, 404 | The health path does not exist | Check healthcheckPath against the routes |
| HEALTHCHECK_FAILED, lastStatus is 3xx | The health endpoint is caught by a login guard or an i18n redirect (see lastLocation) | Exclude the health path in the middleware |
| HEALTHCHECK_FAILED, timed out | Slow start, or a long migration | Raise healthTimeoutSeconds (at most 600) and read the logs |
| A missing environment variable at start / CONFIG_MISSING_REQUIRED | A required parameter is not declared or was not submitted | Add the env declaration, confirm its source with the user (SKILL.md, section 4), and submit |
| A client-side variable is empty (`NEXT_PUBLIC_*` undefined) | The build-time variable was not passed through buildEnv (or `buildEnvMissing` in the deploy output names it: its source file does not have it), or the Dockerfile does not declare the ARG | Add buildEnv and the Dockerfile's ARG / ENV |
| The page opens but assets or links are 404, or go to localhost | A hard-coded absolute address | Use PUBLIC_URL |
| Deployed, but signed out again right after signing in | The cookie is marked Secure while the address is plain HTTP (or the auth library forces Secure in production), so the browser does not keep it | Set Secure from the request's `X-Forwarded-Proto`, or not at all; give NextAuth and similar libraries PUBLIC_URL as their URL |
| Works locally, one feature fails live | A browser API that exists only in a secure context (crypto.subtle, the clipboard, the camera, Service Workers) on an address served over plain HTTP | Tell the user about the limit. Replace it with something that does not need a secure context where that is possible; otherwise say the feature is not available on that address |
