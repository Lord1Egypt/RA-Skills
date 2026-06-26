## Description: <br>
Teaches an AI agent to analyze trading opportunities using Chan theory thinking, including stock buy/sell point analysis, market trend review, trading psychology, strategy planning, and risk-control reasoning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenghd511](https://clawhub.ai/user/chenghd511) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Chan theory-based market analysis, including level selection, structure recognition, buy/sell point review, risk/reward assessment, and strategy drafting. The included scripts support optional market-data retrieval, CZSC structure analysis, and signal analysis for educational decision support. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading signals or strategy suggestions may be incorrect, incomplete, or unsuitable for a user's financial situation. <br>
Mitigation: Treat all analysis as informational only, verify signals independently, apply position sizing and stop-loss controls, and do not let the skill place trades. <br>
Risk: The market-data helper script accepts a Tushare token on the command line, which may expose credentials in shell history or shared environments. <br>
Mitigation: Use a private environment, avoid pasting real credentials into shared command lines, and prefer safer secret handling where available. <br>
Risk: The scripts depend on external market-data and analysis libraries, so outputs depend on data quality, library behavior, and local environment setup. <br>
Mitigation: Confirm dependency versions, validate input CSV fields, and compare generated signals against independent data and analysis before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenghd511/czsc) <br>
- [Chan theory core reference](references/chan-theory-core.md) <br>
- [Usage scenarios](examples/usage-scenarios.md) <br>
- [Script usage guide](scripts/README.md) <br>
- [waditu/czsc](https://github.com/waditu/czsc) <br>
- [CZSC documentation](https://czsc.readthedocs.io/) <br>
- [Tushare](https://tushare.pro/) <br>
- [Tushare API endpoint](https://api.tushare.pro) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, analysis, markdown, code, shell commands] <br>
**Output Format:** [Markdown with inline Python and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce stock-analysis narratives, structured trading plans, risk reminders, and optional command examples for the bundled Python scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
