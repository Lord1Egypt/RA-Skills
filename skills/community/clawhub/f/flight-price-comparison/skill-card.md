## Description: <br>
Flight Price Comparison is intended to help an agent query and compare flight prices across travel platforms such as Fliggy, Ctrip, and Qunar using browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nodermachine](https://clawhub.ai/user/nodermachine) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel planners and agent users use this skill to request one-way or round-trip fare checks by route, date, passenger count, and platform, then receive a comparison-style report. It is most useful for preliminary travel planning before manual booking review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to place real travel-account credentials in TOOLS.md, which can expose those accounts to the agent or local workspace. <br>
Mitigation: Avoid storing real passwords in repository files; prefer QR or manual login, a password manager, OS keychain, or tightly scoped environment secrets. <br>
Risk: The included script does not currently perform real price extraction or comparison, so generated fare results may be incomplete or misleading. <br>
Mitigation: Treat results as planning assistance only and verify prices, fees, availability, and ticket rules directly on the travel platforms before booking. <br>
Risk: Browser automation runs against logged-in travel accounts and may encounter captchas, saved sessions, or account-specific prices. <br>
Mitigation: Supervise initial runs, use the least-privileged account or session practical for the task, and require explicit user review before any purchase or account action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nodermachine/flight-price-comparison) <br>
- [Account Configuration Reference](references/account-config.md) <br>
- [Fliggy](https://www.fliggy.com/) <br>
- [Ctrip](https://www.ctrip.com/) <br>
- [Qunar](https://www.qunar.com/) <br>
- [Umetrip](https://www.umetrip.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with command-line examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires route, date, trip type, passenger details, platform selection, and travel account login state; prices, fees, and booking restrictions should be manually verified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
