---
name: custom-skills-updater
description: Manage manually installed skills (non-ClawHub). Supports checking updates, updating, and listing custom skills from GitHub or local sources.
---

# custom-skills-updater

Manages **manually installed skills not installed from ClawHub**.

Supported types: `github-dir`, `github-file`, `github-readme`, `local`

This skill **checks and updates existing skills only**. It does NOT create new skills.

---

# Prerequisites

All GitHub operations require an authenticated `gh` CLI session.
Before any GitHub request, run `gh auth status`.
If it fails, prompt: `"Run gh auth login first."` and stop.

---

# Operations

## Check for updates

Scan `REGISTRY.yaml`, detect remote versions, compare with stored versions, report:

```
skill-name ........ up-to-date
skill-name ........ update available
```

## Update skills

Target all outdated skills or a specific skill by name.

1. Run update check
2. For each outdated skill, **notify the user before updating**:
   - Skill name and type
   - Summary of what changed (e.g. diff highlights, new commit description, or content delta)
   - How the update will be applied (overwrite, merge, delegate to `skill-creator`, etc.)
   - **Wait for explicit user approval** before proceeding
3. Update approved skill(s)
4. Update `REGISTRY.yaml`

If the user cannot respond immediately (e.g. scheduled/automated run, no active session), **do not execute updates**. Instead, write a summary of pending updates (skill name, change description, proposed action) and leave it for the user to review and approve later.

## List installed skills

Read and list all entries in `REGISTRY.yaml`.

---

# Registry

Location: `REGISTRY.yaml` in the same directory as this `SKILL.md`.

If it does not exist:

1. If `REGISTRY.example.yaml` exists, copy it to `REGISTRY.yaml`
2. Otherwise create with:
```yaml
skills: {}
```

**Do not rename the `skills` root key.**

## Format

Map structure keyed by skill name:

```yaml
skills:
  example-dir-skill:
    type: github-dir
    source: example-owner/example-repo@main:skills/example-dir-skill
    version: abc123
    updated: 2026-01-01
  example-readme-skill:
    type: github-readme
    source: example-owner/example-project@main
    version: def456
    updated: 2026-01-02
```

| Field   | Meaning |
|---------|---------|
| key     | skill name |
| type    | `github-dir` / `github-file` / `github-readme` / `local` |
| source  | source location |
| version | commit SHA (`github-dir`) or SHA256 (file-based types) |
| updated | last update date |

---

# Automatic Skill Discovery

Scan `skills/*/SKILL.md`. Only direct subdirectories of `skills/`, no recursion.

If a skill exists but is not in `REGISTRY.yaml`:

1. Notify the user and ask for source type and location
2. Add to registry

If unable to prompt, register as `local` and notify the user to configure later.

---

# Version Detection

Compare remote version against `version` in `REGISTRY.yaml`.

## github-dir

```
gh api "repos/{owner}/{repo}/commits?path={path}&per_page=1" --jq '.[0].sha // empty'
```

## github-file

```
gh api "repos/{owner}/{repo}/contents/{path}?ref={branch}" -H "Accept: application/vnd.github.raw+json" | shasum -a 256
```

## github-readme

Find README filename:

```
gh api "repos/{owner}/{repo}/contents/?ref={branch}" --jq '.[].name' | grep -i '^readme' | head -n 1
```

Take first match, download and hash:

```
gh api "repos/{owner}/{repo}/contents/{readme_filename}?ref={branch}" -H "Accept: application/vnd.github.raw+json" | shasum -a 256
```

## local

Skip entirely.

---

# Update Procedure

Only update when remote version differs from stored `version`.

## github-dir

```
gh api "repos/{owner}/{repo}/tarball/{branch}" > archive.tar.gz
```

Verify the file is valid gzip before extracting. Copy target path to `skills/{name}/`.

## github-file

```
gh api "repos/{owner}/{repo}/contents/{path}?ref={branch}" -H "Accept: application/vnd.github.raw+json" > skills/{name}/SKILL.md
```

## github-readme

1. Download the new README using the same method as version detection
2. Compare the new README against the existing local README to identify changes
3. Assess change scope:
   - **Major changes** (structural changes, new/removed sections, significant content rewrites): check if the `skill-creator` skill is installed. If yes, delegate the SKILL.md update to `skill-creator` with the new README as input. If `skill-creator` is not installed, fall through to step 4.
   - **Minor changes** (wording tweaks, small additions): proceed to step 4 directly.
4. Evaluate whether the changes contradict any statements in the current `SKILL.md`, or introduce important new information that should be reflected in `SKILL.md`
5. Update the skill only for the relevant parts based on the evaluation above.
---

# Error Handling and Safety

Handle `gh api` failures by HTTP status:

| Status | Action |
|--------|--------|
| 401 | `"Authentication expired. Run gh auth login."` Stop all operations. |
| 403 | `"Permission denied or rate limit for {skill-name}."` Skip. |
| 404 | `"Source not found for {skill-name}."` Skip. |
| Other | `"Check failed for {skill-name}."` Skip. |

On any failure: do NOT overwrite local files, do NOT modify registry.

Registry updates: modify only the target entry, do not reorder or remove others, update `version` and `updated` only after success.

**This skill manages manually installed skills only. ClawHub-installed skills are out of scope.**
