## Description:

Generates deep research reports through the Baidu Qianfan DeepResearch Agent API, automating conversation creation, research execution, clarification skipping, outline confirmation, and Markdown/HTML report link retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ide-rea](https://clawhub.ai/user/ide-rea)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to turn scoped research questions into long-form Baidu Qianfan DeepResearch reports for industry research, market analysis, competitive analysis, technical reviews, policy interpretation, and decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research prompts, generated outlines, and report contents are sent to Baidu Qianfan and remote download links are returned.

Mitigation: Use only approved, non-confidential inputs unless third-party processing has been reviewed and accepted.

Risk: API keys can be supplied on the command line.

Mitigation: Prefer QIANFAN_API_KEY from a protected environment or credential store and avoid exposing credentials in shell history or logs.

Risk: Long-running report generation can consume API quota and cost.

Mitigation: Monitor Qianfan quota and cost before and during extended runs.

Risk: The workflow automatically skips clarification and confirms the generated outline.

Mitigation: Clarify vague research requests before execution and review the final report before using it for decisions.

## Reference(s):

- [DeepResearch Agent API documentation](references/api.md)
- [DeepResearch workflow documentation](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown response with report download links; helper script stdout is JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces remote Markdown and HTML report download links after a long-running API workflow.]

## Skill Version(s):

1.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
