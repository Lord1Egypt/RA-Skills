---
name: commit-poetry
version: 1.0.0
description: >
  Transforms your git history into poetry — sonnets from sprint logs, haiku
  from hotfixes, limericks from legacy code, and epic ballads from major
  rewrites. Turns the mundane chronicle of software development into genuine
  literary art. Also: the most entertaining way to review what actually
  happened last quarter.
author: J. DeVere Cooley
category: fun-tools
tags:
  - creative
  - git-history
  - poetry
  - entertainment
metadata:
  openclaw:
    emoji: "📝"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - fun
      - creative
---

# Commit Poetry

> "In the beginning was the commit. And the commit was 'init'. And it was without form, and void."

## What It Does

Your git log is a chronicle. Every commit message, every branch name, every merge conflict resolution tells a story. Commit Poetry reads that story and retells it as **actual poetry** — matching the poetic form to the nature of the work.

Bug fixes become haiku (short, precise, illuminating). Rewrites become epic poetry (long, dramatic, transformative). Merge conflicts become dramatic dialogues. And the commit history of a legacy module becomes a Gothic horror novella.

## The Poetic Forms

### Haiku (5-7-5 syllables)
*For: Bug fixes, one-line changes, moments of clarity*

```
From commit: "fix: null check in user validation"

  Undefined lurks here
  A single question mark saves
  The production night

From commit: "fix: off-by-one in pagination"

  Less than, not less-or
  Equal — one character changed
  A thousand rows spared

From commit: "remove unused import"

  You were invited
  But never called upon — gone
  The bundle breathes now
```

### Limerick
*For: Silly bugs, embarrassing fixes, "I can't believe this was the problem"*

```
From commit: "fix: typo in environment variable name"

  A developer keen and quite bright
  Debugged through the day and the night
    The prod server crashed
    The logs were all trashed
  'Twas DATABSE_URL spelled not right

From commit: "fix: accidentally committed node_modules"

  A junior pushed code with great pride
  Then noticed the diff was too wide
    Eight thousand new files
    Stretched on for miles
  node_modules was along for the ride
```

### Sonnet (14 lines, iambic pentameter)
*For: Sprint retrospectives, feature completions, meaningful milestones*

```
From: Sprint 42 commit history (checkout rewrite)

  When first we faced the checkout's tangled mess,
  A thousand lines of logic intertwined,
  With payment flows that no one could assess,
  And edge cases the tests could never find.

  Through patient weeks we carved the monolith,
  Each function split to serve a single aim,
  With types to guard the contracts we built with,
  And tests to prove the output stayed the same.

  The old code fell like autumn's fading leaves,
  While new abstractions rose to take their place,
  Each module clean, each boundary that achieves
  The independence of its own namespace.

    So here we ship, with coverage at ninety-four,
    What once was tangled, tangled now no more.
```

### Ballad
*For: Major rewrites, migrations, epic multi-month efforts*

```
From: The Great TypeScript Migration (6 months of commits)

  Come gather 'round, developers all,
  And hear the tale I tell,
  Of JavaScript's long, untyped reign,
  And how the types befell.

  'Twas in the year of twenty-five,
  The errors grew too grand,
  "Cannot read property of undefined!"
  Rang across the land.

  A hero rose, with tsconfig bright,
  And strict mode set to true,
  "AllowJs first," the hero cried,
  "We'll migrate file by file, through."

  Three hundred files of .js to .ts,
  Each `any` type a sin,
  With every interface defined,
  The safety grew within.

  Six months it took, through storm and strife,
  But when the deed was done,
  The compiler caught a thousand bugs
  Before a single one could run.
```

### Free Verse
*For: Chaotic periods, production incidents, "what even happened this week"*

```
From: Incident INC-3847 commit sequence

  3:47 AM
  the pager screams

  "fix: increase connection pool"
  (it wasn't the connection pool)

  "fix: actually increase timeout"
  (it wasn't the timeout either)

  "revert: actually increase timeout"
  4:12 AM

  "fix: the real fix — cache stampede on expired session"
  (it was always the cache)
  (it is always the cache)

  "chore: add monitoring for cache hit rate"
  5:30 AM

  the sun rises on a fixed system
  the developer does not rise until noon
```

### Dramatic Dialogue
*For: Merge conflicts, opposing PRs, refactor debates*

