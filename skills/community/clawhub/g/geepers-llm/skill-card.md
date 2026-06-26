## Description: <br>
Sends requests to the dr.eamer.dev LLM API for chat completions, vision analysis, image generation, text-to-speech, and video generation across multiple model providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lukeslp](https://clawhub.ai/user/lukeslp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to route LLM requests through a unified third-party API when comparing provider responses or accessing chat, vision, image generation, text-to-speech, and video generation endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-selected prompts, files, images, or speech requests to a disclosed third-party API and routed model providers. <br>
Mitigation: Use the skill only when you trust dr.eamer.dev and its provider routing, and avoid sending secrets, regulated data, confidential business content, private images, or personal information unless that processing is acceptable. <br>
Risk: A shared API key could be exposed or overused if reused broadly. <br>
Mitigation: Use a dedicated, revocable DREAMER_API_KEY and rotate or revoke it when access no longer needs to be granted. <br>


## Reference(s): <br>
- [Geepers Llm on ClawHub](https://clawhub.ai/lukeslp/geepers-llm) <br>
- [Publisher profile: lukeslp](https://clawhub.ai/user/lukeslp) <br>
- [Dreamer API](https://api.dr.eamer.dev) <br>
- [Dreamer site](https://dr.eamer.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with endpoint examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to call an external third-party API using a user-provided API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
