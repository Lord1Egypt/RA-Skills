## Description:

Automates 1688 distribution procurement workflows, including shop binding, supply linking, order follow-up, purchasing, inventory synchronization, price monitoring, supplier switching, and Wangwang reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and commerce operators use this skill to manage procurement after downstream sales, including binding shops, linking 1688 supplies, switching suppliers, querying and creating orders, and using ISV procurement flows for Taobao and Douyin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles shop credentials, AK values, and ISV tokens that may be stored locally or exposed in command output.

Mitigation: Use a limited account, keep credentials out of logs and transcripts, and rotate credentials if they may have been exposed.

Risk: Endpoint override settings can redirect API traffic to an untrusted service.

Mitigation: Set custom gateway or API-base environment variables only when the endpoint is controlled and trusted.

Risk: ISV skill path parameters can cause the agent to call code outside the intended reviewed package.

Mitigation: Use only reviewed local skill paths and verify ISV provider selection before invoking procurement actions.

Risk: The security summary flags unsafe token handling and overly restrictive agent instructions.

Mitigation: Require human review before deployment and keep agent policy controls in place for credential prompts and external calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-distribution-procurement-newton)
- [Publisher profile](https://clawhub.ai/user/1688aiinfra)
- [Skill instructions](artifact/SKILL.md)
- [Project README](artifact/README.md)
- [1688 ClawHub AK portal](https://clawhub.1688.com)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [JSON command results with markdown summaries and structured data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese user-facing output; requires Python 3 and ALI_1688_AK configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
