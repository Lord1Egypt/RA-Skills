## Description: <br>
Track finance investment signal evolution and update logic based on new finance market information. Use when monitoring finance signals and determining if they are strengthened, weakened, or falsified. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouzhonglu8-png](https://clawhub.ai/user/zhouzhonglu8-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance analysts use this skill to research, analyze, and update investment signal state as new market, news, and price information arrives. It supports structured signal evolution tracking for strengthened, weakened, falsified, or unchanged theses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact external search, news, model, and LLM services while processing finance signals. <br>
Mitigation: Review and restrict network access, API keys, and permitted providers before using it with proprietary watchlists or sensitive research. <br>
Risk: The skill can store or modify market, news, search, and signal data in a local SQLite database. <br>
Mitigation: Run it with a reviewed database path, least-privilege filesystem access, and backups or test data until database behavior is approved. <br>
Risk: The shipped behavior includes broader web, LLM, model-download, training, and database-mutation capabilities than the main description discloses. <br>
Mitigation: Review the full artifact and security summary before deployment, and disable unused capabilities in production environments. <br>


## Reference(s): <br>
- [AlphaEar Signal Tracker Prompts](references/PROMPTS.md) <br>
- [ClawHub release page](https://clawhub.ai/zhouzhonglu8-png/alphaear-signal-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance, prompt text, Python helper code, and structured JSON signal outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update InvestmentSignal JSON and local SQLite-backed market, news, search, and signal records.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