```
From: Merge conflict between feature/new-auth and feature/new-logging

  ACT I: The Merge

  AUTH BRANCH:
    "I have rewritten the middleware!
     Request flows through ME now, authenticated,
     Validated, blessed with tokens divine."

  LOGGING BRANCH:
    "And I have rewritten the middleware!
     Request flows through ME now, observed,
     Measured, timestamped for eternity."

  GIT:
    "CONFLICT in src/middleware/index.ts"

  DEVELOPER:
    (staring at <<<<<<< HEAD)
    "Why. Why do both of you touch the same file."

  AUTH BRANCH:
    "I was here first."

  LOGGING BRANCH:
    "My PR was approved first."

  DEVELOPER:
    (opens coffee)
    (it is 9 AM and already too late for this)

  ACT II: The Resolution — 47 lines, both changes preserved,
  a new middleware chain that serves two masters.
  The developer commits with the message: "fix: merge conflict"
  and speaks of it no more.
```

### Gothic Horror
*For: Legacy code, ancient modules, the file nobody wants to touch*

```
From: git log --follow src/legacy/invoice-generator.js

  THE INVOICE GENERATOR
  A Tale of Horror in Five Chapters

  Chapter I: Genesis (2019)
    It was born in innocence — 47 lines,
    a simple function that turned numbers into PDFs.
    Its creator committed it with the message "add invoicing"
    and was never heard from again.

  Chapter II: Growth (2020)
    It grew. Tax calculations. Multi-currency. Discounts.
    Five developers contributed. None read what the others wrote.
    By December it was 847 lines and had achieved sentience.

  Chapter III: The Warnings (2021)
    "TODO: refactor this" appeared on line 12.
    Then line 89. Then line 234.
    The TODOs were never addressed.
    They remain, like headstones.

  Chapter IV: Abandonment (2022-2024)
    No commits for 26 months. The module was sealed.
    Developers spoke of it in whispers.
    "Don't touch invoice-generator."
    "Why?" "Just don't."

  Chapter V: Today
    It runs. It generates invoices. It handles $2M monthly.
    Nobody understands it. Nobody will touch it.
    It has no tests. It has no documentation.
    It has only... the TODOs. Waiting.
```

### Rap Verse
*For: Celebratory moments, shipping features, team victories*

```
From: v2.0.0 release tag

  Yo, we shipped the two-point-oh, let me break it down,
  Rewrote the whole stack, turned the codebase around,
  TypeScript strict mode, every type is sound,
  Coverage ninety-five, bugs? They can't be found.

  GraphQL on the API, REST is deprecated,
  Kubernetes deployed, auto-scaled and federated,
  Auth is OAuth2, sessions been cremated,
  Six months of work and we finally graduated.

  Shout out to the team who survived the migration,
  The merge conflicts, the failed CI, the frustration,
  But we're live in prod with zero degradation,
  v2.0 — standing ovation. 🎤
```

## Poetry Modes

| Mode | Input | Output |
|---|---|---|
| **Last Commit** | Most recent commit | Haiku |
| **Last Sprint** | 2-week commit history | Sonnet or Free Verse |
| **Feature Branch** | All commits on a branch | Ballad or Dialogue |
| **File History** | Full history of one file | Gothic Horror or Epic |
| **Incident** | Commits during an incident timeframe | Free Verse (always) |
| **Release** | All commits between two tags | Rap Verse or Ballad |
| **Merge Conflict** | Conflicting commits | Dramatic Dialogue |
| **Random** | Any commit | Limerick |

## When to Invoke

- **Sprint retro** — Present the sprint as a sonnet instead of a bullet list
- **Friday afternoon** — Turn the week's commits into limericks (team morale++)
- **After a production incident** — The free verse write-up is better than any postmortem
- **Release celebration** — Rap verse for the release notes
- **When the legacy code scares you** — Gothic horror for catharsis
- **When you need a laugh** — Random limerick mode on any commit

## Why It Matters

Git logs are the most accurate record of what a team actually did — but nobody reads them because they're boring. Poetry makes the history memorable, shareable, and genuinely enjoyable.

Also: a sonnet about a sprint is a more honest retrospective than most retro meetings produce.

Zero external dependencies. Zero API calls. Pure literary engineering.
