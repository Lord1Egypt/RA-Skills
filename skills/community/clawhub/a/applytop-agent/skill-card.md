## Description: <br>
ApplyTop is a CLI and Node client for the ApplyTop public API that helps users search jobs and access alerts, matches, saved jobs, and CVs, including AI ATS scoring, CV tailoring, and cover-letter generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shman2000](https://clawhub.ai/user/shman2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation builders, and ApplyTop users use this skill to install and operate the ApplyTop CLI or Node client for job search workflows, account data access, CV management, and AI-assisted resume or cover-letter tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ApplyTop CLI can access ApplyTop account data and CVs when used with an API key. <br>
Mitigation: Install and run it only if you trust the ApplyTop service and npm package, and prefer APPLYTOP_API_KEY or logout when credentials should not remain in the saved credentials file. <br>
Risk: AI CV tailoring, cover-letter generation, and ATS scoring consume ApplyTop credits charged to the key owner. <br>
Mitigation: Check the credit balance before running credit-consuming commands and confirm the intended account owns the active API key. <br>
Risk: Using the development-only insecure TLS option could weaken transport security. <br>
Mitigation: Avoid the insecure option for production API calls and use the default ApplyTop HTTPS endpoint. <br>


## Reference(s): <br>
- [ApplyTop](https://applytop.com) <br>
- [ApplyTop API keys](https://applytop.com/dashboard/api-keys) <br>
- [Source repository](https://github.com/shman2000/applytop-agent) <br>
- [ClawHub skill listing](https://clawhub.ai/shman2000/applytop-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands and examples produce JSON responses from the ApplyTop CLI or Node client.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
