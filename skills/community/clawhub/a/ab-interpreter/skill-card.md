## Description: <br>
Interpret A/B test results for ecommerce campaigns and pages by checking statistical significance, practical effect size, and next-step recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce, growth, and analytics teams use this skill to turn A/B test inputs into a concise ship, kill, extend, or redesign recommendation with statistical, practical, segment, and guardrail checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A readout can be misleading when required setup, sample, metric, segment, or guardrail data is missing or inaccurate. <br>
Mitigation: Require the skill to name missing inputs, classify weak evidence as inconclusive, and keep a human reviewer responsible for rollout decisions. <br>
Risk: A/B test exports may include sensitive user-level revenue or segment data. <br>
Mitigation: Provide only the data needed for the readout and anonymize user-level revenue or segment data where possible. <br>
Risk: Server evidence reports overbroad capability tags that do not match the markdown-only behavior. <br>
Mitigation: Treat the capability tags as needing publisher correction and rely on the security summary when assessing execution, purchase, credential, or data-movement risk. <br>


## Reference(s): <br>
- [A/B Test Readout Template](references/output-template.md) <br>
- [Choosing the Right Statistical Test](references/statistical-tests.md) <br>
- [Segment Playbook](references/segment-playbook.md) <br>
- [A/B Readout Quality Checklist](assets/ab-readout-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown readout with verdict, statistics, risk, and next step] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided A/B test setup, metric, sample, segment, and guardrail data; no code execution or credential access is indicated.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
