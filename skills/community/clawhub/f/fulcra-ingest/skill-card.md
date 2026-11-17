## Description:

Autonomously orchestrate the ingestion of 3rd-party data exports (e.g., Spotify, Netflix) from the Fulcra File Store into properly mapped Fulcra Annotations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fulcra](https://clawhub.ai/user/fulcra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to process third-party exports from a Fulcra File Store ingest area, map them to Fulcra Annotations, and ingest records with lineage and idempotency controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate on Fulcra File Store data and Fulcra Annotations, including account-data mutation and deletion.

Mitigation: Require explicit confirmation before deletions, corrections, or re-ingestion, and verify archived files before removing originals.

Risk: Recurring automation may continue checking for new files or fetching data after setup.

Mitigation: Confirm the data source, collection frequency, storage destination, privacy implications, and stop procedure before enabling automation.

Risk: Runtime CLI execution is not pinned by the artifact.

Mitigation: Pin and review the `fulcra-api` CLI version before use.

Risk: External enrichment can fetch or combine additional context with user data.

Mitigation: Confirm each external source and enrichment purpose before fetching or ingesting enriched records.

## Reference(s):

- [Fulcra Ingest on ClawHub](https://clawhub.ai/fulcra/skills/fulcra-ingest)
- [Fulcra CLI for 3rd-Party Data Ingestion](references/fulcra-ingest-cli.md)
- [Fulcra Ingest Source Mapping](references/fulcra-ingest-source-mapping.md)
- [Fulcra CLI Documentation](https://raw.githubusercontent.com/fulcradynamics/agent-skills/main/skills/fulcra-get-started/references/fulcra-cli.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON/JSONL examples, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local parsing scripts, JSONL payloads, source-map updates, ingest logs, and Fulcra CLI operations.]

## Skill Version(s):

0.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
