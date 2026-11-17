## Description:

Fload helps agents use Fload MCP tools for mobile app analytics, reviews, growth metrics, ad performance, anomalies, and app store optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hassanbazzi](https://clawhub.ai/user/hassanbazzi)

### License/Terms of Use:

MIT-0

## Use Case:

Mobile app publishers and their agents use this skill to query Fload MCP tools for app health, reviews, analytics, ad performance, anomalies, growth scoring, and business overviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup runs npm/MCP code with a FLOAD_API_KEY.

Mitigation: Pin or verify the MCP package version, use a narrowly scoped FLOAD_API_KEY, and rotate the key if it is exposed.

Risk: Review-reply approval and rejection tools can publish or delete replies.

Mitigation: Require explicit human approval and review reply content before using approve_action or reject_action.

## Reference(s):

- [Fload app setup](https://app.fload.app)
- [ClawHub Fload skill page](https://clawhub.ai/hassanbazzi/skills/fload)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Fload MCP tools and a FLOAD_API_KEY when configured by the user.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter metadata.version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
