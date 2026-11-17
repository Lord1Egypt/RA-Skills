## Description:

Digest Builder turns raw feed candidates or FreshRSS unread items into structured digest candidates through URL deduplication, event clustering, content checks, noise filtering, summary generation, tagging, and preliminary ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gcdd1993](https://clawhub.ai/user/gcdd1993)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to collect FreshRSS unread items or raw feed entries and turn them into a clean, deduplicated, human-reviewable digest candidate pool. It is intended as preprocessing for digest creation, not as a final daily digest publisher.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: FreshRSS credentials can be exposed if the configured FreshRSS base URL uses insecure HTTP.

Mitigation: Use only an HTTPS FreshRSS base URL and avoid printing or sharing the API password.

Risk: Feed-controlled URLs may be fetched from the user's network context during content checks.

Mitigation: Run against trusted feeds or use a sandboxed environment with constrained outbound network access.

Risk: Raw FreshRSS content and generated summaries are written to local digest files.

Mitigation: Store outputs in an appropriate local workspace and avoid using sensitive feeds unless those files can be protected.

Risk: The mark-read script can change FreshRSS read state for selected items.

Mitigation: Use the mark-read script only after an explicit user decision, preferably with date filters and dry-run review first.

## Reference(s):

- [Digest Spec](artifact/references/digest-spec.md)
- [FreshRSS Google Reader API](artifact/references/freshrss-google-reader.md)
- [ClawHub Skill Page](https://clawhub.ai/gcdd1993/skills/digest-builder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and generated JSON/Markdown digest files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces FreshRSS raw exports, date-sliced candidate files, and structured digest candidates with summaries, tags, cluster metadata, and ranking rationale.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
