## Description: <br>
DataGate parses untrusted CSV or JSON through a deterministic tool boundary before model analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alan-stratcraftsai](https://clawhub.ai/user/alan-stratcraftsai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to parse local CSV or JSON files before asking an agent to summarize, inspect, or analyze them. It keeps raw external data separate from trusted instructions and asks the agent to reason over bounded structured output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parsed file paths, sampled values, schema details, and alerts may enter the assistant context. <br>
Mitigation: Avoid using the skill on sensitive exports unless sharing bounded parser output with the assistant is acceptable. <br>
Risk: Bounded previews may omit rows or truncate long values needed for full-fidelity analysis. <br>
Mitigation: Keep default limits for initial inspection, then rerun with purpose-specific limits when more detail is required. <br>
Risk: Instruction-like text alerts are heuristic labels, not proof that a file is malicious. <br>
Mitigation: Describe flagged content as suspicious data and do not silently discard rows or fields based only on the alert. <br>


## Reference(s): <br>
- [Output Schema](references/output-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Analysis] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON parser output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Parser output is bounded by preview row, string length, and input byte limits.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
