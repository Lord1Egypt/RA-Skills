## Description:

Cn Web Clipper extracts article content from web page URLs and saves the result as local Markdown, with optional cloud output modes described in the artifact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content workers use this skill to clip web articles into Markdown archives from supplied URLs. It is suited for local web research capture where users can review outbound requests and saved content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to user-supplied URLs and may fetch untrusted or internal resources if run in a privileged environment.

Mitigation: Run it only against trusted public URLs or in a network-restricted environment with appropriate outbound request controls.

Risk: Cloud output modes and credential handling are under-documented in the release evidence.

Mitigation: Review cloud integration behavior before enabling Feishu or Notion output, and avoid exposing credentials until that review is complete.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/freedompixels/skills/cn-web-clipper)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Files]

**Output Format:** [Markdown files with terminal status text and a JSON result object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes clipped content locally by default; optional Feishu and Notion modes are present but require separate dependency and credential review.]

## Skill Version(s):

1.2.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
