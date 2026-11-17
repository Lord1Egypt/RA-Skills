## Description:

Audit AI agent skills for security vulnerabilities when scanning installed skills against the OWASP Agentic Skills Top 10, checking skills before running them, gating CI/CD on skill safety, or generating audit reports for stakeholders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markeljan](https://clawhub.ai/user/markeljan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Agentsec to audit installed agent skills, check OWASP Agentic Skills Top 10 coverage, gate CI/CD workflows, and generate security reports for stakeholders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends executing an npm-distributed CLI, including global installation options, to scan local skill directories.

Mitigation: Review before installing in sensitive environments and prefer a pinned version, lockfile-managed local install, or internally vetted package mirror.

Risk: Default scans inspect multiple known skill directories and may cover more local content than intended.

Mitigation: Use targeted scans with --path or --platform when only selected skill directories should be inspected.

## Reference(s):

- [Agentsec homepage](https://agentsec.sh)
- [Agent Skills specification](https://agentskills.io/specification)
- [Skills.sh](https://skills.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated audit reports may be text, JSON, SARIF, or HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide scans across default skill directories or targeted paths and platforms.]

## Skill Version(s):

0.4.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
