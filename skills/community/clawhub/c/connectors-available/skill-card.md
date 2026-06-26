## Description: <br>
Check which exchanges work from your location and search for tokens with trading rules such as minimum order size, price increment, and order types. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengtality](https://clawhub.ai/user/fengtality) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and Hummingbot users use this skill to test which exchange connectors are accessible from their location and to look up trading-rule details for token pairs. It helps summarize connector availability and token-specific order constraints from a local Hummingbot API and bundled or generated trading rules data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts handle user input and local credential files unsafely enough to require review before installation. <br>
Mitigation: Review the scripts before use, pass only trusted token and data-file values, and run them from a directory that does not contain sensitive .env files. <br>
Risk: Default admin/admin credentials and local API access can expose Hummingbot API operations if used carelessly. <br>
Mitigation: Use non-default credentials and keep the Hummingbot API bound to a trusted local interface. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengtality/connectors-available) <br>
- [Publisher profile](https://clawhub.ai/user/fengtality) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown tables, shell command suggestions, and JSON trading-rules files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local shell scripts that call a Hummingbot API and read or write trading_rules.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
