---
name: convert-github-repository
description: >
  Use when (1) user provides a GitHub repository URL or local repo path and asks to convert it to a different format. (2) user asks to export a GitHub repository as Markdown documentation, JSON metadata, or CSV. (3) user wants to transform repository structure into a different representation (e.g., folder tree to JSON, issue tracker to README).
license: MIT
metadata:
  version: "1.0"
  category: productivity
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

## Core Position

This skill converts **GitHub repository content and metadata** into target formats (Markdown documentation, JSON metadata, CSV tables, folder tree JSON). It preserves structure and content fidelity across formats — not a simple file copy, but a semantic transformation that respects GitHub's data model (repos, trees, commits, issues, PRs, releases).

Key responsibilities:
- Parse GitHub repository structure (branches, directory tree, files) using GitHub API or local `.git` directory
- Convert repository data models (issues, PRs, releases, contributors) into target format representations
- Preserve file content and encoding (UTF-8, binary detection) during format transformation
- Provide a manifest of what was converted (file count, type breakdown, size summary)

## Modes

### `/convert-github-repository --markdown`
**Repository → Markdown documentation.** Converts the entire repository into a set of Markdown files:
- `README.md` from repository root
- Each directory becomes a subdirectory with `README.md` describing its contents
- Issues exported as `issues/YYYY-MM-DD-{number}-{title}.md`
- PRs exported as `pull-requests/YYYY-MM-DD-{number}-{title}.md`
- Releases exported as `releases/v{semver}.md`
- Code files preserved in original language with syntax highlighting fences

### `/convert-github-repository --json`
**Repository → JSON metadata.** Exports repository structure and content as a JSON file:
```json
{
  "repo": { "name": "...", "description": "...", "stars": N, "license": "...", "topics": [...] },
  "files": [{ "path": "...", "size": N, "type": "file|dir", "sha": "..." }],
  "branches": [{ "name": "...", "last_commit": "..." }],
  "contributors": [{ "login": "...", "contributions": N }]
}
```

### `/convert-github-repository --csv`
**Issues + PRs → CSV.** Exports issues and pull requests as CSV rows with columns: `number, title, state, author, created_at, updated_at, labels, assignees, milestone, body_preview`.

### `/convert-github-repository --tree`
**Repository → folder tree JSON.** Outputs a tree structure representing the repository layout:
```json
{
  "path": "/",
  "type": "directory",
  "children": [
    { "path": "src/index.js", "type": "file", "size": 1234, "language": "JavaScript" },
    { "path": "tests/", "type": "directory", "children": [...] }
  ]
}
```

### `/convert-github-repository --readme-to-json`
**README.md → structured JSON.** Parses a README.md and extracts: title (first H1), description (first paragraph after title), installation steps, usage examples, contributing guidelines, license.

## Execution Steps

1. **Identify repository source**


**Remote GitHub repo:** Parse URL to extract `owner` and `repo`:
```
https://github.com/owner/repo -> {owner: "owner", repo: "repo"}
```
Use GitHub API with `GITHUB_TOKEN` from env (`os.getenv("GITHUB_TOKEN")`).

**Local repository:** Verify `.git` directory exists. Use `git` CLI to extract:
- `git ls-files` for file list
- `git log --oneline` for recent commits
- `git remote get-url origin` to confirm repo identity

If neither source is available, report: "Cannot identify repository source — provide either a GitHub URL (https://github.com/owner/repo) or a local path with a .git directory."

2. **Fetch repository metadata**


For remote repos, call GitHub API:
```
GET https://api.github.com/repos/{owner}/{repo}
Authorization: Bearer {GITHUB_TOKEN}
Accept: application/vnd.github+json
```

Response contains: `full_name`, `description`, `stargazers_count`, `forks_count`, `license.spdx_id`, `topics`, `default_branch`, `created_at`, `updated_at`, `homepage`, `language`.

If the token is missing or rate-limited (403), try unauthenticated (lower rate limit) or report: "GitHub API unavailable — check GITHUB_TOKEN or try again later (rate limit: 60 req/hr unauthenticated)."

3. **Fetch repository contents**


**Get default branch tree:**
```
GET https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1
```

Returns a flat list of all files with `path`, `type` (blob/tree), `size`, `sha`.

**For local repos:** Run `git ls-tree -r --name-only {branch}` to get the file list, then `git show {sha}:{path}` to read file content.

Filter out common non-essential paths:
- `node_modules/`, `.git/`, `vendor/` — skip unless specifically requested
- Binary files (images, PDFs, compiled binaries) — include in manifest but not content
- `.gitignore`-referenced files that are not committed — skip

4. **Convert to target format**


