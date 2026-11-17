## Description:

Conducts a nine-step tender audit workflow to detect bid rigging and collusion through bidder mapping, relationship analysis, pricing review, timing analysis, document similarity checks, qualification review, risk scoring, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rc17777](https://clawhub.ai/user/rc17777)

### License/Terms of Use:

MIT-0

## Use Case:

Audit, procurement, and compliance teams use this skill to structure an audit of tender activity and surface potential bid-rigging indicators across bidder relationships, pricing patterns, submission timing, document similarity, and qualifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may process sensitive bidder identities, ownership or personnel links, pricing, document metadata, and audit findings.

Mitigation: Use it only for authorized procurement or bidding audits and confirm confidentiality obligations before providing audit materials.

Risk: The workflow references local pipeline scripts and invoked skills that are not included in this artifact.

Mitigation: Verify the referenced pipeline, scripts, and invoked skills in the target environment before running the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rc17777/skills/audit-bidding-detection)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and structured audit report content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bidder profiles, relationship findings, price findings, timing findings, similarity findings, qualification findings, risk assessment, and a final bid-rigging analysis report.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
