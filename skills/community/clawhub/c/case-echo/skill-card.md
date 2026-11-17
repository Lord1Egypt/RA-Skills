## Description:

Extract simple structured JSON fields from a short Chinese medical case description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyheya11](https://clawhub.ai/user/heyheya11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and clinical workflow builders can use this skill to convert brief Chinese case summaries into a small JSON object with obvious fields such as sex, age, diagnosis, stage, EGFR, PD-L1, and brain metastasis status. It structures supplied text only and does not provide diagnosis or treatment recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented shell command can allow specially crafted case text to run local shell commands if user text is pasted directly into command text.

Mitigation: Pass case text as data through a structured process API, file, or standard input rather than interpolating or pasting it into a shell command.

Risk: The skill structures medical case text and could be mistaken for clinical interpretation.

Mitigation: Use the JSON output as field extraction only; require human review before using extracted fields in clinical or downstream analysis workflows.

## Reference(s):

- [Sample Chinese case text](examples/sample_case.txt)
- [ClawHub skill page](https://clawhub.ai/heyheya11/skills/case-echo)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Missing fields are returned as null; extracted values should come only from the supplied case text.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
