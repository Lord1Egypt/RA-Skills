## Description:

Turns banker-memo analysis.md and data-provenance.md into structured slide outlines and investment-banker-style PowerPoint decks with tables, charts, risk heatmaps, scenario grids, and callout views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackdark425](https://clawhub.ai/user/jackdark425)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill after a banker memo has been prepared to turn analysis.md and data-provenance.md into a structured slides-outline.md and a rendered .pptx deck. It is suited for investment-banking-style research decks that need real tables, charts, scenario views, risk heatmaps, and traceable numeric inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated JavaScript execution and mutable dependency installation can create local code-execution risk during deck rendering.

Mitigation: Review the skill before installation, run rendering in a constrained workspace, pin dependencies with a reviewed lockfile, and avoid automatic npm install during normal use.

Risk: Untrusted ticker or company-name inputs may affect generated prompts, rendered content, or local command behavior.

Mitigation: Use only trusted ticker and name inputs, validate ts_code before rendering, and serialize generated JavaScript values safely.

Risk: Rendering in a broad workspace may expose credentials or unrelated files to the workflow.

Mitigation: Run the skill only in a narrow deliverable directory and avoid exposing credentials or unrelated files while rendering.

## Reference(s):

- [Banker Slides Prompt Template](references/banker_slides_prompt.md)
- [ClawHub Skill Page](https://clawhub.ai/jackdark425/skills/banker-slides-pptx)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown slide outline, shell command guidance, and rendered PowerPoint file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires existing analysis.md and data-provenance.md inputs; slide numbers are expected to trace back to provenance before rendering.]

## Skill Version(s):

0.9.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
