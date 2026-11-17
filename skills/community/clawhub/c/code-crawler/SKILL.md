---
name: code-crawler
description: Answer questions about code relationships in an indexed repository - callers, callees, impact, entry points, routes, DI wiring, dead code, cycles - using the code-crawler MCP server's SQLite property graph. Use when the question is about how symbols connect (who calls this, what breaks if I change it, where does a request enter, is this reachable) rather than about text you can find by searching. Do not crawl a repository just to answer a question about a single file you already have open.
metadata:
  openclaw:
    emoji: "🕸️"
    homepage: https://nithin554.github.io/code-crawler/
    requires:
      bins: ["node"]
    install:
      - kind: node
        package: "@nithin554/code-crawler"
        bins: ["codecrawler"]
---

# Code Crawler

A SQLite property graph of a codebase, exposed as 29 MCP tools. The graph is built
once by a crawl, then queried cheaply many times.

## Getting the tools

**Check first.** If no `code-crawler` tools appear in your tool list, the server is not
registered and nothing else in this skill will run. Say so instead of falling back to
`grep` — and ask before editing a client config file, which is the user's machine
state, not yours.

Installing the *skill* does not install the *server*: `npx skills add nithin554/code-crawler`
delivers these instructions, and `npx add-mcp @nithin554/code-crawler` — or the config
below — registers the server that delivers the tools. Both are needed, and they are
independent.

If this skill arrived inside the **code-crawler plugin**, the server is registered for you.
The plugin starts the server from the plugin directory, but resolves a project for each
call — `crawl_project`, the client's workspace roots, or the project this session already
selected — and keeps that repository's graph in `<project>/.code-crawler/index.db`. One
plugin install serves
every repository you open, each with its own database. Set `CODECRAWLER_DB` to pin a single
file instead.

The server is the npm package `@nithin554/code-crawler` and needs Node.js ≥ 22.12. Every
stdio MCP client takes the same command/args/env triple:

```json
{
  "mcpServers": {
    "code-crawler": {
      "command": "npx",
      "args": ["-y", "@nithin554/code-crawler", "serve"],
      "env": { "CODECRAWLER_DB": "/absolute/path/to/index.db" }
    }
  }
}
```

`npx -y` needs no prior install. If the package is already installed globally, use
`"command": "codecrawler"` with `"args": ["serve"]`. From a source checkout, point
`"command": "node"` at `dist/index.js`, keeping `"args": ["serve"]`. `serve` is the default
subcommand, so `args` may omit it.

Writing that JSON by hand is the slow way. `add-mcp` fills it in for whichever client you
name. Run it from inside the repository you want indexed:

```bash
npx add-mcp @nithin554/code-crawler --args serve -a cursor
```

It derives the server name `code-crawler` from the package, so no `--name` is needed. `-a`
accepts `claude-code`, `cursor`, `vscode`, `claude-desktop`, `codex`, `opencode`, `zed` and
about twenty more — `npx add-mcp list-agents` prints the list. Without `-g` the entry lives
in the project (`.mcp.json`, `.cursor/mcp.json`, `.vscode/mcp.json`); `-g` writes user-level
config. Repeat `--args` and `--env` once per value.

`--env CODECRAWLER_DB` is optional: the server indexes into `<project>/.code-crawler/index.db`
by default. Pin it — `--env CODECRAWLER_DB=/absolute/path/index.db` — when you want the file
elsewhere, or when the client's working directory is not the project.

Three things decide whether the graph is usable:

- **`CODECRAWLER_DB`** is the SQLite file holding the graph. The default needs no
  configuration: the server walks up from its working directory to the nearest project root
  (`.git`, `package.json`, `pom.xml`, `build.gradle`, `pyproject.toml`, `setup.py`,
  `requirements.txt`, `go.mod`, `Cargo.toml`) and uses `<project>/.code-crawler/index.db`, so
  **each repository gets its own file**. With no enclosing project it falls back to
  `~/.code-crawler/index.db`. That home file is the fallback and nothing more, never an
  enclosing project, so an unmarked folder under `~` gets its own file rather than sharing
  it. A database still holds exactly one project — crawling a
  different path into one is refused before anything is written; give that project its own
  database (its own registration), or run `clear_index` to replace the existing index.
