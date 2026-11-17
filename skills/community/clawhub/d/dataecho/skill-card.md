## Description:

Deploys files, static sites, and server-side apps built by agents to live DataEcho URLs, and provides private cloud Drives for agent file storage and handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohocp](https://clawhub.ai/user/mohocp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to publish generated files, static websites, and containerized server applications to DataEcho, update existing deployments, claim anonymous sites, and manage private Drive-based handoff storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote installer commands could change after review.

Mitigation: Review installer contents before use, pin and verify downloads, or replace the remote installer flow with bundled scripts.

Risk: The skill can send user files, source code, or generated applications to the DataEcho service.

Mitigation: Use it only when the user explicitly wants publication or storage on DataEcho, and check deployment contents for secrets or private data before upload.

Risk: The workflow handles a long-lived DataEcho API key.

Mitigation: Store the key with restrictive file permissions, avoid printing it in logs or chat, and rotate it if exposure is suspected.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/mohocp/dataecho/tree/main/skills/dataecho)
- [ClawHub skill page](https://clawhub.ai/mohocp/skills/dataecho)
- [DataEcho homepage](https://dataecho.ai)
- [DataEcho agent context](https://dataecho.ai/llms-full.txt)
- [DataEcho OpenAPI specification](https://dataecho.ai/openapi.json)
- [DataEcho documentation](https://dataecho.ai/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell, PowerShell, Dockerfile, and REST API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce deployment commands, Dockerfile guidance, API request examples, live URL handling instructions, and credential storage guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
