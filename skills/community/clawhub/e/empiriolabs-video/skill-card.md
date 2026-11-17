## Description:

Generate short video clips from text prompts or public image URLs with EmpirioLabs AI, track jobs, and save the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[empiriolabs](https://clawhub.ai/user/empiriolabs)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to generate or animate short video clips, check long-running jobs, and download the resulting media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, public image URLs, model settings, and generated media are shared with EmpirioLabs AI.

Mitigation: Use the service only for inputs and media you are comfortable sharing with EmpirioLabs AI.

Risk: The API key grants access to the EmpirioLabs AI account.

Mitigation: Keep EMPIRIOLABS_API_KEY in the environment; do not put it in prompts or project files.

Risk: Longer or higher-resolution video jobs can incur greater charges.

Mitigation: Check model prices and confirm costly renders with the user before submitting jobs.

Risk: The overwrite option can replace an existing output file.

Mitigation: Use --overwrite only when replacing an existing file is intended.

## Reference(s):

- [EmpirioLabs AI](https://empiriolabs.ai)
- [EmpirioLabs AI API documentation](https://docs.empiriolabs.ai)
- [EmpirioLabs AI MCP setup](https://docs.empiriolabs.ai/mcp)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text]

**Output Format:** [Markdown with shell commands and JSON job summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return hosted video URLs and save MP4 files to a user-selected path.]

## Skill Version(s):

1.0.0 (source: skill metadata and release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
