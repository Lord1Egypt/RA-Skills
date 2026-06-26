## Description: <br>
Query Chinese A-share market data using BaoStock. Use when user asks for stock quotes, historical K-line, fundamentals, or market analysis. Supports real-time quotation, daily/minute data, financial reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liyico](https://clawhub.ai/user/liyico) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and finance-focused agents use this skill to query Chinese A-share quotes, historical K-line data, fundamentals, indices, and stock listings through BaoStock. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-supplied stock query fields can be converted into shell command execution. <br>
Mitigation: Replace shell-string execution with a safe argument-array subprocess call and validate query type, symbol, dates, and frequency before execution. <br>
Risk: File access and output behavior may affect paths beyond the intended skill workspace. <br>
Mitigation: Use package-relative bundled scripts and restrict reads, writes, cache, and output files to documented skill-owned paths. <br>


## Reference(s): <br>
- [BaoStock](http://baostock.com) <br>
- [ClawHub release page](https://clawhub.ai/liyico/baostock-skill) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Files] <br>
**Output Format:** [JSON objects or arrays, with optional JSON file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs stock quote, history, index, or stock-list records from BaoStock; real-time data may be delayed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
