## Description:

Generates JSONL question-answer training data by chunking CSV text and using a shared LLM interface to create questions and answers for each chunk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erxiong0](https://clawhub.ai/user/erxiong0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to inspect CSV corpora and synthesize structured QA examples for document, table, or fine-tuning data preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API mode can transmit CSV text and an API bearer token to a configurable endpoint that may use plain HTTP.

Mitigation: Use dry-run for local testing, prefer HTTPS endpoints, and avoid sending API keys or sensitive data to HTTP URLs.

Risk: Generated JSONL stores source chunks and source fields, which may contain private, regulated, or proprietary data.

Mitigation: Review input data before processing and handle generated JSONL as a derivative copy of the source corpus.

Risk: Question generation depends on model output that may not parse cleanly as JSON.

Mitigation: Review the run statistics and errors field, then sample or validate generated QA pairs before using them for training.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/erxiong0/skills/data-synthesis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts are JSON, JSONL, and CSV inspection summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run mode avoids API calls; API mode may send CSV text and bearer credentials to the configured OpenAI-compatible endpoint.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
