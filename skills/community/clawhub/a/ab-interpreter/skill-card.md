## Description:

Interpret A/B test results for ecommerce campaigns and pages by checking statistical significance, practical effect size, and next-step recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce growth, marketing, and analytics teams use this skill to turn A/B test inputs and results into a concise readout with statistical checks, risk flags, and a ship, kill, extend, or redesign recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can advise shipping, killing, extending, or redesigning tests based on business data.

Mitigation: Review the recommendation and supporting statistics before acting on the readout.

Risk: Incomplete inputs such as missing primary metrics, MDE, guardrails, or segment data can make a readout inconclusive or misleading.

Mitigation: Require missing setup fields to be named in the readout and avoid a ship decision when critical inputs are absent.

## Reference(s):

- [A/B Test Readout Template](references/output-template.md)
- [Choosing the Right Statistical Test](references/statistical-tests.md)
- [Segment Playbook](references/segment-playbook.md)
- [A/B Readout Quality Checklist](assets/ab-readout-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown readout with a verdict, statistics, risk notes, and next step.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided A/B test setup, per-arm results, primary metric, MDE, guardrails, and segment data where available.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
