## Description: <br>
Provides cross-market investment review, index valuation-temperature checks, holdings analysis, and multi-format reports for A-share, Hong Kong, and U.S. markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vivifishtl](https://clawhub.ai/user/vivifishtl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individual investors, investment advisors, fund managers, and portfolio analysts use this skill to run weekly market reviews, daily checks, single-instrument analysis, and index-temperature updates. Outputs should be treated as investment research support rather than personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated market analysis or buy/sell ranges may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as research support only and require human review before making investment decisions. <br>
Risk: Feishu integrations may expose more documents or portfolio data than necessary. <br>
Mitigation: Scope Feishu permissions to specific documents or folders and avoid providing account numbers or unnecessary portfolio identifiers. <br>
Risk: The configured deep-research-pro dependency may process sensitive investment data. <br>
Mitigation: Verify the separate deep-research-pro tool before using this skill with sensitive data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vivifishtl/ai-invest-agent) <br>
- [deep-research-pro](https://github.com/paragshah/deep-research-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown reports, summaries, structured tables, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate Word and Excel report artifacts when the host agent supports those formats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
