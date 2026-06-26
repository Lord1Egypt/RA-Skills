## Description: <br>
Analyzes agent execution logs, diagnoses recurring capability gaps, and generates improvement reports, configuration patches, and skill recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to review failed agent tasks, classify root causes, and produce local evolution notes or patch proposals for future behavior. It supports one-time diagnosis and ongoing self-improvement workflows driven by configured execution logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the configured agent log directory, and those logs may contain sensitive task details or credentials. <br>
Mitigation: Configure LOG_DIR to a narrow log location, avoid logs containing secrets, and review access before enabling the skill. <br>
Risk: Generated behavior patches or recommendations may encode incorrect conclusions from incomplete failure logs. <br>
Mitigation: Use conservative or observe_only mode when review is needed, and inspect generated patches before relying on them for future agent behavior. <br>


## Reference(s): <br>
- [Evolution rules reference](references/evolution_rules.md) <br>
- [ClawHub release page](https://clawhub.ai/ai-gaoqian/agent-capability-evolver) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with optional YAML or Markdown patch files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates local analysis reports, rule or default-parameter patch proposals, trigger updates, tool-mapping notes, skill recommendations, and evolution logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
