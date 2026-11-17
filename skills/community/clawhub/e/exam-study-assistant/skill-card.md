## Description:

Full-cycle exam preparation and study assistant for study planning, knowledge summaries, mind-map outlines, mistake review, spaced repetition, practice questions, and exam sprint planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and exam candidates use this skill to organize exam preparation, summarize study material, create review outlines, diagnose missed questions, generate practice items, and plan final review sprints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional self-learning module stores usage counts, error notes, and user preferences in learned_patterns.json.

Mitigation: Review this behavior before installing; disable the learner script, constrain its use, or clear learned_patterns.json when persistent personalization is not wanted.

Risk: The self-learning rules can influence future skill behavior and propose edits to the skill files.

Mitigation: Require explicit review before applying any generated skill-file changes, and rescan the artifact after edits.

Risk: Generated study plans and practice questions may not match official exam scope, difficulty, or scoring.

Mitigation: Use outputs as study aids and verify important content against official syllabi, textbooks, and past papers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/exam-study-assistant)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown study plans, outlines, analyses, practice questions, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local learned_patterns.json when the optional learner script is run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
