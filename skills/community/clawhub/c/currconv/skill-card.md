## Description: <br>
Convert currencies using frankfurter.app free API. Use when converting amounts, checking exchange rates, or viewing rate history. Requires curl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use Currconv to convert amounts, inspect current exchange rates, list supported currencies, and compare historical exchange rates from a public currency API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Currency requests are sent to the public frankfurter.app service. <br>
Mitigation: Avoid entering sensitive transaction details and confirm that public API calls are acceptable for the deployment environment. <br>
Risk: Exchange-rate output may be unsuitable as sole authority for high-stakes financial decisions. <br>
Mitigation: Confirm rates against an approved financial data source before using the output for trading, accounting, or regulated workflows. <br>
Risk: The skill depends on curl, python3, and network availability. <br>
Mitigation: Install required dependencies, allow outbound access to frankfurter.app, and handle network or API failures before relying on the skill operationally. <br>


## Reference(s): <br>
- [Currconv on ClawHub](https://clawhub.ai/bytesagain-lab/currconv) <br>
- [BytesAgain](https://bytesagain.com) <br>
- [frankfurter.app](https://frankfurter.app) <br>
- [European Central Bank Euro foreign exchange reference rates](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output with formatted currency tables and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, python3, and network access; uses frankfurter.app and may cache rate data under ~/.local/share/currconv/.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
