## Description: <br>
Provides a local Markdown-file memory workflow that helps an AI agent maintain session state, daily logs, and long-term summaries without external APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to give an AI agent a lightweight local memory protocol for recording active context, decisions, preferences, and daily logs in workspace files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persists conversation details in local files, which can retain secrets or sensitive personal data. <br>
Mitigation: Avoid storing secrets or sensitive personal data; review and delete SESSION-STATE.md, MEMORY.md, and memory/ entries when retention is no longer wanted. <br>
Risk: The release requests shell execution even though the evidence describes a pure Markdown, local-file workflow. <br>
Mitigation: Install with read/write-only permissions where possible and grant shell execution only if the publisher documents a specific need. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/elite-longterm-memory-local-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions and local memory file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local memory files such as SESSION-STATE.md, MEMORY.md, and memory/YYYY-MM-DD.md when followed by an agent.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
