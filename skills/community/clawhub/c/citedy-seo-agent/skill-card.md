## Description: <br>
Full-stack AI marketing toolkit for scouting social trends, competitor research, content-gap analysis, SEO and GEO article generation, social post adaptation, URL ingestion, lead magnets, short-form video generation, Google Search Console reporting, and automated content sessions through Citedy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nttylock](https://clawhub.ai/user/nttylock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, founders, SEO practitioners, and content operators use this skill to research topics and competitors, generate or adapt content, publish to connected channels, and manage recurring content automation from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend Citedy credits through paid generation, scouting, social adaptation, and automation workflows. <br>
Mitigation: Set spend and cadence limits, check the account balance before expensive operations, and require user approval before paid generation or recurring sessions. <br>
Risk: The skill can publish public articles, social posts, and short-form video to connected accounts. <br>
Mitigation: Require explicit approval before public posting and confirm the target connected accounts and platforms before publishing. <br>
Risk: The skill requires a sensitive Citedy API key that authorizes actions against the user's connected marketing accounts. <br>
Mitigation: Store the API key only in the local agent configuration, avoid exposing it in transcripts or logs, and revoke or rotate it from the Citedy dashboard when needed. <br>
Risk: The skill includes recurring sessions, webhook management, deletes, settings changes, and API key rotation behaviors. <br>
Mitigation: Require explicit approval for recurring automation, webhook changes, deletes, settings changes, and API key rotation; know how to pause sessions and revoke the key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nttylock/citedy-seo-agent) <br>
- [Citedy](https://www.citedy.com) <br>
- [Citedy privacy policy](https://www.citedy.com/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration, Text, Markdown] <br>
**Output Format:** [Markdown instructions with shell commands, HTTP request examples, and human-readable summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CITEDY_API_KEY for authenticated Citedy API calls.] <br>

## Skill Version(s): <br>
3.6.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
