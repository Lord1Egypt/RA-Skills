## Description:

Generates a structured Markdown AI news daily report from recent AI topics and saves it to GetNote.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happyzengfen](https://clawhub.ai/user/happyzengfen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to collect recent AI news signals, shape them into a concise daily Markdown report, and save the result to a GetNote account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads report content and credentials to a separately named GetNote API host.

Mitigation: Verify that openapi.biji.com is the official endpoint for credentials issued by open.getnote.cn, and prefer scoped or disposable API credentials.

Risk: The skill offers recurring unattended execution through cron.

Mitigation: Run the script manually first, review the generated report and logs, and enable the cron job only after documenting how to remove or disable it.

Risk: The current script uploads a template rather than a complete AI-news analysis.

Mitigation: Inspect the generated Markdown before upload or automation, and complete the AI analysis step before relying on the saved report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/happyzengfen/skills/fengxinzi-ai-news)
- [Publisher profile](https://clawhub.ai/user/happyzengfen)
- [GetNote developer center](https://open.getnote.cn/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Text]

**Output Format:** [Markdown report and terminal status text; saved to GetNote through an API call]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GetNote API credentials and external search tools; the bundled script writes a template report for later AI completion.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
