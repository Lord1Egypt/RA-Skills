## Description:

Counts files in a local folder and can summarize the distribution of file types before an indexing workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xjkvbnwe](https://clawhub.ai/user/xjkvbnwe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to estimate the number of files in a local directory and decide whether a folder is small enough to index directly or needs filtering or a slower background workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented PowerShell command references a count_files.ps1 script that is not included in the inspected package.

Mitigation: Confirm the script exists in the deployment environment or replace the command with a reviewed local counting command before use.

Risk: Counting very large folders can take a long time, especially when collecting file type distribution.

Mitigation: Use the fast count-only mode first and narrow the folder or filter file types before detailed analysis.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with PowerShell command examples and plain-text file count summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include total file counts, a file extension breakdown, and indexing guidance based on folder size.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
