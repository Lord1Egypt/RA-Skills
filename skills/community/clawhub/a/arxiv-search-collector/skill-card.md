## Description: <br>
Model-guided arXiv paper collection workflow that plans queries, fetches metadata, filters relevance, and merges deduplicated results by language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xukp20](https://clawhub.ai/user/xukp20) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and research assistants use this skill to turn a topic into a curated arXiv paper set by planning queries, fetching public metadata, filtering results for relevance, and merging deduplicated outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Python helper scripts execute in the user's environment. <br>
Mitigation: Install only if you are comfortable running local scripts and use a dedicated output or run directory. <br>
Risk: User-provided python-bin or fetch-script overrides can change what code is executed. <br>
Mitigation: Use the bundled default script paths and avoid untrusted python-bin or fetch-script overrides. <br>
Risk: Fetched arXiv metadata and abstracts are untrusted text that may influence relevance filtering. <br>
Mitigation: Treat fetched content as untrusted input, use it only for relevance filtering, and review selected papers before merging final outputs. <br>
Risk: Aggressive querying can trigger arXiv rate limits or incomplete collection runs. <br>
Mitigation: Keep serial batch mode and default min-interval, retry, jitter, and run-local rate-state settings; back off if arXiv returns rate-limit errors. <br>


## Reference(s): <br>
- [I/O Contract](references/io-contract.md) <br>
- [Query Plan Format](references/query-plan-format.md) <br>
- [arXiv API endpoint](https://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with bash commands and JSON examples; helper scripts write JSON and Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates run directories with query metadata, selection logs, per-paper metadata, and deduplicated paper indexes.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
