## Description: <br>
Evernote Yinxiang helps agents create, read, search, delete, and organize Yinxiang/Evernote notes through the included CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vikingr2023](https://clawhub.ai/user/vikingr2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage personal or team notes in Yinxiang/Evernote, including creating notes, searching notes, retrieving note content, listing notebooks and tags, and moving notes to trash. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a full-access Yinxiang/Evernote developer token. <br>
Mitigation: Store the token only in the local environment or skill .env file, protect that file from sharing, and rotate or revoke the token if it may have been exposed. <br>
Risk: Search and get operations can expose private note titles and content. <br>
Mitigation: Review command output before sharing, logging, or pasting it into other tools. <br>
Risk: Delete operations act on note GUIDs and can remove the wrong note if the GUID is mistaken. <br>
Mitigation: Confirm the target GUID and note title before running delete commands. <br>
Risk: The release documentation says the skill only depends on requests, while the included script imports Evernote, Thrift, and certificate-related Python modules. <br>
Mitigation: Install and test the actual Python dependencies in a sandbox before relying on the skill in a production workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vikingr2023/evernote-yinxiang) <br>
- [Publisher profile](https://clawhub.ai/user/vikingr2023) <br>
- [Yinxiang developer token page](https://app.yinxiang.com/api/DeveloperToken.action) <br>
- [Yinxiang REST API endpoint](https://app.yinxiang.com/third/third-party-note-service/restful/v1) <br>
- [Evernote service](https://www.evernote.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI returns success/error JSON and may include note GUIDs, titles, URLs, timestamps, notebook or tag identifiers, and note content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
