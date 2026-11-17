## Description:

Checks figure references in manuscripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Authors, editors, and writing-focused developers use this skill to find figure references in manuscript text and support consistency review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current script checks text passed on the command line rather than reading a manuscript file, so documented path-based usage may produce incomplete or misleading results.

Mitigation: Treat results as limited to the provided argument string and verify behavior with representative manuscript inputs before relying on path-based checks.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text command-line output with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports sorted figure-reference identifiers found in the supplied manuscript argument.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
