## Description: <br>
Provides a Chinese-language daily assistant for weather-style lookups, currency conversion, festival reminders, lifestyle tips, and short Chinese-English phrase translation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jenner4S](https://clawhub.ai/user/Jenner4S) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Chinese-speaking ClawHub users can use this skill for quick everyday responses about supported Chinese city weather, common currency conversions, festival dates, lifestyle tips, and common Chinese-English phrases. The weather, exchange-rate, and countdown values should be treated as packaged demo data unless the skill is extended with live data sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather, exchange-rate, and festival countdown responses may be mistaken for current live facts. <br>
Mitigation: Treat these outputs as static demo data unless the skill is updated to use validated live data sources. <br>
Risk: Broad trigger words may cause the skill to answer ordinary weather or translation requests when another tool would be more appropriate. <br>
Mitigation: Review routing and trigger configuration before deployment in environments with overlapping assistant capabilities. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jenner4S/chinese-daily-assistant) <br>
- [README.md](artifact/README.md) <br>
- [Usage examples](artifact/使用示例.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown-style responses, with example shell commands in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are deterministic local responses from packaged data and phrase dictionaries.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact package.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
