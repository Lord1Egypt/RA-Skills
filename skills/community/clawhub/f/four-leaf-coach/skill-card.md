## Description:

Four-Leaf Coach helps job seekers find postings, prepare and practice for interviews, assess résumé fit, track applications, and research compensation using Four-Leaf's hosted tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fourleafai](https://clawhub.ai/user/fourleafai)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers use this skill to find current openings, practice interviews with scored feedback, compare a résumé with job descriptions, manage applications, and prepare for compensation conversations. Live features require a connected Four-Leaf account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting the hosted service grants it access to Four-Leaf account data used for coaching.

Mitigation: Authorize the connection only if comfortable sharing the relevant account data with Four-Leaf.

Risk: Private compensation details, recruiter links, or confidential job descriptions may be processed by Four-Leaf or external search and fetch services.

Mitigation: Avoid providing sensitive material unless you intend it to be processed; check the destination before sharing.

Risk: Saving a job changes the user's application tracker.

Mitigation: Ask which jobs the user wants saved before updating the tracker.

## Reference(s):

- [Four-Leaf Coach release](https://clawhub.ai/fourleafai/skills/four-leaf-coach)
- [Four-Leaf tool reference](https://four-leaf.ai/oss)
- [MCP tools and account requirements](artifact/references/mcp-tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational Markdown with job listings, interview feedback, and sourced compensation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May link to job postings and update the user's application tracker only when requested; live data requires Four-Leaf access.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
