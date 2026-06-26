---
name: Fact Check
description: |
  This skill should be used when the user asks to
  "fact check", "verify this", "is this true",
  "check the facts", "validate claims",
  "are these field names correct",
  "is this API still current",
  "驗證", "是真的嗎", "確認資訊正確",
  or when output contains version numbers, API references,
  model names, dates, or technical claims that could be outdated.
version: 0.1.1
---

# Fact Check: Verify Before You Ship

Verify that every claim, reference, and technical detail is backed by current evidence. AI models have training data cutoffs and frequently hallucinate version numbers, API signatures, field names, CLI flags, and dates. This skill provides a systematic process to catch these errors before they reach users.

## Why This Exists

AI models commonly produce these types of false information:

| Category | Example of Hallucination |
|----------|------------------------|
| **Model names/versions** | Referencing "GPT-5" or "Claude 4" when they don't exist yet |
| **API field names** | Writing `likeCount` when the real API returns `like_count` |
| **CLI flags** | Using `--recursive` when the tool only supports `-r` |
| **Library methods** | Calling `.transformAll()` on a library that has no such method |
| **Dates** | Getting today's date wrong, or citing a "2024 release" that happened in 2025 |
| **SDK versions** | Referencing `v2.0` features when the latest is `v1.8` |
| **Repo structure** | Claiming a file exists at a path where it doesn't |
| **Default values** | Stating "default is 100" when the actual default is 50 |

## The Verification Process

For every piece of output that contains technical claims, run this process:

### Step 1: Identify Claims

Scan the output and tag every verifiable claim:

- Version numbers (library, SDK, model, API)
- Field names (API response, config keys, database columns)
- CLI commands and flags
- URLs and endpoints
- Dates and timelines
- Default values and limits
- File paths and function names
- "It supports X" or "X is available" statements

### Step 2: Classify Each Claim

| Classification | Meaning | Action |
|---------------|---------|--------|
| **Verified** | Confirmed by tool output, API call, or file read | Mark with evidence source |
| **Unverified** | Not yet checked | Must verify before output |
| **Unverifiable** | Cannot be checked with available tools | Label clearly as unverified |
| **Stale** | Based on information older than 6 months | Re-verify from current source |

### Step 3: Verify Using Tools

**For each unverified claim, use the appropriate verification method:**

| Claim Type | Verification Method |
|-----------|-------------------|
| File exists at path | `ls /path/to/file` or Read tool |
| Function/method exists | `grep -r "function_name" /path/to/repo` |
| API field name | Make a real API call and inspect the response |
| CLI flag exists | `command --help` or `man command` |
| npm package version | `npm info package-name version` |
| Python package version | `pip show package-name` |
| GitHub repo info | `gh repo view owner/repo` |
| PR/Issue status | `gh pr view NUMBER --repo owner/repo` |
| Current date | `date` command |
| URL is reachable | `curl -s -o /dev/null -w "%{http_code}" URL` |
| Git branch/tag exists | `git ls-remote --tags origin` |

### Step 4: Label the Output

After verification, every claim in the output should be one of:

- **Verified** (with evidence: "confirmed by `npm info` output")
- **Unverified** (explicitly marked: "not yet confirmed")
- **Corrected** (original was wrong, replaced with verified data)

## Do / Don't Checklist

### Do

