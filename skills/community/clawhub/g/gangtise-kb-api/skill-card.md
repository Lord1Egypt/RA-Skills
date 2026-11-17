## Description:

Searches the Gangtise internal knowledge base for semantically relevant passages from reports, viewpoints, meeting notes, and related documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gangtisegts](https://clawhub.ai/user/gangtisegts)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve, cite, and summarize relevant content from Gangtise knowledge-base documents when they care about the document text rather than only locating files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends credential-bearing requests to Gangtise API endpoints.

Mitigation: Install it only where Gangtise credentials are intended for this skill, use scoped credentials where possible, and keep endpoint environment variables controlled.

Risk: The skill can write retrieved search results and downloaded documents to local workspace paths.

Mitigation: Run it in a contained workspace and review file download behavior before relying on direct downloads.

Risk: Search results may include proprietary or sensitive internal knowledge-base content.

Mitigation: Review retrieved passages before sharing or using them in downstream deliverables.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gangtisegts/skills/gangtise-kb-api)

## Skill Output:

**Output Type(s):** [Markdown, Files, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown search results with optional downloaded PDF or Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include titles, document dates, content excerpts, file types, and source IDs; optional downloads write files into a Gangtise workspace.]

## Skill Version(s):

1.4.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
