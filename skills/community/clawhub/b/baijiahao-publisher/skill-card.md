## Description:

Automates Baijiahao article publishing through the OpenClaw browser, including login, title and body entry, cover upload, AI-content declaration, and publish submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[279458179](https://clawhub.ai/user/279458179)

### License/Terms of Use:

MIT-0

## Use Case:

External publishers and operators use this skill to prepare and submit Baijiahao articles through an OpenClaw browser session. It is intended for workflows where an agent handles page navigation, content entry, cover upload, AI-content declaration, and publish submission with user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a cookie-injection login fallback that could expose session credentials.

Mitigation: Use the normal QR-code login flow under the account owner's control and do not paste cookies or session strings into the agent.

Risk: The skill can publish live content to a Baijiahao account.

Mitigation: Confirm the exact article title, body, cover image, account, AI-content declaration, and final publish action before posting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/279458179/skills/baijiahao-publisher)
- [ClawHub publisher profile](https://clawhub.ai/user/279458179)
- [Baijiahao publishing console](https://baijiahao.baidu.com/builder/rc/edit?type=news&is_from_cms=1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with browser action snippets, upload path guidance, and publishing status interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenClaw browser session and human-controlled account login; may guide actions that submit live content.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact source declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
