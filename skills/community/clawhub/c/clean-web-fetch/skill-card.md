## Description:

Fetches readable webpage content and converts article bodies to Markdown, with WeChat cleanup, selector fallbacks, optional JSON output, and truncation to reduce token use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jllyzzd2023](https://clawhub.ai/user/jllyzzd2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve article, blog, news, and announcement bodies as clean Markdown or text when ordinary fetches are noisy or unreliable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release references missing or unreviewed fetch scripts, including a developer-specific absolute path.

Mitigation: Inspect and bundle executable scripts with the skill, resolve them relative to the skill package, and avoid developer-local paths before deployment.

Risk: The skill asks agents to fetch arbitrary webpages and install fetching dependencies.

Mitigation: Use an isolated environment with pinned dependencies and restrict fetching to user-approved public HTTP/HTTPS URLs.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown text by default, with optional JSON output and selector diagnostics on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a URL and max_chars value; output is truncated to the requested character limit.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
