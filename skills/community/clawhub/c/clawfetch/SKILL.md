---
name: clawfetch
description: Thin OpenClaw and ClawHub wrapper for the published clawfetch npm CLI, used to fetch web pages, GitHub READMEs, and Reddit threads as markdown.
version: 1.0.12
metadata:
  openclaw:
    requires:
      bins:
        - node
        - npm
    homepage: https://github.com/ernestyu/clawfetch
---

# clawfetch

This skill is a thin Agent wrapper around the published `clawfetch` npm CLI. It is not a second scraper product and it does not contain a separate implementation of clawfetch.

Use this skill when an Agent needs to fetch web content into markdown for knowledge-base ingestion, source review, or compact reading. Typical targets include ordinary web pages, GitHub repository README pages, and Reddit threads.

## Boundary

This skill does not:

- vendor the clawfetch source tree
- clone the clawfetch repository
- reimplement browser startup, Playwright runtime handling, GitHub fast-paths, Reddit RSS handling, FlareSolverr support, or markdown conversion
- define a second set of runtime rules
- act as a general shell wrapper

The runtime behavior belongs to the published clawfetch CLI installed by `bootstrap_deps.sh`.

## Bootstrap

Installing this skill through OpenClaw/ClawHub only installs the wrapper files in this directory. Do not treat `openclaw skills install clawfetch` as a complete clawfetch installation.

First-time setup is not complete until both the npm CLI and the browser runtime are installed and checked:

1. Find the installed skill directory, the directory containing this `SKILL.md` and `bootstrap_deps.sh`.
2. Install the published clawfetch npm CLI into this skill directory:

```bash
cd <installed skill directory>
sh bootstrap_deps.sh
```

3. Install the CLI-managed browser runtime:

```bash
node node_modules/clawfetch/clawfetch.js runtime install
```

4. Verify the runtime before fetching pages:

```bash
node node_modules/clawfetch/clawfetch.js runtime check
```

5. Optional smoke test for network and extraction:

```bash
node node_modules/clawfetch/clawfetch.js https://example.com
```

The smoke test should print `--- METADATA ---` and `--- MARKDOWN ---`.

The bootstrap script installs the published `clawfetch` npm package into this skill directory, under `node_modules/clawfetch`, and verifies that `node_modules/clawfetch/clawfetch.js` exists before reporting success. It does not install the browser runtime, clone a repository, install unrelated packages, modify global npm state, or change system paths.

When this skill lives inside the clawfetch project repository, bootstrap reads the project root `package.json` and installs that same version. If the wrapper is distributed without the project root, it uses the pinned fallback version in `bootstrap_deps.sh`; maintainers must keep that fallback aligned with the current published CLI version.

Ready state means `node_modules/clawfetch` exists and `node node_modules/clawfetch/clawfetch.js runtime check` exits successfully. If runtime check fails, run `node node_modules/clawfetch/clawfetch.js runtime diagnose --json` and follow the CLI's `NEXT:` hints.

## Configuration

This skill includes a formal configuration file at:

```text
clawfetch.toml
```

From this skill directory, the CLI resolves that file as the fixed host config for `node_modules/clawfetch/clawfetch.js`. Do not place the long-lived skill configuration inside `node_modules/clawfetch`; that directory is a bootstrap-generated npm package install and may be replaced during repair, upgrade, or re-bootstrap.

The default config is conservative:

```toml
[flaresolverr]
enabled = false
# url = "http://127.0.0.1:8191"
max_timeout_ms = 60000
```

To enable FlareSolverr, edit this skill directory's `clawfetch.toml`, set `enabled = true`, and set `url` to a reachable FlareSolverr-compatible service. `FLARESOLVERR_URL` remains supported only as a compatibility or temporary override; it is not the preferred skill configuration path.

## Invocation

After bootstrap and a successful runtime check, invoke the CLI through the local package installation:

```bash
node node_modules/clawfetch/clawfetch.js https://example.com/article
```

Runtime lifecycle commands are also provided by the CLI itself:

```bash
node node_modules/clawfetch/clawfetch.js runtime install
node node_modules/clawfetch/clawfetch.js runtime check
node node_modules/clawfetch/clawfetch.js runtime diagnose --json
```

Do not bypass these CLI lifecycle commands from the skill layer. Browser runtime install, check, repair, upgrade, clean, and diagnose behavior must remain owned by the clawfetch CLI. `bootstrap_deps.sh` installs the npm CLI; `runtime install` installs the browser runtime. Both are required for first use.

## Agent Guidance

Use the CLI's `NEXT:` hints when recovering from missing dependencies, missing browser runtime, runtime mismatch, protected pages, or weak extraction results. The skill should surface those hints rather than inventing alternate recovery paths.