- **One server per project.** A process opens one database at startup and a database holds
  one project, so register the server once per repository (project-scoped config, above)
  rather than once globally for all of them. `crawl` resolves the same way, so crawling a
  subdirectory such as `repo/src` shares `repo`'s file instead of growing a second one.
- **Never share one `CODECRAWLER_DB` across repositories.** Do that and the second project's
  crawl hits the one-project error above.
- **Use absolute paths.** Clients launch servers from an unpredictable working directory,
  so a relative `CODECRAWLER_DB` or a relative project root lands somewhere unexpected —
  and the default resolution follows the cwd you may not have chosen.
- **Config is all environment variables**, identical for the CLI and the client:
  `CODECRAWLER_DB`, `CODECRAWLER_EXCLUDE_DIRS`, `CODECRAWLER_DEFAULT_LIMIT`,
  `CODECRAWLER_MAX_DEPTH`, `CODECRAWLER_MAX_FILE_BYTES`, `CODECRAWLER_RESPECT_GITIGNORE`,
  `CODECRAWLER_HELPFUL_ERRORS`. Invalid values are clamped and warned about, never fatal.

Some clients namespace tool names with the server key — `code-crawler-search_symbols`
rather than `search_symbols`. Same tools, so match on the suffix if the exact name is
missing.

Once the tools appear, call `index_status` to confirm the server answers, then follow the
bootstrap below. The CLI shares the database, so `npx -y @nithin554/code-crawler crawl
/path/to/repo` warms the index ahead of time if you would rather not spend a turn on it.

## When to reach for it

The graph answers **relationship** questions. Text search answers **location** questions.
Picking the wrong one wastes the most time of anything in this skill.

| Question | Use |
| --- | --- |
| What is this symbol, briefly? | `explain_symbol` - one call instead of five |
| Who calls this method? | `get_callers` |
| What does this method call? | `get_callees` |
| What breaks if I change this? | `impact_analysis` |
| What breaks if I change this diff? | `change_impact` |
| Who reacts when this publishes an event? | `find_event_flows` |
| Where does a request enter this system? | `find_entry_points`, `find_routes` |
| Which implementation handles this interface? | `find_implementations` |
| Is this method reachable at all? | `find_dead_code`, `find_hotspots` |
| How does this request reach that handler? | `trace_path`, `trace_execution` |
| What is wired in by DI or annotations? | `find_injections`, `find_annotated`, `get_decorators` |
| What third-party code is actually used? | `find_external_dependencies` |
| Where is `ThingFactory` defined? | **plain search** - do not crawl |
| Which templates use this i18n key? | **plain search** - the graph indexes symbols, not template text |
| Where is this literal, config key or SQL string? | **plain search** - text only, no symbol |
| Show me the body of this function | **plain file read** - do not crawl |

Crawling is not free: it parses every file in the project. Do it when you intend to ask
several relationship questions, or when one relationship question has no cheaper answer.
For a single-file question you already have open, reading the file beats crawling the repo.

The saving is measured, not asserted: on ten structural questions across four pinned
projects the graph used 12 tool calls and 22.9k tokens, where search-then-read-every-hit
cost 120 calls and 105.8k tokens (8.5k with `compact: true`). The reverse also holds —
a question about text was one search (340 tokens) that the graph could not answer at all.
So: structure and wiring go to the graph, literals and text go to search.

## Bootstrap

1. `index_status` first. If it reports files and a recent crawl, the index is already
   warm and you can skip step 2.
2. `crawl_project` with the project root. It is idempotent and incremental - unchanged
   files are skipped via a content manifest, so a second crawl is cheap.
3. Only then run the query tools.

