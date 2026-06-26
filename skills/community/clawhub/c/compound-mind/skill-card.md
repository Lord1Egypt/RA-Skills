## Description: <br>
CompoundMind distills raw daily memory logs into structured patterns, briefings, growth metrics, and a searchable experience index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cassh100k](https://clawhub.ai/user/cassh100k) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and agent operators use CompoundMind to distill local memory logs into searchable lessons, facts, decisions, relationship notes, and pre-session briefings so future agent sessions can reuse prior experience. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release ships plaintext experience data and may store sensitive operational details in searchable local memory. <br>
Mitigation: Remove bundled experience data before installation, keep the memory directory scoped, and do not store wallet keys, API tokens, credential paths, or account data in memories. <br>
Risk: Optional LLM briefing and report features can send selected memory excerpts to Anthropic when enabled. <br>
Mitigation: Use rule-based mode by default, enable LLM mode only after reviewing the selected memory content, and add secret redaction before indexing. <br>
Risk: Suggested scheduled sync can repeatedly index newly written memory files before human review. <br>
Mitigation: Avoid cron or other automatic sync until the memory source, redaction process, and retention policy have been reviewed. <br>


## Reference(s): <br>
- [CompoundMind ClawHub release](https://clawhub.ai/cassh100k/compound-mind) <br>
- [Cassh publisher profile](https://clawhub.ai/user/cassh100k) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, Markdown briefings, JSON data files, and SQLite-backed search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save local briefing files, maintain local distilled-experience JSON, and rebuild a local SQLite FTS index.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
