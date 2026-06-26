## Description: <br>
Api Quick Tester helps developers test REST and GraphQL APIs, generate lightweight test reports, and create mock data from command-line workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Frontend and backend developers use this skill to send quick API requests, check responses, generate mock data, and produce lightweight reports during API development and validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authentication tokens, API keys, or basic-auth credentials may be exposed through command history, terminal output, CI logs, or shared sessions. <br>
Mitigation: Use test credentials or short-lived tokens, avoid placing real secrets directly in command lines, and review logs before sharing them. <br>
Risk: Requests to production endpoints can modify data when using POST, PUT, PATCH, or DELETE. <br>
Mitigation: Confirm the URL and method before executing mutating requests, and prefer test or staging endpoints for validation. <br>
Risk: API response bodies may contain sensitive data that is printed to the terminal. <br>
Mitigation: Treat response output as sensitive and avoid running the tool in shared terminals or persistent logs when testing protected APIs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yang1002378395-cmyk/api-quick-tester) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, JSON mock data, Markdown reports, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can issue HTTP requests to user-specified endpoints and print response bodies.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
