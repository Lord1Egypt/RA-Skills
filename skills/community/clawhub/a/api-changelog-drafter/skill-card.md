## Description:

Converts code diffs, PR descriptions, and API spec changes into developer-facing changelog entries, deprecation notices, migration guides, semantic version recommendations, and upgrade-impact summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Technical writers, developer advocates, API product managers, and engineering teams use this skill to turn API change evidence into draft release documentation for external, partner, internal, or open-source API consumers. It is intended as a drafting aid whose classifications, semantic version recommendations, and deprecation timelines require engineering and technical-writer review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Breaking-change classifications, semantic version bump recommendations, or deprecation timelines may be incorrect when the provided API change evidence is incomplete or ambiguous.

Mitigation: Have engineering verify compatibility impact, versioning recommendations, and removal or sunset dates before using the draft in a real release.

Risk: Draft changelog language could disclose too much detail about security fixes or imply unapproved release policy.

Mitigation: Review security entries and release-policy statements with the appropriate engineering, product, and technical-writing owners before publication.

## Reference(s):

- [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown draft changelog package]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a draft header, semantic version recommendation, Keep-a-Changelog entry, deprecation notices when applicable, migration guidance for breaking changes, upgrade-impact summary, and open questions.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
