## Description: <br>
Installs, runs, maintains, and troubleshoots a bundled local single-user AKShare financial data workbench for setup, tests, cache management, catalog edits, and responsible public-data access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianyedavid](https://clawhub.ai/user/tianyedavid) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data analysts use this skill to create and operate a local AKShare workbench from bundled assets, start or stop its FastAPI and React services, run tests, clear cache, and maintain the indicator catalog. It is intended for local single-user financial data workflows rather than high-frequency, bulk, or trading-advice use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workbench installs Python and npm dependencies and runs local services. <br>
Mitigation: Run setup in an isolated local environment, review dependency files before installation, and use the controller's doctor and test commands before routine use. <br>
Risk: The workbench contacts AKShare and upstream public financial data providers that may enforce terms, rate limits, or availability restrictions. <br>
Mitigation: Use local caching, conservative request pacing, targeted indicators, and licensed data feeds for production, bulk, commercial, or high-frequency workflows. <br>
Risk: Optional AI configuration stores provider credentials locally in plaintext. <br>
Mitigation: Use only trusted AI providers, avoid entering sensitive financial or account information into chat, and keep ai_config.json, .env files, API keys, proxy credentials, logs, and cache files private. <br>
Risk: Financial data returned by public interfaces can be delayed, incomplete, unavailable, or inaccurate. <br>
Mitigation: Verify important financial data with official or licensed sources and do not treat workbench output as investment, trading, or portfolio advice. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/tianyedavid/akshare-local-workbench) <br>
- [Project Homepage](https://github.com/TianYeDavid/akshare-local-workbench) <br>
- [Maintenance Guide](references/maintenance.md) <br>
- [Bundled Workbench README](assets/akshare-workbench/README.md) <br>
- [Bundled Workbench Disclaimer](assets/akshare-workbench/DISCLAIMER.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown guidance with shell commands, configuration values, and file path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local setup, maintenance, troubleshooting, catalog-editing, and cache-management instructions for the bundled workbench.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
