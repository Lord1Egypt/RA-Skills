## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeytbuilds](https://clawhub.ai/user/joeytbuilds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate browser workflows through the agent-browser CLI, including navigation, ref-based interaction, session isolation, state persistence, screenshots, PDFs, network inspection, and storage operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can submit forms, change account data, or perform actions on authenticated sites. <br>
Mitigation: Use the skill only on sites and accounts the user is authorized to automate, and review actions before submitting forms or changing account data. <br>
Risk: Saved authentication state, cookies, storage data, screenshots, PDFs, and network outputs may contain sensitive information. <br>
Mitigation: Protect generated browser-state and capture files as sensitive data, and avoid storing or sharing them beyond the intended workflow. <br>
Risk: The skill depends on the external agent-browser npm package. <br>
Mitigation: Install and run the external package only when its source and distribution channel are trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/joeytbuilds/agent-browser-jt) <br>
- [agent-browser project homepage](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is centered on the external agent-browser CLI and its compact JSON outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