- [ ] Verify every version number mentioned in output with a tool or API call
- [ ] Verify URLs you generate with `curl -s -o /dev/null -w "%{http_code}" URL` before recommending
- [ ] Never guess URLs — if you can't see it, ask the user to provide it
- [ ] For user-provided URLs: only check HTTP status code (`-o /dev/null`), don't fetch or render content from untrusted sources (phishing/malware risk)
- [ ] Check today's date with `date` if you reference it
- [ ] Run actual API calls to confirm field names (don't guess from memory)
- [ ] Use `--help` or docs to confirm CLI flags exist
- [ ] Check if URLs return 200 before recommending them
- [ ] Mark claims as "unverified" if you cannot check them
- [ ] Date your verification ("verified on 2026-04-11")
- [ ] Re-verify if the source information is older than 6 months
- [ ] Verify PR/issue status with `gh` commands, not from memory

### Don't

- [ ] Don't trust your memory for version numbers, API shapes, or dates
- [ ] Don't assume an API field name — always verify from real output
- [ ] Don't report "I fixed it" without verifying CI passes (`gh pr checks`)
- [ ] Don't report "PR has reviews" without checking (`gh pr view`)
- [ ] Don't cite documentation without confirming the URL exists
- [ ] Don't use old StackOverflow answers as current truth — platforms change
- [ ] Don't claim "push succeeded" means "task complete"
- [ ] Don't state defaults or limits without checking the actual source code or schema

## Common Hallucination Patterns to Watch For

### Pattern 1: Outdated Model/Version References
AI models are frozen at their training cutoff. Always verify:
```bash
# Check latest version of a package
npm info @anthropic-ai/sdk version
pip show openai | grep Version
gh release list --repo owner/repo --limit 3
```

### Pattern 2: Invented API Fields
Never guess API response field names. Always run the API and read the actual response:
```bash
# Real API call to verify field names
curl -s "https://api.example.com/endpoint" | jq '.[0] | keys'
```

### Pattern 3: False Success Reporting
The most dangerous hallucination. "I did it" when the work is incomplete:

| What was said | What it actually means | How to verify |
|--------------|----------------------|---------------|
| "Pushed successfully" | Git push worked | `gh pr checks` — is CI green? |
| "Responded to review" | Committed a change | Does the new code actually fix the issue? |
| "Found 10 problems" | Listed 10 items | Read the code for each — do they exist? |
| "PR has been reviewed" | Someone looked at it | `gh pr view --json reviews` — what's the count? |

### Pattern 4: Phantom References
Referencing things that don't exist:
```bash
# Verify a file exists before referencing it
ls /path/to/claimed/file

# Verify a function exists in a codebase
grep -r "functionName" src/

# Verify an npm package exists
npm info claimed-package-name
```

### Pattern 5: Date Confusion
AI models often get dates wrong, including today's date:
```bash
# Always verify current date
date "+%Y-%m-%d"

# Check when a release was published
gh release view v1.0.0 --repo owner/repo --json publishedAt
```

### Pattern 6: URL Guessing
AI models will fabricate plausible-looking URLs when they don't know the real one:

| Fabricated URL | Why it looks right | Actual URL |
|---------------|-------------------|------------|
| `https://auth.openai.com/activate` | Follows common OAuth patterns | `https://auth.openai.com/codex/device` |
| `https://docs.clawhub.ai` | Standard docs subdomain | Does not exist (returns 404) |
| `https://api.example.com/v2/schema` | Common API convention | Endpoint may not exist |

**Prevention:**
- **Never guess URLs.** If you can't see the full output, ask the user to expand it.
- If recommending a URL, verify it with `curl -s -o /dev/null -w "%{http_code}" URL` first.
- Say "I don't have the URL — can you check the terminal output?" instead of guessing.
- URLs are not inferrable from patterns. `auth.openai.com/activate` vs `auth.openai.com/codex/device` — one character path difference, completely different endpoints.

## Verification Report Format

When fact-checking, produce a report like this:

```markdown
## Fact Check Report

| # | Claim | Status | Evidence |
|---|-------|--------|----------|
| 1 | "API returns `like_count`" | Verified | Real API run, dataset abc123 |
| 2 | "Latest version is v2.3" | Corrected → v2.5 | `npm info package version` |
| 3 | "Supports `--recursive` flag" | Unverified | Cannot test without install |
| 4 | "Default timeout is 30s" | Verified | Source code line 42 |
```

## Tips

- The more confident you feel about a claim, the more important it is to verify. Confidence ≠ correctness.
- "I'm pretty sure" is not evidence. Run the command.
- Verification has a cost (time, API calls), but false information has a higher cost (broken code, lost trust, wasted user time).
- When in doubt, say "I'm not sure — let me verify" instead of guessing.
- If you can't verify something, say so explicitly. An honest "unverified" is better than a confident hallucination.
