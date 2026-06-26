---
name: company-skill-creator
description: Create company-internal skills interactively. Use when users want to create a skill for internal company workflows, APIs, business processes, or tools. Guides the user through providing requirements, API docs, interface specs, reference materials, and scripts — auto-generating anything they don't have on hand. Make sure to use this skill whenever the user mentions creating a company skill, internal skill, work skill, or wants to automate a company workflow.
---

# Company Skill Creator

Create company-internal skills through an interactive interview process. This skill helps users turn their domain knowledge into reusable skills — even when they don't have formal documentation ready.

## Core philosophy

Company skills are different from general-purpose skills. They typically involve:

- **Internal APIs** that Claude can't know about from training data
- **Business processes** specific to the company
- **Domain schemas** (database tables, data models, config formats)
- **Proprietary tools** or internal services
- **Team conventions** and unwritten rules

The key insight: users often have this knowledge in their heads but haven't formalized it. The skill creator's job is to extract that knowledge interactively, fill in the gaps, and produce a well-structured skill.

---

## The creation workflow

At a high level, the process goes like this:

1. **Interview** — Understand what the skill needs to do, gather materials
2. **Scaffold** — Create the skill directory structure
3. **Fill gaps** — Auto-generate missing scripts, references, or templates
4. **Write the skill** — Compose SKILL.md based on everything gathered
5. **Validate & package** — Make sure it's correct, package the .skill file

Your job is to guide the user through each phase, being flexible about the order and knowing when to generate vs. when to ask.

---

## Phase 1: Interactive interview

### Step 1.1: Understand the core task

Start by asking the user a few essential questions. Don't bombard them all at once — ask, listen, then follow up naturally.

**Must-ask questions:**

1. **What should this skill do?** — Get a concrete example. "I want Claude to query our user database" is better than "data access skill."

2. **When should it trigger?** — What would a user say to invoke it? Collect 3-5 example phrases. Include both formal ("query the user database for...") and casual ("can you look up...") phrasings.

3. **What's the output?** — Code? A report? A file? An API call result? A Slack message?

4. **Who will use this?** — Is this for engineers, PMs, data analysts? This affects the tone and level of detail.

### Step 1.2: Ask the user what materials they can provide

This is the critical step that makes company skills different. Tell the user something like:

> "To build a solid skill, I'll need a few things. You don't need all of these — just share whatever you have, and I'll generate the rest. Here's what helps most:"

Then ask about each category. **Do not ask all at once** — let the user respond to each before moving on.

**Required materials (must have at least a verbal description):**

| Category | What to ask for | If they don't have it |
|---|---|---|
| **Requirements** | User stories, spec docs, workflow diagrams, or just describe what the skill should do step by step | Extract from conversation and write up as structured requirements |
| **API / Interface** | Swagger/OpenAPI specs, API docs URLs, curl examples, SDK documentation, or just endpoint names and parameters | Generate a stub reference doc based on their verbal description; mark guessed parts with `⚠️ 待确认` (to be confirmed) |
| **Data / Schema** | Database schemas, table descriptions, field lists, sample queries, example data files | Generate a schema reference from their description; note any guessed fields |
| **Scripts** | Existing scripts, utilities, helper tools the team already uses | Write the scripts from scratch based on requirements |
| **References** | Links to internal docs, coding standards, business logic rules, known edge cases | Generate reference docs from the interview; flag sections that need SME review |
| **Templates** | Report templates, code scaffolds, configuration files, message formats | Create templates from examples the user describes |

**How to phrase this to the user:**

Frame it as a collaborative process. The user is the domain expert; Claude is the skill architect. The user provides the raw knowledge in whatever form they have it; Claude organizes and fills gaps.

### Step 1.3: Collect materials

For each category the user says they have materials for:

1. Ask them to share the content (paste text, provide file paths, share URLs)
2. Read any files they point to
3. If they give a URL to internal docs, try fetching it; if authentication fails, ask them to paste the relevant content
4. Take notes on what's provided

For each category they **don't** have materials for:

1. Ask clarifying questions to extract enough detail
2. Note what they said — you'll auto-generate this later
3. Confirm: "I'll generate a draft based on what you've described. You can review and correct it later."

