## Description: <br>
AI Agent Wars 2026 is a Chinese-language skill that advertises structured comparisons of major AI agent platforms, including capabilities, adoption, safety, financing, tooling, and forecasts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users can ask for Chinese-language comparisons of AI agent platforms across architecture, enterprise adoption, security governance, financing, developer tooling, and forecasts. Reviewers should note that the current executable handler requires an external payment instead of returning the advertised analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The executable handler returns an undisclosed external Alipay payment request instead of the advertised AI-agent analysis. <br>
Mitigation: Do not deploy until the payment behavior is removed or clearly disclosed and reviewed; verify the skill returns the requested analysis before installation. <br>
Risk: Users may rely on market-analysis claims from the bundled data set without source validation. <br>
Mitigation: Treat analysis output as informational guidance and verify important market, investment, or vendor claims against authoritative sources before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/ai-agent-wars) <br>
- [AI Agent Wars data reference](artifact/references/ai-agent-wars.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Advertised Markdown tables and lists; current handler returns a JSON payment-required response.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a bundled JSON data set for analysis claims; security evidence reports the handler returns an external Alipay payment request instead of the advertised analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
