## Description: <br>
The agntdata X API helps agents and automations use one API key to retrieve structured X posts, profiles, followers, search, hashtag, trend, and text-analysis data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaencarrodine](https://clawhub.ai/user/jaencarrodine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation builders, marketing teams, research teams, and data teams use this skill to query X posts, profiles, followers, search results, hashtags, trends, and related text-analysis endpoints through agntdata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AGNTDATA_API_KEY and sends X queries, account identifiers, tweet IDs, use-case text, and analysis or translation text to agntdata. <br>
Mitigation: Use a dedicated API key where possible, monitor usage, avoid sending secrets or sensitive personal data, and review requests before execution. <br>
Risk: The artifact recommends an optional plugin that is separate from this instruction-only skill. <br>
Mitigation: Review and approve any plugin separately before installation. <br>


## Reference(s): <br>
- [agntdata X API Reference](https://agnt.mintlify.app/apis/social/x) <br>
- [agntdata Documentation](https://agnt.mintlify.app) <br>
- [ClawHub Skill Page](https://clawhub.ai/jaencarrodine/agntdata-x) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with curl examples and JSON API schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGNTDATA_API_KEY for authenticated requests and curl for command examples.] <br>

## Skill Version(s): <br>
1.0.15 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
