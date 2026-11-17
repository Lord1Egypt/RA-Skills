## Description:

Creates a single self-contained interactive HTML explainer with hand-built Canvas figures from source files, web research, or mixed intake.

This skill is ready for commercial/non-commercial use.

## Publisher:

[analyticalmonk](https://clawhub.ai/user/analyticalmonk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn papers, reports, transcripts, topics, or mixed sources into browser-openable interactive explainers with prose and Canvas figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated explainers may make external font requests to Google Fonts.

Mitigation: Use the offline font option or remove the font request when outbound network contact is not acceptable.

Risk: Local preview servers can expose generated files beyond the intended machine if bound broadly.

Mitigation: Preview from a dedicated output directory and bind the server to 127.0.0.1.

Risk: The skill may read supplied source material and optionally use web research to draft claims.

Mitigation: Provide only appropriate source material and complete the required fact-check gates before relying on the explainer.

## Reference(s):

- [Article Template](assets/article-template.html)
- [Color Palettes](references/color-palettes.md)
- [Figure Archetypes](references/figure-archetypes.md)
- [Intake From Files](references/intake-from-files.md)
- [Intake From Research](references/intake-from-research.md)
- [Template Walkthrough](references/template-walkthrough.md)
- [Voice and Style](references/voice-and-style.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus a self-contained HTML file with inline CSS and JavaScript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one browser-openable index.html; external network access is limited to optional Google Fonts unless offline fonts are substituted.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
