## Description: <br>
Bookmark intelligence for developers. Browse, search, triage, and manage your AI-analyzed library. Submit URLs, assign projects, trigger deep analysis, and execute staged items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bonesvinyl](https://clawhub.ai/user/bonesvinyl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to browse, search, triage, submit, and update BKMRK bookmarks analyzed against their coding projects. It helps manage bookmark status, project context, deep analysis, and URL submission through the BKMRK API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a BKMRK API key and the user's bookmark library. <br>
Mitigation: Keep the API key private, rotate it if exposed, and install only when the user trusts BKMRK with bookmark content. <br>
Risk: Bookmark content may be processed by BKMRK and Claude for analysis. <br>
Mitigation: Avoid submitting sensitive URLs or bookmark content unless that external processing is acceptable. <br>
Risk: Bulk status changes can trash or alter many bookmarks. <br>
Mitigation: Require explicit user approval before bulk trashing or changing many bookmark statuses. <br>


## Reference(s): <br>
- [BKMRK homepage](https://bkmrkapp.com) <br>
- [BKMRK agent API documentation](https://bkmrkapp.com/agent.json) <br>
- [ClawHub skill page](https://clawhub.ai/bonesvinyl/bkmrk) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, text, configuration] <br>
**Output Format:** [Markdown with HTTP request examples and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a BKMRK API key for authenticated library, project, status, and analysis endpoints.] <br>

## Skill Version(s): <br>
1.4.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
