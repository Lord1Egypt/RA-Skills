## Description:

Expert2Skill guides a domain expert through a structured interview, converts the expert's judgment method into rule_library JSON, and packages it as a local runnable evaluation skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, consultants, and domain experts use this skill to turn an expert's evaluation criteria into a structured rules JSON file and a local skill package. It is suited to rule-based assessment workflows where the expert remains the authority for thresholds, scoring, and non-rule-based judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packager can generate executable Python from user-controlled rule-library metadata.

Mitigation: Use only trusted rule-library JSON, inspect generated Python before execution or sharing, and avoid packaging third-party rules until slug validation and safe source generation are fixed.

Risk: The packager can write outside the intended output directory.

Mitigation: Run packaging only in a controlled empty output directory and verify the generated package path before executing or uploading files.

Risk: Generated skills may contain proprietary methods or sensitive personal data from the expert interview.

Mitigation: Treat publication as optional and inspect generated files before any ComplianceHub or ClawHub upload.

## Reference(s):

- [Interview Guide](artifact/references/interview-guide.md)
- [rule_library Schema v2](artifact/references/rule-library-schema-v2.md)
- [Stock Materials Reference](artifact/references/stock-materials-reference.md)
- [Sample Nutrition Rule Library](artifact/references/sample-nutrition.json)
- [Sample Value Investor Rule Library](artifact/references/sample-value-investor.json)
- [ClawHub Skill Page](https://clawhub.ai/wwumit/skills/expert2skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, rule_library JSON, generated Python skill-package files, package metadata, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated evaluator packages are described as local, zero-network, zero-third-party-dependency Python skills that can emit text reports and JSON scores.]

## Skill Version(s):

1.0.2 (source: evidence release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
