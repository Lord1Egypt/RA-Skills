## Description:

DeepVista Card: Manage your knowledge cards - create, search, and organize context cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingconan](https://clawhub.ai/user/jingconan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage DeepVista Vistabase knowledge cards through the DeepVista CLI, including listing, reading, creating, updating, editing, deleting, pinning, archiving, and searching cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, edit, delete, pin, or archive DeepVista knowledge cards.

Mitigation: Confirm write or destructive card operations with the user before execution.

Risk: The skill depends on the external deepvista-cli package.

Mitigation: Use a pinned or otherwise trusted deepvista-cli release in environments that require stricter dependency control.

## Reference(s):

- [DeepVista CLI homepage](https://cli.deepvista.ai)
- [ClawHub skill page](https://clawhub.ai/jingconan/skills/deepvista-vistabase-card)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and DeepVista card URLs when write operations return card IDs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the DeepVista CLI and the shared DeepVista authentication/profile skill.]

## Skill Version(s):

0.1.0-alpha.21 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
