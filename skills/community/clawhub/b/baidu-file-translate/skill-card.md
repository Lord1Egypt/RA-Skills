## Description:

Baidu File Translate helps agents translate uploaded or referenced documents with Baidu trans-cli while preserving the original document formatting and layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baidu-translate](https://clawhub.ai/user/baidu-translate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user asks to translate a file or convert a document into another language. It covers common office and text formats, submits asynchronous translation jobs, polls for completion, and guides download only after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents submitted for translation are processed by Baidu's translation service.

Mitigation: Use only documents that policy allows to be processed by Baidu, and avoid confidential, regulated, or highly sensitive files unless explicitly approved.

Risk: The translation CLI requires TRANS_API_KEY, which may be exposed to local tooling or logs if mishandled.

Mitigation: Store the key in the agent environment or secret manager, avoid echoing it in commands, and rotate it if exposure is suspected.

Risk: The skill depends on an npm-installed trans CLI package.

Mitigation: Pin or otherwise control the npm dependency in managed environments before deployment.

Risk: Document translation is asynchronous and can exceed an agent's active session.

Mitigation: Use the submit and poll workflow, set a bounded agent timeout, preserve request_id on WAIT_TIMEOUT, and resume later instead of retrying blindly.

## Reference(s):

- [Baidu Translate](https://fanyi.baidu.com)
- [Baidu API Key Management](https://fanyi-api.baidu.com/manage/apiKey)
- [ClawHub Skill Page](https://clawhub.ai/baidu-translate/skills/baidu-file-translate)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses asynchronous submit and poll workflow; requires trans CLI and TRANS_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
