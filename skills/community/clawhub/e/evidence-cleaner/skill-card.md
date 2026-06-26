## Description: <br>
Evidence Cleaner cleans raw search results, web snippets, OCR fragments, and similar material into standardized evidence by removing noise, duplicates, pseudo-entities, and off-topic or low-reliability sources before downstream freshness or narrative work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z1one0415](https://clawhub.ai/user/z1one0415) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and agent builders use this skill after search or document extraction to normalize noisy evidence into cleaner, auditable inputs for later analysis. It is useful when evidence volume is high, source quality is mixed, or snippets need standardized fields before downstream judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence marks the release as suspicious because a bundled review helper may run a nested reviewer with full sandbox bypass. <br>
Mitigation: Review the skill before installing it in sensitive workspaces, trust the publisher and nested reviewer before using the helper, and prefer no-yolo execution unless full local access is explicitly intended. <br>
Risk: The skill may drop, downrank, or flag evidence incorrectly when source quality, pseudo-entity checks, or relevance judgments are ambiguous. <br>
Mitigation: Review removed and downranked items, keep warnings with downstream analysis, and cross-check important claims against trusted primary sources. <br>


## Reference(s): <br>
- [Noise Pattern Reference](references/noise-patterns.md) <br>
- [Clean, Downrank, and Drop Rules](references/clean-vs-drop-rules.md) <br>
- [Evidence Cleaning Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [Structured JSON with cleaned evidence, removed noise, downranked items, warnings, and cleaning statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves source URLs and titles while recording cleaning actions, removal reasons, downrank reasons, and warnings.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
