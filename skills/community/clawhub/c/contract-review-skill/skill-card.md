## Description: <br>
AI-powered contract review that identifies risky clauses, missing provisions, and compliance issues in legal documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to review contract text for risky clauses, missing common provisions, and compliance concerns before routing results to a qualified reviewer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Risk labels may misrepresent safe and risky contracts. <br>
Mitigation: Independently verify scoring thresholds and treat all findings as triage input rather than legal advice. <br>
Risk: Platform metadata includes unrelated high-impact capability tags for crypto and purchases. <br>
Mitigation: Review the capability tags before installation and do not grant unnecessary runtime privileges. <br>
Risk: Generated reports may expose contract names, file paths, and review conclusions. <br>
Mitigation: Store reports only in secure local locations and avoid using the skill for sensitive contracts without appropriate controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/534422530/contract-review-skill) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact manifest](artifact/claw.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Human-readable contract review reports or structured JSON findings with risk scores, issue descriptions, and suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local contract files and can save batch review reports containing contract names, file paths, risk summaries, and review conclusions.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
