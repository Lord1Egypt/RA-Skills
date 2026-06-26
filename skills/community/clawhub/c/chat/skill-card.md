## Description: <br>
Learns communication preferences from explicit feedback. Adapts tone, format, and style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to remember explicitly confirmed communication preferences and adapt future responses by tone, format, and style. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Explicitly confirmed style preferences are stored locally under ~/chat and may persist across future chats. <br>
Mitigation: Review ~/chat/memory.md periodically, avoid confirming sensitive personal information as a preference, and use the documented forget behavior for unwanted entries. <br>
Risk: Incorrect or outdated preferences could steer future responses in an unwanted style. <br>
Mitigation: Rely on explicit feedback only, ask when signals are ambiguous, and remove or update preferences when the user corrects them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/chat) <br>
- [Confirmation criteria](artifact/criteria.md) <br>
- [Preference dimensions](artifact/dimensions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown responses with optional inline shell commands and local preference notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local preference files under ~/chat only from explicit user feedback.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
