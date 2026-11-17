## Description:

Outbound publishing governance for blog, social, and announcement content using hard-block checks, weighted consensus, rewrite paths, and audit artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and publishing teams use this skill as a pre-publication gate for blog posts, social posts, announcements, and other outbound statements that need policy, confidentiality, legal-claim, and unsupported-promise checks before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency and version metadata disagree across package, lockfile, and skill documentation.

Mitigation: Pin dependencies exactly and reconcile package, lockfile, and SKILL.md versions before production deployment.

Risk: External-agent mode can rely entirely on caller-supplied votes.

Mitigation: Document or enforce that caller-supplied votes cannot bypass hard-block checks for sensitive or legally risky content.

Risk: The skill intentionally writes persistent decision artifacts.

Mitigation: Run it with a scoped CONSENSUS_STATE_FILE or CONSENSUS_STATE_ROOT so publish decisions are isolated to the intended board state.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaicianflone/skills/consensus-publish-guard)
- [consensus-guard-core npm package](https://www.npmjs.com/package/consensus-guard-core)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON decision object with optional rewrite patch and board artifact references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent decision artifacts under the configured consensus state path.]

## Skill Version(s):

1.1.17 (source: server release metadata and package.json; artifact SKILL.md and package-lock.json contain older versions)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
