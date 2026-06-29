## Description: <br>
Axiom Css Specificity calculates CSS selector specificity as (a, b, c) tuples and compares selectors for debugging cascade conflicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and frontend engineers use this skill to debug CSS cascade conflicts, audit selectors for excessive specificity, and compare selectors during refactoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation references compute_specificity for Python imports, but the code exports calculate. <br>
Mitigation: Use calculate for Python imports or verify examples before embedding them in downstream guidance. <br>
Risk: The artifact states limitations for @scope, simplified functional pseudo-class handling, and no !important resolution. <br>
Mitigation: Use a browser or full CSS cascade tool when decisions depend on complete cascade behavior beyond selector specificity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/axiom-css-specificity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [JSON or plain text specificity results with markdown usage guidance and Python or shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deterministic local calculation; no network access or LLM calls are described in the evidence.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
