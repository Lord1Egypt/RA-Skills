## Description: <br>
Calls a custom summary API to process user-provided text and return the API result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heqq-github](https://clawhub.ai/user/heqq-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they explicitly need to summarize, extract key points from, or otherwise process supplied text through the configured custom API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided text is forwarded to an external API and may be visible to the API operator or in server logs. <br>
Mitigation: Use the skill only with non-sensitive text and only when the external API operator and runtime environment are trusted. <br>
Risk: The backend API can fail or return unexpected results. <br>
Mitigation: Preserve explicit failure responses and review returned summaries before relying on them for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heqq-github/custom-api-summary) <br>
- [Configured summary API endpoint](https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, JSON] <br>
**Output Format:** [JSON response containing success status and either the API result or an error message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires non-empty content input and returns a failure message instead of fabricating results when the backend API fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
