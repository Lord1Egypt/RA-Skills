## Description: <br>
Command-line client for the Bank of Korea ECOS Open API to list statistic tables and fetch time series data in JSON by code and frequency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and agents use this skill to configure and run a CLI for Bank of Korea ECOS statistics, including listing statistic tables and fetching time-series JSON for downstream processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Bank of Korea ECOS API key, which can be exposed through shared logs, chats, or shell history. <br>
Mitigation: Provide BOK_API_KEY through a secure environment and avoid pasting or echoing it in commands or shared transcripts. <br>
Risk: The reviewed artifact documents CLI usage but does not include the CLI implementation for inspection. <br>
Mitigation: Inspect any repository or package before running pip install -e . and install in a virtual environment from a trusted source. <br>


## Reference(s): <br>
- [ECOS API portal](https://ecos.bok.or.kr/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands, environment variable guidance, and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides use of BOK_API_KEY and BOK_LANG; CLI responses are direct ECOS JSON passthroughs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
