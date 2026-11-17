## Description:

ClawHub reputation checker for clawsec-suite. Adds a standalone reputation gate before guarded skill installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security-conscious operators use this skill to add a ClawHub reputation check before running guarded skill installs through clawsec-suite. It reviews ClawHub metadata and scanner summaries, then requires explicit confirmation when reputation falls below the configured threshold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because documented installation uses mutable or unpinned commands for a security-sensitive installer.

Mitigation: Install a pinned, verified release of this skill and its clawsec-suite dependency, and verify release checksums before trusting the package.

Risk: The skill queries ClawHub metadata and invokes the clawsec-suite guarded installer for user-selected skills.

Mitigation: Review the target skill code and scanner summary before running installation commands or using confirmation overrides.

Risk: Reputation scoring is heuristic and can produce false positives or false negatives.

Mitigation: Treat the reputation score as an additional review signal, keep confirmation gates enabled, and inspect the skill manually before overriding warnings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-clawhub-checker)
- [Publisher profile](https://clawhub.ai/user/davida-ps)
- [ClawSec homepage](https://clawsec.prompt.security/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text, JSON reputation results, and Markdown usage guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional CLAWHUB_REPUTATION_THRESHOLD configuration and confirmation flags for advisory or reputation overrides.]

## Skill Version(s):

0.0.8 (source: server release evidence, frontmatter, skill.json, and changelog released 2026-06-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
