## Description:

Security scanner for OpenClaw skills. Detects malicious patterns, suspicious URLs, and install traps before you install a skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentchan](https://clawhub.ai/user/vincentchan)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to scan OpenClaw or ClawHub skills before installation, review suspicious commands and URLs, and add security checks to local workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner fetches user-supplied URLs and can expose network context when pointed at arbitrary links.

Mitigation: Run it only against URLs and directories you intend to scan, and avoid arbitrary untrusted links from sensitive networks.

Risk: A safe scan result can be incomplete because the tool performs limited pattern checks.

Mitigation: Treat results as triage signals and manually review install instructions, flagged lines, publisher identity, and provenance before relying on a skill.

Risk: Using this skill as the only security gate can create misleading confidence.

Mitigation: Use it as one review step alongside human approval for high-risk findings and normal dependency, source, and behavior review.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/vincentchan/skills/claw-skill-guard)
- [1Password research on OpenClaw skill malware](https://1password.com/blog/from-magic-to-malware-how-openclaws-agent-skills-become-an-attack-surface)
- [Artifact-declared source repository](https://github.com/vincentchan/clawd-workspace/tree/master/skills/claw-skill-guard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, shell command examples, configuration snippets, and scanner report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner reports include risk levels and flagged lines; results are triage signals, not proof that a skill is safe.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
