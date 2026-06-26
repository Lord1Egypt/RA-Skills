## Description: <br>
Baidu trans-cli document translation for PDF, Word, Excel, PowerPoint, text, HTML, and related file formats while preserving formatting and layout. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-translate](https://clawhub.ai/user/baidu-translate) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document translation agents use this skill to submit supported files to Baidu's trans-cli workflow, poll asynchronous translation jobs, handle errors, and download translated files after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Translating a file sends its contents to Baidu's document translation service. <br>
Mitigation: Do not submit confidential, regulated, or customer documents unless the user's organization permits processing by Baidu. <br>
Risk: The skill requires a TRANS_API_KEY credential for Baidu's translation service. <br>
Mitigation: Configure the credential outside the skill content, stop on authentication or configuration errors, and guide the user to update the key when needed. <br>
Risk: Document translation is asynchronous and an unbounded wait can block an agent workflow. <br>
Mitigation: Use the submit and poll loop with an agent-level timeout, save the request_id on WAIT_TIMEOUT, and resume the job later instead of continuing to wait. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/baidu-translate/baidu-file-translate) <br>
- [Baidu Translate](https://fanyi.baidu.com) <br>
- [Baidu Translate API key management](https://fanyi-api.baidu.com/manage/apiKey) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with bash commands and JSON response contracts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the trans CLI binary and TRANS_API_KEY. Translated file downloads should be confirmed with the user before saving.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
