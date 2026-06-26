## Description: <br>
Battle-Tested Agent provides production-hardened patterns, templates, and a local audit script for improving AI agent reliability across memory, verification, ambiguity handling, compaction survival, delegation, handoffs, stale-worker recovery, and self-improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zurbrick](https://clawhub.ai/user/zurbrick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to audit and harden SKILL.md-based agents for production reliability. It helps teams add concrete mechanisms for verification, context survival, delegation, acceptance gates, and recurring self-improvement without adopting every pattern by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory and self-improvement templates could cause an agent to persist sensitive or incidental personal data if copied into a real workspace unchanged. <br>
Mitigation: Add data-minimization rules before adoption and avoid retaining secrets, credentials, account identifiers, private URLs, health or financial details, or incidental personal data unless explicitly requested. <br>
Risk: Applying every reliability pattern indiscriminately can add unnecessary process overhead. <br>
Mitigation: Run the audit first and adopt only the smallest tier and concrete mechanisms that address the observed failure mode. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zurbrick/battle-tested-agent) <br>
- [Publisher profile](https://clawhub.ai/user/zurbrick) <br>
- [Audit Usage](references/audit-usage.md) <br>
- [Starter Patterns](references/starter-patterns.md) <br>
- [Intermediate Patterns](references/intermediate-patterns.md) <br>
- [Advanced Patterns](references/advanced-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with reusable templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a local bash audit script that checks agent workspaces for reliability patterns.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
