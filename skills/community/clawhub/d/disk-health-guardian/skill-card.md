## Description: <br>
Catch Disk Failures Before Disaster -- Advanced bad sector detection and SMART diagnostics that catch disk problems before you lose your data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hezhaoyun](https://clawhub.ai/user/hezhaoyun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support agents use this skill to guide Windows disk-health triage, including SMART checks, bad-sector scans, file-system validation, and preflight checks before disk operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to silently install and run a powerful third-party disk management tool with elevated privileges. <br>
Mitigation: Install only if the publisher and EaseUS are trusted; prefer the vendor download path, verify the installer signature, and approve elevation only when the installation is intentional. <br>
Risk: Disk and partition tools can affect data if users go beyond read-only health checks. <br>
Mitigation: Back up important data first, confirm the target disk, review any operation preview, and stay within SMART or health checks unless a disk change is deliberate. <br>


## Reference(s): <br>
- [EaseUS Partition Master](https://www.easeus.com/partition-manager/) <br>
- [EaseUS Partition Master Free Download](https://down.easeus.com/product/epm_free?source=skills&dest=disk-health-guardian) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with Windows command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, launch, troubleshooting, and validation guidance for Windows disk-health workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
