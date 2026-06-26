## Description: <br>
AI search enhancement tool. Prioritizes authoritative sources for research and fact-checking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephenlzc](https://clawhub.ai/user/stephenlzc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and research-focused agents use AISEACT to plan web searches, prioritize authoritative sources, cross-check claims, and cite source URLs with uncertainty noted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The registry security summary says the skill can affect searches more broadly than the main skill documentation suggests, especially when autonomous mode is enabled. <br>
Mitigation: Keep manual invocation enabled unless autonomous use is intentional, and verify when the agent says it is applying AISEACT methodology. <br>
Risk: The source-quality framework may filter or deprioritize sources in ways that reflect documented methodological bias. <br>
Mitigation: Use overrides such as "Show all sources," "Include [source]," or lower strictness settings when broader or alternative-source coverage is needed. <br>
Risk: Server-resolved provenance is unavailable for this version. <br>
Mitigation: Confirm package provenance and review the submitted skill files before relying on the source lists or enabling autonomous behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stephenlzc/aiseact) <br>
- [Publisher profile](https://clawhub.ai/user/stephenlzc) <br>
- [Provenance unavailable](No server-resolved GitHub import provenance is stored for this version.) <br>
- [Configuration Guide](CONFIGURATION.md) <br>
- [Security Information](SECURITY.md) <br>
- [Trust & Transparency Report](TRUST.md) <br>
- [Quick Reference](references/quick-reference.md) <br>
- [Authoritative Sources Recommendation List](references/authority-sources.md) <br>
- [Search Strategies and Techniques](references/search-strategies.md) <br>
- [Unreliable Sources Reference](references/unreliable-sources.md) <br>
- [AISEACT Reference Cases](references/case-studies.md) <br>
- [Workflow Reference](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown guidance with source citations, source-quality notes, and uncertainty statements] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no executable code, dependencies, credentials, or custom network endpoints are described in the artifact.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
