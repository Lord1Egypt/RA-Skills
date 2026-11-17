## Description:

Generate beautiful bento grid layouts for social media posts. Create Instagram/Twitter cards with statistics, calendars, music visualization, and custom layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[limoxt](https://clawhub.ai/user/limoxt)

### License/Terms of Use:


## Use Case:

External users, social media creators, and developers use this skill to generate bento-style visual assets for social posts, statistics cards, calendar-style data cards, music listening cards, and custom layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated image commands write fixed filenames under /tmp and may overwrite existing files with the same names.

Mitigation: Review or change output paths before running when existing /tmp files need to be preserved.

Risk: The skill depends on Pillow without a pinned version in the artifact metadata.

Mitigation: Pin and maintain an approved Pillow version before production use.

Risk: The skill executes local Python image-generation snippets.

Mitigation: Run the commands in a normal least-privileged local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/limoxt/skills/bento-grid)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files]

**Output Format:** [Markdown with inline bash code blocks and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes image outputs to /tmp/bento_grid.png, /tmp/stats_card.png, or /tmp/music_card.png.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
