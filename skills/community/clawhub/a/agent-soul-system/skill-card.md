## Description: <br>
Create, manage, and validate SOUL.md personality files for multi-agent systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamwgp](https://clawhub.ai/user/adamwgp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create, audit, and maintain SOUL.md files that define agent personalities, responsibilities, collaboration protocols, and output standards for multi-agent systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local scripts can create or update SOUL.md files in the user's agent directory. <br>
Mitigation: Run the scripts manually and back up ~/.openclaw/agents before broad edits. <br>
Risk: Untrusted agent names could create confusing or unintended paths. <br>
Mitigation: Avoid slashes, absolute paths, and traversal-style values when passing agent names. <br>


## Reference(s): <br>
- [Agent Soul System on ClawHub](https://clawhub.ai/adamwgp/agent-soul-system) <br>
- [SOUL.md Template](artifact/references/soul-template.md) <br>
- [Personality Library](artifact/references/personality-library.md) <br>
- [Multi-Agent Collaboration Protocol](artifact/references/collaboration-protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with Python command examples and generated SOUL.md files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local scripts create, list, and validate SOUL.md files under the user's agent directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
