## Description: <br>
Bootstrap skill for DrawForge that helps an agent find the project repository, follow the intended onboarding documents, run the canonical smoke test, and begin the Visio-based drawing workflow safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qweadzchn](https://clawhub.ai/user/qweadzchn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to onboard into DrawForge, validate a local Visio bridge workflow, and start reproducing reference figures as editable Visio assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill points agents to an external GitHub repository and asks them to run Python commands from that repository. <br>
Mitigation: Review or pin the DrawForge repository before executing its scripts. <br>
Risk: The Visio bridge uses a local VISIO_BRIDGE_TOKEN for bridge-backed smoke tests and execution flow. <br>
Mitigation: Set VISIO_BRIDGE_TOKEN only when intentionally using a trusted local Visio bridge. <br>


## Reference(s): <br>
- [DrawForge GitHub repository](https://github.com/qweadzchn/DrawForge) <br>
- [ClawHub skill page](https://clawhub.ai/qweadzchn/drawforge-agent-visio-use) <br>
- [Publisher profile](https://clawhub.ai/user/qweadzchn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell and PowerShell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides cloning, reading project documents, setting local bridge configuration, and running smoke-test commands.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
