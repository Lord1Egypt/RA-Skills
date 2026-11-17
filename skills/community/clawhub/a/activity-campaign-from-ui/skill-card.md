## Description:

Turn campaign UI references into a new H5/Web campaign proposal, page architecture, and HTML/CSS/JavaScript high-fidelity front-end draft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bigin58](https://clawhub.ai/user/bigin58)

### License/Terms of Use:

MIT-0

## Use Case:

Campaign planners, designers, and front-end developers use this skill to analyze campaign UI references, create a new non-copying activity concept, plan H5/Web page architecture, and produce fixed-stack HTML/CSS/JavaScript draft files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated JavaScript may reuse unsafe innerHTML string rendering patterns for campaign data, rules, prize text, records, or popup content.

Mitigation: Review generated JavaScript before campaign use and replace unsafe string rendering with safe DOM construction or textContent for user-controlled or CMS-controlled data.

Risk: Local delivery can generate image assets and write files under project/<delivery-slug>/ when explicitly requested.

Mitigation: Confirm the requested output path and inspect generated files and assets before using them in a real campaign workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bigin58/skills/activity-campaign-from-ui)
- [Scope](artifact/references/scope.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, configuration, guidance]

**Output Format:** [Markdown responses with optional HTML, CSS, JavaScript, mock-data, image asset, and JSON-like campaign configuration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs stay on the H5/Web HTML/CSS/JavaScript stack; local deliveries are written under project/<delivery-slug>/ when explicitly requested.]

## Skill Version(s):

0.6.0 (source: server release evidence and CHANGELOG.md, released 2026-04-08)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
