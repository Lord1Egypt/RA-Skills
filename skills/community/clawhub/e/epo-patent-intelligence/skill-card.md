## Description:

EPO Patent Intelligence monitors European Patent Office patent data, analyzes competitor threats and technology trends, and generates strategic HTML reports for business decision-making.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quratus](https://clawhub.ai/user/quratus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, competitive intelligence teams, and R&D leaders use this skill to collect EPO OPS patent data, assess competitor activity, and produce weekly strategic reports for manufacturing-focused patent monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent public-serving automation and tunnels can expose generated reports more broadly than intended.

Mitigation: Run under a dedicated unprivileged account and avoid public tunnels unless publication is intentional.

Risk: Credential handling can expose EPO or tunnel secrets if tokens or .env contents are committed, sourced, or printed.

Mitigation: Revoke and replace embedded Cloudflare tokens, keep EPO credentials out of version control, and avoid printing .env values.

Risk: Generated patent reports may include unescaped or misleading content.

Mitigation: Review report escaping and validate LLM-generated analysis before publishing reports to viewers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/quratus/skills/epo-patent-intelligence)
- [EPO OPS API Reference Documentation](references/EPO_API.md)
- [Patent Analysis Patterns](references/ANALYSIS_PATTERNS.md)
- [Modern Dashboard & Report Framework Guidelines](references/REPORT_FRAMEWORKS.md)
- [EPO Developer Portal](https://developers.epo.org/)
- [EPO Open Patent Services](https://www.epo.org/searching-for-patents/technical/epo-ops.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and generated HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local SQLite data, logs, and HTML reports when scripts are executed; requires EPO OPS credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
