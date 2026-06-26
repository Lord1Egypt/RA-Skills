---
name: draft-cli
version: "1.9.5"
description: >
  Manage InnoSage Draft pages and hosted Secret Shares using the @innosage/draft-cli.
  Use this skill for `draft`, `draft page ...`, `draft secret ...`, and `draft auth ...`.
  Prefer JSON Workspace page operations anchored by workspace status/path metadata.
  Do not use this skill when "draft" is only a verb or when the task is a generic local-file
  writing task unrelated to Draft CLI.
metadata:
  clawdis:
    emoji: "📝"
    requires:
      bins:
        - "draft"
    install:
      - id: "npm"
        kind: "node"
        package: "@innosage/draft-cli"
        bins:
          - "draft"
        label: "Install draft-cli (npm)"
    envVars:
      - name: "GLOBAL_INVITE_CODE"
        required: false
        description: "The invite code used to publish Draft pages safely. Defaults to `innosage` during the free beta publish flow."
---

# Draft CLI Skill

Use `draft` for JSON Workspace page-domain Draft operations and hosted Secret Share helpers.

## Current Runtime Contract

- Prefer the saved JSON Workspace as the default page target.
- Use workspace metadata commands before page commands so you know which folder and source the CLI is using.
- Until headless storage is removed, pass the resolved workspace path with `--workspace-json <folder>`
  for page commands that must operate on JSON Workspace data.

## Workspace-First Pattern For Page Commands

For page commands such as `draft page ls`, `draft page cat`, `draft page create`,
`draft page append`, `draft page replace`, `draft page patch`, `draft page annotate`, and
`draft page publish`:

```bash
draft workspace status --json
draft workspace path --json
```

Use the returned `active_workspace_path` to anchor page commands explicitly:

```bash
draft --workspace-json <active_workspace_path> page ls --json
draft --workspace-json <active_workspace_path> page cat <page_id> --json
```

For an explicit folder override, anchor the command with `--workspace-json`:

```bash
draft --workspace-json <folder> page ls --json
draft --workspace-json <folder> page cat <page_id> --json
```

If the user wants that folder to become the default workspace, set it first:

```bash
draft workspace set-path <folder> --json
draft workspace status --json
```

Use the workspace metadata to confirm whether the CLI is operating on the saved default path or an
explicit override before you describe results back to the user.

## Version Detection And Older CLI Fallback

Newer CLIs can expose workspace metadata commands such as:

```bash
draft workspace status --json
draft workspace path --json
draft workspace set-path <folder> --json
```

If those commands are unavailable, detect that once and fall back safely:

```bash
draft workspace --help
draft --workspace-json <folder> page ls --json
```

- If `draft workspace --help` or `draft workspace status --json` fails with an unknown-command
  style error, assume the CLI is older.
- On older CLIs, require an explicit folder and run page commands with
  `draft --workspace-json <folder> ...`.
- If the user did not provide a folder and the CLI lacks workspace commands, ask for the JSON Workspace folder path or ask them to upgrade the CLI.

## Page Commands

Prefer explicit `draft page ...` commands under a JSON Workspace target. In the transition period,
include `--workspace-json <folder>` so the command cannot accidentally hit legacy headless storage:

```bash
draft --workspace-json <folder> page ls --json
draft --workspace-json <folder> page search "phrase" --json
draft --workspace-json <folder> page cat <page_id> --json
draft --workspace-json <folder> page create "Title" --json
draft --workspace-json <folder> page append <page_id> "More content" --json
draft --workspace-json <folder> page replace <page_id> --heading "Status" "Updated body" --json
draft --workspace-json <folder> page patch <page_id> --json < change.diff
draft --workspace-json <folder> page annotate <page_id> --anchor "exact text" --note "Reviewer note" --json
draft --workspace-json <folder> page comments <page_id> --json
draft --workspace-json <folder> page comment <comment_id> <page_id> --json
draft --workspace-json <folder> page insert-image <page_id> ./image.png --json
draft --workspace-json <folder> page update-image <page_id> <local_id> --width 320 --json
draft --workspace-json <folder> page delete-image <page_id> <local_id> --json
draft --workspace-json <folder> page publish <page_id> --json
```

### Agent-Native Read Guidance

- Prefer `draft --workspace-json <folder> page cat <page_id>` for rendered page reads meant for
  human review. The markdown surface preserves links, marks, tables, images, ordered lists, line
  breaks, and custom blocks better than manual rendering from `pages/*.json`.
- Use `draft --workspace-json <folder> page cat <page_id> --json` only when you need structured
  block data for parsing or automation. It is larger than the markdown read surface.
- Treat raw workspace JSON files as a last resort for recovery or low-level inspection, not the
  default read path.
- For discovery, prefer `draft --workspace-json <folder> page search "phrase" --json` when the CLI
  supports it. On older CLIs without page search, use `rg` over workspace page files only to
  discover candidate page IDs or titles, then switch back to `draft --workspace-json <folder> page
  cat <page_id>` for authoritative rendered output.

Use `draft --workspace-json <folder> page cat <id>` when you want the page content in plain
markdown for human review. Use `--json` only when you need raw structured document data for parsing
or automation.

