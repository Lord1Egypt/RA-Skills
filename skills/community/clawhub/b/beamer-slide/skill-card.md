## Description:

Beamer Slide helps agents create, compile, review, and polish academic Beamer slide decks, including TikZ diagrams, figure extraction, visual audits, and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noi1r](https://clawhub.ai/user/noi1r)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and educators use this skill to create, compile, review, audit, and validate Beamer slide decks for lectures, seminars, conference talks, defenses, and academic presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can edit Beamer projects and run LaTeX/PDF commands.

Mitigation: Install only when that behavior is acceptable, prefer explicit Beamer requests, and review proposed file changes before use.

Risk: Unsafe filenames or paths could affect shell compilation and PDF utility commands.

Mitigation: Use safe filenames and avoid raw shell metacharacters in paths.

Risk: Figure extraction can create or overwrite files in a figures directory.

Mitigation: Review extracted files before allowing them to overwrite existing figures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noi1r/skills/beamer-slide)
- [Create Workflow](references/create-workflow.md)
- [Review Actions](references/review-actions.md)
- [TikZ Quality Standards and Common Patterns](references/tikz-standards.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and LaTeX/Beamer code with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or edit .tex files, figures, and validation reports when the selected action calls for it.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
