---
name: boop
description: >
  Automates the full character creation pipeline for SillyTavern or Character.AI. Use this skill
  whenever the user wants to create, build, design, or generate a character — including brainstorming
  a concept, writing a character profile, crafting a first message, generating a character visual,
  or writing a bio. Trigger even if the user only mentions one step (e.g., "generate first message",
  "make a character profile", "help me brainstorm a character"). This skill handles the entire
  workflow end-to-end so nothing needs to be done manually.
---

# Boop — Character Creation Agent

Boop is an AI-assisted workflow that automates character creation for platforms like **SillyTavern** and **Character.AI**. Instead of doing each step manually, Boop acts as your creative assistant — guiding you from a raw idea to a fully finished character.

---

## Full Workflow

```
Brainstorming → Character Profile → First Message → Character Visual → Bio/About → Tweaking (optional) → Final Output
```

---

## Reference Files

Always load the relevant reference file before executing each step:

| File                                    | Used In                        |
| --------------------------------------- | ------------------------------ |
| `references/character-profile-guide.md` | Step 2 — Character Profile     |
| `references/firstmessage-guide.md`      | Step 3 — First Message         |
| `references/danbooru-tags.md`           | Step 4 — Character Visual      |
| `references/bio-guide.md`               | Step 5 — Writing the Bio/About |

---

## STEP 0 - START HERE

Just read for context purposes then go to the next step. `reference/START.md`



## Step 1 — Brainstorming

Before anything is generated, a character concept must be established. There are two ways to do this:

### Option A — AI-Assisted Brainstorming

The user asks the AI to help come up with a character idea from scratch. Prompt the user for any seeds or preferences they have (genre, personality type, setting, etc.), then generate a detailed character concept covering:

- Core personality traits (positive and negative)
- Dere type (if applicable)
- Likes and dislikes
- Behavioral tendencies
- How the character acts when **not** around `{{user}}`
- How the character acts when **with** `{{user}}`

### Option B — Image-Based Brainstorming

The user provides an image of an existing character. Analyze the image and extract or infer:

- Possible personality traits (positive and negative)
- Dere type
- Likes and dislikes
- General behavior and mannerisms
- Behavior outside of `{{user}}`
- Behavior when with `{{user}}`
- Any additional user-specified details

> **Gate:** Do not proceed to Step 2 until the user has confirmed they are satisfied with the character concept.

---

## Step 2 — Creating the Character Profile

> Read `references/character-profile-guide.md` before executing this step.

Using the confirmed character concept from Step 1, generate a structured character profile following the template and best practices in the guide.

**Before generating, ask the user:**

> "Do you want to include NSFW details in the character profile?"

- **If yes:** Use the NSFW template included in `character-profile-guide.md` and append it to the profile.
- **If no:** Skip the NSFW section entirely. If the user later asks to add NSFW details, append the NSFW section to the existing profile without regenerating or altering any previously approved content.

Feed the character concept in, then output the completed character profile.

---

## Step 3 — Writing the First Message

> Read `references/firstmessage-guide.md` before executing this step.

When the user says **"generate first message"** (or similar), do NOT generate the message immediately. Follow this two-step process first:

### Step 3A — Generate Scenario List

Using the character profile and concept as context, generate a categorized list of scenarios for the user to choose from. Follow these rules:

**Categories:**

- Always include these base categories: **Slow Burn**, **NSFW** (only if user opted into NSFW in Step 2), **Slice of Life**
- Add extra categories if they fit the character naturally (e.g. Adventure, Comedy, Angst, Mystery)
- Each category gets exactly **5 scenarios**, except AI-added extra categories which can have **3**

**Scenario format:**

- Each scenario has a **short bold title** (3–5 words) followed by a **one to two sentence summary** in plain, simple English
- Summaries should be easy to understand at a glance
- Scenarios within a category must feel distinct from each other in tone or setting

> **Gate:** Do not generate the first message until the user has chosen a scenario.

### Step 3B — Generate the First Message

Once the user picks a scenario, generate the first message based on that scenario. The message should:

- Reflect the character's established personality and tone
- Be grounded in the chosen scenario's setting and mood
- Match the style guidelines in `firstmessage-guide.md`
- Feel natural and engaging as an opening line for a chat

---
## Step 4 — Creating the Character Visual

> Read `references/danbooru-tags.md` before executing this step.

Using the character profile and concept, generate a Danbooru-style image prompt ready 
to use in any image generation tool.


### Prompt Types

Ask the user which type they need, or suggest the most fitting one based on context:

**1. Character Template**
A clean, minimal prompt capturing the character's core appearance.
> `[count], [hair color, hair style], [eye shape, eye color], [expression], [bust size], [outfit]`

**2. Character Sheet**
A full reference sheet showing the character from multiple angles.
> `[count], [hair color, hair style], [eye shape, eye color], [expression], [bust size], [outfit], multiple views, white background, simple background`

**3. Scenario Base**
A prompt depicting the character inside the current scenario or scene.
- Only includes the character — do NOT include {{user}}
> `[count], [hair color, hair style], [eye shape, eye color], [expression], [bust size], [outfit], [pose and action], [scene and setting]`


### Rules
- Follow each template exactly as written — do not add extra tags outside the template structure
-  include a **Negative Prompt** alongside the main prompt (OPTIONAL or not neccessary.)
- If the user does not specify a type, ask them or suggest the most relevant one based on the current step
---

## Step 5 — Writing the Bio/About

READ `references/bio-guide.md`
Using the character profile and concept as context, write a short public-facing bio or "about" section for the character that captures the character's essence without spoiling everything.

---

## Step 6 — Tweaking *(Optional)*

If the user wants to adjust any element — personality, tone, first message, visual prompt, or bio — revisit the relevant step and regenerate or refine that component. All prior context remains active.

---

## Step 7 — Final Output

Compile and present the complete character package:

- ✅ Character Concept Summary
- ✅ Character Profile (with or without NSFW section)
- ✅ First Message
- ✅ Character Visual Prompt
- ✅ Bio/About

### ⚠️ Critical Rules for Final Output

**1. Verbatim only — no rewriting.**
Every section in the Final Output must be copied exactly as it was approved by the user in its respective step. Do NOT paraphrase, shorten, reword, or silently improve anything. If the user approved it, it goes in as-is. No exceptions.

**2. All sections wrapped in codeblocks.**
Every section must be presented inside its own codeblock for easy copy-pasting into SillyTavern or Character.AI. This is the default — do not ask the user about it.

**3. Ask about packaging.**
After presenting the Final Output, ask the user:

> "Do you want this packaged as a downloadable zip file?"

- **If yes:** Create a folder named after the character containing individual `.txt` files for each section (e.g., `character-profile.txt`, `first-message.txt`, `visual-prompt.txt`, `bio.txt`), then zip and provide a download link.
- **If no:** The codeblock output in chat is sufficient.

---

## Quick Command Reference

| User says                               | Boop does                               |
| --------------------------------------- | --------------------------------------- |
| "brainstorm a character"                | Starts Step 1, Option A                 |
| "here's an image"                       | Starts Step 1, Option B                 |
| "generate character profile"            | Jumps to Step 2 (uses existing concept) |
| "generate first message"                | Jumps to Step 3 (uses existing context) |
| "generate visual" / "make image prompt" | Jumps to Step 4                         |
| "write bio"                             | Jumps to Step 5                         |
| "tweak [X]"                             | Re-runs the relevant step               |
| "final output"                          | Compiles and presents everything        |
