## Description:

Researches public Douyin search results, trending topics, creator posts, video details, and comments to identify content and audience opportunities for further validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content strategists, social media operators, marketers, and product teams use the skill to explore Douyin trends, compare public creator content, and summarize audience feedback as hypotheses for follow-up research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied Douyin links are sent to the third-party Guaikei API to retrieve results.

Mitigation: Disclose this data flow and confirm the user is authorized to share the requested terms or links before querying.

Risk: The security scan had medium confidence and only partial static inspection, leaving some executable components unassessed.

Mitigation: Review unassessed executable components before relying on the skill in a production environment.

Risk: The skill requires an API token in GUAIKEI_API_TOKEN.

Mitigation: Keep the token in the environment and avoid placing it in prompts, command examples, or shared output.

## Reference(s):

- [Demand mining guide](artifact/references/demand-mining.md)
- [Command options](artifact/references/options.md)
- [Guaikei service](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyin-opportunity-research)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Markdown]

**Output Format:** [Structured JSON result envelopes with concise Markdown or analysis summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public content and engagement data for agent analysis; summaries should select relevant fields rather than reproduce full result payloads.]

## Skill Version(s):

1.4.2 (source: SKILL.md frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
