## Description: <br>
Use one API key to pull YouTube channel, video, search, comments, subtitle, trend, and recommendation data as structured JSON for agents, automations, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaencarrodine](https://clawhub.ai/user/jaencarrodine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation builders, analytics teams, and product teams use this skill to query YouTube metadata, search results, trends, comments, subtitles, recommendations, channel details, and channel email lookup endpoints through AGNTDATA. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive AGNTDATA API key and sends YouTube queries, channel IDs, URLs, and use-case details to AGNTDATA. <br>
Mitigation: Install only when the publisher and AGNTDATA are trusted, keep the API key in AGNTDATA_API_KEY, and avoid sharing unnecessary sensitive context in requests. <br>
Risk: The skill includes channel email lookup endpoints without clear privacy or authorized-use limits. <br>
Mitigation: Use email lookup only for lawful, authorized purposes, avoid bulk collection or unsolicited outreach, and review applicable privacy obligations before use. <br>


## Reference(s): <br>
- [AGNTDATA YouTube API Reference](https://agnt.mintlify.app/apis/social/youtube) <br>
- [AGNTDATA Documentation](https://agnt.mintlify.app) <br>
- [ClawHub Skill Page](https://clawhub.ai/jaencarrodine/agntdata-youtube) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with curl commands and JSON API schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AGNTDATA_API_KEY and curl for authenticated requests.] <br>

## Skill Version(s): <br>
1.0.15 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
