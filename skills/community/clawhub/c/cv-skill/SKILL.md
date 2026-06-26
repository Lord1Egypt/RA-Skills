---
name: cv-skill
description: Create professional Harvard-style resumes, CVs, and matching cover letters from user-provided candidate descriptions, structured data, or existing resumes. Use when the user wants a polished one-page or role-targeted resume, needs multiple resume versions for different job directions, wants to convert raw candidate notes into structured bullets, or needs DOCX/PDF outputs in any language from structured input data.
version: 1.1.0
---

# CV Skill

Create role-targeted, black-and-white, Harvard-style resumes and matching cover letters from candidate descriptions, structured input, or existing resumes.

## Use this skill when

- The user wants a professional resume or CV in `.docx`
- The user wants a concise cover letter matched to a role and employer
- The user gives a rough candidate description and wants the agent to draft the resume from scratch
- The user wants one candidate rewritten into multiple job-targeted versions
- The user provides a PDF, notes, or rough bullets and wants a polished resume
- The user wants tighter, more professional bullets without fluff
- The user wants a Harvard-style layout with larger spacing and clean hierarchy
- The user needs output in a language other than Chinese or English

## Workflow

### 1. Gather candidate data

Use the structured schema in `references/input-schema.md`.

If you are starting from an existing resume, extract:

- contact info
- summary / positioning
- education
- work experience
- projects
- campus or extracurricular items
- tools, languages, certificates
- target job directions

### 2. Define track-specific positioning

For each job direction, rewrite:

- resume title
- 2-3 sentence summary
- bullet emphasis within experience
- skills ordering
- optional cover letter angle: opening fit, 1-2 proof examples, closing

Keep facts intact. Do not invent results or responsibilities.

### 3. Apply Harvard-style resume rules

Use `references/harvard-hes-2024-notes.md` as the quality checklist:

- tailor content to the target role or industry
- keep format consistent and easy to skim
- use reverse chronological order within sections unless relevance requires a different order
- start bullets with active verbs and include scope, skills, and impact
- quantify results when the source material supports it
- remove personal pronouns, photos, age, marital status, references, slang, and low-signal filler
- check contact email and phone are present before delivery

### 4. Generate the resume

Run:

```bash
python3 scripts/generate_resume.py --input assets/example_profile.json --track all --output-dir /tmp/cv-output
```

Generate a specific track:

```bash
python3 scripts/generate_resume.py --input candidate.json --track operations --output-dir /tmp/cv-output
```

Try PDF export when LibreOffice is installed:

```bash
python3 scripts/generate_resume.py --input candidate.json --track all --output-dir /tmp/cv-output --pdf
```

If `python-docx` is missing, install dependencies first:

```bash
python3 -m pip install -r requirements.txt
```

### 5. Draft a matching cover letter when requested

Use the same font family and general spacing as the resume.

Cover letter structure:

- recipient block when known; otherwise use a clean generic greeting
- opening paragraph naming the role, employer, and fit
- middle paragraph(s) connecting 1-2 specific examples to the role requirements
- closing paragraph restating interest and interview availability

Keep it concise, factual, and no longer than one page. Do not restate the whole resume.

### 6. Validate before delivery

Check that:

- no hardcoded personal info from unrelated candidates remains
- dates and headings are consistent
- bullets are role-targeted rather than generic
- low-signal items are removed or pushed down
- generated filenames are generic and safe
- resume and cover letter use matching typography
- exported PDF preserves layout and does not break bullets or spacing
- required contact info is present: email and phone

## Layout rules

- Single column
- Black and white only
- Letter page size by default; A4 supported with `style.page_size`
- Section headers with strong hierarchy
- Balanced white space; avoid cramped default Word spacing
- Short, factual bullets
- Avoid self-evaluation phrases such as “责任心强” or “结果导向”
- Prefer evidence and scope over adjectives
- Contact line may include city, phone, email, LinkedIn, portfolio, or other relevant links
- Use section order by relevance; education may move down when experience is stronger

## Safety rules

- Do not hardcode real candidate data into scripts
- Do not store secrets, API keys, tokens, or `.env` files in the skill folder
- Keep outputs outside the skill folder unless the user explicitly wants examples saved there
- Use `assets/example_profile.json` only as a redacted example

## Files

- `scripts/generate_resume.py`: generic generator
- `requirements.txt`: Python dependencies
- `references/input-schema.md`: input contract
- `references/rewriting-guide.md`: track-specific rewriting guidance
- `references/harvard-hes-2024-notes.md`: Harvard Extension School resume and cover letter checklist
- `assets/example_profile.json`: safe sample input
- `agents/openai.yaml`: UI metadata
