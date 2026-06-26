---
name: awesome-paper-skill
description: End-to-end pipeline for topic-driven literature research: collect papers from multiple sources, generate an Awesome-style README, and update/push to user GitHub repo.
---

# Awesome Paper Skill

Use this skill when user asks for a full pipeline:

1. User gives a **topic**.
2. Agent researches papers (multi-source, not arXiv-only).
3. Agent builds/updates an Awesome-style `README.md`.
4. Agent pushes changes to user GitHub repo.

## Required Inputs

- `topic` (required)
- `repo_owner` (required)
- `repo_name` (required)
- `visibility` (optional, default: keep current repo visibility)
- `max_arxiv` / `max_crossref` / `max_semantic` (optional)

If owner/repo are omitted, use defaults from current workspace context or ask once.

## Pipeline

### 1) Fetch papers (multi-source)

```bash
python3 skills/awesome-paper-skill/scripts/fetch_papers.py \
  --topic "<topic>" \
  --max-arxiv 60 \
  --max-crossref 60 \
  --max-semantic 60 \
  --out /tmp/research_papers.json
```

Policy:
- Merge arXiv + Crossref + Semantic Scholar.
- Continue on partial source failures; report coverage gaps.
- De-duplicate by title/doi.

### 2) Build Awesome README

```bash
python3 skills/awesome-paper-skill/scripts/build_awesome_readme.py \
  --topic "<topic>" \
  --input /tmp/research_papers.json \
  --output /tmp/README.md
```

Formatting rules (strict):
- English-only.
- One paper per bullet.
- If venue known: show `[Venue]` line.
- If venue unknown: do **not** print `[Preprint]` line.
- Keep arXiv badge line.
- Keep GitHub badge line only when valid repo exists.
- Do **not** include Website placeholders/badges.
- Date on its own line: `(YYYY-MM-DD)`.

### 3) Publish/update GitHub repo

```bash
python3 skills/awesome-paper-skill/scripts/publish_repo.py \
  --owner "<repo_owner>" \
  --name "<repo_name>" \
  --readme /tmp/README.md \
  --visibility private
```

If repo exists: update README and push.
If repo does not exist: create then push.

## Quality Gates

Before final reply:
- README renders.
- `Total papers` count matches entries.
- No Website placeholder links.
- No fake `Repo Not Found` badges.
- Repo push succeeded.

## Deliverables to user

- Brief summary (what changed)
- GitHub commit/repo URL
