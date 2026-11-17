## Description:

Query bird information from dongniao.net using web_fetch. Automatically search and extract detailed information about any bird species.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leogaga](https://clawhub.ai/user/leogaga)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to look up bird species by Chinese, English, or scientific name and receive concise species details such as features, habitat, distribution, and conservation status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bird lookups contact dongniao.net, so use depends on network availability and third-party site behavior.

Mitigation: Disclose outbound access before installation and verify the site is appropriate for the deployment environment.

Risk: CLI use may require the Python requests package.

Mitigation: Install dependencies in an isolated environment and pin requests when packaging this skill for broader use.

Risk: Species data comes from public web sources and may be incomplete or outdated for scientific or conservation decisions.

Mitigation: Cross-check critical information with primary sources or qualified experts before relying on it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leogaga/skills/bird-info)
- [Dongniao](https://dongniao.net)
- [Dongniao Taxonomy](https://dongniao.net/taxonomy.html)
- [IOC World Bird List](https://www.worldbirdnames.org/)
- [China Birdwatching](https://www.birdwatch.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown-style sections with source attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The command-line path exits nonzero when a lookup fails or required dependencies are unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
