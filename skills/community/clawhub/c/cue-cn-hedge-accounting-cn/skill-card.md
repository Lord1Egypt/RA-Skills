## Description:

Converts hedge-accounting disclosures in financial reports into a source-linked register, with each finding tied to a verbatim quotation, location anchor, and [S#] reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Financial analysts and accounting reviewers use the skill to turn annual or interim report disclosures into a seven-section hedge-accounting register. It records only what the source states and leaves strategy judgments, valuation, exposure estimates, ratings, and price targets to human reviewers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan rates the release suspicious because it reports unrelated MCP catalog and credential-routing behavior alongside the hedge-accounting purpose; the scan is partial.

Mitigation: Avoid installation until those steps are removed or justified and the destination is independently validated. If using the skill, do not provide credentials or sensitive attachments until their destination is understood.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-cn-hedge-accounting-cn)
- [Cue MCP documentation](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader documentation](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Chinese Markdown structured register]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Seven fixed sections; findings retain source quotations, location anchors, and [S#] references, while missing information is stated explicitly. Python 3 is used for local checking. CUE_API_KEY is optional for live retrieval and attachment parsing.]

## Skill Version(s):

0.1.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
