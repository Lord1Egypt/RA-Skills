## Description: <br>
Hermes-only runtime security attestation and drift detection skill for operator-managed Hermes infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davida-ps](https://clawhub.ai/user/davida-ps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate deterministic Hermes runtime posture attestations, verify attestation integrity, check signed advisory-feed state, and compare authenticated baselines for drift. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is scoped to operator-managed Hermes infrastructure and can produce sensitive posture attestations. <br>
Mitigation: Install only in the intended Hermes environment and treat generated attestation artifacts as sensitive operational records. <br>
Risk: Configured advisory feed URLs and policy watch paths affect verification results. <br>
Mitigation: Review feed endpoints and policy paths before use, and keep advisory-feed verification signed and fail-closed. <br>
Risk: Scheduler helpers can add recurring checks when invoked with apply mode. <br>
Mitigation: Preview scheduler output with --print-only before using --apply. <br>
Risk: Unsigned advisory-feed bypass can weaken verification if left enabled. <br>
Mitigation: Use unsigned bypass only for temporary emergency recovery and remove it immediately afterward. <br>


## Reference(s): <br>
- [ClawSec homepage](https://clawsec.prompt.security) <br>
- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-hermes-attestation-guardian) <br>
- [Publisher profile](https://clawhub.ai/user/davida-ps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON attestation artifacts produced by the shipped scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for operator review; attestation files may contain sensitive host posture details.] <br>

## Skill Version(s): <br>
0.1.6 (source: frontmatter, changelog, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
