## Description: <br>
Collects global financial market, policy, company, and economic data for daily market reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szrw1825](https://clawhub.ai/user/szrw1825) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and agents preparing daily financial reports use this skill to collect market performance, policy updates, technology-company news, economic data, market-holiday status, and a qualitative global market summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is network-heavy and contacts multiple external market-data and search providers. <br>
Mitigation: Run it only in environments where those outbound requests are expected, and review provider availability, rate limits, and logs before relying on collected data. <br>
Risk: The skill requires search/API credentials such as BOCHA_API_KEY. <br>
Mitigation: Provide credentials through environment variables or a controlled secret store, and avoid embedding secrets in skill files or logs. <br>
Risk: The artifact depends on an external config.py path, output directory, and log path. <br>
Mitigation: Review and adapt the configuration paths before first use so generated reports and logs are written to approved locations. <br>
Risk: Broad trigger phrases may start local report generation and external data collection when a narrower quote lookup was intended. <br>
Mitigation: Use explicit invocation wording or add a confirmation step in deployments where simple market queries should not create files or call external providers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szrw1825/collect-market-data) <br>
- [Bocha Web Search API endpoint](https://api.bocha.cn/v1/web-search) <br>
- [FRED CSV data endpoint](https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}&limit={limit}) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON market-data file with console and log output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes market_data.json under the configured daily output directory and logs execution details to the configured log file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
