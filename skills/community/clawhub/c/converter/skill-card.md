## Description: <br>
Converter identifies safe local routes for document, image, audio, video, archive, and data conversions, prioritizing fidelity, privacy, and host-provided toolchains over cloud uploads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIsearch](https://clawhub.ai/user/AGIsearch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and file-heavy users use this skill to choose and run local conversion routes while understanding fidelity, compatibility, privacy, and tool availability tradeoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local conversion commands and batch operations can affect files, paths, wildcards, and output locations. <br>
Mitigation: Review proposed commands, paths, wildcards, and destinations before execution, and keep backups for important files. <br>
Risk: Some conversion routes are lossy, partially reliable, or structurally reconstruct content rather than preserving it exactly. <br>
Mitigation: Use the route analysis and fidelity notes to confirm acceptable quality loss before converting. <br>
Risk: External services may expose file contents if used for unsupported conversions. <br>
Mitigation: Use local toolchains by default and approve external services only when file sharing is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AGIsearch/converter) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/AGIsearch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown route analysis with fidelity notes and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute or propose local commands only when required host binaries are available; otherwise returns a fallback plan.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
