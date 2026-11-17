## Description:

基于明日DMP开放平台API，提供组合人群、广告行为规则人群、APP规则人群、LBS规则人群、拓展人群和打通人群等6种人群圈选方式，并支持参数检查、格式校验、业务规则校验和参数确认。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingri26](https://clawhub.ai/user/mingri26)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers and DMP operators use this skill to create, query, and manage Mingdata DMP audience segments for targeting, remarketing, audience analysis, regional promotion, competitor analysis, lookalike expansion, and cross-screen activation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill depends on local helper discovery, credential storage, and mandatory logging or installation flows.

Mitigation: Install only after reviewing the publisher and helper skills, use reviewed pinned dependencies, and avoid auto-installing supporting skills without inspection.

Risk: Mingdata DMP API credentials are sensitive and may be stored locally or entered through chat or command-line arguments.

Mitigation: Use short-lived or least-privilege credentials where possible, avoid sharing long-lived AK/SK values in chat or shell history, protect local credential files, and rotate credentials after testing.

Risk: Task logging can store full audience-targeting parameters locally.

Mitigation: Skip optional logging unless local storage of audience criteria is acceptable, and review or delete task history files according to the user's data handling policy.

Risk: Audience creation and targeting workflows can have legal, privacy, and business impact if source data or user authorization is improper.

Mitigation: Confirm that all audience data sources, permissions, and campaign uses comply with applicable policies and regulations before calling the DMP APIs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingri26/skills/dmp-segment)
- [Mingdata DMP auth skill](https://clawhub.ai/mingri26/mingdata-dmp-auth)
- [DMP skill logger](https://clawhub.ai/mingri26/dmp-skill-logger)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with JSON API parameters and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create Mingdata DMP audience tasks, query task status, configure credentials, and optionally record task metadata through a separate logger skill.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
