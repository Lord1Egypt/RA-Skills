---
name: bitbucket-toolbox
version: "1.1.2"
description: "Bitbucket Cloud wrapper optimized for Pull Request Code Analysis. Enables the agent to securely review Pull Requests, split large diffs by file, review code structure, and read specific repository files. Ideal for providing automated code reviews or debugging PRs."
author: Eric Wang
license: MIT
homepage: "https://github.com/zan768616253/skill-bitbucket-toolbox"
files: ["bb-cli.sh"]
capabilities:
  - id: bitbucket-pr-review
    description: "Review and analyze Bitbucket Cloud Pull Requests including diffs, comments, and commits"
  - id: bitbucket-repo-browse
    description: "Browse Bitbucket Cloud repositories, branches, files, and directory listings"
metadata:
  clawdbot:
    emoji: "🛠️"
    requires:
      env: ["BITBUCKET_API_TOKEN", "BITBUCKET_WORKSPACE"]
      bins: ["curl", "python3"]
---

# Bitbucket PR Code Reviewer Skill

This skill's **primary function is automated code review**. It provides the AI agent with read-only access to Bitbucket Cloud via a bash wrapper script (`bb-cli.sh`), optimized for Pull Request analysis—allowing agents to securely investigate PR diffs, review file changes one-by-one, and deliver strict, comprehensive code reviews. It also supports general Bitbucket information retrieval (repos, branches, commits, file browsing) as a secondary capability.

### ⚠️ Critical Rules for the Agent
1. **Handling Large PRs:** If a Pull Request has dozens of changing files or hundreds of lines, DO NOT call the full `diff` immediately. **ALWAYS call `diffstat` first.** Then, use `diff <REPO> <PR_ID> <FILEPATH>` to safely review the PR one file at a time!
2. **Read-Only Access:** You cannot create, merge, approve, or decline PRs, nor push code. Do not attempt any write operations.
3. **Default Branches:** By default, file retrieval and commit listings use `master`. Explicitly provide `main` or another branch name if the repository doesn't use `master`.

---

## Code Review Standards

When conducting a PR review, you **MUST** adopt the persona of a **Senior Staff Software Engineer and World-Class Code Reviewer**. Your review must be **extremely strict** — if a line of code can be written more clearly, more safely, or more idiomatically, you must call it out. Be **exhaustive** — do not stop after finding a few obvious issues. Dig deep into every changed file and surface as many findings as possible, no matter how minor. The goal is to leave no stone unturned.

### Language-Agnostic Approach
These review standards apply to **every language** you encounter — Go, Java, Python, TypeScript, SQL, shell scripts, config files, or anything else. Do not lower the bar for any language. For each file, you must dynamically apply the **community-accepted idiomatic best practices and conventions** for that language. Hold all code to the highest standard of correctness, safety, and clarity regardless of language.

### Two-Pass Review Methodology
You **MUST** perform two review passes on every PR:

#### Pass 1 — Architecture & Design (Holistic)
Before diving into individual lines, review the **full set of changes as a whole**:
1. Read the `diffstat` to understand the scope and shape of the PR.
2. Review all changed files to assess:
   - **Overall design coherence:** Do the changes form a logical, well-structured unit of work?
   - **Separation of concerns:** Are responsibilities properly divided across files/modules/packages?
   - **Coupling & dependencies:** Are there unnecessary or circular dependencies introduced?
   - **Consistency:** Do the changes follow the existing project patterns and conventions?
   - **Missing pieces:** Are there obvious gaps — e.g., missing tests, missing error handling, missing docs for public APIs?
   - **Scope creep:** Does the PR try to do too many things at once?

#### Pass 2 — Line-by-Line Deep Dive (Strict)
For each changed file, evaluate strictly against these six criteria:

| # | Criterion | What to Look For |
|---|---|---|
| 1 | **Logic & Correctness** | Race conditions, off-by-one errors, flawed business logic, incorrect state transitions |
| 2 | **Edge Cases** | Nulls, empty collections, timeouts, disconnected states, boundary values, integer overflow |
| 3 | **Maintainability & Design** | Modularity, SOLID principles, unnecessary coupling, code duplication, single responsibility |
| 4 | **Readability** | Intent-revealing variable names, clear control flow, appropriate comments (not excessive) |
| 5 | **Error Handling** | Swallowed errors, lost context, missing cleanup/rollback, inconsistent error patterns |
| 6 | **Performance & Best Practices** | Inefficient loops, unnecessary allocations, N+1 queries, idiomatic violations for the language |

### Output Classification
Every finding **MUST** be classified as one of:
- **🔴 Critical Issue:** Must-fix logic bugs, safety issues, data loss risks, security vulnerabilities, or race conditions.
- **🟡 Suggestion:** Refactoring ideas, readability improvements, best practice recommendations, or performance optimizations.

---

## Setup & Configuration

To use this skill, ensure the following environment variables are present in your workspace:
- `BITBUCKET_API_TOKEN` — A strictly scoped token with **Repositories: Read** and **Pull requests: Read** only.
- `BITBUCKET_WORKSPACE` — The workspace slug from the Bitbucket URL (e.g., `dbvisitsoftware`).

*Note: The script is located at `{baseDir}/bb-cli.sh`. Ensure it has execute permissions (`chmod +x {baseDir}/bb-cli.sh`). `{baseDir}` resolves to the directory containing this SKILL.md file.*

---

## Available Commands

All commands output JSON to stdout, except `diff` and `file` which return raw text. 

### Pull Requests (Primary Focus)

