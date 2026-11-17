## Description:

用 JSON 生成报纸风竖版金融卡片视频 (1080x1920).

This skill is ready for commercial/non-commercial use.

## Publisher:

[bosslay](https://clawhub.ai/user/bosslay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation teams use this skill to turn structured financial-style JSON entries into local vertical MP4 card videos with newspaper-style layout, optional audio, and built-in compliance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The renderer creates parent directories and overwrites the requested MP4 output path.

Mitigation: Run it in a dedicated project directory and choose an explicit output path that does not point at important existing files.

Risk: User-provided JSON, template, audio, and word-list paths affect local rendering behavior.

Mitigation: Review those paths before execution and keep inputs in a scoped workspace with only the intended assets.

Risk: Financial-style card text can be misleading if it omits disclaimers or uses directive language.

Mitigation: Use explicit footers, run the sensitive-word check in strict mode, and review the final JSON and rendered cards before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bosslay/skills/financial-card-video)
- [Sample card input JSON](artifact/examples/sample_cards.json)
- [Paper card HTML template](artifact/templates/paper_card.html)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [MP4 video files from JSON input, with optional audio and console verification output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 1080x1920 H.264/yuv420p video; optional AAC audio is composed from per-card audio and background music.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
