## Description:

Lists local OpenClaw skills, extracts their descriptions and paths, caches scan results, compares directory changes, and can export the inventory as JSON or Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fantasywoc](https://clawhub.ai/user/fantasywoc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect the local skill directory, see which skills have SKILL.md files, and export a skill inventory for review or integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads and caches local OpenClaw skill instructions, which may include private operational notes or secrets.

Mitigation: Avoid JSON or Markdown export when local skills contain sensitive information, and review generated cache and export files before sharing.

Risk: The server security summary identifies unsafe Pickle cache loading that can execute tampered cache data.

Mitigation: Install only in trusted local environments and replace the Pickle cache with a safer format such as JSON before broad use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fantasywoc/skills/all-skill-list)

## Skill Output:

**Output Type(s):** [text, json, markdown, shell commands]

**Output Format:** [Console text, JSON export, or Markdown export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist cache and export files in the skill scripts directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
