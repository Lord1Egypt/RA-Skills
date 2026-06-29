# Academic Writing Polisher

A context-first academic writing Skill for researchers who need clearer, more coherent, journal-ready text without losing author intent.

Inspired by Dritjon Gruda's Nature Career Column, "Three ways ChatGPT helps me in my academic writing," this Skill turns responsible academic revision into an installable Agent workflow: ask for context first, revise second, and always flag meaning risks.

## What It Helps With

- Polish research paragraphs for clarity, coherence, concision, and academic tone.
- Improve abstracts, introductions, discussions, limitations, and conclusions.
- Refine reviewer responses without sounding defensive or vague.
- Organize peer-review comments and editorial feedback.
- Preserve the author's intended meaning while avoiding invented claims or citations.

## Why This Skill Exists

Generic AI polishing often changes too much: it can add unsupported claims, overstate findings, flatten disciplinary nuance, or silently change what the author meant.

This Skill gives the Agent a stricter academic writing workflow:

1. Collect the research context.
2. Revise only for the requested purpose.
3. Preserve citations, claims, and technical terms.
4. Explain what changed.
5. Flag ambiguity, overstatement, or meaning risks.

## Install

Install from ClawHub:

```bash
clawhub install academic-writing-polisher
```

If you use OpenClaw:

```bash
openclaw skills install academic-writing-polisher
```

ClawHub page: [academic-writing-polisher](https://clawhub.ai/skills/academic-writing-polisher)

If installing from this repository manually, copy the Skill folder into your local skills directory:

```bash
cp -R academic-writing-polisher ~/.codex/skills/
```

## Example Prompts

```text
Polish this paragraph for clarity and journal-ready academic tone. Preserve all claims and citations.
```

```text
I am writing a discussion section for a biomedical paper. I want this paragraph to sound more concise and coherent without overstating the findings.
```

```text
Revise this response to Reviewer 2. Keep it respectful, specific, and clear about what we changed.
```

## Output Shape

The Skill normally returns:

- Polished Version
- What Changed
- Meaning Check
- Risk Flags

This makes the revision auditable instead of a black-box rewrite.

## Search Keywords

academic writing, research writing, paper polishing, Nature-inspired, ChatGPT academic writing, reviewer response, peer review, editorial feedback, journal-ready tone, clarity, coherence, concision, author intent

## Source Inspiration

Gruda, D. (2024). "Three ways ChatGPT helps me in my academic writing." Nature. DOI: [10.1038/d41586-024-01042-3](https://doi.org/10.1038/d41586-024-01042-3)

This Skill is not affiliated with or endorsed by Nature, Springer Nature, or the article author.

## By Figpad

Created by [Figpad](https://github.com/Figpad), makers of [Figpad AI](https://figpad.ai), an AI-powered scientific illustration platform for researchers.
