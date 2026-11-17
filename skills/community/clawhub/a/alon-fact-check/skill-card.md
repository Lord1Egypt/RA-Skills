## Description:

Alon Fact Check verifies factual claims from text or URLs by extracting explicit claims, checking authoritative sources, and returning structured credibility reports or source traces with links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alondotsh](https://clawhub.ai/user/alondotsh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check factual claims from URLs or pasted text, trace original or official sources, and receive structured reports with verdicts, credibility scores, source links, and key qualifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick install command uses a floating npx package/source, which may change between installs.

Mitigation: Pin or verify the installer package/source before installation.

Risk: Fact-check reports can be incomplete or misleading if sources are inaccessible, stale, or not directly tied to the exact claim.

Mitigation: Review the cited links and claim-source alignment, especially for high-stakes medical, legal, financial, public safety, or civic topics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alondotsh/skills/alon-fact-check)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with source links, verdicts, credibility ratings, and source-trace sections when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's language and keeps claim sections concise with direct source URLs.]

## Skill Version(s):

0.1.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
