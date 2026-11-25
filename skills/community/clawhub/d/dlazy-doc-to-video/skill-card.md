## Description:

Turns user-provided documents into explainer, report, courseware, or training videos through dLazy's file-to-video workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can turn Word, Markdown, PDF, PowerPoint, Excel, or other documents into explainer, report, courseware, and training videos. The skill guides a dLazy CLI agent through a project-based workflow and follow-up revisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages, options, and attached files are sent to dLazy services, and attached files are uploaded to its media storage.

Mitigation: Review the dLazy service and install details, and attach only files you are comfortable sending to the service.

Risk: The security review notes that project-listing and login actions may not align with the document-to-video purpose, with some referenced materials unavailable.

Mitigation: Review the CLI actions and referenced materials before using the skill, especially during login or project discovery.

## Reference(s):

- [dLazy homepage](https://dlazy.com)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Video, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated video artifacts and text responses, with CLI commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-based multi-turn workflow; attached local files are uploaded to dLazy storage.]

## Skill Version(s):

1.0.42 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
