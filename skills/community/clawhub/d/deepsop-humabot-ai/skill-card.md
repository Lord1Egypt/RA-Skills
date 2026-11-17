## Description:

DeepSop工作台 helps agents turn natural-language sales requests into DeepSOP customer discovery, email, phone, SMS, and call-script review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuoai](https://clawhub.ai/user/kukuoai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and go-to-market teams use this skill to submit and monitor DeepSOP customer discovery, outbound email, phone, SMS, and call-script review tasks from conversational instructions. Agents can return status summaries and xlsx reports for discovered customers or campaign results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive customer and communication data that may appear in chat summaries or exported reports.

Mitigation: Use only in approved workspaces, minimize or mask personal data in previews and reports, and restrict report access to authorized recipients.

Risk: Automatic result delivery can expose reports if message destinations are not tightly controlled.

Mitigation: Bind delivery to fixed, authorized chat targets and verify the recipient before scheduling or sending report files.

Risk: Shell-oriented payload handling can corrupt JSON or expose task data through command arguments.

Mitigation: Pass structured payloads through stdin or files, avoid shell interpolation for customer data, and preserve the artifact's validation checks before API submission.

Risk: Scheduled callbacks could query and publish task results without adequate authorization.

Mitigation: Require authenticated callback validation and confirm that the callback task, workspace, and delivery target are authorized before querying results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kukuoai/skills/deepsop-humabot-ai)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)
- [DeepSOP platform](https://ai.deepsop.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with JSON payloads, shell commands, API call instructions, status summaries, and xlsx report file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPSOP_API_KEY and may send customer, email, phone, SMS, and task data to DeepSOP APIs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
