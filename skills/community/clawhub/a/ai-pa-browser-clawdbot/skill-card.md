## Description: <br>
Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to automate multi-step browser workflows, interact with pages through stable accessibility references, and manage browser sessions, saved state, and recordings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can operate authenticated sessions and create sensitive saved state, auth files, recordings, or session files. <br>
Mitigation: Prefer isolated sessions, protect saved state and auth files like credentials, avoid committing them, and delete recordings or session files when they are no longer needed. <br>
Risk: JavaScript evaluation and network routing can affect page behavior on untrusted sites. <br>
Mitigation: Use eval and network routing only on trusted sites and review browser actions before execution. <br>


## Reference(s): <br>
- [Agent Browser homepage](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser command reference](references/commands.md) <br>
- [Agent Browser examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The referenced CLI can emit JSON snapshots and save browser state, screenshots, PDFs, and recordings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
