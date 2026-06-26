## Description: <br>
Teaches ADA how to perform file downloads using the browser tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pbseiya](https://clawhub.ai/user/pbseiya) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and ADA users use this skill to locate webpage download controls and save selected files through OpenClaw browser download commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloaded web files may be untrusted or unsafe to open. <br>
Mitigation: Inspect or scan downloaded files before opening or executing them. <br>
Risk: A chosen download path may overwrite an existing local file. <br>
Mitigation: Check the destination filename before saving and avoid overwriting existing files unless intended. <br>
Risk: A browser selector or JavaScript-triggered click may target the wrong page element. <br>
Mitigation: Use the skill only on sites and files intentionally chosen, and confirm the download control before running the action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pbseiya/browser-download) <br>
- [Publisher profile](https://clawhub.ai/user/pbseiya) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the openclaw CLI and a correctly configured browser gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
