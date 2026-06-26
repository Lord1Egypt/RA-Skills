## Description: <br>
Deep Current is a persistent research thread manager with a local Python CLI for tracking topics, notes, sources, and findings while relying on the host agent's web tools for research and digest generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[madebydia](https://clawhub.ai/user/madebydia) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, researchers, and agent users use Deep Current to maintain long-running research threads, store notes, sources, and findings, and guide scheduled agent research digests over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence marks the reviewed release as suspicious and calls for manual review before installation. <br>
Mitigation: Review the skill and its requested local file writes before installing or scheduling automated runs. <br>
Risk: The workflow can direct an agent to perform recurring web research and write reports, which may preserve inaccurate or stale findings if sources are not checked. <br>
Mitigation: Require source links in reports, cross-reference claims, and review generated findings before acting on them. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/madebydia/deep-current) <br>
- [Project homepage](https://github.com/madebydia/deep-current) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI commands emit plain text and update local JSON data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores thread state in deep-current/currents.json and expects reports in deep-current-reports/ as dated Markdown files.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
