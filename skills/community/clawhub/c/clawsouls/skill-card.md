## Description:

Helps agents manage workspace personas, discover and publish Soul packages, and optionally sync encrypted agent memory on explicit request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomleelive](https://clawhub.ai/user/tomleelive)

### License/Terms of Use:

Apache-2.0

## Use Case:

Agent users and developers use this skill to install, switch, restore, create, validate, and publish AI personas across compatible agent workspaces, with optional encrypted memory sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activating a Soul changes agent persona files and may introduce untrusted instructions.

Mitigation: Review each Soul before activation, confirm persona changes with the user, and retain workspace backups.

Risk: Publishing a Soul can expose its contents publicly.

Mitigation: List and review the files to be published and obtain user confirmation first.

Risk: Memory sync moves encrypted agent memory to a configured remote.

Mitigation: Run sync or swarm only on explicit request and confirm the remote destination beforehand.

Risk: Installing or executing a persona tool from an untrusted source can alter workspace behavior.

Mitigation: Prefer trusted, pinned sources and review commands before execution.

## Reference(s):

- [ClawHub release](https://clawhub.ai/tomleelive/skills/clawsouls)
- [ClawSouls registry](https://clawsouls.ai)
- [Soul-Driven Interaction Design](https://doi.org/10.5281/zenodo.18772585)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Text and Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update local persona files; publishing and memory sync require explicit user approval.]

## Skill Version(s):

0.6.8 (source: release evidence, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
