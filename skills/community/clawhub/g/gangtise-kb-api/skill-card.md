## Description: <br>
Searches the Gangtise internal knowledge base for semantically relevant excerpts from reports, opinions, meeting notes, and related documents, with optional file download by type and ID. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gangtisegts](https://clawhub.ai/user/gangtisegts) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Credentialed Gangtise users use this skill to retrieve, summarize, cite, and reason over relevant internal knowledge-base content such as research reports, internal reports, meeting notes, chief analyst views, and announcements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Gangtise credentials to query internal content. <br>
Mitigation: Use least-privilege credentials where possible and keep scripts/.authorization and credential environment variables out of source control and logs. <br>
Risk: Search results, excerpts, reports, or downloaded files can be saved locally. <br>
Mitigation: Avoid shared output directories, enable local saving or downloads only when needed, and delete saved excerpts or reports when no longer required. <br>
Risk: The agent can access internal knowledge-base content through the configured credentials. <br>
Mitigation: Install only in environments where the agent is intended to query Gangtise internal content, and review retrieved content before external sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gangtisegts/gangtise-kb-api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown-like text containing matched excerpts, titles, dates, file types, and source IDs, with optional saved PDF or Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Gangtise access credentials; optional local save and download behavior is controlled by environment variables and CLI flags.] <br>

## Skill Version(s): <br>
1.4.3 (source: server release evidence; artifact metadata reports 1.4.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
