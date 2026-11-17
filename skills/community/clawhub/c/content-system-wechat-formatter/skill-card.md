## Description:

Render article markdown into WeChat-style HTML as an independent executor for WeChat layout preview, WeChat HTML output, or a publishable HTML artifact generated from an article markdown draft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abigale-cyber](https://clawhub.ai/user/abigale-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to convert finalized Markdown articles into WeChat-compatible HTML and optionally append summary, quote, share-copy, and CTA blocks from a sibling writing-pack sidecar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed runtime imports executable renderer code from a hard-coded personal filesystem path outside the packaged artifact.

Mitigation: Package or pin the renderer dependency inside the release and review the resolved runtime path before installing or executing the skill.

Risk: Generated ready HTML files could overwrite an existing output for the same slug.

Mitigation: Confirm generated output filenames or use a clean output directory before running the formatter.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abigale-cyber/skills/content-system-wechat-formatter)

## Skill Output:

**Output Type(s):** [markdown, code]

**Output Format:** [Standalone WeChat-compatible HTML file generated from Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes content-production/ready/<slug>-wechat.html and may include optional sidecar summary, quote, share-copy, and CTA blocks.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
