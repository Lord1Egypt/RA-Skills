## Description:

BytePlusCDN helps agents manage BytePlus CDN domains, origin and policy templates, cache purge and prefetch operations, and offline or real-time log delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whitechenyingxi-maker](https://clawhub.ai/user/whitechenyingxi-maker)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to configure and operate BytePlus CDN domains, distribution policy templates, cache refresh or preload jobs, and log delivery from an agent-guided CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles BytePlus cloud credentials and may prompt for or read secrets used against production CDN resources.

Mitigation: Install in a virtual environment, review dependencies first, use least-privilege BytePlus credentials, and avoid placing secrets directly in command lines or committing credential files.

Risk: CDN domain, purge, preload, and policy-template commands can change production delivery behavior or affect broad domain scopes.

Mitigation: Review every domain, purge, preload, and policy command before execution, especially any all-domain option.

Risk: Offline and real-time log delivery can send operational logs or credentials to external storage and analytics endpoints.

Mitigation: Review log destinations, require HTTPS endpoints, and use protected local output paths when handling generated credential JSON.

## Reference(s):

- [BytePlusCDN ClawHub Skill Page](https://clawhub.ai/whitechenyingxi-maker/skills/bytepluscdn)
- [BytePlus CDN Scripts Documentation](artifact/reference/about.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python CLI examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BytePlus credentials and careful review before executing CDN, purge, preload, or log-delivery changes.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter states v1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
