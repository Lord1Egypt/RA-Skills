## Description:

AI Video Translation guides agents through using the newtranx CLI to translate MP4 videos from local files or URLs and export translated video, subtitle, and speaker metadata outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxj127](https://clawhub.ai/user/wxj127)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and operators use this skill to run terminal-based video and podcast translation workflows through newtranx, including login, MP4 upload, translation submission, status polling, and output retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to run a mutable npm package.

Mitigation: Only run the skill if the Newtranx package and publisher are trusted, and prefer a pinned version or locked local install.

Risk: The login flow stores a 15-day authentication token.

Mitigation: Review where the token is stored, limit the execution environment, and understand how to remove or revoke the token before use.

Risk: Video upload workflows can expose unrelated files or secrets from the execution environment.

Mitigation: Run the commands from a scoped working directory and avoid placing unrelated sensitive files in the environment used for uploads.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline bash code blocks and generated download links for video, subtitles, and metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports MP4 inputs from local files or HTTP URLs; documented limits are 5GB maximum file size and 4 hours maximum duration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
