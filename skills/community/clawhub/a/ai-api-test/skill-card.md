## Description: <br>
AI API Test helps agents run basic API endpoint checks and write Markdown reports with status, latency, content length, and a short response preview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arthasking123](https://clawhub.ai/user/arthasking123) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to send authorized test requests to API endpoints and receive a local Markdown summary of status code, latency, content length, and response preview. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated report can include a local preview of the API response body. <br>
Mitigation: Run the skill only against APIs you own or are authorized to test, and avoid sensitive endpoints unless local response previews are acceptable. <br>
Risk: The release advertises monitoring, load-testing, and advanced validation features that are not evidenced in the current implementation. <br>
Mitigation: Treat this version as a basic API request/report helper and verify any advanced workflow before relying on it for monitoring, CI/CD gates, or performance testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arthasking123/ai-api-test) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [Markdown report file with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are written locally and may include a short API response preview.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
