## Description: <br>
Business Rule Engine helps agents define, load, chain, and evaluate lightweight business rules for dynamic logic execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to define and exercise business rules, rule chains, and JSON-loaded policies for application workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rule text is evaluated as Python code without clear containment. <br>
Mitigation: Install and use only with trusted rule definitions and trusted rule authors; replace eval-based execution with a restricted parser or allowlisted evaluator before using customer-supplied, third-party, or remotely loaded rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/business-rule-engine) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces rule definitions, rule-chain examples, JSON loading examples, and test commands; generated or loaded rules should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
