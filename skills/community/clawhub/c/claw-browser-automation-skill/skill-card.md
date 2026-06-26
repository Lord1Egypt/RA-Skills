## Description: <br>
Complete browser automation with agent-browser CLI. Supports navigation, forms, screenshots, data extraction, and parallel sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weaglewang](https://clawhub.ai/user/weaglewang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to drive Chrome or Chromium through the agent-browser CLI for navigation, form workflows, screenshots, data extraction, saved browser state, and parallel browser sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can perform authenticated actions such as form submissions, uploads, purchases, account changes, public posts, or destructive website actions. <br>
Mitigation: Require explicit user approval before performing high-impact or irreversible browser actions. <br>
Risk: Saved browser state files may contain active sessions or other sensitive authentication material. <br>
Mitigation: Treat saved state files like credentials, store them securely, and clear state and cookies after sensitive work. <br>
Risk: The skill relies on an external globally installed npm CLI package. <br>
Mitigation: Install only when the package is trusted and pin or verify the agent-browser package before use. <br>
Risk: Arbitrary browser JavaScript and authenticated fetch calls can expose data or mutate trusted sites. <br>
Mitigation: Use eval and fetch only on user-approved trusted sites and avoid inline real tokens. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/weaglewang/claw-browser-automation-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes browser automation command patterns, setup instructions, troubleshooting guidance, and security guidance.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
