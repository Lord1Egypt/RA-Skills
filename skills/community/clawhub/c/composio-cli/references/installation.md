# Installation and authentication

Read this reference only when the Composio CLI is missing, signed out, or
running in the wrong execution boundary.

## Check the actual execution environment

Run these read-only checks where OpenClaw will execute the eventual command:

```bash
command -v composio
composio whoami
```

Do not assume that a binary or login on the Gateway host is available inside a
container, sandbox, or remote node. Do not repair that mismatch by copying
host credentials or disabling isolation.

## Install the CLI

If `command -v composio` already succeeds in the execution environment, do not
reinstall or upgrade it. Continue to the sign-in check below.

Before running an installer, tell the trusted operator that the official
installer downloads and verifies a Composio release under `~/.composio`,
creates a `composio` entry point under `~/.local/bin` by default, and may add a
managed Composio block to supported shell startup files.

After the operator authorizes those host changes, run:

```bash
curl -fsSL https://composio.dev/install | sh
```

If execution is not authorized or the environment cannot install software,
show the command for manual use and stop.

The installer supports macOS and Linux. On Windows, use it inside WSL. Follow
the platform and architecture support reported by the official installer
rather than attempting an unlisted binary.

Verify the result. The version must be `0.4.0` or newer:

```bash
command -v composio
composio --version
```

If an existing installation is older than `0.4.0`, do not run the installer
again. Ask the trusted operator to authorize `composio upgrade`, then verify
the version again.

Shell startup changes affect future terminals. In the current task, use the
absolute executable path printed by the installer or ask the operator to begin
a fresh session. Do not make additional shell changes without authorization.

## Sign in

Treat empty `composio whoami` output, explicit unauthenticated output, or a
nonzero exit as signed out.

Ask the trusted operator before initiating login:

```bash
composio login --no-skill-install
```

Keep `--no-skill-install` on every login path. The CLI otherwise installs its
own same-named skill under `~/.agents/skills`; OpenClaw discovers that location
independently of this reviewed workspace skill.

For a headless private operator session:

```bash
composio login --no-browser --no-wait --no-skill-install
composio login --poll --no-skill-install
```

Give an authorization URL only to the trusted operator in a private context.
Never ask anyone to paste an API key, session key, OAuth code, or credential
file into chat. After authorization, run `composio whoami` again and require a
non-empty authenticated identity.

Do not run `composio upgrade` on your own initiative, log out another
session, replace an organization, or install additional agent integrations as
part of ordinary setup.

Do not run `composio --install-skill composio-cli openclaw`. It replaces the
global OpenClaw skill destination with the different artifact bundled in the
CLI release; this workspace skill is already the intended integration.
