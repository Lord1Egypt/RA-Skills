## Description: <br>
Skill for accessing external AI services (ChatGPT, Claude, Hugging Face, etc.) via browser automation (Chrome Relay) and APIs to assist with tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[konscious0beast](https://clawhub.ai/user/konscious0beast) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to consult external AI services through browser automation or provider APIs when a task benefits from another model for reasoning, coding, generation, or summarization. It is intended for user-authorized interactions with third-party services and credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user content to third-party AI services. <br>
Mitigation: Confirm the target provider and the exact content to send before use; avoid confidential, regulated, personal, financial, or secret-bearing data unless the user explicitly approves that data flow. <br>
Risk: Provider API calls or subscription-backed browser sessions may incur costs or consume account quotas. <br>
Mitigation: Use paid APIs only with explicit authorization, estimate likely usage where possible, and prefer lower-cost or browser-based options when they meet the task need. <br>
Risk: Credential-backed requests can expose tokens or logged-in sessions if handled carelessly. <br>
Mitigation: Rely on existing authenticated sessions or environment variables without revealing credential values, and do not log secrets or include them in prompts sent to external services. <br>


## Reference(s): <br>
- [OpenClaw Browser Relay docs](https://docs.openclaw.ai/browser-relay) <br>
- [Hugging Face skill](../huggingface/SKILL.md) <br>
- [Browser automation playbook](../../memory/patterns/playbooks.md) <br>
- [Using free AI models online pattern](../../memory/2026-02-18.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown guidance with inline code blocks and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose browser automation actions or API requests that require user authorization, provider credentials, and cost awareness.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
