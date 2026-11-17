## Description:

Picoclaw security posture skill with advisory awareness, configuration drift detection, and supply-chain verification guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate Picoclaw security posture profiles, compare them against approved baselines, check Picoclaw-relevant advisories, and verify release-artifact supply-chain evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install example uses an unpinned npx command, which can weaken supply-chain predictability.

Mitigation: Prefer the signed-release verification flow or pin the Skills CLI version before installing.

Risk: Generated profiles can include Picoclaw configuration paths, file hashes, and counts of secret-like markers.

Mitigation: Treat profile outputs as local security artifacts and restrict where they are stored or shared.

Risk: Unsigned advisory or checksum-only workflows provide less assurance than signed verification.

Mitigation: Use unsigned modes only for short, documented emergency or offline windows, and require signed feed or manifest verification for production decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davida-ps/skills/clawsec-picoclaw-security-guardian)
- [Publisher Profile](https://clawhub.ai/user/davida-ps)
- [ClawSec Homepage](https://clawsec.prompt.security)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON security-profile outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [On-demand scripts are read-only except for explicit local profile or report outputs.]

## Skill Version(s):

0.0.6 (source: server release evidence, frontmatter, skill.json, CHANGELOG released 2026-06-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
