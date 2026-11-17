## Description:

Guides an agent to create ai.fun.tv text-to-image projects, submit prompts with the Fun-GP-image2 default model, poll for results, return image URLs, and optionally save generated images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amireux0013](https://clawhub.ai/user/amireux0013)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate prompt-based images with ai.fun.tv for posters, promotional visuals, social cover images, and related creative workflows. The skill handles token lookup, project creation, task submission, result polling, and optional local downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist an ai.fun.tv authentication token in a local authorization.txt file.

Mitigation: Prefer an environment variable or --authorization with --no-save-authorization, keep the skill directory private, and review file permissions before use with real credentials.

Risk: The script can download provider-supplied image URLs to a local output directory.

Mitigation: Use --output-dir only when the provider-returned URLs are trusted and local downloads are acceptable for the environment.

Risk: The security verdict is suspicious due to credential persistence and URL download behavior.

Mitigation: Review the skill before installing or running it with account credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amireux0013/skills/ai-fun-tv-image)
- [ai.fun.tv](https://ai.fun.tv)
- [ai.fun.tv OpenClaw authentication](https://ai.fun.tv/openclaw)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls, Files]

**Output Format:** [JSON responses with image URLs and optional local file paths; guidance may include Markdown with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an ai.fun.tv authorization token; defaults to Fun-GP-image2 and can request one to four images per run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
