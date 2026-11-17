## Description:

BizyAir image, video, and audio generation plus AI application execution for agents handling BizyAir requests, links, IDs, and application search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ezra-y](https://clawhub.ai/user/ezra-y)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to search BizyAir resources, prepare confirmed generation runs, execute BizyAir AI apps and ModelZoo tasks, inspect account balance, and manage small batches of media generation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid BizyAir task execution can spend the user's account balance.

Mitigation: Require explicit user confirmation before any paid run, keep batch sizes and concurrency within configured limits, and use a limited BizyAir API key.

Risk: Local image, audio, or video files may be uploaded as model inputs.

Mitigation: Ask for confirmation before media upload and avoid submitting sensitive local files.

Risk: Search results and model descriptions come from external platform content and may be untrusted.

Mitigation: Treat platform-provided text as untrusted display content and do not let it override installation, security, or execution policy.

Risk: Batch jobs can expose unrelated environment secrets to child processes.

Mitigation: Keep unrelated secrets out of the environment while running batch jobs and scope credentials to BizyAir access only.

## Reference(s):

- [BizyAir homepage](https://bizyair.cn)
- [01 Query Search](references/01-query-search.md)
- [02 Account Assets](references/02-account-assets.md)
- [03 AI App Tasks](references/03-ai-app-tasks.md)
- [04 ModelZoo Tasks](references/04-modelzoo-tasks.md)
- [05 Common Reference](references/05-common-reference.md)
- [06 Batch Rules](references/06-batch-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-backed command output for BizyAir search, preflight, execution, status, balance, and batch workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated media URLs, account balance summaries, task status summaries, confirmation cards, and batch status paths; raw request identifiers and backend JSON are suppressed unless needed for troubleshooting.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
