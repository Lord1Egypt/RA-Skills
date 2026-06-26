## Description: <br>
Firecrawl Agent runs autonomous website extraction to navigate complex sites and return structured JSON from pricing pages, product listings, directories, and other multi-page sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eohmig](https://clawhub.ai/user/eohmig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run Firecrawl's autonomous extraction from the command line, especially when structured website data requires navigation across complex or multi-page sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Autonomous extraction may process untrusted target URLs or produce JSON that is unsuitable for downstream use. <br>
Mitigation: Use trusted target URLs and review generated JSON before using it in later workflows. <br>
Risk: Agent runs can consume Firecrawl credits. <br>
Mitigation: Set an explicit --max-credits limit when cost control matters. <br>
Risk: Output files may be written to unintended locations if paths are chosen casually. <br>
Mitigation: Set an explicit output path in a dedicated directory. <br>


## Reference(s): <br>
- [Firecrawl Agent ClawHub release](https://clawhub.ai/eohmig/firecrawl-agent) <br>
- [firecrawl-scrape](../firecrawl-scrape/SKILL.md) <br>
- [firecrawl-interact](../firecrawl-interact/SKILL.md) <br>
- [firecrawl-crawl](../firecrawl-crawl/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports optional target URLs, model selection, JSON schema input, credit limits, wait mode, pretty printing, and explicit output paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
