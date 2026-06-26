## Description: <br>
Query live traffic data, tracking links, and weekly reports from AnalyticLunch <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dandyer](https://clawhub.ai/user/dandyer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query AnalyticLunch website traffic, review traffic sources and weekly competitive intelligence reports, and create marketing tracking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an AnalyticLunch API key and can access analytics data. <br>
Mitigation: Install it only for trusted agents, use a scoped or revocable key when available, and avoid exposing the key in responses. <br>
Risk: The skill can create tracking links that affect marketing measurement. <br>
Mitigation: Confirm the destination URL, label, and placement before creating a tracking link. <br>


## Reference(s): <br>
- [AnalyticLunch service](https://analyticlunch.com) <br>
- [ClawHub skill page](https://clawhub.ai/dandyer/analyticlunch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and tracking URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AnalyticLunch API key configured at skills.entries.analyticlunch.apiKey.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
