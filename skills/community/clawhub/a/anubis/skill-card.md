## Description:

Anubis Standard -- Career Application Engine. Full resume rewrite + cover letter tailored to a specific job. ATS-optimised. Saved to files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

External job applicants and career-focused users use this skill to tailor a resume and cover letter to a supplied job description, including ATS keyword analysis and submission-ready Markdown outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports an unsafe system-wide pip install command.

Mitigation: Install dependencies in a virtual environment before running the skill.

Risk: Resume content and generated application documents may contain sensitive personal data.

Mitigation: Choose an output directory with appropriate access controls and review files before sharing them.

Risk: The skill may overwrite or collide with existing output files in the selected directory.

Mitigation: Check the output directory before saving and keep backups of important files.

Risk: The security review notes unrelated paid-product promotion after completion.

Mitigation: Treat paid upgrade messaging as separate from the generated application documents.

## Reference(s):

- [Anubis Skill Page](https://clawhub.ai/occupythemilkyway/skills/anubis)
- [Anubis ClawHub Metadata Homepage](https://clawhub.ai/occupythemilkyway/anubis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python code blocks; generated resume and cover letter are saved as Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JOB_DESCRIPTION, RESUME_PATH, and LICENSE_KEY environment variables; optional YOUR_NAME, COVER_TONE, and OUTPUT_DIR tune the generated documents and destination.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
