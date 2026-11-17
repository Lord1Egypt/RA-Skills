## Description:

Data Recovery Assistant helps an AI agent diagnose common data loss scenarios, recommend suitable recovery tools and steps, and distinguish SSD and HDD handling guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-jin-xuan](https://clawhub.ai/user/li-jin-xuan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to guide an agent through data recovery triage, including deleted files, formatted disks, missing partitions, RAW partitions, SSD TRIM concerns, and possible drive hardware failure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Disk recovery commands can target the wrong device or write to the failing source disk, causing additional data loss.

Mitigation: Confirm the exact source device before running commands, avoid writes to the source disk, and recover from a clone or disk image where possible.

Risk: Physical drive failure guidance can worsen damage if users keep powering, scanning, or attempting repairs on damaged hardware.

Mitigation: Stop using drives with clicking, non-spinning, water-damaged, or dropped symptoms and use a professional recovery service.

## Reference(s):

- [Data Recovery Fault Reference](references/fault-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/li-jin-xuan/skills/data-recovery-assistant)
- [TestDisk and PhotoRec](https://www.cgsecurity.org/)
- [DMDE](https://dmde.com/)
- [R-Studio](https://www.r-studio.com/)
- [CrystalDiskInfo](https://crystalmark.info/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with diagnostic tables, tool recommendations, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include disk recovery commands that require careful device selection before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
