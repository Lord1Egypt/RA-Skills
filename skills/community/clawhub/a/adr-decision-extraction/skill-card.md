## Description: <br>
Extracts architectural decisions from conversations, session transcripts, and design discussions by identifying problem-solution pairs, trade-off debates, technology choices, and explicit [ADR] tags before ADR writing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn planning conversations, transcripts, and design discussions into structured decision records for later ADR writing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted decisions may be inaccurate or treated as formal ADRs before review. <br>
Mitigation: Review extracted decisions, especially [ADR]-tagged and low-confidence items, before using them to write or publish ADRs. <br>
Risk: Source conversations may contain names, client details, credentials, or sensitive internal plans. <br>
Mitigation: Process and share transcripts only when disclosure is intended, and redact sensitive content before distribution. <br>


## Reference(s): <br>
- [Adr Decision Extraction on ClawHub](https://clawhub.ai/anderskev/adr-decision-extraction) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [JSON object containing a decisions array] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each decision includes title, problem, chosen option, alternatives, drivers, confidence, and source context.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
