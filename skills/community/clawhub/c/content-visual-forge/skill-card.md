## Description:

Content Visual Forge turns PDFs, webpages, articles, screenshots, transcripts, images, and word lists into WeChat covers, knowledge cards, language-learning cards, social carousel visuals, creative micro-assets, and prompt or render packages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fxbin](https://clawhub.ai/user/fxbin)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, educators, marketers, and developers use this skill to convert source material into consistent visual assets for WeChat, Rednote/social carousels, learning cards, covers, and small creative visuals. It is useful when the agent must preserve source fidelity, choose an output format, generate prompts or render packages, and apply quality checks before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private documents or URLs may be processed as source material.

Mitigation: Review source permissions before giving the skill private documents or URLs.

Risk: Local rendering can write visual outputs to disk.

Mitigation: Run the renderer only with trusted local templates and data, and choose an intended output path.

Risk: Generated visuals may misrepresent source facts or overstate derived claims.

Mitigation: Use the skill's Source Lock, content fidelity checks, and quality gate before treating outputs as production-ready.

Risk: External images, brand assets, or style references may have unclear commercial rights.

Mitigation: Record asset source, license, and commercial-use status, and do not use assets in final delivery when those fields are unknown.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fxbin/skills/content-visual-forge)
- [Server-resolved GitHub source](https://github.com/fxbin/skills/tree/main/content-visual-forge)
- [Reference routing index](artifact/references/reference-routing-index.md)
- [Core hard rules](artifact/references/core/hard-rules.md)
- [Execution overview](artifact/references/workflows/execution-overview.md)
- [Asset source policy](artifact/references/config/asset-source-policy.md)
- [Quality checklist](artifact/references/config/quality-checklist.md)
- [Qiaomu Artist Style](https://style.qiaomu.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance, JSON render packages, HTML/CSS render assets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing visual production plans and render packages that can lead to image, PDF, or HTML visual files after generation or local rendering.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
