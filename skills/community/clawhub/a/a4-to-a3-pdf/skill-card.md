## Description:

Merges numbered images from a folder into an A3 landscape PDF with two A4-sized images placed side by side on each page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangchuang9523-gif](https://clawhub.ai/user/wangchuang9523-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and document-processing users can use this skill to create A3 landscape PDFs from ordered image scans or photos, placing two A4 pages side by side per PDF page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper processes local image files and depends on Pillow.

Mitigation: Run it in a virtual environment and consider pinning the Pillow version before use.

Risk: The script primarily searches for numerically named .jpg files and has limited fallback extension handling.

Mitigation: Confirm input files are numbered in the expected order and extension format before generating the PDF.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangchuang9523-gif/skills/a4-to-a3-pdf)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, files]

**Output Format:** [Markdown guidance with shell command examples; the helper script produces a PDF file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local Python script with Pillow; default output is A3 landscape at 300 DPI.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
