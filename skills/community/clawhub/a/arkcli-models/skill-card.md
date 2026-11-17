## Description:

Guides agents in finding, comparing, and inspecting Volcano Engine Ark public foundation models, checking performance and lifecycle information, and activating model services when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to search, list, compare, and inspect public Ark foundation models, including model capabilities, versions, lifecycle status, and Volc performance metrics. It can activate a model service when requested and provides bounded model lookup for a separate deployment workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes that model inference or service activation sits alongside the stated model-discovery purpose; the review is medium-confidence and incomplete.

Mitigation: Keep activation limited to explicit user requests, confirm the intended model and requested service scope, and review the referenced routing components before relying on the incomplete assessment.

## Reference(s):

- [Scenario-based model recommendations](references/arkcli-models-scenario-table.md)
- [Model search guidance](references/arkcli-models-search.md)
- [Model listing guidance](references/arkcli-models-list.md)
- [Model details and pricing guidance](references/arkcli-models-get.md)
- [Model service activation guidance](references/arkcli-models-activate.md)
- [Model performance guidance](references/arkcli-models-performance.md)
- [Ark Agent Plan model deprecation notice](https://ark.volcengine.com/region:cn-beijing/docs/agent-plan-personal-model-deprecation-announcement)
- [Ark Coding Plan model deprecation notice](https://ark.volcengine.com/region:cn-beijing/docs/coding-plan-personal-model-deprecation)
- [Ark platform model deprecation notice](https://ark.volcengine.com/region:cn-beijing/docs/model-deprecation-notice)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with arkcli command examples and summaries of model metadata or performance results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model candidates, capability and lifecycle comparisons, and user-requested activation steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
