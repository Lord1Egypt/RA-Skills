## Description: <br>
Access Gevety health data including biomarkers, healthspan scores, biological age, wearable metrics, supplements, medications, lab reports, health documents, clinical findings, and health content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moclippa](https://clawhub.ai/user/moclippa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to let an agent retrieve and summarize their Gevety health account data through authenticated API calls. It supports health-data review, biomarker trend analysis, wearable summaries, protocol tracking, and document lookup while requiring users to consult healthcare professionals for medical decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve sensitive health data from a user's Gevety account. <br>
Mitigation: Install it only for intended Gevety account access and ask the agent to retrieve the minimum health data needed for the task. <br>
Risk: The skill requires a bearer token that can authorize access to Gevety account data. <br>
Mitigation: Use a dedicated Gevety API token, keep it out of chat where possible, and revoke it when no longer needed. <br>
Risk: Health summaries, trends, and biological-age outputs may be mistaken for medical advice. <br>
Mitigation: Present outputs as informational data review and consult healthcare providers for medical decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moclippa/gevety) <br>
- [Publisher profile](https://clawhub.ai/user/moclippa) <br>
- [Gevety](https://gevety.com) <br>
- [Gevety API](https://api.gevety.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON, HTTP, JavaScript, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided GEVETY_API_TOKEN and returns health-data summaries based on the user's available Gevety data.] <br>

## Skill Version(s): <br>
1.12.0 (source: server release metadata; artifact frontmatter is 1.11.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
