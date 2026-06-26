## Description: <br>
Detects and mitigates hallucinations in agent outputs by self-checking facts, verifying claims, and correcting unsupported or contradictory information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tooled-app](https://clawhub.ai/user/tooled-app) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add structured fact-checking, confidence calibration, and correction workflows to LLM-based agents. It is intended for runtime self-monitoring before an agent makes factual claims, reports tool results, or gives recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hallucination correction logs may retain sensitive user data, private file contents, or confidential project details. <br>
Mitigation: Configure or review the memory logging location before use, and redact or avoid retaining sensitive information in correction logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tooled-app/anti-hallucination-skill) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with checklists, protocols, tables, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no code execution or credential handling is described in the security evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
