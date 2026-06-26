## Description: <br>
Structural documentation for the brand-marketing-workflow skill that helps users understand, audit, or review the workflow design without exposing implementation code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, brand teams, and agent developers use this skill to structure brand inputs into planning, content drafting, competitor review, performance scoring, iteration notes, and approval boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package is advertised as documentation-only, but server security evidence says it ships runnable marketing automation code. <br>
Mitigation: Treat it as runnable automation and review the package before installing or executing it. <br>
Risk: Server security evidence says the skill can read local OpenClaw configuration, use configured LLM or search services, fetch public competitor data, and leave local cache or evidence files. <br>
Mitigation: Install only in environments where those behaviors are acceptable, and verify configured service access, cache handling, and human approval boundaries before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/halfmoon82/brand-marketing-workflow) <br>
- [Skill structural reference](artifact/SKILL.md) <br>
- [Autoresearch optimization notes](artifact/autoresearch.md) <br>
- [Integration test result](artifact/evidence/integration_test_result.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance] <br>
**Output Format:** [Structured JSON workflow results and Markdown-ready brand planning artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit human-assist approval requests when publishing, payment, login, personal-data, or browser-compliance boundaries are reached.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata and artifact clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
