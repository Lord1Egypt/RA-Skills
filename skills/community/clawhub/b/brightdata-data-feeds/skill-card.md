## Description: <br>
Extract structured data from 40+ supported platforms via the Bright Data CLI (`bdata pipelines`) when the user has a known platform URL and wants clean JSON rather than raw HTML. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meirk-brd](https://clawhub.ai/user/meirk-brd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to choose and run Bright Data pipeline commands for supported marketplaces, social platforms, profiles, comments, reviews, posts, and related structured feeds. It is intended for workflows where target URLs are already known; unsupported URLs are routed to scraping and URL discovery is routed to search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Bright Data CLI authentication and may use sensitive credentials. <br>
Mitigation: Install the CLI from an official source, authenticate deliberately, and avoid exposing API keys or saved credentials in command output, logs, or shared files. <br>
Risk: Pipeline runs can collect third-party, profile, comment, review, or social-platform data. <br>
Mitigation: Review URL lists before batching, start with small runs, and ensure collection, use, and retention comply with platform terms, privacy expectations, and applicable law. <br>
Risk: Large feed, review, comment, or batch jobs can consume quota and produce partial failures. <br>
Mitigation: Use low parallelism, raise timeouts for long jobs, parse outputs with `jq`, check record counts, and inspect top-level and per-record error fields before treating results as complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meirk-brd/brightdata-data-feeds) <br>
- [Flags reference](references/flags.md) <br>
- [Patterns](references/patterns.md) <br>
- [Worked examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON verification checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides command selection, timeout tuning, output format choices, batching, and post-run validation for Bright Data pipeline results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