**Never trust a stale index.** Call `index_status` before concluding "there are no
callers". An empty result from an empty or stale index is indistinguishable from a true
negative, and that is the single most common way this tool misleads.

Re-index with the `force` option when the working tree changed underneath the index:

- after a rebase, merge, or `git reset` that rewrote history
- after switching branches with a large diff
- after `git stash pop`

An incremental crawl keys off file content and mtime, which is enough for ordinary
editing but not for a history rewrite. `force: true` bypasses the manifest.

## Reading the results

Two fields decide whether a result means what you think: `confidence` and `external`.
Phantom nodes mark the third trap. See
[reference/edge-semantics.md](reference/edge-semantics.md) before reasoning about
"unreachable" or "no callers".

Short version:

- `confidence` is not a probability. It is a band: `1.0` resolved by construction,
  `0.9`/`0.85` strong static evidence, `0.8` inherited or external, `0.5` heuristics,
  `0` phantom.
- `confidence` is reported per edge on `get_callers`, `get_callees` and `trace_path` rows
  whenever the edge kind has a confidence model. An absent `confidence` means the edge
  kind carries none — it does not mean high confidence.
- Call-graph tools follow `DYNAMIC_DISPATCH` by default, so a method reached only through
  an interface or virtual call still shows callers. Pass `include_dynamic: false` for a
  static-`CALLS`-only view; the response then reports `edgesFollowed: ["CALLS"]`.
- Callers of a `@Transactional`, `@Async` or `@Cacheable` method report `proxy`, and the
  call is not what the annotation promises when either is set: `inert: true` means
  self-invocation bypassed the proxy, `proxyBlocked` (`private`, `static`, `final`,
  `final-type`) means the container could never have honoured it. Do not report an
  annotated method as transactional or asynchronous without checking these.
- An edge with `alternatives` is an unresolved *choice*, not an unresolved call: the call site
  is proven but several overloads matched equally, and the target is the first declaration with
  the rivals listed. Confidence is capped at `0.6`. Report both rather than asserting the one
  that happens to be listed first.
- `external: true` means the target is outside the project. It is *not* dead code and
  *not* unresolved.
- `__phantom__:` / `__reflect__:` / `__inject__:` targets mark something the resolver
  could not bind. They are inventory, not findings.

## Reference

- [reference/tools.md](reference/tools.md) - all 29 tools, grouped by the question they
  answer, with the argument that matters most for each.
- [reference/edge-semantics.md](reference/edge-semantics.md) - `confidence`, `external`,
  phantom nodes, and the ways a "missing" edge is legitimate.

## Budget discipline

Every list-returning tool accepts `max_tokens` (100-200000) and `cursor`. The response
then carries a `page` block with `totalCount`, `truncated`, and `nextCursor`. When the
budget cuts the list, `page.hint` states the exact `cursor` to pass next.

Start with a small `max_tokens` and widen only if the answer is genuinely incomplete.
Reading one page of `get_callers` and reporting the shape is almost always better than
paging through all of them. Prefer `explain_symbol` over chaining `get_node` +
`get_callers` + `get_callees` + `get_decorators` when you want a digest rather than a
specific list.

Every tool also accepts `compact: true`, which returns symbol references as qualified
names instead of objects with `id`, `name`, `kind` and `filePath`. It removes 61-83% of a
response depending on how reference-heavy it is. Use it when you are scanning a wide
trace or comparing name sets; skip it when you need `filePath` to open a file or a node
id to pass on. `get_node` accepts a qualified name, so expand only the names you care
about.

## Do not

- Crawl a monorepo to answer a question about one file.
- Report "no callers" or "dead code" without checking `confidence` (where present) and
  `external` on the edges you did get, and without noting whether dispatch edges were
  followed.
- Treat `find_unresolved` as a bug list. It is a coverage report; some entries are
  dynamic dispatch that cannot be resolved statically.
- Page through an entire result set to count things. Use `totalCount` from the first page.
