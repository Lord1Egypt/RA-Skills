## Description:

Inspects Alibaba Cloud ECS instance health for memory, disk, CPU, load, and resource-leak anomalies, and can trigger deeper SysOM diagnosis for critical memory issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to inspect Alibaba Cloud ECS instances, triage health anomalies, and obtain SysOM diagnosis reports for routine operations, troubleshooting, and risk warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unverified remote installer as root.

Mitigation: Review the installer out of band or replace it with a pinned, verified package before installation.

Risk: The inspection workflow can activate SysOM, install an agent on ECS, call cloud diagnosis APIs, and save local inspection reports.

Mitigation: Run with least-privilege Alibaba Cloud credentials and confirm service activation, agent installation, and local report storage are intended.

Risk: Region-wide mode can inspect a broad set of ECS instances.

Mitigation: Use focused or batch inspection unless region-wide inspection is explicitly authorized and intended.

## Reference(s):

- [RAM Policies](artifact/references/ram-policies.md)
- [Inspection Report Template](artifact/references/report-template.md)
- [Skill Manifest](artifact/references/manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI-readable text or JSON, with Markdown inspection reports saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include inspection conclusions, diagnosis results, report file paths, replay commands, and copy-ready deep-dive commands.]

## Skill Version(s):

0.0.5 (source: server release metadata and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
