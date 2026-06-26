---
name: skill-audit
description: >-
  Audits Claude skills from GitHub repositories for effectiveness, token usage,
  safety, and best-practice compliance, then automatically generates bilingual
  social media posts about the findings. Use when the user wants to audit a skill,
  review a skill from GitHub, analyze a SKILL.md, evaluate skill quality, or
  check a skill for safety and permission issues.
---

# Skill Audit Workflow

Audit a Claude skill from a GitHub repository. Evaluate effectiveness, token usage, time complexity, permissions, safety, and best-practice compliance. Produce a structured audit report.

## Step 1: Clone & Extract

Run the clone script with the user-provided GitHub URL:

```
bash scripts/clone_and_extract.sh <repo-url>
```

The script outputs JSON listing all SKILL.md files found. If multiple skills exist in the repo, present the list to the user and ask which one(s) to audit.

If the script exits with a non-zero code:
- Exit 1: Ask the user to provide a valid GitHub URL
- Exit 2: Check if the repo exists and is public
- Exit 3: The repo has no SKILL.md files — inform the user

## Step 2: Create Output Directory

Create the audit output directory:

```
audits/<skill-name>-<YYYYMMDD-HHMMSS>/
```

Write `metadata.json` with:
```json
{
  "repo_url": "<url>",
  "timestamp": "<ISO 8601>",
  "auditor": "Fenz.AI",
  "skill_name": "<name>",
  "skill_path": "<path within repo>"
}
```

## Step 3: Save Source Files

Copy all files from the skill directory (the directory containing SKILL.md and its subdirectories) into `source/` within the output directory. Then clean up the temp clone directory.

## Step 4: Analyze

Read `references/audit-criteria.md` for detailed rubrics. Evaluate each category:

### 4a. Effectiveness
Read the skill's SKILL.md and evaluate:
- Description quality (WHAT + WHEN)
- Trigger clarity and coverage
- Workflow definition clarity
- Examples for complex steps
- Error handling guidance

Rate: **Strong** / **Adequate** / **Weak**

### 4b. Token Usage
Run the analysis script:
```
python3 scripts/analyze_tokens.py <source-dir>
```
Use the JSON output to assess:
- SKILL.md line count
- Progressive disclosure usage
- Total token footprint
- Category breakdown

Rate: **Low** / **Medium** / **High**

### 4c. Time Spending
Evaluate the workflow for:
- Complexity and branching
- Number of external tool calls
- User interaction requirements
- Scope clarity

Rate: **Quick** / **Moderate** / **Extended**

### 4d. Permissions
Check the skill for:
- `allowed-tools` in frontmatter — what tools are requested?
- Whether each tool is justified by the workflow
- Destructive tool usage (Bash without restrictions, Write to system paths)
- Network access scope
- File system access scope

Flag any red flags. Rate: **Minimal** / **Moderate** / **Broad**

### 4e. Safety
Evaluate:
- Does behavior match the description?
- Network access patterns
- File scope boundaries
- Sensitive data handling
- Input validation (especially for shell commands)

Rate: **Low Risk** / **Medium Risk** / **High Risk**

### 4f. Recommendations
Read `references/skill-best-practices.md` and check the skill against each item. Group findings by priority:
- **High**: Safety, correctness, major effectiveness issues
- **Medium**: Efficiency, maintainability issues
- **Low**: Style and convention suggestions

## Step 5: Generate Report

Read `assets/audit-report-template.md` and fill in all template fields with the analysis results. Save as `audit-report.md` in the output directory.

Include:
- All six category ratings with detailed explanations
- Specific evidence from the skill files for each finding
- Concrete, actionable recommendations
- Positive observations (what the skill does well)
- File appendix with token estimates

## Step 6: Log Everything

Maintain `process-log.md` in the output directory. Append each step as it completes:

```
## [YYYY-MM-DD HH:MM:SS] Step N: <step name>
- Status: success/failed/skipped
- Details: <what happened>
- Errors: <if any>
```

## Step 7: Generate Social Media Posts

Automatically generate posts from the audit report.

1. Run: `python3 ../post-generator/scripts/extract_findings.py <audit-dir>/audit-report.md`
2. Read `../post-generator/references/writing-guide-en.md` and `../post-generator/assets/post-template-twitter-en.md`
3. Generate 2-3 English post variations following the guide
4. Read `../post-generator/references/writing-guide-zh.md` and `../post-generator/assets/post-template-twitter-zh.md`
5. Generate 2-3 Chinese post variations (NOT translations — independently crafted)
6. Save `posts-en.md` and `posts-zh.md` in the audit output directory
7. Log post generation step to `process-log.md`

Quality rules:
- Posts must sound human-written, not AI-generated
- No banned phrases (see writing guides for anti-pattern lists)
- Fenz.AI mentioned once, naturally, first post only
- Max 2 hashtags, no emoji spam
- English: professional/conversational; Chinese: direct/opinionated with full-width punctuation
