## Description:

Analyze a US stock using a value investing checklist and output detailed scoring steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kristian-zf](https://clawhub.ai/user/kristian-zf)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to score a U.S. stock from user-supplied metrics against a simple value investing checklist and review the rating rationale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The stock rating may be misleading if the supplied metrics are stale, incomplete, or incorrect.

Mitigation: Verify all input metrics from trusted financial sources before using the checklist output.

Risk: Users may mistake the checklist score for financial advice.

Mitigation: Present the output as a lightweight screening aid and require human financial review before investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kristian-zf/skills/ai-investing-assistant-with-framework)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON object with ticker, rating, reasons, and note.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only user-provided metrics; missing metrics are reported in the output.]

## Skill Version(s):

0.1.0 (source: frontmatter, skill.yaml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
