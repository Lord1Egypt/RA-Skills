## Description: <br>
Reduce LLM API token consumption by 20-35% through pre-send estimation, memory extraction, and context compression. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[playdadev](https://clawhub.ai/user/playdadev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to reduce model token usage and cost by estimating request size, extracting reusable memory, and compressing older conversation context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected conversation facts may be saved into local memory files or processed by a secondary model. <br>
Mitigation: Avoid secrets, regulated data, and confidential project details unless memory location, access, retention, and deletion rules are defined. <br>
Risk: Aggressive truncation or compression can omit context that affects later agent decisions. <br>
Mitigation: Keep recent messages in full fidelity, preserve decisions and constraints in summaries, and review compressed context before relying on it for sensitive work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/playdadev/claude-code-api-optimizer-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/playdadev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance, configuration] <br>
**Output Format:** [Markdown guidance with token-estimation formulas, compression patterns, memory-file conventions, and JSON prompt examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill with no runtime dependencies; outputs depend on the agent applying the documented optimization rules.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