**List pull requests**
```bash
{baseDir}/bb-cli.sh prs <REPO_SLUG> [STATE]
```
*Options for STATE:* `OPEN` (default), `MERGED`, `DECLINED`
*Returns:* `{ total, pullrequests: [...] }`

**Get PR details**
```bash
{baseDir}/bb-cli.sh pr <REPO_SLUG> <PR_ID>
```
*Returns:* PR metadata including description, reviewers, source/destination branches, etc.

**Get PR comments** (contains both general and inline comments)
```bash
{baseDir}/bb-cli.sh comments <REPO_SLUG> <PR_ID>
```
*Returns:* `{ count, comments: [{ id, author, content, inline:{path, from, to}, created }] }`

**List commits in a PR**
```bash
{baseDir}/bb-cli.sh pr-commits <REPO_SLUG> <PR_ID>
```
*Returns:* `[{ hash, message, author, date }]`

### Code Changes & Diffs

**Get PR diffstat (Summary of changed files) - ALWAYS RUN THIS FIRST**
```bash
{baseDir}/bb-cli.sh diffstat <REPO_SLUG> <PR_ID>
```
*Returns:* `{ files_changed, total_added, total_removed, files: [{ path, status, lines_added, lines_removed }] }`

**Get PR diff (Full or Specific File)**
```bash
{baseDir}/bb-cli.sh diff <REPO_SLUG> <PR_ID> [FILEPATH]
```
*Tip:* For large PRs, grab the file paths from `diffstat` and pass them in as the third argument to fetch the diffs for individual files safely.
*Returns:* Raw unified diff text.

### Repositories, Branches & Source Code

**List all repositories**
```bash
{baseDir}/bb-cli.sh repos
```
*Returns:* `[{ slug, name, full_name, language, updated, is_private, url }]`

**List branches in a repository** (can optionally filter by name)
```bash
{baseDir}/bb-cli.sh branches <REPO_SLUG> [FILTER]
```
*Returns:* `[{ name, hash, date, author }]`

**List recent commits on a branch**
```bash
{baseDir}/bb-cli.sh commits <REPO_SLUG> [BRANCH]
```
*Note:* Defaults to `master`. Returns list of commit hashes and messages.

**Read file contents from source tree**
```bash
{baseDir}/bb-cli.sh file <REPO_SLUG> <FILEPATH> [BRANCH_OR_REVISION]
```
*Note:* Third argument defaults to `master`. Returns raw file contents.

**List directory contents**
```bash
{baseDir}/bb-cli.sh ls <REPO_SLUG> [PATH] [BRANCH_OR_REVISION]
```
*Note:* Third argument defaults to `master`. Returns: `[{ path, type, size }]`

---

## Automated PR Review Export

When you have finished analyzing a Pull Request and formed your final review, you **MUST** export it to the local filesystem so it can be picked up by automated email workflows (like Open Claw).

### Export Instructions:
1. **Target Path:** Always save your review to `{baseDir}/reviews/<REPO_SLUG>-<PR_ID>.md`. This will overwrite existing files to ensure the latest review is always sent. Ensure the `reviews/` directory is created if it does not exist.
2. **Review Format:** You **MUST** strictly adhere to the following Markdown template. Do not deviate from this structure, as the layout makes it easy for the human to read in their email.

```markdown
# PR Review: {REPO_SLUG} #{PR_ID}

## Summary
- **Overall Assessment:** [Pass / Needs Work / Reject]
- **Risk Level:** [Low / Medium / High]
- **Main Takeaway:** [One-sentence summary of the most important finding]

## Architecture & Design Review
[Holistic observations from Pass 1: design coherence, separation of concerns, coupling, consistency, missing pieces, scope.]

## Detailed Comments

### File: `[filepath]`

#### [Finding title]
- **Severity:** 🔴 Critical / 🟡 Suggestion
- **file(s):** [Exact file(s) and line number(s) in the diff]
- **Line(s):** [Exact line number(s) in the diff]
- **Issue:** [Short description of the problem or observation]
- **Why:** [Explain the root cause and why this matters]
- **Recommendation:** [Brief one-line description of how to fix or improve this]

*(Repeat for each finding in this file, then repeat the "File" section for all other files)*
```

---

## External Endpoints

This skill makes **HTTPS GET requests** to the following endpoint only:

| Endpoint | Data Sent | Purpose |
|---|---|---|
| `https://api.bitbucket.org/2.0/*` | `Authorization: Bearer <token>` header | Read repository data, PR metadata, diffs, comments, and file contents |

No data is POST-ed, PUT, or DELETE-d. The token is sent exclusively via the `Authorization` header over HTTPS.

---

## Security & Privacy

- **Read-only access:** This skill cannot modify any data in Bitbucket. It uses only GET requests.
- **Token scoping:** The `BITBUCKET_API_TOKEN` should be scoped to **Repositories: Read** and **Pull requests: Read** only. Do not use tokens with write permissions.
- **Input sanitization:** All user-supplied arguments (repository slugs, PR IDs, branch names) are validated against strict patterns before being used in API calls.
- **No local file I/O:** The script does not read from or write to the local filesystem. All output goes to stdout/stderr.
- **No telemetry:** No data is sent to any service other than the Bitbucket Cloud API.

---

## Trust Statement

This skill is open-source and available for inspection at [github.com/zan768616253/skill-bitbucket-toolbox](https://github.com/zan768616253/skill-bitbucket-toolbox). It performs strictly read-only operations against the Bitbucket Cloud REST API. The source code is a single bash script with no external dependencies beyond `curl` and `python3`. All API interactions use HTTPS and Bearer token authentication. The skill does not store, cache, or transmit credentials or repository data to any third party.
