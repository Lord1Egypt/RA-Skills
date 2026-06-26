## Description: <br>
Provides a documentation-only SRE and incident management system for reliability assessment, SLO definition, incident response, chaos engineering, toil management, and production readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1kalin](https://clawhub.ai/user/1kalin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, SREs, platform engineers, and incident responders use this skill to assess service reliability, define SLOs and error budget policies, run incident workflows, draft postmortems, plan chaos experiments, and prepare operational readiness artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Operational remediation examples such as pod deletion, log cleanup, connection termination, and certificate renewal can disrupt production systems if executed without review. <br>
Mitigation: Treat remediation examples as manual, reviewed actions and adapt them to approved runbooks, safeguards, and environment-specific change controls before use. <br>
Risk: Chaos engineering examples intentionally introduce faults and may affect users or reliability targets if run without controls. <br>
Mitigation: Require explicit approval, define blast radius and abort conditions, test in staging where possible, and monitor SLO burn rate before running experiments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1kalin/afrexai-sre-platform) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with YAML templates, checklists, tables, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces documentation and recommendations; remediation examples should be reviewed before use in production.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
