## Description:

Browse and create custom gifts, including personalized bags, mugs, phone cases, apparel, and other products, by uploading an image to generate an AI-powered product mockup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yqxu](https://clawhub.ai/user/yqxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to browse customizable gift templates, generate product previews from workspace images, and return preview images with purchase links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User images are uploaded to Leewow/COS and generated previews are stored locally under ~/.openclaw/workspace.

Mitigation: Use only non-sensitive images and inform users before upload or preview generation.

Risk: Shell command templates and file-handling could expose local files or credentials if untrusted tool parameters are accepted.

Mitigation: Limit use to trusted operators until commands use safe argument execution and workspace path checks resolve symlinks.

Risk: Loading ~/.openclaw/.env can make unrelated local environment values available during skill execution.

Mitigation: Restrict environment loading to the required Leewow variables and avoid logging credential values.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yqxu/skills/custom-gifts-leewow)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, guidance]

**Output Format:** [JSON tool outputs with local image paths, task status, and signed purchase URLs, plus agent-facing text captions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads template and preview images under ~/.openclaw/workspace and requires a CLAW_SK credential for Leewow API access.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
