## Description: <br>
Access Fireflies.ai meeting transcripts, summaries, action items, and analytics via GraphQL API <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniil-ctrl](https://clawhub.ai/user/daniil-ctrl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external teams, and developers use this skill to query Fireflies.ai meeting records for transcripts, summaries, action items, contacts, active meetings, and speaking analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose confidential meeting transcripts, summaries, attendee details, contacts, audio, and video through Fireflies API queries. <br>
Mitigation: Use a tightly scoped Fireflies API key where possible, query only the transcript IDs or date ranges needed for the task, and treat all returned meeting data as confidential. <br>
Risk: The skill describes permanent no-login embed links for sharing recordings, which can disclose sensitive meetings externally. <br>
Mitigation: Create or share embed links only for meetings approved for external disclosure and after consent, legal, and company policy requirements are satisfied. <br>


## Reference(s): <br>
- [ClawHub Fireflies Skill Page](https://clawhub.ai/daniil-ctrl/fireflies) <br>
- [Fireflies.ai](https://www.fireflies.ai) <br>
- [Fireflies API Integrations](https://app.fireflies.ai/integrations) <br>
- [Fireflies GraphQL API Endpoint](https://api.fireflies.ai/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, JSON, and HTML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FIREFLIES_API_KEY plus curl and jq for the documented shell workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
