## Description: <br>
Runs nightly searches to identify and rank relevant candidates matching your offer and ask, delivering evidence-backed connection briefs for human review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moltlife](https://clawhub.ai/user/moltlife) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agencies, business development teams, and founders use this skill to find public-web connection opportunities, rank candidates, and prepare evidence-backed outreach drafts for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs recurring public-web prospect research that may involve privacy-sensitive targeting decisions. <br>
Mitigation: Keep secrets and sensitive internal targeting strategy out of profiles, restrict inputs to public business information, and review each candidate before outreach. <br>
Risk: Outreach drafts could be mistaken for approved messages or used for unsolicited automatic contact. <br>
Mitigation: Maintain the documented human-in-the-loop workflow and do not configure the skill to send messages automatically. <br>
Risk: Public-web results may include stale, weak, or mismatched evidence. <br>
Mitigation: Use the evidence URLs, candidate risk flags, avoid lists, and recency constraints to verify fit before taking action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moltlife/claw-clawbridge) <br>
- [Output schema](schema/connection_brief.json) <br>
- [Sample Markdown brief](examples/sample_run.md) <br>
- [Sample JSON brief](examples/sample_run.json) <br>


## Skill Output: <br>
**Output Type(s):** [json, markdown, text, guidance] <br>
**Output Format:** [Structured JSON run data and human-readable Markdown connection briefs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ranked candidates, evidence URLs, risk flags, suggested outreach drafts, and recommended next actions for human approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
