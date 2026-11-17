## Description:

Assists with a proactive CV-driven job search by analyzing the user's profile, estimating salary range, scanning job boards and career pages, scoring matches, drafting application materials, and tracking follow-ups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[askenaz](https://clawhub.ai/user/askenaz)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and their agents use this skill to turn a CV into a structured profile, calibrate salary expectations, discover and rank relevant job openings, draft tailored CV and cover-letter material, and maintain an application follow-up pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive CV, profile, job, and application data in local state files.

Mitigation: Install it in a private workspace, keep generated data out of shared profiles and source control, and avoid placing credentials in config.json.

Risk: Job posting text and board responses are untrusted inputs that can affect matching, drafting, and command arguments.

Mitigation: Confirm each web scan and file write, treat posting text as untrusted, and pass job JSON through files or stdin rather than inline shell arguments.

Risk: The scanner flagged the pinned PDF parser dependency as risky.

Mitigation: Update or avoid the pinned PDF parser before processing PDFs, or use TXT/MD CV inputs until the dependency risk is reviewed.

Risk: Salary estimates and match scores are heuristic and may be inaccurate or stale.

Mitigation: Review salary guidance against current market sources and use scores as decision support rather than as final hiring or application decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/askenaz/skills/cv-driven-job-hunter)
- [Job boards reference](artifact/references/job-boards.md)
- [Salary benchmarks reference](artifact/references/salary-benchmarks.md)
- [World-class companies reference](artifact/references/world-class-companies.md)
- [Application record schema](artifact/templates/application-record.schema.json)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON, with shell command suggestions and editable application draft files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user review before any application submission; stores local CV, profile, job, and application state under data/.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
