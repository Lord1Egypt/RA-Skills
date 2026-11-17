## Description:

Write, review, or debug Dataify SERP, Web Unlocker, Builder, MCP, or SDK integration code using correct authentication, task lifecycle, retry, error, and output patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, review, and debug Dataify integrations that handle credentials, retries, async task completion, errors, and production output validation. It is not intended for ordinary end-user searches, scraping, research, or account setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes live Dataify collection helpers that can consume credits or run workflows beyond simple integration guidance.

Mitigation: Install only when Dataify integration helpers are needed, review the shipped scripts, and run business workflow helpers only when live Dataify collection and credit use are intended.

Risk: Credential handling and generated command strings may expose or misuse tokens if copied, logged, or reused without review.

Mitigation: Use DATAIFY_API_TOKEN from the environment, do not paste tokens into chat or logs, rotate any token used with task URLs, and validate generated curl or resume commands before execution.

Risk: Ambiguous Builder submissions can duplicate paid work if retried automatically after an uncertain request outcome.

Mitigation: Persist task IDs, resume existing tasks after local timeouts, and avoid automatic resubmission unless the original request is known not to have reached the server.

## Reference(s):

- [Dataify documentation](https://doc.dataify.com)
- [Dataify support](https://www.dataify.com/)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-api-best-practices)
- [Integration contract](references/integration-contract.md)
- [Authentication](references/authentication.md)
- [Builder API](references/builder-api.md)
- [SERP API](references/serp-api.md)
- [Web Unlocker](references/web-unlocker.md)
- [Task lifecycle](references/task-lifecycle.md)
- [Production checklist](references/production-checklist.md)
- [Error catalog](references/error-catalog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code, shell commands, configuration guidance, and optional JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include static audit findings, Dataify integration patterns, token setup guidance, task resume commands, and final API result handling guidance.]

## Skill Version(s):

1.1.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
