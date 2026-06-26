## Description: <br>
Audit and improve an agent at the right layer: persona/tone, constitutional and operating rules, memory architecture, or skill portfolio / reusable workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent maintainers use this skill to diagnose recurring agent failures and route fixes to the correct layer: persona, rules, memory, or skills. It helps choose the smallest justified change and identify where that patch belongs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may recommend structural agent changes based on insufficient evidence. <br>
Mitigation: Use it as an audit aid and review whether the lane assignment and fix type match the observed problem before applying any patch. <br>
Risk: Daily memory logging may conflict with a workspace's privacy or retention expectations. <br>
Mitigation: Decide whether daily memory logging is acceptable before use and adapt the logging step to local governance. <br>
Risk: A named approval rule may not match the adopting team's authority model. <br>
Mitigation: Replace the named 'Don approval' rule with the appropriate local approval requirement before relying on the placement guidance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zurbrick/agent-architect-zurbrick) <br>
- [Audit Checklist](references/audit-checklist.md) <br>
- [Fix Types](references/fix-types.md) <br>
- [Lane Diagnosis](references/lane-diagnosis.md) <br>
- [Placement Map](references/placement-map.md) <br>
- [Worked Examples](references/worked-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown diagnosis with optional YAML structured output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces recommendations only; it does not apply patches or execute code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
