## Description:

Helps AIGC, ecommerce, advertising, and developer teams assess and plan a testable migration or dual-route fallback from fal.ai-style media API workflows to AI-HIVE, including audits, routing plans, runnable examples, task ledgers, and acceptance criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and content operations teams use this skill to inventory existing fal.ai or media API usage, compare requirements against AI-HIVE, and create a staged migration plan with small-sample validation, routing choices, rollback criteria, and task records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API credentials and allows a configurable API base URL for remote calls.

Mitigation: Use a limited-scope API key with spending controls, keep credentials in environment variables or a restricted local config file, and do not set AI_HIVE_BASE_URL or --base-url to an untrusted host.

Risk: Image and video workflows can upload source media to a remote service and download generated results.

Mitigation: Use authorized, non-confidential test assets first, review service terms and retention expectations before production use, and avoid uploading sensitive media unless the service and storage path are trusted.

Risk: Generation requests may incur cost or create duplicate work during retries and batch testing.

Mitigation: Start with small samples, set budget controls where possible, record input hashes and task IDs, and keep rollback criteria before moving production traffic.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/fal-ai-alternative-ai-hive)
- [Platform source and comparison boundary](artifact/references/platform.md)
- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [fal.ai evidence page](https://fal.ai/seedance-2.0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, API calls, guidance]

**Output Format:** [Markdown guidance with shell commands, Python script usage, JSON audit and blueprint files, API task records, and downloaded media files when generation commands are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use AI_HIVE_API_KEY, AI_HIVE_BASE_URL, local media paths, routing modes, task IDs, and output directories; generated media calls can upload assets, poll remote tasks, download results, and incur service charges.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
