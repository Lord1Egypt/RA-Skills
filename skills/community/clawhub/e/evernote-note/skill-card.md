## Description: <br>
Evernote Note helps an agent search, browse, read, create, append to, and clip web content into Evernote or Yinxiang notes through the documented note APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heavenchenggong](https://clawhub.ai/user/heavenchenggong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to manage personal Evernote or Yinxiang note content, including searching notes, reading note bodies, creating new notes, appending content, and saving web pages into notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires account tokens that can access sensitive Evernote or Yinxiang note data. <br>
Mitigation: Install only for trusted workflows, store EVERNOTE_TOKEN and YX_AUTH_TOKEN as secrets, and avoid exposing test logs or command output that may contain token material. <br>
Risk: The skill can create, append, clip, and potentially delete note content in the connected account. <br>
Mitigation: Confirm write operations before execution and avoid using undocumented destructive paths unless explicit confirmation and recovery guidance are added. <br>
Risk: The security verdict is suspicious because of broad account access, credential handling, and under-disclosed destructive behavior. <br>
Mitigation: Review the security guidance before installation and limit use to accounts where the operator accepts those risks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heavenchenggong/evernote-note) <br>
- [Yinxiang homepage](https://www.yinxiang.com) <br>
- [EDAM API reference](references/api.md) <br>
- [RESTful API reference](references/api-restful.md) <br>
- [Evernote Python SDK](https://github.com/yinxiang-dev/evernote-sdk-python) <br>
- [evernote2 library](https://github.com/JackonYang/evernote2) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline Python and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVERNOTE_TOKEN for EDAM workflows and YX_AUTH_TOKEN for web clipping; may issue API calls that read or modify user notes.] <br>

## Skill Version(s): <br>
2.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
