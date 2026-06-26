## Description: <br>
Searches the ClawHub Skills marketplace to help agents find and discover OpenClaw community skills by keyword and sorting criteria. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mahongting](https://clawhub.ai/user/mahongting) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent users, and skill marketplace users use this skill to search ClawHub Skills, inspect candidate skill metadata, and generate commands for API-based discovery or optional installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a ClawHub API token for authenticated marketplace requests. <br>
Mitigation: Store CLAWHUB_TOKEN in an environment variable or secret store, and avoid pasting the token into chat or source files. <br>
Risk: Search results may lead users to install or run third-party skills. <br>
Mitigation: Review and scan any discovered skill before installation or execution. <br>
Risk: Marketplace API calls can fail because of missing credentials, access issues, or rate limits. <br>
Mitigation: Check token availability and handle failed or limited API responses before relying on search results. <br>


## Reference(s): <br>
- [Clawhub Search skill page](https://clawhub.ai/mahongting/clawhub-search) <br>
- [ClawHub Skills API](https://clawhub.ai/api/v1/skills) <br>
- [ClawHub Skills marketplace](https://clawhub.ai/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CLAWHUB_TOKEN from the environment for authenticated ClawHub API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
