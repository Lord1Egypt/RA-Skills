# clawfetch (ClawHub Skill)

**Languages:** English | [中文说明](README_zh.md)

`clawfetch` is a **web page → markdown scraper CLI** designed primarily for
[OpenClaw](https://github.com/openclaw/openclaw) agents and skills.

This skill wraps the published `clawfetch` npm package so that OpenClaw can
call it as a **trusted, inspectable tool** instead of shipping its own
scraper logic.

It runs especially well inside the patched OpenClaw Docker image
`ernestyu/openclaw-patched`, and is mainly intended as a **front-end
preprocessor for local knowledge bases** (e.g. `clawsqlite` / Clawkb):

- Take a URL → get normalized markdown with a small metadata header
- Feed that markdown into SQLite-based KBs or other ingestion pipelines
- Avoid running a full desktop browser or ad-hoc scrapers inside agents

Under the hood the CLI uses:

- **Playwright** (headless Chromium)
- **Mozilla Readability** (article extraction)
- **Turndown** (HTML → markdown)
- **Optional FlareSolverr backend** for Cloudflare / bot challenge pages (via `FLARESOLVERR_URL`)

Input: a single `http/https` URL

Output: normalized markdown to stdout with an `--- METADATA ---` header, e.g.:

```text
--- METADATA ---
Title: ...
Author: ...
Site: ...
FinalURL: ...
Extraction: readability|fallback-container|body-innerText|github-raw-fast-path|reddit-rss
FallbackSelector: ...   # only when not readability
--- MARKDOWN ---
<markdown>
```

The goal is **not** to invent yet another generic web scraper, but to provide
an **OpenClaw-focused, KB-friendly** fetcher with:

- predictable output format
- site-specific fast paths (GitHub README, Reddit RSS)
- clear `NEXT:` hints on errors for agents

---

## Cloudflare / bot challenge support

For sites protected by Cloudflare or similar bot challenges (for example some Kaggle pages),
`clawfetch` can use an external JS-capable backend such as FlareSolverr:

- When the environment variable `FLARESOLVERR_URL` points to a FlareSolverr-compatible
  service, the CLI can automatically call it when a bot-block page is detected.
- You can also explicitly use `--via-flaresolverr` to force using that backend for a given URL:

```bash
FLARESOLVERR_URL=http://127.0.0.1:8191 \
  node node_modules/clawfetch/clawfetch.js --via-flaresolverr 'https://www.kaggle.com/.../some-article'
```

If `clawfetch` detects a Cloudflare / bot challenge page in browser mode **and** no
`FLARESOLVERR_URL` is configured, it will emit a `NEXT:` hint similar to:

```text
INFO: Detected possible bot-block / Cloudflare challenge page.
NEXT: Configure FLARESOLVERR_URL to point to a FlareSolverr service, or open the URL in a full browser to pass the challenge manually.
```

On normal sites (without such challenges), `clawfetch` still only uses Playwright or its
fast-paths (GitHub / Reddit) and does not depend on FlareSolverr.

---

## 1. Why this skill exists

There are already countless scraping libraries, but in an OpenClaw + KB
workflow we have some specific needs:

- Agents run inside Docker (often `ernestyu/openclaw-patched`)
- We want **one standard CLI** for “URL → markdown + metadata”
- We want clean, predictable markdown for ingestion, not raw HTML
- We want safe, reviewable behavior — no hidden git clones or random scripts

This skill:

- Delegates heavy work to the **published `clawfetch` npm package**
- Keeps the skill artifact itself very small and easy to audit
- Makes it trivial for agents to call `clawfetch` from within the
automatically installed skill directory

If you are building anything around `clawsqlite` / Clawkb, this is the
recommended way to fetch web pages into your KB.

---

## 2. Installation in OpenClaw

> **Note:** Older docs may mention `clawhub install clawfetch` and imply that
> the npm dependencies are auto-installed. The current workflow is
> **two explicit steps** using the `openclaw` CLI.

### Step 1 — Install the skill shell into your workspace

Use the OpenClaw skills CLI to download the skill into the active workspace:

```bash
openclaw skills install clawfetch
```

This will create a directory like:

```text
~/.openclaw/workspace/skills/clawfetch
```

At this point the directory only contains the skill metadata and helper files
(`SKILL.md`, `manifest.yaml`, `bootstrap_deps.sh`, READMEs, etc.).

### Step 2 — Bootstrap the npm CLI (required once)

Change into the skill directory and run the bootstrap script to install the
actual `clawfetch` npm package locally:

```bash
cd ~/.openclaw/workspace/skills/clawfetch
bash bootstrap_deps.sh
```

This script is intentionally minimal and reviewable. It only does:

```bash
npm install clawfetch@0.1.7
```

There is **no** runtime git clone, no vendored source, and no extra packages
beyond `clawfetch` and its declared dependencies.

After this completes, the CLI entrypoint will be available at:

```text
~/.openclaw/workspace/skills/clawfetch/node_modules/clawfetch/clawfetch.js
```

From there, both humans and agents can call the CLI directly.

---

## 3. Runtime usage (from the skill directory)

After installation + bootstrap, the CLI entrypoint lives under the skill directory:

```bash
cd ~/.openclaw/workspace/skills/clawfetch
node node_modules/clawfetch/clawfetch.js <url> [--max-comments N] [--no-reddit-rss]
```

Typical patterns:

### 3.1 General articles / docs

```bash
node node_modules/clawfetch/clawfetch.js https://example.com/some-article > article.md
```

- launches headless Chromium via Playwright;
- waits for content to stabilize;
- uses Readability to extract the main article;
- falls back to common containers or `body.innerText` if needed.

### 3.2 GitHub repositories

```bash
node node_modules/clawfetch/clawfetch.js https://github.com/owner/repo > repo-readme.md
```

For GitHub repo URLs, `clawfetch` treats them as **documentation entry
points**:

- First tries `raw.githubusercontent.com` candidates (e.g. `README.md`,
  `README_zh.md`).
  - On success:
    - `Extraction: github-raw-fast-path`
    - `FinalURL` is the raw README URL
    - Markdown body is the README content
- If all raw candidates fail, it falls back to browser mode.

The CLI will also recommend using git for deeper code exploration, e.g.:

```text
NOTE:
  This content only covers the repository README.
  To inspect the full project or source code, use git:

    git clone git@github.com:owner/repo.git
    cd repo
```

### 3.3 Reddit threads

```bash
node node_modules/clawfetch/clawfetch.js \
  "https://www.reddit.com/r/reinforcementlearning/comments/tsv55f/r_reinforcement_learning_in_finance_project/" \
  --max-comments 5 > reddit-thread.md
```

For Reddit URLs, `clawfetch` **by default** uses an Atom/RSS fast-path:

- Convert `<url>` to `<url>.rss` (e.g. add `.rss` to the thread URL).
- Fetch the feed using a normal desktop browser User-Agent.
- Parse the feed into a structured markdown thread:
  - First entry → main post:

    ```markdown
    ## Post: ...
    by /u/... at ...

    <post body>
    ```

  - Subsequent entries → comments:

    ```markdown
    ---

    ### Comment by /u/... at ...

    <comment body>
    ```

- The number of comments is limited by `--max-comments` (default 50;
  `0` means no limit).

You can disable the RSS fast-path with `--no-reddit-rss` to force full
browser scraping, but for most cases the feed-based path is more stable.

---

## 4. Dependencies and behaviour around missing deps

The skill itself never calls `npm` at runtime beyond the one-time
bootstrap. All dependency management is:

- One-time `npm install clawfetch@0.1.7` in `bootstrap_deps.sh`.
- At run time, **only the `clawfetch` CLI** is allowed to decide what to do.

Inside the CLI, `clawfetch` uses `require()` checks for:

- `playwright-core` (or `playwright`)
- `@mozilla/readability`
- `jsdom`
- `turndown`

If these packages are missing **and `--auto-install` is not used** (in
the upstream CLI, not inside this skill):

- It prints a clear list of missing packages;
- It prints recommended `npm install` commands (global or local);
- It exits with a non-zero code.

If `--auto-install` is passed:

- `clawfetch` will attempt a one-shot local `npm install` for missing
  packages in its own directory;
- On failure it prints `NEXT:` hints and exits.

The skill does **not** perform any implicit installs beyond the initial
`bootstrap_deps.sh` hook. Do **not** create a `.env` inside the skill
folder; configure env on the agent/host or in the upstream `clawfetch`
project instead.

---

## 5. Safety and trust model

To keep ClawHub moderation happy and avoid “suspicious” flags, this skill
follows a constrained model:

- No vendored `clawfetch` source code inside the skill.
- No runtime `git clone`.
- No arbitrary `curl | bash` or shell scripting beyond a single
  `npm install clawfetch@0.1.7` in `bootstrap_deps.sh`.
- All heavy logic lives in the public npm package `clawfetch`, which is
  itself Apache-2.0 licensed.

This mirrors the approach used for `clawhealth-garmin` (PyPI package + thin
wrapper skill) and keeps the actual skill artifact small, auditable, and
predictable.

If you need to review behaviour, you can:

- Inspect `clawfetch` source in the main `ernestyu/clawfetch` repo;
- Inspect this skill’s three files (`SKILL.md`, `manifest.yaml`,
  `bootstrap_deps.sh`).

---

## 6. License

This skill is MIT-licensed, while the underlying `clawfetch` package is
Apache-2.0 licensed. See their respective repositories for full details.
