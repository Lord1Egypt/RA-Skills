## Description: <br>
Uploads images, videos, and attachments to Feishu (Lark) Bitable through the Feishu Drive media APIs and returns a file_token, automatically choosing direct upload for files up to 20 MB or chunked upload for larger files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billzhuang6569](https://clawhub.ai/user/billzhuang6569) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill when an agent needs to upload local files to a Feishu Bitable app and capture the returned file_token for later attachment-field updates. It is useful when official lark-cli workflows do not cover the /drive/v1/medias/ upload path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu App Secret or tenant access token may be exposed through command-line arguments, shell history, logs, process listings, or shared transcripts. <br>
Mitigation: Use a least-privileged Feishu app, provide credentials through protected environment variables or a secret manager, avoid shared logging environments, and rotate credentials if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billzhuang6569/feishu-bitable-upload) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples; script output is plain text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a Feishu file_token after a successful upload] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
