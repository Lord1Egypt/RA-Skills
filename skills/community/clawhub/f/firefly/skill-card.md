## Description: <br>
Fetch meeting transcripts, summaries, and action items from Firefly AI (fireflies.ai). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codes71](https://clawhub.ai/user/codes71) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and teams that use Fireflies.ai can use this skill to list recent meetings, retrieve summaries and action items, search meeting records, and fetch transcripts with an approved API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting transcripts, summaries, action items, and participant details can contain sensitive business or personal information. <br>
Mitigation: Retrieve only meeting data the user requests, prefer summaries or targeted searches for vague requests, and avoid exposing transcript content unnecessarily. <br>
Risk: Fetching or saving full transcripts can retain large amounts of sensitive meeting content in the workspace. <br>
Mitigation: Confirm before retrieving full transcripts for vague requests and save transcript files only when the user is comfortable retaining that content. <br>
Risk: Custom GraphQL queries can request broader meeting data than needed. <br>
Mitigation: Use the predefined list, summary, transcript, and search commands first, and limit custom queries to clearly requested fields. <br>


## Reference(s): <br>
- [Firefly AI API Reference](references/api.md) <br>
- [Firefly AI GraphQL API](https://api.fireflies.ai/graphql) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown meeting lists, summaries, action items, search results, and timestamped transcript lines.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FIREFLY_API_KEY. Full transcripts can be long and should be saved to the workspace only when retention is acceptable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
