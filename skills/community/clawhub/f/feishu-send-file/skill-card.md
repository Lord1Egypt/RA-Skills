## Description: <br>
Sends local files and fallback image uploads to Feishu or Lark by uploading media first and then sending the returned file_key or image_key to a user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadaniya99](https://clawhub.ai/user/dadaniya99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to deliver generated files, documents, code artifacts, archives, and images to Feishu or Lark users. It is especially useful when a local image path would otherwise be sent as plain text instead of visible image content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local files or images may contain sensitive content and are uploaded through Feishu or Lark. <br>
Mitigation: Confirm the exact file path, file name, and recipient before running the helper script, and avoid sending files that contain unintended sensitive data. <br>
Risk: Feishu or Lark app secrets are passed as command arguments and may be exposed in logs, shell history, or process listings. <br>
Mitigation: Use least-privilege app credentials and prefer a safer secret-injection method when operating outside a controlled environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dadaniya99/feishu-send-file) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Lark Open Platform](https://open.larksuite.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python helper scripts and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper scripts perform Feishu or Lark API calls that upload selected local files or images and send the resulting media key to a recipient.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
