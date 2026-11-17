## Description:

Generates an ASCII tree or JSON representation of a directory structure. Use when you need to visualize file hierarchies, document folder contents, or debug directory layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to inspect, document, or debug local directory layouts by generating a readable folder tree or a structured JSON representation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recursive directory scans can follow symbolic links outside the selected folder.

Mitigation: Run the skill on trusted folders, avoid folders containing symbolic links, and add symlink handling before broader deployment.

Risk: The scan can run without a default depth limit and may enumerate large directory trees.

Mitigation: Use an explicit small --depth value when inspecting unfamiliar or large folders.

Risk: Output may expose local directory names and paths.

Mitigation: Review generated output before sharing it outside the intended audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanng-ide/skills/folder-tree-generator)

## Skill Output:

**Output Type(s):** [text, json]

**Output Format:** [ASCII tree text or pretty-printed JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file and directory names and paths; supports optional JSON output and recursion depth limits.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
