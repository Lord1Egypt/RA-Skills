## Description: <br>
Give AI agents persistent semantic memory using the BlueColumn API (bluecolumn.ai) for storing, recalling, and searching memories across notes, conversations, documents, and audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an AI agent to BlueColumn memory endpoints so the agent can store approved session summaries, notes, documents, or audio-derived content and later retrieve relevant stored context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation summaries and user-provided content to an external memory service. <br>
Mitigation: Require explicit user consent before saving session summaries, documents, audio, personal data, credentials, confidential business details, or regulated information. <br>
Risk: The skill requires a sensitive BlueColumn API key. <br>
Mitigation: Store the API key only in a platform secret store, avoid logging or displaying it, and verify the provider endpoint before use. <br>
Risk: Stored memory may have retention or deletion implications outside the agent runtime. <br>
Mitigation: Review BlueColumn retention and deletion terms before using the skill for production or sensitive workflows. <br>


## Reference(s): <br>
- [BlueColumn API Reference](references/api.md) <br>
- [BlueColumn](https://bluecolumn.ai) <br>
- [BlueColumn Memory on ClawHub](https://clawhub.ai/bluecolumnconsulting-lgtm/bluecolumn-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include endpoint selection guidance, curl commands, request fields, response-shape expectations, and API key handling instructions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
