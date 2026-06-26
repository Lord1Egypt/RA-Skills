## Description: <br>
Guides agents through complex application development, CI/CD, and DevOps workflows using staged checklists, validation commands, monitoring templates, and rollback practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smxtx](https://clawhub.ai/user/smxtx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to plan, implement, test, release, monitor, and troubleshoot application changes with structured checklists and helper commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may suggest or run build, deployment, canary, rollback, health-check, or log-inspection commands without enough production scoping. <br>
Mitigation: Review the git diff, package scripts, Docker target, Kubernetes context, namespace, environment, and production authorization before execution. <br>
Risk: The bundled DevOps workflow can affect live services when applied to production or shared infrastructure. <br>
Mitigation: Use the skill as a checklist and script bundle; require explicit user confirmation before deployment, rollback, or environment inspection steps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smxtx/bu-bu-wei-ying) <br>
- [Publisher profile](https://clawhub.ai/user/smxtx) <br>
- [README](README.md) <br>
- [English skill definition](SKILL-en.md) <br>
- [Automation checklist script](scripts/checklist.sh) <br>
- [Grafana alert template](templates/grafana-alerts.json) <br>
- [Datadog alert template](templates/datadog-alerts.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes checklist commands and Grafana/Datadog alert templates; execution should remain user-authorized.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