**`--markdown` conversion:**
- README.md: Preserve as-is, update relative links to point to local files
- Code files: Write with syntax-highlighting fence (```language) based on file extension mapping:
  - `.js` → ` ```javascript`, `.py` → ` ```python`, `.go` → ` ```go`, `.rs` → ` ```rust`, etc.
- Directories: Create `README.md` in each directory with list of contained files
- Issues: Each issue becomes `{number}-{slug}.md` with frontmatter:
  ```yaml
  ---
  number: 42
  state: open
  author: username
  created: 2024-01-15
  labels: [bug, help-wanted]
  ---
  # Title
  body text...
  ```
- PRs: Same format as issues, plus `merged` field and review comments

**`--json` conversion:**
- Build nested structure from flat file list (group by directory path)
- Include file content for text files (base64 encode if large > 1MB)
- For large repos (>10K files), stream output to avoid memory exhaustion

**`--csv` conversion:**
- Headers: `number,title,state,author,created_at,updated_at,labels,assignees,milestone,body_preview`
- Labels: join with `;` delimiter
- Assignees: join with `;` delimiter
- Body preview: first 200 chars, strip markdown formatting
- Quote fields that contain commas; escape internal double quotes as `""`

**`--tree` conversion:**
- Build recursive tree structure
- Detect language from extension using common mapping (`.js` → JavaScript, `.py` → Python, etc.)
- Report total file count, directory count, size breakdown by type

**`--readme-to-json` conversion:**
- Parse markdown using regex or a simple state machine:
  - First `# Heading` → `title`
  - Paragraphs between headings → sections (`installation`, `usage`, `contributing`, etc.)
  - Code blocks → `code_examples` array
  - Tables → parsed as arrays of objects
  - Links `[text](url)` → collected in `links` array

5. **Validate output**


Before delivering:
- If format is JSON: parse with `json.loads()` and confirm no errors
- If format is CSV: verify all rows have same column count
- If format is Markdown: verify all files are readable UTF-8
- Check that files were not silently skipped — report count of skipped vs converted

6. **Deliver with manifest**


Return the converted output plus a manifest:
```
{
  "format": "markdown",
  "files_converted": 142,
  "files_skipped": 3,
  "skipped_reasons": [
    {"path": "node_modules/package/index.js", "reason": "binary or non-text, excluded by default"},
    {"path": ".git/config", "reason": "contains sensitive data"}
  ],
  "total_size_bytes": 2048576,
  "output_path": "./{repo-name}-converted/"
}
```

## Mandatory Rules

### Do not

- Do not hardcode GitHub token — use `os.getenv("GITHUB_TOKEN")`
- Do not convert binary files (images, PDFs, compiled binaries) as text — detect by extension or size > 5MB
- Do not convert files listed in `.gitignore` unless user explicitly requests `--include-ignored`
- Do not silently skip files — every skip must appear in `skipped_reasons` in the manifest
- Do not produce output that fails format validation (malformed JSON, unparseable CSV)
- Do not convert private repos without authentication — verify 401 is not returned before proceeding

### Do

- Always produce a manifest with `files_converted`, `files_skipped`, `skipped_reasons`
- Preserve file encoding — read as binary, decode as UTF-8, replace invalid bytes with `\uFFFD`
- Report the exact file count and size for transparency
- Use pagination when fetching issues/PRs (GitHub API paginates at 30/100 per page)
- For local repos, use `git` CLI — never assume raw file access is available
- Filter out common non-code directories (node_modules, .git, __pycache__, build/, dist/) by default

## Quality Bar

| Criterion | Minimum | Ideal |
|-----------|---------|-------|
| Content preservation | 100% of text file content preserved | Binary files listed in manifest, not content-lost |
| Format validity | Output passes format parser | Strict schema validation (JSON: draft-7, CSV: consistent columns) |
| Manifest completeness | Every skipped file has a reason | Every converted file listed with size and type |
| Encoding correctness | UTF-8 for all text files | Invalid bytes replaced with U+FFFD, not dropped or garbled |
| Rate limit handling | 403 triggers re-auth attempt | Proactive pagination with token refresh on 403 |
| Large repo handling | < 500MB memory for repos up to 10K files | Streaming JSON output, chunked file writes |

A good output passes the target format parser without errors, preserves all semantic content, and includes a complete manifest of what was converted and why some files were skipped.

## Good vs. Bad Examples

| Scenario | Bad | Good |
|---------|-----|------|
| Missing token | Retries unauthenticated forever | Reports "GitHub API auth required — set GITHUB_TOKEN environment variable" |
| Binary file | Tries to read as text, garbles content | Skips binary, reports in manifest: `{"path": "logo.png", "reason": "binary/image, excluded"}` |
| Large repo | Loads all files into memory, crashes | Streams output, reports "Processed 8,432 of 12,000 files (70%)" |
| Rate limited | Fails silently after 3 requests | Reports "Rate limit exceeded (403) — retry after 14:32 UTC or set GITHUB_TOKEN" |
| Missing field | Skips `homepage` when absent | Includes `"homepage": null` — no field silently dropped |
| Format error | Writes malformed JSON with trailing comma | Validates with `json.dumps()`, reports "Output invalid: unexpected token at line 847" |
| Local repo path | Assumes `~/repo` exists | Checks `.git` directory, reports "Path is not a git repository: ./myrepo" |