## Description:

将本地技能发布到 ClawHub 平台，支持设置 slug、名称、版本、路径和更新日志。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaichao87](https://clawhub.ai/user/wuhaichao87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers who publish ClawHub skills use this skill to package and upload a local skill directory with slug, display name, version, path, and changelog metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports a plaintext shared ClawHub bearer token embedded in the skill.

Mitigation: Remove the token, rotate it, and require the user to provide credentials through an appropriate secret mechanism before publishing.

Risk: The release evidence reports that local skill files are uploaded with limited user-facing control or disclosure.

Mitigation: Review the skill directory before publishing and add a clear file preview plus explicit confirmation before upload.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wuhaichao87/skills/clawhub-publish-tool)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Guidance]

**Output Format:** [Markdown usage guidance with shell and Python examples; command execution emits console text and JSON-like result objects.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uploads selected local skill files to ClawHub when executed; credential handling must be fixed before use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
