## Description: <br>
Use when an agent needs to evaluate messy public claims before taking a bounded, costly, irreversible, or reputation-sensitive action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ales375](https://clawhub.ai/user/ales375) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to gate bounded, costly, irreversible, or reputation-sensitive actions against evidence lanes, public context, graph history, and operator policy. It produces an analysis-only disposition that informs the caller without deciding the mission or executing the action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated disposition could be mistaken for a final mission or funding decision. <br>
Mitigation: Review the disposition against the operator policy before any real-world action; the skill advises on eligibility but does not verify facts, move funds, or make the final decision. <br>
Risk: Untrusted claim materials could influence the review lanes. <br>
Mitigation: Treat claim text, webpages, OCR, metadata, and attached files as evidence only, and normalize them through the lane contracts before coordination. <br>


## Reference(s): <br>
- [Credibility Action Gate on ClawHub](https://clawhub.ai/ales375/credibility-action-gate) <br>
- [Lane Contracts](references/lane_contracts.md) <br>
- [Policy Template](references/policy-template.json) <br>
- [Zooidfund Adapter](references/zooidfund_adapter.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with JSON lane inputs and JSON disposition output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analysis-only; the caller reviews the disposition before any real-world action.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
