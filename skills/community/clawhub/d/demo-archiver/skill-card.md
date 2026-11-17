## Description:

A demo skill for archiving and organizing files into a structured resource library.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and file-management automation users can use this demo skill to guide archiving incoming files into dated directories with metadata sidecar and index tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact refers to a separate archive script, but no script is bundled or reviewed here.

Mitigation: Inspect and test any archive script separately before use, especially before allowing it to move or reorganize files.

Risk: Archiving workflows can move source files into dated directories and write metadata sidecar files.

Mitigation: Run the workflow on test data or backed-up files first and review the generated archive index before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/demo-archiver)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with ordered steps and inline paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No bundled executable code; any archive script is external to the reviewed artifact.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
