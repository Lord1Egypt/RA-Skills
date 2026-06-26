## Description: <br>
BoldSign is an e-signature platform integration that lets agents send documents for signature, manage documents, create embedded signing links, and track document status through ClawLink OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect a BoldSign account and operate e-signature workflows from an agent, including document listing, sending, editing, embedded signing, field management, file upload, and API credit checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects to a BoldSign account through ClawLink OAuth and can access account-specific document workflows. <br>
Mitigation: Review the OAuth permissions during connection and install only if connecting the BoldSign account through ClawLink is acceptable. <br>
Risk: Write actions can send, edit, upload, create fields for, or remove authentication from real signing workflows. <br>
Mitigation: Require explicit user confirmation before write or high-impact actions, especially document sending, editing, uploading, field creation, and authentication removal. <br>


## Reference(s): <br>
- [BoldSign API Docs](https://developers.boldsign.com/) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub BoldSign Skill](https://clawhub.ai/hith3sh/boldsign) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown instructions with tool names, JSON argument examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ClawLink OAuth; write and destructive BoldSign operations require user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
