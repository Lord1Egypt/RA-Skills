## Description:

Drive an open-source EDA workflow from spec to GDS using OpenClaw skills, workspace files, and CLI tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[s906903912](https://clawhub.ai/user/s906903912)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and EDA engineers use this skill to turn hardware requirements into normalized specifications, Verilog RTL and testbenches, ordered lint/simulation/synthesis/OpenLane runs, GDS-related artifacts, and report summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional setup scripts can modify host state through package installation, Docker service setup, Docker group membership, and Python environment changes.

Mitigation: Install or run the skill only in a disposable VM or dedicated EDA machine, review setup scripts before use, and avoid permanent Docker group membership where possible.

Risk: Package and Docker image downloads introduce supply-chain and reproducibility risk.

Mitigation: Review network destinations, pin package versions and Docker images by digest, and use trusted mirrors or pre-approved images.

Risk: EDA specifications, RTL, logs, reports, and GDS outputs may contain sensitive design information.

Mitigation: Treat generated artifacts as sensitive, keep dashboards bound to localhost, and do not expose artifact servers outside the local environment.

Risk: OpenLane and related EDA runs can consume significant CPU, memory, disk, and Docker image storage.

Mitigation: Run in a resource-limited environment, monitor disk usage, and clean up Docker images and generated run directories after review.

## Reference(s):

- [Security and Safety Guide](references/SECURITY.md)
- [EDA Workflow](references/workflow.md)
- [OpenLane Playbook](references/openlane-playbook.md)
- [Specification Template](references/spec-template.md)
- [Failure Patterns](references/failure-patterns.md)
- [PPA Report Guide](references/ppa-report-guide.md)
- [Ubuntu 24.04 Setup Guide](references/ubuntu-24-setup.md)
- [Demo Walkthrough](references/demo-walkthrough.md)
- [Dashboard Plan](references/dashboard-plan.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with inline shell commands, JSON/YAML configuration, Verilog code, logs, reports, and workspace artifact paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce normalized specifications, RTL, testbenches, OpenLane configuration, PPA summaries, dashboards, and optional GDS preview artifacts.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
