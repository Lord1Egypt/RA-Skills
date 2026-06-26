# Autoagent Setup Prompt

Every invocation of `/autoagent` starts fresh with these setup questions.

## Step 1: Sandbox Location

Ask the user:

> Where should I create the sandbox folder? Default: `../../autoagent-sandbox/` (resolves to `/clawd/autoagent-sandbox/`)

You can respond with:
- **Empty/default**: Press enter to use `../../autoagent-sandbox/`
- **Just a name**: "news" creates `../../autoagent-news/` → `/clawd/autoagent-news/`
- **Relative path**: "agentDev/optimize" creates `../../agentDev/optimize/` → `/clawd/agentDev/optimize/`
- **Absolute path**: `/some/other/path/optimize/` → exact path

Wait for their response (or empty for default).

## Step 2: Success Criteria Discussion

Ask the user:

> Let's define how we'll measure success. What does a "good" result look like for this task?

Follow up as needed:
- What specific outputs are expected?
- What format should they be in?
- What's the minimum viable quality?
- Any edge cases to consider?

## Step 3: Propose Draft Scoring

Once you've discussed enough to understand the task, propose a draft scoring.md:

```markdown
## Scoring Criteria

**Total:** 100 points

| Component | Points | Description |
|-----------|--------|-------------|
| [Name]    | [X]    | [What it measures] |
| ...       | ...    | ... |

**Notes:**
- [Any additional scoring rules]
```

Wait for user approval or request modifications.

## Step 4: External Scripts/Tools

Ask the user:

> Does the guidance rely on any scripts, tools, or external software?
> - If yes: Note each script/tool path and what functionality it provides
> - The autoagent should analyze these to recommend improvements

## Step 5: Cron Schedule

Ask the user:

> Run optimization every 5 minutes (default), or different interval?

## Step 6: Create Sandbox

After scoring is approved:
1. Create folder at user-specified path
2. Create files:
   - guidance-under-test.md
   - current-guidance.md
   - fixtures/test-cases.json
   - scoring.md (with approved criteria)
   - scores.md
   - scripts/ (optional)
3. Set up cron
4. Return confirmation with sandbox path
