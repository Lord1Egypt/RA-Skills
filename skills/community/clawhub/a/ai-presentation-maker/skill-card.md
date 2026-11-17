## Description:

AI Presentation Maker is an interview-driven pitch deck generator for OpenClaw agents that creates fact-grounded slide decks with speaker notes, validation flags, and exports to Markdown, HTML, Gamma-ready Markdown, PPTX, and PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffjhunter](https://clawhub.ai/user/jeffjhunter)

### License/Terms of Use:

MIT

## Use Case:

Developers, consultants, and creators use this skill to interview a presenter, choose a narrative angle, and generate presentation decks grounded in user-provided facts, costs, results, and caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unsafe HTML export handling for untrusted or third-party Markdown.

Mitigation: Review generated decks before HTML export and avoid exporting untrusted Markdown until sanitization is fixed.

Risk: The security review flags optional Persona OS import behavior that can read SOUL.md or AGENTS.md outside the stated presentation workspace.

Mitigation: Use Persona OS import only when the user explicitly wants those files read for speaker information.

Risk: Optional Python export dependencies can introduce dependency and environment risk.

Mitigation: Install optional dependencies such as python-pptx only in an isolated, pinned environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeffjhunter/skills/ai-presentation-maker)
- [Publisher profile](https://clawhub.ai/user/jeffjhunter)
- [Gamma.app](https://gamma.app)
- [presentation-helper.sh](assets/presentation-helper.sh)
- [export-html-slides.py](references/export-html-slides.py)
- [export-pptx.py](references/export-pptx.py)
- [export-gamma.sh](references/export-gamma.sh)
- [slide-templates.py](references/slide-templates.py)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown slide decks with speaker notes, validation summaries, and optional HTML, Gamma Markdown, PPTX, or PDF exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores presentation JSON and Markdown under ~/workspace/presentations; optional exports require python3, python-pptx, or pandoc depending on format.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, artifact/_meta.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
