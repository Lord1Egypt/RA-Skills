## Description:

Evidence-Based Medicine calculator for sensitivity, specificity, PPV, NPV, NNT, and likelihood ratios for clinical decision making and biostatistics education.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, clinicians, and educators can use this skill to calculate common evidence-based medicine statistics from command-line inputs and receive structured JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional file output can overwrite arbitrary writable paths.

Mitigation: Use --output only with a safe, intended relative path in a disposable or controlled workspace, and avoid elevated filesystem permissions.

Risk: Clinical input validation is weak, so results can be misleading when inputs are invalid or not clinically appropriate.

Mitigation: Validate all inputs externally and treat outputs as calculation assistance rather than clinical advice.

## Reference(s):

- [EBM Calculator References](artifact/references/guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/ebm-calculator)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON results printed to stdout or written to an optional output file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external dependencies or network access are described; optional file output writes JSON to a user-provided path.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
