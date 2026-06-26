## Description: <br>
Helps an agent send local images and files to Feishu or Lark private chats and group chats by uploading media and then sending the resulting message key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shouldnotappearcalm](https://clawhub.ai/user/shouldnotappearcalm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to deliver generated images, reports, archives, and other local files into Feishu or Lark conversations. It is intended for workflows where chat delivery is expected and Feishu app credentials are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Feishu app credentials and sends local files or images to an external chat service. <br>
Mitigation: Use a dedicated low-privilege Feishu app credential and run the skill only where Feishu or Lark delivery is expected. <br>
Risk: Confidential or unintended local files could be transmitted to Feishu or Lark. <br>
Mitigation: Confirm the target file path and recipient ID before execution, and avoid using the skill with confidential files unless external transmission is approved. <br>
Risk: App secrets could be exposed through shell history, process listings, logs, or shared transcripts. <br>
Mitigation: Pass credentials through protected configuration or environment handling and avoid echoing secrets in commands, logs, and transcripts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shouldnotappearcalm/feishu-chatfile-skill) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [Lark Open Platform](https://open.larksuite.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May transmit local files or images to Feishu or Lark using supplied app credentials and recipient identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
