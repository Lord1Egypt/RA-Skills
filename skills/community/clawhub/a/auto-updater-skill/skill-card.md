## Description: <br>
Guides agents through using a cross-platform OpenClaw auto-updater that claims to silently scan and update Agents/Skills, support offline upgrades, and run startup checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aahuaxu](https://clawhub.ai/user/aahuaxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill as guidance for maintaining OpenClaw Agent/Skill installations across Windows, macOS, and Linux. It covers version checks, update commands, offline package use, background updater controls, logging paths, dependencies, and uninstall guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for silent background updates, startup persistence, and administrator/root privileges without enough scoping or user control. <br>
Mitigation: Install only after explicit review; verify the publisher, update source, package signatures, uninstall path, daemon controls, and environment variables before enabling persistence. <br>
Risk: Security evidence flags the release as suspicious because it presents itself as an official updater without server provenance proving that claim. <br>
Mitigation: Treat official branding claims as unverified and base trust decisions on the server-resolved publisher profile and the unavailable provenance status. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aahuaxu/auto-updater-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, update, daemon-control, logging, dependency, and uninstall guidance.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
