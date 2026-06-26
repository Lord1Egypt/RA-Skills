## Description: <br>
1688 Shop Health Check helps 1688 merchants assess shop health across core metrics, abnormal products, top products, activity effectiveness, customer geography, and top-customer retention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1688aiinfra](https://clawhub.ai/user/1688aiinfra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
1688 merchants and commerce operators use this skill to run an interactive shop health diagnostic, identify operational risks, and choose focused follow-up analyses for products, traffic, activities, customer geography, and high-value customers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a 1688 AccessKey for shop analytics. <br>
Mitigation: Use a least-privileged or dedicated key and install only when the credential access is acceptable. <br>
Risk: Configuration depends on the intended local gateway endpoint. <br>
Mitigation: Verify OPENCLAW_GATEWAY_URL before running configure. <br>
Risk: Telemetry may be unsuitable for strict privacy environments. <br>
Mitigation: Review and disable telemetry when required by local policy. <br>
Risk: Optimizer handoff cards may trigger downstream optimization workflows. <br>
Mitigation: Treat handoff cards as action requests and confirm downstream optimizer skills separately before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1688aiinfra/1688-shop-health-check) <br>
- [CLI Commands Reference](artifact/references/cli-commands.md) <br>
- [Analysis Methodology](artifact/references/analysis-methodology.md) <br>
- [Interaction Specifications](artifact/references/interaction-specs.md) <br>
- [Visualization Rules](artifact/references/visualization-rules.md) <br>
- [Anti-Patterns](artifact/references/anti-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown diagnostic reports with seller-report JSON visualization blocks and interactive card payloads; CLI commands return JSON with success, markdown, and data fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only analytics commands support diagnostics; configure stores a local 1688 AccessKey configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
