## Description:

2D Print helps agents send images, PDFs, and text files to local macOS CUPS printers with printer selection, copy count, paper size, orientation, color, quality, queue, and cancellation controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users can use this skill to have an agent prepare local CUPS commands for printing supported files, checking printer status, viewing queues, and cancelling print jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may print the wrong file, use the wrong printer, request too many copies, or send output to a remote or shared printer.

Mitigation: Confirm the exact file, printer, copy count, paper settings, and whether the selected printer is local, remote, or shared before running a print command.

Risk: Queue cancellation commands can remove active print jobs that the user intended to keep.

Mitigation: Review the queue and confirm the specific job ID before cancellation; avoid blanket cancellation unless the affected jobs are understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mayf3/skills/2d-print)
- [Publisher profile](https://clawhub.ai/user/mayf3)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target local macOS CUPS printers and should be confirmed before print or cancellation actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
