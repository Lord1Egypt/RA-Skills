## Description:

Enterprise API testing assistant covering developer self-tests, deep single-API tests, business flow tests, security audits, defect diagnosis, report generation, API-document understanding, global knowledge accumulation, and multi-user isolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaosiming](https://clawhub.ai/user/zhaosiming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and API platform teams use this skill to plan and run API validation workflows, inspect security and defect behavior, maintain API knowledge, and produce Markdown testing reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store sensitive API test data in per-user workspaces, temporary files, knowledge caches, and reports.

Mitigation: Use only test or low-risk API accounts unless redaction and retention controls are added; sanitize workspace user IDs and review reports before sharing.

Risk: Shared global knowledge-base updates can publish incorrect or sensitive test-derived information to other users.

Mitigation: Require independent review before publishing global knowledge-base updates and keep sensitive findings local unless they have been desensitized.

Risk: Bearer tokens and API credentials may be exposed through test inputs, request logs, or generated reports.

Mitigation: Avoid long-lived secrets, prefer scoped test credentials, and remove tokens or secrets from generated artifacts before distribution.

## Reference(s):

- [Skill specification](artifact/SKILL.md)
- [README](artifact/README.md)
- [ClawHub skill page](https://clawhub.ai/zhaosiming/skills/full-flow-testing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and conversational guidance, with optional code or shell-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write per-user session state, temporary files, local knowledge cache files, and test reports when the agent environment permits file access.]

## Skill Version(s):

1.0.0 (source: release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
