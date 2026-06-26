## Description: <br>
Downloads files such as videos, images, documents, and audio from Feishu messages to local storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cindypapa](https://clawhub.ai/user/cindypapa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to fetch Feishu message attachments for local editing, archiving, content workflows, or downstream AI processing. It can be used from command-line flows or Python scripts after Feishu app credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A downloaded attachment may be saved with an unsafe or unexpected filename. <br>
Mitigation: Use a dedicated download directory and provide a simple explicit filename whenever possible. <br>
Risk: Downloaded Feishu attachments may contain sensitive corporate or personal data. <br>
Mitigation: Store downloads only in approved locations, limit access to Feishu app credentials, and review files before sharing or processing them downstream. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cindypapa/feishu-message-download) <br>
- [Feishu message resource API endpoint](https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/resources/{file_key}?type=file) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Downloaded local files, JSON-like result dictionaries, and Markdown usage guidance with bash and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials and the requests Python dependency.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
