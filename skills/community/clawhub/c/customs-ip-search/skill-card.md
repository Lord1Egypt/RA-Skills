## Description: <br>
海关知识产权备案查询 skill automates Chrome-based access to the General Administration of Customs intellectual-property record search system, checks brand record status, and returns risk assessment with logistics guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linhongbijkm-dot](https://clawhub.ai/user/linhongbijkm-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, logistics operators, and compliance reviewers can use this skill to query brand customs intellectual-property filings and summarize the resulting customs risk posture. It is intended for brand compliance screening before shipment or customs handling decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install unpinned browser automation code at runtime. <br>
Mitigation: Review the dependency before use, prefer pinned versions and hashes, and require explicit confirmation before running dependency installation. <br>
Risk: The skill opens Chrome to an external customs search site and performs online brand queries. <br>
Mitigation: Confirm the target site and query intent with the user before online access, and run searches serially as documented. <br>
Risk: The skill stores searched brands and customs results in a local CSV cache. <br>
Mitigation: Treat the CSV as local query history, limit access to the workspace, and provide a clear deletion or no-cache process for sensitive searches. <br>
Risk: The security summary flags WAF-bypass framing. <br>
Mitigation: Review the behavior before deployment and prefer revised wording and implementation that avoids bypass-oriented framing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linhongbijkm-dot/customs-ip-search) <br>
- [Customs Intellectual Property Record Search System](http://202.127.48.145:8888/zscq/search/jsp/vBrandSearchIndex.jsp) <br>
- [Google Chrome](https://www.google.com/chrome/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON command output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Caches searched brands and results in a local CSV; online refresh is used when cache entries are absent or older than seven days.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
