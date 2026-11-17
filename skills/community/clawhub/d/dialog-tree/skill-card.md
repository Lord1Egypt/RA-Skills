## Description:

Dialog Tree helps an agent maintain a local visual map of a branching conversation using a project data file and a self-contained HTML viewer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ikotelkin](https://clawhub.ai/user/ikotelkin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve a navigable map of complex, branching conversations. It is useful when open questions, decisions, and follow-up paths need to survive context loss or later sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated node HTML is rendered as active browser content in the local viewer.

Mitigation: Review generated node content before opening the viewer, and avoid adding untrusted HTML or script-like content to tree data.

Risk: The documented smoke test evaluates the tree data file, which can execute modified JavaScript.

Mitigation: Run the validation only on trusted, locally generated tree data or replace it with a non-evaluating parser-based check.

Risk: Using an on-demand static server can introduce avoidable local execution or dependency risk.

Mitigation: Prefer an already-installed or pinned local static server bound to localhost, and review commands before execution.

## Reference(s):

- [dialog-tree ClawHub release](https://clawhub.ai/ikotelkin/skills/dialog-tree)
- [Claude Code skills documentation](https://code.claude.com/docs/en/skills)
- [README](README.md)
- [Screenshot](docs/screenshot.jpg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript and HTML project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates a paired tree data file and self-contained HTML viewer in the user's project.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
