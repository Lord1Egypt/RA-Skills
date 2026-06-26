# Forgejo Workflow

OpenClaw skill for working with self-hosted Forgejo instances through `fj`, the
Forgejo REST API, and local `git` for review workflows. Published on ClawHub as
`forgejo-fj-api`.

## What this skill does

- Repositories, issues, pull requests, and releases
- Wiki reads through `fj` and wiki writes through the REST API
- Organization labels through `fj`; repository labels through the REST API by default, with `fj repo labels` available on current source builds but not packaged `0.4.x` releases; milestones through the REST API
- Forgejo Actions and CI status inspection
- Structured pull request review workflow

## Setup

Use one of these setup paths depending on whether you already have Forgejo
credentials.

### Manual setup

1. Install `fj`:

```bash
brew install forgejo-cli
```

2. Make sure the other required tools are available:

```bash
command -v curl jq git
```

3. Create an application token in Forgejo:

```text
https://<your-forgejo-host>/user/settings/applications
```

4. Export the required environment:

```bash
export FORGEJO_URL=https://<your-forgejo-host>
export FORGEJO_TOKEN=<your-token>
```

`FORGEJO_URL` must point to the target Forgejo instance, not to this skill
repository URL.

5. Add the same token to `fj` for the target host:

```bash
fj --host <your-forgejo-host> auth add-key <username>
```

6. Verify readiness:

```bash
command -v fj curl jq git
test -n "$FORGEJO_URL" && test -n "$FORGEJO_TOKEN"
fj auth list
```

### Prompt-guided setup

The assistant can guide setup, verify what is missing, and give exact commands.
It cannot create the Forgejo token for you; token creation still happens in the
Forgejo web UI.

If you already have credentials:

```text
Set up this Forgejo skill for https://<your-forgejo-host>. I already have a token and my Forgejo username is alice. First check whether fj, curl, jq, and git are available. If one of them is missing and OpenClaw can install it, install it. Then assume FORGEJO_URL and FORGEJO_TOKEN may already be available either from the OpenClaw .env loaded for this session or from exported shell variables, verify whether they are present, tell me the exact fj --host <your-forgejo-host> auth add-key alice command to run if fj auth is not ready yet, and finally tell me clearly whether the skill is fully ready, partially ready, or blocked, and what is still missing if anything.
```


## Configuration model

This skill targets one active Forgejo instance at a time.

Required environment:

| Variable | Required | Example | Purpose |
|---|---|---|---|
| `FORGEJO_URL` | Yes | `https://<your-forgejo-host>` | Base URL of the Forgejo instance for this skill's REST and instance-selection workflow |
| `FORGEJO_TOKEN` | Yes | `forgejo_pat_...` | Application token for this skill's REST examples and recommended `fj` setup |

Repository targeting:
- Resolve the repository from the current git remote when possible
- Outside a local clone, pass an explicit repo target and ensure `fj` can also resolve the host via `--host`, a host-qualified repo, or other existing CLI context
- Do not assume a public default Forgejo host

## Quick start

`fj` itself stores auth in its own keyring/config flow. These env vars are part
of this skill's explicit configuration contract, especially for REST fallback.

REST-ready requires `FORGEJO_URL` and `FORGEJO_TOKEN`. `fj`-ready also requires
`fj` auth for the target host.

Run a repository command:

```bash
fj --host <your-forgejo-host> repo view owner/repo
```

Inside a local clone, `fj issue search` and `fj pr search` can use repository
context from the current remote.

Outside a local clone, many issue and pull-request commands use embedded targets
such as `owner/repo#42` rather than `--repo owner/repo`.

Use the REST API for coverage gaps:

```bash
curl -sS \
  -H "Authorization: token $FORGEJO_TOKEN" \
  -H "Accept: application/json" \
  "$FORGEJO_URL/api/v1/repos/owner/repo" | jq .
```

## Readiness check

Use this quick check to see whether the skill is ready to operate cleanly:

```bash
command -v fj curl jq git
test -n "$FORGEJO_URL" && test -n "$FORGEJO_TOKEN"
fj auth list
```

Interpretation:
- if a binary check fails, install the missing tool first
- if an env check fails, export the missing value first
- if `fj auth list` does not include the target host, add the key for that host first

If `fj` is missing but `curl` and `jq` are available, the REST references can
still cover API-only tasks.

## Install the skill

```bash
clawhub install forgejo-fj-api
```

## Included references

- `references/api-cheatsheet.md` for verified REST endpoints and payload shapes
- `references/code-review.md` for the Forgejo PR review workflow and output format
- `references/ci-actions.md` for Actions and CI inspection guidance

## Compatibility

- Targeted at self-hosted Forgejo instances
- Requires `fj` for the CLI path, `curl` and `jq` for the REST path, and `git` for review flows
- Requires a valid Forgejo application token
- `fj repo labels` is available on current source builds, but not packaged `0.4.x` releases
- Actions and some API details can vary by Forgejo version; check `$FORGEJO_URL/api/swagger` when behavior differs
- OpenClaw eligibility gating checks declared bins and env vars at load time, but sandboxed runs also need the same tools available inside the sandbox

## Publish

```bash
clawhub publish . --slug forgejo-fj-api --version 0.1.1
```

## License

MIT-0
