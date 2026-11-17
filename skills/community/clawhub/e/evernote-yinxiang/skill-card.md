## Description:

Evernote Yinxiang lets an agent create, read, search, and delete Yinxiang/Evernote notes and list notebooks or tags through a local CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vikingr2023](https://clawhub.ai/user/vikingr2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate a Yinxiang/Evernote account from scripted commands, including creating notes, searching existing notes, reading note contents, deleting notes, and listing notebooks or tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a long-lived Yinxiang token that can access account notes.

Mitigation: Store the token only in a restrictive-permission .env file or environment variable, rotate it if exposure is suspected, and install only for accounts where this access level is acceptable.

Risk: The skill can delete notes without built-in confirmation.

Mitigation: Manually confirm note GUIDs and intent before running delete commands.

Risk: The documented dependency expectations may be incomplete.

Mitigation: Review runtime dependencies before deployment and test the CLI in a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vikingr2023/skills/evernote-yinxiang)
- [Publisher profile](https://clawhub.ai/user/vikingr2023)
- [Yinxiang developer token page](https://app.yinxiang.com/api/DeveloperToken.action)
- [Yinxiang REST API base endpoint](https://app.yinxiang.com/third/third-party-note-service/restful/v1)
- [Evernote international service](https://www.evernote.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require a Yinxiang token configured in a .env file or environment variable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
