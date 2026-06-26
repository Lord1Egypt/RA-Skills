## Description: <br>
DevTool Answer Monitor helps agents monitor how LLMs describe a developer tool, API, SDK, or open-source project, then plan query pools, scoring, repair, activation analysis, and T+7 or T+14 regression validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veeicwgy](https://clawhub.ai/user/veeicwgy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, maintainers, and developer relations teams use this skill to understand how models mention, recommend, or misunderstand a developer product. It guides query design, monitoring, content placement, negative-answer repair, and follow-up validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider API keys may be exposed if users paste secrets into chat or reports. <br>
Mitigation: Keep API keys in local environment variables and use quickstart replay or manual paste mode when live collection is not needed. <br>
Risk: Live API collection can send query text, product context, and model prompts to the configured provider or gateway. <br>
Mitigation: Review OPENAI_BASE_URL and provider settings before API collection, and avoid networked model calls when the monitoring data should stay local. <br>
Risk: Local installation and dependency versions may vary across environments. <br>
Mitigation: Use a local Python virtual environment and pin dependencies when reproducible installs are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/veeicwgy/devtool-answer-monitor) <br>
- [Project homepage from ClawHub metadata](https://github.com/veeicwgy/devtool-answer-monitor) <br>
- [Zero-install demo viewer](https://cdn.jsdelivr.net/gh/veeicwgy/devtool-answer-monitor@main/docs/index.html) <br>
- [MinerU public benchmark](benchmark/mineru-public-benchmark.md) <br>
- [Sciverse API public benchmark](benchmark/sciverse-api-public-benchmark.md) <br>
- [Metric definition](docs/metric-definition.md) <br>
- [Activation metrics](docs/activation-metrics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON/query-pool structures and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May route to bundled sub-skills; live API collection requires locally configured provider credentials.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
