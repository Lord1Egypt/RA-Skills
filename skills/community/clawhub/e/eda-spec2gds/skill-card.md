## Description: <br>
Drive an open-source EDA workflow from spec to GDS using OpenClaw skills, workspace files, and CLI tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[s906903912](https://clawhub.ai/user/s906903912) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and hardware engineers use this skill to turn hardware requirements into structured specifications, RTL, testbenches, synthesis outputs, OpenLane backend runs, GDS artifacts, and report summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional setup and preview paths can make privileged host changes and expose generated local artifacts over the network. <br>
Mitigation: Install or run the skill only in a disposable VM, containerized development environment, or dedicated EDA workstation; review install scripts before execution and avoid shared or production systems. <br>
Risk: Dashboard serving can expose project artifacts to other machines on the network. <br>
Mitigation: Start the dashboard only when artifact exposure is acceptable and prefer changing dashboard binds to 127.0.0.1 before use. <br>
Risk: Tool installation and OpenLane setup may require package downloads, Docker access, and host configuration changes. <br>
Mitigation: Prefer preinstalled tools or manual installation when possible, and review package, Docker, and permission changes before running setup scripts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/s906903912/eda-spec2gds) <br>
- [Security and Safety Guide](references/SECURITY.md) <br>
- [EDA Workflow](references/workflow.md) <br>
- [Specification Template](references/spec-template.md) <br>
- [OpenLane Playbook](references/openlane-playbook.md) <br>
- [Failure Patterns](references/failure-patterns.md) <br>
- [PPA Report Guide](references/ppa-report-guide.md) <br>
- [Ubuntu 24.04 Setup Guide](references/ubuntu-24-setup.md) <br>
- [Demo Walkthrough](references/demo-walkthrough.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with file paths, inline shell commands, generated code, JSON/YAML configuration, and report summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workspace artifacts for staged EDA runs, including RTL, testbenches, logs, reports, PPA JSON, OpenLane configuration, and optional dashboard previews.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
