## Description: <br>
Extract health and fitness data from Garmin Connect including activities, sleep, heart rate, stress, steps, and body composition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[garrza](https://clawhub.ai/user/garrza) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use Garmer to retrieve Garmin Connect health and fitness data through CLI commands or a Python API for personal analysis, health insight workflows, and assistant integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Garmer handles sensitive Garmin Connect tokens and health-data exports. <br>
Mitigation: Treat saved tokens and exported JSON files as sensitive data, avoid broad exports unless needed, and delete tokens with `garmer logout` when access is no longer required. <br>
Risk: `garmer update` can change local package code from the configured git remote. <br>
Mitigation: Run updates only from trusted package sources and review the configured source before changing local code. <br>


## Reference(s): <br>
- [Garmer API Reference](references/REFERENCE.md) <br>
- [Garmer README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell and Python examples; CLI commands can produce JSON health-data exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Garmin Connect authentication and may read saved tokens or exported local health data.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; artifact frontmatter and pyproject.toml report 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
