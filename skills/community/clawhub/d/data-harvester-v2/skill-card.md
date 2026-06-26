## Description: <br>
Batch web scraping for competitor analysis, price monitoring and market research. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[windy-001-crypto](https://clawhub.ai/user/windy-001-crypto) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill as a research helper for command-line summaries around competitor comparisons, batch URL lists, sample market data, and keyword news searches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may overstate live scraping and market-data capabilities, and its stock, fund, news, or price outputs may be static or unreliable. <br>
Mitigation: Treat outputs as research assistance only; verify market, price, and news information against authoritative sources before using it for business or investment decisions. <br>
Risk: Batch mode accepts an arbitrary local file path for URL lists. <br>
Mitigation: Use batch mode only with URL-list files you intentionally created and know contain no sensitive data. <br>
Risk: Scraping workflows can create compliance or authorization issues for target websites. <br>
Mitigation: Respect robots.txt, use reasonable request intervals, and obtain appropriate authorization before commercial use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/windy-001-crypto/data-harvester-v2) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown-style command output from a Python CLI tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs with python3; batch mode reads a user-provided local URL-list file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
