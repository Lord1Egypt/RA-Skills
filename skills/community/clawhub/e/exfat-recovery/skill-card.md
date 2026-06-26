## Description: <br>
Recover corrupted exFAT USB drives on Windows without formatting by diagnosing boot-region corruption, using chkdsk or TestDisk, and applying prevention steps such as write-cache changes, shutdown flush scripts, and boot-region backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, sysadmins, and support engineers use this skill to triage exFAT USB drives that Windows reports as needing formatting, recover accessible data paths, and apply prevention steps after unexpected shutdown or write-cache corruption. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repair and restore steps can write to raw disks or modify filesystem state. <br>
Mitigation: Stop using the affected drive, avoid formatting, make a sector-level image when data matters, and independently verify the drive letter, PhysicalDrive number, partition offset, and backup file before running write operations. <br>
Risk: The prevention workflow includes persistent privileged Windows automation. <br>
Mitigation: Avoid the SYSTEM scheduled task unless the operator understands how to inspect, secure, and remove it. <br>


## Reference(s): <br>
- [Prevention Scripts Setup](references/prevention-scripts.md) <br>
- [TestDisk](https://www.cgsecurity.org/wiki/TestDisk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with PowerShell command examples and step-by-step recovery guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes administrative Windows commands, registry edits, scheduled-task setup, and raw disk backup or restore examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
