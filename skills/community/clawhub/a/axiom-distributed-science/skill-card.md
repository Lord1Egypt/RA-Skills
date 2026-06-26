## Description: <br>
Query scientific findings, experiments, and papers from the Axiom distributed volunteer computing network (113+ hosts, 129 GPUs, 42K+ results). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PyHelix](https://clawhub.ai/user/PyHelix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to query Axiom's public science APIs for network statistics, findings, experiment listings, papers, and plain-text experiment suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and experiment suggestions are sent to Axiom's public API endpoints. <br>
Mitigation: Confirm that submitted ideas and author names are safe to send to axiom.heliex.net; do not include secrets, private research details, or personal data. <br>
Risk: Scientific findings returned by the public API may be incomplete, preliminary, or unsuitable for unsupported conclusions. <br>
Mitigation: Treat API responses as source material for review and cite the underlying Axiom pages or papers when using findings in user-facing work. <br>
Risk: The skill can suggest curl commands that make network requests. <br>
Mitigation: Review commands before execution and only run them in environments where outbound requests to axiom.heliex.net are allowed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/PyHelix/axiom-distributed-science) <br>
- [Axiom Homepage](https://axiom.heliex.net) <br>
- [Axiom Scientific Findings](https://axiom.heliex.net/scientific_findings.php) <br>
- [Example Axiom Paper](https://axiom.heliex.net/reactivity_localization_paper.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline curl commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for documented API calls; the suggestion endpoint accepts plain text up to 5,000 characters and is rate limited.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
