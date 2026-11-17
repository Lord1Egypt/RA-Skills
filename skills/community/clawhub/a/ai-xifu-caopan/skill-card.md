## Description: <br>
Generates bilingual educational reference framework documents for global stocks, futures, funds, forex, and crypto markets upon explicit user request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xgs-520](https://clawhub.ai/user/xgs-520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to generate bilingual educational reference documents for requested market symbols across stocks, futures, funds, forex, and crypto. Developers or operators configure market data sources and API credentials when real market data is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A bundled memory bridge script can back up chat history, profile files, and generated documents, and can upload archives to cloud storage. <br>
Mitigation: Review or remove scripts/memory_bridge_v2.py before installation; do not run backup_cloud or all modes unless cloud transfer is explicitly intended. <br>
Risk: Market data integrations can expose requested symbols and may rely on sensitive API credentials. <br>
Mitigation: Use scoped, rotatable API keys and confirm which external data sources are enabled before generating market-data-backed outputs. <br>
Risk: Generated market frameworks may be mistaken for actionable financial advice. <br>
Mitigation: Treat outputs as educational drafts, verify market data independently, and avoid using generated plans as trading instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xgs-520/ai-xifu-caopan) <br>
- [Data Configuration Guide](global_market/CONFIG_GUIDE.md) <br>
- [Skill README](README.md) <br>
- [Skill Instructions](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Bilingual Word .docx documents with supporting Markdown templates and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user request; real market data may require user-configured APIs or external data sources.] <br>

## Skill Version(s): <br>
5.4.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
