---
name: create-skill
description: Create a new skill through a guided conversation. Use when a user wants help authoring a skill from scratch, choosing between quick or full guidance, analyzing documentation to extract behavior patterns, generating a functional skill with proper workflow, and explaining how to make the new skill take effect.
---

# Create Skill

Guide the user through creating a new skill from scratch.

## Core Philosophy

A skill should define **behavior**, not just store documentation.

- A good skill tells the agent **when** to use it
- A good skill tells the agent **what tools** to use
- A good skill defines the **workflow** (in what order)
- A good skill specifies the **expected output**
- A good skill knows its **constraints**

Static documentation has little value - the agent can fetch that itself. The skill's value is in **encoding the behavior pattern**.

## Interaction Rules

### Input Style

- Always present choices as numbered options (1, 2, 3...).
- Never ask the user to type full words like "quick" or "full".
- Accept the number, the option text, or common abbreviations.

### Question Rhythm

- Ask ONE question at a time.
- Wait for the user's answer before asking the next question.
- Never dump multiple questions in a single message.

### Communication Style

- Never add self-explanatory filler text.
- Never explain what you are going to do before doing it.
- Keep all prompts as concise as possible.
- Use the same terse style as a real CLI tool.

## Workflow

Follow these steps in order:

1. Prompt for mode selection (1 or 2).
2. Prompt for skill purpose (the task it solves).
3. Prompt for trigger conditions (when to use).
4. Prompt for required tools.
5. Prompt for workflow steps.
6. Prompt for expected output.
7. Prompt for constraints.
8. Prompt for install location.
9. Prompt for skill name.
10. (Optional) Fetch and analyze documentation.
11. Show summary.
12. Show preview.
13. Prompt for confirmation.
14. Write files.
15. Show completion with next steps.

## Step 1: Mode Selection

Output exactly:

```
Create a new skill.

1) Quick guidance
2) Full guidance

Choice [1]:
```

- Default to 1 (Quick) if user just presses Enter.
- If user enters invalid option, re-prompt.

## Step 2: Skill Purpose

Ask:

```
What task does this skill solve?
```

Accept any natural language answer. Extract the core task.

Examples:
- "Deploy a static blog to GitHub Pages"
- "Convert images to different formats"
- "Query and analyze database schemas"

## Step 3: Trigger Conditions

After purpose, ask:

```
When should the agent use this skill?

1) User explicitly asks for it
2) When user mentions specific keywords
3) When certain conditions are met
4) Not sure / I'll define later

Choice [1]:
```

If user chooses 2 or 3, ask for the specific trigger details.

## Step 4: Required Tools

After trigger, ask:

```
What tools does this skill need?

1) Built-in tools only
2) External CLI commands
3) API calls
4) Combination of above

Choice [1]:
```

If user chooses 2 or 3, ask:
- "Which CLI commands? (comma separated)"
- "Which APIs? (describe the service)"

## Step 5: Workflow

After tools, ask:

```
What is the workflow? (describe in order)

1) I'll describe step by step
2) Generate from documentation
3) Use a common pattern

Choice [1]:
```

If user chooses 1, ask them to describe each step.

If user chooses 2, proceed to Step 10 (fetch documentation).

If user chooses 3, present common patterns:
- "init → configure → run"
- "check prerequisites → setup → execute → verify"
- "collect input → process → output"

## Step 6: Expected Output

After workflow, ask:

```
What should this skill produce?

1) Files (config, code, etc.)
2) Command output
3) API response
4) Combination

Choice [1]:
```

Ask for specific output format details.

## Step 7: Constraints

After output, ask:

```
Are there any constraints?

1) No constraints
2) OS limitations
3) Required environment variables
4) Configuration requirements
5) I'll specify

Choice [1]:
```

If user chooses 2-5, gather the constraint details.

## Step 8: Install Location

After constraints, ask:

```
Where to install?

1) Current workspace
2) Shared (all projects)

Choice [1]:
```

## Step 9: Skill Name

After install location, ask:

```
Skill name (lowercase, hyphenated):
```

- Propose a name based on the skill purpose if user is unsure.
- Validate format (lowercase, digits, hyphens only).

## Step 10: Fetch and Analyze Documentation (Optional)

If user chose to generate workflow from documentation in Step 5:

```
Where is the documentation?

1) Enter URL
2) GitHub repository
3) Local path
```

After getting the source:
- Fetch the documentation
- **Analyze and extract**:
  - Installation commands
  - CLI usage and options
  - Configuration parameters
  - Common workflows
  - Best practices
  - Limitations
- **Generate behavior** from the analysis:
  - When to trigger
  - What tools to use
  - Step-by-step workflow
  - Expected output format
  - Constraints

Do NOT just copy the documentation. Transform it into **behavioral instructions**.

## Step 11: Summary

After all inputs are collected, show:

```
Skill: <name>
Task: <purpose>
Triggers: <trigger conditions>
Tools: <tool list>
Workflow:
  1. <step 1>
  2. <step 2>
  ...
Output: <expected output>
Constraints: <constraints>
Location: <workspace|shared>

Continue? [y/n]:
```

## Step 12: Preview

Generate the SKILL.md and show key sections:
- Trigger conditions
- Tools required
- Workflow steps
- Output format

## Step 13: Confirmation

Ask:

```
Write files? [y/n]:
```

## Step 14: Write Files

If confirmed:
- Create the skill directory.
- Write SKILL.md with full behavioral instructions.
- Write README.md.
- If directory exists, stop and ask.

## Step 15: Completion

Show:

```
Created: <path>

To activate:
- Restart the agent, or
- Run: refresh skills

To test:
- "<test prompt>"

Done.
```

## Full Guidance Mode

Full mode adds more detail at each step:

After purpose:
- "Target users? (optional)"
- "What problem does it solve? (detailed)"

After trigger:
- "Exact trigger phrases?"
- "Any negative triggers (when NOT to use)?"

After tools:
- "Specific command versions?"
- "Any setup required?"

After workflow:
- "Error handling?"
- "Rollback steps?"

After output:
- "Output format examples?"
- "Where to save files?"

After constraints:
- "Known issues?"
- "Alternative approaches?"

## Writing Rules

### SKILL.md Structure

A good SKILL.md should have:

```markdown
---
name: <skill-name>
description: <brief description>
---

# <Skill Name>

## When To Use

- When user says "..."
- When user wants to "..."

## Tools Required

- tool1: description
- tool2: description

## Workflow

1. Step one - what to do
2. Step two - what to do
3. ...

## Output

- What files/config are produced
- Expected format

## Constraints

- OS limitations
- Prerequisites
- What NOT to do

## Examples

Example usage scenarios
```

### Key Principles

- Write **behavior**, not documentation
- Be specific about tool usage
- Define clear workflow steps
- Specify exact output format
- Include constraints and boundaries

## Generated Skill Quality

The generated skill should be **self-contained**:
- Agent should know when to use it without asking
- Agent should know what tools to call
- Agent should know the exact workflow
- Agent should know the expected output

If the agent still needs to search the web or figure out the workflow, the skill is not complete.

## Language

- Use English by default.
- If user clearly uses another language, switch to that language.
