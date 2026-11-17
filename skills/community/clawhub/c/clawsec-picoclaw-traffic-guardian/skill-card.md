## Description:

Picoclaw runtime traffic monitoring baseline for lightweight AI gateway proxy inspection, egress detection, and posture integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

AGPL-3.0-or-later

## Use Case:

Developers and security engineers use this skill as a Picoclaw traffic-monitoring specification scaffold for building opt-in HTTP/HTTPS proxy inspection, egress exfiltration detection, inbound injection detection, redacted JSONL findings, and posture export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended install command uses unpinned npx execution, which can run changing third-party code.

Mitigation: Prefer the signed standalone verification flow or a pinned, trusted Skills CLI version before installing.

Risk: Future HTTPS inspection could expose sensitive traffic if expanded beyond the documented opt-in, process-scoped model.

Mitigation: Confirm HTTPS inspection remains opt-in, process-scoped, redacts secrets before writing logs, and never installs system CA trust automatically.

## Reference(s):

- [ClawSec homepage](https://clawsec.prompt.security)
- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-picoclaw-traffic-guardian)
- [README](artifact/README.md)
- [Specification](artifact/SPEC.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash commands and JSON schema examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Specification scaffold; v0.0.1 does not ship an active proxy runtime.]

## Skill Version(s):

0.0.1-beta5 (source: frontmatter, skill.json, changelog, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
