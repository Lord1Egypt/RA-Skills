## Description:

Measure information entropy and redundancy in agent group communications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roamer-remote](https://clawhub.ai/user/roamer-remote)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to quantify entropy, redundancy, mutual information, and knowledge overlap in multi-agent communications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Malformed or unusual input may crash a report or produce incorrect overlap metrics.

Mitigation: Review outputs before using them for operational decisions and test the skill with representative message categories and topic sets before deployment.

Risk: Untrusted category names may trigger robustness issues until Set-handling and prototype-key bugs are fixed.

Mitigation: Normalize or constrain category and topic names from untrusted sources before analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roamer-remote/skills/agent-entropy-meter)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance and JavaScript API output, including text reports with ASCII bar charts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local entropy, redundancy, mutual information, and knowledge-overlap metrics from provided message categories and topic sets.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
