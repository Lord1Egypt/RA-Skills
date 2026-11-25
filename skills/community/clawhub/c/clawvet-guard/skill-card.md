## Description:

Scan a third-party agent skill with ClawVet and act on its grade before installing, enabling, or running it. Use when the user asks to scan, vet, or check a skill they did not write, or whether a skill from ClawHub or another untrusted source is safe to install.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohibshaikh](https://clawhub.ai/user/mohibshaikh)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to scan third-party skills before installing, enabling, or running them. It guides users to check scan coverage, findings, recommendations, and declared capabilities before deciding what to do.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawVet command is unpinned, so an upstream change could alter what runs.

Mitigation: Pin a ClawVet version before installing or relying on the scan.

Risk: Skillspector coverage was partial because two local references could not be resolved, so the scan evidence is incomplete.

Mitigation: Resolve the missing local references and rerun the scan before relying on its results.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mohibshaikh/skills/clawvet-guard)
- [ClawVet project repository](https://github.com/MohibShaikh/clawvet)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance, JSON]

**Output Format:** [Markdown guidance summarizing scan coverage, findings, recommendation, and capabilities, based on ClawVet results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include grade and sensitive capability information reported by ClawVet.]

## Skill Version(s):

1.0.10 (source: server-resolved release metadata; artifact frontmatter reports 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
