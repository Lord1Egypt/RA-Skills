## Description: <br>
DKnownAI Guard checks selected text with the DKnownAI Guard API for prompt injection, jailbreak attempts, system-operation risk, and content-risk signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dylanzhangzx](https://clawhub.ai/user/dylanzhangzx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and agent operators use this skill to submit specific text or prompts to DKnownAI Guard and report the returned safety classification for workflow or integration decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a DKnownAI Guard API key, and pasting the key into chat can expose it to the current agent session. <br>
Mitigation: Prefer a platform secret store, environment variable, or private local config file; rotate the key if it was pasted into chat. <br>
Risk: Checked text is sent to DKnownAI Guard for classification. <br>
Mitigation: Submit only the minimum text needed for inspection and avoid including credentials, unrelated private data, system prompts, or internal policy text. <br>
Risk: A failed API call or missing status could be mistaken for a safe classification. <br>
Mitigation: Treat only successful responses with a status field as classifications, and report failures instead of treating them as SAFE. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dylanzhangzx/dknownai-guard) <br>
- [DKnownAI Guard Website](https://dknownai.com/) <br>
- [DKnownAI Guard API Endpoint](https://open.dknownai.com/v1/guard) <br>
- [Guardrail Bridge Plugin](https://clawhub.ai/plugins/@guardrailbridge/guardrail-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance, shell command examples, and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DKnownAI Guard API key through DKNOWNAI_API_KEY or private local config; submitted text is sent to the configured Guard endpoint and results should be treated as classifications, not policy decisions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
