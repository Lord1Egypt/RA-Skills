## Description:

Generate professional baby photo books from photos with intelligent layout, automatic age-stage organization, whitespace-minimizing layouts, and print-ready PDF output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atmosphere16happy](https://clawhub.ai/user/atmosphere16happy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn a local folder of baby photos into a printable A4 photo book with cover, age-stage chapters, photo pages, and date or age annotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes private family photos from the selected folder and scans subdirectories.

Mitigation: Run it in a dedicated virtual environment, avoid administrator or root execution, and point it only at the photo folder intended for the book.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atmosphere16happy/skills/baby-photo-book)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands; generated artifact is a PDF file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an A4 PDF from a local photo folder using Pillow and ReportLab.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
