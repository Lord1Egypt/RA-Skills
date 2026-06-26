## Description: <br>
Downloads structured financial data files from the airoom.ltd WordPress site for AI-agent market monitoring and strategy analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airoom-ai](https://clawhub.ai/user/airoom-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and human-supervised operators use the skill to fetch airoom.ltd financial data files into a local directory, then inspect the downloaded data for global market monitoring and strategy analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be used in workflows involving AI-directed trading or broad financial-market coordination. <br>
Mitigation: Do not connect it to brokerage accounts or automated trading; require human review before any financial action. <br>
Risk: The downloader may require credentials or retrieve files whose contents should not be trusted automatically. <br>
Mitigation: Run it in an isolated environment, use only scoped credentials, cap downloads, and inspect downloaded files before opening or using them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/airoom-ai/airoom-finance) <br>
- [airoom.ltd financial data page](http://airoom.ltd/index.php/airoom/) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Shell commands, Configuration] <br>
**Output Format:** [Downloaded data files plus plain-text console status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads are written to the configured output directory; users should cap file counts when reviewing the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
