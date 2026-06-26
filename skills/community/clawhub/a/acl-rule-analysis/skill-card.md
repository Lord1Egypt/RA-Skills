## Description: <br>
Vendor-agnostic ACL and firewall rule analysis with shadowed rule detection, overly permissive rule identification, unused rule discovery, redundant rule flagging, and rule ordering optimization for ACLs and firewall policies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vahagn-madatyan](https://clawhub.ai/user/vahagn-madatyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, network engineers, and security reviewers use this skill to inspect ACLs and firewall policies for shadowed, overly permissive, unused, redundant, or poorly ordered rules. It supports cleanup, compliance preparation, incident investigation, migration validation, and rulebase optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Counter-reset commands can change network device state and erase hit-count evidence even when presented alongside read-only audit commands. <br>
Mitigation: Do not run clear access-list or counter-reset commands unless resetting counters is intentional, approved through change control, and current hit-count evidence has been preserved. <br>
Risk: Rule cleanup or ordering recommendations can alter effective network access if applied without validation. <br>
Mitigation: Treat remediation output as review guidance; validate proposed changes with policy simulation or test traffic and apply them only through approved operational change procedures. <br>


## Reference(s): <br>
- [ACL and Firewall Rule Analysis - Multi-Vendor CLI Reference](references/cli-reference.md) <br>
- [Rule Analysis Patterns - Detection Logic and Algorithms](references/rule-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/vahagn-madatyan/acl-rule-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands, tables, and remediation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include prioritized findings, rule identifiers, severity labels, and recommended remediation actions.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
