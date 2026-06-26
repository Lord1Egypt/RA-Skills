## Description: <br>
Correlation-aware memory search plugin for OpenClaw that automatically retrieves related decision contexts when an agent queries memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ether-btc](https://clawhub.ai/user/ether-btc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to expand memory searches with rule-based related context, helping agents surface backup, recovery, configuration, and debugging context before decisions are made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad or noisy correlation rules can surface irrelevant memory contexts and reduce result quality. <br>
Mitigation: Review and narrow memory/correlation-rules.json before enabling the skill; tune confidence thresholds, lifecycle states, matching mode, and max_results. <br>
Risk: Sensitive local memories such as access logs or credentials could be surfaced if broad triggers include those contexts. <br>
Mitigation: Avoid broad triggers for sensitive memory areas and keep must_also_fetch entries limited to contexts that are appropriate for the deployment. <br>
Risk: The bundled uninstall.sh modifies OpenClaw configuration. <br>
Mitigation: Prefer the OpenClaw CLI uninstall path where available; otherwise review the script and keep a configuration backup before running it. <br>
Risk: Dependency and source trust are outside the read-only runtime behavior. <br>
Mitigation: Verify the package and repository source before installation, and install only in environments where local rule-based memory expansion is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ether-btc/correlation-memory) <br>
- [Deployment Guide](docs/deployment.md) <br>
- [Production Guide](docs/production-guide.md) <br>
- [Research Background](docs/research.md) <br>
- [Example Correlation Rules](correlation-rules.example.json) <br>
- [OpenClaw](https://openclaw.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [JSON tool responses with matched rules, suggested additional searches, and summaries; Markdown documentation with setup and rule examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenClaw workspace with memory/correlation-rules.json; supports query/context, matching mode, confidence threshold, and max results.] <br>

## Skill Version(s): <br>
2.1.0 (source: evidence.release.version, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
