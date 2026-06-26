## Description: <br>
Evermemos helps an agent store conversation memories, retrieve history, and use EverMemOS as a long-term memory service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shtrend](https://clawhub.ai/user/shtrend) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to connect an assistant to an EverMemOS service for storing user memories and retrieving relevant history in later conversations. It is appropriate when persistent memory is intentionally enabled and governed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist personal conversation details to a long-term memory service without clear consent, deletion, retention, or transport-security guidance. <br>
Mitigation: Require explicit confirmation before saving personal details, avoid storing secrets or regulated data, and ensure users can review, delete, and disable saved memories. <br>
Risk: A remote EverMemOS service can expose sensitive memory data if it is operated without appropriate trust boundaries. <br>
Mitigation: Run the service in a trusted environment and use authentication and HTTPS when the service is remote. <br>


## Reference(s): <br>
- [EverMemOS documentation](https://github.com/evermemos/EverMemOS) <br>
- [ClawHub Evermemos release page](https://clawhub.ai/shtrend/evermemos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, JSON, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API request examples for an EverMemOS service configured through EVERMEMOS_URL and EVERMEMOS_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
