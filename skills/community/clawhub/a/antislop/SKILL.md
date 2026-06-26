---
name: Anti-Slop
description: |
  This skill should be used when the user asks to
  "check for slop", "anti slop review", "quality check",
  "is this AI garbage", "review for originality",
  "check information density", "是不是 slop",
  "品質檢查", "確保原創",
  or before publishing, submitting, or sharing any AI-generated content.
version: 0.1.0
---

# Anti-Slop: No AI Garbage, Only Original Work

Detect and eliminate AI-generated low-quality patterns. Ensure every piece of output is original, has genuine insight, and maintains high information density. Based on patterns identified from real AI agent failures.

## What is Slop?

Slop is AI-generated content that looks productive but adds no real value:

- Generic statements anyone could write without domain knowledge
- Repetitive structure (everything becomes a bullet list or table)
- Filler phrases that add words but not meaning
- Hallucinated "facts" reported with false confidence
- Copy-paste templates with swapped keywords
- Surface-level "analysis" that states the obvious
- Excessive emoji, bold, and formatting as a substitute for substance

## The Anti-Slop Review Process

### Step 1: The Information Density Test

Read every sentence. For each one, ask: **"Does this sentence contain information the reader didn't already have?"**

- If YES → Keep it
- If NO → Delete it or replace it with something specific

**Examples of zero-density sentences (delete these):**

| Slop | Why it's slop |
|------|--------------|
| "This is an important consideration." | Says nothing specific. Important how? To whom? |
| "There are several factors to consider." | List the factors or don't mention them. |
| "Let me help you with that." | Just help. Don't announce it. |
| "This is a comprehensive solution." | Let the reader decide if it's comprehensive. |
| "It's worth noting that..." | Just note it. Drop the meta-commentary. |
| "In today's rapidly evolving landscape..." | Corporate filler. What specific change matters? |
| "I'd be happy to assist with this task." | Start working. Don't perform enthusiasm. |

### Step 2: The Originality Test

For every claim, recommendation, or analysis, ask: **"Is there genuine insight here, or could any AI produce this from a generic prompt?"**

**Signs of original work:**
- Specific file paths, line numbers, or error messages from actual investigation
- "I expected X but found Y" — evidence of real exploration
- Trade-off analysis with concrete reasons, not generic pros/cons
- References to specific versions, dates, or configuration details
- Conclusions that could be wrong (original thinking involves risk)

**Signs of AI slop:**
- Generic advice that applies to everything ("use best practices", "follow the principle of least surprise")
- Pros/cons lists where every item is one sentence of vague platitude
- "Based on my analysis" without showing the actual analysis
- Recommendations without evidence of investigating alternatives
- Perfectly balanced "on one hand... on the other hand" without taking a position

### Step 3: The False Success Audit

Scan for any claim of completion or success. For each one, verify it's real:

| Claim pattern | Verification required |
|--------------|---------------------|
| "Fixed the bug" | Test passes? CI green? Show the passing output. |
| "Updated the file" | Read the file back. Is the change actually there? |
| "Submitted the PR" | `gh pr view` — does it exist? What's the status? |
| "Responded to review" | Is the response correct? Does it actually address the feedback? |
| "Found 5 issues" | List them with file:line evidence. Can you prove each one exists? |
| "Completed the task" | Walk through every deliverable. Is each one actually done? |
| "All tests pass" | Show the test output. Which tests ran? |

### Step 4: The Structure Audit

AI defaults to over-structured output. Check for unnecessary formatting:

- **Tables**: Is a table needed, or would a sentence be clearer?
- **Bullet lists**: Is a list needed, or is this just fragmenting a paragraph?
- **Headers**: Are there so many headers that the content is chopped up?
- **Bold/emphasis**: Is everything bold? Then nothing is bold.
- **Emoji**: Are emoji adding meaning or just decoration?
- **Code blocks**: Is code formatting used for non-code content?

**Rule of thumb:** Use the simplest format that communicates the information. A well-written paragraph is often better than a bullet list.

### Step 5: The Plagiarism / Template Check

