## Description:

Helps an agent evaluate Chinese creator, OPC, and one-person-business benchmarks by separating business signal from surface appeal, identifying copyable layers, and deciding whether deeper case research is worthwhile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cellinlab](https://clawhub.ai/user/cellinlab)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, operators, and advisors use this skill to decide whether a creator, OPC, or one-person-business benchmark is worth studying, what layer is worth copying, and whether to move into deeper case research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Chinese-first default may produce output in the wrong language for users expecting another language.

Mitigation: Ask for the desired response language when it is unclear, and override the default when the user requests another language.

Risk: Broad activation wording may apply the workflow to unrelated general research tasks.

Mitigation: Confirm the task is about evaluating a creator, OPC, one-person business, or content-led business benchmark before applying the filter.

Risk: The skill can overstate benchmark value if public attention is mistaken for business strength.

Mitigation: Require economic signal, model legibility, and copyable mechanism checks before recommending deeper research or imitation.

## Reference(s):

- [五层筛选框架](references/filter-framework.md)
- [模仿颗粒度检查](references/copy-granularity.md)
- [对标筛选卡](assets/benchmark-card-template.md)
- [ClawHub skill page](https://clawhub.ai/cellinlab/skills/cell-benchmark-filter)
- [Server metadata homepage](https://github.com/cellinlab/cell-skills/tree/main/skills/benchmark-filter)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown benchmark-filter card in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a one-line judgment, five-filter results, worth-learning layers, do-not-copy layers, a first move, and an escalation recommendation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
