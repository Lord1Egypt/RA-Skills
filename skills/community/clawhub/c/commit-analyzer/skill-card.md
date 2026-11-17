## Description:

Analyzes git commit frequency, categories, and timing to assess autonomous operation health and detect idle or breakthrough periods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobrenze-bot](https://clawhub.ai/user/bobrenze-bot)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to inspect local git commit patterns, summarize work distribution, and identify low-activity or idle periods in autonomous operation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Numeric days or hours parameters are handled unsafely enough to warrant review before use.

Mitigation: Install only from a specific reviewed commit or release, and avoid passing untrusted text into numeric parameters until bounded positive integer validation is added.

Risk: Generated reports may expose local commit messages in terminal output.

Mitigation: Run the analyzer only in repositories whose commit history may be shown to the current operator or downstream log consumers.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Terminal text reports with optional JSON health-check output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local git history and may display commit messages in terminal output.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
