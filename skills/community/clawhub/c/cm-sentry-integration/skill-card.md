## Description: <br>
Sentry error tracking - list, triage, and resolve issues; manage releases and source maps via CLI and REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent inspect Sentry errors, triage issue details, and prepare CLI or REST API actions for releases, source map uploads, deploy records, and issue state changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose sensitive Sentry event data, including stack traces, breadcrumbs, and issue details. <br>
Mitigation: Use least-privilege Sentry tokens scoped to the required organization and project, fetch full event data only when needed, and redact sensitive output before sharing. <br>
Risk: The skill includes commands that can change production issue state, assignments, ignores, bulk updates, release finalization, deploy records, and source-map uploads. <br>
Mitigation: Require explicit human confirmation before executing any state-changing CLI command or REST API request. <br>
Risk: Token-backed API and CLI access may affect production Sentry projects if environment variables point at the wrong organization or project. <br>
Mitigation: Verify SENTRY_ORG and SENTRY_PROJECT before each action and prefer project-specific tokens over broad account tokens. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/cm-sentry-integration) <br>
- [Sentry REST API Base URL](https://sentry.io/api/0) <br>
- [sentry-cli requirement](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include token-backed Sentry CLI commands, curl requests, issue triage notes, release management steps, and source map upload guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
