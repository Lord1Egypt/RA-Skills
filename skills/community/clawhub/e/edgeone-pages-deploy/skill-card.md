## Description: <br>
Deploy frontend and full-stack projects to Tencent EdgeOne Pages, including login guidance, preview or production deploy commands, and deployment URL extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentism](https://clawhub.ai/user/vincentism) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy frontend or full-stack projects to EdgeOne Pages, choose the correct China or Global site, authenticate, and return the resulting deployment and console URLs. <br>

### Deployment Geography for Use: <br>
Global, with China and Global EdgeOne site selection as required by the EdgeOne workflow. <br>

## Known Risks and Mitigations: <br>
Risk: Complete EdgeOne deployment URLs can contain eo_token and eo_time query parameters that grant access and may be exposed in chat logs, issue trackers, screenshots, or shared transcripts. <br>
Mitigation: Treat any URL containing eo_token or eo_time as sensitive; share it only with intended recipients and avoid posting it in public logs, tickets, or screenshots. <br>
Risk: The skill may save an EdgeOne API token locally in plaintext under .edgeone/.token. <br>
Mitigation: Save tokens only with explicit user consent, keep .edgeone/.token in .gitignore, limit local file access, and rotate or delete the token when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vincentism/edgeone-pages-deploy) <br>
- [EdgeOne Pages China console](https://console.cloud.tencent.com/edgeone/pages?tab=settings) <br>
- [EdgeOne Pages Global console](https://console.intl.cloud.tencent.com/edgeone/pages?tab=settings) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and deployment URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include complete EdgeOne deployment URLs, console URLs, project IDs, login choices, and token-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
