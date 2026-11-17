## Description:

Generates academic survey drafts from a topic or recent arXiv papers, with topic selection, novelty checks, quality scoring, iterative improvement, and LaTeX/PDF output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vixuowis](https://clawhub.ai/user/vixuowis)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and academic users can use this skill to generate literature-survey drafts, organize recent arXiv papers, evaluate draft structure and references, and improve generated LaTeX content before human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically compiles arXiv and user-influenced LaTeX into PDFs.

Mitigation: Run it only in a restricted working directory, sandbox PDF compilation, and review generated citations and claims before use.

Risk: Recurring automated runs can repeatedly fetch, generate, and compile content without adequate safeguards.

Mitigation: Avoid enabling the hourly schedule unless the workflow has containment, monitoring, and manual review checkpoints.

Risk: The security evidence recommends stronger handling for transport, filenames, LaTeX content, and pdflatex execution.

Mitigation: Use HTTPS, enforce strict filename containment, escape LaTeX content, and execute pdflatex in a sandbox before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vixuowis/skills/academic-survey-self-improve)
- [arXiv API endpoint used by the artifact](http://export.arxiv.org/api/query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Command-line guidance and generated LaTeX/PDF survey files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create .tex, .pdf, topic history, figure, and enhanced-writing files in the configured output directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
