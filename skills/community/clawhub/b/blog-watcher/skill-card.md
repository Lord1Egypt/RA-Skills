## Description:

Blog Watcher helps monitor RSS feeds and webpage content changes for user-provided blog or website URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-monitoring users can use this skill to create or operate a lightweight Python watcher for RSS feeds and webpage changes. It is suited to tracking public blogs or websites where outbound network access to the monitored URLs is acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests from the agent environment to user-provided URLs without documented URL validation, timeouts, or response-size limits.

Mitigation: Use only trusted public URLs unless the implementation is hardened with URL allowlisting or validation, request timeouts, response-size limits, and clear dependency pinning.

Risk: The release advertises diff comparison, scheduling, push notifications, and exclusion rules that are not actually present in the artifact.

Mitigation: Treat those advertised capabilities as unavailable until separately implemented and verified; rely only on RSS checks and basic webpage hash-change detection shown in the artifact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/blog-watcher)

## Skill Output:

**Output Type(s):** [code, shell commands, markdown, guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may describe or include code that fetches user-provided URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
