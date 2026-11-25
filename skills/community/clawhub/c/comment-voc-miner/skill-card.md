## Description:

Turn public social comments or comments supplied by the user into an audience-language brief with objections, verbatim lines, purchase concerns, FAQs, live-commerce replies, and spoken hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beatra-ai](https://clawhub.ai/user/beatra-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and commerce teams use this skill to turn a public post's comments or comments they supply into an audience insight brief. The brief supports FAQ writing, live-commerce replies, and spoken hooks grounded in the comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marked this skill suspicious for broad account permissions and persistent installation reporting.

Mitigation: Review the permission requests and reporting behavior; the review recommends avoiding installation until they are narrowed and explained.

Risk: The review also flags shared-credential cleanup and says its scan is incomplete because some local references were unresolved.

Mitigation: Inspect the uninstall and shared-state guidance, and resolve the missing references before authorizing installation.

## Reference(s):

- [Comment lookup and supported platforms](references/comment-lookup.md)
- [Writing the comment brief](references/brief.md)
- [Comment brief workflow](references/workflow.md)
- [Installation and authentication](references/installation-and-auth.md)
- [Updates and security](references/updates-and-security.md)
- [Uninstall and disconnect](references/uninstall-and-disconnect.md)
- [Beatra skill homepage](https://beatra.ai/skills/comment-voc-miner)
- [Beatra MCP service](https://mcp.beatra.ai/mcp)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Structured Markdown brief with grouped insights and comment-attributed quotes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes objections, verbatim lines, FAQs, live-commerce replies, and spoken hooks; findings are grounded in supplied or looked-up comments.]

## Skill Version(s):

0.2.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
