## Description: <br>
AgentMail Wrapper helps agents send, track, schedule, verify, and manage email across providers such as SendGrid, Mailgun, AWS SES, SMTP, and Gmail OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shepherd217](https://clawhub.ai/user/Shepherd217) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to automate transactional email, campaign sequences, delivery tracking, unsubscribe handling, list hygiene, template management, and compliance reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email automation can send messages or change recipient lists in ways that affect customers and compliance obligations. <br>
Mitigation: Require human confirmation before sending mail, scheduling campaigns, or modifying unsubscribe, bounce, or list-management records. <br>
Risk: Open and click tracking may process recipient behavior data and trigger privacy or consent requirements. <br>
Mitigation: Enable tracking only where recipients have appropriate notice, consent, and a valid legal basis, following the security guidance in evidence.json. <br>
Risk: Provider credentials can grant access to email delivery systems. <br>
Mitigation: Use least-privilege API keys or OAuth scopes and rotate credentials according to the selected provider's policy. <br>


## Reference(s): <br>
- [Midas Skills AgentMail Wrapper Docs](https://docs.midas-skills.com/agentmail-wrapper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include provider configuration, email send options, tracking settings, webhook handling, and list-management operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release, artifact/SKILL.md, artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
