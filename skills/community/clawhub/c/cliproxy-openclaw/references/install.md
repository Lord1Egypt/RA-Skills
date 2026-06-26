# Install CLIProxyAPI

Use this file when you need the installation and service workflow.

## Goals

- get CLIProxyAPI running reliably
- avoid fragile one-off shell sessions
- verify the listener before moving on

## Recommended deployment shape

Prefer this order:
1. existing stable deployment method already used on the host
2. systemd-managed process
3. Docker or compose if the host already uses it for nearby services

Avoid leaving CLIProxy running only inside an interactive shell.

## Before install

Check:
- OS
- available package manager
- runtime required by the current CLIProxyAPI release
- whether the target host already has nginx, Caddy, Docker, or systemd
- whether the deployment should stay local or be reachable remotely

## Install procedure

1. Read the current upstream README before using version-specific commands.
2. Clone or fetch the project into a stable path.
3. Install dependencies using the upstream-supported method.
4. Start CLIProxyAPI in a reproducible way.
5. If possible, create a systemd unit so the service survives logout and reboot.

## After install

Verify all of these:
- the process is running
- the intended port is listening
- logs do not show immediate crash loops
- health or landing endpoint responds if one exists

## Prefer service-style deployment

If using systemd, ensure:
- a dedicated working directory
- a restart policy
- environment is explicit, not shell-dependent
- logs are inspectable via journalctl

## Do not proceed until

- dashboard or API listener is reachable locally
- the service survives a restart if persistent deployment was requested
