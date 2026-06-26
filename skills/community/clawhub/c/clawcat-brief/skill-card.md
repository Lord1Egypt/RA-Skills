## Description: <br>
Generates structured industry briefings by selecting data sources, gathering public web/news/finance/research items, checking groundedness, and exporting reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llx9826](https://clawhub.ai/user/llx9826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create daily or weekly topic briefings for technology, finance, research, market intelligence, and competitive analysis from configured public sources and an LLM provider. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries third-party websites/APIs and sends prompts, profile preferences, and fetched snippets to the configured LLM provider. <br>
Mitigation: Use trusted provider settings and your own API keys, and avoid submitting secrets or regulated data unless your provider configuration permits it. <br>
Risk: Cross-run deduplication can persist item identifiers in data/item_memory.json. <br>
Mitigation: Clear data/item_memory.json when you need to reset local report history. <br>
Risk: Reports are generated from public web and API sources that may be incomplete, stale, or unavailable. <br>
Mitigation: Review important claims and source coverage before relying on a generated briefing for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/llx9826/clawcat-brief) <br>
- [artifact/README.md](artifact/README.md) <br>
- [artifact/SKILL.md](artifact/SKILL.md) <br>
- [artifact/config.yaml](artifact/config.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Files] <br>
**Output Format:** [HTML, PDF, PNG, Markdown, and JSON report files, with concise command-line status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured LLM provider; writes report outputs and may persist item IDs for cross-run deduplication.] <br>

## Skill Version(s): <br>
0.7.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
