## Description:

Audits repositories for 2026 marketing readiness by checking README and documentation discoverability for LLMs and generative search engines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmstudio667-commits](https://clawhub.ai/user/tmstudio667-commits)

### License/Terms of Use:


## Use Case:

Developers and marketing engineers use this skill to audit a local repository's README, llms.txt, and documentation signals for LLM discoverability, A2A readiness, and human and agent conversion structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill with npx without a pinned OpenClaw version depends on the package resolved at execution time.

Mitigation: Use a trusted or pinned OpenClaw CLI version when stricter supply-chain control is required.

Risk: The auditor reads README.md content from the target repository and reports documentation readiness findings.

Mitigation: Run it only on repositories whose local README content is acceptable to inspect, and review findings before publishing documentation changes.

Risk: The audit is based on a small set of documentation signals and may miss broader marketing, compliance, or discoverability issues.

Mitigation: Treat results as advisory and confirm important recommendations through human review before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tmstudio667-commits/skills/agentic-marketing-auditor)
- [ClawHub publisher profile](https://clawhub.ai/user/tmstudio667-commits)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text terminal audit output with recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local README.md and llms.txt presence from the target repository path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
