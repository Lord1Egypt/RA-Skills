## Description:

Manage bookmarks using the buku CLI for adding, searching, listing, tagging, importing, exporting, updating, and deleting saved links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[god4saken](https://clawhub.ai/user/god4saken)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to operate a local buku bookmark database through non-interactive CLI commands for bookmark creation, search, listing, tagging, import, export, update, and deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill normalizes deletion commands that bypass confirmation and can remove individual bookmarks, ranges of bookmarks, or tags from the local buku database.

Mitigation: Before delete, range delete, tag deletion, import, or export operations, require the agent to show the matching bookmarks and get explicit confirmation of the exact index, range, tag, or file path.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, guidance, configuration]

**Output Format:** [Markdown guidance with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target a local buku bookmark database, including operations that can modify or remove saved bookmarks.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
