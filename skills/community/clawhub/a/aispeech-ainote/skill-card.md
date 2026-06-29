## Description: <br>
Enables OpenClaw agents to access AISpeech office notebook and recording-card product capabilities for notes, meeting records, todos, personal knowledge search, label knowledge bases, and hotword management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fairylong](https://clawhub.ai/user/fairylong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent retrieve, create, update, and delete AISpeech notes, todos, labels, knowledge-base entries, and hotwords through the AIWork APIs. It is intended for controlled access to a user's own AIWork account data with explicit care around write and delete actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write or delete personal notes, todos, groups, labels, and hotwords. <br>
Mitigation: Require the agent to show the exact target and obtain explicit confirmation before delete, bulk-change, or other destructive actions. <br>
Risk: The skill uses an AIWork authorization token and can access account data according to granted scopes. <br>
Mitigation: Install only for trusted AIWork accounts, grant the minimum scopes needed, and store AIWORK_AUTH_TOKEN only in the intended OpenClaw environment. <br>
Risk: Broad note-content retrieval can expose unnecessary meeting transcripts, OCR text, summaries, or AI insights. <br>
Mitigation: Fetch lightweight note metadata first, use summaries before full content, and retrieve ASR, OCR, or insight content only when the user's request requires it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fairylong/aispeech-ainote) <br>
- [AIWork service](https://aiworks.cn) <br>
- [API reference](api_reference.md) <br>
- [API details](references/api-details.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP API endpoints, JSON request and response examples, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIWORK_AUTH_TOKEN for protected API access; content retrieval should be incremental and write or delete actions should identify the exact target before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
