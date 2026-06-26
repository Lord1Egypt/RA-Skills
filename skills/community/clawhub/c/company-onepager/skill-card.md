## Description: <br>
Generates a one-page public-company research brief with company basics, market data, ten-year financial tables, ten-year monthly price charts, shareholder structure, recent news, and source labels for each section. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laigen](https://clawhub.ai/user/laigen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and financial research workflows use this skill to assemble a concise stock or company brief from iFinD, Tushare, AkShare, and web-search-assisted source material. It is intended for generating Markdown and PDF one-pagers for company research, not for making investment decisions without review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles finance API credentials while one remote request disables TLS certificate verification. <br>
Mitigation: Use isolated, revocable finance API tokens and remove or fix disabled TLS verification before sending iFinD credentials. <br>
Risk: The skill imports code from another local skill path, which can execute unexpected local code. <br>
Mitigation: Inspect or disable the hard-coded local brave-search import before installing or running the skill. <br>
Risk: The skill can process confidential watchlists through web search and remote font requests. <br>
Mitigation: Run in an environment where web search and remote font access are acceptable, or disable those features for confidential inputs. <br>


## Reference(s): <br>
- [Data Sources and Field Mapping](references/data_sources.md) <br>
- [Tushare](https://tushare.pro) <br>
- [Company Onepager on ClawHub](https://clawhub.ai/laigen/company-onepager) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown report, PDF file, chart image, JSON data file, and console summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a stock code input and finance data credentials for the higher-priority data sources.] <br>

## Skill Version(s): <br>
7.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
