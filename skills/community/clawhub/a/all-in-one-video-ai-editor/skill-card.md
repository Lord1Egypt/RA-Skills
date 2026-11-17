## Description:

This skill helps agents upload MP4 or MOV footage to Sparki, create AI video editing projects with style and format parameters, poll for completion, and return a time-limited processed video URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sparki-dev](https://clawhub.ai/user/sparki-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to automate AI-assisted video edits such as short-form clips, captions, commentary, resizing, highlights, vlogs, montages, and talking-head edits from local source videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Sparki API key and user videos to a hardcoded API domain that is not visibly under sparki.io.

Mitigation: Verify that agent-api-test.aicoding.live is authorized by Sparki before use, and avoid uploading sensitive or regulated videos until provider handling and retention are understood.

Risk: The documented key-status command can print the SPARKI_API_KEY value when it is configured.

Mitigation: Check only whether the variable is set, and do not echo or log the secret value.

Risk: Processed output is delivered through a time-limited result URL that may expose the edited video to anyone with the link while valid.

Mitigation: Treat result URLs as sensitive, share them only with intended recipients, and download required outputs promptly.

## Reference(s):

- [Sparki](https://sparki.io)
- [ClawHub skill page](https://clawhub.ai/sparki-dev/skills/all-in-one-video-ai-editor)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and result URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a 24-hour download URL after asynchronous upload and processing completes.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
