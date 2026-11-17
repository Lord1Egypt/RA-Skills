## Description:

OpenClaw runtime traffic monitoring baseline for opt-in HTTP/HTTPS proxy inspection, egress detection, inbound injection detection, and social-account policy review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

AGPL-3.0-or-later

## Use Case:

Developers and security engineers use this skill as a specification scaffold for opt-in OpenClaw runtime traffic monitoring, including HTTP/HTTPS proxy inspection, exfiltration detection, injection detection, and review records for approval-sensitive social-account mutations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented Skills CLI install command is unpinned and auto-confirming.

Mitigation: Prefer a pinned and reviewed Skills CLI version or use the signed standalone release-verification path before installation.

Risk: A future traffic-monitoring implementation could expose sensitive request or response content if logging is too broad.

Mitigation: Keep monitoring opt-in and process-scoped, bound scan sizes, and redact secrets before writing logs or sending alerts.

Risk: Optional HTTPS inspection could become invasive if trust is installed globally.

Mitigation: Require explicit operator action and per-process CA trust; do not install system-wide CA trust automatically.

Risk: Traffic enforcement could block, mutate, or approve actions without operator intent.

Mitigation: Keep the first implementation detect-and-log only and create operator-review records without auto-blocking, auto-approving, or rewriting requests.

## Reference(s):

- [Skill page](https://clawhub.ai/davida-ps/skills/clawsec-openclaw-traffic-guardian)
- [ClawSec homepage](https://clawsec.prompt.security/)
- [OpenClaw Traffic Guardian specification](artifact/SPEC.md)
- [OpenClaw Traffic Guardian README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with shell command examples and JSON schema examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current release is a specification scaffold and does not ship an active proxy or runtime implementation.]

## Skill Version(s):

0.0.1-beta5 (source: frontmatter, skill.json, changelog, released 2026-06-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
