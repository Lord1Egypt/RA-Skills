## Description:

Create, edit, and ship ad creative through the AdMakeAI API, including ad images, edits, batch ad sets, copy, UGC video, Meta uploads, campaign drafts, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesmerlord](https://clawhub.ai/user/mesmerlord)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and marketing teams use this skill to guide an agent through AdMakeAI ad creation, editing, research, Meta upload, campaign draft, and analytics workflows while confirming credit-spending or write actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend AdMakeAI credits for generation, video, batch, and Meta upload workflows.

Mitigation: Confirm user intent before credit-spending actions, check credits before large batches, and prefer read or list calls when the request is exploratory.

Risk: The skill can push uploads or campaign drafts to Meta accounts when the user has connected Facebook.

Mitigation: Read the proposed Meta action back to the user and require explicit confirmation before creating uploads or pushing campaign drafts.

Risk: The skill requires an AdMakeAI API key and can access account, project, ad, and analytics data.

Mitigation: Read the key from ADMAKEAI_API_KEY, never echo or store it, and install only when the agent is intended to operate AdMakeAI ad workflows.

Risk: Generating into the wrong project can spend credits on the wrong brand or product.

Mitigation: List projects before generation, select only when the requested brand is clear, and ask for clarification when multiple projects match.

## Reference(s):

- [AdMakeAI Homepage](https://admakeai.com)
- [AdMakeAI API Documentation](https://admakeai.com/api/docs)
- [AdMakeAI API Key Dashboard](https://admakeai.com/dashboard/integrations/api)
- [ClawHub Skill Page](https://clawhub.ai/mesmerlord/skills/admakeai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API request examples, shell commands, and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, curl, and ADMAKEAI_API_KEY for live AdMakeAI API use.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
