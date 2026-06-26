## Description: <br>
Aispeech Ainote lets OpenClaw agents access Aispeech office notebook and recording-card notes, todos, labels, personal knowledge search, and hotword APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fairylong](https://clawhub.ai/user/fairylong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query and manage Aispeech office notes, todos, labels, personal knowledge search, and hotword content through OpenClaw. It is intended for workflows around AI office notebooks and recording-card products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify personal notes, todos, labels, hotwords, and knowledge-search results. <br>
Mitigation: Grant only the scopes needed for the intended workflow and manually confirm the exact item before deletes, moves, syncs, binding changes, or other write operations. <br>
Risk: The skill requires an AIWORK_AUTH_TOKEN and documents a fallback that can read a saved local token file. <br>
Mitigation: Prefer OpenClaw-managed per-skill secret injection, avoid relying on the local token-file export fallback, and protect any stored token from shell history, logs, and shared workspaces. <br>
Risk: Office notes, todos, labels, and knowledge-search content may contain sensitive personal or business information. <br>
Mitigation: Install only when the publisher and connected Aispeech service are trusted for the intended data, and avoid using the skill with confidential content outside approved environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fairylong/aitablet) <br>
- [Publisher profile](https://clawhub.ai/user/fairylong) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [API reference](api_reference.md) <br>
- [API details](references/api-details.md) <br>
- [AIWorks service](https://aiworks.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API endpoint details, JSON request and response examples, shell commands, and OpenClaw configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIWORK_AUTH_TOKEN and optionally AIWORK_BASE_URL; API responses use JSON with code, message, and data fields.] <br>

## Skill Version(s): <br>
1.0.9 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
