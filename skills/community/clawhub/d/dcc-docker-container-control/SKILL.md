---
name: dcc-docker-container-control
description: Fast manual CI for Docker Compose apps. Use "dcc deploy APP" to fetch the app's latest Git commit, build it, deploy it, restart containers, and verify status on a known Docker server.
metadata:
  openclaw:
    homepage: https://github.com/localsplash/dcc-docker-container-control-skill
    emoji: "🚀"
---

# DCC Docker Container Control

Use DCC as a fast manual alternative when a traditional CI pipeline is unavailable or too slow.

## Fast path

When the user says:

`dcc deploy website_app`

run this on the known Docker server:

```
sudo /opt/docker-container-control deploy website_app
```

Do the work immediately. The controller finds the app under `/opt`, fast-forward pulls its latest Git commit, pulls images, builds, starts/restarts the Compose deployment, waits for it to become running/healthy, and prints final status.

## Docker server

Resolve the server from the request, current thread, or authoritative environment documentation.

If the Docker server is unknown or ambiguous, ask which Docker server to use before proceeding. Never guess.

Use the configured SSH helper. Run remote deployment commands with a bounded timeout long enough for builds to finish. If the local SSH process is interrupted, verify on the remote server whether the deployment command is still running.

## Install the controller when needed

The bundled controller is `docker-container-control` at the skill root. Legacy installations may place it at `scripts/docker-container-control`.

Check the remote server:

```
test -x /opt/docker-container-control
```

If missing:

1. Locate the bundled controller.
2. Validate it locally with `python3 -m py_compile <controller>`.
3. Copy it to a temporary path on the Docker server.
4. Install it as root-owned mode `755` at `/opt/docker-container-control`.
5. Verify with `sudo /opt/docker-container-control list`.
6. Continue the user's requested DCC action without making them repeat it.

If an existing remote controller differs from the bundled version, do not silently overwrite it. Report the difference and ask before replacing it.

## Commands

- `dcc deploy <app>` — get the latest Git commit, pull images, build, deploy, restart, wait for health, and show status.
- `dcc dry-run <app>` — show the Git and Compose deployment plan without changing containers.
- `dcc list` — list detected deployments and usable app names.
- `dcc status <app>` — show Compose status.
- `dcc restart <app>` — restart the existing Compose deployment and verify health.
- `dcc recreate <app>` — rebuild and force-recreate the Compose deployment, then verify health.

Map them directly to:

```
sudo /opt/docker-container-control <action> [app]
```

Deployment names can be the app folder name, Compose project name, or running container name. Use exact names. If no deployment matches or more than one matches, show the detected names and ask the user to choose.

## Deployment behavior

For a Git checkout, `deploy`:

1. Refuses to run when tracked files have uncommitted changes.
2. Runs `git fetch --prune origin`.
3. Runs `git pull --ff-only`.
4. Runs Compose image pull with failures tolerated.
5. Runs `docker compose up -d --build`.
6. Waits up to 120 seconds for discovered containers to be running and healthy.
7. Prints final Compose status.

A non-Git app skips the Git step and still pulls/builds/starts the Compose deployment.

## Reporting

Return the important command output and final Compose status. State success only when the command exits successfully and the deployment reaches running/healthy state.

Do not expand DCC into unrelated operations such as Docker prune, Compose down, Git reset, force-pull, or branch changes.
