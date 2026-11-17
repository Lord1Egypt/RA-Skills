## Description:

Create AI marketing videos for ads, promos, product launches, and brand content using inference.sh CLI workflows for video, image, voiceover, music, and media assembly models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Marketing teams, creators, and developers use this skill to draft command-line workflows for product promos, social ads, launch videos, testimonials, explainers, voiceovers, music, and assembled marketing clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick-start path uses a mutable remote installer executed directly in a shell.

Mitigation: Prefer a separately downloaded, version-pinned inference.sh CLI and verify its checksum or signature before installation.

Risk: Marketing plans, customer data, unreleased launch details, and private media may be sent to external generation services.

Mitigation: Submit only data approved by the organization for those services, and remove confidential or regulated content from prompts and media inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/okaris/skills/ai-marketing-videos)
- [inference.sh](https://inference.sh)
- [inference.sh CLI installer](https://cli.inference.sh)
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON command inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides reusable prompt and command templates for external inference.sh services; generated media quality and data handling depend on those services.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
