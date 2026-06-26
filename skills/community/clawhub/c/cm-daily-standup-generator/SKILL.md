---
name: cm-daily-standup-generator
description: Generate structured daily standup reports by analyzing git commits, pull request activity, issue trackers, and project context. Produces yesterday/today/blockers summaries tailored to your team's standup format. Use when asked to prepare a standup, summarize yesterday's work, generate a daily status update, create a standup report, or draft a scrum update. Triggers on "standup", "daily standup", "scrum update", "daily status", "what did I do yesterday", "standup report", "daily report", "status update", "stand-up".
metadata:
  tags: ["standup", "scrum", "agile", "productivity", "git", "project-management", "daily-report", "team-collaboration"]
---

# Daily Standup Generator

Generate comprehensive daily standup reports by analyzing your actual development activity across git history, pull requests, issue trackers, and branch context. Instead of trying to remember what you did yesterday, this skill reads the evidence and builds an accurate, well-structured standup for you.

## Usage

Invoke this skill when you need to prepare for a daily standup meeting or async status update. The agent examines your recent development activity and produces a structured report.

**Basic invocation:**
> Generate my standup report

**With options:**
> Generate my standup for the last 2 days
> Generate standup for user "jane.doe" in /path/to/repo
> Generate standup report covering repos /app and /infrastructure

The agent will ask clarifying questions if needed (which repo, which git author, time range).

## How It Works

### Step 1: Identify the Developer and Time Range

The agent determines who the standup is for and what period to cover:

- **Git author**: detected from `git config user.name` and `git config user.email` in the target repository. Can be overridden if the user specifies a name or email.
- **Time range**: defaults to "since yesterday morning" (the last working day). Adjusts for weekends and holidays automatically: if today is Monday, it covers Friday through Sunday. The user can request a custom range (e.g., "last 2 days", "since Tuesday").

```bash
# The agent runs these to identify context
git config user.name
git config user.email
date +%A    # Check day of week for weekend adjustment
```

### Step 2: Gather Git Commit Activity

The agent collects all commits authored by the developer in the time range:

```bash
# Fetch recent commits with full context
git log --author="developer@email.com" --since="yesterday 00:00" \
  --format="%h|%s|%b|%ai|%D" --all

# For multi-repo setups, the agent repeats across each repository
git -C /path/to/repo log --author="developer@email.com" \
  --since="yesterday 00:00" --format="%h|%s|%b|%ai" --all
```

The agent then analyzes commits to:
- **Group by logical work stream**: related commits are clustered (e.g., all commits touching auth module grouped under "Authentication refactor")
- **Extract meaningful descriptions**: commit messages are parsed, conventional commit prefixes interpreted (feat, fix, refactor, docs, test, chore)
- **Identify scope of changes**: `git diff --stat` for key commits to understand magnitude
- **Detect work patterns**: large refactors vs. small fixes vs. new features

```bash
# Understand the scope of specific commits
git diff --stat HEAD~5..HEAD --author="developer@email.com"

# Check which files/modules were touched
git log --author="developer@email.com" --since="yesterday 00:00" \
  --name-only --format="" | sort -u
```

### Step 3: Analyze Pull Request Activity

The agent checks GitHub/GitLab for PR-related work:

```bash
# PRs authored by the developer (opened, merged, updated)
gh pr list --author="@me" --state all --json title,state,url,updatedAt,reviews,labels

# PRs reviewed by the developer
gh pr list --json title,state,url,reviews \
  --jq '.[] | select(.reviews[]?.author.login == "username")'

# Recently merged PRs
gh pr list --author="@me" --state merged --json title,url,mergedAt \
  --jq '.[] | select(.mergedAt > "2026-04-29T00:00:00Z")'
```

The agent categorizes PR activity into:
- **PRs opened**: new work submitted for review
- **PRs merged**: completed work that shipped
- **PRs reviewed**: code review contributions to teammates
- **PRs updated**: addressed review feedback, resolved conflicts
- **PRs with blockers**: PRs awaiting review, failing CI, or with unresolved conversations

### Step 4: Check Issue Tracker Activity

The agent looks for issue movement:

```bash
# Issues assigned to the developer
gh issue list --assignee="@me" --state all \
  --json title,state,url,labels,updatedAt

# Recently closed issues
gh issue list --assignee="@me" --state closed \
  --json title,url,closedAt \
  --jq '.[] | select(.closedAt > "2026-04-29T00:00:00Z")'

# Issues with recent comments from the developer
gh issue list --json title,url,comments \
  --jq '.[] | select(.comments[-1]?.author.login == "username")'
```

### Step 5: Detect Active Branches and Work-in-Progress

The agent identifies what the developer is currently working on:

