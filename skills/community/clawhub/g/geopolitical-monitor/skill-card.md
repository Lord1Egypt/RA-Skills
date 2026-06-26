## Description: <br>
Generates local demonstration reports that map geopolitical news keywords to sector impact summaries and stock watchlists. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[zrisingz-crypto](https://clawhub.ai/user/zrisingz-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts can run this skill locally to prototype geopolitical-news-to-sector-impact reporting with configurable keywords and mock news data. Its reports should be treated as demonstration content, not live market intelligence or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script creates local report files under ~/shared_memory/geopolitical. <br>
Mitigation: Run it only where that output path is acceptable, or modify DATA_DIR before execution. <br>
Risk: The included analysis uses mock/demo content and can be mistaken for live geopolitical or market intelligence. <br>
Mitigation: Label outputs as demonstration reports unless the script is updated to use validated real data sources and reviewed analytical logic. <br>
Risk: The artifact declares a requests dependency that the current script does not use. <br>
Mitigation: Avoid installing unnecessary dependencies, or remove the unused dependency declaration when packaging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zrisingz-crypto/geopolitical-monitor) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON report files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the local script writes JSON reports and console summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes report files under ~/shared_memory/geopolitical by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
