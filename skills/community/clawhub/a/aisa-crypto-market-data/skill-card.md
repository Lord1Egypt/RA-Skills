## Description: <br>
Run web, multi-source, or last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, research-ready outputs, and structured retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve and synthesize recent web and crypto market data through AIsa-backed APIs, including CoinGecko-style price, market, category, exchange, trending, and news queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes research and API requests through AIsa using AISA_API_KEY. <br>
Mitigation: Install only when that routing is approved, provide only the AISA_API_KEY required for this skill, and avoid sharing unrelated secrets. <br>
Risk: External provider responses can be incomplete, delayed, or unavailable. <br>
Mitigation: Report queried sources, provider errors, and timeouts clearly instead of implying unsupported coverage. <br>
Risk: Evidence security guidance references Twitter/X research and posting workflows even though this artifact is a crypto market data package. <br>
Mitigation: Require explicit confirmation before any public posting workflow and do not provide Twitter passwords, browser cookies, or unrelated credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/baofeng-tech/aisa-crypto-market-data) <br>
- [AIsa](https://aisa.one) <br>
- [AIsa API endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON API responses from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; external AIsa API requests may return provider errors or timeouts that should be reported honestly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
