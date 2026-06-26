## Description: <br>
Monitors earnings calls for selected stocks, generates analyst-style earnings reports, saves them to Obsidian, updates Notion, and sends Telegram alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[realshangxinwang](https://clawhub.ai/user/realshangxinwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and agent operators use this skill to monitor a configured stock watchlist, generate concise earnings reports, and publish updates across Obsidian, Notion, and Telegram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled API keys and fixed destination identifiers could expose credentials or send data to unintended services. <br>
Mitigation: Remove bundled credentials, rotate any exposed keys, and configure Notion, Gemini, Obsidian, and Telegram destinations through user-controlled secrets before use. <br>
Risk: The skill can install packages, call external APIs, write local files through Obsidian tooling, update Notion, and send Telegram messages. <br>
Mitigation: Run it first in a limited environment and verify each external service, local path, and message target before enabling routine execution. <br>
Risk: Generated analyst reports may contain incomplete or inaccurate financial analysis. <br>
Mitigation: Review generated reports against trusted market data before using them for investment research or publishing them to a knowledge base. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/realshangxinwang/earnings-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/realshangxinwang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown earnings reports, Notion page entries, Telegram alert text, and local configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are generated per configured ticker and written to user-selected destinations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
