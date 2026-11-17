## Description:

FCPX Assistant helps agents automate Final Cut Pro X video production workflows, including script generation, media collection, TTS voiceover, video assembly, color grading, B-roll insertion, publishing, and editing support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lasbder-ops](https://clawhub.ai/user/lasbder-ops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and video-production operators use this skill to generate scripts, collect media, create voiceovers, assemble videos, apply finishing steps, and prepare platform-specific publishing workflows for Final Cut Pro X projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Web UI and scripts may permit unauthenticated command execution.

Mitigation: Do not run the Web UI on a networked machine; bind it to localhost with authentication and remove shell=True or eval-style command construction before installation.

Risk: Automation may delete unrelated media files during cleanup.

Mitigation: Disable broad cleanup by default, scope cleanup to known temporary directories, and review target paths before execution.

Risk: Publishing workflows handle cookies and tokens.

Mitigation: Store publishing credentials outside the project with restricted permissions and isolate them from the automation environment.

Risk: Unpinned dependencies and HTTP downloads can change behavior or fetch content insecurely.

Mitigation: Pin dependencies and avoid forced HTTP downloads before deployment.

## Reference(s):

- [FCPX Assistant ClawHub page](https://clawhub.ai/lasbder-ops/skills/fcpx-assistant)
- [Dependencies and TTS deployment](references/dependencies.md)
- [Publishing configuration](references/publishing.md)
- [Style options and parameters](references/styles-options.md)
- [Pexels API](https://www.pexels.com/api/)
- [Pixabay API docs](https://pixabay.com/api/docs/)
- [DashScope compatible API](https://dashscope.aliyuncs.com/compatible-mode/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local scripts, external media APIs, TTS tools, and publishing credential configuration.]

## Skill Version(s):

3.0.0-beta (source: server release metadata; artifact/package.json reports 2.4.2-beta)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
