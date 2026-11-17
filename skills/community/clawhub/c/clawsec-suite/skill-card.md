## Description:

ClawSec suite manager with embedded advisory-feed monitoring, cryptographic signature verification, approval-gated malicious-skill response, and guided setup for additional security skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security operators use this skill to monitor ClawSec advisories, check installed skills against advisory feed entries, and set up approval-gated safeguards for risky skill installs or removals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable or unsigned remote advisory data can influence security decisions or guarded install outcomes.

Mitigation: Use the manual verified install path or a pinned ClawHub version, keep CLAWSEC_ALLOW_UNSIGNED_FEED disabled, and verify feed signatures and checksum manifests.

Risk: Custom feed or catalog URLs can redirect the suite to untrusted security data.

Mitigation: Only set CLAWSEC_* feed, signature, checksum, or catalog overrides for sources you control and verify.

Risk: The hook and cron setup create ongoing OpenClaw automation in the user's environment.

Mitigation: Review the setup output before enabling persistent automation and rely on the suite's approval-gated flow before any removal or risky install action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/davida-ps/skills/clawsec-suite)
- [ClawSec Homepage](https://clawsec.prompt.security/)
- [ClawSec Advisory Feed](https://clawsec.prompt.security/advisories/feed.json)
- [ClawSec Skill Catalog Index](https://clawsec.prompt.security/skills/index.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and setup oriented; removal and risky install actions remain approval-gated.]

## Skill Version(s):

0.1.16 (source: frontmatter, artifact/skill.json, changelog released 2026-07-14, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
