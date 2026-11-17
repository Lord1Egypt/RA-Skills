## Description:

AI agent governance, trust scoring, and policy enforcement powered by AgentMesh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imran-siddique](https://clawhub.ai/user/imran-siddique)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to enforce action policies, verify agent identities, check trust scores, and maintain audit trails for OpenClaw agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell wrapper inputs for agent names, policy paths, messages, signatures, and action strings may be unsafe when values are untrusted.

Mitigation: Review the skill before installation, run it in a constrained environment, and avoid passing untrusted values to the scripts.

Risk: Some scripts return fallback baseline results when AgentMesh is unavailable, which can make governance checks less authoritative.

Mitigation: Install and verify AgentMesh before relying on trust scoring, identity verification, or audit integrity outputs.

Risk: Dependencies are described through install commands but are not pinned in the skill artifact.

Mitigation: Use a reviewed environment with pinned dependency versions before commercial deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imran-siddique/skills/agentmesh-governance)
- [OpenClaw Skill Homepage](https://github.com/imran-siddique/agentmesh-integrations/tree/master/openclaw-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts expect local command-line arguments and may read policy files from the workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
