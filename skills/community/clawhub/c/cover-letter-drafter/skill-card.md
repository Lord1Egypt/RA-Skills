## Description:

Generates professional cover letters for journal submissions and job applications in medical and academic contexts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, and academic professionals use this skill to draft journal submission, job application, and fellowship cover letters from recipient details and key points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional output path can overwrite arbitrary writable files because the script does not enforce path limits or overwrite protection.

Mitigation: Use a dedicated workspace output filename and avoid existing files, absolute paths, parent-directory paths, and symlinked destinations until path validation and overwrite protection are added.

## Reference(s):

- [Cover Letter Drafter Guidelines](references/guidelines.md)
- [Cover Letter Drafter on ClawHub](https://clawhub.ai/aipoch-ai/skills/cover-letter-drafter)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [JSON containing a cover letter, purpose, and word count; optionally saved as a JSON file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The output path is user supplied when file output is requested.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
