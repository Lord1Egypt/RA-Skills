## Description:

Generates AI portrait images through the DiversityFaces.org API for professional headshots, character design, fashion visualization, and diverse representation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luruibu](https://clawhub.ai/user/luruibu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative teams use this skill to guide agents through generating portrait images with the DiversityFaces.org API, including quota checks, prompt submission, status polling, and image retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portrait prompts, signup details, and BEAUTY_API_KEY are sent to DiversityFaces.org.

Mitigation: Use a scoped or disposable API key where possible, avoid private personal details in prompts, and install only if this data sharing is acceptable.

Risk: The artifact includes guidance that can encourage insecure API-key handling, including persistence in shell startup files, .env files, or command-line arguments.

Mitigation: Keep API keys out of persistent shell configuration, local dotenv files, logs, and command histories; pass secrets through a safer per-session secret mechanism when available.

Risk: Broad activation around portrait-generation requests could cause the skill to be invoked more often than intended.

Mitigation: Use the skill only for explicit adult portrait-generation workflows and review proposed API calls before execution.

Risk: Support, donation, and starring links appear in the artifact and could be surfaced as part of normal task output.

Mitigation: Treat those links as optional documentation and do not include them in normal generation responses unless the user asks for project support information.

## Reference(s):

- [DiversityFaces.org API homepage](https://gen1.diversityfaces.org)
- [ClawHub skill page](https://clawhub.ai/luruibu/skills/beauty-generation-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with curl commands and optional script templates; API responses are JSON and generated images are retrieved as files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and a user-provided BEAUTY_API_KEY; prompts and signup details are sent to DiversityFaces.org.]

## Skill Version(s):

1.2.52 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
