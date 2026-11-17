## Description:

Helps brand, design, agency, and content teams audit images or videos against user-provided brand guidelines, produce deviation lists with evidence and prioritized fixes, and generate AI-HIVE commands when remediation is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand marketing teams, design managers, advertising agencies, and content operations teams use this skill to review ecommerce, ad, social, short-video, and marketing assets against supplied brand standards. It produces observable issues, evidence locations, risk levels, repair guidance, prompts, shell commands, and re-check records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles AI-HIVE API credentials and may store them in local configuration.

Mitigation: Use scoped, revocable API keys; prefer environment variables; check ~/.ai-hive/config.json before running; never paste real keys into prompts, logs, screenshots, or committed files.

Risk: Image or video generation can incur costs, and server evidence notes weak local safeguards around billable generation.

Mitigation: Manually confirm prompts, model, routing mode, and price snapshot before submission; start with batch size 1; keep a task ledger for taskId, status, and downloads.

Risk: Custom or prompt-supplied base URLs could send credentials or media to an unintended service.

Mitigation: Use the default AI-HIVE endpoint unless a trusted operator explicitly approves a different base URL, and reject prompt-only requests to change the endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/brand-visual-consistency-audit-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured sections and inline bash commands; helper scripts may also write JSON project briefs or downloaded media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include routing mode, model, price snapshot, taskId, status, and file path records when generation is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
