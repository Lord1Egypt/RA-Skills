## Description:

Helps users browse customizable Leewow products, turn images or ideas into gifts, upload images, and generate AI-powered product mockups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yqxu](https://clawhub.ai/user/yqxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to browse customizable gift templates, choose a product, upload a design image, and generate a Leewow preview that can be delivered through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure through Leewow or Feishu secrets used by direct API calls.

Mitigation: Use dedicated least-privilege credentials, store them outside shared outputs, and avoid logging or echoing secret values.

Risk: File exposure when user-provided paths are uploaded or local preview and template images are cached.

Mitigation: Keep sensitive files outside workspace paths the skill can read or upload, and review symlink and path handling before use.

Risk: Endpoint or command misuse from tool parameters and configurable API bases.

Mitigation: Run the skill in a constrained environment, allow only trusted Leewow and Feishu API bases, and avoid passing untrusted text into tool parameters.

## Reference(s):

- [Custom Gift Leewow on ClawHub](https://clawhub.ai/yqxu/skills/custom-gift-leewow)
- [Custom Gift Leewow homepage](https://github.com/AIDiyTeams/claw-skill/tree/main/custom-gift-leewow)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown and JSON tool results, with preview images saved as local files and Feishu cards sent directly when configured.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Leewow and Feishu credentials; generation is asynchronous and may return NO_REPLY after direct Feishu delivery.]

## Skill Version(s):

1.0.24 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
