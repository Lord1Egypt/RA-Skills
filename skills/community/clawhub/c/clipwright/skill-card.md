## Description:

Make short videos through Clipwright's MCP server: an AI actor speaking your script, or a faceless video of up to 90 seconds with narration over generated scenes. Quote first for free, then start a run and collect the MP4. Clipwright returns the file and does not publish anywhere.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seocombat](https://clawhub.ai/user/seocombat)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to connect an agent to Clipwright, prepare and quote video jobs, and request short presenter-led or faceless narrated videos. The agent can also help retrieve completed media and troubleshoot the workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local server uses a changing npm dependency, and the hosted service and external package were not audited in the supplied security assessment.

Mitigation: Prefer the hosted connection or pin a reviewed local version, and restrict its access.

Risk: Scripts and selected media are sent to Clipwright; paid retries and diagnostic runs can incur charges.

Mitigation: Preview and approve feedback before sending it, exclude private scripts, credentials, and signed links, and approve paid retries or diagnostics.

## Reference(s):

- [Clipwright documentation](https://clipwright.io/docs)
- [Clipwright API OpenAPI specification](https://api.clipwright.io/openapi.json)
- [Clipwright changelog](https://clipwright.io/changelog)
- [Clipwright service](https://clipwright.io/?ref=clawhub)
- [Clipwright release on ClawHub](https://clawhub.ai/seocombat/skills/clipwright)

## Skill Output:

**Output Type(s):** [Video files (MP4), Guidance, Shell commands, Configuration]

**Output Format:** [MP4 video files; setup and workflow guidance in Markdown, shell commands, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presenter-led or faceless narrated short videos, up to 90 seconds; the service returns the file and does not publish it.]

## Skill Version(s):

0.36.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
