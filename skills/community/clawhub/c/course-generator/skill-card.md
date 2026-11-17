## Description:

Generates structured, source-traceable courses from transcripts or documents, and can archive existing courses or extract tailored training plans when explicitly requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and course creators use this skill to turn long transcripts, written materials, or verified course assets into structured Markdown course outputs with a manifest for traceability and validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow reads user-selected course materials that may contain private transcript, customer, or training content.

Mitigation: Use only the necessary local input scope and review generated course and manifest files before sharing or archiving them.

Risk: Generated course prose can omit nuance or overstate source material even when structural validation passes.

Mitigation: Run the bundled verifier, then manually review source mappings, factual claims, skipped materials, and cross-chapter consistency before delivery.

Risk: The self-test is intended for verifier validation rather than ordinary course generation.

Mitigation: Run the self-test only when intentionally validating the verifier; use verify.sh against the course directory for normal acceptance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cat-xierluo/skills/course-generator)
- [Project homepage](https://github.com/cat-xierluo/legal-skills)
- [course-manifest.json product contract](artifact/references/course-manifest.md)
- [Course manifest JSON Schema](artifact/config/course-manifest.schema.json)
- [Course outline prompt](artifact/references/outline_prompt.md)
- [Overview document prompt](artifact/references/overview_prompt.md)
- [Chapter writing prompt](artifact/references/chapter_prompt.md)
- [Extraction mode prompt](artifact/references/extract_prompt.md)
- [Verification entrypoint](artifact/scripts/verify.sh)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown course files, a JSON course manifest, optional audit files, and inline shell commands for validation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are local files; generated course content should be reviewed for semantic fidelity after deterministic validation passes.]

## Skill Version(s):

2.8.1 (source: frontmatter and changelog, released 2026-08-25; ClawHub release 2.8.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
