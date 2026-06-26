## Description: <br>
OpenClaw Security Guard helps agents run lightweight local checks for prompt injection, secrets, risky commands, suspicious URLs, sensitive paths, and skill-folder publish or install risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[X-RayLuan](https://clawhub.ai/user/X-RayLuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and agent operators use this skill to preflight untrusted text, commands, URLs, paths, and third-party skill folders before installation, automation, or publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lightweight local checks can miss unsafe behavior or produce findings that still need context. <br>
Mitigation: Use the results as a preflight signal, then manually review WARN or BLOCK findings before trusting, installing, or publishing a skill. <br>
Risk: Generated audit JSON or markdown notes may include excerpts from scanned files. <br>
Mitigation: Treat generated reports as sensitive when the scanned input may contain secrets, private paths, or proprietary content. <br>
Risk: The hook installer creates a persistent local prepublish helper. <br>
Mitigation: Run the installer only when a persistent local helper is intended and the target workspace path is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/X-RayLuan/clawlite-openclaw-security-guard) <br>
- [Security Guard Checklist](references/checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON audit output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local audit notes or a prepublish helper when the user runs the relevant script.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
