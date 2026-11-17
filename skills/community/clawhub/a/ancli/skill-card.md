## Description:

Read and write Apple Notes from the command line on macOS: list folders and notes, search, show, create, append, move and delete, with JSON output for agent use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopaljigaur](https://clawhub.ai/user/gopaljigaur)

### License/Terms of Use:

MIT-0

## Use Case:

macOS users and agents use the CLI to find and manage Apple Notes, including reading selected notes and creating, editing, moving, or deleting notes. The JSON output supports command-line workflows and agent use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release bundle omits JXA automation scripts, so their runtime safeguards could not be verified.

Mitigation: Review the exact npm version and its missing JXA scripts before granting Notes Automation access. Grant access only if you want the agent to read and modify notes, confirm deletions, and avoid permanent deletion unless intended.

## Reference(s):

- [Apple Notes CLI on ClawHub](https://clawhub.ai/gopaljigaur/skills/ancli)
- [@gopaljigaur/ancli on npm](https://www.npmjs.com/package/@gopaljigaur/ancli)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON or human-readable command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the local Notes library and the terminal's granted Notes Automation access.]

## Skill Version(s):

0.1.2 (source: package.json; server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
