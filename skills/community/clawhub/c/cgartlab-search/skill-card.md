## Description:

Searches the internet across multiple backends and returns source-attributed results as a cited summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgartlab](https://clawhub.ai/user/cgartlab)

### License/Terms of Use:

CC-BY-NC-SA-4.0

## Use Case:

Developers and other users use this skill to find current web information, technical documentation, developer answers, news, sports coverage, and Chinese-language sources, then receive a cited summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to selected external providers and may disclose sensitive information.

Mitigation: Keep confidential details out of search terms.

Risk: API keys and stored secrets can be exposed if configured or stored carelessly.

Mitigation: Configure only the keys needed and protect the local secrets.json file.

Risk: The optional Tencent installer and its persistent key configuration can affect the local environment.

Mitigation: Review the installer before running it and understand where its key configuration persists.

## Reference(s):

- [Project source listed in release metadata](https://github.com/cgartlab/cgartlab-search)
- [Backend reference guide](references/backends.md)
- [Search routing guide](references/routing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Cited Markdown summary with source links and excerpts; the Node.js script can also emit normalized JSON search results.]

**Output Parameters:** [Search query, selected backend or backends, and optional result limit.]

**Other Properties Related to Output:** [Results depend on backend availability and configured credentials; unavailable sources are reported rather than fabricated.]

## Skill Version(s):

0.1.1 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
