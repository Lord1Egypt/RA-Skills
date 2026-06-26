## Description: <br>
Reference and refresh a local OpenClaw documentation snapshot for product usage, deployment, configuration, CLI commands, channels, gateway behavior, tools, troubleshooting, and docs-version verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lueashes](https://clawhub.ai/user/lueashes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to answer OpenClaw product, setup, configuration, CLI, integration, security, and troubleshooting questions from a pinned local documentation snapshot. Maintainers can also use it to refresh the bundled docs snapshot, rebuild indexes, validate the corpus, and summarize documentation changes when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Refresh mode can replace the bundled documentation snapshot and relies on git or network access to the fixed upstream OpenClaw repository. <br>
Mitigation: Run refresh only after an explicit user request, validate the docs, rebuild indexes, and review the generated diff before relying on refreshed answers. <br>
Risk: Documentation examples may include commands, tokens, passwords, API keys, or bearer-auth examples that are not real credentials. <br>
Mitigation: Treat example values as documentation text only; do not execute install snippets blindly or use/extract credential-like examples. <br>
Risk: Answers can become outdated if the pinned local snapshot is stale. <br>
Mitigation: For freshness-sensitive questions, read the source lock and report the snapshot commit/date; refresh from the upstream docs only when requested. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lueashes/claw-wiki) <br>
- [OpenClaw documentation snapshot source lock](artifact/state/source-lock.json) <br>
- [OpenClaw update workflow](artifact/references/update-workflow.md) <br>
- [OpenClaw routing cheatsheet](artifact/references/routing-cheatsheet.md) <br>
- [OpenClaw query examples](artifact/references/query-examples.md) <br>
- [OpenClaw docs navigation metadata](artifact/docs.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown answers with file-path citations, command snippets, and maintenance summaries when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Answers should be grounded in local snapshot files; refresh responses should include snapshot commit/date and validation or diff status.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
