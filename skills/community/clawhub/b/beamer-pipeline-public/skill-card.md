## Description:

Convert academic papers or notes into Chinese academic Beamer slides using a seven-phase local pipeline with pluggable agent execution and LaTeX compilation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccmxigua](https://clawhub.ai/user/ccmxigua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and academic users use this skill to turn paper Markdown or structured notes into a local Beamer slide package with analysis, slide planning, equation and notation coverage, LaTeX source, and optional PDF output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch remote images referenced in input Markdown during asset preparation.

Mitigation: Run it on trusted papers or in a sandboxed environment, or use --skip-assets for untrusted Markdown.

Risk: Default agent execution and recovery behavior can access local OpenClaw configuration, sessions, or prior task outputs.

Mitigation: Prefer --no-agent or an explicit --agent-cmd workflow until ~/.openclaw access and output-directory access are reviewed and constrained.

Risk: Automatically generated academic decks may contain incorrect or incomplete equation coverage, notation definitions, translations, or rendered slide content.

Mitigation: Use the included validation gates and review analysis.json, slides.json, main.tex, and main.pdf before publishing or presenting the deck.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ccmxigua/skills/beamer-pipeline-public)
- [Beamer Pipeline Public Architecture Notes](artifact/references/beamer-pipeline-code-explanation.md)
- [Upstream Design Notes](artifact/references/UPSTREAM_DESIGN_NOTES.md)
- [Beamer Generation Contract](artifact/templates/beamer_contract.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prompts and contracts, JSON artifacts, LaTeX source, optional PDF output, and CLI text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes files into a user-selected output directory; may invoke a configured agent command and LaTeX compiler.]

## Skill Version(s):

0.3.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
