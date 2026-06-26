## Description: <br>
Ai Xifu Caopan Public helps agents generate structured educational trading-analysis plans for stocks, futures, funds, and market-risk signals. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[xgs-520](https://clawhub.ai/user/xgs-520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to draft educational trading-analysis plans, market-risk summaries, and watchlist-oriented research for stocks, futures, funds, and macro market scenarios. It may fetch market data with user-provided credentials and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global; users are responsible for complying with local financial-services and trading regulations. <br>

## Known Risks and Mitigations: <br>
Risk: Generated finance and trading analysis can be incorrect, incomplete, or misleading. <br>
Mitigation: Treat all output as unverified educational material, verify market data independently, and consult a licensed financial professional before making trading decisions. <br>
Risk: The skill may use configured market-data credentials and execute local helper scripts. <br>
Mitigation: Review and restrict environment variables before running the skill, use only trusted market-data credentials, and run helper scripts in a controlled workspace. <br>
Risk: The skill can create local DOCX, watchlist, and tracking files. <br>
Mitigation: Confirm file writes before allowing them, review generated files before sharing, and clear watchlist or tracker data when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xgs-520/ai-xifu-caopan-public) <br>
- [Tushare API](https://tushare.pro) <br>
- [Guosen Securities](https://www.guosen.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance, console text or JSON from helper scripts, and generated DOCX trading-plan files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided market-data credentials for some data sources and may create local DOCX, watchlist, and tracker files after user confirmation.] <br>

## Skill Version(s): <br>
5.3.7 (source: server release evidence, skill.json, package.json, and SKILL.md changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
