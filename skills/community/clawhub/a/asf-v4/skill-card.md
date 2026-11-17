## Description:

Asf V4 provides governance checks, ownership proofing, economics scoring, rework-risk analysis, safe optimization, and UI generation tools for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alshowse-tech](https://clawhub.ai/user/alshowse-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to evaluate API and contract changes, assign ownership, compare cost and role tradeoffs, predict rework risk, and generate UI artifacts from product requirements in OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review classifies the release as suspicious because it is a broad governance and administration toolkit rather than a focused parser.

Mitigation: Install only after publisher trust review and run it in an environment with constrained command execution, deployment rights, file writes, outbound network access, and log or memory visibility.

Risk: Artifact behavior includes CLI-style commands, deployment-related operations, and skill-loading surfaces that can affect development workflows.

Mitigation: Require explicit approvals, dry-run review where available, and least-privilege credentials before enabling deployment, command execution, or skill-loading capabilities.

Risk: Server-resolved GitHub import provenance is unavailable for this version.

Mitigation: Ask the publisher for signed or pinned release evidence and verify the release fingerprint before using the skill in sensitive workflows.

Risk: Server evidence and artifact files disagree on the license identifier.

Mitigation: Confirm the authoritative license terms with the publisher before redistribution or commercial deployment.

## Reference(s):

- [ClawHub listing for Asf V4](https://clawhub.ai/alshowse-tech/skills/asf-v4)
- [Artifact README](artifact/README.md)
- [Release 1.5.6 report](artifact/RELEASE-1.5.6.md)
- [Skill manifest](artifact/skill.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured tool results, Markdown/code snippets, and CLI-style command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include governance decisions, proofs, risk scores, optimization recommendations, generated UI code, and configuration guidance.]

## Skill Version(s):

1.5.6 (source: server release evidence, artifact skill.yaml, package.json, and release report)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
