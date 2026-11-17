## Description:

Hermes runtime traffic monitoring baseline for opt-in proxy inspection, egress detection, and attestation-aware traffic posture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill as a Hermes traffic-monitoring specification baseline for scoped proxy inspection, exfiltration and injection detection, redacted local findings, and attestation posture export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes an unpinned npx install command.

Mitigation: Install only from a trusted source and prefer the documented signed-release verification workflow or a pinned CLI/source version.

Risk: Future runtime proxy functionality could broaden traffic inspection or trust-store impact if implemented carelessly.

Mitigation: Review future implementations for opt-in operation, per-process proxy scope, no automatic system CA changes, redacted logs, and no default blocking.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davida-ps/skills/clawsec-hermes-traffic-guardian)
- [Publisher Profile](https://clawhub.ai/user/davida-ps)
- [ClawSec Homepage](https://clawsec.prompt.security)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON schema examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Specification-only release; no runtime proxy code is shipped in this version.]

## Skill Version(s):

0.0.1-beta5 (source: server release metadata, frontmatter, skill.json, changelog released 2026-06-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
