## Description:

Create HTML presentations in 24 international design styles and optionally convert them to editable PowerPoint .pptx files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create visually styled HTML slide decks from prompts or existing content, then optionally extract PPTX content or convert generated HTML slides into editable .pptx files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional Vercel deployment step can run an unbundled local shell script and may publish presentation content externally.

Mitigation: Review or disable the deployment step; only run deployment after inspecting the deploy script, confirming the publication target, and verifying the deck contains no confidential material.

Risk: PPTX extraction and conversion depend on python-pptx in the local Python environment.

Mitigation: Use a virtual environment with pinned dependencies before running PPTX tooling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xcjl/skills/cjl-slides)
- [Style Previews](artifact/STYLE_PREVIEWS.md)
- [Chart.js CDN Reference](https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown responses with HTML code blocks plus generated HTML, JSON, and PPTX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PPTX extraction and conversion require python-pptx; generated chart slides may reference Chart.js CDN resources.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
