## Description: <br>
Use when the user wants an Abel causal read on what drives a market, company, asset, sector, or macro node, how two nodes connect, what changes under intervention, or how a career, education, housing, lifestyle, or investment decision with meaningful money, time, career-capital, or downside tradeoff should be evaluated through Abel proxy signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[exenvitor](https://clawhub.ai/user/exenvitor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce Abel-grounded causal analysis for market, business, macro, lifestyle, housing, education, career, and investment decisions involving meaningful money, time, career-capital, or downside risk. It supports direct graph questions and proxy-routed decision analysis, including web grounding when current facts matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Abel API key and may store it locally for authenticated probing. <br>
Mitigation: Treat ABEL_API_KEY as a secret, keep .env.skill and .env out of commits and shared workspaces, and revoke or rotate the key if exposed. <br>
Risk: Authenticated Abel probes involve an external service in finance, housing, career, business, or other high-impact decision advice. <br>
Mitigation: Confirm the user wants Abel analysis before running probes on ambiguous high-impact questions, and frame outputs as decision support rather than causal proof. <br>
Risk: Graph or proxy analysis can be misleading when premises are stale, unsupported, or graph-sparse. <br>
Mitigation: Use the skill's freshness checks, web-grounding rules, contradiction search, and claim-strength caveats before presenting decision guidance. <br>
Risk: OAuth handling can expose credentials if the agent asks for raw secrets or codes. <br>
Mitigation: Use the documented OAuth handoff URL flow, never ask for an email address, OAuth code, or raw API key, and wait for authorization before probing. <br>


## Reference(s): <br>
- [Causal Abel on ClawHub](https://clawhub.ai/exenvitor/causal-abel) <br>
- [Abel Skills Repository](https://github.com/Abel-ai-causality/Abel-skills) <br>
- [Probe Usage](references/probe-usage.md) <br>
- [Direct Graph Route](references/routes/direct-graph.md) <br>
- [Proxy-Routed Route](references/routes/proxy-routed.md) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Web Grounding](references/web-grounding.md) <br>
- [Rendering Rules](references/rendering.md) <br>
- [Causal Abel Report Guide](assets/report-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with concise decision guidance and optional inline shell commands for setup or probe usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to the main answer only; probe traces, appendices, and raw graph details are omitted unless explicitly requested.] <br>

## Skill Version(s): <br>
1.1.6 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
