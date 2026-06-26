## Description: <br>
Generates and prioritizes US equity long-side research tickets from end-of-day observations and exports pipeline-ready strategy specifications for Phase I backtesting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative researchers use this skill to turn market observations, anomalies, and trading hypotheses into reproducible research tickets, then validate and export compatible strategy.yaml and metadata.json artifacts for the trade-strategy-pipeline Phase I interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user-supplied helper command passed through --llm-ideas-cmd can run with local user permissions and receive market observations. <br>
Mitigation: Only use trusted local commands or providers for LLM-assisted hint generation, and review what data will be sent before execution. <br>
Risk: Unsafe candidate identifiers or forced export behavior can write files outside the intended strategy output location. <br>
Mitigation: Use trusted ticket YAML, validate candidate IDs before export, and avoid --force until the resolved output paths have been reviewed. <br>
Risk: Generated research tickets and strategy specifications can contain incorrect or unprofitable trading assumptions. <br>
Mitigation: Review generated tickets manually and validate exported specs through the downstream pipeline before considering any trading use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/clawdiri-ai/einstein-research-edge-dv) <br>
- [Research Ticket Schema](references/research_ticket_schema.md) <br>
- [Pipeline Interface v1](references/pipeline_if_v1.md) <br>
- [Signal Mapping](references/signal_mapping.md) <br>
- [Ideation Loop](references/ideation_loop.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML strategy specifications, JSON metadata, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces research tickets and pipeline handoff artifacts; it does not run backtests or provide live trading signals.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
