## Description: <br>
A Chinese relationship-advice skill that reviews relationship descriptions or chat records, scores the relationship across structured dimensions, and gives a direct breakup-or-stay recommendation plus a diagnostic card. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sachi-pp](https://clawhub.ai/user/sachi-pp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can provide relationship context, pasted chat logs, or screenshots and receive a structured relationship assessment. The skill helps them identify red flags, compare relationship quality dimensions, and decide whether to continue or end the relationship. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may submit sensitive relationship chats, screenshots, or personal identifiers for analysis and image-card rendering. <br>
Mitigation: Redact names, phone numbers, addresses, photos, and other identifiers before use, and avoid sharing generated cards that contain private details. <br>
Risk: The artifact behavior can write submitted chat-derived content to local temporary render files and serve it through a local background web server for screenshot generation. <br>
Mitigation: Review and confirm the render/send step before use, and remove temporary card files after generating any needed output. <br>
Risk: The skill uses a blunt relationship-advice persona that may feel harsh or unsuitable for vulnerable users. <br>
Mitigation: Use it as informal decision support only, and seek trusted personal or professional support for safety, abuse, crisis, or mental-health concerns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sachi-pp/dump-or-not) <br>
- [Publisher profile](https://clawhub.ai/user/sachi-pp) <br>
- [Relationship evaluation dimensions](references/dimensions.md) <br>
- [One-vote veto conditions](references/veto-conditions.md) <br>
- [Stop-gain breakup scenario](references/ziying-scenario.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, files] <br>
**Output Format:** [Conversational Markdown followed by a generated 1080px vertical diagnostic card image.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask up to two follow-up questions when required relationship details are missing.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
