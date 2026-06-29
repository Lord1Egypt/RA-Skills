## Description: <br>
Use when an external event thesis needs market confirmation before commitment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to evaluate event-driven Polymarket strategy ideas by waiting for post-catalyst filled-trade confirmation before committing. It helps frame market mapping, catalyst timing, entry/exit logic, and configuration knobs for later NautilusTrader strategy development. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Catalyst information may already be priced in, or the selected market may not map cleanly to the event. <br>
Mitigation: Require an exact market slug, a clear catalyst timestamp, direct question-to-event mapping, and a filled-trade confirmation move after the catalyst window. <br>
Risk: Single-event backtests can overfit or mistake temporary price spikes for durable confirmation. <br>
Mitigation: Treat the skill output as an archetype, test across comparable events, tune thresholds conservatively, and review the generated NautilusTrader strategy before use. <br>
Risk: Authoritative security guidance warns that hosted memory services can retain agent context across sessions. <br>
Mitigation: Use OAuth or scoped API keys when applicable, avoid storing secrets or sensitive personal/customer data unless intended, and review or delete retained context when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superior-ai/catalyst-confirmation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, code] <br>
**Output Format:** [Markdown guidance with JSON configuration example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a trading strategy archetype that should be reviewed, tuned, and converted into custom NautilusTrader code before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
