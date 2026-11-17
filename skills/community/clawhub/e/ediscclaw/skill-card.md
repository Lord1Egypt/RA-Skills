## Description:

edisclaw processes, deduplicates, culls, and searches ESI collections locally for a fraction of outsourced e-discovery costs, giving small firms litigation-support capabilities from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jagadeeshmurali-coder](https://clawhub.ai/user/jagadeeshmurali-coder)

### License/Terms of Use:


## Use Case:

External legal practitioners, paralegals, solo attorneys, small firms, and litigation teams use this skill to operate the edisclaw CLI for local e-discovery ingestion, deduplication, culling, search, review, production, reporting, and audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles sensitive legal matter data and stores local ESI under ~/.edisclaw/.

Mitigation: Run the skill only on authorized matter data, protect the host and local storage, and apply normal legal-data access controls.

Risk: Privilege, redaction, TAR, and production decisions can affect litigation outcomes.

Mitigation: Require qualified legal review of privilege calls, redactions, production sets, audit logs, and defensibility reports before production use.

Risk: The skill depends on an external edisclaw Homebrew package and some Pro or Litigation features may use external API-backed functionality.

Mitigation: Install only if the edisclaw package source is trusted, and review paid-tier behavior before allowing external API use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jagadeeshmurali-coder/skills/ediscclaw)
- [Publisher profile](https://clawhub.ai/user/jagadeeshmurali-coder)
- [edisclaw homepage](https://github.com/legal-tools/edisclaw)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assumes the edisclaw binary is installed; commands may operate on sensitive local legal matter data under ~/.edisclaw/.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
