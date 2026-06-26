## Description: <br>
Build and operate a crypto signal trading automation using RapidAPI cryptexAI Buy & Sell Signals as signal source and dYdX v4 for execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mdann1992](https://clawhub.ai/user/mdann1992) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-automation operators use this skill to build a RapidAPI-to-dYdX v4 crypto signal pipeline with environment setup, connectivity checks, order execution guidance, TP/SL handling, retry behavior, cleanup, and Telegram notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports live crypto-trading automation and asks an agent to handle exchange credentials. <br>
Mitigation: Use a sandbox or low-balance subaccount, require manual approval before live orders, and define a clear stop or disable process before enabling automation. <br>
Risk: API keys, dYdX signing material, mnemonics, passphrases, and Telegram tokens may be exposed during setup. <br>
Mitigation: Keep secrets out of chat and source control, store them in a permission-restricted env file, and rotate any credential that was exposed. <br>
Risk: Unattended scheduled execution can place, retry, or clean up orders incorrectly if generated code is not reviewed. <br>
Mitigation: Review generated trading and cron code before use, start with one symbol in controlled mode, and verify TP/SL and cleanup behavior before expanding the symbol set. <br>


## Reference(s): <br>
- [Crypto Signals Automation release page](https://clawhub.ai/mdann1992/crypto-signals-automation) <br>
- [RapidAPI cryptexAI mapping](references/rapidapi-cryptexai.md) <br>
- [Setup checklist](references/setup-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python scripts, shell commands, and environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions and automation scaffolding that require user-supplied exchange, RapidAPI, and notification credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
