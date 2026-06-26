## Description: <br>
Provides data-recovery troubleshooting guidance for diagnosing accidental deletion, formatting, partition loss, drive failure, RAW partitions, and choosing SSD or HDD recovery steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[li-jin-xuan](https://clawhub.ai/user/li-jin-xuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support agents, and end users use this skill to triage data-loss scenarios, choose safer next steps, and identify when professional recovery is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Disk-recovery commands or tool guidance can cause additional data loss if run against the wrong drive or directly against a damaged source disk. <br>
Mitigation: Confirm exact drive paths before following commands, avoid writing to the source disk, and work from a disk image where possible. <br>
Risk: Clicking, dropped, water-damaged, or otherwise physically failing drives can worsen if repeatedly powered or opened outside a specialist environment. <br>
Mitigation: Power down physically failing drives and use a professional recovery service for hardware-level failures. <br>


## Reference(s): <br>
- [Data Recovery Fault Reference](references/fault-reference.md) <br>
- [TestDisk and PhotoRec](https://www.cgsecurity.org/) <br>
- [DMDE](https://dmde.com/) <br>
- [R-Studio](https://www.r-studio.com/) <br>
- [CrystalDiskInfo](https://crystalmark.info/) <br>
- [ClawHub Skill Page](https://clawhub.ai/li-jin-xuan/data-recovery-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with diagnostic tables and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides cautious troubleshooting steps and tool recommendations; does not execute recovery commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
