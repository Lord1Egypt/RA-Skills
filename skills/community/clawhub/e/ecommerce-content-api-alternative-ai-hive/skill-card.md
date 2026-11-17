## Description:

This Chinese-language skill helps e-commerce content teams plan an evidence-based migration or comparison from an existing e-commerce content API workflow to AI-HIVE for product images, detail pages, ads, and selling videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, content operations teams, and e-commerce migration owners use this skill to design non-production AI-HIVE comparison runs, acceptance criteria, rollback gates, and deliverables for SKU content matrices, channel size tables, image/video batches, and manual quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may trigger automatically for Chinese-language AI-HIVE and e-commerce content migration prompts.

Mitigation: Review invocation behavior before deployment and install only for teams that need this AI-HIVE-focused migration workflow.

Risk: Production data, unauthorized materials, or exposed API keys could create privacy, licensing, or credential-handling issues during real migration tests.

Mitigation: Use non-production samples, confirm material authorization, and keep API keys in environment variables.

Risk: The local planning helper writes to the path supplied with --output and could overwrite an important existing file.

Mitigation: Point --output at a disposable or reviewed path and keep generated planning files separate from critical workspace files.

## Reference(s):

- [AI-HIVE chat reference](https://ai-hive.iclip.cn/chat)
- [Skill evidence worksheet](references/evidence.md)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ecommerce-content-api-alternative-ai-hive)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON planning output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper writes a local JSON migration plan when invoked with sample names, owner, and output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
