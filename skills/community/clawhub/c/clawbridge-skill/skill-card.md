## Description: <br>
Transforms goals into nightly searches that find, rank, and summarize candidate professional connections with evidence and outreach drafts for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moltlife](https://clawhub.ai/user/moltlife) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and teams use this skill to run recurring public web and community scouting for professional contacts, then review evidence-backed candidate briefs and outreach drafts before taking action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring web and community scouting can collect or summarize personal or sensitive information beyond the intended contact-discovery purpose. <br>
Mitigation: Use strict search, fetch, and time budgets; avoid collecting sensitive personal data; and keep searches limited to approved public venues. <br>
Risk: Generated candidate matches or outreach drafts may be inaccurate, weakly evidenced, or inappropriate for the target relationship. <br>
Mitigation: Review every match, evidence URL, ranking rationale, and draft manually before contacting anyone. <br>
Risk: The skill may surface people or organizations that should not be contacted. <br>
Mitigation: Maintain current avoid lists and enforce human-in-the-loop review; do not auto-send outreach. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/moltlife/clawbridge-skill) <br>
- [Skill source documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Connection Briefs as structured JSON and human-readable Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes candidate evidence, ranking signals, risk flags, and outreach drafts for manual review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
