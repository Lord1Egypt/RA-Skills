## Description:

Generates a weekly Bilibili creator video report with video metrics and top comments, and supports configured report delivery workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wgfuying](https://clawhub.ai/user/wgfuying)

### License/Terms of Use:

Apache 2.0

## Use Case:

Creators, operators, and agents use this skill to collect Bilibili account video performance into a weekly report and send it to a configured contact. It is intended for local automation after the user provides their own Bilibili cookie and target creator UID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Bilibili account cookie and uses that session to call Bilibili endpoints.

Mitigation: Run it only in a controlled local environment, use a low-risk account cookie, and never commit or share the cookie file.

Risk: The WeChat helper builds shell command strings from configurable values such as WECHAT_SEND_PY and the contact argument.

Mitigation: Use only trusted static values for those inputs, and replace shell-string execution with argument-based process execution before unattended use.

Risk: The advertised Agent Mail two-stage confirmation is not present in the shipped scripts.

Mitigation: Do not rely on that confirmation path until it is implemented and verified; manually review outbound report content before sending.

Risk: Push behavior depends on an external WeChat sender script and local desktop state.

Mitigation: Use a trusted sender script, test manually before automation, and verify the intended recipient before scheduled runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wgfuying/skills/bilibili-video-monitoring)
- [Source repository (server-resolved provenance)](https://github.com/WGfuying/bilibili-video-monitoring)
- [SkillHub listing](https://skillhub.cn/skills/bilibili-video-monitoring)
- [Bilibili website](https://www.bilibili.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text report content with configuration and execution guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local cookie, creator UID, and optional message-delivery configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter states 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
