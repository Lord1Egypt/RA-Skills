## Description:

Extract valid downloadable URLs from Array[String] structures, clean and standardize them, then output directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract valid HTTP and HTTPS download URLs from JSON arrays or code snippets and return them as clean, line-separated text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided arrays or snippets may contain sensitive URLs.

Mitigation: Only provide arrays and snippets that are appropriate for the agent to process.

Risk: Extracted URLs may point to untrusted or unsafe downloads.

Mitigation: Review and validate URLs before opening or downloading content.

## Reference(s):

- [Array Url Extractor on ClawHub](https://clawhub.ai/openlark/skills/array-url-extractor)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text with one URL per line]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No explanatory prose; only valid downloadable HTTP or HTTPS URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