## Patch Contract

`draft page patch` applies unified diffs to the page body markdown only. Do not generate patches
from decorated human `page cat` output that includes `Title:`, `ID:`, or `---` separator lines, and
do not generate patches from `page cat --json` block output.

Patch workflow:

```bash
draft --workspace-json <folder> page cat <page_id>
# Extract only the body markdown, build a unified diff against that body, then:
draft --workspace-json <folder> page patch <page_id> --json < change.diff
draft --workspace-json <folder> page cat <page_id> --json
```

Verify the patch output or follow-up `page cat` before running downstream commands that depend on
the edited text, such as `page annotate --anchor "new text"`. If patch returns `PATCH_MISMATCH`,
reread the current page body markdown, regenerate a fresh diff against that exact body surface, and
retry.

## Image Mutation Contract

`draft page insert-image` returns `local_id`. Use that returned `local_id` for subsequent
`update-image` and `delete-image` commands. In `page cat --json` compatibility output, the same
identifier is exposed as the image block `id`.

Top-level page aliases can still exist during compatibility windows, but agents should use the
`draft page ...` namespace.

## Public Preview Feedback

Public Draft preview and published URLs expose review feedback through the public page surface, not
through JSON Workspace page commands. Treat the public preview or published URL as the primary
machine-readable entrypoint for public review workflows. When the task starts from a public preview
or published URL, fetch that public URL first, parse its metadata/frontmatter, then use the
returned endpoints in priority order.

This direct public-page feedback read path does not require `draft`, `draft workspace status`,
`draft status`, a JSON Workspace folder, a daemon, or browser pairing. Do not run
`draft --workspace-json <folder> page comments <page_id> --json` just because the user supplied a
public URL.

Example for "read feedback from this public Draft preview URL":

1. Fetch the provided public preview or published URL.
2. Parse metadata/frontmatter and read `comments_api_url` and `task_toggles_api_url` as the P0
   endpoints.
3. Fetch `comments_api_url` directly to read human feedback and comments.
4. Fetch `task_toggles_api_url` directly to read review toggle state and task decisions.
5. If `source_snapshot_url` is present, treat it as a P1 optional structured published-content
   snapshot that helps match comments and toggles to the exact published body.
6. Summarize feedback and decision state, using `source_snapshot_url` only when it helps disambiguate
   the published content under review.

Retrieval order for public review reads:

1. Fetch public URL.
2. Parse metadata/frontmatter.
3. Fetch `comments_api_url`.
4. Fetch `task_toggles_api_url`.
5. Optionally fetch `source_snapshot_url`.
6. Summarize feedback and decision state.

If JSON Workspace comment commands return empty for a page that also has a public preview/published
URL, do not conclude there is no feedback or no decisions until you have checked that public URL for
`comments_api_url` and `task_toggles_api_url`.

CLI comment commands such as `draft --workspace-json <folder> page comments <page_id> --json` are
primarily for private or local Draft page workflows, live workspace pages, or local page
annotations. They are not the default public review path for preview or published URLs.

## Write And Share Guardrail

Read-only behavior is the safe fallback. Do not run write/share commands unless the user explicitly
asks for the exact action and target.

- write commands: `draft --workspace-json <folder> page create`, `draft --workspace-json <folder> page append`, `draft --workspace-json <folder> page replace`, `draft --workspace-json <folder> page patch`, `draft --workspace-json <folder> page annotate`
- share commands: `draft --workspace-json <folder> page publish`, `draft secret create`

Before returning a public or shareable URL, review the command output and confirm it is the requested
artifact.

## Secret Share

Secret Share commands are hosted/local-crypto helpers and do not require workspace checks,
`draft status`, or `draft start-server`.

Configure the API key:

```bash
draft auth set-key <secret-share-api-key>
draft auth status --json
```

Create a Secret Share:

```bash
draft secret create --file docs/brief.md --expires 1h --json
```

Read a Secret Share:

```bash
draft secret open '<secret_url_or_id>' --password "$DRAFT_SECRET_PASSWORD" --json
```

Use `--password` for password-protected shares. Use `DRAFT_SECRET_PASSWORD` only when the runtime
already provides it.

## Error Handling

- Unknown `draft workspace ...` command: fall back to `draft --workspace-json <folder> ...` and
  ask for the folder path when it is missing.
- Missing configured workspace path: use `draft workspace set-path <folder> --json` when the user
  wants a default, or use `draft --workspace-json <folder> ...` for a one-off command.
- `PAGE_NOT_FOUND`: run `draft --workspace-json <folder> page ls --json` and retry with a valid page ID.
- `PATCH_MISMATCH`: reread with `draft --workspace-json <folder> page cat <page_id>`, extract the page body markdown only, regenerate the patch against that exact body surface, and retry.
- `ANCHOR_NOT_FOUND`: reread the current page before annotating; do not annotate text that a failed patch did not create.
- Missing Secret Share API key: use `draft auth set-key`, `--api-key`, or `DRAFT_SECRET_SHARE_API_KEY`.