```bash
# Current branch
git branch --show-current

# Recent branches with activity
git for-each-ref --sort=-committerdate --count=5 \
  --format='%(refname:short)|%(committerdate:relative)|%(subject)' \
  refs/heads/

# Uncommitted work (staged and unstaged)
git status --porcelain

# Stashed work
git stash list
```

This reveals:
- Active feature branches and their purpose
- Uncommitted changes that indicate ongoing work
- Stashed work that might need attention

### Step 6: Identify Blockers and Risks

The agent proactively identifies potential blockers by checking:

- **Failing CI**: PRs with red checks
  ```bash
  gh pr checks --json name,state,conclusion \
    --jq '.[] | select(.conclusion == "failure")'
  ```
- **Stale PRs**: PRs open more than 48 hours without review
- **Dependency waits**: PR descriptions or commit messages mentioning "blocked by", "waiting for", "depends on"
- **Merge conflicts**: branches that diverge significantly from main
  ```bash
  git log --oneline main..feature-branch | wc -l
  git merge-tree $(git merge-base main feature-branch) main feature-branch
  ```
- **Unresolved review threads**: PRs with pending requested changes

### Step 7: Synthesize the Standup Report

The agent compiles everything into a structured standup report with three sections:

#### Yesterday (What I Did)

The agent groups completed work into logical categories:
- Feature development (commits, PRs merged)
- Bug fixes (fix commits, issues closed)
- Code reviews performed
- Infrastructure/DevOps work
- Documentation updates
- Meetings and discussions (inferred from gaps in commit activity or mentioned in commit messages)

Each item includes:
- A clear, human-readable description (not raw commit messages)
- Links to relevant PRs and issues
- Scope indication (e.g., "3 files changed" or "major refactor across 12 files")

#### Today (What I Plan to Do)

The agent infers planned work from:
- Open PRs that need attention (review feedback to address)
- In-progress branches with uncommitted work
- Issues assigned and not yet started
- Follow-up work from yesterday's PRs (e.g., "merge after CI passes")
- Sprint board items (if accessible)

#### Blockers

The agent surfaces anything that could slow down progress:
- PRs waiting for review (with reviewer names and wait time)
- Failing CI pipelines (with failure details)
- Merge conflicts
- Dependencies on other team members' work
- External dependencies (API access, credentials, environments)

### Step 8: Format and Deliver

The agent produces the standup in the requested format:

**Default format (concise bullet points):**
```
## Standup — April 30, 2026

### Yesterday
- Completed authentication token refresh logic (PR #142, merged)
- Fixed race condition in session cleanup (commit a3f9c21)
- Reviewed 2 PRs: #138 (caching layer), #140 (metrics endpoint)

### Today
- Address review feedback on PR #145 (API rate limiting)
- Start work on PROJ-289: user export feature
- Merge PR #142 after CI passes

### Blockers
- PR #145 waiting for review from @backend-team (opened 2 days ago)
- Staging environment down since yesterday — can't test export feature
```

**Verbose format** adds context, file lists, and diff stats.

**Slack format** produces a compact message suitable for async standup channels.

**JSON format** for integration with standup bots and dashboards.

## Output

The agent produces a standup report containing:

- **Yesterday section**: 3-8 bullet points summarizing completed work, grouped by work stream, with PR/issue links
- **Today section**: 2-5 bullet points of planned work, derived from open branches, assigned issues, and pending PRs
- **Blockers section**: 0-3 items that could slow progress, with specific details (who, what, how long)
- **Optional metrics**: commits count, files changed, PRs merged, reviews given

The report is written in first person, uses clear non-technical language where possible, and is sized for a 60-second verbal delivery (approximately 150-250 words).

## Multi-Repo Support

For developers working across multiple repositories, the agent scans each repo and produces a unified standup:

```
Repos analyzed:
  /home/dev/backend-api (12 commits)
  /home/dev/infrastructure (3 commits)
  /home/dev/shared-libs (1 commit)
```

Work items from different repos are interleaved chronologically and grouped by logical theme rather than by repository.

## Team Standup Mode

When invoked with a team flag, the agent generates standups for all team members:

> Generate standup for the whole team in /path/to/repo

This produces individual sections per developer, useful for team leads preparing for standup facilitation. The agent identifies cross-team dependencies (e.g., "Alice's PR #142 blocks Bob's feature branch").

## Tips for Best Results

- Run this skill from within the git repository you want to analyze, or specify the path
- Ensure `gh` CLI is authenticated (`gh auth status`) for PR and issue data
- For the most accurate "Today" section, keep your issue tracker assignments current
- Use conventional commit messages (feat:, fix:, docs:) for better categorization
- The agent handles monorepos by detecting subdirectory-scoped changes
