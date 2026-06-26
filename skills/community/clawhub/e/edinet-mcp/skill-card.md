## Description: <br>
Analyze and compare Japanese public company financial statements from EDINET using company names or stock codes with J-GAAP, IFRS, and US-GAAP data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajtgjmdjp](https://clawhub.ai/user/ajtgjmdjp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and finance teams use this skill to guide EDINET CLI workflows for finding Japanese public-company filings, extracting BS/PL/CF statements, comparing periods, and screening companies by financial metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires an EDINET-specific API key. <br>
Mitigation: Use a dedicated EDINET key where possible and avoid running the tool in environments that expose unrelated credentials. <br>
Risk: EDINET requests are rate-limited and large company screens can take time. <br>
Mitigation: Keep screening batches within the documented maximum of 20 companies and account for the default 0.5 requests-per-second rate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ajtgjmdjp/edinet-mcp) <br>
- [EDINET API key registration](https://disclosure2dl.edinet-fsa.go.jp/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and CLI option guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EDINET_API_KEY and the edinet-mcp CLI; CLI results may be JSON or CSV depending on command options.] <br>

## Skill Version(s): <br>
0.6.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
