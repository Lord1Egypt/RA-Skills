## Description:

Uses the Flyelep AI Tool API to redraw selected regions of an image from a source image URL, text prompt, and optional reference or mask image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyelepai](https://clawhub.ai/user/flyelepai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to perform localized image edits, such as replacing backgrounds or modifying a specific region while preserving the main subject.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local images supplied for editing may be uploaded to Flyelep and exposed through permanent public links without a clear deletion path.

Mitigation: Ask for explicit user acceptance before uploading local files, and avoid identity documents, private photos, confidential designs, regulated data, or other sensitive images unless the user accepts that exposure.

Risk: The Flyelep secretKey could be exposed if written into files, examples, repositories, or logs.

Mitigation: Request the API key only at runtime, pass it in request headers, and do not persist it in skill files, configuration, examples, or shared logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flyelepai/skills/flyelep-partial-redrawing)
- [Flyelep partial redrawing API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/poster/aiTool/partialRedrawing)
- [Flyelep file upload API endpoint](https://www.flyelep.cn/prod-api/poster-design/api/v1/file/upload)
- [Flyelep control board](https://www.flyelep.cn/controlboard)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the redrawn image URL from the Flyelep API and instructs the agent not to read back image contents.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
