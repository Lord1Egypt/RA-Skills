## Description: <br>
Monitor, report, and get AI-generated fixes for JavaScript and TypeScript production errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hankmint](https://clawhub.ai/user/hankmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use Codemend to add JavaScript and TypeScript error monitoring, report production errors, check analysis status, and retrieve AI-generated fix guidance or pull request links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script contacts an unexpected AutoHeal domain and uses AUTOHEAL_API_KEY instead of the documented Codemend API key. <br>
Mitigation: Review or disable scripts/check-errors.sh unless the publisher explains or fixes the AutoHeal domain and API key mismatch. <br>
Risk: Production error monitoring can send stack traces, source URLs, and other application error data to an external service. <br>
Mitigation: Treat API keys as secrets, redact sensitive stack traces and URLs, and confirm privacy and compliance requirements before enabling automatic production capture. <br>


## Reference(s): <br>
- [Codemend skill page](https://clawhub.ai/hankmint/codemend) <br>
- [Codemend homepage](https://codemend.ai) <br>
- [OpenClaw registry](https://github.com/anthropics/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with shell commands, code snippets, and JSON API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CODEMEND_API_KEY; responses may include error IDs, status values, fix prompts, dashboard URLs, and pull request URLs.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
