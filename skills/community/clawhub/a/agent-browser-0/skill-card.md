## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kdegeek](https://clawhub.ai/user/kdegeek) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation-focused agent users use this skill to drive headless browser sessions for navigation, interaction, form filling, UI testing, page inspection, and structured data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad control over browser sessions, including authenticated pages. <br>
Mitigation: Use isolated browser sessions or test accounts, avoid sensitive sites unless necessary, and review browser actions before they affect real accounts or data. <br>
Risk: Commands can enter credentials, upload files, submit forms, run JavaScript, read cookies or storage, inspect network traffic, and save authentication state. <br>
Mitigation: Require explicit approval before credential entry, file upload, form submission, eval execution, cookie or storage access, network inspection, or saving auth state. <br>
Risk: The skill depends on the upstream agent-browser npm package and local browser automation tooling. <br>
Mitigation: Install only from trusted package sources, keep the CLI updated, and verify command behavior in a non-sensitive environment before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kdegeek/agent-browser-0) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser CLI skill issue tracker](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands may return text, JSON, screenshots, PDFs, video recordings, or saved browser state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm, plus the agent-browser CLI installation described by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
