## Description: <br>
Auto Summarization Loop helps agents manage long conversations with core, working, and long-term memory, dual watermark compression triggers, and structured persona summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhoujj8009](https://clawhub.ai/user/zhoujj8009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building long-running AI chat or persona applications use this skill to keep conversation context within model limits, reduce API cost, and preserve important user facts across turns or sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation summaries and profile facts may retain personal or sensitive user information across turns or sessions. <br>
Mitigation: Define retention, inspection, edit, expiration, and deletion controls before production use, and make the memory behavior clear to users. <br>
Risk: Summary generation may send conversation history to a model provider selected by the implementer. <br>
Mitigation: Choose approved model providers and data handling policies before enabling summarization in production. <br>


## Reference(s): <br>
- [Summary Prompt Templates](references/summary_prompts.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhoujj8009/auto-summarization-loop) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with Python code examples and JSON-oriented summary templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces memory-management guidance, Python helper code, prompt templates, and integration examples for conversation summarization workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
