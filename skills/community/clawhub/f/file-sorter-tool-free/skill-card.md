## Description:

Uses a vision-capable agent to inspect local files, summarize visible content, rename files, and move them into fixed categories for personal desktop or downloads-folder cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and individual developers use this skill to organize local folders by previewing files, identifying content with visual model support, and producing rename or move actions for categories such as finance, work, images, and unclassified files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad local file inspection and command authority while organizing files.

Mitigation: Run it first in dry-run mode on a small, explicit folder and review every proposed rename and destination before allowing changes.

Risk: Loose triggers could apply the skill to unrelated conversion or content-extraction requests.

Mitigation: Use it only for explicit local file organization workflows and avoid unrelated conversion, extraction, or recovery tasks.

Risk: Automatic rename and move actions can disrupt local file organization if the classification is wrong.

Mitigation: Keep deletion disabled, preserve file extensions, and back up or copy important folders before applying bulk moves.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/file-sorter-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown with inline shell commands and structured status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local file inspection, rename, and move operations; dry-run review is recommended before applying changes.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
