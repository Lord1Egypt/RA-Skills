## Description:

This skill should be used when users need to search the web for information, find current content, look up news articles, search for images, or find videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwirx](https://clawhub.ai/user/dwirx)

### License/Terms of Use:


## Use Case:

Developers and agents use Duckse to run web, news, image, video, and book searches through the duckse CLI for current research, fact-checking, and source discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions run an unverified remote installer directly in a shell.

Mitigation: Audit or replace the installer path before installation; prefer a pinned release or reviewed package and verify checksums or signatures when available.

Risk: Web search queries may leave the local environment and disclose sensitive terms.

Mitigation: Avoid searching for secrets, credentials, regulated data, internal project names, or other sensitive terms unless that disclosure risk is accepted.

## Reference(s):

- [Duckse ClawHub skill page](https://clawhub.ai/dwirx/skills/duckse)
- [duckse installer script](https://raw.githubusercontent.com/dwirx/duckse/main/scripts/install.sh)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands; duckse can return pretty text or JSON search results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports search type, result count, time limit, region, safe search, backend selection, URL expansion, proxy, timeout, and TLS verification options.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
