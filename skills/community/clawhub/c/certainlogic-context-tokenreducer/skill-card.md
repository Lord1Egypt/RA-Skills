## Description: <br>
CertainLogic Context Manager helps agents manage long sessions by counting turns, warning at a threshold, writing a dense handoff file before reset, and loading recent handoffs when a new session starts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certainlogicai](https://clawhub.ai/user/certainlogicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to keep long OpenClaw-based sessions lean, preserve actionable task state across /new resets, and reduce token-cost growth from accumulated conversation history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plaintext handoff.md files may contain secrets, customer data, personal information, or sensitive project details. <br>
Mitigation: Install only in workspaces where plaintext handoff files are acceptable, review or delete handoff.md when sensitive details may be present, and prefer explicit /handoff use if automatic topic-switch saves are too broad. <br>
Risk: Automatic topic-switch handoffs can save broader session context than the user intended. <br>
Mitigation: Configure deployments to use explicit handoff commands or a conservative topic-switch policy when users handle sensitive work. <br>


## Reference(s): <br>
- [Handoff Format Specification](references/handoff-format.md) <br>
- [Token Math Reference](references/token-math.md) <br>
- [ClawHub Release Page](https://clawhub.ai/certainlogicai/certainlogic-context-tokenreducer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown and plain-text operational guidance with inline command names and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local plaintext session_query_count.txt and handoff.md files when the host agent follows the skill instructions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