### Step 1.4: Confirm scope

Before writing anything, summarize what you've gathered:

> "Here's what I understand so far:
> - **Skill name**: [proposed kebab-case name]
> - **Purpose**: [one-line summary]
> - **Inputs**: [what the user provides]
> - **Outputs**: [what the skill produces]
> - **Materials provided**: [list what the user gave you]
> - **To be generated**: [list what you'll create from scratch]
>
> Does this look right? Anything to add or change?"

---

## Phase 2: Scaffold the skill

### Step 2.1: Create the directory structure

Use the `scripts/init_skill.py` script to create the directory structure:

```bash
python <path-to-company-skill-creator>/scripts/init_skill.py <skill-name> --path <output-directory>
```

This creates:

```
skill-name/
├── SKILL.md              (with frontmatter template)
├── scripts/
│   └── __init__.py
├── references/
└── assets/
```

### Step 2.2: Generate missing components

Based on what the user couldn't provide, generate the necessary files. Work in this priority order:

**1. Scripts first** — If the skill needs to interact with an API, format data, or automate a repetitive task, write the scripts now. Put them in `scripts/`. These should be:
- Well-tested with happy path and basic error handling
- Documented with brief usage comments
- Written in a language the user's team uses (ask if unsure)

**2. References next** — Create reference documents in `references/`:
- API reference docs (endpoints, parameters, auth, examples)
- Schema/docs references (tables, fields, relationships)
- Business logic rules
- Each file should have a table of contents if over 100 lines
- Mark unverified information with `⚠️ 待确认` so the user can review

**3. Assets last** — Templates, config files, boilerplate. Put in `assets/`.

### Step 2.3: Flag what needs review

For every generated file, decide the confidence level:

| Confidence | Marking | Meaning |
|---|---|---|
| High | No mark | Based on concrete user input, likely correct |
| Medium | `⚠️ 待确认` on specific lines | Reasonable guess but user should verify |
| Low | `⚠️ 待确认` in file header | Mostly inferred, user must review before use |

Tell the user clearly which files need their review and which are ready to go.

---

## Phase 3: Write SKILL.md

Now compose the SKILL.md. This is the heart of the skill — follow the same patterns as skill-creator but tuned for company skills.

### Frontmatter

```yaml
---
name: <kebab-case-name>
description: <what it does AND when to trigger. Include 3-5 concrete trigger examples. Make it slightly pushy — err on the side of triggering. Max 1024 chars.>
---
```

**Description writing rules:**
- Be specific about when to trigger — include phrases users would actually say
- For company skills, include context clues: team names, system names, jargon
- Keep it under 1024 characters
- No angle brackets
- Make it "pushy" — if in doubt, the skill should trigger

### Body structure

```markdown
# <Skill Title>

## Overview
<1-2 sentences about what this skill does and why it exists.>

## Quick start
<The most common use case, with a concrete example.>

## Workflow
<Step-by-step instructions. Use imperative mood. Explain WHY, not just WHAT.>

## API / Tool reference
<Pointer to references/ files. Don't duplicate — just link.>

## Output format
<What the skill should produce. Use templates where helpful.>

## Edge cases & known issues
<Things the user mentioned during the interview.>
```

### Key rules for company skills

1. **Explain the "why"** — Company processes often have historical reasons. The skill should capture these so Claude understands context, not just rules.

2. **Progressive disclosure is critical** — Company skills often have large reference files (API docs, schemas). Keep SKILL.md lean; put details in `references/` with clear pointers.

3. **Don't duplicate information** — If a schema is in `references/schema.md`, don't summarize it in SKILL.md. Just link to it.

4. **Use the company's language** — If the team says "workspace" not "project", use "workspace" throughout.

5. **Scripts over instructions** — If a task requires deterministic behavior (API calls, data transforms), provide a script rather than text instructions. Scripts don't consume context window when executed.

6. **Mark uncertainty** — If you're unsure about a business rule or API behavior, note it with `⚠️ 待确认`.

---

## Phase 4: Review with the user

### Step 4.1: Present the complete skill

Walk the user through what was created:

1. **SKILL.md** — Read through the key sections together
2. **Scripts** — Explain what each script does and when it runs
3. **References** — Point out files that need SME review
4. **Assets** — Show any templates or scaffolds

### Step 4.2: Collect feedback

Ask targeted questions:

- "Does the trigger description match how you'd actually ask for this?"
- "Looking at the API reference, are there any endpoints or parameters I got wrong?"
- "Try describing a task to me — let's see if I'd invoke the right skill."

### Step 4.3: Iterate

Apply feedback immediately. If the user has substantial changes, make them and present again. If the changes are minor, note them and move on.

---

## Phase 5: Validate & package

### Step 5.1: Validate

Run the validation script:

```bash
python <path-to-company-skill-creator>/scripts/quick_validate.py <path-to-skill>
```

Fix any issues it reports.

### Step 5.2: Package

```bash
python <path-to-company-skill-creator>/scripts/package_skill.py <path-to-skill>
```

This produces a `.skill` file. Tell the user where it is and how to install it.

### Step 5.3: Final checklist

Present a summary to the user:

```
✅ Skill created: <skill-name>
📁 Location: <path>
📦 Package: <skill-name>.skill
⚠️  Needs review: <list of files with unconfirmed content>
📋 Next steps:
   1. Review files marked with ⚠️ 待确认
   2. Install the .skill file
   3. Test with a real task
   4. Come back to iterate if needed
```

---

## Quick mode

If the user is in a hurry or the skill is simple, you can compress the workflow:

1. Ask: "What should this skill do? Got any docs or scripts I should know about?"
2. Generate everything from their answer
3. Present for quick review
4. Package

Skip the formal interview steps. Trust your judgment on when to use quick mode vs. full interview.

---

## Communication style

Company skill creators work with people who may not be technical writers. Adjust your communication:

- **Engineers**: Use technical terms freely. Focus on correctness and efficiency.
- **PMs / Analysts**: Explain what you're doing in plain language. "I'm going to create a reference file that documents your API" rather than "I'll generate an OpenAPI stub."
- **Mixed audiences**: Default to the less technical audience's level.

Always be encouraging. Users often feel their materials aren't "good enough" — reassure them that verbal descriptions and rough notes are perfectly fine starting points.

---

## Special cases

### The user has a complete spec

If the user has a well-written specification document, API docs, and sample code:

1. Read everything they provide
2. Scaffold the skill
3. Generate SKILL.md from the spec (don't make them re-explain)
4. Present for confirmation — "Here's what I built based on your docs. Did I get it right?"
5. Minimal interview needed

### The user has nothing but an idea

If the user says "I want a skill for X" but has no materials:

1. Ask for a concrete example of what they'd want to do
2. Walk through what the skill would need step by step
3. Generate everything: scripts, references, templates
4. Be explicit about uncertainty — "I wrote this API client based on what you described. You'll need to fill in the actual endpoint URLs and auth method."
5. Iterate more — expect more rounds of feedback

### The user wants to convert existing documentation

If the user has internal wiki pages, READMEs, or runbooks they want turned into a skill:

1. Read all the docs
2. Identify the procedural knowledge (the "how to") vs. reference material (the "what is")
3. Structure the procedural knowledge as SKILL.md workflow instructions
4. Structure the reference material as `references/` files
5. Remove anything Claude already knows (don't explain what REST is, etc.)

---

## Reference files

- `agents/interviewer.md` — Detailed interview prompts and question templates for different skill types (API skills, data skills, workflow skills, template skills)
- `references/company-context.md` — Template for capturing company-specific context (tech stack, team structure, common workflows)

---

## Bundled scripts

- `scripts/init_skill.py` — Scaffold a new skill directory with the standard structure
- `scripts/quick_validate.py` — Validate SKILL.md frontmatter format
- `scripts/package_skill.py` — Package a skill folder into a .skill file

---

That's it. The most important thing: **extract what the user knows, generate what they don't have, and always flag what needs review.** A company skill with a few `⚠️ 待确认` marks is far more useful than no skill at all.
