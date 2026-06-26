## Description: <br>
Compares dev, staging, and prod configuration differences and translates technical differences into business risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, release engineers, and operations reviewers use this skill to compare configuration files or directories across environments and turn differences into reviewable risk summaries, alignment recommendations, and verification steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration inputs may include sensitive values or private operational details. <br>
Mitigation: Use copied or scoped configuration files, redact sensitive values before analysis where possible, and review generated reports before sharing. <br>
Risk: The local script can write or overwrite the report file specified by the user. <br>
Mitigation: Choose output paths deliberately and use dry-run or stdout output when reviewing behavior. <br>
Risk: Reports depend on the completeness and accuracy of the provided environment files or text. <br>
Mitigation: Treat generated findings as review drafts and confirm unresolved items before making deployment or configuration changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/env-diff-explainer) <br>
- [README](artifact/README.md) <br>
- [Behavior specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports or JSON payloads with structured risk and verification sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a local report file when an output path is provided; otherwise prints to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
