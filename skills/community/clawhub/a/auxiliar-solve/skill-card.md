## Description: <br>
Ranks installable tools for agent jobs including OCR, PDF extraction, NFS-e invoices, bookkeeping, boletos, receipts, and web scraping, using reproducible evals on real-world corpora. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tlalvarez](https://clawhub.ai/user/tlalvarez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to choose an installable OCR, document extraction, web scraping, bookkeeping, or service-recommendation tool based on ranked evaluations rather than ad hoc guesses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to add and query the external auxiliar-mcp package and then install recommended follow-on tools. <br>
Mitigation: Review returned install commands before running them and prefer a sandbox for document-processing tools. <br>
Risk: Recommended services or tools may involve cloud API keys, paid usage, licenses, or sensitive documents. <br>
Mitigation: Check each service or tool's trust, cost, license, and data-handling terms before sharing credentials or documents. <br>
Risk: Ranked recommendations are based on evaluated corpora and may not fit every user's document set or workflow. <br>
Mitigation: Read the scorecards, alternatives, corpus summaries, and methodological caveats, then test candidates on representative samples before relying on them. <br>


## Reference(s): <br>
- [Auxiliar Solve ClawHub page](https://clawhub.ai/tlalvarez/auxiliar-solve) <br>
- [Human-readable rankings](https://auxiliar.ai/solve/) <br>
- [Reproducible eval harness](https://github.com/Tlalvarez/Auxiliar-ai/tree/main/scripts/ocr-walkthrough) <br>
- [Methodology](https://github.com/Tlalvarez/Auxiliar-ai/blob/main/docs/proposals/agent-upgrade-engine.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Text] <br>
**Output Format:** [Markdown with inline shell commands and task-query examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm; recommendations may include install commands, scorecards, alternatives considered, corpus summaries, FAQs, caveats, and agent-fit notes.] <br>

## Skill Version(s): <br>
v0.1.0 (source: server release metadata; SKILL.md frontmatter version 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
