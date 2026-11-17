## Description:

Analyzes binary files with Dr. Binary and Ghidra-backed tools to identify behavior, malicious indicators, decompiled functions, and threat assessment details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepbitstech](https://clawhub.ai/user/deepbitstech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security analysts use this skill to upload a selected binary to the Dr. Binary sandbox, inspect metadata and Ghidra-derived analysis, and produce a Markdown threat assessment with recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected binaries are uploaded to a remote Dr. Binary/Deepbits analysis service.

Mitigation: Use only with files approved for external analysis, and do not submit confidential samples without approval.

Risk: The upload helper reads values from a shared .env path.

Mitigation: Provide only DRBINARY_API_KEY for this workflow and keep unrelated secrets out of the shared .env path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deepbitstech/skills/binary-analysis)
- [Remote sandbox upload endpoint](https://mcp.deepbits.com/workspace/upload)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with file metadata, detailed findings, threat assessment, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local shell commands and remote analysis tool calls for the selected binary.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