Verify the output is not:
- A lightly reworded version of documentation or Stack Overflow
- A template with variables swapped out
- A generic "how to do X" that could be found in any tutorial
- Suspiciously similar to common AI training data patterns

**If writing about a topic, add value beyond what exists:**
- What's YOUR specific experience or context?
- What's the non-obvious insight?
- What would someone miss if they only read the docs?

## Do / Don't Checklist

### Do

- [ ] Delete sentences with zero information density
- [ ] Include specific evidence (file:line, error messages, tool output)
- [ ] Take a position — don't present perfectly balanced non-opinions
- [ ] Verify every success claim with a tool or test
- [ ] Use the simplest format that works (paragraph > bullets > table)
- [ ] Add unique insight that can't be found in generic docs
- [ ] Show your work — how you arrived at a conclusion matters
- [ ] Admit uncertainty ("I'm not sure about X") instead of filling with fluff

### Don't

- [ ] Don't use filler phrases ("It's worth noting", "As we can see", "In conclusion")
- [ ] Don't start responses with "Certainly!", "Great question!", "I'd be happy to"
- [ ] Don't use emoji unless the user specifically requests it
- [ ] Don't create tables/lists when a sentence would suffice
- [ ] Don't report success without verification
- [ ] Don't write generic advice ("follow best practices") — be specific
- [ ] Don't pad responses with unnecessary context the user already knows
- [ ] Don't restate the user's question back to them
- [ ] Don't add disclaimers about being an AI or having limitations
- [ ] Don't generate template-style content with swapped keywords

## Real-World Slop Patterns (From Documented Incidents)

### Pattern 1: Listing Problems Without Reading Code
An agent listed 10 "optimization targets" in a codebase. On verification, 7 didn't exist — the agent had pattern-matched on file names and generated plausible-sounding issues without reading the actual code.

**Prevention:** Every claimed problem must have a file:line reference. If you can't point to the exact line, you haven't verified the problem exists.

### Pattern 2: Reporting From Memory Instead of Tools
An agent reported "PR #1198 has reviews" — it actually had 0 reviews. The agent generated this from its understanding of what should be true, not from running `gh pr view`.

**Prevention:** Never report status from memory. Always use `gh pr view`, `gh pr checks`, or equivalent tools.

### Pattern 3: Using Outdated Information as Current Truth
An agent reported that GitHub Actions `schedule` events don't provide `github.event.repository.name`. This was true until September 2022, when GitHub fixed it. The agent used stale training data.

**Prevention:** For platform behaviors, check official changelogs and current documentation. Date your sources.

### Pattern 4: Partial Code Reading
An agent reported "file is missing `set -e`" — but `set -e` was on line 7. The agent only read the first few lines and the end of the file.

**Prevention:** When auditing a file, read the entire file. Don't skim and assume.

### Pattern 5: Submitting to Wrong Audience
Agents submitted PRs to repositories that explicitly don't accept external contributions, and submitted new plugins to a project where community plugins had never been merged.

**Prevention:** Before submitting anything, verify the target accepts what you're offering. Check CONTRIBUTING.md, merged PR history, and maintainer responses to similar submissions.

## Severity Levels

When reviewing output, classify issues:

| Level | Meaning | Action |
|-------|---------|--------|
| **Critical** | False claim, hallucinated fact, phantom reference | Must fix before output |
| **High** | Unverified success claim, outdated information | Verify or remove |
| **Medium** | Low information density, filler text | Rewrite or remove |
| **Low** | Unnecessary formatting, minor style issues | Fix if time permits |

## Tips

- The goal is not to write less — it's to write denser. Every sentence earns its place.
- Original insight often comes from saying what's unexpected or counterintuitive, not from restating consensus.
- If you're not sure something is true, saying "I'm not sure" IS the high-quality response. Confident hallucination is the worst kind of slop.
- Run this checklist on your own output before presenting it. Self-review catches most slop.
- The best antidote to slop is genuine investigation. Read the code. Run the API. Check the docs. Real work produces real output.
