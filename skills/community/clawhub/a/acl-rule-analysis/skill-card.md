## Description:

Vendor-agnostic ACL and firewall rule analysis with shadowed rule detection, overly permissive rule identification, unused rule discovery, redundant rule flagging, and rule ordering optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan)

### License/Terms of Use:

MIT-0

## Use Case:

Network security engineers and operators use this skill to review ACLs and firewall policies, identify risky or ineffective rules, and produce prioritized remediation guidance for rulebase cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is labeled read-only while documenting commands that reset live device counters.

Mitigation: Use accounts restricted to show and export operations, and run counter-reset commands only with separate change-control approval.

Risk: Unused-rule recommendations can be misleading when device counters were recently reset.

Mitigation: Verify device uptime and counter history before treating zero-hit rules as removal candidates.

## Reference(s):

- [ACL and Firewall Rule Analysis - Multi-Vendor CLI Reference](references/cli-reference.md)
- [Rule Analysis Patterns - Detection Logic and Algorithms](references/rule-patterns.md)
- [ClawHub skill page](https://clawhub.ai/vahagn-madatyan/skills/acl-rule-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and analysis tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only collection steps, rule analysis findings, severity classifications, and remediation recommendations.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
