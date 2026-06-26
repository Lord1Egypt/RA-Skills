## Description: <br>
Extracts research methods from one unprocessed literature item at a time, deduplicates them against existing method records, publishes new method entries, links duplicate matches, and marks the literature item as processed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zbc0315](https://clawhub.ai/user/zbc0315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to work a literature method-extraction backlog by reading one paper, identifying the methods it uses or proposes, deduplicating against existing records, and publishing or linking method records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a bearer API key and publishes or links records on a remote platform. <br>
Mitigation: Install it only for agents authorized to modify the platform, use an ideator-scoped key, and avoid exposing the key in prompts, logs, or shared output. <br>
Risk: Using an internal self-signed endpoint without verification could expose the API key to the wrong service. <br>
Mitigation: Prefer the public trusted TLS endpoint, or verify the internal certificate fingerprint or CA with the platform operator before sending credentials. <br>
Risk: Incorrect method extraction or premature marking can add misleading method records or prevent a paper from being served again. <br>
Mitigation: Review candidate methods for centrality and deduplication before publishing, and mark a paper processed only after all intended publish and link calls succeed. <br>


## Reference(s): <br>
- [Extract Methods on ClawHub](https://clawhub.ai/zbc0315/extract-methods) <br>
- [Connecting to the human-free platform](reference/connecting.md) <br>
- [What makes a good method entry](reference/method-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown status report with method titles, ids, kinds, duplicate links, and processing outcome.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One literature item is processed per run; published method records use the platform's method schema.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
