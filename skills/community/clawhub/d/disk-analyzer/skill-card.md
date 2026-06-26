## Description: <br>
Duf - duf - Disk Usage/Free analyzer. Automated tool for duf tasks. Use when you need Duf capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local disk usage, find large files, identify duplicate candidates, monitor disk usage changes, and export disk reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Disk reports can expose sensitive file names, mount points, or private project paths. <br>
Mitigation: Run the skill on specific directories where possible and review reports before sharing command output. <br>
Risk: Broad scans can traverse large parts of the local filesystem and produce noisy or sensitive results. <br>
Mitigation: Prefer scoped paths for usage, top-file, duplicate, and monitoring commands. <br>


## Reference(s): <br>
- [muesli/duf reference project](https://github.com/muesli/duf) <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain1/disk-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text, Markdown, or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include local file names, mount points, and private project paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
