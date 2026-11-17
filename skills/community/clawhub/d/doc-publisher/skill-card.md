## Description:

Doc Publisher helps an agent convert local Markdown document series into WeChat Official Account draft articles and publish records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[403914291](https://clawhub.ai/user/403914291)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to scan local Markdown files, format them for WeChat Official Account articles, create drafts through the WeChat API, and record publication results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports hardcoded credential-like values and WeChat secret handling.

Mitigation: Replace credential-shaped examples with placeholders, store real credentials only in a local .env file, and rotate any real WeChat secret that may have been exposed.

Risk: The security review reports unsafe account-level draft-clearing scripts.

Mitigation: Avoid running draft-clearing utilities until confirmation prompts, backups, and targeted deletion safeguards are added.

Risk: The security review reports cross-skill credential handling through sibling .env access.

Mitigation: Remove sibling .env lookup behavior and restrict credential loading to the skill's own explicitly configured environment file.

Risk: Markdown and HTML are transformed before preview or publication.

Mitigation: Sanitize untrusted Markdown and HTML before previewing or publishing content to WeChat.

## Reference(s):

- [Doc Publisher ClawHub page](https://clawhub.ai/403914291/skills/doc-publisher)
- [Project documentation homepage](https://docs.esupagent.com)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WeChat-styled HTML content, WeChat draft API calls, and publish-record JSON files when the bundled scripts are executed.]

## Skill Version(s):

1.0.0 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
