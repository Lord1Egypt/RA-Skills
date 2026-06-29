## Description: <br>
Generates bilingual educational reference framework documents for global stocks, futures, funds, forex, and crypto markets upon explicit user request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xgs-520](https://clawhub.ai/user/xgs-520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users invoke this skill to create bilingual educational reference frameworks for market instruments across stocks, futures, funds, forex, and crypto. The outputs are intended for learning and review, not investment advice, trading signals, or autonomous financial decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Under-disclosed memory backup, conversation archiving, cloud upload, and restore behavior may move or persist user data beyond the finance-document workflow. <br>
Mitigation: Review before installing, avoid backup_cloud/all and restore modes unless explicitly needed, and restrict any cloud-drive credentials available to the skill. <br>
Risk: Market-data integrations may send requested symbols to external data providers and may require sensitive API credentials. <br>
Mitigation: Use dedicated least-privilege API keys, avoid wallet or trading credentials, and run the skill only for explicit user requests. <br>
Risk: Educational finance framework outputs may be mistaken for investment advice or trading signals. <br>
Mitigation: Keep outputs framed as educational references, require user review, and do not use generated plans for autonomous trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xgs-520/ai-xifu-caopan) <br>
- [README](artifact/README.md) <br>
- [Data configuration guide](artifact/global_market/CONFIG_GUIDE.md) <br>
- [Skill source documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Bilingual Markdown-style guidance and locally generated Word .docx documents] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs on explicit user requests, may use user-configured market data sources, and may save generated documents locally before sending them through the chat channel.] <br>

## Skill Version(s): <br>
5.4.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
