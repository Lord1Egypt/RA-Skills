## Description:

Audits and diagnoses SEO issues using Bright Data CLI live web data, including rendered schema, hreflang, canonical tags, crawlability, on-page checks, and SERP-based ranking signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meirk-brd](https://clawhub.ai/user/meirk-brd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and SEO practitioners use this skill to run evidence-backed technical and on-page SEO audits for a site or page and receive prioritized remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an embedded remote installer command for Bright Data CLI.

Mitigation: Review before installing and use a trusted, verifiable installation method for Bright Data CLI.

Risk: Shell-command patterns can mishandle untrusted URLs or keywords.

Mitigation: Quote and validate user-supplied domains, URLs, and keywords before running commands.

Risk: Audits may send domains, URLs, and keywords through Bright Data and search services.

Mitigation: Avoid private or internal targets unless the user has confirmed tool and account policy permit that use.

## Reference(s):

- [Audit Framework](references/audit-framework.md)
- [bdata Recipes](references/bdata-recipes.md)
- [Output Templates](references/output-templates.md)
- [Site-Type Playbooks](references/site-type-playbooks.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown SEO audit report with evidence blocks and a prioritized action plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each finding includes a runnable bdata command and output excerpt; unavailable measurements are routed to out-of-scope notes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
