# Search Strategy - Clawic CLI

`clawic search` does local lexical scoring after downloading the registry index.
That means query wording matters more than with a semantic registry.

## Query Rules

### 1. Lead with likely product nouns

Good:
- `pocketbase`
- `github actions`
- `skill installer`
- `sentry`

Weak:
- `help with backend`
- `make deployments easier`
- `something for skills`

### 2. Rewrite intent into likely slug words

If the user says:
- "I need safer installs" -> try `skill installer`, `skill manager`, `install`
- "I need CI help" -> try `github actions`, `ci-cd`
- "I need product analytics" -> try `analytics`, `mixpanel`, `amplitude`

### 3. Split broad jobs into multiple probes

Instead of one vague query, probe the main job facets:
- creation
- inspection
- deployment
- analysis

### 4. Use `show` on near matches

If the result set is close but not obvious, inspect the top 1-3 matches before recommending an install.

## Why This Matters

The published package scores against:
- `slug`
- `name`
- `description`
- `summary`

Exact and prefix matches are rewarded heavily. Abstract paraphrases are not.
