## Description: <br>
Respond to user requests for AIOZ Pin API. Use provided scripts to manage API keys, pin files to IPFS, track usage, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[namle-aioz](https://clawhub.ai/user/namle-aioz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run AIOZ Pin workflows from an agent, including IPFS pinning, pin management, API key management, usage lookup, and billing lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires AIOZ Pin credentials and the security verdict says credential handling needs review. <br>
Mitigation: Use the skill only when the publisher is trusted, provide least-privilege credentials through environment variables, and avoid pasting secrets into chat or command arguments. <br>
Risk: Some operations can change AIOZ Pin account state, including upload, unpin, API key creation, and API key deletion. <br>
Mitigation: Confirm the exact file path, CID, pin ID, or API key ID before running state-changing operations. <br>


## Reference(s): <br>
- [AIOZ Pin Toolkit ClawHub Page](https://clawhub.ai/namle-aioz/aioz-pin-toolkit) <br>
- [namle-aioz Publisher Profile](https://clawhub.ai/user/namle-aioz) <br>
- [AIOZ Pin Documentation](https://docs.pin.aioz.io/) <br>
- [AIOZ Pin API Reference](artifact/references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq, plus AIOZ Pin credentials supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
