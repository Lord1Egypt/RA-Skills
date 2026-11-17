## Description:

Helps agents discover, assess, install, update, and organize skills using local catalogs, marketplace searches, and static security checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdhewei](https://clawhub.ai/user/cdhewei)

### License/Terms of Use:

MIT-0

## Use Case:

People and developers managing agent skills use it to find relevant skills, review community packages, and manage installations, updates, and duplicates, including from an offline catalog.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A forced community update may bypass the advertised security gate.

Mitigation: Do not rely on the gate for community updates; review packages manually and prefer official marketplace installs until the bypass is fixed.

Risk: Scanner exclusions may leave unsafe files unscanned in an installed skill directory.

Mitigation: Inspect the entire community package before installation and test this skill in a separate agent profile before it manages real installed skills.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/cdhewei/skills/find-skills-plusplus)
- [CLI reference](artifact/references/cli.md)
- [Security reference](artifact/references/security.md)
- [Ranking reference](artifact/references/ranking.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON]

**Output Format:** [Skill recommendations and review guidance in text or Markdown; CLI reports in text or optional JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can report quality scores, risk levels, and requested file, network, and command permissions.]

## Skill Version(s):

5.3.1 (source: ClawHub release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
