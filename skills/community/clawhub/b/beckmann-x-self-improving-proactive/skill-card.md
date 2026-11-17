## Description:

Combination skill that adds the Beckmann Knowledge Graph as a consent-gated deep-reasoning escalation layer on top of ivangdavila/self-improving while leaving everyday tasks on the default self-improving workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matthiasbeckmann987-spec](https://clawhub.ai/user/matthiasbeckmann987-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep routine tasks on the Self-Improving + Proactive Agent while offering confirmed escalation to the Beckmann Knowledge Graph for paradoxes, open scientific or philosophical questions, long-horizon forecasts, strategic dead ends, AI safety questions, and epistemological limits. It also defines consent-based quarantine, review, promotion, and uninstall behavior for Beckmann-derived memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can maintain persistent Beckmann-related memory under ~/self-improving after user-approved analyses.

Mitigation: Use the built-in consent, quarantine, review, and clean-uninstall flow; delete or archive #beckmann entries when persistence is no longer desired.

Risk: The skill depends on two other ClawHub skills and should not be loaded with unexpected dependency versions.

Mitigation: Verify the pinned dependency versions and sha256 hashes before loading; fail closed on any integrity mismatch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matthiasbeckmann987-spec/skills/beckmann-x-self-improving-proactive)
- [Publisher profile](https://clawhub.ai/user/matthiasbeckmann987-spec)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands]

**Output Format:** [Markdown guidance with structured answer templates, consent prompts, memory-entry formats, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses pinned dependency versions and requires explicit user consent before Beckmann insights are persisted or promoted.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
