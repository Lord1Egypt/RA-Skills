## Description: <br>
Send and receive email as your AI agent, including checking inbox, sending email, replying to messages, setting up an email alias, and managing agent email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agnicpay-prog](https://clawhub.ai/user/agnicpay-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage an Agnic agent email address, including setup, address checks, inbox review, sending, and replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive email data, including inbox contents, recipients, subjects, and message bodies. <br>
Mitigation: Treat email data as sensitive and review message content before exposing, sending, or replying. <br>
Risk: The skill may use AGNIC_TOKEN for headless authentication. <br>
Mitigation: Store AGNIC_TOKEN securely, avoid logging it, and pass it only to trusted Agnic commands. <br>
Risk: Send and reply commands can contact external recipients. <br>
Mitigation: Review the exact recipient, subject, and body before executing send or reply commands. <br>
Risk: The skill invokes `npx agnic@latest`, which depends on the Agnic npm package at execution time. <br>
Mitigation: Use the skill only when you trust the Agnic npm package and the execution environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agnicpay-prog/agnic-agent-email) <br>
- [Agnic app](https://app.agnic.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown with inline bash commands and JSON command output references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Agnic authentication and may handle sensitive email contents, recipients, subjects, bodies, and AGNIC_TOKEN.] <br>

## Skill Version(s): <br>
2.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
