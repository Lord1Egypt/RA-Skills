## Description: <br>
Self-improvement through conversation analysis that extracts learnings from corrections and success patterns and encodes them into agent definitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mmyg11](https://clawhub.ai/user/mmyg11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to analyze conversations for corrections, successful patterns, and reusable learnings, then propose agent or skill updates for explicit review before applying them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved changes can alter future assistant behavior by updating agent instructions or creating skills. <br>
Mitigation: Review every proposed diff and target file before approval, and keep auto-reflection disabled unless intentionally needed. <br>
Risk: Reflection logs or proposed changes may retain sensitive conversation details. <br>
Mitigation: Avoid approving raw quotes that contain secrets or sensitive project details, and periodically inspect or delete configured reflection state directories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mmyg11/agent-reflect-temp) <br>
- [README.md](artifact/README.md) <br>
- [Signal detection patterns](artifact/signal_patterns.md) <br>
- [Agent mappings reference](artifact/agent_mappings.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with proposed diffs, status summaries, configuration snippets, and review prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write approved learning logs and reflection state to configured project-level or user-level locations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
