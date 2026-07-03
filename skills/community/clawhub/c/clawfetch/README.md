# clawfetch Skill

This directory is a thin OpenClaw/ClawHub skill wrapper for the published `clawfetch` npm CLI. It is not a standalone scraper project and does not copy clawfetch source code.

## Why It Exists

The skill lets Agents call clawfetch as a controlled tool for turning web pages, GitHub README pages, and Reddit threads into knowledge-base friendly markdown. The CLI remains the only implementation of scraping, runtime lifecycle, site-specific behavior, and error recovery.

## First-Use Install Model

Installing this skill wrapper is not the same as installing a ready-to-run clawfetch environment. A first-time Agent must complete all stages below.

1. Install or copy this skill wrapper directory.
2. Enter the installed skill directory, the directory containing `SKILL.md` and `bootstrap_deps.sh`.
3. Bootstrap the published npm CLI into this skill directory:

```bash
cd <installed skill directory>
sh bootstrap_deps.sh
```

4. Install the browser runtime through the CLI:

```bash
node node_modules/clawfetch/clawfetch.js runtime install
```

5. Check the runtime before fetching:

```bash
node node_modules/clawfetch/clawfetch.js runtime check
```

Only after step 5 succeeds should an Agent treat clawfetch as ready for browser-backed fetching.

Optional smoke test:

```bash
node node_modules/clawfetch/clawfetch.js https://example.com
```

A successful smoke test prints `--- METADATA ---` and `--- MARKDOWN ---`.

The bootstrap script installs the published `clawfetch` npm package into this skill directory as `node_modules/clawfetch` and verifies that `node_modules/clawfetch/clawfetch.js` exists before reporting success. It does not install the browser runtime, run `git clone`, download a source tree, modify global npm state, change system paths, or install unrelated tools.

By default the script follows the version in the project root `package.json`. If the wrapper is distributed without the project root, it falls back to the pinned version recorded in the script. That fallback exists only because standalone ClawHub distribution cannot dynamically read the project root; keep it aligned with the current published CLI version.

## Configuration

This skill ships with a formal config file:

```text
clawfetch.toml
```

In the normal skill layout, the CLI entry is:

```text
node_modules/clawfetch/clawfetch.js
```

That CLI resolves the fixed host config as this skill directory's `clawfetch.toml`.
It does not search upward from the caller's current working directory. Keep
long-lived FlareSolverr settings in this file, not inside
`node_modules/clawfetch`, because `node_modules/clawfetch` is an npm install
artifact that may be replaced during bootstrap, repair, or upgrade.

Default config:

```toml
[flaresolverr]
enabled = false
# url = "http://127.0.0.1:8191"
max_timeout_ms = 60000
```

To enable FlareSolverr, edit `clawfetch.toml`, set `enabled = true`, and provide
a reachable `url`, for example `http://127.0.0.1:8191` or
`http://flaresolverr:8191` in Docker/service-network setups. `FLARESOLVERR_URL`
is still accepted as a compatibility or temporary override, but it is not the
recommended primary configuration path.

## Usage

After bootstrap and a successful runtime check, call the local CLI:

```bash
node node_modules/clawfetch/clawfetch.js https://example.com/article
node node_modules/clawfetch/clawfetch.js https://github.com/owner/repo
node node_modules/clawfetch/clawfetch.js https://www.reddit.com/r/example/comments/...
```

Runtime lifecycle commands also go through the CLI:

```bash
node node_modules/clawfetch/clawfetch.js runtime install
node node_modules/clawfetch/clawfetch.js runtime check
node node_modules/clawfetch/clawfetch.js runtime repair
node node_modules/clawfetch/clawfetch.js runtime upgrade
node node_modules/clawfetch/clawfetch.js runtime diagnose --json
```

The skill layer must not manage browser runtime directly. It should surface the CLI's `NEXT:` hints to the Agent or operator.

The browser runtime install location and lifecycle are decided by the CLI/project itself. This wrapper does not participate in path selection, runtime repair logic, or version matching.

If setup fails, run:

```bash
node node_modules/clawfetch/clawfetch.js runtime diagnose --json
```

Then follow the CLI's `NEXT:` output instead of inventing a skill-layer workaround.

## Boundaries

This skill does not implement scraping logic, browser launch logic, Playwright package resolution, browser runtime management, GitHub fast-paths, Reddit RSS handling, FlareSolverr support, or markdown conversion.

This skill also does not hide downloads, clone repositories, perform unrelated filesystem operations, or act as a general shell tool.

ClawHub publishes skill content under its registry license policy. The `clawfetch` npm CLI package remains licensed separately under Apache-2.0.
