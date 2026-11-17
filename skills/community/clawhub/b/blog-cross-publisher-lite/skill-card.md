## Description:

Publish markdown articles to Dev.to via their REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apex-stack-ai](https://clawhub.ai/user/apex-stack-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to prepare and publish Markdown articles to Dev.to, either as drafts or live posts, using a Dev.to API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example command passes the Dev.to API key directly on the command line.

Mitigation: Use a secure secret prompt or protected environment/secret store instead of placing the API key directly in a shell command.

Risk: The example command includes `--publish`, which can make a post public immediately.

Mitigation: Omit `--publish` until the article has been reviewed and is ready for live publication.

Risk: Articles may accidentally include secrets or sensitive information.

Mitigation: Review the article for secrets and sensitive content before submitting it to Dev.to.

Risk: The referenced publishing script was not included in the inspected artifact.

Mitigation: Verify the actual publishing script before relying on the skill for production publishing.

## Reference(s):

- [Dev.to API articles endpoint](https://dev.to/api/articles)
- [Dev.to API key settings](https://dev.to/settings/extensions)
- [ClawHub skill page](https://clawhub.ai/apex-stack-ai/skills/blog-cross-publisher-lite)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides use of a Dev.to API key and publish/draft flags; users should review content and credentials before publishing.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
