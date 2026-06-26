## Description: <br>
Meta-skill for iterative, hypothesis-driven deep research using deepresearchwork, tavily-search, literature-search (Semantic Scholar mapping), and perplexity-deep-search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4gen](https://clawhub.ai/user/h4gen) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to scope a research question, gather web and academic evidence across multiple rounds, resolve source contradictions, and produce a sourced scientific Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup instructions include `clawhub update --all`, which can update every installed skill rather than only this skill's dependencies. <br>
Mitigation: Install or update only the named dependencies unless a full local skill update is intentional. <br>
Risk: Research topics and prompts may be sent to Tavily and Perplexity through required API-backed upstream skills. <br>
Mitigation: Use dedicated API keys and avoid confidential topics unless those providers are acceptable for the intended use. <br>
Risk: The skill depends on upstream skills and external services whose behavior, access limits, or costs can affect results. <br>
Mitigation: Review upstream skills before use, disclose missing access in the report, and keep unresolved contradictions visible. <br>


## Reference(s): <br>
- [Deep Researcher on ClawHub](https://clawhub.ai/h4gen/deep-researcher) <br>
- [ClawHub](https://clawhub.ai) <br>
- [Inspected Upstream Skills](references/inspected-skills.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Scientific Markdown report with footnotes and occasional inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include methodology, findings, contradictions, confidence assessment, limitations, outlook, and traceable footnotes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
