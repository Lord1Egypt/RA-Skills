## Description: <br>
Helps agents produce source-grounded research answers by checking citations, source boundaries, unsupported claims, and uncertainty before publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, documentation agents, and knowledge-work assistants use this skill to keep cited answers, evidence briefs, literature notes, and source-bounded summaries aligned with allowed sources. It is especially useful when unsupported claims, invented citations, stale evidence, or missing caveats would create false confidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents could include secrets, private records, paywalled full text, or unrelated user messages in a review payload. <br>
Mitigation: Use only minimal redacted summaries for review payloads and exclude secrets, tokens, passwords, unrelated private records, and full source text when a summary is sufficient. <br>
Risk: Unsupported, forbidden, stale, or uncertain evidence could be presented as a confident sourced claim. <br>
Mitigation: Apply the grounding loop before publishing: identify allowed sources, verify important claims, label uncertainty, and revise, retrieve, ask, defer, or refuse when evidence is insufficient. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mindbomber/aana-research-grounding) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Research Grounding Review Schema](artifact/schemas/research-grounding-review.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, json] <br>
**Output Format:** [Markdown guidance with an optional JSON review payload shape] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; it does not execute commands, install dependencies, call remote services, write files, or persist memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact manifest lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
