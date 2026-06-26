## Description: <br>
Fireflies.ai GraphQL API integration with managed OAuth for accessing meeting transcripts, summaries, users, contacts, and AI-powered meeting analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect agents to Fireflies.ai through Maton so they can retrieve meeting transcripts, summaries, participant, user, and contact data, and perform AskFred meeting analysis. It also provides examples for approved GraphQL mutations such as transcript updates, audio uploads, user role changes, and live-meeting actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Fireflies meeting transcripts, audio, video URLs, participant data, and account metadata through Maton. <br>
Mitigation: Install only when that access is acceptable, keep MATON_API_KEY private, and request only the transcript or account fields needed for the user task. <br>
Risk: GraphQL mutations can create, update, delete, change roles, or affect live-meeting resources. <br>
Mitigation: Require explicit user confirmation of the target resource and intended effect before any create, update, delete, role-change, or live-meeting action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/fireflies-api) <br>
- [Fireflies API Documentation](https://docs.fireflies.ai/) <br>
- [Fireflies GraphQL API Reference](https://docs.fireflies.ai/graphql-api) <br>
- [Fireflies Developer Program](https://docs.fireflies.ai/getting-started/developer-program) <br>
- [Maton Settings](https://maton.ai/settings) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Python, JavaScript, GraphQL, JSON, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized Fireflies connection through Maton.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
