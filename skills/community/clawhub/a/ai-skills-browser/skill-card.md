## Description:

Skills Browser is a local HTML and Python tool for filtering skills in a skills directory and viewing each skill's details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quntion](https://clawhub.ai/user/quntion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to launch a local browser for inspecting nearby skills, filtering the skill list, and reading skill frontmatter and Markdown details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local server may expose nearby skill contents more broadly than intended.

Mitigation: Bind the server to 127.0.0.1 and remove wildcard CORS before use.

Risk: Skill detail lookup may read unexpected paths if a skill ID is not constrained to known skill directories.

Mitigation: Validate requested skill IDs against the enumerated skill list before reading any SKILL.md file.

Risk: Rendered Markdown may include unsafe HTML from local skill content.

Mitigation: Sanitize rendered Markdown or disable raw HTML rendering in the Markdown parser.

Risk: The launcher kills any process using port 8765.

Mitigation: Replace forced port termination with a clear port-conflict message or a verified graceful shutdown path.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/quntion/skills/ai-skills-browser)
- [Publisher profile](https://clawhub.ai/user/quntion)
- [marked Markdown parser](https://github.com/markedjs/marked)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown instructions and a local browser interface]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Displays skill metadata and Markdown content from the local skills directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
