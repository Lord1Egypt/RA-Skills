## Description:

Reviews finished AI video ads for platform and advertising compliance by extracting claims and depicted people, checking claims against seller evidence, and producing pass/fix/block findings with supporting rules, suggested rewrites, and disclosure labels; it is not legal advice or an ad-writing tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT

## Use Case:

External sellers and marketers use the skill to review finished AI product ads against platform and advertising requirements, compare claims with supporting evidence, and prepare a pass, fix, or block report with suggested rewrites and disclosure labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The video-analysis workflow may send ad videos or video URLs to an external provider, and the scanner guidance notes the lack of a clear notice before that transfer.

Mitigation: Tell users before analysis that videos or URLs may be sent to VARG; avoid sending unpublished or sensitive material unless they are comfortable with that transfer.

Risk: The security summary reports broad tool access.

Mitigation: Review the installed skill source and installer before use, and limit granted tools to those needed for the requested review.

Risk: ClawScan reports that scanning was partial because a local reference could not be resolved, so the evidence does not establish that every reference was reviewed.

Mitigation: Inspect the unresolved reference and the full skill source before relying on the compliance workflow.

## Reference(s):

- [VARG guide](https://varg.ai/how-to)
- [VARG MCP connection](https://mcp.varg.ai/mcp)
- [Skill rules](references/rules.json)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Markdown compliance report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pass/fix/block findings with timestamps, rule sources and dates, suggested rewrites, platform disclosure labels, and an overall verdict.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
