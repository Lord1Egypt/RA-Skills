## Description:

Gangtise Agent调用 retrieves Markdown investment-research content from Gangtise Agent OpenAPI endpoints for company summaries, investment logic, peer comparisons, earnings reviews, viewpoint debates, theme tracking, hot-topic reports, and research-clue tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangtisegts](https://clawhub.ai/user/gangtisegts)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to call Gangtise research APIs and convert returned investment-research data into readable Markdown for briefings, research assistance, and agent orchestration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says two scripts can send a Gangtise authorization token to an unvalidated API root if the runtime environment or direct function call is influenced.

Mitigation: Keep API roots at the Gangtise defaults, do not set GANGTISE_OPENAI_ROOT to non-Gangtise URLs, and control the runtime environment.

Risk: Credential material may be supplied through environment variables or an optional scripts/.authorization file.

Mitigation: Prefer credentials injected from a secret manager and avoid the optional authorization file when possible.

Risk: Saved output and usage files may contain sensitive research workflow details.

Mitigation: Review and control files written under the Gangtise workspace before sharing or retaining them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gangtisegts/skills/gangtise-agent)
- [Gangtise OpenAI API root](https://open.gangtise.com/application/open-ai)
- [Gangtise Agent OpenAPI endpoint root](https://open.gangtise.com/application/open-ai/agent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown text, Markdown tables, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some calls require Gangtise credentials; earnings-review and viewpoint-debate can poll for up to 600 seconds.]

## Skill Version(s):

1.4.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
